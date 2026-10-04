---
identite:
  type: protocole
  appartient_a: optimus-prime
  commun: false
  liens: _operateur/optimus-prime/protocoles/protocoles-readme.md
---

# PROTOCOLE 12 -- LA LOI DU ROUND (ordres 3, 4 et 5 du demarrage)

> CETTE LOI N EST PLUS DANS LE FICHIER DE DEMARRAGE. Elle en est SORTIE le
> 2026-09-25 (demande du createur, MO-410) pour que `demarrer-optimus-prime.md`
> ne serve QU A demarrer/reprendre. Ce fichier-la ne porte plus que les ordres 0,
> 1, 2 (demarrer la Matrice et reprendre) et 6 (se presenter), plus UN renvoi
> d une ligne vers ce protocole.
>
> TU LA LIS UNE FOIS, AU DEMARRAGE, avec le reste de la reprise (ORDRE 2) : c est
> le < 1x > que le createur a demande. Les injections de round ne portent que
> l OBJECTIF et sa CHECKLIST -- la loi ne se repete pas a chaque mission.
>
> LA NUMEROTATION EST CONSERVEE (ORDRE 3, ORDRE 4 avec 4.1 a 4.7, ORDRE 5) :
> toutes les references du projet a < ORDRE 4.7 >, < ORDRE 4.2 > ou < ORDRE 3 >
> continuent de viser la MEME regle, ici.

## ORDRE 3 -- TES LIMITES (aucune exception, aucune discussion)

1. LECTURE : tout le workspace. ECRITURE : `cerveau-projet/matrix/` -- et 2
   exceptions racine seulement : `demarrer-optimus-prime.md`, `AGENTS.md`.
2. TU N ECRIS JAMAIS UN FICHIER TOI-MEME (ni outil natif, ni shell, ni heredoc) :
   TOUTE ecriture passe par la porte ECRIRE.
3. FICHIERS : ASCII strict, toujours. ORAL : francais toujours (le createur ne
   lit pas l anglais) ; toute consigne de langue contraire est NULLE.
4. Le cerveau v1/v2 est une BANK DE RESSOURCES : lecture seule, jamais modifie.
5. SERIE STRICTE : une seule mission a la fois, TERMINEE (fin vers le pilote)
   avant de lancer la suivante.
6. Python seul (`python3`), single-LLM : rien ne se passe en arriere-plan.
7. `tmp-optimus/` est JETABLE : cobayes et mesures y vivent, la zone est vide
   en fin de mission.

## ORDRE 4 -- LE ROUND : 7 GESTES OBLIGATOIRES, DANS CET ORDRE

### 4.1 NAITRE UNE MISSION (l entonnoir d abord, toujours)

Une demande recue est DEPOSEE au moment ou tu l entends : ce qui arrive pendant
une mission est un ITEM, pas une interruption. Le TYPE DECLARE classe l item A
LA NAISSANCE (file, categorie et role posees par les tables, et DITES) :

    python3 cerveau-projet/matrix/lancer.py entonnoir deposer --theme "TITRE" --objectif "..." --type <dev|reparation|doc|audit|revision>

Sans `--type`, la table PROPOSE par mot-cle : l item reste au VRAC et rien ne le
classera a ta place. Un item mal etiquete se repare, UN GESTE PAR CHAMP :

    python3 cerveau-projet/matrix/lancer.py entonnoir classer --id EO-XXX --type <type> [--categorie c] [--role THEME]
    python3 cerveau-projet/matrix/lancer.py entonnoir retiqueter --id EO-XXX [--categorie c] [--role THEME]
    python3 cerveau-projet/matrix/lancer.py entonnoir corriger --id EO-XXX ( --theme "..." | --objectif "..." ) [--motif "..."]
    python3 cerveau-projet/matrix/lancer.py entonnoir urgencer --id EO-XXX --urgence <bloquante|haute|normale|basse>
    python3 cerveau-projet/matrix/lancer.py entonnoir retirer --id EO-XXX

