# Controle croise -- spec-refonte-cartes-decision v0.1.3 (Janus)

**Date** : 2026-08-11
**Mission** : controle croise de la documentation du BUDGET PONDERE dans la spec-refonte (mise a jour par Promethee)
**Verdict** : **VALIDE** (1 observation non bloquante)

## Points controles

| # | Controle | Resultat |
|---|---|---|
| J1 | Version 0.1.3 + historique complet (v0.1.2 convention cT* conservee) | OK |
| J2 | Ancienne regle "> 3 indices" absente (0 occurrence) | OK |
| J3 | Coherence du modele avec valider-case v1.1.0 : SEUIL_COURT 100, poids 0,5/1, budget 3,0, plafond 160 identiques | OK |
| J4 | Normes : non-ASCII 0, CRLF 0 | OK |
| J5 | Contenu complet : usage --surcharge, verifications Allegement, section 7.1, critere d acceptation 2, version stale valider-case v1.0.2 -> v1.1.0 corrigee | OK |
| J6 | Aucun residu temporaire | OK |

## Observation non bloquante

- **Section 7.1** : le titre dit encore "generateurs-case (v0.2.2 actuel)" alors que l'outil est en **v0.4.2**. Version stale preexistante, hors perimetre de la mission budget pondere. A traiter dans une prochaine passe de synchronisation des versions (spec de reference vs outils).

## Lecons

1. La spec-refonte (spec de reference des outils de cases) reflete desormais exactement le modele implante : les memes seuils (100 car. / 0,5 / 1 / 3,0 / 160) apparaissent dans la spec et dans valider-case v1.1.0.
2. Le croisement spec <-> outil est un controle efficace : verifier que les constantes documentees (SEUIL_COURT, BUDGET_INDICES) correspondent mot pour mot aux valeurs codees.
3. La section 7.1 conserve une version stale (v0.2.2) : penser a inclure les sections "actuel" des spec dans les scans de synchronisation de versions.
