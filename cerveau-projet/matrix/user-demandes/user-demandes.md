---
identite:
  type: passerelle
  appartient_a: optimus-prime
  commun: false
---

# PASSERELLE USER -- user <-> optimus (via la Matrice)

Ce fichier est TON CANAL. Tu y ecris tes demandes en clair, dans ta langue. La
Matrice les LIT, les suit, les extrait vers son entonnoir, puis un agent les
mene a terme. Une demande extraite est RETIREE d ici : a la fin, ce fichier ne
garde que ce HEAD et tes demandes pas encore extraites.

Tes mots ne sont jamais reecrits : ni tes accents, ni tes apostrophes, ni tes
crochets. Seul le HEAD et le squelette ci-dessous sont ecrits par la Matrice.

## 1. LE SQUELETTE D UNE DEMANDE (a copier tel quel)

    ##A-FAIRE################################
    ##FAIT###################################
    ##A-CONTROLER############################
    [<un des crochets listes plus bas>] <ta demande, en une phrase>

    pourquoi : <la raison, si tu en as une>

    resultat attendu : <ce que tu verras quand ce sera fait>

Tu supprimes les lignes dont tu n as pas besoin. Le seul element OBLIGATOIRE est
le CROCHET : c est lui, et lui seul, dit ce que ta demande declenche.

## 2. LES PATTERNS D ETAPE

<!-- CROCHETS:DEBUT -->
| Pattern | Ce qu il signifie |
|---|---|
| `##A-FAIRE###` | a faire : rien n a encore ete vu |
| `##FAIT###` | vu et execute |
| `##A-CONTROLER###` | execute, mais pas encore controle, valide ou certifie |
| `##CERTIFIER###` | fait, controle et certifie |
<!-- CROCHETS:FIN -->

Un bloc de tete indique ou en est la demande. Ils se lisent PAR ORDRE : le
dernier avant la demande gagne.

Un pattern ne franchit JAMAIS deux etapes dans la meme mission : chaque etape
est une injection, donc une MISSION a part entiere.

## 3. LES MOTS ENTRE CROCHETS

Le crochet dit l INTENTION, et l intention decide de l ordre dans la file.
C est donc le crochet le plus sur de ton texte : un crochet faux met une
construction devant une question, ou l inverse.

<!-- CROCHETS:DEBUT -->
| Crochet | Ce que tu demandes | Ce que ca declenche |
|---|---|---|
| `[mission]` | construire, creer ou corriger | le travail part en CONSTRUCTION |
| `[tache]` | une commande a executer | une tache : corriger, mesurer ou construire |
| `[revision]` | revoir l existant et le dire AVANT d ecrire | revision de l existant |
| `[question]` | une reponse, sans construire | une reponse, avant toute construction |
| `[audit]` | un etat des lieux, lecture seule | un rapport, aucune reparation |
| `[???]` | tu ne sais pas encore ce qu il faut faire | un CADRAGE : la liste des actions est preparee avant le travail |
| `[preparer]` | preparer, cadrer ou planifier | une preparation |
| `[preparation]` | idem [preparer] | une preparation |
| `[cablage]` | sur une demande ancienne : verifier son CABLAGE | controle du cablage |
| `[investigation]` | sur une demande ancienne : verifier qu elle a abouti ET qu elle est fonctionnelle, puis certifier | investigation, puis certification |
| `[crochet]` | creer, corriger ou retirer un mot entre crochets | le PROCESS de fabrication, injecte par le pilote |
<!-- CROCHETS:FIN -->

Ce tableau n est pas recopie : il est genere depuis la table de la porte, a
chaque fois. Un crochet nouveau y apparait donc des qu il est ajoute -- et le
controle refuse de publier tant que la porte et ce tableau ne disent pas la
meme chose.

