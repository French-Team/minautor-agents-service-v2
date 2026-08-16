# Specification -- detecter-decalages-catalogue

**Version :** 0.2.2
**Statut :** ebauche
**Categorie :** Detecter
**Date :** 2026-08-11
**Agent :** Vulcain
**Historique :** v0.2.1 (PERFORMANCE 2026-08-13 : aides des commandes lancees en PARALLELE -- pool de threads min(16, nb) + CACHE par (interpreteur, script) ; ~85s en serie -> ~14s, goulot test-028 de la suite anti-regression) -> v0.2.0 (round 11 coherence documentaire : SCAN DES SOUS-COMMANDES argparse -- quand l aide racine expose un bloc {sous-cmd1,...}, l outil lance l aide de CHAQUE sous-commande et fusionne les options ; corrige les faux positifs generateurs-case-convertir / generateurs-ligne) -> v0.1.1 (section COMBOS : cles des cases generateur vs catalogue, spec-combos-moteur v0.2.1) -> v0.1.0 (creation)
**Pense-bete source :** scan systematique Atlas 2026-08-09 (scan-catalogue.py dans explorations/, institutionnalise)

## Objectif

Comparer CHAQUE entree du catalogue du generateur (`catalogue-commandes.json`)
a l'interface reelle de son outil (options `--aide` puis `--help` en fallback)
pour garantir **0 decalage modele/interface** avant et apres chaque modification
du catalogue ou generalisation du pilote strict.

## Contexte

- Le test reel Atlas (2026-08-09 10:16) a revele un decalage : `valider-relecture`
  composait `--fichier` alors que l'outil utilise `--agent` (corrige par Vulcain,
  catalogue v0.2.1).
- Le scan systematique Atlas (2026-08-09) a confirme 105 conformes / 0 decalage /
  1 non testable (test formel sans aide) / 0 alerte.
- L'outil institutionalise le script temporaire `scan-catalogue.py` ecrit par
  Atlas dans `explorations/` (infraction : les outils vivent dans tools/, le
  rapport reste une trace dans explorations/).
- Lecons integrees : regex placeholders avec chiffres (`[a-z_0-9]+`), classement
  NON TESTABLE honnete (jamais conforme par defaut), tests formels sans aide.

## Fonctionnalites

| # | Fonctionnalite | Detail |
|---|---|---|
| 1 | Scan complet | Parcourt les entrees du catalogue (defaut : chemin fixe du catalogue) |
| 2 | Interface reelle | Lance chaque script avec `--aide` puis `--help` en fallback (timeout 8s) |
| 3 | Classification | CONFORME / DECALAGE / NON TESTABLE / ALERTE (placeholder obligatoire absent du modele) |
| 4 | Rapport | Rapport markdown avec synthese + detail des decalages + non testables justifies |
| 5 | Sortie parametrable | `--sortie CHEMIN` (defaut : rapport date dans le dossier courant) |
| 6 | Performance | (v0.2.1) Aides lancees en PARALLELE (pool de threads min(16, nb)) + CACHE par (interpreteur, script) : ~85s en serie -> ~14s sur 147 commandes |

## Criteres d'acceptation

1. `python3 detecter-decalages-catalogue.py --version` affiche 0.2.1
2. `python3 detecter-decalages-catalogue.py --aide` affiche l'aide
3. Execution sans argument : rapport ecrit, synthese imprimee (conformes/decalages/non testables/alertes)
4. RACINE calculee correctement (6 niveaux depuis tools/detecter/detecter-decalages-catalogue/) : le scan trouve le catalogue
5. ASCII strict 0 sur py/md/spec, nommage `detecter-decalages-catalogue` valide (prefixe de categorie)
6. Entree au catalogue du generateur : `generateurs-commande --commande detecter-decalages-catalogue` compose et executable
7. Rejouable : meme resultat a chaque execution sur catalogue inchange (idempotence)

## Historique

| Version | Date | Description |
|---|---|---|
| 0.2.2 | 2026-08-16 | PERFORMANCE : sondage SELECTIF - seules les commandes avec flags sont sondees (99 commandes sans flag + 23 tests du catalogue non executes) - goulot detecter-decalages 12.6s -> 4.6s |
| 0.2.1 | 2026-08-13 | PERFORMANCE : aides lancees en parallele (pool de threads min(16, nb)) + CACHE par (interpreteur, script) - goulot test-028 85s -> 14s |
| 0.1.1 | 2026-08-11 | Section COMBOS ajoutee : garde-fou des cles des definitions-combo vs catalogue (KO test-003) |
| 0.1.0 | 2026-08-09 | Creation - institutionnalisation du scan Atlas dans tools/detecter/ |
