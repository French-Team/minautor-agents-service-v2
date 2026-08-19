---
identite:
  type: outil
  appartient_a: commun
  commun: true
  tags: consultation, combos, catalogue
---
# consulter-combos

**Version :** 0.1.0
**Statut :** prepare
**Categorie :** consulter
**Chemin :** `agents/tools/consulter/consulter-combos/`
**Proprietaire :** Vulcain (outil partage)

## Description

Consulte le catalogue central des combos (`catalogue-combos.json`, source de
verite creee le 2026-08-19) pour repondre a la question : **ou est utilise
l outil X et par qui ?** Il croise le catalogue (combos -> membres) avec les
fiches outils (champ `combos` du frontmatter).

## Utilisation

```bash
python3 consulter-combos.py --outil evaluer-coherence
python3 consulter-combos.py --combo combos-audit-general
python3 consulter-combos.py --tous
```

## Options

| Option | Description |
|---|---|
| `--outil <nom>` | Afficher les combos qui utilisent cet outil (+ proprietaire) |
| `--combo <nom>` | Afficher les membres d un combo (+ proprietaire) |
| `--tous` | Afficher tout le catalogue |
| `--agent <nom>` | Agent qui consulte (journalise dans le registre) |
| `--rapport <f>` | Ecrire un rapport markdown |
| `--version` | Afficher la version |
| `--aide` | Afficher l aide |

## Exemple

```bash
python3 consulter-combos.py --outil evaluer-coherence
# === Outil : evaluer-coherence ===
# Utilise par 1 combo(s) :
#   - combos-audit-general (proprietaire : themis)
```

## Source de verite

- `catalogue-combos.json` : chaque combo -> proprietaire + outils membres.
- Les fiches outils membres portent le champ `combos:` dans leur frontmatter
  (declaration inverse, synchronisee par le test garde-fou).

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-19 | Creation (mission lacune combo->outils) : consultation du catalogue-combos.json, reponse "ou est utilise X et par qui" |
