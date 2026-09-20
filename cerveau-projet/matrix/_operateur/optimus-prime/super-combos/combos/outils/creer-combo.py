#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
creer-combo.py -- Suite de generation des combos NUMEROTES dedies aux BDD

CONTRAT DE NOMMAGE (decisions createur 2026-09-13, convention CV-008 de la BDD
conventions-matrice) : un combo et un
super-combo portent TOUJOURS un numero, visible dans le nom :
    combo       -> c-001-lecons      (id c-001)
    super-combo -> sc-001-auto-xxx   (id sc-001)
Tout est en MINUSCULES : le `C-` MAJUSCULE est reserve au champ `constat`
fige de historiques-missions.jsonl (regle CV-009 : une famille = un prefixe).
Zero-padde sur 3 chiffres, JAMAIS reutilise (le compteur ne redescend pas).
Les outils (`outils/`) ne sont PAS des combos : ils ne sont pas numerotes.

    banque                      -- lister la banque des BDD disponibles
    creer <slug> --bdd <id>     -- generer combos/c-<NNN>-<slug>/ (main + README)
                                   et l'enregistrer dans registry.json
    verifier <nom>              -- structure + py_compile + ASCII + registre + numero
                                   + CONTRAT DE LANCEMENT ("verbe"/"verbes" : un objet
                                   sans contrat serait inlancable -- MO-071/EO-114)
                                   (DEUX familles : `c-` dans combos/, `sc-` dans super-combos/)
    creer-super-combo <slug> --description "..." --phases "a,b" --verbes "x,y"
                                [--verbe <defaut>]
                                -- generer super-combos/sc-<NNN>-<slug>/
                                   (main + README) et l enregistrer dans SON
                                   registre (section super-combos, compteur sc)
    lister                      -- etat numerote des combos et super-combos

Usage: python creer-combo.py <verbe> [args...]
"""

import re
import sys
import json
import argparse
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime


# --- Constantes (convention-zero-valeurs-en-dur) ---------------------------

ENCODAGE = "utf-8"
FINS_LIGNE = "\n"

BANQUE_NOM = "banque-combos-bdd.json"
REGISTRY_NOM = "registry.json"
DOSSIER_MAIN = "main.py"
DOSSIER_README = "README.md"
DOSSIER_RESERVE = ("outils", "__pycache__")
# Reserve de la famille SUPERIEURE : `combos/` n'est pas un super-combo, c'est la
# famille inferieure (modele createur : un super-combo peut contenir des combos).
DOSSIER_RESERVE_SUPER = DOSSIER_RESERVE + ("combos",)
CLE_BANQUE = "banque"
CLE_COMBO = "combos"
CLE_SUPER_COMBO = "super-combos"
CLE_COMPTEURS = "compteurs"
FORMAT_DATE = "%Y-%m-%d %H:%M:%S"

# Contrat de LANCEMENT (MO-071, EO-114) : chaque entree de registre declare
# COMMENT son objet se lance. Le lanceur LIT ces champs (il n'invente plus le
# verbe) et le `verifier` les EXIGE : sans contrat, un objet peut naitre
# inlancable par construction -- c'est exactement le trou mesure sur sc-002
# (le lanceur ecrivait "executer" en dur, sc-002 refuse ce verbe).
CLE_CONTRAT_VERBE = "verbe"
CLE_CONTRAT_VERBES = "verbes"
# Verbes du template des combos generes (main.py : executer / lire / status).
CONTRAT_COMBO_VERBE = "executer"
CONTRAT_COMBO_VERBES = ("executer", "lire", "status")

# Numerotation obligatoire (CV-008).
PREFIXE_COMBO = "c"
PREFIXE_SUPER_COMBO = "sc"
LARGEUR_NUMERO = 3
NUMERO_DEFAUT = 1
MOTIF_NOM = re.compile(r"^(c|sc)-(\d{3})-([a-z0-9]+(?:-[a-z0-9]+)*)$")

OUTIL_USAGES_REL = "matrice/data/outils/bdd-usages/main.py"
COMMANDE_LIRE_DEFAUT = "lire"
OPTION_FILTRE_DEFAUT = "--tag"

# Ancrage sur le fichier + garde structurelle (contrat fondamental CV-007) :
# jamais Path(".")/cwd, jamais parents[N] nu.
REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_COMBOS = REPERTOIRE_OUTIL.parent
if REPERTOIRE_OUTIL.name != "outils" or REPERTOIRE_COMBOS.name != "combos":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_OUTIL) + " n'est pas combos/outils/"
    )

BANQUE_PATH = REPERTOIRE_OUTIL / BANQUE_NOM
REGISTRY_PATH = REPERTOIRE_COMBOS / REGISTRY_NOM

# UNE famille = UN registre, a cote de ses objets (MO-067, 2026-09-13) : les
# super-combos vivent dans super-combos/, un cran AU-DESSUS de combos/, avec
# leur PROPRE source de verite. Cette porte lit les deux registres pour son
# `lister` -- mais n'ecrit jamais que le sien : une porte n'ecrit pas le
# registre d une autre famille. ARBITRAGE CREATEUR du 2026-09-19 (MO-202) :
# cette porte fait desormais NAITRE les deux familles (verbe creer-super-combo) ;
# elle ecrit alors le registre de la famille du NOM, jamais un registre melange.
REPERTOIRE_SUPER_COMBOS = REPERTOIRE_COMBOS.parent
if REPERTOIRE_SUPER_COMBOS.name != "super-combos":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_SUPER_COMBOS) + " n'est pas super-combos/"
    )
REGISTRY_SUPER_PATH = REPERTOIRE_SUPER_COMBOS / REGISTRY_NOM

BORNES_REMONTEE = 30
_courant = REPERTOIRE_OUTIL
for _ in range(BORNES_REMONTEE):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        break
    _courant = _courant.parent
else:
    raise RuntimeError("Racine matrix/ introuvable en remontant.")
RACINE_MATRICE = _courant


# --- Templates -------------------------------------------------------------

TEMPLATE_MAIN = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@@NOM@@ -- Combo numerote @@ID@@ dedie a la BDD @@TITRE@@

Genere par creer-combo.py (imperatif 46, contrat de nommage CV-008) le @@DATE@@.
Chaine : lire (filtre par tags) -> normaliser -> noter usage.

Usage:
    python main.py executer [--tag <tag>] [--mission <id>]
    python main.py lire [--tag <tag>]
    python main.py status
"""

