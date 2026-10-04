---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# REVISION MO-429 -- DECLENCHEMENT, DUREE DE VIE ET CYCLE DES ROUTINES

> Posture REVISEUR (TH-020) : le disque fait foi, chaque changement est propose
> avec son impact, AUCUNE regle modifiee sans decision du createur (proto-6).
> Sujet relu EN ENTIER le 2026-09-26 : routines/ (7 routines + vie), portes
> signaler et maintenir, gardes du flux, moule routine, manuel des outils.
> Source : demande createur (user-demandes.md, crochet [mission], item EO-395
> depose pendant MO-374).

## 1. CE QUI EXISTE AUJOURD HUI (mesures sur disque, jamais de memoire)

### 1.1 Le declenchement

- Point d entree : lancer.py vie activer -> activer.py lance server_matrice.py
  (detache, invisible, motif data/commun/lancement.py).
- Le serveur est l AUTORITE de la vie : il (re)publie les pid files
  (recreer_pid_files), nettoie les fantomes, et RELANCE toute routine morte
  (server_matrice.py, boucle_principale).
- Sa propre cadence de supervision : INTERVALLE_SUPERVISION_SECONDES = 60
  (c est SON temps, jamais celui des routines).
- Table unique : routines/vie/constants.py (BOUCLES, COMMANDE_PAR_NOM,
  CADENCE_PAR_NOM, PID_PAR_NOM, DRAPEAU_PAR_NOM) -- le serveur et l etat
  l IMPORTENT, ils ne la recopient pas.

### 1.2 Les 7 routines et leurs cadences (declarees CHEZ CHACUNE)

| Routine | Cadence declaree | Passe (one-shot) | Allumage actuel |
|---|---|---|---|
| routeur-maintenance | 30 s | routeur.py tour | boucle |
| suivi-sync | 60 s | main.py --once | boucle |
| veille-flux | 300 s | main.py veille | boucle |
| espion-integrite | 300 s | main.py tour | boucle |
| vigie-portes | 900 s | main.py tour [--si-due] | boucle |
| vigie-profil | 900 s | main.py tour | boucle |
| verifier-liens-cartes | 3600 s | main.py --once | boucle |

MESURE (vie etat, 2026-09-26 16:13) : 7/7 routines ACTIVEES + serveur ACTIVE
= 8 processus residents permanents. Soit environ 4112 passes par jour
(2880 routeur + 1440 suivi-sync + 576 veille + 576 espion + 192 vigies +
24 liens).

### 1.3 Duree de vie

- Une routine est un DEMON : ecrire_pid, while True, attendre(cadence, drapeau),
  arret cooperatif par drapeau (zero processus tue).
- Elle vit aussi longtemps que le serveur (adoptee ou relancee par lui).
- Double regime PID NON TRANCHE (MO-458) : le serveur publie les pid de toutes
  les routines SAUF routeur-maintenance, qui ecrit le sien dans sa boucle.

### 1.4 Le cycle d une passe (aujourd hui)

1. rotation du journal verifiee AVANT la passe (un refus ne tue jamais la passe, L-026) ;
2. la passe (tour/fonctions.passer) ;
3. etat court publie : dernieres_passes = anneau (moteur partage data/commun/battement.py) ;
4. faits NOTABLES au journal (ajout seul) ; le trafic normal reste un ETAT ;
5. alertes par la PORTE signaler (niveaux critique / haute / moyenne / basse) ;
6. sommeil COUPE par attendre(cadence, drapeau) -- le drapeau se voit en 2 s.

### 1.5 Ou vont les resultats

- etats courts + journaux : lus par vie etat, le cockpit, les gardes de la suite ;
- journal-lancement.log : la CAUSE du dernier lancement (EO-409 / MO-400), lue
  par vie etat et par le maillon 7 SANS attendre ;
- alertes : signaler -> intercom/matrice/inbox.jsonl -> routeur-maintenance
  (30 s) -> _operateur/maintenance/matrice/inbox.jsonl -> maintenir / pilote
  filtrer -> entonnoir (urgence bloquante / haute / normale / basse) ;
