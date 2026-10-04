# Controle croise : detecter-cablages-manquants (reprise de mission)

**Date** : 2026-08-12
**Controleur** : Janus
**Chaine** : Vulcain (outil v0.1.1 + orphelines clio) -> Morpheus (test-001 + garde-fou test-026) -> Janus

---

## Verdict : VALIDE (J1-J6 verts)

| # | Verification | Resultat |
|---|---|---|
| J1 | Outil `detecter-cablages-manquants` v0.1.1 | CONFORME : compile, `--version` v0.1.1, 5 detections (CASE_DEPART, FIN_NON_JOIGNABLE, CAS_ORPHELINE, BOUCLE_BLOQUANTE vs BOUCLE_RE_TRAVAIL, REF_MORTE), options --tous/--rapport/--verbose, doc .md, entree catalogue **146** (modele --tous), index-tools Detecter **10** + Total **115**, badge README **127** |
| J2 | Orphelines clio corrigees | CONFORME : vestiges c6/c6a/c7/c8 retires (c6a etait une case VIDE), parcours-clio **0.5.3** (30 cases), fiche Pattern 14 a jour, valider-case CONFORME, valider-cartes --tous **11/11** |
| J3 | test-001-detecter-cablages-manquants.sh | **8/8 VALIDE** (version, parcours sain PROPRE, bug simule detection 100%, --tous, --rapport) |
| J4 | Garde-fou test-026 | **10/10 OK** : 0 CAS_ORPHELINE, 0 BOUCLE_BLOQUANTE, 0 REF_MORTE, 0 CASE_DEPART, 0 FIN_NON_JOIGNABLE sur les 11 parcours + --tous PROPRE + normes |
| J5 | Tests et non-regression | test-007 adapte (146, Total 115), test-024 point 8 adapte (146), non-regression **26/26 OK**, registre 0 ligne |
| J6 | Discipline et documentation | Lecons Vulcain + Morpheus documentees, registre usages complet, delegation respectee (Vulcain n a touche a aucun fichier de test) |

## Details

### J1 - Outil v0.1.1

- 5 familles de detection : le maillon manquant du bug des questions orphelines
  est la **CAS_ORPHELINE** (toute case non atteignable, pas seulement les fins).
- Les boucles de re-travail (cycle AVEC sortie) sont en **avertissement** et non
  en erreur : c'est la distinction voulue (re-essai legitime vs blocage).
- Scan `--tous` : **PROPRE sur 11 parcours**, avec 8 boucles de re-travail
  documentees comme voulues (buffy c37->c13b->c13c->c14->c11, cerberus
  c25->c26 / c33->c32 / c15b->c15c, themis c3->c8->c8b->c8c->c8d).

### J2 - Orphelines clio (decouverte de l'outil)

L'outil a **prouve sa valeur des la premiere execution** : il a revele que le
parcours-clio contenait 4 cases vestiges (c6/c6a/c7/c8) de l'ancien flux manuel
(avant les combos maj-readme), invisibles pour valider-case car non-fins.
Retrait via `editer-parcours` (0 pointeur vers chacune) + bump 0.5.2 -> 0.5.3.

### J5 - Tests adaptes

- test-007 : point 13 (catalogue 145 -> 146 + entree detecter-cablages-manquants)
  et point 14 (index-tools Total 111 -> 115).
- test-024 : point 8 (catalogue 145 -> 146).

## Points de vigilance (a signaler, hors perimetre)

1. **`regenerer-catalogue` est bloque** par une erreur pre-existante
   (`generateurs-ligne` : cles dupliquees `branche/mode/source` dans les
   parametres). L'entree catalogue de detecter-cablages-manquants a donc ete
   ajoutee a la main (trie). A corriger dans une mission dediee (Vulcain).
2. **README badge reecrit en cours de mission** : le badge 127 a ete remplace
   par 126 puis retabli (probablement une autre session LLM active en
   parallele qui a mis a jour le README). A verifier lors de la prochaine
   synchronisation README (Clio).

---

**Fin de controle** : Janus reactive Cerberus avec le bilan consolide.
