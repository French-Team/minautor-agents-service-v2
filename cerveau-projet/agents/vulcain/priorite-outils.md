# Priorité de création des outils

**Agent** : Vulcain
**Date** : 2026-08-05
**Mission** : Créer tous les outils du dossier tools par ordre de priorité

---

## Principe

Les outils doivent être créés dans un ordre qui permet :
1. Les outils de base en premier (nécessaires pour les autres)
2. Les outils d'exploration ensuite (pour comprendre le projet)
3. Les outils de validation ensuite (pour vérifier le travail)
4. Les outils de correction en dernier (pour corriger les erreurs)

---

## Ordre de priorité

### Priorité 1 — Outils de base (indispensables)

| Outil | Raison | Statut |
|---|---|---|
| `verifier-systeme` | Nécessaire pour connaître le système utilisateur | À créer |
| `gerer-sous-mission` | Nécessaire pour gérer les sorties/retrées du flux | À créer |

### Priorité 2 — Outils d'exploration (comprendre le projet)

| Outil | Raison | Statut |
|---|---|---|
| `lister-dossiers` | Explorer la structure du projet | À créer |
| `lister-fichiers` | Trouver les fichiers | À créer |
| `lister-fonctions` | Comprendre le code | À créer |
| `lister-appels` | Comprendre les dépendances | À créer |
| `lister-agents` | Connaître les agents disponibles | À créer |
| `lister-outils` | Connaître les outils disponibles | À créer |

### Priorité 3 — Outils de validation (vérifier le travail)

| Outil | Raison | Statut |
|---|---|---|
| `valider-cartes-decision` | Vérifier que les agents respectent les cartes | À créer |
| `valider-liens` | Vérifier que les liens sont valides | À créer |
| `valider-nommage` | Vérifier que le nommage est correct | À créer |
| `valider-conventions` | Vérifier que les conventions sont respectées | À créer |

### Priorité 4 — Outils de correction (corriger les erreurs)

| Outil | Raison | Statut |
|---|---|---|
| `corriger-liens` | Corriger les liens cassés | À créer |
| `corriger-nommage` | Corriger le nommage | À créer |
| `modifier-agents-md` | Modifier AGENTS.md de manière fiable | À créer |

### Priorité 5 — Outils d'analyse (comprendre en profondeur)

| Outil | Raison | Statut |
|---|---|---|
| `analyser-structure` | Analyser la structure du projet | À créer |
| `analyser-dependances` | Analyser les dépendances | À créer |

---

## Processus de création pour chaque outil

### Étape 1 : Vérifier le système

```
Exécuter : verifier-systeme (si disponible)
Sinon : Utiliser des commandes de base (uname -a, etc.)
```

### Étape 2 : Lire la spécification

```
Fichier : cerveau-projet/agents/tools/[catégorie]/[outil]/spec/spec-[outil].001.01.ebauche.md
Si pas de spec : Créer une spec basique
```

### Étape 3 : Choisir la technologie

```
Critères :
1. Disponibilité sur le système (40%)
2. Performance (30%)
3. Facilité (20%)
4. Portabilité (10%)
```

### Étape 4 : Développer l'outil

```
Fichier : cerveau-projet/agents/tools/[catégorie]/[outil]/[outil].sh
Format : Script bash exécutable
```

### Étape 5 : Tester l'outil

```
1. Rendre exécutable : chmod +x [outil].sh
2. Exécuter : ./[outil].sh --aide
3. Vérifier la sortie
```

### Étape 6 : Documenter

```
1. Mettre à jour le fichier .md avec les instructions
2. Ajouter les exemples d'utilisation
3. Documenter les choix technologiques
```

---

## Suivi de progression

| # | Outil | Catégorie | Priorité | Statut | Début | Fin |
|---|---|---|---|---|---|---|
| 1 | verifier-systeme | analyser | 1 | ✅ Terminé | 2026-08-05 | 2026-08-05 |
| 2 | gerer-sous-mission | corriger | 1 | ✅ Terminé | 2026-08-05 | 2026-08-05 |
| 3 | lister-dossiers | explorer | 2 | ✅ Terminé | 2026-08-05 | 2026-08-05 |
| 4 | lister-fichiers | explorer | 2 | ✅ Terminé | 2026-08-05 | 2026-08-05 |
| 5 | lister-fonctions | explorer | 2 | ✅ Terminé | 2026-08-05 | 2026-08-05 |
| 6 | lister-appels | explorer | 2 | En attente | - | - |
| 7 | lister-agents | explorer | 2 | En attente | - | - |
| 8 | lister-outils | explorer | 2 | En attente | - | - |
| 9 | valider-cartes-decision | valider | 3 | ✅ Terminé | 2026-08-05 | 2026-08-05 |
| 10 | valider-liens | valider | 3 | ✅ Terminé | 2026-08-05 | 2026-08-05 |
| 11 | valider-nommage | valider | 3 | En attente | - | - |
| 12 | valider-conventions | valider | 3 | En attente | - | - |
| 13 | corriger-liens | corriger | 4 | ✅ Terminé | 2026-08-05 | 2026-08-05 |
| 14 | corriger-nommage | corriger | 4 | En attente | - | - |
| 15 | modifier-agents-md | corriger | 4 | En attente | - | - |
| 16 | analyser-structure | analyser | 5 | En attente | - | - |
| 17 | analyser-dependances | analyser | 5 | En attente | - | - |

---

## Règles à suivre

1. **Un outil à la fois** — Ne pas mélanger les créations
2. **Tester avant de passer** — Chaque outil doit être testé
3. **Documenter les choix** — Pourquoi cette technologie ?
4. **Respecter la portabilité** — Fonctionner sur tous les systèmes
5. **Revenir à Cerberus** — Après chaque outil créé

---

