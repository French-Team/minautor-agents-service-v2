# Corrections linguistiques - session admin 2026-09-04

Cette note est un aide-mémoire interne : elle récapitule les textes anglais ou mal formulés qui ont été produits pendant cette session, ainsi que les corrections appliquées ou à appliquer.

## Sources actives touchées

1. `cerveau-projet/agents/tools/oracle/outbox/cerberus.jsonl`
   - Le message de mission `3827ca5d` était en anglais.
   - Il a été réécrit en français.

2. `AGENTS-historique.md`
   - Quelques lignes de bilan étaient partiellement en anglais.
   - Elles ont été mise en français.

3. `cerveau-projet/agents/socrate/corrections-db.md`
   - Document en anglais.
   - Réécrit en français.

4. `cerveau-projet/agents/corrections-db.md`
   - Certains passages étaient flous ou mal formulés.
   - Ajout d'une ligne de garde linguistique.

5. `cerveau-projet/docs-dev-cerveau-projet/amelioration-philosophie.md`
   - Le fichier contient plusieurs blocs internes en anglais.
   - Traduction progressive en cours ; il reste encore du travail.
   - À ne pas publier tel quel tant que les internals ne sont pas tous en français.

## Remarque importante

La polluée ne vient pas d'un seul endroit. Il y a une part legacy (anciens notes de dev), une part message de mission active, et une part notes de réflexion internes. La priorité est donc la source active, puis le document de dev sil il risque d'être lu tel quel.

## Prochaines étapes possibles

- Finir la traduction du bloc interne du fichier `amelioration-philosophie.md`.
- Ajouter une courte règle de langue dans la pipeline de génération de mission, pour éviter qu' une nouvelle mission ne sorte en anglais.
- Vérifier que les autres `outbox.jsonl` et `inbox.jsonl` actifs ne contiennent pas d'autres messages en anglais ou en dev mixte.
