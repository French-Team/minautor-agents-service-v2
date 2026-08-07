# Priorite de creation des outils

**Agent** : Vulcain
**Date** : 2026-08-05
**Mission** : Creer tous les outils du dossier tools par ordre de priorite

---

## Principe

Les outils doivent etre crees dans un ordre qui permet :
1. Les outils de base en premier (necessaires pour les autres)
2. Les outils d'exploration ensuite (pour comprendre le projet)
3. Les outils de validation ensuite (pour verifier le travail)
4. Les outils de correction en dernier (pour corriger les erreurs)

---

## Ordre de priorite

### Priorite 1 -- Outils de base (indispensables)

| Outil | Raison | Statut |
|---|---|---|
| `verifier-systeme` | Necessaire pour connaitre le systeme utilisateur | A creer |
| `gerer-sous-mission` | Necessaire pour gerer les sorties/retrees du flux | A creer |

### Priorite 2 -- Outils d'exploration (comprendre le projet)

| Outil | Raison | Statut |
|---|---|---|
| `lister-dossiers` | Explorer la structure du projet | A creer |
| `lister-fichiers` | Trouver les fichiers | A creer |
| `lister-fonctions` | Comprendre le code | A creer |
| `lister-appels` | Comprendre les dependances | A creer |
| `lister-agents` | Connaitre les agents disponibles | A creer |
| `lister-outils` | Connaitre les outils disponibles | A creer |

### Priorite 3 -- Outils de validation (verifier le travail)

| Outil | Raison | Statut |
|---|---|---|
| `valider-cartes-decision` | Verifier que les agents respectent les cartes | A creer |
| `valider-liens` | Verifier que les liens sont valides | A creer |
| `valider-nommage` | Verifier que le nommage est correct | A creer |
| `valider-conventions` | Verifier que les conventions sont respectees | A creer |

### Priorite 4 -- Outils de correction (corriger les erreurs)

| Outil | Raison | Statut |
|---|---|---|
| `corriger-liens` | Corriger les liens casses | A creer |
| `corriger-nommage` | Corriger le nommage | A creer |
| `activer-agent-principal` | Modifier AGENTS.md de maniere fiable | A creer |

### Priorite 5 -- Outils d'analyse (comprendre en profondeur)

| Outil | Raison | Statut |
|---|---|---|
| `analyser-structure` | Analyser la structure du projet | A creer |
| `analyser-dependances` | Analyser les dependances | A creer |

---

## Processus de creation pour chaque outil

### Etape 1 : Verifier le systeme

```
Executer : verifier-systeme (si disponible)
Sinon : Utiliser des commandes de base (uname -a, etc.)
```

### Etape 2 : Lire la specification

```
Fichier : cerveau-projet/agents/tools/[categorie]/[outil]/spec/spec-[outil].001.01.ebauche.md
Si pas de spec : Creer une spec basique
```

### Etape 3 : Choisir la technologie

```
Criteres :
1. Disponibilite sur le systeme (40%)
2. Performance (30%)
3. Facilite (20%)
4. Portabilite (10%)
```

### Etape 4 : Developper l'outil

```
Fichier : cerveau-projet/agents/tools/[categorie]/[outil]/[outil].sh
Format : Script bash executable
```

### Etape 5 : Tester l'outil

```
1. Rendre executable : chmod +x [outil].sh
2. Executer : ./[outil].sh --aide
3. Verifier la sortie
```

### Etape 6 : Documenter

```
1. Mettre a jour le fichier .md avec les instructions
2. Ajouter les exemples d'utilisation
3. Documenter les choix technologiques
```

---

## Suivi de progression

| # | Outil | Categorie | Priorite | Statut | Debut | Fin |
|---|---|---|---|---|---|---|
| 1 | verifier-systeme | analyser | 1 | [OK] Termine | 2026-08-05 | 2026-08-05 |
| 2 | gerer-sous-mission | corriger | 1 | [OK] Termine | 2026-08-05 | 2026-08-05 |
| 3 | lister-dossiers | explorer | 2 | [OK] Termine | 2026-08-05 | 2026-08-05 |
| 4 | lister-fichiers | explorer | 2 | [OK] Termine | 2026-08-05 | 2026-08-05 |
| 5 | lister-fonctions | explorer | 2 | [OK] Termine | 2026-08-05 | 2026-08-05 |
| 6 | lister-appels | explorer | 2 | En attente | - | - |
| 7 | lister-agents | explorer | 2 | En attente | - | - |
| 8 | lister-outils | explorer | 2 | En attente | - | - |
| 9 | valider-cartes-decision | valider | 3 | [OK] Termine | 2026-08-05 | 2026-08-05 |
| 10 | valider-liens | valider | 3 | [OK] Termine | 2026-08-05 | 2026-08-05 |
| 11 | valider-nommage | valider | 3 | En attente | - | - |
| 12 | valider-conventions | valider | 3 | En attente | - | - |
| 13 | corriger-liens | corriger | 4 | [OK] Termine | 2026-08-05 | 2026-08-05 |
| 14 | corriger-nommage | corriger | 4 | En attente | - | - |
| 15 | activer-agent-principal | corriger | 4 | En attente | - | - |
| 16 | analyser-structure | analyser | 5 | En attente | - | - |
| 17 | analyser-dependances | analyser | 5 | En attente | - | - |

---

## Regles a suivre

1. **Un outil a la fois** -- Ne pas melanger les creations
2. **Tester avant de passer** -- Chaque outil doit etre teste
3. **Documenter les choix** -- Pourquoi cette technologie ?
4. **Respecter la portabilite** -- Fonctionner sur tous les systemes
5. **Revenir a Cerberus** -- Apres chaque outil cree

---

