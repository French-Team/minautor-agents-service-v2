"""Fonctions de la porte `passerelle` : une seule tache chacune.

DEUX GESTES, et le premier ne peut rien casser :
  - `diagnostiquer` LIT le canal et DIT tout (head, demandes, etats, crochets,
    anomalies) -- AUCUNE ecriture ;
  - `extraire` DEPOSE un item par la porte de l entonnoir, ARCHIVE les mots exacts
    du user dans le journal du canal, puis RETIRE la demande du canal.
DRY PAR DEFAUT : sans `--appliquer`, `extraire` ne fait que DIRE ce qu il ferait.
Le canal est ecrit par le user EN CONTINU : une porte qui ecrit sans le dire
serait la pire des portes.
"""
import re
import subprocess
import sys
from datetime import datetime

from passerelle.constants import (
    CHEMIN_CANAL,
    CHEMIN_JOURNAL,
    CHEMIN_ENTONNOIR_MAIN,
    CHEMIN_ENTONNOIR,
    ETAT_SERVABLE,
    LARGEUR_TITRE,
    MARQUE_SOURCE,
    convertir_texte,
)
import json  # local : l index du garde lit l entonnoir
import passerelle_user as P  # le domicile commun, une seule fois
from passerelle_user import (
    decouper_demandes,
    retirer_demande,
    reconnaitre_demande,
    titre_sans_crochet,
)

# L IDENTIFIANT SE LIT SUR LA LIGNE QUE LA PORTE ECRIT (mesure du 2026-09-29) : la
# sortie d un depot porte AUSSI les items PROCHES (le verdict de DOUBLON POSSIBLE
# les NOMME). Un `search` du motif large rendait donc le PREMIER id cite -- mesure
# reelle : la demande du user a ete archivee sous EO-476 alors que l entonnoir
# venait d attribuer EO-482, c est-a-dire sous l item d un AUTRE. Ancre sur la
# ligne, et la sortie se DIT au lieu d etre avalee.
MOTIF_ITEM = re.compile(r"^Mission (EO-\d+)", re.MULTILINE)
MOTIF_LIGNE_ITEM = re.compile(r"^Mission EO-\d+", re.MULTILINE)


def lire_canal():
    """Le TEXTE du canal, ou None s il est absent (jamais une exception).

    LES FINS DE LIGNE SONT PRESERVEES, octet pour octet (exigence 4 de la mission,
    mesure du 2026-09-29). Le canal est ecrit par le user EN CONTINU : une lecture
    qui TRADUIT ses fins de ligne (le comportement par defaut de `read_text`)
    reecrit TOUT le fichier au premier retrait. Mesure reelle : un canal cobaye en
    CRLF (18 fins CRLF) ressortait en LF (0 fin CRLF) -- un fichier ENTIEREMENT
    modifie pour UNE demande retiree. On lit donc SANS traduction ; l ecriture
    (`ecrire_canal`) ne traduit pas non plus : ce qui entre ressort identique.
    """
    if not CHEMIN_CANAL.is_file():
        return None
    with open(str(CHEMIN_CANAL), "r", encoding="utf-8", newline="") as flux:
        return flux.read()


def repartition(valeurs):
    """[(valeur, nombre)] trie par nombre DECROISSANT -- la meme forme partout."""
    comptes = {}
    for valeur in valeurs:
        comptes[valeur] = comptes.get(valeur, 0) + 1
    return sorted(comptes.items(), key=lambda couple: (-couple[1], couple[0]))


def en_ligne(couples):
    """Un resume compact : <etiquette nombre, etiquette nombre>."""
    return ", ".join(etiquette + " " + str(nombre) for etiquette, nombre in couples)


