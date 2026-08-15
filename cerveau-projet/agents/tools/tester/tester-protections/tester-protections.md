# tester-protections

Point d entree UNIQUE des protections de tests (format Python canonique).

- Version : 0.1.0
- Statut : prepare
- Proprietaire : Morpheus (outil partage)
- Emplacement : `cerveau-projet/agents/tools/tester/tester-protections/tester-protections.py`

## Pourquoi ce module

L audit 2026-08-12 (demande utilisateur) a revele que les 29 tests-0XX
n importaient AUCUNE protection : les anciennes protections
(`tester-protection-boucles-infinies`, `-erreurs-silencieuses`, `-blocage`)
etaient des wrappers autonomes (sous-processus `shell=True`), NON IMPORTABLES
depuis un test .py. Aucune protection STOP (fail-fast) n existait : quand un
point echouait, le test continuait betement les points suivants.

## Liste centrale (deploiement dynamique, v0.2.0)

Les protections vivent dans la **liste centrale**
[liste-protections.md](liste-protections.md) et sont deployees
AUTOMATIQUEMENT dans chaque test qui importe ce module (template-test.md
comme constructeur, demande utilisateur 2026-08-15) : ajouter une
protection dans `LISTE_PROTECTIONS` (tester-protections.py) la deploie
sur TOUS les tests sans toucher a leur code.

```bash
python3 tester-protections.py --liste   # affiche la liste vivante
```

Ce module fusionne les protections en une **API unique importable** :

| Protection | Detection | Action |
|---|---|---|
| boucles-infinies | Depassement delai | Arret force de l arbre + STOP |
| erreurs-silencieuses | stderr non vide, mots-cles d erreur | Signalement (le test juge) |
| blocage | Pas de reponse pendant X sec | Arret force + STOP |
| **stop** | Point critique en echec | **Arret immediat du test** (fail-fast) |

## Regle d utilisation (obligatoire)

> CHAQUE test-0XX DOIT charger les protections via `charger_protections()`.
> Le template-test.md v0.2.1 l impose ; le garde-fou test-030 le verifie.

## Import dans un test (bloc standard)

```python
import importlib.util

def charger_tester_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

PROTECTIONS = charger_tester_protections()
```

## API

### `PROTECTIONS.lancer_protege(cmd, timeout=120)`

Execute une commande SOUS PROTECTION :

- `cmd` : liste de mots (shell=False) ou chaine (shell=True)
- `timeout` : delai maximum en secondes (defaut 120)

Retourne un objet avec `.returncode`, `.stdout`, `.stderr` (compatible
`subprocess.CompletedProcess`).

Leve `ArretProtection` si le timeout expire (boucle infinie ou blocage) :
l arbre de processus est tue (cross-platform) et le test DOIT s arreter.

### `PROTECTIONS.verifier_critique(nom, condition, detail="")`

**PROTECTION STOP (fail-fast)** : verifie un point CRITIQUE du test.

- condition vraie -> affiche `[OK]` et continue
- condition fausse -> affiche `[KO]` puis LEVE `ArretProtection`

Le test s arrete immediatement au premier echec critique, au lieu de
continuer betement. Le `main()` du test attrape `ArretProtection` pour
afficher un bilan propre et retourner 1.

### `PROTECTIONS.ArretProtection`

Exception levee par les protections STOP (timeout ou point critique).

Attrapee dans `main()` :

```python
try:
    # ... points du test ...
except PROTECTIONS.ArretProtection as e:
    print("  [KO] ARRET PROTECTION : %s" % e.message)
    return 1
```

### `PROTECTIONS.VERSION`, `PROTECTIONS.PROTECTIONS_ACTIVES`

Version du module et liste des protections actives.

## CLI (execution directe)

```
python3 tester-protections.py --version
python3 tester-protections.py --liste
python3 tester-protections.py --help
```

## Exemple complet dans un test

```python
PROTECTIONS = charger_tester_protections()

def main():
    try:
        r = PROTECTIONS.lancer_protege([PYTHON, OUTIL, "--version"], timeout=60)
        verifier("1. --version fonctionne", r.returncode == 0, r.stdout)
        PROTECTIONS.verifier_critique("2. Point critique : la commande aboutit",
                                      "RESULTAT" in r.stdout, r.stdout[-80:])
    except PROTECTIONS.ArretProtection as e:
        print("  [KO] ARRET PROTECTION : %s" % e.message)
        return 1
    print("=== RESULTAT : %d OK / %d KO ===" % (NB_OK, NB_KO))
    return 1 if NB_KO else 0
```

## Historique

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-12 | Creation : point d entree unique importable (fusion des 3 protections + protection STOP fail-fast) |