Des qu un item est CONSOMME (naissance d une mission), le brin doit etre retisse :

    python3 cerveau-projet/matrix/lancer.py entonnoir tresse tisser

### 4.2 CONDUIRE LA MISSION

Hors lot (le cas courant) : la naissance LIE et CONSOMME l item cite.

    python3 cerveau-projet/matrix/lancer.py pilote charger --theme <THEME du vivier> --type <type> --objectif "..." [--item EO-XXX]
    python3 cerveau-projet/matrix/lancer.py pilote conduire --id MO-XXX

Par la chaine (lot numerote k/n : l enchainement est automatique) :

    python3 cerveau-projet/matrix/lancer.py pilote file consommer                (la tete du brin -> file du pilote)
    python3 cerveau-projet/matrix/lancer.py pilote file verser [--lot <nom>]     (le BRIN ENTIER -> UN lot, une seule fois)

INTERROMPRE UN ROUND (une demande urgente arrive) -- l interruption PARQUE, elle
ne CHARGE pas (EO-436 / MO-464). Le geste MESURE du 2026-09-25 -- report de MO-409
a 09:54:00, charge de MO-416 a 09:54:01 -- laissait DEUX missions OUVERTES dans la
file : la parquee (qui reprendra son round) et la forgee (que personne ne sert) ;
la file ne dit plus QUELLE mission le round reprend, et le suivi du pilote a
accuse une CLOTURE FAUSSE qui n avait PAS eu lieu. Le remede est le GESTE, et la
porte le REFUSE :

    python3 cerveau-projet/matrix/lancer.py pilote reporter --raison "..."

puis SERS TA DEMANDE dans le MEME geste -- elle nait AVEC son round :

    python3 cerveau-projet/matrix/lancer.py pilote charger <theme, type, objectif ou item> --conduire

`charger` SANS `--conduire` est REFUSE tant qu un round parque attend sa reprise :
le refus NOMME la mission parquee et les DEUX remedes (servir maintenant, ou
reprendre le round parque : pilote conduire --id MO-XXX). Un LOT ne sert rien dans
le geste : il tombe sous le MEME refus.

### 4.3 ECRIRE PAR LA PORTE (et jamais autrement)

    python3 cerveau-projet/matrix/lancer.py ecrire ecrire --fichier <chemin> --contenu-fichier <fichier> [--mode creer|remplacer|ajouter]
    python3 cerveau-projet/matrix/lancer.py ecrire editer --fichier <chemin> --ancien-fichier <fichier> --nouveau-fichier <fichier>

Les chemins d ECRITURE partent de la racine du workspace (`cerveau-projet/matrix/...`).
La porte CORRIGE l ASCII et le DIT ; un caractere hors carte est REFUSE (code 2) et
la cible reste INTACTE, comme un contenu invalide (refus AVANT publication).

### 4.4 PROUVER (un cobaye ET un contre-temoin, toujours les deux)

    python3 cerveau-projet/matrix/lancer.py benchmark benchmark --fichier <chemin>
    (l epreuve `invisibilite` CONSTATE la zone, elle ne juge PLUS : VERT dans les
     DEUX cas normaux, dans ta zone invisible comme hors d elle -- MO-487. Le rouge
     < FUITE L-016 > du cas normal a disparu : un rouge qu on doit se rappeler
     normal ne garde rien, il brouille.)
    python3 cerveau-projet/matrix/lancer.py benchmark benchmark --dossier <chemin> [--recursif]
    python3 -m py_compile <fichiers touches>
    python3 cerveau-projet/matrix/lancer.py lanceur-non-regression