def diagnostiquer(arguments=None):
    """LIT le canal et DIT tout. AUCUNE ecriture, quoi qu il arrive."""
    texte = lire_canal()
    if texte is None:
        print("REFUS : le canal est INTROUVABLE : " + str(CHEMIN_CANAL))
        return 2
    entete, demandes, anomalies = decouper_demandes(texte)
    servables = [d for d in demandes if d["etat"] == ETAT_SERVABLE]
    print("CANAL : " + str(CHEMIN_CANAL))
    print("  head : " + str(len(entete)) + " ligne(s) -- les mots du user ne sont pas juges ici")
    print("  demandes : " + str(len(demandes)) + " dont " + str(len(servables))
          + " a l etat " + ETAT_SERVABLE + " (extractibles)")
    print("  etats : " + en_ligne(repartition([d["etat"] or "(VIDE)" for d in demandes])))
    print("  crochets : " + en_ligne(repartition([d["crochet"] or "(aucun)" for d in demandes])))
    for rang, demande in enumerate(demandes, 1):
        marque = "*" if demande["etat"] == ETAT_SERVABLE else " "
        print("  " + marque + str(rang).rjust(3) + ". [" + (demande["etat"] or "VIDE") + "] "
              + (demande["crochet"] or "(sans crochet)") + " L" + str(demande["ligne_debut"])
              + "-" + str(demande["ligne_fin"]) + " : "
              + demande["titre"][:LARGEUR_TITRE])
    print("  anomalies : " + (str(len(anomalies)) if anomalies else "aucune"))
    for anomalie in anomalies:
        print("    [!] " + anomalie)
    print("  (* = extractible. RIEN n a ete ecrit : ce verbe ne fait que lire.)")
    return 0


def texte_pour_la_matrice(demande):
    """L item porte une TRANSCRIPTION ASCII des mots du user (la Matrice est ASCII).

    Les mots EXACTS ne sont pas perdus : ils partent au journal d extraction AVANT
    le retrait, et le canal est suivi par git. La transcription est DITE a chaque
    extraction -- jamais silencieuse.
    """
    brut = demande["texte"]
    transpose, non_convertibles = convertir_texte(brut)
    return transpose, non_convertibles, transpose != brut


def journaliser(demande, item, horodatage):
    """CONSERVE les mots EXACTS de la demande extraite, dans le journal du canal.

    Le journal vit dans la zone du canal : ses accents, ses apostrophes et ses
    crochets y sont legitimes (exemption declaree a son domicile). C est la MEMOIRE
    des mots du user -- l item, lui, porte leur transcription.
    """
    entete = ("\n---\n\n## Demande extraite vers " + item + " (" + horodatage + ")\n\n"
              "Etiquette : " + (demande["crochet"] or "(aucun crochet)")
              + " | etat " + (demande["etat"] or "VIDE")
              + " | bloc L" + str(demande["ligne_debut"]) + "-" + str(demande["ligne_fin"]) + "\n\n")
    CHEMIN_JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    with open(str(CHEMIN_JOURNAL), "a", encoding="utf-8", newline="\n") as flux:
        flux.write(entete + "~~~~\n" + demande["texte"] + "\n~~~~\n")


def ecrire_canal(texte):
    """Reecrit le canal ATOMIQUEMENT (tmp + remplacement) -- jamais en place.

    AUCUN `.bak` n est laisse DANS le canal : mesure du 2026-09-29 (MO-504), la
    porte ECRIRE y deposait une copie des mots du user, dans son propre dossier.
    Ici les filets sont ailleurs : le journal d extraction et git.
    """
    temporaire = CHEMIN_CANAL.with_name(CHEMIN_CANAL.name + ".tmp")
    with open(str(temporaire), "w", encoding="utf-8", newline="") as flux:
        flux.write(texte)
    temporaire.replace(CHEMIN_CANAL)


def item_de_sortie(sortie):
    """L IDENTIFIANT attribue par la porte de l entonnoir, lu DANS SA SORTIE.

    POURQUOI une fonction NOMMEE (mesure du 2026-09-29) : la sortie d un depot
    porte AUSSI les items PROCHES -- le verdict de DOUBLON POSSIBLE les NOMME. Un
    `search` du motif large rendait donc le PREMIER id cite ; mesure reelle : la
    demande du user a ete archivee sous EO-476 alors que l entonnoir venait
    d attribuer EO-482, c est-a-dire sous l item d un AUTRE. L identifiant se lit
    sur la LIGNE D ITEM (`Mission EO-XXX ...`), et nulle part ailleurs : pas de
    ligne d item = aucun identifiant (et rien ne quitte le canal).
    """
    trouve = MOTIF_ITEM.search(sortie or "")
    return trouve.group(1) if trouve else ""


def dire_sortie_entonnoir(sortie, masquer_item=False):
    """DIT ce que la porte de l entonnoir a DIT, hors la ligne qui donne l id.

    POURQUOI (mesure du 2026-09-29) : la sortie d un depot porte le verdict de
    DOUBLON POSSIBLE (les items proches, nommes) et le geste exact qui sort
    l item du vrac. Les taire, c est taire un doute -- et c est precisement ce
    silence qui a laisse passer un identifiant faux.
    """
    for ligne in (sortie or "").splitlines():
        if not ligne.strip():
            continue
        if masquer_item and MOTIF_LIGNE_ITEM.match(ligne):
            continue
        print("    " + ligne)


