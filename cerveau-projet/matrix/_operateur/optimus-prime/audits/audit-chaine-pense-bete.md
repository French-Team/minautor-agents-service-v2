---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
  maj: 2026-10-02
---

# AUDIT -- LA CHAINE PENSE-BETE / SPEC / TODO-LIST EST-ELLE DEVENUE LE MODE DE FONCTIONNEMENT ? (MO-538)

> Question du createur : verifier ce qui a ete fait pour cette serie, qui aurait
> du devenir le mode de fonctionnement des missions ; quand le pilote injecte une
> mission, il declenche la suite, puis il utilise les documents pour diriger
> Optimus et suivre la progression -- et les checklist du pilote doivent etre
> combinees pour suivre le travail de Optimus.

## LE CONSTAT EN QUATRE LIGNES

Le travail de reflexion est FAIT et il est bon. Le mode de fonctionnement
n EXISTE PAS, et il ne peut pas exister tel qu il est ecrit : la chaine s arrete
a l ecriture de la todo-list, elle n a aucun etat d execution. Les deux liens que
le createur nomme -- le declencheur a l injection, la consommation par la
checklist -- ne sont pas dans le code.

## CE QUI EST FAIT, ET MIEUX QUE PREVU

1. LA PORTE EXISTE ET JOUE. `chaine-pense-bete` (matrice/data/outils/), trois
   verbes : `naitre`, `avancer`, `etat`. Elle tient l identite de l objet DANS
   sa carte d identite (nom stable, statut, les trois ids), et elle tient un
   INDEX du domicile, pose par elle.
2. QUATRE OBJETS ONT ETE NES : PB-001 (doctrine de la chaine), PB-002 (reparation
   de masse des 32 refus muets), PB-003 (suivi du pilote), PB-004 (bruit des
   documents sources). Chacun a son document unique, sa carte, ses trois ids, un
   NEMESIS joue, et un fichier sur disque.
3. LE TODO DE PB-003 EST LIVRE, SES QUATRE TACHES. T1 la liste fermee des pannes
   du pilote existe (suivi-pilote/pannes-declarees.json, 29 Ko) ; T2 la porte
   suivi-pilote existe avec sa vue derivee et son journal de verdicts ; T3 les
   templates invisibles existent (6 familles) ; T4 le controle permanent existe,
   c est un maillon de la non-regression. Et le livrable de T1 travaille : c est
   lui qui a nomme la panne `bilan-adresse-a-autre`, qui a attrape deux fois
   dans la journee.
4. LA PORTE EST PROPOSEE A L AGENT : elle figure dans la liste de priorite de
   modes_emploi.py (rang 1381), donc l injection peut la servir.

## LES DEUX LIENS DU CREATEUR, MESURES ABSENTS

### LIEN 1 -- LE DECLENCHEUR : il n existe pas

On cherche un appel a la chaine dans le code qui injecte, classe ou conduit.
LE SEUL appelant de tout le projet est une liste de priorite dans
`pilote/injection/modes_emploi.py`. Donc : quand le pilote injecte une mission,
la chaine ne se declenche pas. Elle ne se declenche que si l agent pense a
l appeler -- et elle n est dans aucune checklist, donc l occasion ne se presente
qu au hasard.

### LIEN 2 -- LA CONSOMMATION ET LE SUIVI : il n existe pas

Aucun code du pilote ne lit `preparation/chaine-*.md`. La checklist du pilote est
une liste fermee ecrite en dur dans `pilote/checklist/listes.py` : `TYPES`,
`ETAPES_COMMUNES`, `ETAPES_PAR_TYPE`, `VERIFICATIONS_PAR_TYPE`, `OUTILS_PAR_TYPE`.
Elle ne connait ni TD-, ni SP-, ni PB-. Les deux systemes sont PARALLELES : le
travail decompose par la chaine n apparait nulle part dans ce qui dirige
l agent, et ce qui dirige l agent n enrichit jamais la chaine.

