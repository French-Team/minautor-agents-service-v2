---
identite:
  type: rapport-themis
  date: 2026-08-13
  objet: audit mission Morpheus (adaptation tests axe D Themis)
---

# Audit Themis : mission Morpheus (tests adaptes + non-regression)

**Contexte** : mission Themis (activee par Morpheus, maillon automatique axe D) -
auditer l adaptation des tests de version par Morpheus apres les bumps des
parcours (axe D Themis de Buffy).

## Verifications (T1-T4)

| Check | Resultat |
|---|---|
| T1. Versions dans les 5 tests | test-004 morpheus v0.4.4 (2 occ), test-016 buffy v0.4.2 + action 40 + controle 5, test-005 atlas v0.4.2 + residus c30+c11a + navigations OUI final, test-006 48 cases, test-017 contrat outil 7x |
| T2. Compteurs parcours reel (source de verite) | buffy v0.4.2 : action 40 / question 8 / controle 5 / fin 10 = identiques au test-016 |
| T3. Normes ASCII/LF | 0/0 sur les 5 tests + corrections.md Morpheus |
| T4. Non-regression complete | 36/36 OK (pool-16, 42.0 s, chrono conforme) |

## Analyse de fond

1. **Cause racine test-017** : generateurs-ligne n affiche que les 6 dernieres
   lignes de valider-case. Avant l axe D : 1 seul avertissement (deviation) ->
   le verdict CONFORME etait visible. Depuis : 3 avertissements de re-essai
   Themis (c8b/c22b/c27b) + deviation = 4 -> le verdict sort de la fenetre.
   Adaptation correcte : verifier le contrat reel de l outil
   ('[OK] valider-case : conforme' emis uniquement si returncode 0).

2. **Cause racine test-005** : les nouvelles cases atlas c11a (action Activer
   Themis avec commande catalogue) et c11b (controle Retour de Themis) ont
   change le residu catalogue (1 -> 2) et les navigations (+1 reponse OUI).

3. **Lecon a retenir** : un test qui verifie la sortie d un outil re-affichant
   un sous-ensemble de lignes d un validateur doit verifier le message de
   succes FINAL de l outil, pas une ligne de verdict fragile.

## Verdict : VALIDE

La mission Morpheus est conforme : adaptations exactes, compteurs recalcules
depuis le parcours reel, normes 0/0, non-regression 36/36. Aucun ecart.
