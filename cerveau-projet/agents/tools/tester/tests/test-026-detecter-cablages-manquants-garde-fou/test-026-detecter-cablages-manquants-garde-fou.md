# test-026-detecter-cablages-manquants-garde-fou

**Categorie** : Garde-fou
**Version** : 0.1.1
**Statut** : ebauche
**Agent** : Morpheus
**Date** : 2026-08-12

Garde-fou anti-recurrence du bug des **cases orphelines** : verifie que les 11
parcours des agents ont **0 cas orphelin, 0 boucle bloquante, 0 reference
morte** (via l'outil `detecter-cablages-manquants`).

## Pourquoi ce garde-fou ?

Le bug des questions orphelines (vulcain c9b/c15b "Ameliorations possibles"
inaccessibles, decouvert le 2026-08-12) a montre que `valider-case` ne
verifie QUE les **fins** non joignables :

- une case orpheline **non-fin** passe inapercue ;
- une boucle **indirecte** (c22 -> c9b -> c22) n'est pas signalee.

L'outil `detecter-cablages-manquants` (v0.1.1) ferme ce trou. Ce garde-fou
verrouille la non-recurrence : toute regression du cablage (case orpheline,
boucle sans issue, reference cassee) fait **KO** la non-regression.

## Points verifies (10)

1. `detecter-cablages-manquants --version` = v0.1.1
2. 11 parcours d'agents trouves
3. **0 CAS_ORPHELINE** sur les 11 parcours (anti-recurrence)
4. 0 BOUCLE_BLOQUANTE
5. 0 REF_MORTE
6. 0 CASE_DEPART manquante
7. 0 FIN_NON_JOIGNABLE
8. `--tous` : verdict global PROPRE
9. ASCII strict (0 non-ASCII) sur outil + doc + test
10. LF pur (0 CRLF) sur outil + doc + test

## Utilisation

```bash
python3 cerveau-projet/agents/tools/tester/tests/test-026-detecter-cablages-manquants-garde-fou/test-026-detecter-cablages-manquants-garde-fou.py
```

Retour : `0` = garde-fou vert (aucun cablage manquant), `1` = KO.

Note : comme les garde-fous precedents (test-024, test-025), ce test **n'a
pas d'entree au catalogue** generateurs-commande (le compteur test-007 reste
a 146).
