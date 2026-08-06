# Règle Immuable — Choisir le Bon Agent
---

## Principe Fondamental
---

## Comment choisir ?

### Étape 1 — Identifier le type de tâche

| Type de tâche | Secteur | Agent recommandé |
|---|---|---|
| Modifier `index-cerveau.md` | Cerveau | Buffy |
| Modifier `demarrer.md` | Cerveau | Buffy |
| Modifier `AGENTS.md` | Agents | Buffy |
| Créer/modifier une convention | Cerveau | Buffy |
| Créer/modifier un protocole | Cerveau | Buffy |
| Créer un pense-bête | Contenu | Buffy |
| Créer une spec | Contenu | Buffy |
| Créer un todo | Contenu | Buffy |
| Explorer le code | Recherche | Atlas |
| Documenter en détail | Documentation | Atlas |
| Analyser des dépendances | Analyse | Atlas |
| Chercher sur le web | Recherche | Atlas |

### Étape 2 — Vérifier la fiche de l'agent

```
1. Lire agents/[nom-agent]/[nom-agent].md
2. Vérifier les spécialités
3. Vérifier les forces
4. Vérifier les faiblesses
5. Confirmer que l'agent est adapté
```

### Étape 3 — Appliquer les corrections

```
1. Lire agents/[nom-agent]/corrections.md EN PREMIER
2. Appliquer les surcharges
3. Noter les règles spécifiques
4. Respecter les limites de l'agent
```

### Étape 4 — Exécuter la tâche

```
1. Travailler selon le style de l'agent
2. Respecter les conventions
3. Documenter les changements
4. Mettre à jour les fichiers liés si nécessaire
```

---

## Matrice de décision

### Par secteur

| Secteur | Agent | Tâches |
|---|---|---|
| **Agents** | Buffy | Fiches, corrections, AGENTS.md, changements d'agent |
| **Cerveau** | Buffy | Conventions, règles, protocoles, index |
| **Contenu** | Buffy | Pense-betes, specs, todos |
| **Recherche** | Atlas | Exploration, documentation, analyse |

### Par complexité

| Complexité | Agent | Approche |
|---|---|---|
| **Simple** | Buffy | Directe, efficace |
| **Moyenne** | Buffy ou Atlas | Selon la spécialité |
| **Complexe** | Buffy + Atlas | Coordonner les deux |

---

## Règles de choix

### Règle 1 — Buffy par défaut

**Buffy est l'agent principal.** Par défaut, c'est Buffy qui fait le travail, sauf si une tâche est clairement du domaine d'un autre agent.

### Règle 2 — Atlas pour la recherche

**Atlas est l'explorateur.** Quand il faut chercher, documenter en détail, ou analyser, Atlas est plus adapté.

### Règle 3 — Demander en cas de doute

**En cas de doute, demander à l'utilisateur.** "Quel agent souhaitez-vous pour cette tâche ?"

### Règle 4 — Ne pas forcer

**Ne pas forcer un agent** pour une tâche qui ne correspond pas à ses spécialités.

---

## Exemples

### Exemple 1 — Modifier une convention

```
Tâche : Modifier convention-structures.md
Secteur : Cerveau
Agent : Buffy (spécialiste des conventions)
```

### Exemple 2 — Explorer le code pour comprendre un module

```
Tâche : Comprendre comment fonctionne le module X
Secteur : Recherche
Agent : Atlas (explorateur)
```

### Exemple 3 — Créer un nouveau pense-bête

```
Tâche : Créer un pense-bête sur le thème Y
Secteur : Contenu
Agent : Buffy (création de contenu)
```

### Exemple 4 — Tâche complexe

```
Tâche : Refactoring majeur du cerveau
Secteur : Cerveau + Recherche
Agents : Buffy (orchestration) + Atlas (exploration)
```

---

## Vérification

Avant de commencer un travail, vérifier :

- [ ] Le type de tâche est identifié
- [ ] Le secteur est identifié
- [ ] L'agent optimal est choisi
- [ ] La fiche de l'agent est lue
- [ ] Les corrections sont appliquées
- [ ] Les spécialités de l'agent correspondent à la tâche

---

## Pièges courants

| Piège | Solution |
|---|---|
| Utiliser Buffy pour tout | Vérifier si Atlas serait plus adapté |
| Utiliser Atlas pour modifier le cerveau | Buffy est le spécialiste du cerveau |
| Ignorer les corrections | Toujours lire `corrections.md` en premier |
| Forcer un agent inadapté | Demander à l'utilisateur |

---

## Lien avec les autres règles

- [protocole-auto-correction](protocole-auto-correction/) — comment gérer les agents
- [convention-protocoles](../../conventions/protocoles/convention-protocoles.md) — comment créer des protocoles
- [regles-hierarchie-par-niveau](../hierarchie/regles-hierarchie-par-niveau.md) — structure du cerveau

---

