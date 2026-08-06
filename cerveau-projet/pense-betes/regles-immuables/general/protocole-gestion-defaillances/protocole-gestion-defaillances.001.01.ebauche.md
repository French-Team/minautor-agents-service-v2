# Protocole — Gestion des Défaillances
---

## Objectif

Détecter et corriger automatiquement les défaillances du cerveau-projet avant qu'elles n'impactent le travail des agents.

---

## Quand ce protocole est déclenché ?

| Déclencheur | Exemple | Priorité |
|---|---|---|
| **Protocole non suivi** | Agent n'a pas lu AGENTS.md | Haute |
| **Mise à jour oubliée** | index-cerveau.md pas mis à jour | Haute |
| **Lien cassé** | Fichier référencé inexistant | Moyenne |
| **Convention non respectée** | Fichier mal nommé | Moyenne |
| **Incohérence détectée** | Deux fichiers contradictoires | Haute |
| **Erreurs récurrentes** | Même erreur 2+ fois | Haute |

---

## Étapes du protocole

### Étape 1 — Détecter la défaillance

```
1. Identifier le type de défaillance
2. Localiser le fichier ou le protocole concerné
3. Évaluer l'impact (haute/moyenne/basse priorité)
4. Noter les détails de la défaillance
```

### Étape 2 — Diagnostiquer la cause racine
```
1. Appliquer le sous-protocole de diagnostic (voir sous-protocole)
2. Identifier la cause racine
3. Proposer des solutions
4. Valider avec l'utilisateur
```

### Étape 3 — Classifier la défaillance

| Type | Description | Action |
|---|---|---|
| **Oubli** | Mise à jour non faite | Mettre à jour immédiatement |
| **Erreur** | Contenu incorrect | Corriger le contenu |
| **Incohérence** | Deux versions contradictoires | Harmoniser |
| **Manque** | Élément absent | Créer l'élément |
| **Obsolète** | Contenu dépassé | Mettre à jour ou archiver |

### Étape 3 — Corriger la défaillance

```
1. Appliquer la correction appropriée
2. Vérifier que la correction est conforme aux conventions
3. Mettre à jour les fichiers concernés
4. Mettre à jour les index
```

### Étape 4 — Traiter la cause racine

```
1. Pourquoi cette défaillance s'est-elle produite ?
2. Le protocole existant couvre-t-il ce cas ?
3. Faut-il créer un nouveau protocole ?
4. Faut-il améliorer un protocole existant ?
```

### Étape 5 — Prvenir les récidives

```
1. Ajouter une règle si nécessaire
2. Modifier le protocole si nécessaire
3. Ajouter un test de validation
4. Documenter l'amélioration
```

### Étape 6 — Documenter

```
1. Ajouter une entrée dans l'historique
2. Mettre à jour le fichier de l'agent (corrections.md)
3. Mettre à jour les index
4. Signer : "[nom-agent] -- [date]"
```

---

## Points de déclenchement

### Dans demarrer.md

Le protocole est vérifié à chaque étape critique :
- **Étape 0.1** : Vérifier que AGENTS.md est à jour
- **Étape 0.3** : Vérifier que les corrections sont appliquées
- **Étape 0.4** : Vérifier que AGENTS.md est mis à jour

### Dans les protocoles d'auto-amélioration

Le protocole est vérifié à chaque amélioration :
- **protocole-autoameliorer-cerveau** : Vérifier la cohérence
- **protocole-autoameliorer-agents** : Vérifier les fiches
- **protocole-autoameliorer-outils** : Vérifier les outils
- **protocole-autoameliorer-conventions** : Vérifier les conventions
- **protocole-autoameliorer-protocoles** : Vérifier les protocoles
- **protocole-autoameliorer-regles** : Vérifier les règles

### Dans les protocoles de travail

Le protocole est vérifié avant chaque modification :
- Vérifier les dépendances
- Vérifier les conventions
- Vérifier la cohérence

---

## Système de détection automatique

### Détection par les agents

Chaque agent doit vérifier :

```
1. Avant de commencer :
   - AGENTS.md est-il à jour ?
   - Ma fiche est-elle à jour ?
   - Ai-je appliqué mes corrections ?

2. Pendant le travail :
   - Est-ce que je respecte les conventions ?
   - Est-ce que je mets à jour les fichiers concernés ?
   - Est-ce que je documente mes changements ?

3. Après le travail :
   - Ai-je mis à jour tous les fichiers concernés ?
   - Ai-je mis à jour les index ?
   - Ai-je documenté mes changements ?
```

### Détection par les fichiers

Chaque fichier doit contenir :

```
1. Un en-tête avec les métadonnées
2. Un historique des modifications
3. Des liens vers les fichiers connexes
4. Un statut à jour
```

### Détection par les index

Chaque index doit contenir :

```
1. La liste de tous les éléments
2. Le statut de chaque élément
3. Les liens vers les éléments
4. Un résumé rapide
```

---

## Tableau des défaillances courantes

| Défaillance | Cause | Correction | Prévention |
|---|---|---|---|
| **AGENTS.md pas à jour** | Oubli | Mettre à jour | Vérifier à chaque session |
| **Index pas à jour** | Oubli | Mettre à jour | Vérifier après chaque modification |
| **Lien cassé** | Fichier déplacé | Corriger le lien | Vérifier les liens |
| **Convention non respectée** | Méconnaissance | Corriger + documenter | Lire les conventions |
| **Incohérence** | Modification partielle | Harmoniser | Vérifier la cohérence |
| **Protocole non suivi** | Méconnaissance | Suivre le protocole | Lire les protocoles |

---

## Priorités

| Priorité | Délai d'action | Exemple |
|---|---|---|
| **Haute** | Immédiat | Protocole non suivi, incohérence |
| **Moyenne** | Avant la prochaine session | Mise à jour oubliée, lien cassé |
| **Basse** | Quand possible | Amélioration mineure |

---

## Liens

- [convention-autoamelioration.md](../../../conventions/protocoles/convention-autoamelioration.md)
- [protocole-autoameliorer-cerveau.md](../protocole-autoameliorer-cerveau/protocole-autoameliorer-cerveau.001.01.ebauche.md)
- [protocole-auto-correction.md](../protocole-auto-correction/protocole-auto-correction.001.01.ebauche.md)

---

*Protocole conforme aux conventions du cerveau-projet*
