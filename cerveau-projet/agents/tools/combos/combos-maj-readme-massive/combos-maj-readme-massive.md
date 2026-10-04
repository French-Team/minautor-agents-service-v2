---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# combos-maj-readme-massive

**Version :** 0.1.7
**Statut :** prepare
**Categorie :** combos
**Chemin :** `agents/tools/combos/combos-maj-readme-massive/`
**Proprietaire :** Clio (outil partage)

## Description

Combo de GROSSE mise a jour conservative du README : analyse complete
(combos-analyse-projet) -> verifier (--verifier) -> maj des compteurs (--maj)
-> correctifs de fond (nouvelles categories, tables) -> verification
ASCII -> rapport final. Les badges du header sont alignes
automatiquement (affichage ET lien href) sur leurs sources de verite :
Outils-N (compter_outils), Version-vX.Y.Z (clio/version-readme.txt),
Statut-X (clio/statut-projet.txt). Les badges statiques (Plateforme,
Fait_avec, Langages) voient leur href aligne sur l affichage. Le mode CONSERVATIF preserve la structure du README :
on corrige les compteurs, tables et badges, on ne refond pas les sections.

## Utilisation

```bash
python3 agents/tools/combos/combos-maj-readme-massive/combos-maj-readme-massive.py [RACINE] [--rapport]
bash agents/tools/combos/combos-maj-readme-massive/combos-maj-readme-massive.sh [RACINE] [--rapport]
```

- `RACINE` : racine du projet (defaut : `.`)
- `--rapport` : sauvegarder le rapport dans `clio/rapports/maj-readme-massive-<date>.md`

## Etapes (5)

> **PATTERN VERSION README** : si le README change pendant le
> combo (compteurs/badges corriges par --maj), la version dans
> `cerveau-projet/agents/clio/version-readme.txt` est bumpee
> automatiquement (increment mineur) et le rapport mentionne
> l ancienne -> nouvelle version.

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

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.6 | 2026-08-17 | MESSAGES INFORMATIONNELS : rappels apres MAJ README (version-readme.txt + badge Outils + test-020/038, Clio seule habilitee) - regle immuable v0.3.0 |
