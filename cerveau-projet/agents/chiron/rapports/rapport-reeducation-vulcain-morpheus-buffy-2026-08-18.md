---
identite:
  type: rapport
  appartient_a: commun
  commun: true
---
# Rapport de re-education Chiron -- Vulcain, Morpheus, Buffy

**Date** : 2026-08-18
**Demande** : Cerberus (via audit Themis A REVOIR) - verifier si les agents
principaux (Vulcain, Morpheus, Buffy) ont leur carte conforme au modele
pedagogique etabli par la re-education de Themis (v0.4.10) et Janus (v0.5.0).

## Diagnostic

Les 3 cartes sont **structurellement saines** :
- versions carte = versions fiche (PARCOURS) : vulcain 0.4.28, morpheus
  0.4.15, buffy 0.4.14
- verifier-conformite-fiche : CONFORME pour les 3
- bumper --tous : 0 outil incoherent
- cases "Activer l agent habilite" presentes (Pattern 17) : vulcain
  c15d/c9d/c17, morpheus c15/c8d, buffy c15d/c31/c34

MAIS **pedagogiquement en retard** (exactement le diagnostic fait pour Janus) :

| Garde-fou | cerberus/themis/janus (conformes) | vulcain 0.4.28 | morpheus 0.4.15 | buffy 0.4.14 |
|---|---|---|---|---|
| GARDE-FOU C1 en c1 (indice de classification) | OK (1 indice) | KO (0) | KO (0) | KO (0) |
| Redirection outil bloque (verrou -> agent habilite) | OK | KO | KO | KO |
| Indice AGENTS HABILITES dans la case d activation | OK | KO | KO | KO |

Historique d education (BDD lecons) : Chiron n a eduque que Themis (#23) et
Janus (#34). Aucune lecon d education pour Vulcain, Morpheus ou Buffy.

## Corrections de formation proposees (modele Themis v0.4.10 / Janus v0.5.0)

Pour CHACUNE des 3 cartes (vulcain, morpheus, buffy) :
1. **c1 : ajouter l indice GARDE-FOU C1** : la case de classification doit
   porter un indice regle qui force la classification de la demande (branches
   explicites + cas "aucune branche -> autre"). Modele : cerberus c1, themis
   c1, janus c1.
2. **Ajouter la redirection "outil bloque"** : quand le verrou bloque un outil
   (message BLOQUE), la carte doit ordonner de signaler et d activer l agent
   habilite - jamais re-tenter, jamais s arreter. Modele : themis c21/c22,
   janus c27/c28.
3. **Ajouter l indice AGENTS HABILITES** dans la case d activation : Buffy
   cartes, Vulcain outils, Morpheus tests, Hygie suppression, Chiron
   education. Modele : themis c22, janus c28.
4. **Bump de version** (modele : janus 0.4.20 -> 0.5.0) + synchronisation
   fiche (Pattern 14) + resync cartes-lock.

## Verdict

**A REVOIR** - 3 cartes a re-eduquer (vulcain 0.4.28, morpheus 0.4.15, buffy
0.4.14), 3 corrections de formation chacune (modele Themis v0.4.10 / Janus
v0.5.0). CHIRON NE CORRIGE PAS : les corrections de carte vont a Buffy (seule
habilitee editer-parcours).

## Signale a Buffy

Re-education des 3 cartes sur le modele etabli :
1. c1 : indice GARDE-FOU C1 (classification).
2. Redirection "outil bloque" -> activer l agent habilite.
3. Indice AGENTS HABILITES dans la case d activation.
4. Bump de version + sync fiche + resync lock.
