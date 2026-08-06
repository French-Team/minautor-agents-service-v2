# audit-general

Combo d'evaluation qui chainage les 4 evaluateurs et produit une synthese.

## Usage

```bash
bash audit-general.sh [DOSSIER] [--rapport]
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
