---
# Template de Test (format Python canonique)
# Version : 0.2.0
# Statut : ebauche

test:
  nom: "test-XXX-nom-du-test"
  version: "0.2.0"
  outil_teste: "nom-de-l-outil-ou-du-garde-fou"
  cree: "2026-08-12"
  format: "python"

---

# Test: [NOM DU TEST]

## Objectif

Tester [ce que le test verifie : l outil, le garde-fou, la regle].

> **REGLE (audit 2026-08-12)** : le TEMPLATE est la reference pour chaque
> nouveau test, PAS les tests precedents. Meme si un test existant semble
> fournir un bon exemple, copier la structure depuis CE template. Un test
> ancien peut porter des derives (ex: coding utf-8, format bash) : il sera
> corrige separement.

## Emplacement

```
cerveau-projet/agents/tools/tester/tests/test-XXX-nom-du-test/test-XXX-nom-du-test.py
```

- Le nom du dossier ET du fichier commence par `test-0XX-` (numerotation
  sequentielle, jamais reutilisee).
- Chaque test est un fichier .py UNIQUE, autonome, executable directement :
  `python3 test-XXX-nom-du-test.py`.

## Structure OBLIGATOIRE du fichier .py

1. Shebang : `#!/usr/bin/env python3`
2. Coding : `# -*- coding: ascii -*-` (ASCII strict, JAMAIS utf-8)
3. Docstring `"""..."""` : nom du test + contexte/lecon qui motive le test
4. Constantes globales : `NB_POINTS = 0`, `NB_OK = 0`, `NB_KO = 0`
5. Fonction `verifier(nom, condition, detail="")` : incremente les compteurs
   et affiche `  [OK] ...` ou `  [KO] ...`
6. Fonction `run(cmd, timeout=120)` : `subprocess.run` avec
   `capture_output=True, text=True`
7. Fonctions `ascii_count(chemin)` et `crlf_count(chemin)` pour les normes
8. Fonction `main()` : les points numerotes `1.`, `2.`, ... appellent
   `verifier(...)` ; affiche `=== RESULTAT : N OK / M KO (sur P points) ===`
   et retourne `1 if NB_KO else 0`
9. `if __name__ == "__main__": sys.exit(main())`

## Canevas complet (a copier et remplir)

```python
#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-XXX-nom-du-test.py
[1-2 phrases : ce que verifie le test].

Contexte :
  - [contexte / lecon / mission qui motive ce test]
  - [regle ou anti-recurrence verifiee]
"""
import io
import os
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

# Chemins des fichiers verifies (adapter au test)
OUTIL_DIR = os.path.join(TOOLS_DIR, "categorie", "nom-outil")
OUTIL_PY = os.path.join(OUTIL_DIR, "nom-outil.py")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(cmd, timeout=120):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    print("=== [NOM DU TEST] ===")

    # 1. Version / comportement nominal
    r = run([PYTHON, OUTIL_PY, "--version"])
    verifier("1. --version affiche la version attendue",
             "vX.Y.Z" in r.stdout, r.stdout.strip())

    # 2. Fonctionnalite principale
    r = run([PYTHON, OUTIL_PY, "arg1", "arg2"])
    verifier("2. La fonctionnalite principale reussit",
             "MOTIF ATTENDU" in (r.stdout + r.stderr), r.stdout[-120:])

    # N. Normes (ASCII strict + LF pur) sur les fichiers concernes
    fichiers = [OUTIL_PY, OUTIL_MD, os.path.abspath(__file__)]
    total_non_ascii = sum(ascii_count(f) for f in fichiers)
    verifier("N. ASCII strict : 0 non-ASCII (outil + doc + test)",
             total_non_ascii == 0, "total=%d" % total_non_ascii)
    total_crlf = sum(crlf_count(f) for f in fichiers)
    verifier("N+1. LF pur : 0 CRLF (outil + doc + test)",
             total_crlf == 0, "total=%d" % total_crlf)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
```

## Checklist avant de valider un nouveau test

- [ ] Le fichier est un .py, dans `tester/tests/test-0XX-*/test-0XX-*.py`
- [ ] Shebang + `# -*- coding: ascii -*-` (JAMAIS utf-8)
- [ ] Docstring : contexte / lecon qui motive le test
- [ ] Structure copiee depuis CE template (NB_POINTS, verifier, run, main, bilan)
- [ ] Chaque point est numerote et affiche `[OK]`/`[KO]`
- [ ] Le bilan `=== RESULTAT : N OK / M KO ===` et le retour `1 if NB_KO else 0`
- [ ] ASCII strict : 0 caractere non-ASCII
- [ ] LF pur : 0 CRLF
- [ ] Le test est affecte a une serie dans tester-lancer-non-regression.py
  (constante SERIES) : sans affectation, la non-regression le signale
  hors-serie (garde-fou test-027)
- [ ] Non-regression complete verte apres ajout

## Rapports

Les tests affichent leur bilan dans la sortie standard ; le lanceur
`tester-lancer-non-regression.py` agrege les bilans en rapport markdown
(option `--rapport`).

## Historique

| Version | Date | Changements |
|---|---|---|
| 0.2.0 | 2026-08-12 | Format PYTHON canonique (audit Morpheus, demande utilisateur : le template est LA reference, pas les tests precedents). Les tests reels sont des .py purs avec [OK]/[KO] ; l ancien format bash/protections (v0.1.0) etait obsolete et inutilisable |
| 0.1.0 | 2026-08-06 | Creation : format bash avec protections (tester-protection-*) |
