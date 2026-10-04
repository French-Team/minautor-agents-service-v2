# Controle croise Janus -- --no-journal aux tests (2026-08-11)

**Objet** : verification croisee de l ajout de --no-journal aux 4 tests qui passent
par le generateur (suite de l option combos-moteur v0.3.1 creee par Vulcain).
**Mission** : Cerberus -> Vulcain (combos-moteur --no-journal) -> Morpheus (tests) -> Janus (controle).
**Date** : 2026-08-11
**Verdict** : **VALIDE**

## Controles effectues (J1-J4)

### J1 -- Normes des 4 tests modifies
| Test | ASCII | CRLF | py_compile |
|---|---|---|---|
| test-005-generateurs-commande | 0 | 0 | OK |
| test-002-combos-moteur | 0 | 0 | OK |
| test-003-combos-creer | 0 | 0 | OK |
| test-004-combos-tester-outil | 0 | 0 | OK |

### J1b -- Le .sh du generateur n a PAS recu --no-journal
`grep no.journal generateurs-commande.sh` = **0 occurrence** (conforme : il ne journalise pas
et ne supporte pas l option ; l option n a ete ajoutee qu a l appel py de test-005).

### J2 -- combos-moteur v0.3.1 propage --no-journal (py + sh)
- py : VERSION 0.3.1, `executer_case_generateur(..., no_journal=False)`, `cmd.append("--no-journal")`.
- sh : VERSION 0.3.1, meme logique dans le heredoc python.

### J3 -- generateurs-commande v0.2.3 accepte --no-journal
3 occurrences (argparse + condition de journalisation) dans le .py.

### J4 -- Verification reelle
| Test | code | pollution (lignes registre) |
|---|---|---|
| test-005-generateurs-commande | 0 | 0 |
| test-002-combos-moteur | 0 | 0 |
| test-003-combos-creer | 0 | 0 |
| test-004-combos-tester-outil | 0 | 0 |

**Non-regression complete : 23 OK / 0 KO.**
**Registre apres non-regression : 0 ligne** (source de verite propre, purgee en fin).

## Observations
1. La pollution venait de 4 tests : test-005 (generateur direct, ~30 invocations py),
   test-002/003/004 (combos avec cases generateur via combos-moteur).
2. La methode d identification par test individuel (purge -> lancer -> compter) a permis
   de trouver les 4 pollueurs exacts, y compris les 2 non-evidents (test-003 : 49 lignes,
   test-004 : 3 lignes).
3. Le registre est desormais exploitable comme source de verite des usages reels :
   la non-regression ne le pollue plus.
