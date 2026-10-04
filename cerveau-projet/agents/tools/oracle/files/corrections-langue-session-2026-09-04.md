# Corrections linguistiques - session admin 2026-09-04

Cette note est un aide-memoire interne : elle recapitule les textes anglais ou mal formules qui ont ete produits pendant cette session, ainsi que les corrections appliquees ou a appliquer.

## Sources actives touchees

1. `cerveau-projet/agents/tools/oracle/outbox/cerberus.jsonl`
   - Le message de mission `3827ca5d` etait en anglais.
   - Il a ete reecrit en francais.

2. `AGENTS-historique.md`
   - Quelques lignes de bilan etaient partiellement en anglais.
   - Elles ont ete mise en francais.

3. `cerveau-projet/agents/socrate/corrections-db.md`
   - Document en anglais.
   - Reecrit en francais.

4. `cerveau-projet/agents/corrections-db.md`
   - Certains passages etaient flous ou mal formules.
   - Ajout d'une ligne de garde linguistique.

5. `cerveau-projet/docs-dev-cerveau-projet/amelioration-philosophie.md`
   - Le fichier contient plusieurs blocs internes en anglais.
   - Traduction progressive en cours ; il reste encore du travail.
   - A ne pas publier tel quel tant que les internals ne sont pas tous en francais.

## Remarque importante

La polluee ne vient pas d'un seul endroit. Il y a une part legacy (anciens notes de dev), une part message de mission active, et une part notes de reflexion internes. La priorite est donc la source active, puis le document de dev sil il risque d'etre lu tel quel.

## Prochaines etapes possibles

- Finir la traduction du bloc interne du fichier `amelioration-philosophie.md`.
- Ajouter une courte regle de langue dans la pipeline de generation de mission, pour eviter qu' une nouvelle mission ne sorte en anglais.
- Verifier que les autres `outbox.jsonl` et `inbox.jsonl` actifs ne contiennent pas d'autres messages en anglais ou en dev mixte.
