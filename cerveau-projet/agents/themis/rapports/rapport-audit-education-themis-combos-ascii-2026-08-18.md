# Rapport d audit -- Education de Themis aux combos ASCII (Themis)

- **Date** : 2026-08-18
- **Auditrice** : Themis (evaluation croisee, activee par Buffy c8a)
- **Objet** : audit des modifications appliquees a MA carte et MA fiche pour
  l education aux combos ASCII (demande utilisateur, diagnostic Chiron)
- **Verdict** : **CONFORME**

## Contexte

Demande utilisateur : eduquer Themis aux combos/outils ASCII (sa carte ne
referencait aucun outil ASCII, combo-corriger-ascii jamais utilise, 8 usages
de scripts temporaires). Chiron a diagnostique : regle d outil presente mais
aucun outil ASCII assigne dans le parcours -> inoperante. Buffy a applique
les corrections.

## Verifications independantes

1. **Case c9** ("Ecrire le rapport dans themis/rapports/") : regle ASCII en
   TETE des indices (pattern 2 : rappel ASCII obligatoire dans les cases
   d ecriture) + indice OUTIL `combos-corriger-non-ascii` (commande
   --full --dry-run). La regle precise : verifier apres redaction, dry
   OBLIGATOIRE avant wet.
2. **Navigation guider-parcours** : la case c9 guide vers l outil
   combos-corriger-non-ascii avec la regle ASCII affichee en premier. Le
   flux c9 -> c12 est conserve.
3. **Fiche themis.md** : table des outils enrichie de `combo-corriger-ascii`
   et `combos-corriger-non-ascii` (lignes 153-154). PARCOURS v0.5.0
   synchronisee.
4. **Outil** : combos-corriger-non-ascii v0.3.0-py repond (--version OK).
   Le mode --full (dry obligatoire avant wet) est celui que je devrai
   utiliser apres redaction de rapports.
5. **Garde-fous** : lock themis MATCH, test-058 6/6 CONFORME, bumper 0/0,
   evaluateur 15 liens preexistants (0 nouveau), aucun residu.
6. **valider-cartes --agent themis** : verrouille pour Themis (artefact de
   session, habilities : argus/buffy/janus/vulcain) -- deja verifie CONFORME
   par Buffy sous sa session habilitante.

## Verdict

**CONFORME** -- mon education aux combos ASCII est complete : l outil est
assigne dans la case d ecriture (c9), la regle ASCII est en tete (pattern 2),
ma fiche reference les 2 combos, et tous les garde-fous sont verts. La
prochaine fois que je redige un rapport, je verifierai l ASCII avec
combos-corriger-non-ascii --full (dry puis wet) au lieu de scripts
temporaires. La chaine peut continuer : Buffy -> Janus -> Cerberus.