- defcon : veille-flux appelle machine-defcon surveiller a chaque passe VIGILE
  (3 declencheurs declares : perimetre-write niveau 5, marbre-hors-porte
  niveau 5, perimetre-tmp niveau 4) -- audit-defcon-declenchement.md ;
- non-regression : maillon 7 du flux = PID vivant + derniere fin de passe
  fraiche (NB_CADENCES_TOLEREES = 3, plancher TOLERANCE_MINIMALE_SECONDES = 120).

### 1.6 Ce qui existe DEJA et sert directement la demande

- Un verbe POUR UNE PASSE existe deja pour les 7 routines (table 1.2) :
  la mecanique d allumage ponctuel est deja payable aujourd hui ;
- --si-due (vigie-portes) : la passe n est jouee QUE si la cadence declaree est
  echue (EO-291 / MO-363) -- c est le germe du planning ;
- CADENCE_PAR_NOM (vie/constants.py) : dit SEULEMENT OU LIRE chaque cadence --
  voix unique, aucune valeur recopiee ;
- anneau de passes + verifier-cadence (ecart MEDIAN) : declarer, publier et
  mesurer sont trois choses ; mesurer ne demande plus d attendre ;
- trace de lancement (data/commun/lancement.py) : sortie du fils journalisee,
  lecture bornee, cause = derniere ligne non vide ;
- porte signaler : 4 routines s en servent deja (veille-flux, espion-integrite,
  vigie-portes, vigie-profil).

## 2. CE QUI MANQUE (4 lacunes, mesurees)

1. AUCUN PLANNING : le mot n existe que dans la demande (user-demandes.md:108).
   Zero fichier, zero table, zero echeance -- rien au disque.
2. Le service ne sait ALLUMER qu EN BOUCLE : server_matrice ne relance que la
   commande de COMMANDE_PAR_NOM (toujours la boucle). Jamais la passe, jamais
   selon une echeance : il ne connait que mort ou vivant.
3. Le service ne RECOIT PAS le resultat : lancer_invisible est DETACHE (il rend
   le pid, pas de code retour) ; le serveur ne lit ni etat publie ni journal de
   lancement pour DECIDER -- il ne fait que constater un PID mort et relancer.
4. Personne ne TRANSFORME un probleme de routine en MESSAGE : une routine morte
   est un rouge de suite (maillon 7) et une ligne de vie etat, jamais un message
   niveau important/urgent dans l inbox. Les 4 appelants de signaler le font
   PENDANT LEUR PASSE (routine vivante) : un plantage a l ALLUMAGE -- le cas
   le plus grave -- ne depose RIEN, alors que sa cause est deja ecrite dans
   journal-lancement.log.

## 3. LA PROPOSITION

### 3.1 Le PLANNING (les delais + la rotation d allumage)

Un fichier UNIQUE declare par la Matrice, matrice/routines/planning/planning.json :

- une entree par routine : nom, cadence (voir D1 : reference ou valeur),
  DECALAGE INITIAL (c est lui la rotation : au demarrage, les routines ne
  s allument pas toutes en meme temps), MODE (passe | boucle), PRIORITE.
- principe ZERO COPIE (M-076 / L-029) : si la cadence reste chez la routine
  (voix unique), le planning ne declare que le decalage, le mode et le domicile
  de la cadence -- exactement le faisceau CADENCE_PAR_NOM qui existe deja.
- le planning dit aussi OU RELIRE l echeance : l anneau de passes publie dans
  l etat court de chaque routine (dernieres_passes) -- on COMPARE, on n ATTEND
  jamais (attente-ne-prouve-rien).

### 3.2 Le SERVICE (allume, recoit, transforme)

Evolution du serveur de vie, MEME domicile, MEME porte (lancer.py vie ...) :

