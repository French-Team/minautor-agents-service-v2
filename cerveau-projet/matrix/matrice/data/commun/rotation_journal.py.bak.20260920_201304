"""MOTIF UNIQUE de rotation d'un journal de la Matrice (M-076 : jamais recopie).

Un journal en AJOUT SEUL ne se supprime jamais : le borner, c'est DEPLACER ses
evenements les plus anciens dans une archive DATEE. Ce module est le moteur
PARTAGE -- les routines l'utilisent avec LEURS constantes (seuil, gardes,
prefixe d'archive), elles ne le recopient pas (lecon L-029 : un moteur recopie
quatre fois diverge quatre fois).

Trois invariants portent la surete (lecon L-040 et mesures MO-077) :

  1. ARCHIVER D'ABORD, reecrire ensuite : si l'archive echoue, le journal n'a pas
     ete touche ; si la reecriture echoue, l'archive contient deja tout.
  2. L'ARCHIVE EST DANS LE "DEJA CONNU" : une rotation qui ignore ce qu'elle a
     deja deplace se reecrit des jumeaux au passage suivant -- elle s'annule
     toute seule, en silence, apres que tout a ete verifie.
  3. UNE COURSE SE REFUSE, ELLE NE S'ECRASE PAS : la boucle et les appels a la
     demande ecrivent dans le journal ligne par ligne. Si la taille a bouge entre
     la lecture et le remplacement, on recommence (le journal n'est pas touche),
     et on REFUSE en le nommant si ca bouge encore.

Le module fournit aussi la lecture BORNEE de la queue d'un journal : une
surveillance se lit dans les DERNIERS evenements, jamais dans tout l'historique.

Ce module est PARTAGE (data/commun) : son nom ne doit jamais etre celui d'une
categorie importable d'un pilote ou d'une routine (lecon L-029). Il ne fait
AUCUNE hypothese sur le format des lignes : une ligne est une chaine, ce qui
marche pour un .jsonl comme pour un journal texte.
"""
import argparse
import ast
import json
import os
import re
from datetime import datetime
from pathlib import Path

ENCODAGE = "utf-8"

# --- FENETRE DE LECTURE D'UNE QUEUE (MO-099) --------------------------------
# La lecture d'une queue est BORNEE : une surveillance lit les DERNIERS
# evenements, jamais tout l'historique. Le nombre 256 Ko vivait RECOPIE dans
# onze fichiers (aucune valeur en dur dans la logique ? non : onze), alors que
# chaque journal DECLARE sa propre borne de rotation (`SEUIL_OCTETS_JOURNAL` :
# 2 Mo pour la veille, 8 Mo pour l'espion, 512 Ko pour les vigies) -- c'est le
# motif L-029 applique a une VALEUR. Regle unique, ici, et nulle part ailleurs :
#
#   la fenetre n'est JAMAIS plus petite que la borne DECLAREE du journal lu ;
#   sinon une rotation pourrait CACHER au lecteur des evenements qu'elle garde.
#
# Un lecteur qui n'a AUCUNE borne declaree (cobaye, journal etranger) garde le
# PLANCHER : la surveillance ne balaie jamais un fichier entier par accident.
OCTETS_QUEUE_PLANCHER = 256 * 1024
NOM_CONSTANTE_BORNE = "SEUIL_OCTETS_JOURNAL"
# Une declaration d'une seule ligne : `NOM = <expression d'entiers>`. Le motif
# des routines est reellement une EXPRESSION (`2 * 1024 * 1024`), d'ou le petit
# evaluateur ci-dessous : on n'utilise JAMAIS eval() sur un fichier lu.
MOTIF_ASSIGNATION = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$")


def horodater():
    """Retourne la date-heure locale au format des journaux."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# --- LECTURES --------------------------------------------------------------

def lire_lignes_fichier(chemin):
    """Retourne les lignes d'un fichier (vide si absent ou illisible)."""
    if chemin is None or not Path(chemin).is_file():
        return []
    try:
        with open(str(chemin), "r", encoding=ENCODAGE, errors="replace") as flux:
            return [ligne.rstrip("\r\n") for ligne in flux if ligne.strip()]
    except OSError:
        return []


