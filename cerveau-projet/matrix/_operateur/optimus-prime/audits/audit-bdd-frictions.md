---
identite:
  type: analyse
  appartient_a: operateur
  commun: false
  version: 1
  date: 2026-10-02
  statut: a-jour
  tags: MO-546,EO-552,bdd-frictions,lacunes,audit
---

# La porte bdd-frictions dort-elle, ou l'agent oublie-t-il de s'en servir ?

Mission **MO-546** (AUDITEUR / audit, EO-552). Mesure du 2026-10-02.

## LA QUESTION

> `bdd-frictions ajouter` est une porte complete et enregistree au registre,
> mais absente du lanceur : elle n est jouable par aucune routine, et les 98
> frictions sont archivees (0 active) depuis le 2026-09-30. Decision createur :
> rappeler la porte au lanceur, ou la laisser volontairement dormante.

## LE PRESUPPOSE, CORRIGE SUR TROIS POINTS

**1. "Absente du lanceur" : vrai, et sans consequence.** Elle ne vit pas dans
`matrice/data/outils/` mais dans la zone privee de l operateur, a
`_operateur/optimus-prime/super-combos/combos/outils/bdd-frictions/`. C'est la
profondeur 3, or le lanceur sert la profondeur 2 au plus (EO-556) : une brique
privee n est pas Lanceur-servie **par construction**, pas par oubli.

**2. "N est jouable par aucune routine" : vrai, et c est la conception.** Aucun
code n appelle `ajouter`. Les frictions sont posees par l AGENT, a la main,
quand il rencontre un defaut -- c est le sens du mot friction. Un appelant
automatique aurait transforme un jugement en Piece.

**3. "L agent ne sait pas qu elle existe" : FAUX.** L'injection de MO-546, que
je viens de lire, declare **trois** outils, et le premier d entre eux est
`bdd-frictions`, avec son mode d'emploi complet :

```
rechercher, bdd-frictions, sc-006-lacunes
```

L outil est donc passe a l agent **a chaque round**, nomm et usage fourni. Ce
n est pas un instrument livre a personne : c est un instrument livre a tous, et
que personne n employer's.

## L ETAT MESURE

| Mesure | Valeur |
|---|---|
| Frictions au total | 98 (avant cet audit) |
| Actives | **0** |
| Archivees validees | 96 |
| Archivees annulees | 2 |
| Premiere / derniere friction | 2026-09-11 09:44 / **2026-09-30 07:05** |
| Par type | 73 `outil`, 10 `regle`, 5 `protocole`, 4 `ordre`, 4 `convention`, 2 `combo` |
| Par gravite | 72 majeures, 24 mineures, 2 bloquantes |
| Recidives | 0 |

## LE CONSTAT QUI VAUT LA MESURE

Le 2026-09-30, la derniere friction a ete posee. Les deux journees suivantes ont
produit des defauts reels -- et **aucune friction n'a ete deposee**.

Je suis l'agent qui les a rencontres, et je les avais laisses passer :

- une preuve non discriminante, verte dans les deux cas, dans un maillon de la
  non-regression ;
- un dry-run git muet rendant zero alors que le motif en matchait 910 ;
- un garde bloquant qui a refuse deux depots legitimes a tort ;
- une affirmation de restitution ecrite sans l'avoir mesuree.

Chacun meritait une ligne. Aucune n'a ete ecrite. Ce n est pas une panne de la
porte : c'est une habitude absente.

## LA PREUVE QUE LA PORTE SERT

Plutot que de le decider, je l'ai joue. Quatre frictions de cet audit meme, posees
par la porte, avec type, gravite, frequence et mission :

| ID | type | gravite | frequence | le fait |
|---|---|---|---|---|
| 99 | regle | majeure | recurrente | un contre-temoin vert dans les deux cas ne prouve rien |
| 100 | outil | mineure | ponctuelle | un dry-run `--quiet` rend un zero que rien ne distingue d une absence |
| 101 | outil | majeure | recurrente | un garde bloquant accuse un acces d attribut |
| 102 | convention | majeure | ponctuelle | une affirmation de restitution ecrite sans la mesurer |

Apres le geste : **102 frictions, 4 actives** (contre 0 avant), 96 validees,
2 annulees. La porte a accepte les quatre, avec leur mission d'origine, et les
rend en une lecture.

## LA DECISION, ET ELLE N'EST PAS CELLE-LA

La question posee est : rappeler la porte au lanceur, ou la laisser dormante ?
Les deux options passent a cote du fait.

- **La rappeler au lanceur ne servirait a rien.** Elle est deja nommee a chaque
  round. Un agent ne la cherche pas parce qu'elle manque a l'annuaire : il ne la
  cherche pas parce qu'il n'a pas l'habitude de le faire.
- **La laisser dormante est une formule fausse** : elle n'est pas dormante. Elle
  est disponible, servie, et inutilisee.

La seule question qui reste est donc : **qu'est-ce qui, dans un round, rappelle a
l'agent qu'il doit y penser ?** Trois pistes, toutes reversibles :

1. une ligne durapper DU CHECKLIST de la mission (une case a cocher), ce qui la
   rend visible au lieu d'etre un savoir-faire ;
2. un rappel dans la remise de cloture, quand l'agent vient de dire ce qu'il a
   rencontre ;
3. un reflexe dans le super-combo `sc-006-lacunes`, qui mesure deja la panne et
   pourrait la dire au moment ou il mesure.

La piste 3 est la moins couteuse : l'instrument existe, il contient deja la
mesure du 2026-10-02, et il se joue au moment du constat.

## CE QUE JE NE DECIDE PAS

Le registre a 184 entrees, la porte est complete, et le lanceur sert la
profondeur 2 par choix. Modifier la profondeur de service serait une regle
d arborescence, pas une reparation de lacune. Je le depose plutot que de le
faire : c'est une decision de structure, pas un defaut mesure.

## CE QUI RESTE A QUALIFIER

Les quatre frictions posees sont ACTIVES : elles attendent d etre qualifiees
(validee ou annulee). C'est le travail du round suivant, pas de celui-ci -- un
audit qui qualifierait ses propres constats les ferait disappear au lieu de les
traiter.
