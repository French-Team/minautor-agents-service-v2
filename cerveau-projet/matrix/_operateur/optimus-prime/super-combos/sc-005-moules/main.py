#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sc-005-moules -- garde des MOULES (`matrice/templates/`).

POURQUOI CE SUPER-COMBO (demande du createur, 2026-09-25). Un MOULE
(`matrice/templates/<moule>/`) est le PATRON dont `dupliquer-template` fabrique
chaque clone. Un moule qui DERIVE ne casse pas UN objet : il casse TOUS les
clones a venir, en silence -- la faute est payee une fois par clone. La classe a
ete MESUREE le 2026-09-25 (corvee C-009) : le moule outil-bdd produisait un clone
qui faisait crier TROIS gardes du projet (prefixe d identifiant EN DUR dans
`ajouter/fonctions.py`, `DESCRIPTION.md` SANS carte d identite, commandes NON
ANCREES). La reparation a ete prouvee par un cobaye JETABLE -- qui meurt a la
cloture : RIEN ne surveillait la suite (lecon MO-246 : un controle qui vit dans
un cobaye meurt avec lui). Mesure du meme jour sur les DEUX autres moules de
generation : `theme-bdd` et `routine` portaient ENCORE les trois memes classes
d ecart dans leur `DESCRIPTION.md.moule`, pendant que leurs clones VIVANTS
(theme-vivier, veille-flux) avaient ete REPARES A LA MAIN -- le clone etait sain,
le moule etait perime : la prochaine generation ramenait la regression.

CE QU IL EXIGE, moule par moule -- les invariants que les gardes du projet
exigent d un VIVANT, lus sur le MOULE (donc sur le clone A VENIR) :
  1. un moule de GENERATION porte des fichiers `.moule` (sinon il ne fabrique
     rien) ;
  2. CHAQUE document du moule (`.md`, `.md.moule`) porte une CARTE D IDENTITE
     VALIDE -- la grammaire est CONSOMMEE a son domicile
     (`matrice/data/commun/carte_identite.py`), jamais recopiee (M-076) ;
  3. les COMMANDES citees dans le moule sont CONFORMES : pas de `python -c`
     (code en argument), pas de heredoc, et tout script `.py` est ANCRE
     (`cerveau-projet/...` ou chemin absolu -- jamais `main.py` nu) ;
  4. aucun `.py.moule` ne porte de PREFIXE D IDENTIFIANT EN DUR (`"C-"`) : le
     prefixe vit dans les constantes du moule, sous le jeton `__PREFIXE_ID__`.

Les moules HORS generation (un dossier `templates/` sans `.moule`, par exemple
`carte-identite` et ses `.modele`) sont INVENTORIES mais NON juges : ils ne sont
pas consommes par `dupliquer-template`, un garde qui les jugerait accuserait a
tort.

CE QU IL NE FAIT PAS : lecture seule sur les moules reels. L auto-test ecrit des
moules COBAYES dans une zone jetable SYSTEME (jamais dans la Matrice).

Usage : python main.py verifier [--templates <dossier>] | inventaire | status | auto-test
  code 0 = tous les moules de generation conformes, 1 = au moins un ecart (nomme),
  2 = refus.