def lire_lignes_journal(chemin):
    """Lignes BRUTES du journal : lecture complete, reservee a la ROTATION.

    La rotation doit tout voir pour ne rien perdre. Les lecteurs, eux, lisent la
    QUEUE (lire_queue_journal) : c'est ce qui rend leur cout constant.
    """
    return lire_lignes_fichier(chemin)


def lire_queue_journal(chemin, octets):
    """Retourne les DERNIERES lignes d'un journal, sans balayer l'historique.

    La premiere ligne lue peut etre TRONQUEE (on a coupe au milieu) : elle n'est
    gardee que si la lecture a commence au debut du fichier.
    """
    chemin = Path(chemin)
    if not chemin.is_file():
        return []
    try:
        taille = chemin.stat().st_size
        debut = max(0, taille - octets)
        with open(str(chemin), "rb") as flux:
            flux.seek(debut)
            bloc = flux.read()
    except OSError:
        return []
    lignes = bloc.decode(ENCODAGE, errors="replace").splitlines()
    if debut > 0 and lignes:
        lignes = lignes[1:]
    return [ligne for ligne in lignes if ligne.strip()]


def _valeur_entiere(expression, valeurs, vus=None):
    """Valeur d'une expression d'ENTIERS (digits, +, *, parentheses, renvois).

    Aucune execution de code lu : l'arbre est parcouru a la main, seuls les
    entiers, les sommes, les produits et les renvois a une autre constante du
    MEME fichier sont acceptes. Tout le reste rend None (declaration non lue =
    annoncee comme telle par l'appelant, jamais un zero silencieux).
    """
    vus = vus or set()
    try:
        noeud = ast.parse(expression, mode="eval").body
    except SyntaxError:
        return None

    def valeur(courant, deja):
        if isinstance(courant, ast.Constant) and isinstance(courant.value, int):
            return courant.value
        if isinstance(courant, ast.Name):
            if courant.id in deja:
                return None
            brut = valeurs.get(courant.id)
            return None if brut is None else valeur(ast.parse(brut, mode="eval").body, deja | {courant.id})
        if isinstance(courant, ast.BinOp) and isinstance(courant.op, (ast.Add, ast.Mult)):
            gauche = valeur(courant.left, deja)
            droite = valeur(courant.right, deja)
            if gauche is None or droite is None:
                return None
            return gauche + droite if isinstance(courant.op, ast.Add) else gauche * droite
        return None

    try:
        return valeur(noeud, vus)
    except SyntaxError:
        return None


def lire_constante_declaree(chemin_constantes, nom):
    """Valeur ENTIERE d'une constante, lue dans SON fichier de declarations.

    Pourquoi lire au lieu d'importer (lecon L-029) : les modules `constants` des
    routines portent TOUS le meme nom ; les importer ferait se marcher dessus.
    On lit donc la declaration chez son proprietaire, renvois resolus.
    """
    chemin = Path(chemin_constantes)
    if not chemin.is_file():
        return None
    try:
        contenu = chemin.read_text(encoding=ENCODAGE, errors="replace")
    except OSError:
        return None
    valeurs = {}
    for ligne in contenu.splitlines():
        resultat = MOTIF_ASSIGNATION.match(ligne)
        if resultat:
            valeurs[resultat.group(1)] = resultat.group(2).split("#")[0].strip()
    return _valeur_entiere(valeurs.get(nom, ""), valeurs)


def octets_queue(borne_declaree=None):
    """Fenetre de lecture (octets) : jamais moins que le planCHER ni que la borne.

    `borne_declaree` = la borne de rotation que le journal lu DECLARE lui-meme.
    Rendre le planCHER quand rien n'est declare est un CHOIX assume : un journal
    etranger (cobaye) se lit borne, jamais en entier.
    """
    planche = OCTETS_QUEUE_PLANCHER
    if borne_declaree is None:
        return planche
    try:
        borne = int(borne_declaree)
    except (TypeError, ValueError):
        return planche
    return max(borne, planche)


def octets_queue_du_journal(chemin_journal, nom=NOM_CONSTANTE_BORNE):
    """Fenetre deduite de la borne que le DOMAINE du journal declare.

    Le domaine d'un journal, c'est son dossier : `routines/<nom>/journal-*.jsonl`
    declare sa borne dans `routines/<nom>/constants.py`. Aucun appelant ne
    recopie donc un nombre : il demande la fenetre au journal qu'il lit.
    Si le domaine ne declare rien, le planCHER fait foi (et l'appelant peut le
    DIRE -- voir verifier-cadence).
    """
    chemin = Path(chemin_journal)
    return octets_queue(lire_constante_declaree(chemin.parent / "constants.py", nom))