import sys
import argparse
import subprocess
from pathlib import Path


# --- Constantes (convention-zero-valeurs-en-dur) ---------------------------

COMBO_ID = "@@NOM@@"
COMBO_NUMERO = "@@ID@@"
BDD_ID = "@@BDD_ID@@"
BDD_TITRE = "@@TITRE@@"
OUTIL_BDD_REL = "@@OUTIL_REL@@"
COMMANDE_LIRE = "@@CMD_LIRE@@"
OPTION_FILTRE = "@@OPTION_FILTRE@@"
OUTIL_USAGES_REL = "@@OUTIL_USAGES_REL@@"
TAGS_USAGE = "combo,bdd," + BDD_ID
COMMANDE_USAGE = "executer"

BORNES_REMONTEE = 30
REPERTOIRE_COMBO = Path(__file__).resolve().parent
_courant = REPERTOIRE_COMBO
for _ in range(BORNES_REMONTEE):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        break
    _courant = _courant.parent
else:
    raise RuntimeError("Racine matrix/ introuvable en remontant.")
RACINE_MATRICE = _courant
OUTIL_BDD = RACINE_MATRICE / OUTIL_BDD_REL
OUTIL_USAGES = RACINE_MATRICE / OUTIL_USAGES_REL

CODE_OK = 0
CODE_ECHEC = 1
CODE_INJOIGNABLE = 127


def lancer_outil(chemin, arguments):
    """Executer un outil Python et retourner (code, stdout, stderr)."""
    if not chemin.exists():
        return CODE_INJOIGNABLE, "", "Outil introuvable : " + str(chemin)
    resultat = subprocess.run(
        [sys.executable, str(chemin)] + arguments,
        capture_output=True,
        text=True,
    )
    return resultat.returncode, resultat.stdout, resultat.stderr


def args_lecture(tag):
    """Construire les arguments de lecture (commande + filtre optionnel)."""
    arguments = [COMMANDE_LIRE]
    if tag:
        arguments += [OPTION_FILTRE, tag]
    return arguments


def lire_bdd(tag):
    """Etape 1 : lire la BDD (filtre par tags optionnel)."""
    return lancer_outil(OUTIL_BDD, args_lecture(tag))


def normaliser(sortie):
    """Etape 2 : resumer la sortie (lignes utiles, jamais vides)."""
    lignes = [l for l in sortie.splitlines() if l.strip()]
    return len(lignes), lignes


def noter_usage(code):
    """Etape 3 : noter l'usage du combo dans la BDD usages."""
    return lancer_outil(
        OUTIL_USAGES,
        ["noter", "--outil", COMBO_ID, "--commande", COMMANDE_USAGE,
         "--code", str(code), "--tags", TAGS_USAGE],
    )


def cmd_lire(arguments):
    """Passerelle directe vers la lecture de la BDD."""
    parser = argparse.ArgumentParser(description="Lire la BDD " + BDD_TITRE)
    parser.add_argument("--tag", default=None, help="Filtre par tag")
    parsed = parser.parse_args(arguments)

    code, sortie, erreur = lire_bdd(parsed.tag)
    if sortie:
        print(sortie, end="")
    if erreur:
        print(erreur, end="", file=sys.stderr)
    return code


def cmd_executer(arguments):
    """Chaine complete : lire -> normaliser -> noter usage."""
    parser = argparse.ArgumentParser(description="Executer le combo " + COMBO_ID)
    parser.add_argument("--tag", default=None, help="Filtre par tag")
    parser.add_argument("--mission", default=None, help="ID de mission (trace)")
    parsed = parser.parse_args(arguments)

    print("=" * 60)
    print("COMBO " + COMBO_NUMERO + " (" + COMBO_ID + ") -- BDD " + BDD_TITRE)
    print("=" * 60)

    print("\\nETAPE 1/3 -- LIRE")
    code, sortie, erreur = lire_bdd(parsed.tag)
    if sortie:
        print(sortie, end="")
    if erreur:
        print(erreur, end="", file=sys.stderr)

    print("\\nETAPE 2/3 -- NORMALISER")
    nombre, lignes = normaliser(sortie)
    print("Lignes utiles : " + str(nombre))

    print("\\nETAPE 3/3 -- NOTER USAGE")
    code_usage, _, erreur_usage = noter_usage(code)
    if erreur_usage:
        print(erreur_usage, end="", file=sys.stderr)
    print("Usage note : " + COMBO_ID)

    print("\\n" + "=" * 60)
    print("RESULTAT : code " + str(code) + " (" + str(nombre) + " lignes)")
    print("=" * 60)
    return code if code in (CODE_OK, CODE_ECHEC) else CODE_ECHEC


