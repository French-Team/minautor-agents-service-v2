---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# combos-audit-general

**Version :** 0.2.1
**Statut :** prepare
**Categorie :** combos
**Chemin :** `agents/tools/combos/combos-audit-general/`
**Proprietaire :** Themis (outil partage)

## Description

Combo d'evaluation qui chainage les 4 evaluateurs et produit une synthese.

## Utilisation

### CLI Python (version 0.2.0-py)

```
python3 combos-audit-general.py [DOSSIER] [--rapport]

Options :
  --rapport     Sauvegarder le rapport dans themis/rapports/
  --version     Afficher la version
```

### CLI bash (version originale)

```bash
bash combos-audit-general.sh [DOSSIER] [--rapport]
```

## Options

- `--rapport` : sauvegarder le rapport dans `themis/rapports/`

## Chainage

| Etape | Evaluateur | Ce qu'il verifie |
|---|---|---|
| 1 | `evaluer-structure` | Dossiers, fichiers, arborescence |
| 2 | `evaluer-conventions` | Nommage, ASCII, format |
| 3 | `evaluer-coherence` | Liens, references, dossiers vides |
| 4 | `evaluer-agents` | Fiches, outils, declarations |

## Sortie

- Score global /100
- Severite : CRITIQUE / MAJEUR / MINEUR / INFORMATION
- Nombre d'erreurs et d'avertissements
- Tableau des scores par evaluateur

## Quand l'utiliser

- Audit post-travail (apres plusieurs agents successifs)
- Doute d'un agent (verification croisee)
- RVAV phase Analyser (protocole l'exige)

## Code retour

| Code | Signification |
|---|---|
| 0 | Le combo s'est execute (meme avec des erreurs detectees par les evaluateurs) |
| 1 | Le dossier cible n'existe pas |

## Dependances

- Les 4 evaluateurs : evaluer-structure, evaluer-conventions, evaluer-coherence, evaluer-agents

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-py | 2026-08-07 | Version Python creee (orchestrateur subprocess des 4 evaluateurs, meme logique que le .sh, base sur outil-template.py) |
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter ajoute, VERSION 0.2.0, en-tete corrige (combos-combos- -> combos-). Bug corrige : affichage des 4 scores du tableau (SCORES sur une ligne) |

---