1. TOUR DE SERVICE (sa cadence declaree, 60 s) : pour chaque entree du
   planning, comparer l echeance (derniere passe publiee) a la cadence -> si
   DUE, allumer la routine en mode PASSE (sa commande one-shot, table
   COMMANDE_PAR_NOM qui s etend d une cle mode -> commande de passe).
2. ROTATION D ALLUMAGE : au tour de service, allumer AU PLUS UNE routine due
   par tour (ordre : priorite puis decalage) -- jamais le pic des 7 en meme
   temps, et jamais deux allumages de la meme routine.
3. RECEPTION : code retour du fils (lancer_enfant plafonne a
   DELAI_SOUS_PROCESSUS_SECONDES = 120 s, data/commun/lancement.py) OU, en
   detache, lecture de l etat publie + journal de lancement au tour suivant
   (decision D2).
4. TRANSFORMATION -- un ecart devient un MESSAGE par la PORTE signaler
   (jamais une ecriture directe), niveau DECLARE :
   | Fait mesure | Niveau |
   |---|---|
   | plantage a l allumage (trace de journal-lancement.log) | critique |
   | passe non publiee depuis plus de N cadences (routine due qui ne repond pas) | haute |
   | code retour non nul (passe faite mais en echec) | haute |
   | rotation refusee / ecart annonce par la routine | moyenne |
5. GARDES du service : un seul allumage par routine a la fois (etat en-cours
   avec plafond, refuse en le nommant), tout depot est trace, un refus se DIT
   (jamais de degradation silencieuse, L-055).

### 3.3 Duree de vie resultante

- residents : 1 (le service) au lieu de 8 ; une routine N EXISTE QUE PENDANT
  SA PASSE : elle sort, zero fantome, zero double lancement possible.
- les modes boucle conserves (si decide) restent supervises comme aujourd hui :
  le service sait gerer les DEUX modes (mode mixte, decision D2).

## 4. IMPACTS (a peser avant de toucher quoi que ce soit)

| Cible | Aujourd hui | Apres | Risque si on ne l adapte pas |
|---|---|---|---|
| lanceur-non-regression-flux maillon 7 | juge PID vivant + fin de passe fraiche | critere = derniere passe PUBLIEE vs cadence declaree (meme tolerance 3 cadences / plancher 120 s), PID garde pour le mode boucle | ROUGE PERMANENT : une routine en mode passe n a aucun PID, le maillon crierait a tort |
| vie etat | ACTIVE/ARRET par PID | etat par planning : eteinte (prochaine ech t+X) / en-cours / boucle ACTIVE | faux verdict : La Matrice vit devient faux dans les deux sens |
| verifier-sans-attendre | controle la fabrique des boucles (aucun sommeil en bloc) | doit juger le SERVICE (son tour de service est aussi coupe) | un controle qui juge l ancien monde passe au vert sur du neuf |
| verifier-cadence | ecart MEDIAN sur l anneau | compatible : l anneau avance a chaque passe (declare / publie / mesure reste vrai) | aucun (a verifier en vol) |
| double regime PID (MO-458) | serveur publie, routeur ecrit le sien | a TRANCHER ICI : le service est le SEUL a publier, ou chaque routine publie | deux verites sur QUI est vivant (mesure MO-458) |
| routeur-maintenance | boucle 30 s permanente | mis au planning : sa fraicheur = son echeance | les alertes mettent plus longtemps a arriver chez Optimus |
| moule templates/routine | genere boucle + PID + arret | le squelette doit generer le MODE PASSE par defaut | toute routine neuve reinstallerait l ancien monde |
| docs | routines-readme, DESCRIPTION des 7, manuel-outils, DESCRIPTION vie | a reecrire avec le nouveau contrat | deux doctrines qui se contredisent |
| cockpit /sante + garde-flux2 | lisent vie etat et les pid | doivent lire le planning + les etats de passe | voyant rouge permanent ou faux vert |

## 5. PREUVES ATTENDUES (checklist de la mission, nominal + negatif)

