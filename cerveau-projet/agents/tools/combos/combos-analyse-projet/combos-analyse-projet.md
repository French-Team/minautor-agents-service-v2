---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# combos-analyse-projet

**Version :** 0.1.3
**Statut :** prepare
**Categorie :** combos
**Chemin :** `agents/tools/combos/combos-analyse-projet/`
**Proprietaire :** Clio (outil partage)

## Description

Combo d'analyse qui mesure l'etat reel du projet (agents, outils par categorie)
et le compare aux README : badge Outils et compteur agents dans README.md,
table des categories dans readme-dev.md section 6 (la table a quitte le README
public lors de la refonte grand public). Produit un rapport d'ecarts. C'est la PREMIERE etape avant toute mise a
jour du README : savoir CE QUI A CHANGE avec precision (Pattern 3).

## Utilisation

```bash
python3 agents/tools/combos/combos-analyse-projet/combos-analyse-projet.py [RACINE] [--rapport]
bash agents/tools/combos/combos-analyse-projet/combos-analyse-projet.sh [RACINE] [--rapport]
```

- `RACINE` : racine du projet (defaut : `.`)
- `--rapport` : sauvegarder le rapport dans `clio/rapports/analyse-projet-<date>.md`

## Sorties

- **Etat reel** : agents reels, outils reels, outils par categorie
- **Ecarts README vs realite** : badge Outils + compteur agents (README.md),
  categories absentes ou compteur different (readme-dev.md section 6)
- **Verdict** : A CORRIGER (avec liste des ecarts) ou A JOUR

## Enchainer

- **Aucun ecart** : README a jour, pas de correction necessaire.
- **Petits ecarts** (1-2 compteurs) : `combo-maj-readme` (encapsule).
- **Gros ecarts / refonte** : `combos-maj-readme-massive` (orchestre).

## Notes

- La logique Python est la source de verite ; le .sh delegue au .py (parite).
- Piege Windows : utiliser des forward slashes dans les chemins.
- ASCII strict : aucun caractere accentue ou Unicode dans les sorties.
