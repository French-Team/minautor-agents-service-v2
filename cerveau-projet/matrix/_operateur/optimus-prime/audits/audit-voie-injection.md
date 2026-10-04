---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# AUDIT -- LA VOIE D INJECTION : QUI LIT L INJECTION DU PILOTE, ET QUAND L AGENT LA VOIT

> Consigne (mission MO-365, EO-131) : mesurer la voie d injection du champ recherche et
> de la carte des modes d emploi. Le pilote ecrit une injection (demarrage +
> avant-mission) : QUI la lit, et a quel moment l agent qui execute une mission la
> voit-il ? Si le fichier d injection (outbox.jsonl) n est lu par personne, le champ est
> DECORATIF. Preuve attendue : la chaine des lecteurs, nommee, ou l aveu mesure que rien
> ne lit.
>
> AUDIT = lecture seule : aucun fichier de service n a ete modifie, aucun ecart n a ete
> repare ici (consigne de l AUDITEUR). Chaque ligne porte son domicile (fichier:ligne)
> ou sa mesure.

## 1. LA CHAINE DES LECTEURS, NOMMEE (le fait mesure)

ECRITURE -- injection/fonctions.py:389 preparer_injection fabrique l injection et la
DEPOSE. Deux branches, deux dicts :
  - injection SIMPLE : injection/fonctions.py:484-499 (9 champs + poids_tokens), depot
    ligne 499 ;
  - branche LOT : injection/fonctions.py:610-624, depot ligne 624.
  Le flux cameleon depose de la meme facon : matrice/pilote/injection/fonctions.py:130
  et :190.

DOMICILE -- BOITE_PILOTE_OUT (_operateur/optimus-prime/pilote/constants.py), soit
_operateur/maintenance/pilote/outbox.jsonl. MESURE : 3 187 076 octets, 215 lignes, toutes
lisibles en JSON -- 79 injection, 80 debut-mission, 56 fin-mission.

LECTEUR UNIQUE DU CONTENU -- pilote/commun.py:1110 derniere_injection(mission_id) : relit
le fichier et prend en remontant la DERNIERE ligne dont la mission vaut l identifiant ET
dont l objectif est non vide. Grep exhaustif : derniere_injection n existe QUE dans le
pilote Optimus (commun.py:1110, fin/fonctions.py:17 et :70).

PORTEUR JUSQU A L AGENT -- pilote/fin/fonctions.py:52 remettre_les_ordres : c est le SEUL
endroit qui IMPRIME le contenu d une injection. Appele par fin/fonctions.py:101
enchainer_et_prendre, donc AU MOMENT DE LA CLOTURE, quand la boucle sert le round suivant
(et par le verbe injecter, ORDRE 2, au demarrage). La veille
(preparer_injection -> annoncer_debut, commun.py:496) n imprime RIEN de l injection :
identifiant, theme, position, et rien d autre.

CONCLUSION DE CHAINE : le fichier n est pas lu par personne -- REPONSE MESUREE -- il est
lu par la PORTE, quand elle remet les ordres. Le contenu atteint l agent par la CONSOLE,
jamais par la boite.

## 2. MESURE -- CE QUI EST DEPOSE CONTRE CE QUI EST IMPRIME

CHAMPS_PESES (injection/fonctions.py:101) declare 9 champs que l injection doit porter :
objectif, checklist, lecons_utiles, themes_utiles, role, recherche, rappel, modes_emploi,
profil. remettre_les_ordres (fin/fonctions.py:74-89) en IMPRIME 4.

| champ depose | MO-365 | imprime a l agent |
|---|---|---|
| objectif | 524 o | oui |
| checklist | 459 o | oui |
| rappel | 340 o | oui |
| theme | (titre) | oui |
| recherche | 568 o | NON |
| modes_emploi | 2 871 o | NON |
| role | 1 043 o | NON |
| profil | 506 o | NON |
| themes_utiles | 9 042 o | NON |
| lecons_utiles | 23 964 o | NON |

Sur les 30 dernieres injections du fichier : recherche 30/30 non vide, modes_emploi 30/30
non vide. Les deux champs de cette mission sont donc CORRECTEMENT FABRIQUES et DEPOSES --
et AUCUN des deux n atteint l agent.

