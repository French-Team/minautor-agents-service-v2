---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Protocole -- Gestion des Defaillances
---

## Objectif

Detecter et corriger automatiquement les defaillances du cerveau-projet avant qu'elles n'impactent le travail des agents.

---

## Quand ce protocole est declenche ?

| Declencheur | Exemple | Priorite |
|---|---|---|
| **Protocole non suivi** | Agent n'a pas lu AGENTS.md | Haute |
| **Mise a jour oubliee** | index-cerveau.md pas mis a jour | Haute |
| **Lien casse** | Fichier reference inexistant | Moyenne |
| **Convention non respectee** | Fichier mal nomme | Moyenne |
| **Incoherence detectee** | Deux fichiers contradictoires | Haute |
| **Erreurs recurrentes** | Meme erreur 2+ fois | Haute |

---

## Etapes du protocole

### Etape 1 -- Detecter la defaillance

```
1. Identifier le type de defaillance
2. Localiser le fichier ou le protocole concerne
3. Evaluer l'impact (haute/moyenne/basse priorite)
4. Noter les details de la defaillance
```

### Etape 2 -- Diagnostiquer la cause racine
```
1. Appliquer le sous-protocole de diagnostic (voir sous-protocole)
2. Identifier la cause racine
3. Proposer des solutions
4. Valider avec l'utilisateur
```

### Etape 3 -- Classifier la defaillance

| Type | Description | Action |
|---|---|---|
| **Oubli** | Mise a jour non faite | Mettre a jour immediatement |
| **Erreur** | Contenu incorrect | Corriger le contenu |
| **Incoherence** | Deux versions contradictoires | Harmoniser |
| **Manque** | Element absent | Creer l'element |
| **Obsolete** | Contenu depasse | Mettre a jour ou archiver |

### Etape 3 -- Corriger la defaillance

```
1. Appliquer la correction appropriee
2. Verifier que la correction est conforme aux conventions
3. Mettre a jour les fichiers concernes
4. Mettre a jour les index
```

### Etape 4 -- Traiter la cause racine

```
1. Pourquoi cette defaillance s'est-elle produite ?
2. Le protocole existant couvre-t-il ce cas ?
3. Faut-il creer un nouveau protocole ?
4. Faut-il ameliorer un protocole existant ?
```

### Etape 5 -- Prvenir les recidives

```
1. Ajouter une regle si necessaire
2. Modifier le protocole si necessaire
3. Ajouter un test de validation
4. Documenter l'amelioration
```

### Etape 6 -- Documenter

```
1. Ajouter une entree dans l'historique
2. Mettre a jour le fichier de l'agent (corrections.md)
3. Mettre a jour les index
4. Signer : "[nom-agent] -- [date]"
```

---

## Points de declenchement

### Dans demarrer.md

Le protocole est verifie a chaque etape critique :
- **Etape 0.1** : Verifier que AGENTS.md est a jour
- **Etape 0.3** : Verifier que les corrections sont appliquees
- **Etape 0.4** : Verifier que AGENTS.md est mis a jour

### Dans les protocoles d'auto-amelioration

Le protocole est verifie a chaque amelioration :
- **protocole-autoameliorer-cerveau** : Verifier la coherence
- **protocole-autoameliorer-agents** : Verifier les fiches
- **protocole-autoameliorer-outils** : Verifier les outils
- **protocole-autoameliorer-conventions** : Verifier les conventions
- **protocole-autoameliorer-protocoles** : Verifier les protocoles
- **protocole-autoameliorer-regles** : Verifier les regles

### Dans les protocoles de travail

Le protocole est verifie avant chaque modification :
- Verifier les dependances
- Verifier les conventions
- Verifier la coherence

---

## Systeme de detection automatique

### Detection par les agents

Chaque agent doit verifier :

```
1. Avant de commencer :
   - AGENTS.md est-il a jour ?
   - Ma fiche est-elle a jour ?
   - Ai-je applique mes corrections ?

2. Pendant le travail :
   - Est-ce que je respecte les conventions ?
   - Est-ce que je mets a jour les fichiers concernes ?
   - Est-ce que je documente mes changements ?

3. Apres le travail :
   - Ai-je mis a jour tous les fichiers concernes ?
   - Ai-je mis a jour les index ?
   - Ai-je documente mes changements ?
```

### Detection par les fichiers

Chaque fichier doit contenir :

```
1. Un en-tete avec les metadonnees
2. Un historique des modifications
3. Des liens vers les fichiers connexes
4. Un statut a jour
```

### Detection par les index

Chaque index doit contenir :

```
1. La liste de tous les elements
2. Le statut de chaque element
3. Les liens vers les elements
4. Un resume rapide
```

---

## Tableau des defaillances courantes

| Defaillance | Cause | Correction | Prevention |
|---|---|---|---|
| **AGENTS.md pas a jour** | Oubli | Mettre a jour | Verifier a chaque session |
| **Index pas a jour** | Oubli | Mettre a jour | Verifier apres chaque modification |
| **Lien casse** | Fichier deplace | Corriger le lien | Verifier les liens |
| **Convention non respectee** | Meconnaissance | Corriger + documenter | Lire les conventions |
| **Incoherence** | Modification partielle | Harmoniser | Verifier la coherence |
| **Protocole non suivi** | Meconnaissance | Suivre le protocole | Lire les protocoles |

---

## Priorites

| Priorite | Delai d'action | Exemple |
|---|---|---|
| **Haute** | Immediat | Protocole non suivi, incoherence |
| **Moyenne** | Avant la prochaine session | Mise a jour oubliee, lien casse |
| **Basse** | Quand possible | Amelioration mineure |

---

## Liens

- [convention-autoamelioration.md](../../../conventions/protocoles/convention-autoamelioration.md)
- [protocole-autoameliorer-cerveau.md](../protocole-autoameliorer-cerveau/protocole-autoameliorer-cerveau.001.01.ebauche.md)
- [protocole-auto-correction.md](../protocole-auto-correction/protocole-auto-correction.001.01.ebauche.md)

---

*Protocole conforme aux conventions du cerveau-projet*
