---
identite:
  type: routine
  appartient_a: matrice
  commun: true
  version: 1
  date: 2026-09-23
  liens: matrice/templates/carte-identite/README.md, matrice/data/commun/carte_identite.py
---

# verifier-liens-cartes

Mesure le GRAPHE DES LIENS des cartes d identite du corpus : liens morts, liens
non reciproques, liens fautifs ou egocentriques, et COUVERTURE des liens.

## Fonctionnement

- Cadence declaree : 3600 s. Elle est DECLAREE dans `constants.py`, publiee a
  chaque passe dans `verifier-liens-cartes-etat.json` et MESUREE par
  `verifier-cadence` : declarer ne suffit pas.
- La passe est `passe/fonctions.passer()`. Elle lit les cartes par le DOMICILE de
  la grammaire (`matrice/data/commun/carte_identite.py`) et juge la forme des
  chemins par `matrice/data/commun/cible.py` : rien n est devine, tout est
  consomme (M-076).
- Le controle que le GARDE des cartes ne fait pas : le RETOUR. Si A nomme B,
  B doit nommer A -- c est ce qui permet de retrouver les fichiers CONNECTES a
  celui qu on doit modifier (EO-347, demande createur du 2026-09-23).
- Le rapport complet vit dans `rapport-liens.json` (comptes + anomalies) ; les
  messages affiches sont le resume, et les anomalies BORNEES (anti-spam).

## Fichiers d etat

| Fichier | Role |
|---|---|
| `verifier-liens-cartes.pid` | PID du demon (jamais ecrit par `--once`) |
| `verifier-liens-cartes.arret` | drapeau d arret cooperatif |
| `verifier-liens-cartes-etat.json` | etat court de la derniere passe (temoin de cadence) |
| `rapport-liens.json` | rapport long : comptes du graphe + anomalies detaillees |
| `provenance.json` | marqueur de provenance (origine moule) |
