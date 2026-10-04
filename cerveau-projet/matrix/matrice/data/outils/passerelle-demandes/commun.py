"""Fonctions communes de l'outil passerelle-demandes : une seule tache chacune.

LE DRY/WET, ET POURQUOI IL EST ICI (demande createur 2026-09-30).
Deposer 35 items d'un coup est irreversible dans les faits : un id est consomme,
un item apparait dans l entonnoir du createur. Le DRY prepare et MONTRE, le WET
ecrit. Ce n est pas une commodite : c est la seule facon de voir ce qu on va
deposer avant de l avoir depose. Le WET n est pas un mode cache -- il appelle
lui-meme la meme preparation, et dit ce qu il a fait.

UNE DEMANDE SANS TYPE N EST PAS DEPOSEE.
Le crochet du user dit l intention. La table de traduction vit dans les
constantes, entiere et lisible. Un crochet INCONNU ne devine pas : la demande
est DITEE et laissee au canal. Deposer sous un type choisi a la place du createur
serait une decision prise a son detriment, et il la decouvrirait dans son
entonnoir sans savoir pourquoi.
"""
import io
import json
import subprocess
import sys

from constants import (
    APPELANT,
    CHEMIN_CANAL,
    CHEMIN_ENTONNOIR,
    CROCHETS_TYPES,
    ENCODAGE,
    LANCEUR,
    NOM_ENTONNOIR_BRIQUE,
    MOTIF_TRACE,
    PREFIXE_TRACE,
    SOURCE_ENTONNOIR,
    VERBE_DEPOT,
)
import passerelle_user as P

# LA CORRECTION ASCII (demande createur 2026-09-30). Le canal est ecrit en
# francais accentue ; la Matrice est 100 % ASCII. Sans cette conversion, un item
# depose emporte ses accents -- mesure : 35 items sur 35 en portaient.
# La conversion se fait AU DEPOT, sur le TEXTE prepare, et par la FONCTION du
# domicile unique (carte_ascii) : ni table, ni regle recopiees ici. Le chemin
# est deja pose par constants (CIRCUIT).
from carte_ascii import convertir_texte  # noqa: E402


def normaliser(texte):
    """La CLEF de comparaison d une demande -- la REGLE est au DOMICILE COMMUN.

    On ne garde ici que le NOM : `passerelle_user.normaliser` en est le
    domicile unique, consomme par les DEUX chemins qui deposent une demande
    (M-076). Une regle copiee dans l outil diverge de celle du voisin le jour
    ou l un des deux evolue -- et c est exactement ce qui etait arrive (EO-538 :
    le chemin du pilote n avait pas de reconnaissance du tout).
    """
    return P.normaliser(texte)


def indexer_entonnoir():
    """(par_trace, par_theme) -- les items DEJA deposes, lus en lecture seule.

    La trace est la reconnaissance EXACTE : elle porte le numero de ligne de la
    demande dans le canal, et survit a une reecriture du texte par le createur.
    Le theme est le REPLI, pour les items deposes avant que la trace existe. Un
    repli n est jamais presente comme une preuve : `deja_deposee` dit par quel
    niveau il a reconnu.
    """
    par_trace = {}
    par_theme = {}
    try:
        donnees = json.loads(io.open(str(CHEMIN_ENTONNOIR), encoding=ENCODAGE).read())
    except (OSError, ValueError) as erreur:
        raise RuntimeError("l etat de l entonnoir est ILLISIBLE : "
                           + str(CHEMIN_ENTONNOIR) + " -- " + str(erreur))
    for items in donnees.get("files", {}).values():
        for item in items:
            identifiant = str(item.get("id", ""))
            marqueur = trace_de_l_item(item)
            if marqueur:
                par_trace[marqueur] = identifiant
            par_theme.setdefault(normaliser(item.get("theme", "")), identifiant)
    return par_trace, par_theme


def trace_de_l_item(item):
    """La ligne de canal portee par la trace d un item, ou "" (trace absente)."""
    for champ in ("trace", "motif", "source"):
        valeur = str(item.get(champ, ""))
        if valeur.startswith(PREFIXE_TRACE + " "):
            return valeur[len(PREFIXE_TRACE) + 1:].strip()
    return ""


