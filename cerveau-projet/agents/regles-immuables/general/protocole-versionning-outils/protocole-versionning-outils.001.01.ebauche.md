---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Protocole Immuable -- Versionning des Outils
**Portee :** Tous les outils dans `agents/tools/`
**Prerequis :** Protocole-outils, conventions de nommage

---

## Objectif

Garantir que chaque outil est :
1. **Cree en beta** avec une documentation complete
2. **Teste independamment** avant toute integration
3. **Optimise** via une boucle de travail dediee
4. **Valide** par un second controle (agent dedie)
5. **Integre** uniquement apres validation complete

---

## Cycle de vie d'un outil

```
BETA -> TEST -> OPTIMISATION -> INTEGRATION -> SECOND CONTROLE -> PRODUCTION
  1       2          3               4               5              6
```

---

## Etape 1 -- Creation en beta

1. **Identifier le besoin** : Qu'est-ce que je fais souvent ?
2. **Creer la structure** : Copier le outil-template vers `agents/tools/[categorie]/[nom-outil]/`
3. **Documenter l'outil** : Objectif, utilisation, parametres, exemples (dans `[nom-outil].md`)
4. **Versionner** : la version est portee par le `.md` (ex: `**Version :** 0.1.0-beta`) ; les spec/ et fichiers de test sont ajoutes si necessaire

---

## Etape 2 -- Tests independants

1. **Phase 1** : Tests de l'outil et de ses fonctions
2. **Phase 2** : Tests d'integration
3. **Resultat** : Tous les tests doivent passer

---

## Etape 3 -- Boucle de travail dediee

1. **Lister les optimisations** : Chaque amelioration = 1 fichier distinct
2. **Documenter** : Probleme, solution, impact
3. **Valider** : Tester chaque amelioration

---

## Etape 4 -- Recherche web de confirmation

1. **Identifier** : Commande/fonction a utiliser
2. **Rechercher** : Documentation officielle
3. **Confirmer** : Existence et syntaxe
4. **Documenter** : Source dans le fichier

---

## Etape 5 -- Second controle

1. **Demande** : Cerberus active Janus -- la mission "Construire / optimiser un outil" figure dans la liste definie
2. **Agent** : Janus (dedie au controle)
3. **Mission** : Ecrite pour la tache en cours
4. **Points** : Documentation, tests, conventions
5. **Verdict** : Valide ou rejete
6. **Retour** : la fin de Janus suit SA carte (modele aero) - reactiver-fin janus --cible oracle ; le pilote ramene le verdict a Cerberus en fin de round

---

## Etape 6 -- Promotion en production

1. **Conditions** : Tests OK, integration OK, controle OK
2. **Promotion** : le statut passe de `ebauche` a `prepare` dans le `.md` de l'outil
3. **Version** : le numero de version evolue dans la documentation (pas de dossier `versions/`)

---

## RVAV a chaque etape

| Etape | Rechercher | Verifier | Analyser | Valider |
|---|---|---|---|---|
| **1. Beta** | Besoin existant ? | Structure complete ? | Coherence ? | Pret pour tests ? |
| **2. Tests** | Commandes valides ? | Tous les tests passent ? | Risques identifies ? | Tests valides ? |
| **3. Optimisation** | Ameliorations documentees ? | Fichiers distincts ? | Impact analyse ? | Optimisations validees ? |
| **4. Web** | Sources trouvees ? | Documentation officielle ? | Compatibilite ? | Confirmation validee ? |
| **5. Controle** | Missions ecrite ? | Points de controle ? | Angles morts couverts ? | Controle valide ? |
| **6. Production** | Conditions reunies ? | Version prete ? | Index a jour ? | Promotion validee ? |

---

## Pieges courants

| Piege | Solution |
|---|---|
| Integrer avant de tester | TOUJOURS tester independamment d'abord |
| Oublier la recherche web | CONFIRMER chaque commande |
| Fusionner les ameliorations | UN fichier par amelioration |
| Ignorer le second controle | Cerberus TOUJOURS active Janus (liste definie) |
| Promouvoir trop tot | S'assurer que TOUTES les conditions sont reunies |

---

## Liens

- **Protocole parent** : [protocole-outils](../protocole-outils/)
- **Convention** : [convention-protocoles](../../../conventions/protocoles/convention-protocoles.md)
- **Agent Janus** : [agents/janus/](../../../../agents/janus/)
- **Regles** : [regles-validation-rigoureuse](../regles-validation-rigoureuse.md)
