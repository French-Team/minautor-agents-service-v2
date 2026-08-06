# Outil — Valider les Cartes de Décision

**Catégorie** : Valider
**Version** : 0.1.0-beta
**Statut** : beta
**Date création** : 2026-08-05
**Propriétaire** : Vulcain (outil partagé)

---

## Objectif

Vérifier que les agents respectent les cartes de décision dans leurs fichiers.

**Pourquoi cet outil ?**
- Les agents peuvent ne pas respecter les cartes de décision
- Les cartes peuvent être incomplètes ou incorrectes
- Cet outil automatise la vérification
- Il garantit la cohérence du système

---

## Utilisation

```
valider-cartes-decision(agent="Buffy")
valider-cartes-decision(tous="true")
valider-cartes-decision(fichier="chemin/vers/fichier.md")
```

---

## Paramètres

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `agent` | string | Non | Nom de l'agent à vérifier |
| `tous` | boolean | Non | Vérifier tous les agents |
| `fichier` | string | Non | Vérifier un fichier spécifique |

---

## Ce que l'outil vérifie

### 1. Présence de la section "Carte de Décision"

```
□ La section existe
□ Elle est placée après "Vue d'ensemble"
□ Elle contient "CARTE DE DÉCISION" en majuscules
```

### 2. Structure de la carte

```
□ Tableau "Missions disponibles" présent
□ Chaque mission a un nom
□ Chaque mission a des étapes
□ Chaque mission a des protocoles
```

### 3. Détail des missions

```
□ Chaque mission a un titre "Mission : [nom]"
□ Chaque mission a "QUAND" (condition de déclenchement)
□ Chaque mission a un tableau d'étapes
□ Chaque étape a : Action, Protocole, Sortie
```

### 4. Règles absolues

```
□ Au moins une règle absolue est définie
□ La règle est en majuscules
□ La règle est pertinente pour l'agent
```

---

## Format de sortie

### Format tableau (défaut)

```markdown
## Résultat de la validation — Agent Buffy

| Vérification | Statut | Notes |
|---|---|---|
| Section Carte de Décision | ✓ | Présente |
| Tableau Missions | ✓ | 5 missions |
| Détail des missions | ✓ | Toutes complètes |
| Règles absolues | ✓ | 2 règles |

**Verdict** : ✓ CONFORME
```

### Format détaillé

```markdown
## Résultat détaillé

### Mission : Créer un fichier

| Étape | Action | Protocole | Statut |
|---|---|---|---|
| 1 | Vérifier le nommage | convention-renommage | ✓ |
| 2 | Vérifier la structure | convention-structures | ✓ |
| 3 | Créer le fichier | - | ✓ |
| 4 | Mettre à jour l'index | - | ✓ |
```

---

## Erreurs courantes

| Erreur | Correction |
|---|---|
| Section manquante | Ajouter "## CARTE DE DÉCISION" |
| Pas de tableau missions | Ajouter tableau avec Missions/Étapes/Protocoles |
| Étape sans protocole | Ajouter protocole ou "-" si aucun |
| Pas de règle absolue | Ajouter au moins une règle en majuscules |

---

## Dépendances

- `agents/[nom]/[nom].md` — fichier de l'agent à vérifier

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Création initiale |

---

## Notes

- Cet outil est ESSENTIEL pour maintenir la qualité des cartes
- Il doit être exécuté après chaque modification de carte
- Les résultats doivent être documentés

---