Trois distinctions qui se perdent souvent :

  - `[audit]` et `[investigation]` ne sont PAS pareil. `[audit]` regarde
    l EXISTANT (un code, un dossier, un etat). `[investigation]` interroge une
    DEMANDE ANCIENNE pour savoir si elle a abouti et si elle tient encore.
  - `[???]` et `[preparer]` ne sont PAS pareil non plus. `[???]` dit "je ne sais
    pas" et attend qu on prepare le chemin ; `[preparer]` dit "je sais, je veux
    qu on organise".
  - `[mission]` et `[tache]` ne sont PAS pareil. `[mission]` construit ;
    `[tache]` commande une action qui peut aussi etre une mesure ou un correctif.

## 4. CE QUI PEUT BLOQUER UNE DEMANDE AVANT SON DEPOT

La porte de conformite passe le canal AVANT toute extraction. Elle rend trois
verdicts, et un seul refus suffit a arreter le depot :

| Verdict | Ce que ca veut dire | Ce que tu fais |
|---|---|---|
| `CONFORME` | rien a corriger | rien |
| `CORRIGIBLE` | un geste MECANIQUE (crochet en majuscules, caractere convertible) | tu le corriges, le rapport nomme la ligne |
| `REFUSE` | une DECISION te revient : crochet inconnu, caractere hors carte, ou crochet qui ne dit pas ce que la demande fait | tu corriges la demande dans le canal |

Un crochet INCONNU n est jamais devine a ta place : la demande reste au canal,
et son type n est pas choisi pour toi.

## 5. LES AUTRES PIECES DU DOSSIER

| Piece | Ce qu elle est |
|---|---|
| `user-demandes.md` | CE FICHIER : ton canal. Toi seul y ecris les demandes. |
| `template-demande.md` | le formulaire : le squelette, un exemple rempli, et comment inserer une demande |
| `README.md` | le role du dossier et le chemin d une demande, de bout en bout |
| `concepts/le-vivier.md` | tes idees de concept pour la v3 |

## 6. CE QUE LA MATRICE NE FAIT JAMAIS ICI

1. Elle ne reecrit pas tes mots. L extraction RETIRE une demande servie, elle ne
   la reformule pas.
2. Elle ne corrige pas ton orthographe : une correction de prose peut inverser un
   sens. Elle est signalee, jamais appliquee.
3. Elle ne juge pas le fond. Le canal est HORS JUGEMENT (MO-475).

## SPEC D ORIGINE DU CREATEUR (conservee telle quelle)

Ce bloc est ta reflexion de depart, celle qui a fait naitre ce canal. Elle est
CONSERVEE TELLE QUELLE : la Matrice ne la reecrit pas, elle ne la corrige pas
et elle ne la complete pas. Elle reste le temoin de ce qui a ete demande, a
cote du mode d emploi qui le sert.

# Ce document doit servir de passerelle de communication entre user & optimus via la matrice.
# doit permettre de suivre les demandes de 'user' et d'avoir un suivi de ce fichier. 
# instaurer des conventions de delimitation qui facilite l'encadrement (debut/fin) de mes demandes et retrouvable dans notre moteur de recherche.
# ce fichier doit permettre a 'user' d'ajouter ces demandes dans ce fichier qui devra etre consulter regulierement pour le suivi.
# avoir une legende des types de delimitations possibles.
# une delimitation vide = pattern à lire
# une delimitation avec un mot = declenche une instruction ou suite d'instruction.
# exemple : 
# phase 1 :
# - """##A-FAIRE################################""" = vide
# - """##FAIT###################################""" = pattern qui a deja été 'vu + executer'
# phase 2 :
# - """##A-CONTROLER############################""" = pattern qui a deja été 'vu + executer' mais n'a pas été 'controler/valider/certifier'
# - """##CERTIFIER##############################""" = pattern qui a été 'vu + executer' -> 'controler/valider/certifier'
# un pattern ne pas passer les etapes dans la meme mission(les injections seront differentes pour chaque etape de ce processus) ! 

