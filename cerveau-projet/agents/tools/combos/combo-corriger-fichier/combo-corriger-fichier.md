---
identite:
  type: combo
  appartient_a: commun
  commun: true
---
# combo-corriger-fichier

**Version :** 0.1.0
**Statut :** prepare
**Categorie :** combos
**Chemin :** `agents/tools/combos/combo-corriger-fichier/`
**Definition :** `agents/tools/combos/combo-corriger-fichier/definition-combo.json`

## Description

Correction complete d'un fichier du cerveau en UN lancer : enchaine les 6
outils de correction/nettoyage sur le meme fichier (Pattern 3 - la carte
allegee lance UN combo au lieu d'une suite d'outils).

Suite encapsulee (anciennes cases c12+c13 de la carte de Buffy) :

```
corriger-nommage -> corriger-liens -> corriger-emojis
-> corriger-accents-zones-sensibles -> condenser-fichier -> nettoyer-fichier
```

## Utilisation

```bash
# Le fichier a corriger est passe en variable initiale
python3 cerveau-projet/agents/tools/combos/combos-moteur/combos-moteur.py \
  cerveau-projet/agents/tools/combos/combo-corriger-fichier/definition-combo.json \
  --var fichier=<chemin>
```

## Cases

| Case | Type | Outil execute | Sortie |
|---|---|---|---|
| c1 | outil | corriger-nommage `{fichier}` | resultat_nommage |
| c2 | outil | corriger-liens `{fichier}` | resultat_liens |
| c3 | outil | corriger-emojis `{fichier}` | resultat_emojis |
| c4 | outil | corriger-accents-zones-sensibles `{fichier}` | resultat_accents |
| c5 | outil | condenser-fichier `{fichier}` | resultat_condense |
| c6 | outil | nettoyer-fichier `{fichier}` | resultat_nettoye |
| c7 | fin | - | message de cloture |

## Pourquoi un combo ?

| Avant (suite dans la carte) | Apres (1 case de carte) |
|---|---|
| 6 indices outil dans 2 cases (c12 + c13) | 1 case `Lancer le combo corriger-fichier` (c37) |
| L'agent enchaine 6 commandes a la main | L'agent lance combos-moteur une fois |
| Plus de surface de derive | Moins d'etapes a sauter |

## Regles

1. TOUJOURS citer le combo avant de le lancer (regle tracabilite) : nom +
   chemin de la definition.
2. La variable `fichier` est OBLIGATOIRE (--var fichier=<chemin>) : le
   fichier modifie par la mission, dans le workspace.
3. Le combo s'insere dans le flux : apres la modification (generateurs-case
   ou editer-fichier) et avant le controle des impacts (combo-controle-impacts).

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-08 | Creation : encapsule les 6 outils de correction/nettoyage (alleger la carte de Buffy, Pattern 3) |
