# Controle croise Janus -- Registre d usage branche dans les 11 cartes (2026-08-11)

**Objet** : verification croisee du branchement du registre d usage dans les 11 cartes :
nouvelle case dediee "Enregistrer mes usages d outils" (outil PASSE PAR LE GENERATEUR ->
enregistrer-usage-outil) avant chaque fin de mission.
**Chaine** : Cerberus -> Buffy (parcours + fiches) -> Morpheus (6 tests) -> Janus (controle).
**Date** : 2026-08-11
**Verdict** : **VALIDE**

## Controles effectues (J1-J6)

### J1 -- Les 13 nouvelles cases (11 parcours)
| Parcours | Cases | Type | PASSE PAR LE GENERATEUR | Poids | Suivant |
|---|---|---|---|---|---|
| cerberus | c24 | action | OUI | 1.0 | c20 (fin) |
| buffy | c42 | action | OUI | 1.0 | c22 (fin) |
| vulcain | c22, c23 | action | OUI | 1.0 | c9, c15 (fins) |
| morpheus | c20, c21 | action | OUI | 1.0 | c10, c14 (fins) |
| janus | c34 | action | OUI | 1.0 | c10 (fin) |
| atlas | c34 | action | OUI | 1.0 | c11 (fin) |
| themis | c26 | action | OUI | 1.0 | c13 (fin) |
| clio | c19 | action | OUI | 1.0 | c12 (fin) |
| athena/promethee/minerve | c24 | action | OUI | 1.0 | c10 (fin) |

Toutes : indice outil enregistrer-usage-outil (catalogue + chemin, SANS commande en dur = PASSE
PAR LE GENERATEUR) + 1 regle courte. Budget pondere 1.0 <= 3.0 OK.

### J2 -- Navigation reelle
buffy (flux agent) : passe par c42 "Enregistrer mes usages d outils" -> c22 TERMINE.
athena (flux creer + corriger) : passe par c24 -> c10 TERMINE.
cerberus (flux accueil) : passe par c24 -> c20 TERMINE.

### J3 -- valider-cartes-decision --tous : 11/11 CONFORME

### J4 -- Pattern 14 : les 11 fiches mentionnent la version du parcours (0.4.0/0.5.0/0.3.0) OK

### J5 -- Non-regression complete : 23 OK / 0 KO, registre a 0 ligne apres (source de verite propre)

### J6 -- Normes : JSON/LF/ASCII OK sur les 11 parcours + 11 fiches + 6 tests modifies

## Observations
1. Les ecarts valider-case de vulcain (c9e/c15e non joignables, c6c/c12c A ALLEGER) et clio
   (c6c) sont PREEXISTANTS (confirmes via git HEAD avant la mission) : hors perimetre.
2. Le registre d usage est desormais pleinement operationnel : chaque agent passe par la case
   "Enregistrer mes usages d outils" (PASSE PAR LE GENERATEUR) avant de cloturer sa mission.
   Les controles (Janus/Themis) pourront croiser ces traces avec les rapports de mission.