--> [MISSIONS] POUR CE FICHIER :
	- preparer le readme.md du dossier 
		- description du contenu et des dossiers(sujet-individuel à traiter ) dans le dossier
	- preparer le head du fichier
	- preparer sa carte d'identité
	- preparer le template + type de delimiteur
	- extraire les missions de ce fichier
	- quand une mission a été extraite -> elle est retiré de ce fichier -> au final : il conserve le head (carte d'indentité + mode d emploi) + mission pas encore extraite. 
	- analyser ou & comment il doit etre calé et integré a la matrice vers son inbox/outbox -> vers pilote -> pour diriger optimus
	- preparer les missions pour creer la suite d'outils dedié / routine de surveillance / routine de suivi, etc...
	- se lancer dans l'aventure... 


##A-FAIRE################################
##FAIT###################################
##A-CONTROLER############################
[revision] comment optimus choisi et utilise les outils ? 
pourquoi ? : je vois souvent des problemes quand tu les utilise.
raison : tu oublie 'comment les utiliser'.
solution : le pilote doit injecter un mini mode d'emploi de l'outil.
pourquoi : optimus sera plus a l'aise si on lui fourni le mode d'emploie que de devoir lire l'outils pour se souvenir de son utilisation. on doit corriger 'regles, protocoles, conventions, etc' pour generailser cette pratique. 'fournir des outils, combos, super-combos sans explication' n'est pas productif et genere des actions inutile.
##A-FAIRE################################
##FAIT###################################
##A-CONTROLER############################
[revision] on doit verifier le fonctionnement des rotations, les .bak, les archives, les audit, les constats, etc. 
pourquoi doivent ils vivre si longtemps, si les informations importantes sont dans les bdd ? 
les .bak sont utile au moment des changements, etc(securité 1). par la suite quand tout est bon, ils deviennent inutile -> ils doivent etre 'archivé'. 
les archives sont utile pendant quelques heures (securité 2) mais en sachant que l'on a les bdd et le git. elles doivent etre supprimer avant chaque commit (je pense ?)

##A-FAIRE################################
##FAIT###################################
##A-CONTROLER############################
[question] comment les missions sont tel preparer avant d'etre injecter dans l'entonnoir -> dans le pilote ? 
pourquoi : je veux inserer une etape pour preparer la liste des outils que optimus doit avoir a sa disposition pour la mission 
resultat : pour chaque mission, la liste des outils qu'il aura besoin et fourni dans la mission, ce qui permet de savoir quel mode d'emploi, optimus va avoir besoin pour sa mission, si la mission d'apres et differente, elle va surement utiliser des outils differents, si la liste a été preparé en amont , au moment de preparer la mission, le pilote pourra facilement injecter les modes d'emploies au bon moment. --> [preparer] -> transformer en [mission] 

##A-FAIRE################################
##FAIT###################################
##A-CONTROLER############################
[???] comment ameliorer le process pour les "tmp-optimus/MOxxx-xxx-old ou new.txt, les cobayes, etc..."  comme je ne vois pas ce que tu fais, je ne comprend pas ce qui ce passe ? 
si on creer des combos completement dedié aux fichier tmp qui seront creer par optimus(invisible pour le cameleon) ou le cameleon(qui devra avoir ces propres outils). 
j'imagine optimus comme si il etait 'user', user aurait du suivre un formulaire pour remplir chaque partie qui compose ses correctifs. 
le super-combos permet de fournir les espaces a remplir, il les remplie simplement et c'est le combos qui transforme les fichiers a sa place. par la suite, cela nous permet d'avoir des possibilités infinis sur le fonctionnement, on pourra y automatiser des actions (analayse, verif, constant, test, etc...sans que optimus ne doivent intervenir)
optimus -> lance le super-combos -> le super-combos contient tout ce quil faut pour obtenir le resultat final -> optimus repond et/ou remplie le formulaire (comme si il etait 'user') -> le super-combos utilise les informations dans son deroulement et fourni le rapport des changements effectuté. c'est le super-combos qui va verifier (dry/wet) avant de modifier et mettre à jour les fichiers connexes que optimus aurait oublié, etc...
on conserve le concept du 'old' & 'new' qui permette de mieux cerné les modifications 

##A-FAIRE################################
##FAIT###################################
##A-CONTROLER############################
[question] est-ce que le pilote de optimus injecte les infos de 'user-profil.md' ?

##A-FAIRE################################
[question] est il possible d'utiliser le presse-papier de windows ? 

##A-FAIRE################################
##FAIT###################################
##A-CONTROLER############################
[mission] verifier si les outbox ont des rotations pour eviter de depasser les 5mo.

##A-FAIRE################################
##FAIT###################################
##A-CONTROLER############################
[mission] comme on l a fait dans la v1, je voudrais que l'on transforme 'N IMPORTE QUOI' en mermaid -> svg.
interet : pouvoir composer dans mermaid -> convertir en svg = pour que optimus(mermaid) & user(svg) suivre et reperer les erreur et incoherence qui serait caché dans les parcours de optimus et par la suite : 'le vivier'. 

##A-FAIRE################################
##FAIT###################################
##A-CONTROLER############################
[question] est-il possible de separé les portes communes et celle qui serait 'privée' que le cameleon ne pourait pas utiliser. je vois que le fait d'avoir que des portes communes, nous oblige 'toujours' a verifier par nous meme, ce qui n'est pas productif ? 

##A-FAIRE################################
##FAIT###################################
##A-CONTROLER############################
[???] creer une routine qui va verifier si les cartes d'identités des fichiers contiennent bien les liens des fichiers connecté a eux (qui doit permettre de facilement retrouver les fichiers connecté a modifier) -> on doit avoir aussi un template de nos cartes d'identités qui vont etre tres importante pour etre retrouvé par notre moteur de recherche

##A-FAIRE################################
##FAIT###################################
##A-CONTROLER############################
[mission] comme on l'a fait pour nemesis et le 'OUI,MAIS...' on doit travailler sur : """si j'etais 'user' , je ne voudrais pas devoir faire ça et ça pour obtenir mon resultat.
le but :automatiser toutes les taches ingrates que 'user' ne voudrais pas devoir toujours faire quand il doit faire ceci ou cela pour obtenir un resultat de tout types""". 
pourquoi : il va etre tres utile d'avoir cette phase de remise en question qui doit permettre de refflechir a qui peut etre eviter (automatiser) pour par la suite en faire les process pour les agents 
philosophie : si on peut faciliter la vie de 'user', on peut le faire aussi pour optimus et le cameleon

##A-FAIRE################################
##FAIT###################################
##A-CONTROLER############################
[???] quand on ajoute une routine, pour l'instant, on duplique une routine existante (mauvaise pratique) -> on doit avoir un template (source de verité plus fiable) qui doit TOUJOURS etre utiliser avec notre outil 'copier/coller' qu'on a mis en place (a verifier ou il est encore dans les mission en attente)

##A-FAIRE################################
##FAIT###################################
##A-CONTROLER############################
##CERTIFIER##############################
[audit] je voudrais savoir ou son stocké les bdd de la v3 ?  

##A-FAIRE################################
##FAIT###################################
##A-CONTROLER############################
[MISSION] "TOUTE EVOLUTION SIGNIFICATIVE OU OBLIGATOIRE DOIT ETRE DECIDER ET EXECUTER" doit devenir une regle immuable et un protocole.

##A-FAIRE################################
##FAIT###################################
##A-CONTROLER############################
[mission] on doit revoir le declenchement des routines , leur duree de vie et leur cycle. 
quand on demarre la matrice, c'est elle qui gere le demarrage des routines. 
probleme : elles tournent en permanence alors que l'on pourrait les allumer quand elles doivent 'agir' , elle ferait leur travail, puis elle s'eteind. 
au final , la matrice doit avoir un planning qui contiendrait les delais des routines et la mecanique de rotation d'allumage. la matrice qui doit avoir un service qui gere le planning des routines, les demarre individuellement, recois leur resultat, transforme les problemes en message important, urgent, etc. pour quelle soient prise en compte rapidement.

##A-FAIRE################################
[MISSION] on doit creer des nouveaux mots entre crochets :
- [investigation] + ancienne demande de user -> declenche un cycle de controle pour verifier si elle a été mené a son terme + si elle est fonctionnelle + validation et certification.
- [cablage] + ancienne demande de user -> declenche un cycle de controle pour verifier le cablage de la demande de user. 
ajouter [investigation] aux 'mots entre crochets'.
[cablage] doit etre ajouter aux sous-process.

##A-FAIRE################################
[cablage] renforcer ou creer le protocole de raisonnement : 
- un raisonnement ne peut pas etre 'continu' et sans traces.
- il doit etre progressif et tracé.
quand on raisonne en 'continu', on accumule des donnees qui finnissent finisse a la poubelle alors que l'on pourrait s'en servir pour les raisonnement futur sur les memes sujets.
quand on raisonne 'progressivement', chaque partie du raisonnement doit devenir un 'segment' du raisonnement general. chaque segment devient plus concret et concis pour la suite du raisonnement et permet de collecter les informations et les conserver 'plus loin' que la fenetre de context du llm. ces segments pourrait etre reutilisé dans des raisonnement futur qui serait sur le meme sujet. 
on doit ameliorer l'utilisation la bdd des lecons qui doit etre 'pertinente' sans 'surcharger' les injections
- le raisonnement et les leçons doivent etre utilisé ensemble pour devenir plus efficace. on devrait avoir une bdd 'raisonnement' qui va contenir les segments et pourront etre facilement retrouver par notre moteur de recherche. un segment doit avoir sa carte d'identité. (creer le template) 

##A-FAIRE################################
[mission] on doit lister nos besoins de template -> creer les templates manquants : 
- templates :
	- leçons
	- frictions
	- regles immuables
	- conventions
	- protocoles
	- carte d'identité
	- informations systeme
	- environnement de travail
l'interet : obtenir une fiche technique de travail (alleger & optimal sans perte) et reduire le bruit (consomation inutile)

##A-FAIRE################################
[???] je voudrais que l'on reflechisse à un 'concept basé sur les alias' pour obtenir des lignes de commandes plus courte et propre pour nos outils, combos, super-combos.(inspire des snippets) tu en penses quoi ? on aurait une routine qui gere les listes d'outils, combos, super-combos. quand optimus veut utiliser l'outil, il n'aurait qu'a ecrire l'alias + les flags (quelque chose comme ça, a refflechir...) cela va pemettre aussi d'avoir dans le pilote et les outils, combos, super-combos : des aides plus compact et legere (les liens seraient dans le fichier de liens dans la matrice)
style : """{@->ecrire -aide ...""" -> trouver un style personnalisé qui ne sera pas confondu.

##A-FAIRE################################
[mission] on doit comprendre pourquoi nos routines qui surveille les flux ne detectent pas les elements qui ne sont pas cabler ! 
- on doit mettre en place 'une equipe de pisteurs' qui doivent pouvoir suivre une direction dans les flux, ils doivent le suivre regulierement, si ils sont stoppé dans le flux, ils s'arrete et le signale en urgence et passe en defcon4, la matrice doit savoir pourquoi (bug, cablage, integration, theme, parcours, etc...) chaque pisteur aura une partie a pister a intervalle regulier (en respectant la config de la machine de user)

##A-FAIRE################################
[mission] creer le super-combos 'lacunes' : il doit servir à retrouver les lacunes sur des sujets precis ou general. dans l'idee, j'imagine un super-combos qui va permettre de rechercher et retrouver des fragments precis qui doivent etre corriger, ameliorer, creer, etc parce qe l'on a des lacunes sur un sujet (exemple : si on detecte que optimus ou le cameleon reproduise souvent les memes erreurs, etc) grace a ce super-combos, on doit etre capable de combler cette lacune. (comme on l a fait pour nemesis, on doit avoir des parcours dedié à chaque phase de ce super-combos : 'rechercher les lacunes' , 'comparer', 'investiguer', 'analyser' , 'QQCP'(QUi, QUOI, COMMENT, POURQUOI)). le travail obtenu de chaque phase va etre utilisé pour la phase suivante.

##A-FAIRE################################
[mission] creer le super-combos 'table-ronde' : permettra de reunir plusieurs profils(role) dedié à une façon de penser et refflechir les choses. la table-rond va reunir les 5 profils qui vont devoir chacun fournir leur vision et approche en fonction : du probleme, de la demande, du sujet mis sur la table. on doit etablir une boucle des 5 profils sur 3 rounds :
exemple:
- le sujet -> profil 1 -> fourni son analyse / profil 2 -> fourni son analyse / etc.
une fois que les 5 profils ont fourni leur 1° analyse : le contenu de la table a changé, elle contient maintenant les 5 analyses : cela lance le round 2 qui se base manteant sur le nouveau contenu de la table (les 5 analyses) -> a la fin du round 2 -> le contenu de la table devient les 5 nouvelles analyses -> qui devient le contenu du round 3 -> une fois que le round 3 est terminé, un 6° profil va faire la synthese des 5 dernieres analyses pour en faire un contenu reutilisable par la suite pour en faire une ou plusieurs missions. 
on a deja les methodes 'nemesis' + 'karpathy' -> on pourrait creer ces 2 roles et refflechir aux 3 autres roles + le decideur final.

##A-FAIRE################################
[mission] on va creer les differents fichier de suivi et leur outils dedié pour : la matrice, les routines, les espions, les outils, le pilote de optimus, du cameleon. on va devoir etre capable de suivre tous ces parties maitresse dans la v3. 

##A-FAIRE################################
[preparer] on va ajouter un mot entre crochet qui va declencher une serie de plusieurs mot entre crochet pour avoir une suite d'action qui vont permettre une analyse poussé avant de chercher a resoudre la demande sans avoir toutes les informations necessaire. 
on va utiliser "[???]".
[???] -> doit lancer un parcours dedié qui va permettre à optimus de constituer sa liste -> qui doit devenir une suite de missions 'collé les une aux autres' (elles doivent former un ensemble qui devra etre injecter dans l'entonnoir comme une seule mission qui va contenir plusieurs missions : audit, nemeis, etc pour obtenir une suite logique et au final : notre mission qui va contenir l'ensemble des missions a enchainer de bout en bout). la mission ne sera pas prioritaire, elle sera placer dans la file d'attente normal sauf si classer comme urgente.

##A-FAIRE################################
[???] on doit ameliorer le dogwatch de optimus et du cameleon pour qu'il puisse suivre leur flux et detecter les goulots d'etranglements (temps, tokens, ressources)

##A-FAIRE################################
[???] on doit comprendre pourquoi le llm utilise son outil native 'search' au lieu de notre moteur de recherche qui serait plus efficace. on doit comprendre d'ou vient cette lacune. 
pour moi, quand il se lance dans une mission, soit il n'utilie pas le pilote de optimus, soit le pilote a un bug : notre moteur de recherche doit toujours faire partie des outils pour les missions.

##A-FAIRE################################
[???] on doit mettre en place tout ce qui va etre necessaire pour la documentation (outils, combos, routine, espion) :
- on doit pouvoir : retrouver, lister, classer, ordonner, produire un dossier complet qui permet de 'TOUT' savoir sur la V3 à la racine du workspace. 
nom du dossier : "documentation-v3" qi va contenir un lexique detaillé + une suite de .md qui permettrons de facilement trouver et lire les parties que l'on veux consulter.
pourquoi : la documentation est eparpillé dans toute la v3 : le but etant d'avoir a la racine un dossier de documention 'maitre' pour eviter de devoir chercher partout dans la v3 , la documentation que l'on a besoin de lire.
- chaque doc a sa carte d'identité (pour le moteur de recherche)
- on doit continué a avoir nos docs proche de leur dossier/fichier + dans la docs 'maitre' -> le/les lexiques qui permettent la navigation amelioré de la doc de la v3.

##A-FAIRE################################
[preparation] on va devoir creer tout les fichiers (regles, protocoles, conventions, theme) pour le depot "git". on doit revoir sa description et son utilité. depuis que j'utilise des llm, je me rend compte qu'il ne sont pas en phase avec l'utilisation du 'git'. 
le depot 'git' est une sauvegarde vivante partagée. ce qui veut dire qu'elle n'est une source de verité que si le travail en cours est 'mort' et qu'il faille revenir dans un etat fonctionnel. 
son utilisation : 
- on ne sauvegarde que quand on va commencer une nouvelle mission(critique) pour nous garantir de pouvoir revenir en arriere juste avant la mission critique. (on ne sauvegarde JAMAIS a la fin d'une mission qui pourrait etre buggé et non-verifier et valider) <-- c'est une tres mauvaise pratique. si on agit comme ça, on contamine le depot 'git' et donc la sauvegarde qui devrit etre une source de verité parfaite ! 
- les outils 'git' vont devoir etre lister, trier, evalué, bloqué(si besoin). 
- le theme va devoir couvrir plusieurs scenarios pour eviter de faire 'ce qu'il ne faut pas faire' 
- creer un concept evaluation de l'interet de sauvegarder le projet avant des changements critique. 
- chaqu'une de nos interventions ne va toujours merité d'etre sauvegarder une par une : on doit diviser 'ce qui est critique ou pas' et qui merite de proteger le projet en sauvegardant le projet dans le depot 'git'

##A-FAIRE################################
[???] ajouter une routine qui va calculer le temps, les tokens envoyé /reçu , les pointes de cpu/ram , etc. 
cette routine doit tourner en arriere-plan, elle demarre au demarrage du flux 1 ou 2 -> recupere les informations deja produites 
quand elles changent -> si la session n'est pas fini correctement, on doit avoir reussi a conservé les traces de cette routines. on attend jamais la fin de la session pour enregistrer les trace de cette routine (elle doit etre edentifier comme une routine :qua "extreme" qui precise quelle est tres importante et son interet)

##A-FAIRE################################
[mission] il faut corriger 'demarrer-optimus-prime.md'
pourquoi ? : quand je commence une session, je dis """lire demarrer-optimus-prime.md""" pour qu'il demarre la session.
probleme : le llm(si autre modele que 'deepseek') ne fait que lire le fichier au lieu d'executer le fichier
meme si je lui demande de le lire, le fichier doit contenir les instructions qui l'oblige a lire et executer le contenu  du fichier

##A-FAIRE################################
[mission] verifier ce qui a été fait pour la serie 'pense-bete -> spec -> todolist' et qui aurait du devenir le mode de fonctionnement pour les missions. quand le pilote injeecte une mission -> declenche  la suite  -> une fois que la suite est créé -> le pilote utile les documents pour diriger optimus et suivre la progression et le suivi du travail. (les checklist dans le pilote doivent etre combiné pour suivre le travail de optimus) 

##A-FAIRE################################
[mission] reviser la fiche de optimus prime qui doit refleter le veritable 'optimus prime' , cela ne doit pas juste etre le nom d'un agent, notre agent doit devenir 'optimus prime', il va etre tres important d'avoir cette section 'role' pour representer le plus fidelement le personnage designé dans le nom de l'agent. et il va etre important d'injecter regulierment ce role qui doit toujours avoir en tete pour agir au plus proche des criteres du personnage dans 'role'. 

##A-FAIRE################################
[audit] quel sont les differentes appellations comme 'M-xxx', 'MO-xxx', 'EO-xxx', etc... je veux avoir la liste de toutes ces appellations et une breve description de chaqu'une. 

##A-FAIRE################################
[???] tres important de corriger et reviser : comment et quand on injecte les leçons, raisonnement, etc. 
il est important de reussir à injecter les informations necessaire de façon a ce que optimus obtienne des resultats 100% positif plutot que de faire des conneries et s'en rendre compte(je ne sais pas comment ?) pour au final : s'appercevoir que l'informations existé , qu'il se corrige et obtenr son 100% de reussite.

##A-FAIRE################################
[question] serait-il bien d'avoir des library de nos verbe, mot-clé, etc pour faciliter le travail permanent qui sera fait dans la matrice ? si la matrice doit devenir le centre de 'tout', je pense que c'est une bonne idée d avoir des library + des routines de collecte, de depot, de lecture, d'injection, etc... 

##A-FAIRE################################
[mission] creer le parcours pour optimus pour le dossier "user-demande/concepts/". 
a quoi va servir ce dossier : je vais y placer des idées de concept pour la v3.
le parcour va devoir : lire/analyser/contre-dire/preparer la mission principal et ces sous-missions. 