## LA CAUSE RACINE, JOUEE PAS AFFIRMEE

J ai appele la porte sur l objet dont le TODO est livre :

    chaine-pense-bete avancer --id PB-003
    REFUS : l'objet est deja au dernier etat (todo-list)

Et le code le dit en une ligne (`constants.py`, ligne 47) :

    ETAPES = (pense-bete, spec, todo)

Trois etats, et `todo` est le DERNIER. La chaine modelise la PRODUCTION d un
document, pas l ACCOMPLISSEMENT d un travail. Les quatre objets sont donc, tous
les quatre, a `statut: todo` -- y compris PB-003 dont les quatre taches sont
livrees. Aucun ne peut passer a `fait`, parce que cet etat n existe pas.

C est la que le reve du createur s arrete : "suivre la progression" suppose un
etat de plus. Ce n est pas un oubli d appel, c est un trou dans le modele.

## LA DECISION QUI APPARTIENT AU CREATEUR

Deux facons de le fermer, et elles ne se valent pas.

A. DONNER UN QUATRIEME ETAT A LA CHAINE (`execute`, avec sa date et son
   emplacement dans le document). La chaine devient un suiveur de travail. Cout :
   on touche au modele arbitre en MO-220 (trois etats, trois familles d ids).

B. LAIRE LA CHAINE ETRE UN PRODUCTEUR, et faire de la CHECKLIST son lecteur :
   la checklist du pilote lit le TD- de l objet lie a la mission, et le pilote
   coche l avancement a partir de la. Cout : aucun changement de modele, mais la
   checklist cesse d etre une liste fermee ecrite en dur.

Ma recommandation est B, et la mesure la justifie : les trois etats actuels
decrivent un document, pas un travail -- les garder tels quels et y ajouter un
etat de travail, c est faire cohabiter deux modeles dans une seule porte. Et le
vivier de la checklist est deja la que le pilote range ses listes par type. Le
trou de l etat d execution se bouche du cote de la checklist, qui est deja le
lieu ou l agent lit ce qu il a a faire.

Ce que je ne decide pas seul : le createur peut vouloir A, parce que la chaine
doit rester la seule source du decoupage. C est un choix de modele, pas une
question de mesure.

## CE QUI RESTE, QUOI QU IL EN SOIT

- Aucun des quatre objets ne peut etre marque fait, faute d etat execute. Ils
  resteront tous a `statut: todo`, meme apres un travail complet. C est un fait
  a dire au createur, pas un bug a corriger en douce.
- Le declencheur de l injection reste absent, que l on choisisse A ou B : sous A
  comme sous B, il faut une regle qui dise QUELLES missions ouvrent une chaine.
  Ma mesure : toutes ne le doivent pas. Une mission de reparation n a pas besoin
  d etre decoupee en PB/SP/TD, elle a une liste d etapes qui suffit. La regle
  que je proposerais est celle du createur lui-meme, celle de son crochet
  `[tache]` : une demande analysee et decortiquee AVANT d etre dirigee. Donc la
  chaine ne s ouvre que sur ce que le crochet ouvre.
- Les TODO de PB-001, PB-002 et PB-004 n ont pas ete livres comme celui de
  PB-003. PB-004 (le bruit des documents sources) est d ailleurs toujours pose au
  vrac de l entonnoir sous EO-482, sous forme de question du createur.

## LA PREUVE, RASSEMBLEE

1. La porte repond, elle tient quatre objets, elle tient un index.
2. `avancer` sur un objet livre REFUSE, en nommant le dernier etat.
3. `constants.py` ligne 47 nomme trois etats, dont aucun n est un etat de travail.
4. La seule reference du projet a la chaine hors de son code est une liste de
   priorite d injection : elle peut la proposer, jamais la declencher.
5. `checklist/listes.py` ne contient ni TD-, ni SP-, ni PB- : la consommation
   n existe pas.
