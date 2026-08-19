# Controle -- Education de Themis aux combos ASCII (Janus)

- **Date** : 2026-08-18
- **Controleur** : Janus (second controle, active par Buffy c8)
- **Objet** : controle final de l education de Themis aux combos ASCII
  (demande utilisateur, 2e volet)
- **Verdict** : **VALIDE**

## Contexte

Demande utilisateur : eduquer Themis aux combos/outils ASCII (sa carte ne
referencait aucun outil ASCII, combo-corriger-ascii jamais utilise, 8 usages
de scripts temporaires). Chaine : Chiron (diagnostic + rapport d education) ->
Buffy (application des corrections de carte) -> Themis (audit CONFORME) ->
Janus (controle final).

## Verifications sous session Janus

1. **valider-cartes-decision --agent themis** : CONFORME (fiche PARCOURS
   v0.5.0 == parcours 0.5.0).
2. **Case c9** ("Ecrire le rapport") : regle ASCII en TETE des indices
   (pattern 2) + indice OUTIL `combos-corriger-non-ascii` (commande
   --full --dry-run). La regle precise le dry OBLIGATOIRE avant wet.
3. **Navigation guider-parcours** : c9 guide vers l outil avec la regle
   ASCII en premier, flux c9 -> c12 conserve.
4. **Fiche themis.md** : table des outils + `combo-corriger-ascii` et
   `combos-corriger-non-ascii` (lignes 153-154), PARCOURS v0.5.0 sync.
5. **Garde-fous** : lock themis MATCH, test-058 6/6 CONFORME, test-006
   19/19, test-027 11/11, bumper 0/0, marbre 8/8, evaluateur 15 liens
   preexistants (0 nouveau), registre JSONL 718/718, aucun residu.
6. **Rapport d education Chiron** : rapport-education-themis-combos-ascii-
   2026-08-18.md present (diagnostic + corrections proposees + lecons).

## Verdict

**VALIDE** -- l education de Themis aux combos ASCII est complete : l outil
combos-corriger-non-ascii est assigne dans la case d ecriture (c9) avec la
regle ASCII en tete (pattern 2), la fiche reference les 2 combos ASCII, tous
les tests et garde-fous sont verts sous la session habilitee. Les 2 volets de
la demande utilisateur (Chiron auto-correction + Themis combos ASCII) sont
termines. La chaine est terminee : je REACTIVE Cerberus avec le bilan
consolide.
