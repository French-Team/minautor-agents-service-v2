---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# AUDIT -- CYCLE DE VIE DES FICHIERS DE TRAVAIL DE LA ZONE JETABLE

> MO-371 (theme AUDITEUR, Flux 2). LECTURE SEULE : aucune reparation.
> Chaque fait est MESURE (disque, BDD, journal) ; la commande qui le rejoue est citee.
> Zone concernee : _operateur/optimus-prime/tmp-optimus (et sa jumelle workspace/tmp-cameleon).

## 0. CE QUE LA MISSION DEMANDE

(a) QUI cree les fichiers de travail de la zone jetable, et AVEC QUOI ;
(b) COMBIEN de residus en restent apres une cloture ;
(c) ce qui EXISTE DEJA : les fonctions de data/commun/zone_tmp.py et
    data/commun/cobayes_jetables.py, et leurs APPELANTS reels.

## 1. (a) QUI CREE, ET AVEC QUOI

FAIT 1.1 -- Le PILOTE ne cree AUCUN fichier de travail. Il n'a que deux actes, sur
des objets differents : preparer la ZONE (dossier + README) et la VIDER a la cloture.

- PREPARER : UN SEUL appelant dans tout le depot --
  matrice/pilote/commun.py:313 (preparer_zone_temporaire, flux CAMELEON).
  Le pilote d'OPTIMUS n'appelle JAMAIS preparer : 0 appelant mesure dans
  _operateur/optimus-prime/pilote. La zone d'Optimus existe donc de FAIT
  (README.md, mtime 2026-09-15 21:04), nee hors du code.
- VIDER : deux appelants, un par flux --
  _operateur/optimus-prime/pilote/commun.py:2564 et matrice/pilote/commun.py:355.

