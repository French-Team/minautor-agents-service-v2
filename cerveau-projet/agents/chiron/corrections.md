---
famille: cerveau-projet
identite:
  type: corrections-agent
  nom: Chiron
  version: 0.1.0
  date_creation: 2026-08-17
---

# Corrections -- Chiron

> Ce fichier contient les lecons apprises par Chiron au fil de ses missions.
> Chaque lection documente : CONTEXTE, LECON, PREUVES.
## [LECON] 2026-08-18 -- REEDUCATION DE THEMIS : CARTE SAINE MAIS GUIDAGE PEDAGOGIQUE MANQUANT (Chiron)

**Contexte** : session-llm-2 (kilo-llm) - Themis a recu la mission 'Inventaire
et audit des outils de performance' qui ne correspond a aucune branche de sa
case c1. Elle a improvise au lieu de repondre 'autre' -> c21 (hors perimetre),
et a tente editer-parcours (outil reserve a Buffy), bloque 2x par le verrou a
17:44:00. L utilisateur a demande sa reeducation : sa carte est en retard sur
celles de cerberus, vulcain, morpheus et janus.

**Diagnostic** : la carte de Themis est STRUCTURELLEMENT SAINE (verifier-
conformite-fiche CONFORME, detecter-cablages PROPRE 37/37, bumper 149/149
coherent, 0 divergence de version). Le retard est PEDAGOGIQUE :
1. c1 (Mission) n a AUCUN indice de classification - Cerberus a un indice
   regle 'GARDE-FOU C1' qui guide la reponse ; Themis n en a pas. Un LLM ne
   sait pas qu une mission hors branches -> reponse 'autre' -> c21.
2. AUCUNE redirection quand le verrou bloque un outil (message BLOQUE) : la
   carte de Themis ne dit pas de se diriger vers c21 -> c22 (activer l agent
   habilite). Les cartes recentes couvrent ce cas.
3. c21 (hors perimetre) n a aucun indice listant les domaines des autres
   agents (Atlas/Buffy/Vulcain/Morpheus/Hygie/Janus).

**Lecons** :
1. UNE CARTE STRUCTURELLEMENT VALIDE PEUT ETRE PEDAGOGIQUEMENT EN RETARD : les
   verifications de structure (conformite, cablages, versions) passent toutes
   alors que le guidage (indices de classification) manque. L education doit
   verifier le CONTENU des indices, pas seulement la forme.
2. LE GARDE-FOU C1 DE CERBERUS EST LE MODELE : une case de mission doit porter
   un indice regle qui force la classification (branches explicites + cas
   'aucune branche -> autre'). Sans lui, la classification est libre.
3. LE VERROU BLOQUE EST UN SIGNAL DE REDIRECTION, PAS UN ARRET : quand
   proteger-verrou-habilitation bloque un outil, la carte doit ordonner de
   signaler et d activer l agent habilite (c21 -> c22) - jamais de re-tenter
   ni de s arreter (cas observe : 2 tentatives editer-parcours puis arret).
4. CHIRON NE CORRIGE PAS : les 3 corrections proposees (indices c1/c21/c22)
   vont a Buffy (seule habilitee pour editer-parcours). Chiron documente et
   signale, c est le modele Argus.

**Preuves** : verifier-conformite-fiche themis CONFORME, detecter-cablages
themis PROPRE (37/37), bumper --tous 149/149, detecter-divergences 0
DIVERGENTE. Rapport : rapports/rapport-reeducation-themis-2026-08-18.md.

**Verdict** : A REVOIR - 3 corrections de formation proposees (2 hautes,
1 moyenne), signalees a Buffy.
