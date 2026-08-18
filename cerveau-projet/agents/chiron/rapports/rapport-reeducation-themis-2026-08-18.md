---
identite:
  type: rapport-chiron
  appartient_a: chiron
  commun: false
---

# RAPPORT CHIRON -- REEDUCATION DE THEMIS

**Date** : 2026-08-18
**Agent cible** : themis (parcours v0.4.9 initial puis v0.4.10 apres correction, fiche v0.2.0)
**Declencheur** : session-llm-2 (kilo-llm) - Themis a recu une mission hors
perimetre ('Inventaire et audit des outils de performance') et a improvise au
lieu de suivre le chemin hors-perimetre ; elle a tente editer-parcours (outil
reserve a Buffy), bloque 2x par le verrou a 17:44:00, sans se rediriger.

---

## VERIFICATIONS EFFECTUEES

| Outil | Resultat |
|---|---|
| verifier-conformite-fiche --agent themis | CONFORME (9 sections, sections specifiques toleeres) |
| detecter-cablages-manquants parcours-themis | PROPRE (37/37 cases atteignables, 5 boucles re-travail = avertissements voulus) |
| mettre-a-jour-versions --tous | 149/149 coherent, 0 incoherence |
| detecter-divergences-version | 0 DIVERGENTE (23 alignees) |

**Conclusion structurelle** : la carte et la fiche de Themis sont SAINES
(conformes, cablees, versions alignees). Le probleme est PEDAGOGIQUE : des
indices de guidage presents dans les cartes recentes manquent chez Themis.

---

## INCOHERENCES DETECTEES (corrections de formation proposees)

### INC-1 : c1 (Mission) sans indice de classification (GRAVITE : HAUTE)

- **Fichier** : cerveau-projet/agents/themis/parcours/parcours-themis.json, case c1
- **Constat** : la case c1 a 7 branches (audit/doute/rvav/autre/audit-agent/
  audit-fin-mission/readme) mais AUCUN indice. Cerberus a un indice regle
  'GARDE-FOU C1' dans sa c1 qui guide la classification ; Themis n'en a pas.
- **Impact** : un LLM qui recoit une mission ne correspondant a aucune branche
  ne sait pas qu'il doit repondre 'autre' -> c21 (hors perimetre). Il improvise
  (cas observe : mission 'inventaire de performance' -> tentative d'edition de
  carte au lieu de rediriger vers Atlas/Buffy).
- **Correction proposee** : ajouter un indice type 'regle' en tete des indices
  de c1, format Cerberus :
  'GARDE-FOU C1 : une demande qui ne correspond a AUCUNE branche (audit, doute,
  rvav, audit-agent, audit-fin-mission, readme) -> reponse autre -> c21. JAMAIS
  improviser, JAMAIS utiliser un outil hors de ma carte.'
  (texte ASCII, <= 200 caracteres, poids indices conforme)

### INC-2 : aucune redirection quand le verrou bloque un outil (GRAVITE : HAUTE)

- **Fichier** : cerveau-projet/agents/themis/parcours/parcours-themis.json,
  cases c21/c22 (et eventuellement c2/c3)
- **Constat** : quand proteger-verrou-habilitation bloque un outil non autorise
  (message BLOQUE), la carte de Themis ne contient AUCUN indice disant quoi
  faire. Les cartes recentes couvrent ce cas (Cerberus GARDE-FOU, Vulcain a
  proteger-verrou-habilitation dans sa carte).
- **Impact** : Themis a tente editer-parcours 2x (17:44:00), bloque, et n'a pas
  su se rediriger vers c21 -> c22 (activer l'agent habilite = Buffy pour les
  cartes). Elle s'est arretee au lieu de signaler.
- **Correction proposee** :
  a) ajouter dans c21 un indice regle :
  'REDIRECTION OUTIL BLOQUE : si le verrou d habilitation bloque un outil que je
  viens de tenter (message BLOQUE), la demande concerne un domaine d un autre
  agent -> reponse OUI -> c22 (activer l agent habilite).'
  b) ajouter dans c22 un indice regle rappelant les agents habiles :
  'AGENTS HABILITES : Buffy (cartes, fiches, editer-parcours), Vulcain (outils),
  Morpheus (tests), Hygie (suppression), Janus (controle).'

### INC-3 : chemin hors-perimetre incomplet pour les missions d'inventaire (GRAVITE : MOYENNE)

- **Fichier** : cerveau-projet/agents/themis/parcours/parcours-themis.json,
  c21 -> c22 -> c24
- **Constat** : la question c21 ('La demande concerne-t-elle un domaine d un
  autre agent ?') n'a aucun indice d'aide. Les missions d inventaire/analyse
  relevent d Atlas/Buffy, les demandes de tests de Morpheus, les outils de
  Vulcain - rien dans la carte ne l indique a l agent.
- **Impact** : meme derive que INC-1 - sans guide, le LLM choisit au hasard.
- **Correction proposee** : ajouter dans c21 un indice regle :
  'DOMAINES DES AUTRES AGENTS : inventaire/exploration -> Atlas, contenu/
  developpement/cartes -> Buffy, outil -> Vulcain, tests -> Morpheus,
  suppression -> Hygie, controle -> Janus.'

---

## VERDICT CHIRON

**A REVOIR** : 3 corrections de formation proposees (2 hautes, 1 moyenne),
toutes dans la carte de Themis (parcours-themis.json). La carte est
structurellement saine - il manque le GUIDAGE PEDAGOGIQUE present dans les
cartes recentes (indices de classification et de redirection).

**Corrections SIMPLES et COMPLEXES signalees a Buffy** (seule habilitee a
corriger les cartes via editer-parcours). Chiron ne modifie rien.