def empreinte_fichier(chemin):
    """Retourne (taille en octets, mtime en nanosecondes) ; (None, None) si absent.

    La taille est un VERSIONNAGE bon marche du journal : un ajout la fait bouger,
    et c'est ce qui permet de refuser d'ecraser ce qui a ete ecrit pendant la
    rotation.
    """
    try:
        etat = os.stat(str(chemin))
    except OSError:
        return None, None
    return etat.st_size, etat.st_mtime_ns


# --- ARCHIVES --------------------------------------------------------------

def signature(ligne):
    """Signature EXACTE d'une ligne (la date COMPTE).

    Deux evenements identiques a deux dates sont DEUX faits : un journal est une
    suite, pas un ensemble. La signature ne sert donc qu'a reconnaitre ce qui est
    DEJA dans l'archive (reprise apres arret), jamais a fusionner deux faits.
    """
    try:
        return json.dumps(json.loads(ligne), ensure_ascii=True, sort_keys=True)
    except (ValueError, TypeError):
        return ligne


def archives_existantes(repertoire, prefixe):
    """Toutes les archives de ce journal, dans l'ordre de leur nom (donc du jour)."""
    repertoire = Path(repertoire)
    if not repertoire.is_dir():
        return []
    return sorted(repertoire.glob(prefixe + "-*.jsonl"))


def deja_connu(repertoire, prefixe):
    """Le "deja connu" de la rotation : CE QUE LES ARCHIVES CONTIENNENT DEJA.

    L'archive fait partie du connu au meme titre que le journal actif : c'est
    exactement ce que la lecon L-040 exige d'un nettoyage qui DEPLACE.
    """
    connues = set()
    for chemin in archives_existantes(repertoire, prefixe):
        for ligne in lire_lignes_fichier(chemin):
            connues.add(signature(ligne))
    return connues


def nom_archive(prefixe, date=None):
    """Nom de l'archive du jour : prefixe-AAAAMMJJ.jsonl."""
    date = date or datetime.now()
    return prefixe + "-" + date.strftime("%Y%m%d") + ".jsonl"


def ajouter_archive(chemin, lignes, connues):
    """AJOUTE a l'archive ce qui n'y est pas deja (append, LF forces).

    Retourne (ecrits, jumeaux). Un jumeau est une ligne DEJA presente dans une
    archive : reprise apres un arret entre l'archivage et la reecriture, ou
    rotation relancee. On l'IGNORE, on ne l'ecrit pas deux fois.

    `connues` n'est pas enrichi au fil du lot : deux lignes identiques DANS le
    meme lot sont deux evenements d'origine et doivent etre ecrites deux fois,
    sinon la rotation perdrait une ligne sans le dire.
    """
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    ecrits = 0
    jumeaux = 0
    with open(str(chemin), "a", encoding=ENCODAGE, newline="\n") as flux:
        for ligne in lignes:
            if signature(ligne) in connues:
                jumeaux += 1
                continue
            flux.write(ligne + "\n")
            ecrits += 1
    return ecrits, jumeaux


def reecrire_journal(chemin, lignes):
    """Reecrit le journal de facon ATOMIQUE (tmp + remplacement, LF forces)."""
    chemin = Path(chemin)
    temporaire = chemin.with_name(chemin.name + ".tmp")
    with open(str(temporaire), "w", encoding=ENCODAGE, newline="\n") as flux:
        for ligne in lignes:
            flux.write(ligne + "\n")
    os.replace(str(temporaire), str(chemin))


def partager(lignes, gardees):
    """Separe (a archiver, a garder) : on garde la QUEUE, on archive la TETE."""
    coupe = max(0, len(lignes) - gardees)
    return lignes[:coupe], lignes[coupe:]


def controler_archive(repertoire, prefixe, a_archiver):
    """Apres coup : tout ce qui a QUITTE le journal est-il dans les archives ?"""
    manquantes = []
    connues = deja_connu(repertoire, prefixe)
    for ligne in a_archiver:
        if signature(ligne) not in connues:
            manquantes.append(ligne)
    return manquantes


