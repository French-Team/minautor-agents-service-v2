# Controle croise : double README (Buffy outillage -> Clio contenu -> Janus)

**Date** : 2026-08-14
**Agent controle** : Janus

## Contexte

L utilisateur a decide de scinder le README en 2 fichiers :
- README.md (racine) = GRAND PUBLIC (titres revus, sans structure ni detail technique)
- cerveau-projet/readme-dev.md = DEVELOPPEURS (detaile, sources de verite uniquement)

Chaine : Buffy (outillage) -> Clio (contenu) -> Janus (controle).

## Outillage (Buffy, controle 13/13)

1. Template readme-dev (cerveau-projet/agents/readme-dev-template.md)
2. Parcours Clio 0.5.5 (branche readme-dev + case c20)
3. Carte Cerberus 0.4.4 (indice section amelioration dans c1b)

## Contenu (Clio)

1. readme-dev.md : vrai README developpeur (15 Ko, 12 sections) base sur les sources
   de verite : demarrage session, identification LLM, multi-session, agents, cartes
   de decision/parcours/indices, outils (131), combos, RVAV, tests + protections,
   auto-amelioration, sources de verite, checklist developpeur.
2. README.md : allege pour le grand public (5.8 Ko) - structure/boite a outils/
   workflow/regles immuables RETIREES, section Amelioration continue AJOUTEE, lien
   vers readme-dev.md, vocabulaire conserve.
3. Version README : refonte majeure 0.3.0 -> 1.0.0 puis bump automatique du combo
   massif (lors du test-020) -> 1.1.0. Source (version-readme.txt) + badge synchronises.

## Verifications

| # | Verification | Resultat |
|---|---|---|
| J1 | readme-dev : 15 Ko, 11 sections, sources citees, brouillon remplace, normes 0/0 | OK |
| J2 | README public : section amelioration, lien readme-dev, sections techniques retirees, normes 0/0 | OK |
| J3 | Badges : Outils-131 (x2), Version 1.1.0 (x2) | OK |
| J4 | test-038 : 7/7 (reconfirme seul apres le bump combo) | OK |
| J5 | test-020 : 46/46 (combos intacts) | OK |
| J6 | 131 outils reels (badge coherent) | OK |
| J7 | combo massive intact (332 lignes - incident d ecrasement restaure par git checkout) | OK |
| J8 | registre : 6 usages clio | OK |

## Verdict

**VALIDER : 16/16 OK** - double README conforme. IMPACT A PREVOIR : test-013
(carte cerberus 0.4.4, version en dur a adapter par Morpheus - compteurs inchanges).

## Note incident

Clio a ecrase par erreur combos-maj-readme-massive.py (write_file sur mauvais
fichier). Restauration immediate par git checkout (aucun dommage). Lecon documentee.
