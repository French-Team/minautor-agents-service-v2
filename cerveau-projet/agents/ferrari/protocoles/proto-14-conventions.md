# PROTOCOLE 14 -- Modifier conventions.md

> Ce protocole s'applique QUAND Mecano modifie
> cerveau-projet/freelance/conventions/conventions.md.
> LIRE CE PROTOCOLE AVANT TOUTE ECRITURE.

---

## IDENTITE DU FICHIER

| Champ | Valeur |
|---|---|
| **Chemin** | cerveau-projet/freelance/conventions/conventions.md |
| **Proprietaire** | Rogers |
| **Type** | Reference centrale (SSOT) |
| **Version** | 0.2.0 |
| **Taille** | ~387 lignes |
| **Encodage** | UTF-8 + CRLF |

---

## POURQUOI CE FICHIER EST CRITIQUE

conventions.md est la SOURCE DE VERITE pour TOUTES les conventions v2.
Si ce fichier est casse, TOUS les agents v2 sont impactes.

---

## REGLE ABSOLUE

> JE NE MODIFIE JAMAIS conventions.md sans avoir VERIFIE
> que TOUS les agents v2 existants sont toujours conformes
> aux nouvelles conventions. Si une convention change,
> tous les agents et outils doivent etre verifies.

---

## AVANT de commencer

1. **Lire le fichier EN ENTIER** (~387 lignes)
2. **Verifier la version** : est-ce la derniere ?
3. **Lister les sections** : comprendre la structure
4. **Identifier ce qui va changer** : quelle section, quelle convention
5. **Verifier les agents existants** : sont-ils conformes AVANT le changement ?

---

## CE QUI EST DANS CE FICHIER

| Section | Contenu | Impact |
|---|---|---|
| FORMAT DE FICHIERS | UTF-8, CRLF, emojis | TOUT le freelance |
| NOMMAGE AGENTS | MARVEL, kebab-case | Tous les agents |
| STRUCTURE FICHIERS | Fiche, corrections, parcours | Tous les agents |
| NOMMAGE THEMES | MAJUSCULES, verbe d'action | Tous les arbres |
| NOMMAGE OUTILS | Catalogue SSOT | Tous les outils |
| NOMMAGE FICHIERS | <type>-<sujet>-<date> | Tous les produits |
| CARTE IDENTITE D17 | Frontmatter complet | Tous les fichiers |
| TEMPLATE AGENT | Structure exacte | Tout nouvel agent |
| TEMPLATE OUTIL | Structure exacte | Tout nouvel outil |
| AUTONOMIE V2 | Pas d'outils v1 | Toute la v2 |

---

## APRES modification

1. **Relire la section modifiee** : est-ce clair ?
2. **Verifier 1 agent au hasard** : est-il toujours conforme ?
3. **Verifier 1 outil au hasard** : est-il toujours conforme ?
4. **Bumper la version** : incrementer le champ version dans le frontmatter
5. **Mettre a jour le cahier de dev** : noter ce qui a change et pourquoi
6. **Signaler a Cerberus** : si le changement est majeur

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| Pas de changement de la structure D17 | Casse tous les frontmatters existants |
| Pas de changement du format de nommage | Casse tous les fichiers existants |
| Pas de changement de l'encodage | Casse tous les fichiers |
| Pas de suppression de conventions | Les agents existants en dependent |
| Pas de changement sans verification | Risque de regression massive |