# --- DECISION ET ROTATION --------------------------------------------------

def decision_rotation(taille_octets, nb_lignes, seuil_octets, gardes):
    """Decision PURE : (faut_il_tourner, evenements_gardes, motif).

    Rien n'est decide par une horloge ni par un fichier : la fonction rend la
    meme reponse pour les memes nombres, donc elle se teste sans disque.
    """
    if taille_octets is None:
        return False, 0, "journal absent"
    if taille_octets <= seuil_octets:
        return (
            False,
            nb_lignes,
            str(taille_octets) + " octets <= seuil " + str(seuil_octets) + " : rien a faire",
        )
    gardees = min(gardes, nb_lignes)
    if gardees >= nb_lignes:
        return (
            False,
            nb_lignes,
            str(nb_lignes) + " evenement(s) : tous a garder (seuil de garde " + str(gardes) + ")",
        )
    return (
        True,
        gardees,
        str(taille_octets) + " octets > seuil " + str(seuil_octets)
        + " : on archive tout sauf les " + str(gardees) + " derniers evenements",
    )


def rapport_vide(journal, motif):
    """Rapport d'une rotation qui n'a pas eu lieu (toujours motive)."""
    return {
        "rotation": False,
        "motif": motif,
        "essai": 0,
        "journal": str(journal),
        "lignes_avant": 0,
        "lignes_archivees": 0,
        "lignes_gardees": 0,
        "octets_avant": None,
        "octets_apres": None,
        "ecrits": 0,
        "jumeaux": 0,
        "archive": "",
    }


def tourner(journal, seuil_octets, gardes, essais, prefixe, forcer=False):
    """Rotation complete. Rend un rapport (dict) -- jamais d'exception."""
    journal = Path(journal)
    rapport = rapport_vide(journal, "")
    if not journal.is_file():
        rapport["motif"] = "journal absent : " + str(journal)
        return rapport

    repertoire = journal.parent
    for essai in range(1, essais + 1):
        rapport["essai"] = essai
        taille_avant, _ = empreinte_fichier(journal)
        lignes = lire_lignes_journal(journal)
        faut, gardees, motif = decision_rotation(taille_avant, len(lignes), seuil_octets, gardes)
        if forcer and len(lignes) > 1:
            faut = True
            gardees = min(gardes, len(lignes))
            motif = "FORCEE (--force) -- " + motif
        rapport.update(
            {
                "motif": motif,
                "lignes_avant": len(lignes),
                "octets_avant": taille_avant,
                "lignes_gardees": gardees,
            }
        )
        if not faut:
            return rapport

        a_archiver, a_garder = partager(lignes, gardees)
        chemin_archive = repertoire / nom_archive(prefixe)
        connues = deja_connu(repertoire, prefixe)
        ecrits, jumeaux = ajouter_archive(chemin_archive, a_archiver, connues)

        taille_controle, _ = empreinte_fichier(journal)
        if taille_controle != taille_avant:
            # Quelqu'un a ecrit pendant la rotation : on n'ecrase RIEN.
            rapport["motif"] = (
                "course : le journal a grossi pendant la rotation (" + str(taille_avant)
                + " -> " + str(taille_controle) + " octets), nouvel essai"
            )
            continue

        reecrire_journal(journal, a_garder)
        octets_apres, _ = empreinte_fichier(journal)
        manquantes = controler_archive(repertoire, prefixe, a_archiver)
        rapport.update(
            {
                "rotation": not manquantes,
                "lignes_archivees": len(a_archiver),
                "ecrits": ecrits,
                "jumeaux": jumeaux,
                "archive": chemin_archive.name,
                "octets_apres": octets_apres,
            }
        )
        if manquantes:
            rapport["motif"] = (
                "ECART : " + str(len(manquantes)) + " ligne(s) archivee(s) absente(s) des archives"
            )
        return rapport

    rapport["motif"] = (
        "REFUS : le journal bouge a chaque essai (" + str(essais)
        + ") -- rien n'a ete ecrase, la rotation sera retentee"
    )
    return rapport


