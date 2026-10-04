# Controle croise -- Pattern 16 ALLEGEMENT aligne budget pondere (Janus)

**Date** : 2026-08-11
**Mission** : controle croise de l'alignement du Pattern 16 (ALLEGEMENT) de la spec-guider-parcours sur le budget pondere (correction par Promethee)
**Verdict** : **VALIDE** (7 points J1-J7 verts, non-regression 22/22)

## Points controles

| # | Controle | Resultat |
|---|---|---|
| J1 | Ancienne regle ("plus de 3 indices" / "> 3 indices") : 0 occurrence dans spec-guider-parcours | OK |
| J2 | Budget pondere : 6 occurrences (PRINCIPE UNE PLACE + Pattern 16) | OK |
| J3 | Bump Pattern 16 : v0.2.29 present (3x), v0.2.28 absent | OK |
| J4 | Normes : non-ASCII 0, CRLF 0 | OK |
| J5 | Non-regression complete : 22/22 OK | OK |
| J6 | Coherence 3 specs : memes seuils (100 car. / 0,5 / 1 / 3,0 / 160) dans spec-refonte v0.1.3, spec-valider-case v1.1.0, spec-guider-parcours v0.6.2 | OK |
| J7 | Tests sensibles : test-014 13/13, test-015 10/10, test-009 23/23 | OK |

## Corrections validees

| Element | Correction |
|---|---|
| Pattern 16, Probleme | "valider-case : plus de 3 indices" -> "budget pondere des indices depasse 3,0 unites -- court <= 100 car. = 0,5 / long > 100 = 1 -- ou texte de regle > 160 caracteres" |
| Pattern 16, Etape 1 | "(seuils : > 3 indices...)" -> "(seuils : poids des indices > 3,0 unites, ou texte de regle > 160 caracteres)" |
| Pattern 16, Etape 2 LEVIER B | "(plus de 3 indices)" -> "(poids des indices > 3,0 unites)" |
| Version Pattern 16 | v0.2.28 -> v0.2.29 (titre + 2 listes de versions) |

## Lecons

1. Une meme regle peut etre documentee a PLUSIEURS endroits d'une meme spec : le Pattern 16 (methode d'allegement) utilisait encore l'ancienne regle alors que le PRINCIPE UNE PLACE (meme fichier) documentait deja le budget pondere. Le scan de coherence spec <-> spec est indispensable, pas seulement spec <-> outil.
2. La coherence des SEUILS est verifiable par un simple grep croise sur les 3 specs : 100 car. / 0,5 / 1 / 3,0 / 160 identiques partout.
3. Le bump de version d'un pattern doit etre coherent sur toutes ses occurrences (titre + listes).
4. test-014 ne depend pas du texte du Pattern 16 : aucun test casse par cette correction documentaire.
