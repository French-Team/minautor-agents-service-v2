---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# LA CHAINE DE PREPARATION DES OUTILS (question createur, EO-504)

Question du createur (reprise de EO-502, deuxieme moitie du meme cable) :
"comment les missions sont-elles preparees avant d etre injectees dans
l entonnoir, puis dans le pilote ? Je veux inserer une etape qui prepare, pour
chaque mission, la liste des outils dont Optimus aura besoin -- pour que le
pilote injecte le bon mode d emploi au bon moment."

## 1. LA CHAINE EXISTE DEJA, DE BOUT EN BOUT

Le createur demande une etape qui n existe pas. Elle existe, et elle est
cablee sur TROIS points mesures :

1. PREPARER (l entonnoir, au moment ou l item est prepare) --
   `entonnoir/preparer/fonctions.py:preparer_outils(etat, identifiant,
   outils_texte)` ecrit la liste d outils de l ITEM, conserve l ancienne
   (CHAMP_OUTILS_AVANT) et l horodate (CHAMP_OUTILS_LE). C est ici, et nulle
   part ailleurs, que la liste se prepare.

2. LE PONT (l item devient une mission) -- `commun.py:2540-2542` RECOPIE
   `item[outils]` dans `mission[outils]`. Une mission porte donc SES outils, et
   deux missions du meme TYPE peuvent en porter de differents.

3. L INJECTION (au moment du round) -- `injection/fonctions.py:
   _noms_des_outils(mission)` lit `mission[outils]` (voie "item") et, si elle est
   vide, se replie sur le type (voie "type"). Puis `charger_modes_emploi`
   extrait le mode d emploi de chaque brique (extrait de la brique elle-meme,
   jamais recopie, M-076).

Donc le mode d emploi "au bon moment" existe deja. Ce que le createur demande
est deja cable.

## 2. LE VRAI PROBLEME, MESURE : PERSONNE NE FAIT L ETAPE 1

La chaine est cablee mais l etape 1 n est jamais jouee. Mesure sur les 85
missions de la file (le meme chiffre que celui mesure en EO-515) : 0 portent
une liste d outils preparee. Le pont recopie donc toujours une liste VIDE, et
l injection retombe a chaque coup sur le repli par type. Le mode d emploi servi
est generique-par-type, jamais la liste reelle de la mission.

Autrement dit : le cable est en place, la prise n est pas branchee.

## 3. LA DECISION QUI MANQUE (et pourquoi on ne peut pas la deviner)

On NE PEUT PAS preparer la liste automatiquement a partir du type de la
mission : le repli par type EST deja cette derivation, et il est justamente ce
que le createur refuse ("fournir des outils sans explication n est pas
productif"). Pour qu une mission porte SES outils, il faut que quelquun qui
sait ce que la mission va appeler -- le PREPAREUR, au moment ou il prepare
l item -- nomme les outils. Ce geste est un ACTE de connaissance, pas une
regle automatique.

La question qui revient donc a la Matrice, et qui n est pas une evidence :
QUIJOUE l etape 1 ? Le createur peut-il la faire porter par l item a son
depot, ou par l entonnoir quand il classe/prepare l item ? Tant que ce
preparateur n est pas designe, le champ restera vide et le repli par type
continuera de servir -- en silence, parce qu il fonctionne.

## 4. VERDICT

La chaine de preparation des outils existe et fonctionne de bout en bout ; le
maillon manquant n est pas un cable, c est un ACTE : preparer la liste au
moment ou l item est prepare. Le geste est cable (preparer_outils), il n est
simplement pas joue. Le preparateur qui doit le jouer est la seule decision
qui reste, et elle appartient au createur.
