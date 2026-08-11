---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# combos-maj-readme-massive

**Version :** 0.1.0
**Statut :** prepare
**Categorie :** combos
**Chemin :** `agents/tools/combos/combos-maj-readme-massive/`
**Proprietaire :** Clio (outil partage)

## Description

Combo de GROSSE mise a jour conservative du README : analyse complete
(combos-analyse-projet) -> verifier (--verifier) -> maj des compteurs (--maj)
-> correctifs de fond (nouvelles categories, badges, tables) -> verification
ASCII -> rapport final. Le mode CONSERVATIF preserve la structure du README :
on corrige les compteurs, tables et badges, on ne refond pas les sections.

## Utilisation

```bash
python3 agents/tools/combos/combos-maj-readme-massive/combos-maj-readme-massive.py [RACINE] [--rapport]
bash agents/tools/combos/combos-maj-readme-massive/combos-maj-readme-massive.sh [RACINE] [--rapport]
```

- `RACINE` : racine du projet (defaut : `.`)
- `--rapport` : sauvegarder le rapport dans `clio/rapports/maj-readme-massive-<date>.md`

## Etapes (5)

1. **Analyse** : `combos-analyse-projet` (etat reel + ecarts README)
2. **Verifier** : `mettre-a-jour-readme --verifier`
3. **Maj compteurs** : `mettre-a-jour-readme --maj`
4. **Correctifs de fond** (manuel) : nouvelles categories absentes de la table
   (lecon Clio : --maj ne cree pas les nouvelles lignes), badges du header,
   table des agents
5. **ASCII** : `valider-conformite-ascii README.md`

## Quand l'utiliser

- Gros ecarts detectes par `combos-analyse-projet`
- Refonte des tables, compteurs et badges
- Pour une PETITE MAJ (1-2 compteurs), utiliser `combo-maj-readme` a la place

## Notes

- La logique Python est la source de verite ; le .sh delegue au .py (parite).
- Piege Windows : utiliser des forward slashes dans les chemins.
- ASCII strict : aucun caractere accentue ou Unicode dans les sorties.
