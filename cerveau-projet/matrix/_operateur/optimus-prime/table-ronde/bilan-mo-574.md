---
identite:
  type: journal
  appartient_a: optimus-prime
  commun: false
---

# BILAN MO-574 -- LES 137 ARCHIVES DISPARUES, SOLDEES

> Les 237 ecarts de la perte : 237 -> 100. Les 137 solderes ne sont pas
> 137 disparitions a reparer -- ce sont des archives qui n ont jamais existe.

## CE QUE LE CHIFFRE DISAIT, ET CE QU IL DISAIT VRAIMENT

Je repetais "237 ecarts de conservation" depuis deux jours, comme si c etait
une derive dont je ne comprenais pas la cause. Le createur a tranche : une
mission bornee, avec un chiffre attendu. J ai donc mesure au lieu de
supposer, et la mesure a renverse le probleme.

Les 237 se decomposaient en DEUX populations de nature opposee :

| population | nombre | octets | nature |
|---|---|---|---|
| incident du 2026-10-03 | 114 | 3 889 726 | archives nees puis mortes dans la zone effacee |
| anciennes (19-24 septembre) | 23 | 103 251 | purges anciennes, temoin deja "introuvable" |

**Les 114 ne sont pas une faute de conservation. C sont une consequence
mecanique de l incident deja connu.** Ces archives sont nees le jour meme ou
un auto-test a supprime toute la zone `_operateur/`, et elles sont mortes avec
elle. Elles n ont jamais ete versionnees par git : la restauration du
2026-10-03 par `git checkout` rendait les FICHIERS, pas les ARCHIVES, qui
n avaient jamais existe hors de la zone. Aucune porte ne pouvait les sauver,
et personne n avait rien vole.

Le chiffre que j ai repete ne comptait donc pas une derive. Il comptait un
incident deja solde, deux fois.

## LE SOLDE, PAR LA PORTE QUI EXISTE

`bdd-conservation declarer-disparition` (EO-276), avec DEUX motifs distincts
pour que la trace dise la bonne cause a chacun :

- **114** : `incident 2026-10-03 : archive nee dans la zone _operateur effacee
  par un auto-test, morte avec elle ; jamais versionnee par git, donc non
  restaurable`
- **23** : `archive purgee avant sa copie (point age de 2026-09) : le temoin
  la declarait deja introuvable, la disparition precede le temoin`

Simulation blanche d abord, element par element : **137 acceptes, 0 refuses**.
Les quatre refus metier de la porte ont ete verifies un par un avant coup
(aucune source encore presente, aucun contenu vivant dans l archive, un
temoin pour chacun, raison et mission requises).

**La mesure est conservee.** Le temoin portait `origine: introuvable` et
`octets: null` pour ces 137 -- c est-a-dire qu il les avait deja perdus. La
porte n ecrase `octets_avant` que si le temoin en fournit, donc les 114
gardent leur poids (267 octets pour K-362, 7617 pour K-1248...). On a solde
un etat, on n a pas efface une mesure.

## LES 100 QUI RESTENT, ET CE QU ILS SONT

Le compte a change de NATURE en soldant : ce ne sont plus des archives
manquantes, mais l inverse -- `statut=supprime` (contenu purge) alors que
l archive existe encore.

Les 98 de ce lot datent **tous du 2026-10-03** : ce sont les `.bak` que la
restauration a ramenes, et qui ne font pas partie des 137 soldes. Ils
occupent **4 218 060 octets** -- soit la totalite de l ecart en octets, ce qui
confirme que les deux chiffres racontent la meme chose.

Ils ne sont pas soldables par `declarer-disparition` : ce sont des archives
VIVANTES, et `purger-archive` les refuse faute de preuve de recouvrabilite
(les 2 archives datees du depot qu il vise ont un blob absent). C est un
**autre chantier**, et je le dis plutot que de forcer un outil qui refuse.

## CE QUE CETTE MISSION A CHANGE DANS MA FACON DE RAISONNER

Deux choses que j aurais du voir plus tot :

1. **Un chiffre repete n'est pas une cause.** < 237 ecarts > repete deux jours
   est devenu une boite noire. Il suffisait de decomposer par jour : 114 le
   2026-10-03, 23 avant. La boite s'ouvrait en une requete.
2. **J'ai corrige la trace du journal hier (MO-573) et aujourd'hui la BDD de
   conservation. Les deux portaient le meme defaut de nature** -- melanger ce
   qui est un livre et ce qui est une ephemere dans le meme champ. Hier j'ai
   tranche sur l'action `purge` ; aujourd'hui sur le statut `archive`. Le
   meme piege, a deux endroits, et il n'est pas encore epuise.

## CE QUE JE LAISSE OUVERT

- **Les 100 (98 archives `.bak` du 2026-10-03 + 2 sans preuve de
  recouvrabilite)** : un vrai chantier, mais il demande une porte qui n'existe
  pas -- declarer une archive VIVANTE disparue serait un mensonge.
- **Les 6 fichiers de l attribution**, seul KO de la non-regression.
- Le **nonsens** `or True` de `sc-006-lacunes/main.py:339`, toujours la.

## SEGMENT

RS-123 -- Un chiffre que l on repete n est pas une cause : 237 ecarts de
conservation se revelaient etre 114 archives nees et mortes dans un incident
deja solde, et 23 purges anciennes. Le solde s est fait par la porte
existante, a blanc d abord, en conservant la mesure que le temoin avait deja
perdue.

## MESURE FINALE DE LA PORTE

```
origine : 4637 point(s), 136409766 octet(s)
archive : 12   actif : 565   purge : 3735   disparu : 227
ECARTS : 100  (etat avant : 237)
```