FAIT 1.2 -- Les FICHIERS DE TRAVAIL sont crees par l'AGENT, a la main, par la PORTE
ECRIRE (verbes ecrire et editer). Aucun outil ne les cree pour lui (voir 3.3).
Signature mesuree : les residus presents sont des paires -- paires/*.ancien,
paires/*.nouveau -- et des *.nouveau, exactement la FORME que le verbe editer impose
quand il n'a pas de chemin bit-exact.

FAIT 1.3 -- AVEC QUOI. La porte ECRIRE a un chemin BIT-EXACT pour le CONTENU
(--contenu-base64) mais AUCUN pour l'EDITION :
  ecrire : --contenu | --contenu-fichier | --contenu-base64
  editer : --ancien | --nouveau | --ancien-fichier | --nouveau-fichier
Mesure : python3 cerveau-projet/matrix/matrice/data/outils/ecrire/main.py --help
(section GARANTIES / TRANSPORT).
Consequence : des qu'un texte porte un accent, un accent grave ou un guillemet, la
coquille le mange ; l'agent passe donc par des FICHIERS .ancien / .nouveau qui
RESTENT dans la zone. C'est la premisse de MO-376 (en-attente), CONFIRMEE ici.

FAIT 1.4 -- Origine de la zone pleine AUJOURD'HUI (mesure) : aucun round pilote n'a
tourne entre le report de MO-371 et cette session.
  - suivi-optimus.jsonl : AUCUN evenement apres 2026-09-23 08:32:33 (report MO-371) ;
  - cycle-historique : une seule injection demarrage aujourd'hui avant celle-ci
    (07:12:09) ; la suivante est 20:38:10 ;
  - les residus portent des mtime 2026-09-23 19:40 a 19:51, et le depot a 140
    fichiers touches apres 18:00 (dont des .bak poses par la porte ECRIRE).
Un travail NON pilote a donc rempli la zone : sans cloture, pas de purge.

## 2. (b) COMBIEN DE RESIDUS RESTENT APRES UNE CLOTURE

FAIT 2.1 -- APRES une cloture ATTEINTE, la purge vide la zone (le README seul
demeure). Mesure : 8 purges tracees aujourd'hui --
  MO-363:24, MO-364:15, MO-365:6, MO-366:19, MO-367:7, MO-368:1, MO-394:17, MO-369:2.
Commande : python3 cerveau-projet/matrix/lancer.py suivi-optimus lire --action purge --n 8

FAIT 2.2 -- APRES une cloture NON ATTEINTE (report / interruption), les residus
PERSISTENT. Compte mesure CE JOUR dans la zone d'Optimus :
  20 FICHIERS + 1 DOSSIER = 21 elements (README excepte).
Liste :
  constants-routeur.py.nouveau
  constants-selecteur.py.nouveau
  extraire-constants-routeur.py
  routeur.py.nouveau
  paires/routeur-description.ancien
  paires/routeur-description.nouveau
  paires/vc-routeur.ancien
  paires/vc-routeur.nouveau
  paires/vhr-chargeur.ancien
  paires/vhr-chargeur.nouveau
  paires/vhr-fabrique.ancien
  paires/vhr-fabrique.nouveau
  paires/vhr-refs.ancien
  paires/vhr-refs.nouveau
  paires/vie-cadence.ancien
  paires/vie-cadence.nouveau
  paires/vr-commentaire.ancien
  paires/vr-commentaire.nouveau
  paires/vr-table.ancien
  paires/vr-table.nouveau
Commande : parcours os.walk de _operateur/optimus-prime/tmp-optimus, README exclu.

FAIT 2.3 -- La mesure du 2026-09-20 (2 fichiers) est REPRODUITE, avec sa cause.
MO-394 est close a 08:22:45 et sa purge (08:23:02) retire 17 elements ; la cloture
SUIVANTE, MO-369 (08:30:05), en retire ENCORE 2 -- mo394-h-new.txt et
mo394-h-old.txt. Deux fichiers nes APRES la purge echappent donc a la purge de LEUR
mission et ne sont soldes que par la purge d'une AUTRE. Classe : un fichier cree
apres l'instant de purge survit a sa propre cloture.

## 3. (c) LES FONCTIONS EXISTANTES ET LEURS APPELANTS REELS

### 3.1 data/commun/zone_tmp.py

| element | role | appelants REELS (mesures) |
|---|---|---|
| contenu | liste ce qu'une zone doit vider | INTERNE : vider. 0 appelant externe. |
| vider | vide la zone, rend (supprimes, echecs) | _operateur/optimus-prime/pilote/commun.py:2564 ; matrice/pilote/commun.py:355 |
| preparer | cree la zone + son README | matrice/pilote/commun.py:313 (CAMELEON). 0 appelant cote Optimus. |
| chemin_zone_optimus | chemin ABSOLU de la zone d'Optimus | verifier-source-item.py:152 ; verifier-profil-injection.py:114 ; dry-run.py:31 ; fragment.py:81 ; data/outils/domicilier/constants.py:20 ; _operateur/optimus-prime/pilote/constants.py:44 |
| chemin_zone_cameleon | idem cote cameleon | matrice/pilote/constants.py:72 ; garde-tmp.py:56 |
| est_dans_zone_cameleon | perimetre : une exemption NOMMEE | garde-perimetre-write.py:33 |
| NOM_ZONE_* / DOMICILE_ZONE_* / PREFIXE_ZONE / CONTENU_README_ZONE | les valeurs DECLAREES (M-076) | matrice/pilote/constants.py:72 ; _operateur/optimus-prime/pilote/constants.py:44 et 233 ; veille-flux/constants.py:30 ; garde-tmp.py:56 ; controle-attribution.py:203 |

### 3.2 data/commun/cobayes_jetables.py

| element | role | appelants REELS (mesures) |
|---|---|---|
| fixtures | ouvre un dossier de fixtures JETABLES (retrait garanti) | verifier-rotation-journal.py:522 ; verifier-marbre.py:241 ; verifier-contrat-fondamental.py:935 et 1104 |
| copier_sous | copie sous un nom CHOISI (miroirs de meme nom) | verifier-contrat-fondamental.py:891, 894, 1106 |
| litteraux | declarations LITTERALES de module (lecture AST) | verifier-contrat-fondamental.py:900, 1114, 1157, 1320 |
| litteraux_illisibles | celles qu'on ne peut PAS comparer | verifier-contrat-fondamental.py:1116, 1159 |
| muter_litteral | mute (valeur) ou retire (absent) une declaration d'une COPIE | verifier-contrat-fondamental.py:897, 1110 |
| retirer | retire un dossier jetable, rend (retires, echecs) | INTERNE : fixtures. 0 appelant externe. |
| copier | pose des copies de fichiers reels | 0 appelant MESURE. |
| muter_valeur | la meme valeur, mutee | INTERNE : muter_litteral. |

Les trois gardes chargent la fabrique par CHEMIN (importlib), jamais par nom : les
outils de la Matrice portent des tirets et ne sont pas importables par nom.

### 3.3 VERDICT SUR LA PREMISSE

La premisse de la mission -- AUCUNE PORTE ne les expose, donc RIEN ne les emploie --
est PARTIELLEMENT FAUSSE, et la nuance est le VRAI defaut :

- les MOTEURS SONT employes : zone_tmp par les DEUX pilotes (vider) et par la porte
  domicilier (un chemin) ; cobayes_jetables par TROIS gardes ;
- ce qui MANQUE est une PORTE POUR L'AGENT : aucun outil de data/outils (38 portes)
  ni de combos/outils n'expose liste / cree / vide d'une zone par NOM, ni le JOURNAL
  de ce qui a ete cree puis purge. C'est exactement l'objet de MO-374 (en-attente).

## 4. CE QUE CET AUDIT NE TRANCHE PAS

- La creation de la zone d'Optimus (0 appelant de preparer) : elle existe de fait.
  Faut-il la faire naitre par son pilote (R-005) ou declarer la zone permanente ?
  Decision hors perimetre d'un audit.
- Le sort des 21 residus presents : ils appartiennent a un travail non pilote ; les
  vider est une REPARATION (MO-374), pas une mesure.
- L'etendue exacte du travail de 18:00-19:51 (140 fichiers, dont des .bak de la
  porte ECRIRE) : il n'a laisse AUCUNE trace au marbre ni a bdd-modifications ; son
  perimetre exact n'est pas reconstituable par la seule lecture des traces.

## 5. MESURES DE L'AUDIT LUI-MEME

Le rapport a ete ecrit PAR LA PORTE ECRIRE, en quatre tranches : une premiere en
--mode creer, trois en --mode ajouter, chacune en --contenu-base64 (chemin bit-exact
du CONTENU). La premiere tentative, avec un base64 unique de la taille du document,
a ete REFUSEE par la coquille (option --fichier tronquee) : la limite de longueur de
ligne est une raison DE PLUS de decouper, et elle est DITE.
