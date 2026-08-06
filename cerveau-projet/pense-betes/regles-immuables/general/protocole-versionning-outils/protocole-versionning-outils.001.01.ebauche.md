# Protocole Immuable — Versionning des Outils
**Portée :** Tous les outils dans `agents/tools/`
**Prérequis :** Protocole-outils, conventions de nommage

---

## Objectif

Garantir que chaque outil est :
1. **Créé en bêta** avec une documentation complète
2. **Testé indépendamment** avant toute intégration
3. **Optimisé** via une boucle de travail dédiée
4. **Validé** par un second contrôle (agent dédié)
5. **Intégré** uniquement après validation complète

---

## Cycle de vie d'un outil

```
BÊTA → TEST → OPTIMISATION → INTÉGRATION → SECOND CONTRÔLE → PRODUCTION
  1       2          3               4               5              6
```

---

## Étape 1 — Création en bêta

1. **Identifier le besoin** : Qu'est-ce que je fais souvent ?
2. **Créer la structure** : Dossier avec spec/, todo/, tests/, versions/
3. **Documenter l'outil** : Objectif, utilisation, paramètres, exemples

---

## Étape 2 — Tests indépendants

1. **Phase 1** : Tests de l'outil et de ses fonctions
2. **Phase 2** : Tests d'intégration
3. **Résultat** : Tous les tests doivent passer

---

## Étape 3 — Boucle de travail dédiée

1. **Lister les optimisations** : Chaque amélioration = 1 fichier distinct
2. **Documenter** : Problème, solution, impact
3. **Valider** : Tester chaque amélioration

---

## Étape 4 — Recherche web de confirmation

1. **Identifier** : Commande/fonction à utiliser
2. **Rechercher** : Documentation officielle
3. **Confirmer** : Existence et syntaxe
4. **Documenter** : Source dans le fichier

---

## Étape 5 — Second contrôle

1. **Demande** : Cerberus active Janus — la mission "Construire / optimiser un outil" figure dans la liste définie
2. **Agent** : Janus (dédié au contrôle)
3. **Mission** : Écrite pour la tâche en cours
4. **Points** : Documentation, tests, conventions
5. **Verdict** : Validé ou rejeté
6. **Retour** : Janus réactive Cerberus

---

## Étape 6 — Promotion en production

1. **Conditions** : Tests OK, intégration OK, contrôle OK
2. **Promotion** : bêta → stable
3. **Structure** : Version stable dans versions/stable/

---

## RVAV à chaque étape

| Étape | Rechercher | Vérifier | Analyser | Valider |
|---|---|---|---|---|
| **1. Bêta** | Besoin existant ? | Structure complète ? | Cohérence ? | Prêt pour tests ? |
| **2. Tests** | Commandes valides ? | Tous les tests passent ? | Risques identifiés ? | Tests validés ? |
| **3. Optimisation** | Améliorations documentées ? | Fichiers distincts ? | Impact analysé ? | Optimisations validées ? |
| **4. Web** | Sources trouvées ? | Documentation officielle ? | Compatibilité ? | Confirmation validée ? |
| **5. Contrôle** | Missions écrite ? | Points de contrôle ? | Angles morts couverts ? | Contrôle validé ? |
| **6. Production** | Conditions réunies ? | Version prête ? | Index à jour ? | Promotion validée ? |

---

## Pièges courants

| Piège | Solution |
|---|---|
| Intégrer avant de tester | TOUJOURS tester indépendamment d'abord |
| Oublier la recherche web | CONFIRMER chaque commande |
| Fusionner les améliorations | UN fichier par amélioration |
| Ignorer le second contrôle | Cerberus TOUJOURS active Janus (liste définie) |
| Promouvoir trop tôt | S'assurer que TOUTES les conditions sont réunies |

---

## Liens

- **Protocole parent** : [protocole-outils](../protocole-outils/)
- **Convention** : [convention-protocoles](../../../conventions/protocoles/convention-protocoles.md)
- **Agent Janus** : [agents/janus/](../../../../agents/janus/)
- **Règles** : [regles-validation-rigoureuse](../../regles-validation-rigoureuse.md)