def resumer(rapport):
    """Rend le rapport lisible (une ligne par fait, jamais un silence)."""
    lignes = []
    etat = "ROTATION" if rapport["rotation"] else "SANS ROTATION"
    lignes.append(etat + " : " + rapport["motif"])
    if rapport["lignes_avant"]:
        lignes.append(
            "  journal  : " + str(rapport["lignes_avant"]) + " -> "
            + str(rapport["lignes_gardees"]) + " evenement(s) actif(s)"
            + (
                " (" + str(rapport["octets_avant"]) + " -> " + str(rapport["octets_apres"]) + " octets)"
                if rapport["octets_apres"] is not None
                else ""
            )
        )
    if rapport["rotation"]:
        lignes.append(
            "  archive  : " + str(rapport["ecrits"]) + " ecrit(s) / "
            + str(rapport["lignes_archivees"]) + " deplace(s), "
            + str(rapport["jumeaux"]) + " jumeau(x) deja archive(s) ignore(s) -> "
            + rapport["archive"]
        )
    return "\n".join(lignes)


def evenement_rotation(rapport):
    """L'evenement de trace d'une rotation (ou d'un refus), pret a journaliser."""
    return {
        "type": "rotation",
        "archive": rapport["archive"],
        "lignes_archivees": rapport["lignes_archivees"],
        "lignes_gardees": rapport["lignes_gardees"],
        "ecrits": rapport["ecrits"],
        "jumeaux": rapport["jumeaux"],
        "octets_avant": rapport["octets_avant"],
        "octets_apres": rapport["octets_apres"],
        "motif": rapport["motif"],
    }


def tourner_et_journaliser(journal, seuil_octets, gardes, essais, prefixe,
                           journaliser=None, verbeux=False, forcer=False):
    """Rotation + trace au journal. Rend (code, rapport). Ne leve JAMAIS.

    code 0 = fait ou rien a faire ; code 1 = refus (course) ou ecart d'archive.
    Un controle de fond ne tue pas la passe qui l'appelle (lecon L-026), et la
    trace va dans le journal de CETTE rotation -- jamais dans celui du service
    quand on tourne sur un cobaye (lecon L-015).
    """
    try:
        rapport = tourner(journal, seuil_octets, gardes, essais, prefixe, forcer)
    except Exception as erreur:  # noqa: BLE001 -- on AVOUE l'echec, on ne plante pas
        return 1, rapport_vide(
            journal, "rotation impossible (" + type(erreur).__name__ + ") : " + str(erreur)
        )

    if verbeux:
        print(resumer(rapport))
    trace = rapport["rotation"] or "REFUS" in rapport["motif"] or "ECART" in rapport["motif"]
    if trace and journaliser is not None:
        journaliser(evenement_rotation(rapport))
    if "REFUS" in rapport["motif"] or "ECART" in rapport["motif"]:
        return 1, rapport
    return 0, rapport


# --- VERBES -----------------------------------------------------------------

def cli(arguments, journal_pour_racine, seuil_octets, gardes, essais, prefixe, journaliser=None):
    """Verbe `rotation` d'une routine : borne SON journal en archivant.

    `journal_pour_racine(racine)` rend le journal a traiter pour une racine
    donnee : un cobaye peut ainsi jouer la porte REELLE sur ses propres fichiers
    (lecon L-032 : un controle qu'on ne peut pas pieger ne prouve rien).
    """
    analyseur = argparse.ArgumentParser(
        description="Borne un journal en ARCHIVANT ses evenements anciens"
                    " (jamais de suppression : rien ne se perd)"
    )
    analyseur.add_argument("--racine", default=None,
                           help="Racine matrix/ a traiter (defaut : celle du depot ; sert aux cobayes)")
    analyseur.add_argument("--seuil", type=int, default=None, help="Seuil de declenchement en octets")
    analyseur.add_argument("--gardes", type=int, default=None,
                           help="Evenements gardes dans le journal actif")
    analyseur.add_argument("--force", action="store_true",
                           help="Tourner meme sous le seuil (reserve aux cobayes)")
    options = analyseur.parse_args(arguments)
    code, _ = tourner_et_journaliser(
        journal_pour_racine(options.racine),
        options.seuil if options.seuil is not None else seuil_octets,
        options.gardes if options.gardes is not None else gardes,
        essais, prefixe, journaliser, verbeux=True, forcer=options.force,
    )
    return code
