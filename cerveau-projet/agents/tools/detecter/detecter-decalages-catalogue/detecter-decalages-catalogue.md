# detecter-decalages-catalogue

**Version :** 0.2.0
**Categorie :** detecter
**Statut :** ebauche

## LIRE AVANT USAGE

Cet outil compare **CHAQUE entree du catalogue du generateur** (`catalogue-commandes.json`)
a l'**interface reelle** de son outil (options `--aide` puis `--help` en fallback),
pour garantir **0 decalage modele/interface** avant toute generalisation du pilote strict
(les parcours ne doivent plus contenir de commandes en dur : l'agent compose via le generateur).

## Usage

```bash
python3 detecter-decalages-catalogue.py [--sortie CHEMIN] [--version]
```

| Option | Description |
|---|---|
| `--sortie CHEMIN` | Chemin du rapport genere (defaut : `rapport-detecter-decalages-catalogue-<date>.md` dans le dossier courant) |
| `--version` | Affiche la version |
| `--aide` | Affiche cette aide |

## Sortie

Le rapport (markdown) contient :
- **Synthese** : nombre de CONFORME / DECALAGE / NON TESTABLE
- **DECALAGES** : detail de chaque entree dont un flag du modele est absent de l'aide reelle (nom, modele, flags manquants, options reelles, .md present)
- **NON TESTABLES** : outils sans aide reconnue (script absent, `--aide` et `--help` rejetes, timeout) avec la raison
- **Alertes** : placeholder obligatoire du catalogue absent du modele
- **Conformes** : liste des entrees alignees

## Classification

| Classe | Definition |
|---|---|
| CONFORME | Tous les flags du modele existent dans l'aide reelle (aide reconnue obligatoire) |
| DECALAGE | Un flag du modele est absent de l'aide reelle |
| NON TESTABLE | Pas d'aide reconnue (script absent, rejet des 2 flags, timeout) - classe honnetement, jamais conforme par defaut |

## Pieges connus (lecons 2026-08-09)

1. La regex des placeholders `{cle}` doit inclure les CHIFFRES (`[a-z_0-9]+`) sinon `{paire1}` n'est pas detecte = faux positif
2. Un test formel (`tester/tests/test-XXX`) n'a pas d'aide : classer NON TESTABLE avec justification (modele sans flag = risque nul)
3. Un outil qui rejette `--aide` ET `--help` est NON TESTABLE, jamais conforme par defaut
4. (v0.2.0) Un outil a SOUS-COMMANDES argparse (ex: generateurs-case, generateurs-ligne) cache ses flags dans les sous-commandes : l'aide racine seule cree des FAUX POSITIFS. Depuis la v0.2.0, le scan lance aussi l'aide de chaque sous-commande (bloc `{sous-cmd1,...}` de l'aide racine) et fusionne les options

## Historique

| Version | Date | Description |
|---|---|---|
| 0.2.0 | 2026-08-12 | SCAN DES SOUS-COMMANDES argparse (round 11 coherence documentaire) : fusion des options des sous-commandes - corrige les faux positifs generateurs-case-convertir / generateurs-ligne |
| 0.1.0 | 2026-08-09 | Institutionnalisation du scan ecrit par Atlas (explorations/) - deplacement vers tools/detecter/, identite, --sortie, RACINE 6 niveaux |