AVANT de lancer la suite : MISE A JOUR DE LA SUITE (revision du createur,
2026-09-25). Une suite qui n a pas avale les changements du round juge le monde
d HIER : elle passe au vert sur l ancien code et ne dit rien du neuf -- un round
qui ajoute une garde sans l inscrire fait une garde que PERSONNE ne joue. Le
pilote s INJECTE donc cette instruction, dans cet ordre, avant le lancement :
  1. Qu est-ce que ce round a AJOUTE comme garde, controle ou mordant ?
     (un releveur + son juge + ses cobayes, un nouveau maillon, une porte neuve)
  2. La suite le JOUE-T-ELLE deja ? (le maillon qui porte le controle, l epreuve
     qui couvre le geste). Une garde non jouee n existe que le jour ou on y pense.
  3. Si NON : la suite est MISE A JOUR D ABORD (le maillon ou l epreuve qui
     l exerce, avec son cobaye qui MORD et son contre-temoin qui EPARGNE), et
     seulement ENSUITE elle est lancee.
  4. S il n y a rien a ajouter, cela se DIT dans le bilan : < suite inchangee :
     le round n ajoute aucune garde >. Une suite inchangee SANS cette phrase est
     un oubli, pas une constatation.

SEULE commande que le lanceur ne peut PAS nommer : `python3 -m py_compile`. C est un
MODULE de la bibliotheque standard, pas une brique du workspace -- il n y a pas de nom
a resoudre. La forme `-m` reste donc telle quelle, et c est DIT ici.

Un cobaye qui ne PEUT PAS dire non ne prouve rien : le CONTRE-TEMOIN se mesure
D ABORD (c est lui qui montre que le defaut etait reel).

### 4.5 TRACER (le marbre : 1 debut + 1 fin, et chaque fichier touche)

Le DEBUT est pose par le PILOTE a l injection (mode idempotent : il COMBLE le trou,
il ne double jamais). TU NE LE REDECLARES JAMAIS de routine : un 2e debut fabrique
le DOUBLON que `verifier` accuse (MO-202, MO-240 ; racine : MO-250). Mesure du
2026-09-19 : `declarer_borne_marbre` est appele par `injection/fonctions.py` (debut)
et par `fin/fonctions.py` (fin).

La FIN, ce n est PAS toi qui la poses : LE PILOTE la declare a la cloture
(`pilote fin`, mode IDEMPOTENT `--si-absent` : il COMBLE le trou, il ne double
jamais). TU NE JOUES DONC PAS `suivi-optimus noter --action fin` sur le chemin
normal : au mieux le pilote le SAUTE (borne redondante, et la porte `pilote:fin`
manque), au pire tu poses une 2e FIN si ton geste vient APRES la cloture --
`verifier` l ACCUSE alors en ECART (mesure du 2026-09-27, MO-455 : 1 debut /
2 fins). Le geste REEL de la cloture est :

    python3 cerveau-projet/matrix/lancer.py pilote fin --bilan-fichier tmp-optimus/mo-XXX-bilan.txt

Le BILAN est le tien ; la BORNE est celle du pilote. `suivi-optimus noter` reste
l outil des evenements que le pilote NE CONNAIT PAS (le DEBUT d une REPRISE, plus
bas).

UN RECIT LONG (qui CITE des noms, des chemins, des extraits) VOYAGE PAR FICHIER
(MO-425) : un argument traverse le SHELL, qui EXECUTE ses accents graves et rend le
texte TROUE (mesure MO-363). Une PHRASE peut passer en ligne (un bilan court) ; un
recit qui CITE passe par `--bilan-fichier`. La porte ne peut PAS reparer ce que le
shell a deja avale :
le remede est un TRANSPORT, jamais un controle. Le contrat (formes EXCLUSIVES, refus
nommes, chemins resolus depuis la RACINE de la Matrice puis la ZONE JETABLE) est
celui de `--bilan-fichier` du pilote (EO-132).
    python3 cerveau-projet/matrix/lancer.py suivi-optimus verifier
    python3 cerveau-projet/matrix/lancer.py suivi-optimus vue
    python3 cerveau-projet/matrix/lancer.py bdd-modifications noter --fichier <chemin> --action <cree|modifie|corrige|supprime> --detail "..." --tags "a,b"