def cmd_status(arguments):
    """Etat du combo : outil BDD joignable, BDD declaree, piste d'usage."""
    print("Combo  : " + COMBO_NUMERO + " (" + COMBO_ID + ")")
    print("BDD    : " + BDD_ID + " (" + BDD_TITRE + ")")
    print("Outil  : " + str(OUTIL_BDD) + (" [OK]" if OUTIL_BDD.exists() else " [ABSENT]"))
    print("Usages : " + str(OUTIL_USAGES) + (" [OK]" if OUTIL_USAGES.exists() else " [ABSENT]"))
    return CODE_OK if OUTIL_BDD.exists() else CODE_ECHEC


VERBES = {
    "executer": cmd_executer,
    "lire": cmd_lire,
    "status": cmd_status,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in VERBES:
        print(__doc__)
        return CODE_ECHEC
    return VERBES[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    sys.exit(main())
'''


TEMPLATE_README = '''# @@NOM@@

> **Combo numerote @@ID@@** -- le numero est OBLIGATOIRE et jamais reutilise
> (contrat de nommage obligatoire CV-008 -- BDD conventions-matrice,
> decision createur 2026-09-13).

Combo dedie a la BDD **@@TITRE@@** (`@@BDD_ID@@`).

> @@DESCRIPTION@@
> Genere par `creer-combo.py` (imperatif 46) le @@DATE@@.

## Chaine

1. **lire** : outil `@@OUTIL_REL@@`, commande `@@CMD_LIRE@@` (filtre `@@OPTION_FILTRE@@ <tag>`)
2. **normaliser** : compte les lignes utiles
3. **noter usage** : piste dans `@@OUTIL_USAGES_REL@@` (tags `combo,bdd,@@BDD_ID@@`)

## Usage

```bash
python main.py executer [--tag <tag>] [--mission <id>]
python main.py lire [--tag <tag>]
python main.py status
```

## Tags de la BDD

@@TAGS_EXEMPLE@@
'''


# --- Fonctions simples -----------------------------------------------------

def date_maintenant():
    """Horodatage lisible, format unique de la Matrice."""
    return datetime.now().strftime(FORMAT_DATE)


def lire_json(chemin, defaut):
    """Lire un JSON ; retourne le defaut s'il est absent."""
    if not chemin.exists():
        return defaut
    with open(chemin, "r", encoding=ENCODAGE) as fichier:
        return json.load(fichier)


def ecrire_atomique(chemin, texte):
    """Ecrire par tmp + remplacement (jamais de fichier tronque), LF forces."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding=ENCODAGE, newline=FINS_LIGNE,
        dir=str(chemin.parent), delete=False, suffix=".tmp",
    ) as temporaire:
        temporaire.write(texte)
        nom_tmp = temporaire.name
    Path(nom_tmp).replace(chemin)


def est_ascii(texte):
    """Vrai si le texte est ASCII strict (convention du depot)."""
    try:
        texte.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def rendre(template, valeurs):
    """Remplir un template par jetons @@TOKEN@@ (jamais de format())."""
    texte = template
    for jeton, valeur in valeurs.items():
        texte = texte.replace(jeton, str(valeur))
    return texte


def analyser_nom(nom):
    """(prefixe, numero, slug) d'un nom numerote, ou None si non conforme."""
    correspondance = MOTIF_NOM.match(nom)
    if correspondance is None:
        return None
    return correspondance.group(1), int(correspondance.group(2)), correspondance.group(3)


def former_nom(prefixe, numero, slug):
    """Nom canonique numerote : c-001-lecons (contrat CV-008)."""
    return prefixe + "-" + str(numero).zfill(LARGEUR_NUMERO) + "-" + slug


def former_id(prefixe, numero):
    """Identifiant canonique : c-001 (minuscules, contrat CV-008).

    Le `C-` MAJUSCULE n'est pas un id de combo : il designe le champ `constat`
    fige de historiques-missions.jsonl (regle CV-009 : une famille = un prefixe).
    """
    return prefixe + "-" + str(numero).zfill(LARGEUR_NUMERO)


def compter(registre, cle):
    """Entrees enregistrees dans une section (combos ou super-combos)."""
    return len(registre.get(cle, []))


def numero_suivant(registre, prefixe, cle):
    """Numero suivant : compteur haut (JAMAIS reutilise), jamais un trou."""
    compteurs = registre.setdefault(CLE_COMPTEURS, {})
    haut = compteurs.get(prefixe, 0)
    for entree in registre.get(cle, []):
        analyse = analyser_nom(entree.get("nom", ""))
        if analyse and analyse[0] == prefixe and analyse[1] > haut:
            haut = analyse[1]
    return haut + NUMERO_DEFAUT


def charger_banque():
    """Charger la banque des BDD ; erreur claire si absente ou invalide."""
    if not BANQUE_PATH.exists():
        print("Banque introuvable : " + str(BANQUE_PATH))
        return None
    try:
        return lire_json(BANQUE_PATH, {})
    except json.JSONDecodeError as erreur:
        print("Banque invalide : " + str(erreur))
        return None


def trouver_modele(banque, bdd_id):
    """Retrouver une entree de la banque par son id (ou None)."""
    for modele in banque.get(CLE_BANQUE, []):
        if modele.get("id") == bdd_id:
            return modele
    return None


def valeurs_combo(nom, identifiant, modele):
    """Valeurs a injecter dans les templates (aucune valeur en dur ailleurs)."""
    return {
        "@@NOM@@": nom,
        "@@ID@@": identifiant,
        "@@BDD_ID@@": modele.get("id", ""),
        "@@TITRE@@": modele.get("titre", ""),
        "@@DESCRIPTION@@": modele.get("description", ""),
        "@@OUTIL_REL@@": modele.get("outil", ""),
        "@@CMD_LIRE@@": modele.get("commande_lire", COMMANDE_LIRE_DEFAUT),
        "@@OPTION_FILTRE@@": modele.get("option_filtre", OPTION_FILTRE_DEFAUT),
        "@@TAGS_EXEMPLE@@": modele.get("tags_exemple", ""),
        "@@OUTIL_USAGES_REL@@": OUTIL_USAGES_REL,
        "@@DATE@@": date_maintenant(),
    }


def enregistrer_registry(nom, identifiant, numero, slug, modele, date):
    """Enregistrer (ou rafraichir) le combo numerote dans registry.json."""
    registre = lire_json(REGISTRY_PATH, {})
    entrees = registre.setdefault(CLE_COMBO, [])
    entree = {
        "id": identifiant,
        "numero": numero,
        "slug": slug,
        "nom": nom,
        "fichier": nom + "/" + DOSSIER_MAIN,
        "bdd": modele.get("id", ""),
        "description": modele.get("description", ""),
        "usage": "python main.py executer [--tag <tag>]",
        CLE_CONTRAT_VERBE: CONTRAT_COMBO_VERBE,
        CLE_CONTRAT_VERBES: list(CONTRAT_COMBO_VERBES),
        "cree_le": date,
    }
    entrees[:] = [e for e in entrees if e.get("nom") != nom]
    entrees.append(entree)
    scores = registre.setdefault(CLE_COMPTEURS, {})
    scores[PREFIXE_COMBO] = max(scores.get(PREFIXE_COMBO, 0), numero)
    ecrire_atomique(REGISTRY_PATH, json.dumps(registre, indent=2, ensure_ascii=True) + FINS_LIGNE)
    return entree


def dossiers_numerotes(dossier, reserves=DOSSIER_RESERVE):
    """Dossiers d'objets presents dans UN dossier de famille (numerotes ou pas)."""
    presents = []
    if not dossier.is_dir():
        return presents
    for chemin in sorted(dossier.iterdir()):
        if not chemin.is_dir() or chemin.name in reserves or chemin.name.startswith("."):
            continue
        presents.append(chemin.name)
    return presents


# --- Categorie : banque ----------------------------------------------------

def cmd_banque(arguments):
    """Lister la banque des BDD disponibles pour un combo."""
    banque = charger_banque()
    if banque is None:
        return 1

    entrees = banque.get(CLE_BANQUE, [])
    print("=" * 62)
    print("BANQUE DES COMBOS BDD -- " + str(len(entrees)) + " bdd(s) disponibles")
    print("=" * 62)
    for modele in entrees:
        print("  " + modele.get("id", "?").ljust(14) + " | " + modele.get("titre", ""))
        print("  " + " " * 14 + " | outil : " + modele.get("outil", ""))
        print("  " + " " * 14 + " | filtre: " + modele.get("option_filtre", "") +
              " / " + modele.get("commande_lire", ""))
        print("  " + " " * 14 + " | tags  : " + modele.get("tags_exemple", ""))
        print()
    print("Utilisation : python creer-combo.py creer <slug> --bdd <id>")
    return 0


TEMPLATE_SUPER_README = "\n".join((
    # CARTE D IDENTITE en TETE (EO-266, 2026-09-19) : le garde verifier-cartes-identite
    # exige une carte sur CHAQUE .md de la zone -- sans elle, tout sc- cree par cette
    # porte naissait HORS convention et le garde accusait chaque nouveau super-combo
    # (mesure : cartes-presentes SANS CARTE (1) sur sc-004-auto-diagnostic/README.md).
    # Le type vaut `readme` (vocabulaire FERME du garde), appartient_a est un NOM.
    "---",
    "identite:",
    "  type: readme",
    "  appartient_a: optimus-prime",
    "  commun: false",
    "---",
    "",
    "# @@NOM@@",
    "",
    "> **Super-combo numerote @@ID@@** -- le numero est OBLIGATOIRE et jamais",
    "> reutilise (contrat de nommage CV-008, BDD conventions-matrice).",
    "",
    "@@DESCRIPTION@@",
    "",
    "Phases declarees : @@PHASES@@",
    "",
    "Genere par `creer-combo.py creer-super-combo` le @@DATE@@.",
    "",
    "## Usage",
    "",
    "```bash",
    "python main.py @@VERBE@@",
    "python main.py status",
    "python main.py auto-test",
    "```",
    ""))


def enregistrer_registry_super(nom, identifiant, numero, slug, valeurs, phases, verbe, verbes):
    # Enregistrer le super-combo dans SON registre (section super-combos, compteur sc).
    registre = lire_json(REGISTRY_SUPER_PATH, {})
    entrees = registre.setdefault(CLE_SUPER_COMBO, [])
    entree = {
        "id": identifiant,
        "numero": numero,
        "slug": slug,
        "nom": nom,
        "fichier": nom + "/" + DOSSIER_MAIN,
        "description": valeurs["@@DESCRIPTION@@"],
        "phases": list(phases),
        "usage": "python main.py " + (verbe or "[verbe]") + " [--fichier <fichier>]",
        CLE_CONTRAT_VERBE: verbe,
        CLE_CONTRAT_VERBES: list(verbes),
        "cree_le": valeurs["@@DATE@@"],
    }
    entrees[:] = [e for e in entrees if e.get("nom") != nom]
    entrees.append(entree)
    scores = registre.setdefault(CLE_COMPTEURS, {})
    scores[PREFIXE_SUPER_COMBO] = max(scores.get(PREFIXE_SUPER_COMBO, 0), numero)
    ecrire_atomique(REGISTRY_SUPER_PATH, json.dumps(registre, indent=2, ensure_ascii=True) + FINS_LIGNE)
    return entree


# --- Categorie : creer -----------------------------------------------------

def cmd_creer(arguments):
    """Generer un combo NUMEROTE dedie a une BDD et l'enregistrer."""
    parser = argparse.ArgumentParser(description="Generer un combo numerote")
    parser.add_argument("slug", help="Slug du combo (ex: lecons) ou nom deja numerote (c-001-lecons)")
    parser.add_argument("--bdd", required=True, help="ID de la BDD (voir 'banque')")
    parsed = parser.parse_args(arguments)

    banque = charger_banque()
    if banque is None:
        return 1

    modele = trouver_modele(banque, parsed.bdd)
    if modele is None:
        print("BDD inconnue : " + parsed.bdd)
        print("Voir la banque : python creer-combo.py banque")
        return 1

    registre = lire_json(REGISTRY_PATH, {})
    analyse = analyser_nom(parsed.slug)
    if analyse is not None:
        prefixe, numero, slug = analyse
        if prefixe != PREFIXE_COMBO:
            print("Refus : un combo porte le prefixe '" + PREFIXE_COMBO + "-' (recu : " + parsed.slug + ")")
            return 1
    else:
        slug = parsed.slug
        prefixe = PREFIXE_COMBO
        numero = numero_suivant(registre, PREFIXE_COMBO, CLE_COMBO)

    nom = former_nom(prefixe, numero, slug)
    identifiant = former_id(prefixe, numero)
    base = REPERTOIRE_COMBOS / nom
    if base.exists():
        print("Combo deja existant : " + str(base))
        return 1

    valeurs = valeurs_combo(nom, identifiant, modele)
    contenu_main = rendre(TEMPLATE_MAIN, valeurs)
    contenu_readme = rendre(TEMPLATE_README, valeurs)

    if not est_ascii(contenu_main) or not est_ascii(contenu_readme):
        print("Generation refusee : contenu non ASCII (convention du depot)")
        return 1

    ecrire_atomique(base / DOSSIER_MAIN, contenu_main)
    ecrire_atomique(base / DOSSIER_README, contenu_readme)

    entree = enregistrer_registry(nom, identifiant, numero, slug, modele, valeurs["@@DATE@@"])

    print("Combo cree : " + str(base))
    print("  numero   : " + identifiant)
    print("  - " + DOSSIER_MAIN + " (executer / lire / status)")
    print("  - " + DOSSIER_README)
    print("  - registry.json : " + entree["id"] + " -> bdd " + entree["bdd"])
    print("\nVerifier : python creer-combo.py verifier " + nom)
    return 0


def cmd_creer_super_combo(arguments):
    # Generer un SUPER-COMBO numerote (famille sc-) et l enregistrer dans SON registre.
    parser = argparse.ArgumentParser(description="Generer un super-combo numerote")
    parser.add_argument("slug", help="Slug du super-combo (ex: auto-diagnostic)")
    parser.add_argument("--description", default="", help="But du super-combo")
    parser.add_argument("--phases", default="", help="Phases, separees par des virgules")
    parser.add_argument("--verbe", default="", help="Verbe par defaut (vide = cycle a phases)")
    parser.add_argument("--verbes", default="", help="Verbes acceptes, separes par des virgules")
    parsed = parser.parse_args(arguments)

    registre = lire_json(REGISTRY_SUPER_PATH, {})
    analyse = analyser_nom(parsed.slug)
    if analyse is not None:
        prefixe, numero, slug = analyse
        if prefixe != PREFIXE_SUPER_COMBO:
            print("Refus : un super-combo porte le prefixe " + repr(PREFIXE_SUPER_COMBO)
                  + " (recu : " + parsed.slug + ")")
            return 1
    else:
        slug = parsed.slug
        numero = numero_suivant(registre, PREFIXE_SUPER_COMBO, CLE_SUPER_COMBO)

    nom = former_nom(PREFIXE_SUPER_COMBO, numero, slug)
    identifiant = former_id(PREFIXE_SUPER_COMBO, numero)
    base = REPERTOIRE_SUPER_COMBOS / nom
    if base.exists():
        print("Super-combo deja existant : " + str(base))
        return 1

    phases = [phase.strip() for phase in parsed.phases.split(",") if phase.strip()]
    verbes = [item.strip() for item in parsed.verbes.split(",") if item.strip()]
    verbe = parsed.verbe.strip()
    if verbe and verbe not in verbes:
        print("Refus : le verbe par defaut " + repr(verbe) + " est absent de --verbes ("
              + ", ".join(verbes) + ")")
        return 1
    if not verbes:
        print("Refus : un super-combo sans --verbes serait INLANCABLE par construction (MO-071).")
        return 1

    valeurs = {
        "@@NOM@@": nom,
        "@@ID@@": identifiant,
        "@@DESCRIPTION@@": parsed.description,
        "@@PHASES@@": repr(phases),
        "@@VERBE@@": verbe,
        "@@VERBES@@": repr(verbes),
        "@@DATE@@": date_maintenant(),
    }
    contenu_main = rendre(TEMPLATE_SUPER_MAIN, valeurs)
    contenu_readme = rendre(TEMPLATE_SUPER_README, valeurs)
    if not est_ascii(contenu_main) or not est_ascii(contenu_readme):
        print("Generation refusee : contenu non ASCII (convention du depot)")
        return 1

    ecrire_atomique(base / DOSSIER_MAIN, contenu_main)
    ecrire_atomique(base / DOSSIER_README, contenu_readme)
    entree = enregistrer_registry_super(nom, identifiant, numero, slug, valeurs, phases, verbe, verbes)

    print("Super-combo cree : " + str(base))
    print("  numero   : " + identifiant)
    print("  phases   : " + ", ".join(phases))
    print("  registre : " + str(REGISTRY_SUPER_PATH.name))
    print("")
    print("Verifier : python creer-combo.py verifier " + nom)
    return 0


# --- Categorie : verifier --------------------------------------------------

def verifier_compile(base):
    """py_compile sur le main.py du combo (aucun fichier livre non compile)."""
    resultat = subprocess.run(
        [sys.executable, "-m", "py_compile", str(base / DOSSIER_MAIN)],
        capture_output=True,
        text=True,
    )
    return resultat.returncode, (resultat.stderr or "").strip()


def lire_bdd_id(base):
    """Lire l'id de BDD grave dans le main.py du combo (source unique)."""
    marqueur = "BDD_ID = "
    for ligne in (base / DOSSIER_MAIN).read_text(encoding=ENCODAGE).splitlines():
        if ligne.startswith(marqueur):
            return ligne.split(marqueur, 1)[1].strip().strip('"')
    return None


def famille_du_nom(nom):
    """Retourne (libelle, prefixe, dossier-racine, registre, cle) de la famille du nom.

    UNE famille = UN dossier + UN registre, a cote de ses objets (MO-067) : un
    nom `sc-` se juge dans super-combos/, un nom `c-` dans combos/. Le prefixe
    du nom DECIDE de la source de verite -- jamais un dossier devine a cote.
    """
    analyse = analyser_nom(nom)
    prefixe = analyse[0] if analyse else PREFIXE_COMBO
    if prefixe == PREFIXE_SUPER_COMBO:
        return ("SUPER-COMBO", prefixe, REPERTOIRE_SUPER_COMBOS, REGISTRY_SUPER_PATH,
                CLE_SUPER_COMBO)
    return "COMBO", prefixe, REPERTOIRE_COMBOS, REGISTRY_PATH, CLE_COMBO


def entree_registre(nom, chemin_registre=REGISTRY_PATH, cle=CLE_COMBO):
    """Entree du registre de la famille pour ce nom, ou None."""
    registre = lire_json(chemin_registre, {})
    for entree in registre.get(cle, []):
        if entree.get("nom") == nom:
            return entree
    return None


def numero_deja_pris(registre, numero, sauf_nom, cle=CLE_COMBO):
    """Vrai si un AUTRE objet de la famille porte deja ce numero (jamais reutilise)."""
    for entree in registre.get(cle, []):
        if entree.get("nom") != sauf_nom and entree.get("numero") == numero:
            return True
    return False


def controler_contrat_lancement(entree, nom):
    """Ecarts du CONTRAT DE LANCEMENT d'une entree de registre (MO-071, EO-114).

    Le contrat se LIT et se VERIFIE : "verbes" (la liste acceptee) non vide, et
    le "verbe" par defaut -- quand il est declare -- present dans cette liste.
    Un objet sans contrat serait inlancable : le lanceur n'a aucun verbe a
    lire, et DEVINER serait inventer. On refuse donc a la porte.
    """
    verbes = [verbe for verbe in (entree.get(CLE_CONTRAT_VERBES) or []) if verbe]
    if not verbes:
        return ["contrat de lancement absent : " + nom + " doit declarer \""
                + CLE_CONTRAT_VERBES + "\" (les verbes acceptes) dans son registre"]
    defaut = entree.get(CLE_CONTRAT_VERBE, "")
    if defaut and defaut not in verbes:
        return ["contrat de lancement incoherent : \"" + CLE_CONTRAT_VERBE + "\" = " + defaut
                + " est absent de \"" + CLE_CONTRAT_VERBES + "\" (" + ", ".join(verbes) + ")"]
    return []


def cmd_verifier(arguments):
    """Verifier un combo numerote : nom, numero, structure, compile, ASCII, registre."""
    parser = argparse.ArgumentParser(description="Verifier un combo numerote")
    parser.add_argument("nom", help="Nom du combo a verifier")
    parser.add_argument("--dossier", default=None,
                        help="Verifier un combo hors combos/ (cobaye, convention-tmp)")
    parsed = parser.parse_args(arguments)

    # MO-067 : la famille du nom decide du dossier ET du registre (jamais un
    # chemin devine) -- `sc-` vit dans super-combos/, `c-` dans combos/.
    libelle, prefixe_famille, racine_famille, registre_famille, cle_famille = famille_du_nom(parsed.nom)
    base = Path(parsed.dossier) if parsed.dossier else racine_famille / parsed.nom
    ecarts = []

    if not base.is_dir():
        print("Combo introuvable : " + str(base))
        return 1

    # 1. Numerotation obligatoire (CV-008)
    analyse = analyser_nom(parsed.nom)
    if analyse is None:
        ecarts.append("nom non numerote : attendu c-<NNN>-<slug> ou sc-<NNN>-<slug> (contrat CV-008)")
    else:
        prefixe, numero, slug = analyse
        entree = entree_registre(parsed.nom, registre_famille, cle_famille)
        if entree is None:
            ecarts.append("absent de " + registre_famille.name + " (section '" + cle_famille + "')")
        else:
            if entree.get("id") != former_id(prefixe, numero):
                ecarts.append("id du registre incoherent avec le nom : " + str(entree.get("id")))
            if entree.get("numero") != numero:
                ecarts.append("numero du registre incoherent avec le nom : " + str(entree.get("numero")))
            ecarts.extend(controler_contrat_lancement(entree, parsed.nom))
        registre = lire_json(registre_famille, {})
        if numero_deja_pris(registre, numero, parsed.nom, cle_famille):
            ecarts.append("numero deja pris par un autre " + libelle.lower() + " : " + str(numero))

    # 2. Structure
    for fichier in (DOSSIER_MAIN, DOSSIER_README):
        if not (base / fichier).exists():
            ecarts.append("fichier manquant : " + fichier)

    # 3. ASCII
    for fichier in (DOSSIER_MAIN, DOSSIER_README):
        chemin = base / fichier
        if not chemin.exists():
            continue
        try:
            texte = chemin.read_text(encoding=ENCODAGE)
        except UnicodeDecodeError:
            ecarts.append("encodage invalide : " + fichier)
            continue
        if not est_ascii(texte):
            ecarts.append("non ASCII : " + fichier)

    # 4. Compilation
    if (base / DOSSIER_MAIN).exists():
        code, erreur = verifier_compile(base)
        if code != 0:
            ecarts.append("py_compile : " + erreur)

    # 5. Outil BDD joignable (sauf cobaye hors depot, et sauf super-combo :
    # un super-combo ORCHESTRE, il n'est pas dedie a UNE BDD -- MO-067)
    if not parsed.dossier and cle_famille == CLE_COMBO:
        banque = charger_banque()
        bdd_id = lire_bdd_id(base) if (base / DOSSIER_MAIN).exists() else None
        modele = trouver_modele(banque, bdd_id) if (banque and bdd_id) else None
        if modele is None:
            ecarts.append("BDD declaree dans le main.py absente de la banque")
        else:
            outil = RACINE_MATRICE / modele.get("outil", "")
            if not outil.exists():
                ecarts.append("outil BDD injoignable : " + modele.get("outil", ""))

    if ecarts:
        print(libelle + " " + parsed.nom + " : " + str(len(ecarts)) + " ecart(s)")
        for ecart in ecarts:
            print("  - " + ecart)
        return 1

    print(libelle + " " + parsed.nom + " : conforme (numero + main + README + compile + ASCII + registre)")
    return 0


# --- Categorie : lister ----------------------------------------------------

def cmd_lister(arguments):
    """Etat numerote des DEUX familles : chacune a SON dossier et SON registre
    (MO-067) -- un objet est juge contre sa propre source de verite."""
    familles = (
        (CLE_SUPER_COMBO, "SUPER-COMBO", REGISTRY_SUPER_PATH, REPERTOIRE_SUPER_COMBOS),
        (CLE_COMBO, "COMBO", REGISTRY_PATH, REPERTOIRE_COMBOS),
    )
    ecarts = 0
    connus = []
    compteurs = {}

    for cle, libelle, chemin_registre, dossier in familles:
        registre = lire_json(chemin_registre, {})
        entrees = sorted(registre.get(cle, []), key=lambda e: e.get("numero", 0))
        reserves = DOSSIER_RESERVE_SUPER if cle == CLE_SUPER_COMBO else DOSSIER_RESERVE
        presents = dossiers_numerotes(dossier, reserves)
        print("--- " + libelle + "S (" + str(len(entrees)) + ") -- " + dossier.name
              + "/" + chemin_registre.name)
        if not entrees:
            print("  (aucun)")
        for entree in entrees:
            nom = entree.get("nom", "")
            connus.append(nom)
            if nom in presents:
                print("  " + str(entree.get("id", "?")).ljust(7) + " OK     " + nom)
            else:
                ecarts += 1
                print("  " + str(entree.get("id", "?")).ljust(7) + " ABSENT " + nom)
            for ecart in controler_contrat_lancement(entree, nom):
                ecarts += 1
                print("  ECART   " + nom + " : " + ecart)
        print()
        compteurs.update(registre.get(CLE_COMPTEURS, {}))
        for nom in presents:
            analyse = analyser_nom(nom)
            if analyse is None:
                ecarts += 1
                print("ECART : dossier NON numerote sur le disque (" + dossier.name + ") : " + nom)
            elif nom not in connus:
                ecarts += 1
                print("ECART : dossier numerote absent du registre (" + dossier.name + ") : " + nom)

    print("Compteurs (haut atteint, jamais reutilise) : " +
          ", ".join(k + "=" + str(v) for k, v in sorted(compteurs.items())))
    print("RESULTAT : " + str(ecarts) + " ecart(s)")
    return 0 if ecarts == 0 else 1


TEMPLATE_SUPER_MAIN = "\n".join((
    "#!/usr/bin/env python3",
    "# -*- coding: utf-8 -*-",
    "# @@NOM@@ -- super-combo numerote @@ID@@ (genere par creer-combo.py le @@DATE@@)",
    "# @@DESCRIPTION@@",
    "#",
    "# Phases declarees : @@PHASES@@",
    "# Usage : python main.py @@VERBE@@ | status | auto-test",
    "",
    "import sys",
    "",
    "SUPER_ID = \"@@ID@@\"",
    "SUPER_NOM = \"@@NOM@@\"",
    "DESCRIPTION = \"@@DESCRIPTION@@\"",
    "PHASES = @@PHASES@@",
    "VERBE_DEFAUT = \"@@VERBE@@\"",
    "VERBES = @@VERBES@@",
    "",
    "CODE_OK = 0",
    "CODE_ECHEC = 1",
    "",
    "",
    "def cmd_status(arguments):",
    "    # Etat de l objet : ce qu il DECLARE, et rien de plus.",
    "    print(\"Super-combo  : \" + SUPER_NOM + \" (\" + SUPER_ID + \")\")",
    "    print(\"Description  : \" + DESCRIPTION)",
    "    print(\"Phases       : \" + \", \".join(PHASES))",
    "    print(\"Verbe defaut : \" + (VERBE_DEFAUT or \"(aucun)\"))",
    "    print(\"Verbes       : \" + \", \".join(VERBES))",
    "    return CODE_OK",
    "",
    "",
    "def cmd_auto_test(arguments):",
    "    # Preuve que l objet SAIT ACCUSER : un verbe hors contrat est REFUSE.",
    "    ecarts = []",
    "    if not PHASES:",
    "        ecarts.append(\"aucune phase declaree : l objet ne dirait rien\")",
    "    if not VERBES:",
    "        ecarts.append(\"aucun verbe declare : l objet serait inlancable\")",
    "    if VERBE_DEFAUT and VERBE_DEFAUT not in VERBES:",
    "        ecarts.append(\"verbe par defaut absent de la liste : \" + VERBE_DEFAUT)",
    "    if principal([\"verbe-hors-contrat\"]) != CODE_ECHEC:",
    "        ecarts.append(\"un verbe hors contrat est ACCEPTE\")",
    "    if ecarts:",
    "        print(\"AUTO-TEST \" + SUPER_ID + \" : \" + str(len(ecarts)) + \" ecart(s)\")",
    "        for ecart in ecarts:",
    "            print(\"  - \" + ecart)",
    "        return CODE_ECHEC",
    "    print(\"AUTO-TEST \" + SUPER_ID + \" : conforme (\" + str(len(PHASES))",
    "          + \" phase(s), \" + str(len(VERBES)) + \" verbe(s))\")",
    "    return CODE_OK",
    "",
    "",
    "def principal(arguments):",
    "    # Diriger : verbe connu -> sa fonction ; verdict du contrat, jamais un silence.",
    "    if not arguments:",
    "        print(\"Usage : python main.py @@VERBE@@ | status | auto-test\")",
    "        return CODE_ECHEC",
    "    verbe = arguments[0]",
    "    if verbe == \"status\":",
    "        return cmd_status(arguments[1:])",
    "    if verbe == \"auto-test\":",
    "        return cmd_auto_test(arguments[1:])",
    "    if verbe in VERBES:",
    "        print(\"REFUS : phase \" + verbe + \" declaree mais NON IMPLEMENTEE dans \"",
    "              + SUPER_ID + \".\")",
    "        return CODE_ECHEC",
    "    print(\"REFUS : verbe inconnu : \" + verbe)",
    "    print(\"  verbes acceptes : \" + \", \".join(list(VERBES) + [\"status\", \"auto-test\"]))",
    "    return CODE_ECHEC",
    "",
    "",
    "if __name__ == \"__main__\":",
    "    sys.exit(principal(sys.argv[1:]))",
    ""))

VERBES = {
    "banque": cmd_banque,
    "creer-super-combo": cmd_creer_super_combo,
    "creer": cmd_creer,
    "verifier": cmd_verifier,
    "lister": cmd_lister,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in VERBES:
        print(__doc__)
        return 1
    return VERBES[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    sys.exit(main())