NOMINAL
1. une routine DUE est allumee UNE seule fois, publie sa passe dans son etat,
   puis SORT (zero processus residant au-dela de la passe) ;
2. le service recoit le resultat et le publie (bien passee / passee en echec) ;
3. un retard de N cadences depose un message niveau haute dans l inbox -- on
   le LIT a la porte (signaler), pas dans un rouge de suite ;
4. la rotation se voit : au demarrage, les 7 routines ne s allument pas en
   meme temps (decalage applique).

NEGATIF
5. une routine NON DUE n est PAS allumee ;
6. un plantage a l allumage depose un message CRITIQUE qui porte la CAUSE lue
   dans journal-lancement.log ;
7. un second allumage pendant qu une passe est en cours est REFUSE en le
   nommant (jamais deux passe de la meme routine) ;
8. un planning illisible est REFUSE en nommant le fichier -- le service ne
   devine pas, il dit (L-055).

CONTRE-TEMOIN
9. une routine en mode boucle (mode conserve) n est PAS accusee par le nouveau
   critere du maillon 7.

AVANT DE CLORE : suite MISE A JOUR d abord (les maillons concernes sont nommes
au section 4 : maillon 7, vie etat, verifier-sans-attendre, moule routine),
puis py_compile global, puis non-regression. Un round qui ajoute une garde sans
l inscrire fait une garde que PERSONNE ne joue.

## 6. DECISIONS DU CREATEUR (obligatoires -- posture REVISEUR / proto-6)

D1 -- OU VIT LE PLANNING
   (a) le planning ne DECLARE QUE les decalages/modes/priorites et dit OU LIRE
       la cadence (voix unique conservee chez la routine) -- RECOMMANDE ;
   (b) le planning DEVIENT la source des cadences, les routines le lisent.

D2 -- MODE PAR DEFAUT D ALLUMAGE
   (a) mode PASSE pour les 7 routines (le service est le seul resident) ;
   (b) HYBRIDE : passe pour les cadences longues (>= 900 s : verifier-liens,
       vigie-portes, vigie-profil), boucle pour les rapides (routeur 30 s,
       suivi-sync 60 s, veille/espion 300 s) ;
   (c) tout en boucle : le planning ne ferait qu ORDONNER les allumages
       (gain mesure nul : 8 processus residents conserves).

D3 -- DOUBLE REGIME PID (MO-458, a tranche d un coup)
   (a) le service est le SEUL a publier les pid files (le routeur cesse d ecrire
       le sien) ;
   (b) chaque routine publie le sien, le service ne fait plus que REPARER.

D4 -- TRANSFORMATION DES PROBLEMES
   (a) les niveaux du tableau 3.2 vous conviennent tels quels ;
   (b) ajouter une MONTEE DE DEFCON par la porte machine-defcon monter pour le
       niveau critique (les declencheurs existent, l audit dit que la montee
       n a jamais ete observee en production) ;
   (c) autre regle a ecrire.

D5 -- PERIMETRE DE LA CONSTRUCTION
   (a) construire TOUT d un trait : planning + service + gardes + docs ;
   (b) PILOTABORD sur UNE routine (ex. vigie-profil, cadence 900 s, peu
       dangereuse) puis generalisation apres preuves.

## 7. CE QUE JE NE TOUCHE PAS SANS VOUS

- la voix unique des cadences (chaque routine declare SON temps) ;
- l arret COOPERATIF (drapeau, zero processus tue) et le motif de lancement
  invisible partage (data/commun/lancement.py) ;
- la porte UNIQUE signaler pour tout depot d alerte ;
- l anneau de passes / verifier-cadence (declare, publier, mesurer) ;
- python seul, ASCII strict, ecriture atomique (deja dans la checklist) ;
- la separation des flux (Flux 1 routines Matrice / Flux 2 Optimus).

## 8. ETAT DE LA MISSION

Relecture terminee, proposition ecrite, AUCUNE regle modifiee. La suite
(construction) demarre des que les decisions D1 a D5 sont rendues.