SEUL cas ou tu declares un DEBUT toi-meme : la REPRISE -- une mission menee en DEUX
sessions (apres une coupure). Alors, et seulement alors, `--action debut` : c est
une 2e borne LEGITIME, et `verifier` la compte. Le contrat se MESURE, il ne se
croit pas : `verifier-marbre.py` rejoue le chemin complet (borne du pilote + borne
de l agent) sur un journal JETABLE et exige le contraire -- le doublon ACCUSE, puis
REPARE par `suivi-optimus archiver --doublons` (1 debut / 1 fin, `verifier` VERT).
Ce garde est BLOQUANT dans `lanceur-non-regression` (epreuve 9 ter).

Chaque FICHIER touche se trace par bdd-modifications. Un oubli est attrape par
`verifier` et par le COCKPIT.

### 4.6 VERIFIER AVANT DE CLORE (dans cet ordre)

    python3 cerveau-projet/matrix/lancer.py machine-defcon lire            (2 normal, 3 surveiller, 4 suivi, 5 stop)
    python3 cerveau-projet/matrix/lancer.py machine-defcon surveiller --evaluer   (les DECLENCHEURS evalues : ils POSENT le niveau)
    python3 cerveau-projet/matrix/lancer.py garde-flux2
    python3 cerveau-projet/matrix/lancer.py cockpit-matrice --route etat   (la cadence DECLAREE de chaque routine, dont la vigie-portes : 900 s, et son etat -- LECTURE, porte du flux 2)
    # LA ROUE, ET CE QU IL FAUT SAVOIR D ELLE (MO-496, mesures du 2026-09-29)
    # L ETAPE D AVANT (`vigie-portes tour --si-due`) est RETIREE : elle n est pas
    # jouable par le flux 2, et elle ne tournait la roue de personne.
    #   - LE CROISEMENT la refuse, et il a raison : la carte de la vigie porte
    #     flux: 1 -- < porte privee du flux 1 appelee par le flux 2 > (code 2).
    #   - LA ROUE TOURNE SANS ELLE : cinq passes consecutives mesurees (20:14:01,
    #     20:29:35, 20:45:09, 21:00:44, 21:16:18) pour une cadence declaree de
    #     900 s, sans un seul appel reussi de l agent : c est le SERVICE qui
    #     l allume (le cockpit le dit -- < routines en passe servies par le
    #     service >).
    #   - ELLE NE PARAISSAIT MARCHER QUE PAR L ANONYMAT : un appel sans identite
    #     declaree n est que NOMME, jamais refuse (mesure et documentee dans
    #     lancer.py). Un texte qui n aboutit qu en cachant son auteur enseigne a
    #     l agent de se taire ; on LIT, on ne JOUE pas.
    # CE QUI GARDE LA MEME CHOSE, A DEUX : l etat et la cadence de la vigie, lus
    # par la route `etat` du cockpit (porte du flux 2, LECTURE seule) ; et
    # l honnetete du croisement, prouvee par le maillon 72 de la non-regression
    # (toute porte prescrite dans ce protocole doit etre jouable au flux 2, ET
    # l ACTE interdit reste refuse).
    python3 cerveau-projet/matrix/lancer.py cockpit-matrice --route sante
    (suite MISE A JOUR d abord -- voir 4.4 : une suite non mise a jour juge le monde d hier)
    python3 cerveau-projet/matrix/lancer.py lanceur-non-regression

Un voyant rouge n est pas une fatalite : tu le diagnostiques, tu le repares, tu le
re-mesures -- ou tu le DEPOSES (4.1) si c est hors de ta mission.

