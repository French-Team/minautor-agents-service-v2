---
identite:
  type: rapport
  appartient_a: commun
  commun: true
---
# Rapport d'audit Themis -- conformite carte Janus

**Date** : 2026-08-18
**Demande** : l utilisateur se demande si Janus a ete eduque et si sa carte
est conforme (observation : Janus a enumere les choses et suivi sa carte en
activant le maillon suivant).

## Perimetre audite

1. Version de la carte Janus (parcours-janus.json) vs fiche (janus.md).
2. Presence des garde-fous pedagogiques (modele re-education Themis v0.4.10) :
   GARDE-FOU C1 (classification en c1), redirection "outil bloque",
   indice "AGENTS HABILITES".
3. Structure generale (cases, fins, branches, boucle KO, Pattern 17).
4. Historique d education de Janus (corrections.md + BDD lecons).

## Verifications

| Verification | Resultat |
|---|---|
| Version carte JSON = 0.4.20, fiche PARCOURS (v0.4.20) | [OK] synchronisees |
| Structure : 51 cases (28 action, 7 question, 11 fin, 5 controle) | [OK] |
| c27 -> c28 (mission hors parcours -> agent habilite) | [OK] present |
| c9g (boucle KO : activer l agent habilite pour reparer) | [OK] present |
| Pattern 17 (c9c/c9d : generateur d abord + delegation) | [OK] present |
| c10 (FIN - Reactiver Cerberus, dernier maillon) | [OK] present |
| GARDE-FOU C1 en c1 (indice de classification) | [KO] ABSENT (0 indice en c1) |
| Redirection "outil bloque" par le verrou d habilitation | [KO] ABSENT (aucune case ne traite le cas) |
| Indice "AGENTS HABILITES" (Buffy cartes, Vulcain outils, Morpheus tests, Hygie suppression, Janus controle) en c28 | [KO] ABSENT |
| Education par Chiron | [KO] JAMAIS (seule lecon Chiron #23 = Themis) |
| Description du parcours (v0.4.8) vs version JSON (0.4.20) | [WARN] mention perimee (pattern commun a tous les agents : la description est une note d epoque, pas la version courante) |

## Analyse

La carte de Janus est **structurellement saine** : version a jour (0.4.20),
synchronisee avec la fiche, cablage complet (boucle KO, Pattern 17, fins
correctes). Son comportement observe par l utilisateur (enumerer les verifications
puis activer le maillon suivant) est EXACTEMENT ce que sa carte ordonne : il a
suivi sa carte.

MAIS la carte est **pedagogiquement en retard**, exactement comme l etait celle
de Themis avant sa re-education (v0.4.10) :

1. **c1 sans indice GARDE-FOU C1** : la case de classification n a AUCUN indice
   rappelant la regle (modele : Cerberus c1, Themis c1). Un indice de
   classification est le garde-fou anti-improvisation.
2. **Aucune redirection quand le verrou bloque un outil** : la carte de Themis
   a recu c21 (REDIRECTION OUTIL BLOQUE) -> c22 (Activer l agent habilite) lors
   de sa re-education. La carte de Janus n a pas d equivalent : si le verrou
   bloque un outil que Janus tente d utiliser, sa carte ne lui dit pas
   d activer l agent habilite.
3. **c28 (Activer l agent habilite) sans l indice AGENTS HABILITES** : la liste
   des agents habilites par domaine (Buffy cartes, Vulcain outils, Morpheus
   tests, Hygie suppression, Janus controle) manque - Janus doit savoir QUI
   activer selon le fichier en cause.

Preuve concrete du manque 2 : pendant cet audit, le verrou a bloque Themis sur
valider-cartes-decision (habilites : argus, buffy, janus, vulcain). La carte
re-education de Themis (c21/c22) a correctement redirige vers l agent habilite.

## Verdict

**A REVOIR** -- carte structurellement saine mais guidage pedagogique manquant :
c1 sans indice de classification (GARDE-FOU C1), aucune redirection "outil
bloque", c28 sans l indice "AGENTS HABILITES". Janus n a JAMAIS ete re-eduque
par Chiron.

## Recommendation

Re-education de Janus sur le modele de celle de Themis (v0.4.10) :
1. c1 : ajouter l indice GARDE-FOU C1 (classification de la demande).
2. Ajouter une redirection "outil bloque" -> activer l agent habilite (modele
   Themis c21/c22).
3. c28 : ajouter l indice AGENTS HABILITES (Buffy cartes, Vulcain outils,
   Morpheus tests, Hygie suppression, Janus controle).
4. Bump de version de la carte + synchronisation de la fiche (Pattern 14).
