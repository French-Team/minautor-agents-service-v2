---
type: controle
agent: janus
date: 2026-08-19
mission: renforcer test-001 (0 lien casse) - controle final
verdict: VALIDE
---

# Controle final : mission liens casses

## Resultats

| Profil | Resultat |
|---|---|
| cartes | 27/27 OK |
| outils | 36/36 OK |
| tests | 19/19 OK |
| fiches-agents | 17/17 OK |
| docs | 5/5 OK |
| registre | 18/18 OK |
| **TOTAL** | **122/122 OK** |

| Garde-fou | Resultat |
|---|---|
| evaluer-coherence : liens casses | **0** |
| evaluer-processus : problemes | **0** |
| test-001 renforce (point 9 : 0 lien casse) | 11/11 OK |
| Registre usages | JSONL 621 lignes valide |

## Incident decouvert et corrige

Pendant la non-regression, test-035 (evaluer-processus) a revele un KO
LATENT : OUTILS_P0_PARTAGES n etait pas inclus dans les outils autorises de
detecter_outils_hors_carte. Les usages declares au registre de
evaluer-coherence (outil partage, proprietaire Themis) par tous les agents
en mission etaient signales OUTIL_HORS_CARTE a tort. Le test n avait pas
tourne le 18 (entrees hors fenetre) : KO latent revele par les entrees du
jour. Correctif Vulcain (evaluer-processus 0.1.6) : autorises =
outils_carte | outils_p0 | OUTILS_P0_PARTAGES + evaluer-coherence ajoute a
la liste. test-035 10/10.

## Verdict

VALIDE. Mission terminee : les 15 liens casses preexistants sont corriges
(10 chemins relatifs par Buffy, 5 exemples de format ignores par Vulcain)
et test-001 exige desormais 0 lien casse dans toute la non-regression.