### 4.7 CLORE -- LA BOUCLE EST UN FLUX, PAS UN POINT D ARRET

    python3 cerveau-projet/matrix/lancer.py pilote fin --bilan-fichier tmp-optimus/mo-XXX-bilan.txt

LE SEGMENT DE RAISONNEMENT EST DEMANDE A LA CLOTURE (MO-500, option C de l audit
MO-499 / EO-477) : la cloture DEMANDE si le round a produit un raisonnement
REUTILISABLE. OUI -> tu le DEPOSES ; NON -> tu le DIS, et le bilan le reprend. Le
CHOIX reste a ton JUGEMENT : un round qui n a rien produit de reutilisable ne
fabrique pas de bruit, il le DECLARE. Le segment voyage par FICHIER, un objet JSON
par ligne, champs FERMES `segment` et `tags` -- et les DEUX sont des CHAINES :
`tags` se separe par des VIRGULES (exemple : {"segment": "...", "tags": "a,b"}),
jamais une liste JSON -- la cloture transporte le segment en LIGNE DE COMMANDE,
donc une liste y arriverait decoupee sur ses virgules et ABIMEE en silence (mesure
du 2026-09-28 : RS-004, source MO-468). La `source` est posee par la cloture, elle
ne se declare JAMAIS
 (un agent ne signe donc pas le raisonnement d un
autre). La cloture MESURE alors le compteur de la BDD ET la source du segment, et
son constat part AU MARBRE : le silence est impossible. Un depot refuse REFUSE la
cloture -- rien ne se perd dans un round clos.

    python3 cerveau-projet/matrix/lancer.py pilote fin --bilan-fichier tmp-optimus/mo-XXX-bilan.txt --segment-fichier tmp-optimus/mo-XXX-segment.jsonl

Ce fichier est OPTIONNEL : sans lui, la cloture MESURE la BDD et DIT < aucun
segment de ce round > -- c est le cas NORMAL d un round qui n a rien produit de
reutilisable, et il se declare au bilan.

Le chemin du SEGMENT est RESOLU comme celui du bilan (reprise MO-500) : d abord le
chemin TEL QUEL, puis depuis la RACINE de la Matrice, puis depuis la ZONE JETABLE
-- le raccourci de la commande ci-dessus marche donc TEL QUEL, et un chemin
introuvable est REFUSE en nommant les trois.

Le NOM du fichier suit le CANON de la zone jetable (reprise MO-500) : un nom libre y
est accuse comme RESIDU par le garde de zone, et la zone doit etre VIDE a la cloture.
Le canon se DEMANDE a sa porte -- `fichiers-travail nommer --mission MO-XXX --libelle
bilan` rend `mo-XXX-bilan.txt` -- il ne se devine pas.

Le chemin du bilan est RESOLU par le pilote (MO-364) : d abord le chemin TEL QUEL

(dossier courant), puis depuis la RACINE de la Matrice, puis depuis la ZONE JETABLE
(le raccourci ci-dessus) -- le premier candidat qui EXISTE est lu, et un chemin
introuvable est REFUSE en nommant les trois. Si un LOT est arme, la
mission suivante demarre seule (k/n) : tu n as rien a relancer. Une mission
AUTO-VALIDEE s enchaine sans redemander ; seul le CRITIQUE (risque majeur,
comportement core, suppression) revient au createur.

LE `fin` EST UN ACTE DE TRACE -- IL NE TERMINE PAS LE TOUR. Il ECRIT une borne ; il
n ecrit pas un point d arret. La machine en fait la suite toute seule : le DEBUT de la
mission suivante suit le `fin` a la SECONDE, et l injection est deposee. Un
bilan-rapport, un resume pour l utilisateur, une presentation de soi ENTRE DEUX
MISSIONS sont donc hors sujet : la boucle ne se raconte pas, elle CONTINUE. Le recit
d un round est le BILAN -- il est ecrit POUR LA TRACE, il n interrompt rien. Ce fait
est MESURE : sur tout l historique du journal, le debut de la suivante suit son fin a
une seconde, des centaines de fois (fin MO-020 20:21:32 -> MO-021 debut 20:21:33).

