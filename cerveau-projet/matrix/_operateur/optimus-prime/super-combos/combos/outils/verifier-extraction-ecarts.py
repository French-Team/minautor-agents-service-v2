#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier-extraction-ecarts.py -- Garde : tout FILTRE d extraction a un PRODUCTEUR imprime.

Pourquoi (lecon L-163, MO-382 / MO-383 / MO-384) : un extracteur qui filtre la
SORTIE d un garde par un prefixe que ce garde n imprime JAMAIS rend un ROUGE MUET
-- le verdict sait QUE quelque chose a echoue, jamais QUOI. Mesure du 2026-09-22 :
le lanceur de non-regression portait DEUX fois le meme defaut (les maillons 34 et
35 cherchaient `KO]` quand les gardes impriment `[KO`), et personne ne le voyait
car la cause ecrite par le garde etait perdue au dernier metre de la LECTURE.

CE QU'IL EXIGE :
  1. UN PRODUCTEUR : tout filtre d extraction applique a la sortie decoupee en
     lignes doit etre le DEBUT d une ligne qu un fichier de la Matrice IMPRIME --
     convention `controler()` (qui imprime `[OK]` / `[KO]`) ou premier litteral
     d un `print`. Sans producteur, le filtre est ACCUSE avec son fichier et sa
     ligne.
  2. DES EXEMPTIONS NOMMEES : certains filtres ne visent PAS une ligne de statut
     mais un DOCUMENT (markdown, aide, indentation). Ils sont exemptes, et CHAQUE
     exemption porte son MOTIF (doctrine des exemptions visibles, MO-075) : une
     exemption muette serait un angle mort -- c est exactement le defaut que ce
     garde surveille.
  3. LA COUVERTURE SE MESURE : un plancher DECLARE de sites lus. En dessous, le
     garde DIT que sa MESURE est cassee au lieu de rendre un vert muet (un
     controle qui ne lit rien est un controle qui passe).
  4. LA CAUSE EST UNE ACCUSATION : chaque ecart est imprime sur une ligne
     commencant par `[KO]`, comme les autres gardes de la famille. Une cause
     ecrite en clair mais HORS du format que l appelant extrait serait -- encore
     -- un rouge muet, et ce garde se l interdirait a lui-meme.

CE QU'IL NE FAIT PAS : aucune ecriture, aucun etat modifie. Il lit le .py de la
Matrice (zones jetables, caches et points de restauration EXCLUS) et appelle des
fonctions PURES. L auto-test ne touche a aucun fichier.

LIMITE DITE : la mesure des producteurs est STATIQUE. Un garde qui imprime par une
variable composee, ou qui ecrit sur la sortie sans `print`, peut etre declare MUET
a tort -- c est pourquoi l exemption est la VOIE DE DROIT et se NOMME, jamais un
silence.

Usage: python verifier-extraction-ecarts.py [--racine <path>] [--auto-test]
  code 0 = sain, 1 = ecart (imprime [KO] et nomme le coupable), 2 = racine introuvable.