Pour les lire, il faudrait ouvrir un fichier de 3,1 Mo et y retrouver la derniere ligne
de sa mission : rien dans le demarrage ne le demande (grep -n outbox
demarrer-optimus-prime.md = 0 occurrence) et rien ne le facilite (la boite est AJOUT SEUL,
seul un SEUIL DE TAILLE est surveille : commun.py:2452, plafond 5 242 880 o).

VERDICT : le champ n est pas DECORATIF dans le fichier -- il est decoratif DANS LE ROUND.
La fabrication, la pesee (poids_injection) et la lecture existent ; c est la REMISE a
l agent qui s arrete a 4 champs sur 9.

## 3. ECARTS MESURES (deposes, jamais repares ici)

EC1 -- MOYENNE -- 7 champs sur 9 n ont aucun porteur : fin/fonctions.py:74-89 contre
injection/fonctions.py:101. Consequence directe : EO-131 (le champ recherche, < la
question a poser au moment utile >) et la carte des modes d emploi n atteignent jamais
l agent qui execute. Ce sont deux champs qui ont coute des missions entieres (MO-141 pour
la carte) et que rien ne remet au moment dit.

EC2 -- BASSE, LATENTE -- la branche LOT (injection/fonctions.py:610-618) ne pose PAS
modes_emploi, alors qu il est declare dans CHAMPS_PESES (ligne 101) : la pesee se tairait
sur 2 871 o (poids_injection ne pese que ce qui existe, fonctions.py:116). MESURE : 0/30
injections sur le chemin LOT (la chaine passe par l injection simple) -- l ecart est
LATENT, pas actif.

EC3 -- BASSE -- aucun lecteur des lignes ANCIENNES : la boite est ajout seul, la seule
surveillance est un seuil de taille (commun.py:2452), et derniere_injection ne regarde
qu une seule mission. Une boite de 3,1 Mo dont 4 champs sont lus est un poids porte sans
usage.

EC4 -- MOYENNE (FLUX 1) -- le pilote cameleon depose ses injections
(matrice/pilote/injection/fonctions.py:130 et :190) et AUCUN lecteur de code ne reprend
ce contenu : grep -rn derniere_injection / remettre_les_ordres = 0 occurrence hors du
pilote Optimus. Les seules autres mentions de cette boite sont des mesurages de taille
(cockpit) et de la documentation (matrice/pilote/DESCRIPTION.md:40,
matrice/intercom/indices.md:8). Pour le Flux 1, la boite est un depot sans porteur.

## 4. TESTS (nominal + negatif), lectures seules

NOMINAL -- derniere_injection(MO-365) rend l entree : 15 cles, 9 champs peses TOUS non
vides, poids declare 9 831 tokens. La porte LIT, et elle lit la BONNE ligne.

NEGATIF -- derniere_injection(MO-999) = None, (chaine vide) = None, (None) = None, sans
exception. 136 lignes du fichier portent une mission SANS objectif (types debut-mission
et fin-mission) : elles sont IGNOREES par la porte, comme son contrat le dit -- verifie
sur le fichier REEL, pas sur une fixture.

SYNTAXE -- 523 fichiers .py analyses (ast), 0 erreur. Aucun fichier de service ecrit par
cet audit : le rapport et son script de mesure sont les SEULES ecritures, et le script
vit en zone jetable (purgee a la cloture, trace au marbre).

## 5. LIMITES DITES

- EC2 est une LECTURE DE CODE : la branche LOT n a pas ete empruntee une seule fois dans
  les 30 dernieres injections, donc l ecart n a pas ete vu en vol.
- Cet audit ne dit PAS quelle forme doit prendre le remede (tout imprimer, resumer,
  confier ces champs a la fiche ou a un mode d emploi) : c est une DECISION du createur,
  hors de mon perimetre d AUDITEUR. Il dit ce qui est mesure.
- La valeur des 7 champs non imprimes n a pas ete jugee : leur POIDS est mesure
  (lecons_utiles 23 964 o pour MO-365), leur utilite ne se mesure pas ainsi.
