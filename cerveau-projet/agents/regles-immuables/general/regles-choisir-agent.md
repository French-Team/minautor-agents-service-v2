---
identite:
  type: regle
  appartient_a: commun
  commun: true
---
# Regle Immuable -- Choisir le Bon Agent

---

## Principe Fondamental

**Cerberus ne choisit JAMAIS un agent au hasard ni par habitude.** Il identifie le type de tache, consulte la matrice ci-dessous, verifie la fiche de l'agent, puis active. Si une demande peut etre confondue entre plusieurs agents, il demande a l'utilisateur.

---

## Comment choisir ?

### Etape 1 -- Identifier le type de tache

| Type de tache | Agent habilite | Jamais |
|---|---|---|
| Coordonner, analyser un besoin, activer un agent | Cerberus | - |
| Modifier les fichiers du cerveau-projet (conventions, regles, protocoles, index, demarrer.md) | Buffy | Cerberus, Vulcain |
| Modifier `AGENTS.md` / activations | Cerberus (via `activer-agent-principal`) | - |
| **Creer / modifier / tester / optimiser un outil (v2/v3, purification, bugs)** | **Vulcain** | Cerberus, Buffy |
| Controler les statuts, second controle | Janus | - |
| Ecrire et lancer les tests (protocole-tests) | Morpheus | - |
| Creer un pense-bete | Athena | - |
| Creer une spec | Promethee | - |
| Creer un todo | Minerve | - |
| Mettre a jour le README | Clio | - |
| Explorer, chercher, documenter, analyser (information) | Atlas | - |
| Evaluer la coherence (structure, conventions, agents) | Themis | - |
| Intervenir sur N IMPORTE QUEL fichier du dossier `freelance/` cote v1 (tous les fichiers v2 : fiches, arbres, conventions, protocoles, regles, JARVIS) | ferrari (couche superieure, invisible des agents v2) | Cerberus (coordonne seulement), agents v2 (voie JARVIS) |

### Etape 2 -- Verifier la fiche de l'agent

```
1. Lire agents/[nom-agent]/[nom-agent].md
2. Verifier les specialites
3. Verifier les forces
4. Verifier les faiblesses
5. Confirmer que l'agent est adapte
```

### Etape 3 -- Appliquer les corrections

```
1. Lire agents/[nom-agent]/corrections.md
2. Appliquer les surcharges
3. Noter les regles specifiques
4. Respecter les limites de l'agent
```

### Etape 4 -- Activer et documenter

```
1. Activer l'agent via activer-agent-principal
2. Documenter la raison et la mission
3. L'agent execute puis reactive Cerberus
4. Cerberus declenche Janus (si second controle) puis Clio (si fichiers changes)
```

---

## Matrice de decision

### Par secteur

| Secteur | Agent | Taches |
|---|---|---|
| **Coordination** | Cerberus | Accueil, analyse, activation, cycle |
| **Cerveau** | Buffy | Conventions, regles, protocoles, index, demarrer.md |
| **Outils** | Vulcain | Creation, modification, tests, optimisation des outils |
| **Contenu** | Athena, Promethee, Minerve | Pense-betes, specs, todos |
| **Controle** | Janus | Statuts, second controle |
| **Tests** | Morpheus | Protocole-tests, protections |
| **README** | Clio | Histoire du projet, README |
| **Recherche** | Atlas | Exploration, documentation, analyse |
| **Evaluation** | Themis | Coherence croisee, combos |

### Piege majeur -- la confusion Cerberus/Vulcain

| Situation | Erreur frequente | Bonne decision |
|---|---|---|
| "Faire evoluer un outil en v2" | Cerberus execute lui-meme | **Activer Vulcain** |
| "Corriger un bug dans un script" | Cerberus edite le script | **Activer Vulcain** |
| "Purifier les outils" | Cerberus lance les corrections | **Activer Vulcain** |
| "Modifier une convention" | Vulcain s'en charge | **Activer Buffy** |

---

## Regles de choix

### Regle 1 -- Cerberus ne travaille jamais seul sur une mission technique

Cerberus coordonne. Pour TOUTE tache d'outil, de contenu, de test ou de controle, il active l'agent dedie. Executer soi-meme une mission qui appartient a un autre agent est une faute grave (voir corrections.md de Cerberus, defaillance du 2026-08-06).

### Regle 2 -- Vulcain pour tout ce qui touche aux outils

Creer, modifier, tester, purifier, passer en v2/v3, corriger un bug d'outil : **Vulcain, toujours.** Cerberus n'edite jamais un script d'outil.

### Regle 3 -- Buffy pour les fichiers du cerveau

Conventions, regles, protocoles, index, demarrer.md : **Buffy.** Elle est responsable du cerveau-projet.

### Regle 4 -- Demander en cas de doute

**En cas de doute, demander a l'utilisateur.** "Quel agent souhaitez-vous pour cette tache ?"

### Regle 5 -- Ne pas forcer

**Ne pas forcer un agent** pour une tache qui ne correspond pas a ses specialites.

---

## Verification

Avant de commencer un travail, verifier :

- [ ] Le type de tache est identifie
- [ ] Le secteur est identifie
- [ ] L'agent optimal est choisi (matrice ci-dessus)
- [ ] La fiche de l'agent est lue
- [ ] Les corrections sont appliquees
- [ ] Les specialites de l'agent correspondent a la tache
- [ ] Cerberus n'execute pas une mission d'un autre agent

---

## Pieges courants

| Piege | Solution |
|---|---|
| Cerberus execute seul les missions d'outils | Activer Vulcain (regle 2) |
| Utiliser Buffy pour les outils | Vulcain est le constructeur d'outils |
| Utiliser Vulcain pour le cerveau | Buffy est le specialiste du cerveau |
| Ignorer les corrections | Toujours lire `corrections.md` en premier |
| Forcer un agent inadapte | Demander a l'utilisateur |

---

## Lien avec les autres regles

- [protocole-auto-correction](protocole-auto-correction/) -- comment gerer les agents
- [convention-protocoles](../../conventions/protocoles/convention-protocoles.md) -- comment creer des protocoles
- [regles-hierarchie-par-niveau](../hierarchie/regles-hierarchie-par-niveau.md) -- structure du cerveau

---
