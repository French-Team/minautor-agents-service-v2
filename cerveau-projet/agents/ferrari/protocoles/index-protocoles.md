# INDEX DES PROTOCOLES -- Mecano

> **REGLE ABSOLUE** : pour chaque intervention, je suis le PARCOURS-PROTOCOLES
> (parcours-protocoles.json) qui determine l'ordre d'execution.

---

## Parcours-protocoles (GUIDE D'EXECUTION)

Le parcours-protocoles determine l'ordre exact des etapes pour chaque
intervention. LIRE le parcours, pas les protocoles au hasard.

---

## Protocoles par type de fichier (1-8, 14-20)

| Protocole | Quand le lire | Fichiers |
|---|---|---|
| [Proto 1](proto-1-agent-v2.md) | Modifier un agent v2 | fiche .md, corrections.md |
| [Proto 2](proto-2-jarvis.md) | Modifier JARVIS | jarvis.py, jarvis-server.py |
| [Proto 3](proto-3-routines.md) | Modifier les routines | routines/* |
| [Proto 4](proto-4-arbre-vs-carte.md) | Modifier un arbre | arbre-*.json, theme-*.json |
| [Proto 5](proto-5-outils-combos.md) | Modifier un outil | tools-commun/*, tools/* |
| [Proto 6](proto-6-protocoles.md) | Modifier un protocole | protocoles/* |
| [Proto 7](proto-7-regles-immuables.md) | Modifier les regles | regles/* |
| [Proto 8](proto-8-marbre.md) | Marbre | LIRE UNIQUEMENT |
| [Proto 14](proto-14-conventions.md) | Modifier conventions.md | conventions/conventions.md |
| [Proto 15](proto-15-templates.md) | Modifier un template | templates/* |
| [Proto 16](proto-16-defcon.md) | Modifier defcon-server.py | tools-commun/defcon/ |
| [Proto 17](proto-17-securite.md) | Modifier securite | tools-commun/securite/ |
| [Proto 18](proto-18-docs.md) | Modifier la documentation | docs/* |
| [Proto 19](proto-19-edith.md) | Modifier EDITH | edith/* |
| [Proto 20](proto-20-philosophie.md) | Modifier la philosophie | regles/philosophie/* |

## Protocoles transversaux (10-13) -- CHAQUE intervention

| Protocole | Quand le lire | Couvre |
|---|---|---|
| [Proto 10](proto-10-non-regression.md) | AVANT + APRES modification | Checklist non-regression |
| [Proto 11](proto-11-reordonnancement.md) | APRES modification | Ordre des elements |
| [Proto 12](proto-12-transversal.md) | AVANT + APRES intervention | Existence, canaux, historisation, perimetre, coordination, cahier |
| [Proto 13](proto-13-scripts-temporaires.md) | Creer/executer un script temporaire | Lifecycle complet + harnais obligatoire |

## Protocoles futurs

| Protocole | Quand le lire | Statut |
|---|---|---|
| [Proto 9](proto-9-harnais.md) | Harnais de securite | SPECIFICATION + combos |

## Combos harnais

| Combo | Usage |
|---|---|
| [combo-harnais-test](combos-harnais.json) | Ecrire et lancer des tests |
| [combo-harnais-edition](combos-harnais.json) | Editer des fichiers sensibles |
| [combo-harnais-modification](combos-harnais.json) | Modifier outils/protocoles |
| [combo-harnais-creation](combos-harnais.json) | Creer de nouveaux fichiers |
| [combo-harnais-reordonnancement](combos-harnais.json) | Reordonnancer un fichier |
| [combo-harnais-script-temporaire](combos-harnais.json) | Scripts temporaires (OBLIGATOIRE pour v2) |

---

## ORDRE OBLIGATOIRE (par intervention)

1. **Proto 12** : verifier existence + canaux + cahier (AVANT)
2. **Proto 1 a 8, 14 a 20** : lire le protocole du type de fichier
3. **Proto 10** : checklist non-regression (AVANT modification)
4. **Modification** (avec combo harnais si applicable)
5. **Proto 10** : checklist non-regression (APRES modification)
6. **Proto 11** : reordonnancement (APRES modification)
7. **Proto 12** : historisation + canaux + maj cahier (APRES)

---

## CAS PARTICULIERS

| Situation | Protocole(s) | Combo |
|---|---|---|
| Modifier jarvis.py | Proto 2 + 10 + 11 + 12 | harnais-modification |
| Modifier un arbre | Proto 4 + 10 + 11 + 12 | harnais-edition |
| Modifier conventions.md | Proto 14 + 10 + 11 + 12 | harnais-edition |
| Modifier regles-immuables | Proto 7 + 10 + 11 + 12 | harnais-modification |
| Modifier protocoles | Proto 6 + 10 + 11 + 12 | harnais-modification |
| Modifier templates | Proto 15 + 10 + 11 + 12 | harnais-edition |
| Modifier defcon-server | Proto 16 + 10 + 11 + 12 | harnais-modification |
| Modifier securite | Proto 17 + 10 + 11 + 12 | harnais-modification |
| Modifier docs | Proto 18 + 10 + 11 + 12 | harnais-edition |
| Modifier EDITH | Proto 19 + 1 + 10 + 11 + 12 | harnais-edition |
| Modifier philosophie | Proto 20 + 10 + 11 + 12 | harnais-edition |
| Ecrire un test | Proto 10 + 12 | harnais-test |
| Creer un fichier | Proto 1 + 10 + 11 + 12 | harnais-creation |
| Reordonnancer | Proto 11 + 12 | harnais-reordonnancement |
| Script temporaire | Proto 13 + 10 + 12 | harnais-script-temporaire |
| Lire le marbre | Proto 8 + 12 | Aucun |
| Modifier le marbre | INTERDIT | Aucun |
