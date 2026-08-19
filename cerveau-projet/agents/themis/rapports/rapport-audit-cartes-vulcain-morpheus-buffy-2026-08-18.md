---
identite:
  type: rapport
  appartient_a: commun
  commun: true
---
# Rapport d'audit Themis -- conformite pedagogique des cartes de Vulcain, Morpheus et Buffy

**Date** : 2026-08-18
**Demande** : Cerberus - verifier si les autres agents principaux (Vulcain,
Morpheus, Buffy) ont leur carte conforme au modele pedagogique etabli par la
re-education de Themis (v0.4.10) et applique a Janus (v0.5.0).

## Modele de conformite pedagogique (reference)

Une carte d agent principal est pedagogiquement conforme si elle a :
1. **GARDE-FOU C1** : un indice regle en c1 qui force la classification de la
   demande (branches explicites + cas "aucune branche -> autre"). Sans lui,
   la classification est libre (garde-fou anti-improvisation).
2. **Redirection outil bloque** : quand le verrou d habilitation bloque un
   outil (message BLOQUE), la carte ordonne de signaler et d activer l agent
   habilite - jamais re-tenter, jamais s arreter.
3. **AGENTS HABILITES** : la liste des agents habilites par domaine dans la
   case d activation (Buffy cartes, Vulcain outils, Morpheus tests, Hygie
   suppression, Chiron education).

## Verifications

| Agent | Version carte | Version fiche | c1 indices | GARDE-FOU C1 | Redirection outil bloque | AGENTS HABILITES | Eduque par Chiron |
|---|---|---|---|---|---|---|---|
| cerberus (ref) | 0.5.4 | 0.5.4 | 1 | OK | OK | OK | modele |
| themis (ref) | 0.4.10 | 0.4.10 | 1 | OK | OK | OK | OK |
| janus (ref) | 0.5.0 | 0.5.0 | 1 | OK | OK | OK | OK |
| **vulcain** | 0.4.28 | 0.4.28 | **0** | **KO** | **KO** | **KO** | **JAMAIS** |
| **morpheus** | 0.4.15 | 0.4.15 | **0** | **KO** | **KO** | **KO** | **JAMAIS** |
| **buffy** | 0.4.14 | 0.4.14 | **0** | **KO** | **KO** | **KO** | **JAMAIS** |

Les 3 cartes sont **structurellement saines** : version carte = version fiche
(PARCOURS), nombre de cases et de fins complet (vulcain 58 cases/9 fins,
morpheus 35/7, buffy 64/10), cases "Activer l agent habilite" presentes pour
le Pattern 17 (vulcain c15d/c9d/c17, morpheus c15/c8d, buffy c15d/c31/c34).

MAIS elles sont **pedagogiquement en retard**, exactement comme Janus et
Themis avant leur re-education :
1. **c1 sans AUCUN indice** : la case de classification n a pas de GARDE-FOU
   C1 (0 indice, contre 1 pour cerberus/themis/janus).
2. **Aucune redirection outil bloque** : si le verrou bloque un outil tente,
   la carte ne dit pas d activer l agent habilite.
3. **Aucun indice AGENTS HABILITES** : les cases d activation n ont pas la
   liste des agents habilites par domaine.

Historique d education (BDD lecons) : Chiron n a eduque que Themis (#23) et
Janus (#34). Aucune lecon d education pour Vulcain, Morpheus ou Buffy.

## Verdict

**A REVOIR** -- les 3 cartes sont structurellement saines mais pedagogiquement
en retard : Vulcain (v0.4.28), Morpheus (v0.4.15), Buffy (v0.4.14) n ont ni
GARDE-FOU C1 en c1, ni redirection outil bloque, ni indice AGENTS HABILITES,
et n ont JAMAIS ete eduques par Chiron.

## Recommendation

Re-education des 3 agents sur le modele etabli (Themis v0.4.10, Janus v0.5.0) :
1. c1 : ajouter l indice GARDE-FOU C1 (classification de la demande).
2. Ajouter la redirection "outil bloque" -> activer l agent habilite.
3. Ajouter l indice AGENTS HABILITES dans la case d activation.
4. Bump de version + synchronisation fiche (Pattern 14) + resync lock.