"""

import argparse
import re
import sys
from pathlib import Path

# Les domiciles : declares UNE fois, jamais recopies dans la logique.
DOSSIER_COMMUN = Path("matrice") / "data" / "commun" / "racine.py"
DOSSIER_PILOTE = Path("_operateur") / "optimus-prime" / "pilote" / "commun.py"

DOSSIERS_IGNORES = ("__pycache__",)
PREFIXE_ZONE_JETABLE = "tmp-"
MARQUEUR_BAK = ".bak."
# La fenetre de lecture d un site : le filtre peut vivre a la ligne suivante
# (une comprehension Python se replie), jamais a plus de quelques lignes.
FENETRE_LECTURE = 240

# Marqueurs du PRODUCTEUR : la convention `controler()` et l appel `print`.
MARQUEUR_CONTROLEUR = "def controler("
PREFIXES_CONTROLEUR = ("[OK", "[KO")
MOTIF_PRINT = re.compile(r'print\(\s*(?:f?)("([^"]*)"|\x27([^\x27]*)\x27)')

# Le SITE d extraction : une sortie decoupee en lignes, filtree par un prefixe.
MOTIF_SITE = re.compile(r'splitlines\(\)[\s\S]{0,' + str(FENETRE_LECTURE)
                        + r'}?startswith\(\s*(\([^)]*\)|"[^"]*"|\x27[^\x27]*\x27)')
MOTIF_LITTERAL = re.compile(r'"([^"]*)"|\x27([^\x27]*)\x27')

# LES EXEMPTIONS DECLAREES : filtre -> MOTIF (doctrine MO-075 : jamais un silence).
EXEMPTIONS = {
    "#": "parseur de DOCUMENT (lignes de markdown ou de commentaire)",
    "```": "parseur de DOCUMENT (bloc de code markdown)",
    "## Encart : ": "parseur de DOCUMENT (titre d encart markdown)",
    "usage": "parseur d AIDE (bloc Usage d un outil)",
    "  ": "parseur d INDENTATION (lignes indentees d un rapport)",
}

# Le PLANCHER de couverture : mesure du 2026-09-22, 67 sites vivent dans la
# Matrice. Le plancher est DECLARE et volontairement bas (marge pour les
# refactorings) : tres en dessous, la MESURE est cassee, pas le code.
COUVERTURE_MIN = 40

RESULTATS = []


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def accuser(detail):
    """Imprime un ECART dans le FORMAT que l appelant extrait ([KO] ...).

    Sans cette forme, la cause serait ecrite et l appelant ne l extrairait pas :
    le rouge muet (L-163) reproduit par le garde cense l empecher.
    """
    print("[KO] " + detail)


def commence_par(texte, marqueur):
    """True si `texte` COMMENCE par `marqueur` (jamais un startswith litteral :
    ce garde ne doit pas etre son propre site d extraction)."""
    return texte[:len(marqueur)] == marqueur


def trouver_racine(depart):
    """Le dossier qui porte la Matrice, ou None."""
    for candidat in (depart, depart / "cerveau-projet" / "matrix", depart / "matrix"):
        if (candidat / DOSSIER_COMMUN).is_file() or (candidat / DOSSIER_PILOTE).is_file():
            return candidat
    return None


def est_en_champ(chemin, racine):
    """True si le fichier est du CODE en champ (hors garde, zones jetables, caches)."""
    try:
        parties = chemin.relative_to(racine).parts
    except ValueError:
        return False
    if chemin.name == Path(__file__).name:
        return False
    if MARQUEUR_BAK in chemin.name:
        return False
    for partie in parties[:-1]:
        if partie in DOSSIERS_IGNORES or commence_par(partie, PREFIXE_ZONE_JETABLE):
            return False
    return True


def prefixes_imprimes(texte):
    """Les prefixes de lignes qu un fichier IMPRIME (convention controler + print)."""
    prefixes = set()
    if MARQUEUR_CONTROLEUR in texte:
        prefixes |= set(PREFIXES_CONTROLEUR)
    for morceaux in MOTIF_PRINT.finditer(texte):
        valeur = morceaux.group(2) if morceaux.group(2) is not None else (morceaux.group(3) or "")
        litteral = valeur.split("{")[0].lstrip()
        if litteral:
            prefixes.add(litteral)
    return prefixes


def extraire_sites(texte):
    """[(ligne, [filtres])] : les extractions appliquees a une sortie decoupee en lignes."""
    sites = []
    for morceaux in MOTIF_SITE.finditer(texte):
        filtres = []
        for double, simple in MOTIF_LITTERAL.findall(morceaux.group(1)):
            valeur = double or simple
            if valeur:
                filtres.append(valeur)
        if filtres:
            sites.append((texte[:morceaux.start()].count("\n") + 1, filtres))
    return sites


def filtres_sans_producteur(sites, producteurs, exemptions):
    """[(ligne, filtre)] : les filtres NON exempts qu AUCUN producteur ne commence."""
    manquants = []
    for ligne, filtres in sites:
        for filtre in filtres:
            if filtre in exemptions:
                continue
            if not any(commence_par(prefixe, filtre) for prefixe in producteurs):
                manquants.append((ligne, filtre))
    return manquants


def auto_test():
    """Le MEME detecteur doit MORDRE, et EPARGNER le legitime (lecon L-032)."""
    producteurs = {"[OK", "[KO", "ECART : "}
    texte = (
        'ecarts = [l.strip() for l in r.stdout.splitlines()\n'
        '          if l.strip().startswith(("[KO", "ZZ-BIDON"))]\n'
        'doc = [l for l in t.splitlines() if l.startswith("#")]\n'
        'aide = [l for l in s.splitlines() if l.startswith("usage")]\n'
    )
    sites = extraire_sites(texte)
    manquants = filtres_sans_producteur(sites, producteurs, EXEMPTIONS)
    accuses = sorted(filtre for _, filtre in manquants)
    attendus = ["ZZ-BIDON"]
    mord = accuses == attendus
    print("cobaye extraction : accuse " + str(accuses) + " (attendu : " + str(attendus)
          + ") -- mord : " + str(mord))
    print("cobaye exemptions : '#' et 'usage' epargnes, 'ZZ-BIDON' seul accuse : "
          + str(mord and len(manquants) == 1))
    return mord and len(manquants) == 1


def main():
    parseur = argparse.ArgumentParser(
        description="Garde : tout filtre d extraction a un producteur imprime.")
    parseur.add_argument("--racine", default=".", help="racine du depot")
    parseur.add_argument("--auto-test", action="store_true", help="ne joue que le cobaye")
    arguments = parseur.parse_args()
    racine = trouver_racine(Path(arguments.racine).resolve())
    if racine is None:
        print("ECART : racine introuvable (ni matrice/data/commun, ni _operateur/optimus-prime).")
        return 2
    if arguments.auto_test:
        ok = auto_test()
        print("\nVERDICT : " + ("OK" if ok else "KO"))
        return 0 if ok else 1

    fichiers = [p for p in sorted(racine.rglob("*.py")) if est_en_champ(p, racine)]
    textes = {}
    producteurs = set()
    for chemin in fichiers:
        contenu = chemin.read_text(encoding="utf-8", errors="replace")
        textes[chemin] = contenu
        producteurs |= prefixes_imprimes(contenu)

    sites = 0
    manquants = []
    for chemin in fichiers:
        trouves = extraire_sites(textes[chemin])
        sites += len(trouves)
        for ligne, filtre in filtres_sans_producteur(trouves, producteurs, EXEMPTIONS):
            manquants.append((chemin.relative_to(racine), ligne, filtre))

    # La CAUSE est accuse AVANT les controles : elle porte le format extrait par
    # l appelant (lecon L-163), et elle est plus precise que le resume qui suit.
    for relatif, ligne, filtre in manquants:
        accuser("filtre-sans-producteur : " + str(relatif) + ":" + str(ligne)
                + " filtre " + repr(filtre))
    if sites < COUVERTURE_MIN:
        accuser("couverture-de-la-mesure : " + str(sites) + " site(s) lus (< "
                + str(COUVERTURE_MIN) + ") -- la MESURE est cassee, pas le code")

    controler("filtres-d-extraction-avec-producteur", not manquants,
              str(len(manquants)) + " filtre(s) sans producteur sur " + str(sites) + " site(s)")
    controler("couverture-de-la-mesure", sites >= COUVERTURE_MIN,
              str(sites) + " site(s) lus (plancher declare : " + str(COUVERTURE_MIN) + ")")
    cobaye_ok = auto_test()
    if not cobaye_ok:
        accuser("cobaye : le detecteur n a pas mordu -- le garde serait vert par construction")

    if manquants or sites < COUVERTURE_MIN or not cobaye_ok:
        print("\nVERDICT KO : la cause est NOMMEE ci-dessus, sur les lignes [KO].")
        return 1
    print("\nVERDICT OK : tout filtre d extraction a un PRODUCTEUR imprime, ou est exempte et DIT.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