def deja_deposee(demande, par_trace, par_theme):
    """("trace"|"texte", id) si la demande est deja la, ("", "") sinon.

    On rend le NIVEAU de la reconnaissance : une trace est une preuve, une
    correspondance de texte est une deduction. L appelant l affiche, donc le
    createur sait sur quoi repose son saut.
    """
    marqueur = PREFIXE_TRACE + " l." + str(demande["ligne"])
    if marqueur in par_trace:
        return "trace", par_trace[marqueur]
    identifiant = par_theme.get(normaliser(demande["theme"]), "")
    if identifiant:
        return "texte", identifiant
    return "", ""


def lire_canal(chemin=None):
    """Le TEXTE du canal, ou None s il est illisible (le motif se DIT)."""
    cible = chemin or CHEMIN_CANAL
    try:
        return io.open(str(cible), encoding=ENCODAGE).read()
    except (OSError, UnicodeDecodeError):
        return None


def decouper(texte):
    """(entete, demandes, anomalies) -- lu au DOMICILE partage, jamais recopie."""
    return P.decouper_demandes(texte)


def type_pour(crochet):
    """Le TYPE d un crochet du user, ou "" si la table ne le parle pas.

    La casse est normalisee : `[MISSION]` et `[mission` veulent dire la meme
    chose, et le choix de la casse appartient au user, pas a la Matrice.
    """
    if not crochet:
        return ""
    nu = crochet.strip().lower()
    if nu.startswith("[") and nu.endswith("]"):
        nu = nu[1:-1].strip()
    return CROCHETS_TYPES.get(nu, "")


def titre_de(demande):
    """Le TITRE de l item : le crochet retire -- la REGLE est au DOMICILE COMMUN.

    Les mots du user ne sont jamais reecrits. On garde ici le NOM seul : la
    regle vit dans `passerelle_user.titre_sans_crochet`, consommee par les deux
    chemins (M-076). C est cette regle qui manquait au second chemin, et c est
    pour cela que sa reconnaissance ne mordait pas (EO-538).
    """
    return P.titre_sans_crochet(demande.get("titre", ""),
                                demande.get("crochet", ""))


def preparer(texte=None):
    """Prepare le DEPOT : (deposes, retenues, anomalies, deja_deposees).

    `deposes`        : ce qui serait depose (theme, objectif, type, ligne)
    `retenues`       : les demandes qu on refuse de deviner, avec la raison
    `anomalies`      : ce que l extraction a DIT (bloc vide, mot d etat inconnu)
    `deja_deposees`  : (ligne, niveau, id) -- deja dans l entonnoir, SAUTEES

    Le dernier est la raison d etre de l outil : sans lui, un second `deposer`
    recreerait 35 items fantomes dans l entonnoir du createur.
    """
    if texte is None:
        par_trace, par_theme = indexer_entonnoir()
    else:
        par_trace, par_theme = {}, {}
    source = texte if texte is not None else lire_canal()
    if source is None:
        return [], [], ["le canal est ILLISIBLE : " + str(CHEMIN_CANAL)], []
    entete, demandes, anomalies = decouper(source)
    deposes = []
    retenues = []
    deja_deposees = []
    for demande in demandes:
        type_cible = type_pour(demande.get("crochet", ""))
        if not type_cible:
            retenues.append(
                (demande.get("ligne_debut", 0),
                 demande.get("crochet") or "(aucun crochet)",
                 "aucun type pour ce crochet : la demande n est PAS devinee")
            )
            continue
        titre = titre_de(demande)
        if not titre:
            retenues.append((demande.get("ligne_debut", 0),
                             demande.get("crochet") or "(vide)",
                             "titre vide : rien a deposer"))
            continue
        theme_propre, theme_perdus = convertir_texte(titre)
        objectif_propre, objectif_perdus = convertir_texte(
            demande.get("texte", "").strip())
        perdus = sorted(set(theme_perdus) | set(objectif_perdus))
        if perdus:
            anomalies.append("l." + str(demande.get("ligne_debut", 0))
                             + " : caracteres NON convertis (conserves tels quels) : "
                             + " ".join("U+" + format(ord(c), "04X") for c in perdus))
        item = {
            "theme": theme_propre,
            "objectif": objectif_propre,
            "type": type_cible,
            "crochet": demande.get("crochet", ""),
            "ligne": demande.get("ligne_debut", 0),
            # L AVANCEMENT (MO-561) : deduit du bloc de patterns, jamais pose a la
            # main. Il part AVEC l item -- sans lui l entonnoir classerait des
            # demandes sans savoir lesquelles attendaient depuis des semaines.
            "avancement": P.avancement_de(demande),
        }
        # LE GARDE. Il porte sur l item PREPARE, dont le theme est deja ASCII :
        # une reconnaissance faite avant la conversion serait aveugle exactement
        # sur les items accentues -- et la mesure le prouve (13 non reconnus,
        # 13 items jamais corriges).
        niveau, identifiant = deja_deposee(item, par_trace, par_theme)
        if identifiant:
            deja_deposees.append((item["ligne"], niveau, identifiant, item["theme"]))
            continue
        deposes.append(item)
    return deposes, retenues, anomalies, deja_deposees


