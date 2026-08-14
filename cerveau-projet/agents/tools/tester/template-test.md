---
# Template de Test (format Python canonique)
# Version : 0.3.0
# Statut : ebauche

test:
  nom: "test-XXX-nom-du-test"
  version: "0.3.0"
  outil_teste: "nom-de-l-outil-ou-du-garde-fou"
  cree: "2026-08-13"
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

> **REGLE PROTECTIONS (demande utilisateur 2026-08-12)** : CHAQUE test DOIT
> charger les protections via le point d entree unique `tester-protections`
> (bloc OBLIGATOIRE ci-dessous). Les anciennes protections (tester-protection-*)
> sont des wrappers non importables : le module `tester-protections` les
> fusionne en une API importable (lancer_protege + protection STOP).

> **REGLE IMMUABLE PROTECTIONS + OPTIONS + CHRONO (demande utilisateur
> 2026-08-13)** : TOUT fichier contenant des fonctions, des tests ou des
> workflows DOIT embarquer : (a) des PROTECTIONS (anti-erreurs, anti-blocage),
> (b) des OPTIONS on/off (--isoler / --desactiver pour isoler un test, une
> fonction ou un workflow complet sans toucher au code), (c) un CHRONO
> (--no-chrono pour couper, bilan de duree par etape en fin). Les temps
> mesures alimenteront les futurs outils de suivi (detecter les lenteurs,
> ameliorer les procedures). Le TEMPLATE impose le triplet ci-dessous.

## Emplacement

```
cerveau-projet/agents/tools/tester/tests/test-XXX-nom-du-test/test-XXX-nom-du-test.py
```

- Le nom du dossier ET du fichier commence par `test-0XX-` (numerotation
  sequentielle, jamais reutilisee).
- Chaque test est un fichier .py UNIQUE, autonome, executable directement :
  `python3 test-XXX-nom-du-test.py`.

## Options on/off du test (regle immuable v0.3.0)

| Option | Effet | Usage |
|---|---|---|
| `--no-chrono` | Desactive le chrono (defaut : actif) | Diagnostic sans mesure |
| `--isoler N` | N execute QUE le point N | Isoler un test/point qui echoue |
| `--desactiver 1,3,5` | Saute les points listes | Desactiver des points sans toucher au code |

Le test reste **vert au lanceur sans option** : ces options sont des leviers
de diagnostic et d'integration pour les futurs outils de suivi (isoler un
test, desactiver une fonction ou un workflow complet).

## Structure OBLIGATOIRE du fichier .py

1. Shebang : `#!/usr/bin/env python3`
2. Coding : `# -*- coding: ascii -*-` (ASCII strict, JAMAIS utf-8)
3. Docstring `"""..."""` : nom du test + contexte/lecon qui motive le test
4. Constantes globales : `NB_POINTS = 0`, `NB_OK = 0`, `NB_KO = 0`
5. **Options on/off + chrono (v0.3.0)** : `CHRONO_ACTIF`, `ISOLE`,
   `DESACTIVES` (parsing de sys.argv), `DEBUT_TEST`, `ETAPES`, fonctions
   `point_actif(numero)` et `chrono_etape(nom, t_debut)`, `bilan_chrono()`
6. **Import OBLIGATOIRE des protections** : `PROTECTIONS = charger_protections()`
   (bloc standard ci-dessous) - le garde-fou test-030 verifie sa presence
7. Fonction `verifier(nom, condition, detail="")` : incremente les compteurs
   et affiche `  [OK] ...` ou `  [KO] ...`
8. Fonction `run(cmd, timeout=120)` : retourne `PROTECTIONS.lancer_protege(cmd,
   timeout)` (sous protection : timeout + tuer l arbre + erreurs silencieuses)
9. Fonctions `ascii_count(chemin)` et `crlf_count(chemin)` pour les normes
10. Fonction `main()` : les points numerotes `1.`, `2.`, ... appellent
    `verifier(...)` (chaque point demarre par `if point_actif(N):` et mesure
    sa duree via `chrono_etape`) ; les points CRITIQUES appellent
    `PROTECTIONS.verifier_critique(...)` (protection STOP) ; le tout dans un
    `try/except PROTECTIONS.ArretProtection` ; affiche
    `bilan_chrono()` PUIS `=== RESULTAT : N OK / M KO (sur P points) ===`
    et retourne `1 if NB_KO else 0`
11. `if __name__ == "__main__": sys.exit(main())`

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
import importlib.util
import io
import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

# Chemins des fichiers verifies (adapter au test)
OUTIL_DIR = os.path.join(TOOLS_DIR, "categorie", "nom-outil")
OUTIL_PY = os.path.join(OUTIL_DIR, "nom-outil.py")
OUTIL_MD = os.path.join(OUTIL_DIR, "nom-outil.md")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N (diagnostic cible)
#   --desactiver 1,3,5     saute les points listes (sans toucher au code)
# ------------------------------------------------------------------
CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for i, arg in enumerate(sys.argv):
    if arg == "--isoler" and i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[i + 1])
        except ValueError:
            ISOLE = None
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        DESACTIVES = [int(x) for x in sys.argv[i + 1].split(",")
                      if x.strip().isdigit()]

