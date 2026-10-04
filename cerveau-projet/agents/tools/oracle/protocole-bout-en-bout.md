# Protocole bout en bout -- pilote et super-pilote v1

## Objectif

Chaque mission suit un vol complet et trace :

```text
DEMANDE -> DECOLLAGE -> LARGAGE -> PRISE -> TRAVAIL -> FIN -> RECUPERATION -> RETOUR A L AEROPORT
```

Une remise ou une lecture de message ne constitue pas une fin. Une mission
est terminee uniquement apres une reaction explicite, un bilan et une fin
pilotee.

## Etats obligatoires

| Etat | Responsable | Preuve minimale |
|---|---|---|
| DEPOSEE | emetteur | identifiant unique |
| DECOLLAGE | pilote/super-pilote | trace de vol + etat de carte |
| LARGUEE | pilote | cible et identifiant |
| PRISE | agent | mission passee a PRISE |
| EN_TRAVAIL | agent | accuse explicite + action commencee |
| FIN | agent/pilote | bilan et trace FIN |
| RECUPEREE | pilote | maillon precedent reactive |
| RETOUR AEROPORT | pilote | retour vers Oracle |
| CLOTUREE | Oracle | aucune etape pendante |

## Regles

1. Une mission possede un identifiant stable et un vol_id.
2. Le super-pilote ne passe pas a l etape suivante avant FIN ou mise en attente.
3. Le pilote distingue lu, accuse, en_travail et terminee.
4. Toute reaction reference mission_id et message_id.
5. Toute activation pose un DEBUT une seule fois.
6. Toute fin pose un FIN une seule fois.
7. Une fin sans bilan est refusee.
8. Une relance reutilise l identifiant de mission et incremente son compteur.
9. Apres la limite de relances, la mission est mise en quarantaine.
10. Le super-pilote orchestre ; il ne fait pas le travail de l agent.
11. Le pilote ne prend pas une decision metier libre a la place de l agent.
12. Toute incoherence arrete le vol et produit une alerte unique.

## Contrat de reaction agent

```text
REAGIR mission=<mission_id> message=<message_id> action="..." bilan="..."
```

La reaction enregistre accuse, reaction_date, action, bilan, mission_id et
vol_id. L agent passe explicitement par EN_TRAVAIL puis fournit sa FIN.

## Controle du pilote

Le pilote verifie l habilitation, l unicite de l agent cible, l ordre DEBUT/FIN,
les reactions attendues et le retour vers Oracle. Une mission PRISE sans
reaction au dela du delai est suspendue et signalee.

## Controle du super-pilote

Le super-pilote impose une seule etape en vol, sauf parallelisme declare. Il
ne lance l etape suivante qu apres preuve de fin de l etape courante et ferme
la chaine par un retour a Oracle.

## Echec et quarantaine

Une mission est mise en quarantaine si l agent ne reagit pas, si l identifiant
est absent ou duplique, si l agent n est pas habilite, si FIN arrive avant
DEBUT, ou si une etape suivante part trop tot. La quarantaine preserve la
preuve mais retire la mission du flux actif.
