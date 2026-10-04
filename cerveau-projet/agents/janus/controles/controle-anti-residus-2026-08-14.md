# Controle Janus : correction anti-residus (causes racines)

**Date** : 2026-08-14 | **Controleur** : Janus | **Mission controlee** : Morpheus (correction des 2 causes racines de residus)

## Verdict : VALIDE (11/11)

| # | Verification | Resultat |
|---|---|---|
| J1 | test-004 corrige (forward slashes point 6) : 16/16 | OK |
| J1b | Point 6 en forward slashes (replace antislash) | OK |
| J2 | test-028 corrige : --sortie + tempfile + try/finally | OK |
| J2b | test-028 : 8/8 | OK |
| J3 | rapport detecter-decalages NON regenere (age > 1h, date 22:39 inchangee) | OK |
| J3b | aucun NOUVEAU rapport detecter-decalages a la racine | OK |
| J4 | normes ASCII 0 + LF 0 (test-004 + test-028) | OK |
| J5 | lecon Morpheus anti-residus + complement carte | OK |
| J5b | usages Morpheus au registre (lire-fichier, tester-lancer-non-regression) | OK |
| J6 | 0 dossier temporaire de mission (discipline tmp-*) | OK |
| J7 | KO test-035 documente : 5 problemes (4 preexistants + ecart carte a arbitrer) | OK |

## Les 2 causes racines corrigees
1. **test-004** (residu `analyste-in-console.tmp-test004x.sh`) : le point 6 passait un chemin Windows a backslashes -> shlex.split posix les mangeait -> fichier cree a la racine sous un nom mache, hors du rmtree. Corrige en forward slashes (comme le point 5). Plus aucun .sh ne part a la racine.
2. **test-028** (residu `rapport-detecter-decalages-catalogue-<date>.md`) : le point 5 appelait sans --sortie -> rapport ecrit a la racine par defaut. Corrige : --sortie vers tempfile + suppression try/finally garantie. Preuve : l ancien rapport (22:39) n est plus regenere.

## Ecarts restants a arbitrer (PRE-EXISTANTS, hors perimetre de cette mission)
- **test-035 KO** : 5 problemes evaluer-processus :
  1. FIN_MISSION_ERRONEE morpheus (ligne 171 AGENTS-historique) : mission chrono 00:08 porte 'reactiver Cerberus' - consigne legitime a l epoque (carte renforcee a 17:54) -> faux positif retroactif.
  2. OUTIL_HORS_CARTE buffy : tmp-buffy/ajouter-workspace-gitignore.py (registre 22:43).
  3-4. OUTIL_HORS_CARTE janus : detecter-divergences-version + detecter-residus (registre 22:41).
  5. OUTIL_HORS_CARTE morpheus : tester-lancer-non-regression absent des indices de la carte morpheus (ecart de carte structurel - outil central du testeur non assigne).
- Recommandation : mission dediee Buffy (assigner tester-lancer-non-regression a la carte morpheus + nettoyer les usages scripts temporaires hors carte) puis reverdir la serie e.

## Residus physiques restants (pour Hygie)
- `analyste-in-console.tmp-test004x.sh` (ancien, 13/08 22:39 - non regenere)
- `rapport-detecter-decalages-catalogue-2026-08-13.md` (ancien, 13/08 22:39 - non regenere)