def deposer_item(demande, horodatage):
    """DEPOSE l item par la porte de l ENTONNOIR (jamais une ecriture directe).

    Rend (code, item, sortie) : l item est lu dans la SORTIE de la porte -- c est
    elle qui l attribue, la porte n invente pas un identifiant. Il se lit sur la
    LIGNE D ITEM (`Mission EO-XXX ...`), jamais au premier motif venu : la meme
    sortie nomme les items proches, et les confondre archiverait les mots du user
    sous l item d un AUTRE (mesure du 2026-09-29, mo-505).
    """
    transpose, non_convertibles, transpose_est_differente = texte_pour_la_matrice(demande)
    objectif = transpose
    if transpose_est_differente:
        objectif += ("\n\n[TRANSCRIPTION ASCII : les mots EXACTS du user sont au journal "
                     "du canal (" + str(CHEMIN_JOURNAL) + ") et dans git. Caracteres non "
                     "convertibles : " + (", ".join(sorted(non_convertibles)) or "aucun") + "]")
    objectif += ("\n\n[Source : " + MARQUE_SOURCE + " " + str(CHEMIN_CANAL.name)
                 + ", demande des lignes " + str(demande["ligne_debut"]) + " a "
                 + str(demande["ligne_fin"]) + ", etat " + (demande["etat"] or "VIDE")
                 + ", crochet " + (demande["crochet"] or "aucun")
                 + " -- extraite le " + horodatage + "]")
    commande = [sys.executable, str(CHEMIN_ENTONNOIR_MAIN), "deposer",
                "--theme", transpose.split("\n")[0][:LARGEUR_TITRE] or "Demande de la passerelle",
                "--objectif", objectif,
                "--trace", MARQUE_SOURCE + " " + str(CHEMIN_CANAL.name) + " L"
                + str(demande["ligne_debut"])]
    resultat = subprocess.run(commande, capture_output=True, text=True)
    sortie = (resultat.stdout or "") + (resultat.stderr or "")
    return resultat.returncode, item_de_sortie(sortie), sortie


