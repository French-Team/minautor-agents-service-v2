---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
  mission: MO-156
  statut: valide
---

# CONTRE-ANALYSE (NEMESIS, CASE 5) -- ROTATION DES POINTS DE RESTAURATION

> Sujet attaque : la doctrine proposee pour la famille `.bak.*` -- "garder les N
> plus recents par source, archiver le reste par une porte dediee, jamais un rm".
> Trois axes, trois "OUI, MAIS", chaque fois avec un scenario MESURE. Un "mais"
> sans preuve est rejete (regle du theme).

## AXE 1 -- CAS LIMITES

### OUI, MAIS le nombre N n'est PAS fonde sur le besoin des portes
Mesure : `revert-fichier.py` et `revert-periode.py` prennent tous deux **le
`.bak` LE PLUS RECENT** de la cible (`glob` puis `max` sur la date). Le contrat
des portes exige donc **N = 1**, pas N = 2 ni N = 3. "Garder les N plus recents"
n'est pas une reponse a une mesure : c'est une politique, et un chiffre sans
proprietaire derive (L-100/L-102).
Nombre mesure : N=1 archive 73 fichiers / **1,45 Mo (69 %)** ; N=2 n'archiverait
que 41 fichiers (le gain fond) -- parce que 41 familles n'ont QU'UNE version.

### OUI, MAIS un `.bak` peut etre plus recent que sa source
Scenario : la porte depose le point de restauration AVANT d'ecrire ; si
l'ecriture echoue, le `.bak` devient le SEUL temoin de l'etat d'avant, et il est
plus recent que la source. Mesure du jour : **0 cas sur 75 familles** -- le
danger n'est pas present, il est POSSIBLE. Regle a poser dans la porte :
"ne jamais archiver un point de restauration plus recent que sa source".

### OUI, MAIS une source peut disparaitre
Scenario : la source est supprimee ; le `.bak` devient la derniere copie du
contenu. Mesure du jour : **0 famille orpheline**, mais rien ne l'empeche.
Regle : "ne jamais archiver le DERNIER point de restauration d'une source
absente" (l'archive est reversible, mais un fichier sans source n'a plus de
chemin de restauration naturel).

### OUI, MAIS la forme n'est acquise que si elle est CONFORME
Mesure : **0 bak malforme sur 148** (tous portent `.bak.<8 chiffres>_<6>`, le
motif du domicile). L'exemption du contrat fondamental est donc entierement
acquise ici. Une forme non conforme, elle, sort de l'exemption et n'est PAS une
rotation : la porte doit la SIGNALER, jamais l'absorber.

### OUI, MAIS deux elements ne sont pas de mon perimetre
Mesure : 2 points de restauration vivent dans `tmp-cameleon/` (zone du cameleon,
Flux 1). Regle : SIGNALER, aucune ecriture -- c'est deja leur categorie.

## AXE 2 -- OPTIMISATION

### OUI, MAIS le gain n'est PAS le disque
Mesure : la famille entiere pese **2,11 Mo**. Sur un workspace de cette taille,
le disque n'est pas le sujet. Le vrai gain est ailleurs, et il se mesure :
- **le bruit de surface** : la famille s'invite dans les listages et les
  recherches ; la moitie des familles (**36 / 75**) ont leur point de
  restauration le PLUS RECENT vieux de plus de 24 h (mediane 23,6 h, maximum
  255 h) -- autrement dit, la famille est froide pour la moitie du parc ;
- **une REGLE au lieu d'une accumulation** : aujourd'hui rien ne borne (102
  fichiers ecrits le 16/09 seul) ; demain une borne declaree chez le producteur
  (la porte d'ecriture, qui produit la forme).

### OUI, MAIS l'archive ne doit pas DEPLACER le bruit
Scenario : si l'archive est un dossier ordinaire sous `matrix/`, le moteur de
recherche l'indexera comme le reste et le bruit sera deplace, pas supprime.
Regle : l'archive est une **zone declaree exclue** (porte `pause-session
perimetre`), donc couverte par le domicile d'invisibilite (MO-152/MO-153).

## AXE 3 -- SECURITE

### OUI, MAIS l'archive contient du CONTENU INTERNE
Mesure : les points de restauration portent des copies de code de la Matrice et
des fichiers du pilote. Une archive lisible par le cameleon serait une FUITE
nouvelle. Regle : archive = zone invisible declaree, verifiee par l'audit
d'invisibilite apres creation.

### OUI, MAIS une rotation qui court est une course
Scenario : la rotation s'execute pendant qu'une porte ecrit (le `.bak` vient
d'etre depose, la source n'est pas encore a jour). Regles : "archiver d'abord,
jamais supprimer sec", "archive dans le deja connu", "course refusee" -- la
surete existe DEJA dans le moteur partage `data/commun/rotation_journal.py`
(MO-101) : la porte doit le consommer, pas le reinventer.

### OUI, MAIS il faut pouvoir revenir, et le prouver
Le plan exige (case 8) : "archive + actif = origine (aucun octet perdu)". Sans
manifeste (source, date, empreinte, destination) et sans statut `restaure`, une
archive est une croyance. Regle : manifeste obligatoire + empreintes avant/apres.

### OUI, MAIS les gardes ne sont pas tous d'accord sur ce qu'ils surveillent
Mesure : l'espion d'integrite EXCLUT les points de restauration de son registre
(il consomme le motif du domicile) -- archiver ne perturbe donc PAS son registre.
Mais la zone d'archive, elle, sera un dossier neuf dans une zone surveillee :
la porte devra gerer son inscription, sinon l'espion criera (a tort, mais il
crira -- et on ne rend pas un garde muet pour faire passer une rotation).

## CE QUE LA CONTRE-ANALYSE CHANGE DANS LA DOCTRINE

La doctrine "garder les N plus recents" devient un CONTRAT, chiffre et borne :

1. **N = 1** : le contrat des portes de revert ne sert QUE le plus recent.
   Garder plus n'ajoute aucune capacite ; l'archive garde tout (rien n'est perdu).
2. **5 refus** que la porte devra opposer, chacun avec sa mesure :
   jamais un point plus recent que sa source ; jamais le dernier d'une source
   absente ; jamais une forme non conforme (signaler) ; jamais une zone hors
   perimetre (signaler) ; jamais deux fois le meme element (idempotence).
3. **La borne vit chez le PRODUCTEUR** (la porte d'ecriture, qui produit la
   forme), pas chez l'observateur -- lecon de la rotation des usages (MO-101).
4. **L'archive est invisible** (zone declaree exclue) et porte un MANIFESTE.
5. **Rien n'est execute ici** : la case 6 rend un verdict par element, la case 7
   construira la porte et executera, la case 8 verifiera.

## RESERVE ASSUMEE

Cette contre-analyse attaque la doctrine, pas les donnees : aucune mesure du
jour ne montre de perte possible dans l'etat actuel (0 orphelin, 0 ecriture
interrompue, 0 forme non conforme). Le risque est donc **prospectif** : il porte
sur ce que la porte FERA quand ces cas se presenteront -- c'est precisement
pourquoi il doit etre ecrit dans le contrat avant l'acte, et pas apres.