def deposer_un(item):
    """Depose UN item par la PORTE. Rend (code, sortie).

    Jamais d ecriture directe de l etat de l entonnoir : la porte classe
    l item, pose son role et son avis d auto-validation. Un item ecrit a la
    main n aurait aucun de ces trois -- ce serait un fantome dans la file du
    createur, sans trace et sans conduite.
    """
    commande = [
        sys.executable, LANCEUR, "--appelant", APPELANT,
        NOM_ENTONNOIR_BRIQUE, VERBE_DEPOT,
        "--theme", item["theme"],
        "--objectif", item["objectif"] or item["theme"],
        "--type", item["type"],
        "--source", SOURCE_ENTONNOIR,
        # L AVANCEMENT (MO-561) : la porte le REFUSE s il est hors liste, donc une
        # valeur deduite du bloc ne peut pas passer en FORCE -- elle est ou bien
        # conforme, ou bien le depot echoue en le disant.
        "--avancement", item["avancement"],
        # LA TRACE PORTE LA LIGNE DE CANAL. C est la preuve du depot, et la
        # clef de reconnaissance du prochain passage : un item qui sait d ou il
        # vient ne peut pas etre depose deux fois.
        "--trace", PREFIXE_TRACE + " l." + str(item["ligne"]) + " | " + MOTIF_TRACE,
    ]
    resultat = subprocess.run([str(part) for part in commande],
                              capture_output=True, text=True, encoding=ENCODAGE,
                              errors="replace")
    return resultat.returncode, (resultat.stdout or "") + (resultat.stderr or "")


def afficher_preparation(deposes, retenues, anomalies, deja_deposees=(), prefixe="  "):
    """Rend la preparation, lisible. Utilise par le DRY comme par le WET."""
    lignes = []
    if deja_deposees:
        lignes.append(prefixe + "DEJA DANS L ENTONNOIR -- " + str(len(deja_deposees))
                      + " demande(s) SAUTEE(S), rien ne sera re-depose :")
        for ligne, niveau, identifiant, theme in deja_deposees:
            portee = "trace" if niveau == "trace" else "texte (repli)"
            lignes.append(prefixe + "  l." + str(ligne).rjust(4) + " deja "
                          + str(identifiant).ljust(8) + " reconnu par "
                          + portee.ljust(15) + " " + theme[:52])
    for anomalie in anomalies:
        lignes.append(prefixe + "ANOMALIE : " + anomalie)
    for ligne, crochet, raison in retenues:
        lignes.append(prefixe + "RETENUE (ligne " + str(ligne) + ") " + crochet
                      + " : " + raison)
    par_type = {}
    for item in deposes:
        par_type.setdefault(item["type"], []).append(item)
    for type_cible in sorted(par_type):
        lignes.append(prefixe + type_cible.ljust(12) + " : "
                      + str(len(par_type[type_cible])) + " item(s)")
    lignes.append(prefixe + "-" * 56)
    for item in deposes:
        lignes.append(prefixe + "l." + str(item["ligne"]).rjust(4) + " "
                      + item["type"].ljust(10) + " " + item["theme"][:86])
    lignes.append(prefixe + "-" * 56)
    lignes.append(prefixe + "TOTAL a deposer : " + str(len(deposes))
                  + " | retenues : " + str(len(retenues))
                  + " | anomalies : " + str(len(anomalies)))
    return lignes