def extraire(arguments):
    """DEPOSE les items, ARCHIVE les mots exacts, RETIRE les demandes du canal.

    Options : `--rang N` (une demande precise, 1 = la premiere), `--tout` (toutes
    les demandes servables), `--appliquer` (ECRIRE : sans lui, RIEN n est ecrit).
    Le code rendu dit le fait : 0 = fait, 1 = rien a faire, 2 = refus.
    """
    appliquer = "--appliquer" in arguments
    tout = "--tout" in arguments
    rang_vise = None
    if "--rang" in arguments:
        position = arguments.index("--rang")
        if position + 1 < len(arguments):
            rang_vise = arguments[position + 1]

    texte = lire_canal()
    if texte is None:
        print("REFUS : le canal est INTROUVABLE : " + str(CHEMIN_CANAL))
        return 2

    lignes = texte.split("\n")
    entete, demandes, anomalies = decouper_demandes(texte)
    if anomalies:
        for anomalie in anomalies:
            print("  [!] " + anomalie)
    servables = [rang for rang, demande in enumerate(demandes)
                 if demande["etat"] == ETAT_SERVABLE]
    if not servables:
        print("RIEN A EXTRAIRE : aucune demande a l etat " + ETAT_SERVABLE + ".")
        return 1

    if rang_vise is not None:
        if not rang_vise.isdigit() or not (1 <= int(rang_vise) <= len(demandes)):
            print("REFUS : --rang attendu entre 1 et " + str(len(demandes))
                  + " (recu : " + str(rang_vise) + ").")
            return 2
        choisis = [int(rang_vise) - 1]
        if choisis[0] not in servables:
            print("REFUS : la demande " + rang_vise + " est a l etat "
                  + demandes[choisis[0]]["etat"] + " -- seul " + ETAT_SERVABLE
                  + " s extrait (l etat se SUIT, il ne se saute pas).")
            return 2
    else:
        choisis = servables if tout else servables[:1]

    # LES DEUX JUGES DU GARDE. `indexer` lit l entonnoir en LECTURE SEULE et
    # rend ses deux tables ; `reconnaitre` applique le juge du DOMICILE COMMUN.
    # Elles ne sont appelees qu au moment d ecrire : au DRY, rien n est lu.
    def indexer():
        """(par_trace, par_theme) -- les items deja deposes, lus en lecture seule."""
        par_trace, par_theme = {}, {}
        chemin = CHEMIN_ENTONNOIR
        try:
            donnees = json.loads(chemin.read_text(encoding="utf-8"))
        except (OSError, ValueError) as erreur:
            print("  [i] l entonnoir est illisible (" + type(erreur).__name__
                  + ") : le garde ne peut rien reconnaitre, et le dit.")
            return par_trace, par_theme
        fichiers = donnees.get("files") or {}
        collections = [fichiers.get(nom, []) or [] for nom in fichiers]
        collections.append(donnees.get("brin") or [])
        collections.append(donnees.get("vrac") or [])
        for items in collections:
            for item in items:
                identifiant = str(item.get("id", ""))
                if not identifiant:
                    continue
                for morceau in str(item.get("trace", "") or "").split(";"):
                    if "canal l." in morceau:
                        par_trace[morceau.strip()] = identifiant
                par_theme.setdefault(P.normaliser(item.get("theme", "")),
                                     identifiant)
        return par_trace, par_theme

    def reconnaitre(demande, index):
        """Le couple (niveau, id) si deja servie, sinon ("", "")."""
        return reconnaitre_demande(
            titre_sans_crochet(demande.get("titre", ""),
                               demande.get("crochet", "")),
            demande.get("ligne_debut", 0), index[0], index[1])

    index = indexer()
    if index[0] or index[1]:
        print("  garde : " + str(len(index[1])) + " item(s) deja"
              " servi(s) reconnu(s) -- une demande deja servie ne sera"
              " pas deposee une seconde fois.")
    print("EXTRACTION" + ("" if appliquer else " (DRY -- RIEN n est ecrit)")
          + " : " + str(len(choisis)) + " demande(s) sur " + str(len(servables)) + " servable(s).")
    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    retirees = []
    retenues = 0
    for rang in choisis:
        demande = demandes[rang]
        print("  " + str(rang + 1) + ". " + (demande["crochet"] or "(sans crochet)") + " : "
              + demande["titre"][:LARGEUR_TITRE])
        # LE GARDE (EO-538) : une demande deja servie n est pas deposee une
        # seconde fois. Il joue AVANT le depot -- rien n est ecrit -- et la
        # demande RESTE au canal : un refus ne retire jamais une ligne.
        # Il joue AVANT meme la sortie DRY : un apercu qui cache un refus fait
        # croire que le geste aboutirait, et il ne dit rien de la reconnaissance
        # qu il a pourtant faite.
        niveau, deja = reconnaitre(demande, index)
        if deja:
            print("    REFUS DOUBLON -- la demande " + str(rang + 1)
                  + " est deja servie par " + deja + " (reconnue " + niveau
                  + ") : elle ne sera pas deposee deux fois, et elle RESTE"
                  " au canal." + ("" if appliquer else " (DRY : rien ne sera ecrit)"))
            retenues += 1
            continue
        if not appliquer:
            continue
        code, item, sortie = deposer_item(demande, horodatage)
        if code != 0 or not item:
            print("    REFUS de l entonnoir (code " + str(code) + ") : rien n est retire"
                  " -- une demande qui n a PAS d item ne quitte pas le canal.")
            if not item:
                print("    (sa sortie ne portait AUCUNE ligne d item : les mots du user"
                      " restent au canal, intacts.)")
            dire_sortie_entonnoir(sortie)
            continue
        dire_sortie_entonnoir(sortie, masquer_item=True)
        journaliser(demande, item, horodatage)
        retirees.append(rang)
        print("    item " + item + " depose ; les mots EXACTS sont au journal du canal.")


    if not appliquer:
        print("  Pour ecrire : ajouter --appliquer.")
        return 0

    if retenues:
        print("  " + str(retenues) + " demande(s) REFUSEE(S) comme deja"
              " servie(s) : elles restent au canal, mot pour mot.")
    if not retirees:
        print("AUCUN retrait : le canal est INTACT.")
        return 1
    for rang in sorted(retirees, reverse=True):
        _, a_jour, _ = decouper_demandes("\n".join(lignes))
        lignes = retirer_demande(lignes, a_jour, rang)
    ecrire_canal("\n".join(lignes))
    _, restantes, _ = decouper_demandes("\n".join(lignes))
    print("  canal : " + str(len(restantes)) + " demande(s) restante(s) ; "
          + str(len(retirees)) + " retiree(s) du canal, archivee(s) au journal.")
    return 0