DEBUT_TEST = time.monotonic()
ETAPES = []  # (nom, duree_secondes) alimente le bilan chrono


def charger_protections():
    """Importe le point d entree unique des protections (test-030 le verifie)."""
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def point_actif(numero):
    """True si le point N doit s executer (options on/off du test)."""
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    """Enregistre la duree d une etape (no-op si --no-chrono)."""
    if CHRONO_ACTIF:
        ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    """Affiche le bilan des durees : total + detail par etape."""
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - DEBUT_TEST
    detail = " | ".join("%s=%.2fs" % e for e in ETAPES)
    print("=== CHRONO : total %.2fs (%s) ===" % (total, detail))


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
    return PROTECTIONS.lancer_protege(cmd, timeout=timeout)


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def main():
    global NB_POINTS, NB_OK, NB_KO
    print("=== [NOM DU TEST] ===")
    try:
        # 1. Version / comportement nominal (chronometre)
        if point_actif(1):
            t = time.monotonic()
            r = run([PYTHON, OUTIL_PY, "--version"])
            verifier("1. --version affiche la version attendue",
                     "vX.Y.Z" in r.stdout, r.stdout.strip())
            chrono_etape("1. version", t)

        # 2. Fonctionnalite principale (point CRITIQUE -> protection STOP)
        if point_actif(2):
            t = time.monotonic()
            r = run([PYTHON, OUTIL_PY, "arg1", "arg2"])
            PROTECTIONS.verifier_critique(
                "2. La fonctionnalite principale reussit (STOP si echec)",
                "MOTIF ATTENDU" in (r.stdout + r.stderr), r.stdout[-120:])
            chrono_etape("2. fonctionnalite", t)

        # 3. Normes (ASCII strict + LF pur) sur les fichiers concernes
        if point_actif(3):
            t = time.monotonic()
            fichiers = [OUTIL_PY, OUTIL_MD, os.path.abspath(__file__)]
            total_non_ascii = sum(ascii_count(f) for f in fichiers)
            verifier("3. ASCII strict : 0 non-ASCII (outil + doc + test)",
                     total_non_ascii == 0, "total=%d" % total_non_ascii)
            total_crlf = sum(crlf_count(f) for f in fichiers)
            verifier("4. LF pur : 0 CRLF (outil + doc + test)",
                     total_crlf == 0, "total=%d" % total_crlf)
            chrono_etape("3. normes", t)
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        NB_KO += 1

    print("")
    bilan_chrono()
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
- [ ] **Protections importees** : bloc `PROTECTIONS = charger_protections()`
  present (point d entree unique `tester-protections`)
- [ ] **Options on/off + chrono (v0.3.0)** : `CHRONO_ACTIF`/`ISOLE`/`DESACTIVES`
  + fonctions `point_actif`, `chrono_etape`, `bilan_chrono` presents
- [ ] Chaque point demarre par `if point_actif(N):` et mesure sa duree
  via `chrono_etape` ; `bilan_chrono()` affiche avant le `=== RESULTAT ===`
- [ ] `run()` passe par `PROTECTIONS.lancer_protege` (timeout + tuer l arbre)
- [ ] Points critiques via `PROTECTIONS.verifier_critique` + `try/except
  ArretProtection` dans main (protection STOP)
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
(option `--rapport`). Les durees `=== CHRONO ===` affichees par chaque test
sont la matiere premiere des futurs outils de suivi de performance.

## Historique

| Version | Date | Changements |
|---|---|---|
| 0.3.0 | 2026-08-13 | REGLE IMMUABLE PROTECTIONS + OPTIONS + CHRONO (demande utilisateur) : options on/off `--isoler`/`--desactiver` + chrono par etape `--no-chrono`/`chrono_etape`/`bilan_chrono`/`point_actif` dans le canevas et la checklist. Les tests EXISTANTS ne sont PAS migres (decision utilisateur) ; le triplet s impose aux FUTURS tests. Ajout OUTIL_MD manquant dans le canevas. CORRECTION BUG LATENT (decouvert par le premier test conforme test-044) : `global NB_POINTS, NB_OK, NB_KO` en tete de main() - sans lui, `NB_KO += 1` dans le except rendait NB_KO local et le bilan final levait UnboundLocalError |
| 0.2.1 | 2026-08-12 | Import OBLIGATOIRE des protections via le point d entree unique tester-protections (lancer_protege + protection STOP verifier_critique/ArretProtection) - demande utilisateur : chaque test DOIT etre protege |
| 0.2.0 | 2026-08-12 | Format PYTHON canonique (audit Morpheus, demande utilisateur : le template est LA reference, pas les tests precedents). Les tests reels sont des .py purs avec [OK]/[KO] ; l ancien format bash/protections (v0.1.0) etait obsolete et inutilisable |
| 0.1.0 | 2026-08-06 | Creation : format bash avec protections (tester-protection-*) |