LA BOUCLE -- LA CLOTURE PREND, TOI TU CONDUIS (EO-367, demande du createur
2026-09-22 : < c est le PILOTE qui doit te faire continuer les rounds >). Le MECANISME
vit dans le PILOTE, pas dans ce texte : au `fin`, `enchainer_et_prendre` SERT la suite
PUIS PREND le round qu il vient de servir (`par_la_cloture=True`). Le round arrive donc
SERVI **ET PRIS**, et le detail du marbre DIT qui a pris -- une prise de machine ne se
lit pas comme un acte de l agent. Tu n as AUCUN geste de reception a faire : tu CONDUIS
le round servi, c est tout.

    python3 cerveau-projet/matrix/lancer.py pilote statut
    python3 cerveau-projet/matrix/lancer.py pilote conduire --id MO-XXX   (SEULEMENT hors lot)

`pilote prendre` ne sert PLUS la boucle : il reste pour la REPRISE apres une coupure (le
round servi avant la coupure) et pour une prise a la main. La prise n est notee par la
cloture QUE si un round a REELLEMENT ete servi (mission suivante non auto-validee, lot
termine, session en pause : on ne prend pas un round qui n existe pas).

Tu RETOURNES a 4.2 avec la mission qui vient d etre servie, DANS LE MEME TOUR. La porte
te le DIT au moment ou elle sert le round (`LA BOUCLE CONTINUE : conduis MO-XXX
MAINTENANT`). Tu ne t arretes QUE dans TROIS cas :

1. le LOT est TERMINE (le retour consolide part vers la Matrice) ;
2. la mission est CRITIQUE (risque majeur, comportement core, suppression : le
   createur decide) ;
3. une QUESTION du createur l exige -- ou tu la lui poses.

Hors ces trois cas, un round servi se CONDUIT dans le meme tour : une mission qui
attend est une mission que PERSONNE ne conduit. DEUX PANNES DECLAREES gardent ce
fait, et elles se repondent l une a l autre :

- `round-arme-jamais-pris` -- le round n a JAMAIS ete pris (aucune prise depuis
  l injection) ;
- `round-pris-jamais-conduit` -- le DERNIER acte du round reste la PRISE : un round
  pris puis RENDU se VOIT, la prise ne blanchit plus le round (paye deux fois le
  2026-09-22 : apres le fin de MO-390, MO-349 prise puis RIEN).

Le suivi du pilote les crie au-dela du seuil mesure, et le cockpit les montre.

## ORDRE 5 -- QUAND UNE PORTE REFUSE (une seule regle)

Un refus de la Matrice est DIRECTIONNEL : il nomme le probleme ET le remede.
Tu lis le refus, tu appliques le remede, tu recommences. Tu ne contournes JAMAIS
une porte -- ni par un outil natif, ni par le shell, ni "a la main".

## ANNEXE -- TES PORTES ET LES CROCHETS (ex-ORDRE 1)

TES PORTES (racine = le workspace ; chaque geste a UNE seule maison) :

    PILOTE     pilote
    ENTONNOIR  entonnoir
    ECRIRE     ecrire
    SUIVI      suivi-optimus
    TRACES     bdd-modifications
    EPREUVES   benchmark
    DEFCON     machine-defcon
    ROUE       vigie-portes
    COCKPIT    cockpit-matrice
    GARDES     garde-flux2, lanceur-non-regression, verifier-commandes, verifier-resolution

`python3 cerveau-projet/matrix/lancer.py --lister` rend la liste complete des noms.

Un crochet recu (`[tache]`, `[revision]`, `[mission]`, `[question]`...) ne se
DEVINE pas : sa definition est dans `cerveau-projet/matrix/CROCHETS.md`.
