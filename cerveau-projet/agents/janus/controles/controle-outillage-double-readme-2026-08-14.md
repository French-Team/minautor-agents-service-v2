# Controle croise : outillage double README (Buffy -> Janus)

**Date** : 2026-08-14
**Agent controle** : Janus
**Mission controlee** : outillage des 2 README (public + dev)

## Contexte

L utilisateur a decide de scinder le README en 2 fichiers :
- README.md (racine) = GRAND PUBLIC (titres revus, sans structure ni detail technique)
- cerveau-projet/readme-dev.md = DEVELOPPEURS (detaile, base uniquement sur les sources de verite)

Buffy a realise l OUTILLAGE (le contenu sera rempli par Clio) :
1. Template readme-dev (cerveau-projet/agents/readme-dev-template.md)
2. Parcours Clio 0.5.5 (branche readme-dev + case c20)
3. Carte Cerberus 0.4.4 (indice section amelioration dans c1b)

## Verifications

| # | Verification | Resultat |
|---|---|---|
| J1 | Template readme-dev : present, 10 sections dev, normes 0/0 | OK |
| J2 | Parcours clio 0.5.5 : branche readme-dev + case c20 -> c10 | OK |
| J3 | Carte cerberus 0.4.4 : indice section amelioration c1b | OK |
| J4 | Fiches synchronisees (clio 0.5.5, cerberus 0.4.4) | OK |
| J5 | valider-cartes cerberus + clio : CONFORME | OK |
| J6 | Compteurs carte cerberus inchanges (23/5/5/3) - impact test-013 = version seule | OK |

## Verdict

**VALIDER : 13/13 OK** - outillage conforme. Prochaine etape : Clio remplit les
2 README (branche readme-dev + combo massif pour le public), puis Morpheus adaptera
test-013 (version 0.4.4), puis non-regression.