"""

import argparse
import re
import sys
import tempfile
from pathlib import Path

SUPER_ID = "sc-005"
SUPER_NOM = "sc-005-moules"
PHASES = ["inventaire", "verifier"]
VERBE_DEFAUT = "verifier"
VERBES = ["inventaire", "verifier", "status", "auto-test"]

CODE_OK = 0
CODE_ECHEC = 1
CODE_REFUS = 2

# --- DOMICILE DE LA MATRICE (MO-088 : aucun parents[N] nu) -------------------
BORNES_REMONTEE = 30
REPERTOIRE_SUPER = Path(__file__).resolve().parent
_courant = REPERTOIRE_SUPER
for _ in range(BORNES_REMONTEE):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        break
    _courant = _courant.parent
else:
    raise RuntimeError("Racine matrix/ introuvable en remontant.")
RACINE_MATRICE = _courant

# --- DOMICILE PARTAGE DE LA GRAMMAIRE DES CARTES (M-076 : consomme, jamais recopie)
REPERTOIRE_COMMUN = RACINE_MATRICE / "matrice" / "data" / "commun"
if str(REPERTOIRE_COMMUN) not in sys.path:
    sys.path.insert(0, str(REPERTOIRE_COMMUN))
from carte_identite import (  # noqa: E402
    CLES_OBLIGATOIRES,
    SEPARATEURS_INTERDITS,
    TYPES_RECONNUS,
    lire_carte,
)

REPERTOIRE_TEMPLATES = RACINE_MATRICE / "matrice" / "templates"
SUFFIXE_MOULE = ".moule"

# Les documents d un moule : les .md (README) ET les .md.moule (qui deviendront
# des .md dans le clone -- c est EUX que le garde des cartes jugera alors).
MOTIF_BLOC = re.compile(r"```[^\n]*\n(.*?)```", re.S)
MOTIF_SPAN = re.compile(r"`([^`\n]+)`")
MOTIF_INTERPRETEUR = re.compile(r"^(python3?|py)\b")
MOTIF_PY = re.compile(r"\.py$")
# Un prefixe d identifiant EN DUR : deux a cinq MAJUSCULES suivies d un tiret,
# entre guillemets (`"C-"`, `"MO-"`). Le prefixe du moule vit dans les constantes
# sous le jeton __PREFIXE_ID__ -- jamais en clair dans le code.
MOTIF_PREFIXE_EN_DUR = re.compile(r"['\"]([A-Z]{1,5}-)['\"]")
ANCRAGES = ("cerveau-projet/", "/")

CARTE_SAINE = ("---\nidentite:\n  type: outil\n  appartient_a: matrice-data-outils\n"
               "  commun: true\n---\n")


def moules_de_generation(templates):
    """Les dossiers de `templates/` qui sont de VRAIS moules de generation.

    Un moule de generation porte au moins un fichier `.moule` -- c est la forme
    que `dupliquer-template` consomme. Un dossier sans `.moule` (par exemple
    `carte-identite`, fait de `.modele`) n est pas juge : il ne fabrique pas de
    clone par ce generateur.
    """
    if not templates.is_dir():
        return []
    trouves = []
    for dossier in sorted(templates.iterdir()):
        if not dossier.is_dir() or dossier.name.startswith("."):
            continue
        if any(dossier.rglob("*" + SUFFIXE_MOULE)):
            trouves.append(dossier)
    return trouves


def fichiers_moule(moule):
    """Les fichiers `.moule` du moule, tries (les .bak horodates sont exclus par
    la forme du suffixe)."""
    return sorted(chemin for chemin in moule.rglob("*" + SUFFIXE_MOULE) if chemin.is_file())


def documents_moule(moule):
    """Les documents du moule : les `.md` (README) et les `.md.moule`.

    Le `.md.moule` deviendra un `.md` dans le clone : c est donc sur lui que les
    gardes du projet (cartes, commandes) jugeront le clone A VENIR.
    """
    documents = [chemin for chemin in moule.rglob("*.md") if chemin.is_file()]
    documents += [chemin for chemin in moule.rglob("*.md" + SUFFIXE_MOULE) if chemin.is_file()]
    return sorted(set(documents))


def lire_texte(chemin):
    # Lecture tolerante : une erreur de decodage ne doit pas faire tomber un garde.
    return chemin.read_text(encoding="utf-8", errors="replace")


def juger_carte(texte, rel):
    """Ecarts de la CARTE d identite d un document, lus avec la grammaire PARTAGEE."""
    carte = lire_carte(texte)
    if not carte:
        return [(rel, "SANS carte d identite : le clone naitra SANS carte (type,"
                      " appartient_a, commun) -- la grammaire vit dans"
                      " matrice/data/commun/carte_identite.py")]
    ecarts = []
    for cle in CLES_OBLIGATOIRES:
        if cle not in carte:
            ecarts.append((rel, "carte INCOMPLETE : cle obligatoire absente (" + cle + ")"))
    appartenance = str(carte.get("appartient_a", "") or "")
    if any(separateur in appartenance for separateur in SEPARATEURS_INTERDITS):
        ecarts.append((rel, "carte : appartient_a est un CHEMIN (" + appartenance
                            + ") -- un NOM est attendu"))
    type_doc = str(carte.get("type", "") or "")
    if type_doc and type_doc not in TYPES_RECONNUS:
        ecarts.append((rel, "carte : type hors vocabulaire (" + type_doc + ")"))
    return ecarts


def lignes_commandes(texte):
    """Les lignes d un document : (ligne, dans_bloc).

    On lit les BLOCS de code (chaque ligne) PUIS les spans inline -- et on DIT si
    la ligne vient d un bloc. Un span inline est bien plus souvent une REFERENCE
    (`constants.py`, `battement.py`) qu une commande ; seuls les spans qui
    COMMENCENT par un interpreteur sont des commandes (meme regle que le garde
    des commandes, MO-249). Les spans sont lus HORS des blocs (sinon un bloc
    entier serait relu par ses spans et une commande serait jugee deux fois).
    """
    lignes = []
    for bloc in MOTIF_BLOC.findall(texte or ""):
        for ligne in bloc.splitlines():
            propre = ligne.strip()
            if propre:
                lignes.append((propre, True))
    hors_bloc = MOTIF_BLOC.sub("", texte or "")
    for span in MOTIF_SPAN.findall(hors_bloc):
        propre = span.strip()
        if propre:
            lignes.append((propre, False))
    return lignes


def est_commande(ligne, dans_bloc):
    """Vrai si (ligne, dans_bloc) EST une commande.

    Dans un BLOC de code : une ligne qui commence par un interpreteur, OU dont le
    premier mot est un script `.py`. HORS bloc (span inline) : SEULEMENT si elle
    commence par un interpreteur -- un nom de fichier nu n est pas une commande.
    """
    noyau = ligne[2:].strip() if ligne.startswith("$ ") else ligne
    if not noyau:
        return False
    if MOTIF_INTERPRETEUR.match(noyau):
        return True
    if not dans_bloc:
        return False
    premier = noyau.split()[0]
    return bool(MOTIF_PY.search(premier))


def juger_commande(ligne):
    """L ecart d une commande, ou "" : les trois formes que le garde des
    commandes accuse (code en argument, heredoc, chemin non ancre)."""
    noyau = ligne[2:].strip() if ligne.startswith("$ ") else ligne
    if re.match(r"^python3?\s+-c\b", noyau):
        return "python -c : du code en ARGUMENT (le shell le transporte mal)"
    if "<<" in noyau:
        return "heredoc << : du contenu en ARGUMENT (interdit, EO-132)"
    fautes = []
    for jeton in noyau.split():
        if jeton.startswith("-"):
            continue
        if jeton.endswith(".py") and not jeton.startswith(ANCRAGES):
            fautes.append("chemin non ancre : " + jeton)
    return " ; ".join(fautes)


def juger_moule(moule):
    """Les ecarts d un moule de generation : liste de (chemin relatif, message)."""
    ecarts = []
    if not fichiers_moule(moule):
        ecarts.append(("(moule)", "aucun fichier .moule : ce moule ne fabrique rien"))
        return ecarts
    for document in documents_moule(moule):
        rel = document.relative_to(moule).as_posix()
        texte = lire_texte(document)
        ecarts.extend(juger_carte(texte, rel))
        for ligne, dans_bloc in lignes_commandes(texte):
            if not est_commande(ligne, dans_bloc):
                continue
            faute = juger_commande(ligne)
            if faute:
                ecarts.append((rel, "commande NON CONFORME (" + faute + ") -- <"
                                    + ligne[:90] + ">"))
    for source in fichiers_moule(moule):
        if not source.name.endswith(".py" + SUFFIXE_MOULE):
            continue
        rel = source.relative_to(moule).as_posix()
        for trouve in MOTIF_PREFIXE_EN_DUR.finditer(lire_texte(source)):
            ecarts.append((rel, "prefixe d identifiant EN DUR : " + repr(trouve.group(1))
                                + " -- le prefixe vit dans les constantes du moule"
                                  " (jeton __PREFIXE_ID__), jamais en clair"))
    return ecarts


def cmd_inventaire(arguments):
    # INVENTAIRE : ce que la zone porte, en distinguant generation et hors generation.
    if not REPERTOIRE_TEMPLATES.is_dir():
        print("REFUS : dossier des moules introuvable : " + str(REPERTOIRE_TEMPLATES))
        return CODE_REFUS
    dossiers = sorted(d for d in REPERTOIRE_TEMPLATES.iterdir()
                      if d.is_dir() and not d.name.startswith("."))
    generation = set(moules_de_generation(REPERTOIRE_TEMPLATES))
    print("INVENTAIRE DES MOULES (" + str(len(dossiers)) + " dossier(s) sous templates/)")
    for dossier in dossiers:
        nombre = len(fichiers_moule(dossier))
        documents = len(documents_moule(dossier))
        if dossier in generation:
            print("  " + dossier.name.ljust(16) + " generation (" + str(nombre)
                  + " .moule, " + str(documents) + " document(s))")
        else:
            print("  " + dossier.name.ljust(16) + " hors generation (aucun .moule)")
    return CODE_OK


def cmd_verifier(arguments):
    # VERIFIER : le verdict sur chaque moule de generation.
    analyseur = argparse.ArgumentParser(description="Juger les moules de generation")
    analyseur.add_argument("--templates", default=None,
                           help="Dossier des moules (cobaye) ; defaut : matrice/templates")
    parsed = analyseur.parse_args(arguments)
    templates = Path(parsed.templates) if parsed.templates else REPERTOIRE_TEMPLATES
    if not templates.is_dir():
        print("REFUS : dossier des moules introuvable : " + str(templates))
        return CODE_REFUS
    moules = moules_de_generation(templates)
    if not moules:
        print("REFUS : aucun moule de generation (.moule) dans " + str(templates))
        return CODE_REFUS
    total = 0
    print("GARDE DES MOULES (" + SUPER_ID + ") -- " + str(len(moules)) + " moule(s) de generation")
    for moule in moules:
        ecarts = juger_moule(moule)
        if not ecarts:
            print("  " + moule.name.ljust(16) + " conforme (" + str(len(fichiers_moule(moule)))
                  + " fichier(s) .moule, " + str(len(documents_moule(moule))) + " document(s))")
            continue
        total += len(ecarts)
        print("  " + moule.name.ljust(16) + " " + str(len(ecarts)) + " ecart(s)")
        for rel, message in ecarts:
            print("    - " + rel + " : " + message)
    if total:
        print("VERDICT : " + str(total) + " ecart(s) -- un moule qui derive contamine"
              " TOUS les clones a venir.")
        return CODE_ECHEC
    print("VERDICT : tous les moules de generation sont conformes.")
    return CODE_OK


def cmd_status(arguments):
    print("Super-combo  : " + SUPER_NOM + " (" + SUPER_ID + ")")
    print("Phases       : " + ", ".join(PHASES))
    print("Moules       : " + str(REPERTOIRE_TEMPLATES)
          + (" [OK]" if REPERTOIRE_TEMPLATES.is_dir() else " [ABSENT]"))
    print("Generation   : " + str(len(moules_de_generation(REPERTOIRE_TEMPLATES))) + " moule(s)")
    print("Verbe defaut : " + VERBE_DEFAUT)
    print("Verbes       : " + ", ".join(VERBES))
    return CODE_OK


def cmd_auto_test(arguments):
    # Le garde est EPROUVE : un moule CASSE doit MORDRE, un moule SAIN doit EPARGNER.
    ecarts = []
    if principal(["verbe-hors-contrat"]) != CODE_ECHEC:
        ecarts.append("un verbe hors contrat est ACCEPTE")
    with tempfile.TemporaryDirectory(prefix="cobaye-sc005-") as zone:
        templates = Path(zone) / "templates"
        sain = templates / "moule-sain"
        casse = templates / "moule-casse"
        (sain / "ajouter").mkdir(parents=True)
        (casse / "ajouter").mkdir(parents=True)
        (sain / "constants.py.moule").write_text('PREFIXE_ID = "__PREFIXE_ID__"\n',
                                                 encoding="utf-8")
        (sain / "ajouter" / "fonctions.py.moule").write_text(
            "from constants import PREFIXE_ID\n\n\ndef former(numero):\n"
            "    return PREFIXE_ID + \"-\" + str(numero)\n", encoding="utf-8")
        (sain / "DESCRIPTION.md.moule").write_text(
            CARTE_SAINE + "\n# OUTIL -- __NOM_OUTIL__\n\n```\n"
            "python3 cerveau-projet/matrix/lancer.py __NOM_OUTIL__ lire\n```\n",
            encoding="utf-8")
        (casse / "constants.py.moule").write_text('PREFIXE = "C-"\n', encoding="utf-8")
        (casse / "ajouter" / "fonctions.py.moule").write_text(
            "def former(numero):\n    return \"C-\" + str(numero)\n", encoding="utf-8")
        (casse / "DESCRIPTION.md.moule").write_text(
            "# OUTIL -- __NOM_OUTIL__\n\n```\npython main.py lire\n```\n",
            encoding="utf-8")
        ecarts_sains = juger_moule(sain)
        ecarts_casses = juger_moule(casse)
        if ecarts_sains:
            ecarts.append("le CONTRE-TEMOIN (moule sain) est ACCUSE a tort : "
                          + " ; ".join(message for _rel, message in ecarts_sains))
        if not ecarts_casses:
            ecarts.append("le COBAYE (moule casse) n est PAS accuse : le garde ne mord pas")
    if ecarts:
        print("AUTO-TEST " + SUPER_ID + " : " + str(len(ecarts)) + " ecart(s)")
        for ecart in ecarts:
            print("  - " + ecart)
        return CODE_ECHEC
    print("AUTO-TEST " + SUPER_ID + " : conforme (cobaye qui MORD, contre-temoin qui EPARGNE)")
    print("  cobaye   : moule casse ACCUSE (carte absente + prefixe en dur + commande non ancree)")
    print("  temoin   : moule sain EPARGNE")
    return CODE_OK


def principal(arguments):
    # Diriger : verbe connu -> sa fonction ; verdict du contrat, jamais un silence.
    if not arguments:
        print("Usage : python main.py verifier [--templates <dossier>] | inventaire"
              " | status | auto-test")
        return CODE_ECHEC
    verbe = arguments[0]
    table = {
        "inventaire": cmd_inventaire,
        "verifier": cmd_verifier,
        "status": cmd_status,
        "auto-test": cmd_auto_test,
    }
    if verbe in table:
        return table[verbe](arguments[1:])
    print("REFUS : verbe inconnu : " + verbe)
    print("  verbes acceptes : " + ", ".join(VERBES))
    return CODE_ECHEC


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
