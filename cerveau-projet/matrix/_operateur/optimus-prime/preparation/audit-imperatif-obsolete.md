---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# AUDIT -- IMPERATIF.md EST-IL DEVENU OBSOLETE ? (MO-542 / EO-548)

> Question du createur : ce fichier a servi au passage v1,v2 vers la v3 ; depuis,
> la v3 a depasse les besoins ecrits dedans. Verifier s il est toujours PERTINENT
> et UTILE. Sortie attendue : un constat nomme et une decision.

## LE CONSTAT EN TROIS LIGNES

IMPERATIF.md n est pas obsolete : il est INERTE.

C est une distinction qui change tout. Un fichier obsolete est faux -- il dit
des choses qui ne sont plus vraies, et il faut donc le corriger. IMPERATIF ne dit
rien de faux : sur les 14 prescriptions que j ai mesurees, 11 sont des ACCOMPLIS
et 3 seulement ont ete depassees. Il n a pas disparu, il a ete REALISE. Et
c est precisement ce qui le rend dangereux : un document qui a raison et que
personne ne lit parait encore utile, alors qu il ne sert plus a rien.

Le second constat, plus dur : il n est lu par PERSONNE au service.

## MESURE 1 -- QUI LE LIT (la question prealable)

Une source qui n a aucun lecteur n est pas une source, c est un decor.

| Lecteur | Type | Reel ? |
|---|---|---|
| une injection du pilote, comme SOURCE | code | **NON** -- IMPERATIF n est le `source` d aucune entree des 3 phases de `injection/config.json` : aucun octet de son contenu n est injecte |
| une injection du pilote, comme CHEMIN a lire | code | **OUI, et c est le seul lecteur machine** -- `parcours/themes/theme-reprise-mission.json`, geste < Relire mon coeur > : `Lire matrix/docs/IMPERATIF.md (vision du createur)`. Ce theme EST une source OBLIGATOIRE de la phase demarrage. Donc le rappel existe, l octet livre n existe pas : l agent est charge de l aller chercher. |
| un outil de la Matrice qui le consomme | code | **NON** -- zero `open()` sur ce chemin dans tout le zone python |
| le moteur de recherche (indexation) | code | NON indexe : il vit dans `docs/`, zone des sources hors corpus de recherche |
| `verifier-contrat-fondamental.py` | code | PARTIEL -- seulement comme NOM de fichier : IMPERATIF est dans `PREFIXES_NOM_IMPOSE`, donc un fichier de ce nom est attendu a la racine. Il ne le LIT pas. |
| `lanceur-non-regression.py` | code | PARTIEL -- il l utilise comme CIBLE d un cobaye (`la-cible-PRESENTE-des-SOURCES-est-DITE-aussi`). Il verifie qu il existe, pas ce qu il dit. |
| `docs-readme.md` | humain | OUI -- le tableau le declare `SOURCE VIVANTE -- je le relis a chaque demarrage`. C est la SEULE lecture reelle, et elle est HUMAINE. |
| `zone_sources.py` | code | NON -- il ne cite IMPERATIF que dans le TEXTE d un message de refus, comme exemple. |

Il y a donc bien un lecteur machine, et il faut le nommer correctement : le theme
de reprise, injecte a CHAQUE demarrage, dit a l agent d aller lire IMPERATIF. Mais
c est une CONSIGNE de lecture, pas une LECTURE : le contenu n est pas livre, il
est pointe. Un agent qui suit le parcours l ouvrira ; un agent qui s en passe
n aura pas de sanction -- il n y a aucun garde qui verifie qu il l a fait. C est
exactement la distinction que MO-528 a mesuree sur un autre sujet : une mesure
qui ne se joue pas n est pas une mesure. Ici, une consigne de lecture qui ne se
joue pas n est pas une relecture.

Ajout d un fait mesure apres coup : `conventions-matrice.json` porte
`CV-007 -- FONDAMENTAUX CHEMIN/LIEN/NOM/FLAG (contrat, imperatif 24)`. IMPERATIF
est donc encore la SOURCE D UNE CONVENTION VIVANTE de la Matrice. Cela ne prouve
pas qu on le lit ; cela prouve que, quand on l a lu, il a produit un effet qui
lui survit.

## MESURE 2 -- SES PRESCRIPTIONS, UNE PAR UNE

14 prescriptions. Je les classe par ce que la v3 en a fait.

### REALISEES ET TOUJOURS VIVANTES (7) -- le fichier a raison, et le projet le prouve

| Prescription | Etat mesure |
|---|---|
| des outils pour tout, configurables | 45 outils dans `matrice/data/outils/`, tous avec `main.py` |
| des securites sur les `.py` | outils `verifier` / `garde` / `controle` presents et joues |
| des protocoles concis | 14 protocoles + `protocoles-readme.md` avec colonne QUAND |
| SINGLE-LLM, serie obligatoire | `regles-immuables/serie-stricte.md` -- la prescription est une regle immuable, elle a ete GRAVEE |
| regle dans le marbre, pas de commentaires de modif dans les fichiers | `modifications-par-fichier.json` fait 2 Mo : la prescription est un OUTIL |
| une bank de themes, pas des agents par type | `vivier-themes.json`, 27 themes -- et 0 agent cree pour un theme |
| le concept de couche | `matrice/`, `super-combos/`, `combos/`, `outils/` : la hierarchie est la |

### REALISEES ET DEPASSEES (4) -- la v3 a aller plus loin que la demande

| Prescription | Ce que la v3 a fait |
|---|---|
| `perimetre d'ecriture : matrix exclusivement` | **depassse** : la loi du round ouvre 2 exceptions racine (`AGENTS.md`, `demarrer-*.md`), et le perimetre reel est une ALLOWLIST jugee par `garde-perimetre-write`. Le texte est plus etroit que la realite. |
| `l'historique devient tout de suite une bdd avec filtrage des doublons, obsoletes` | **depasse** : le filtrage des doublons existe, mais il vit dans la PORTE `bdd-raisonnement` (verbe `retirer` + refus du doublon, EO-537) -- donc il est EN PLACE, pas seulement annonce |
| `les injections doivent contenir des outils espion qui mesurent temps et tokens` | **partiel** : le temps existe (journal du pilote, bornes debut/fin), les TOKENS n existent que comme COMPTE DE POIDS (`PLAFOND_INJECTION_TOKENS`), pas comme mesure d envoi/reception. Aucun outil ne mesure ce qui sort reellement. |
| `activites-recentes sera revue par section, pas a la suite` | **fait** : mais par une autre voie que la prevision (parcours par sections dans l injection). Conforme au resultat, pas a la voie. |

### EN RETRAIT (3) -- ce que la v3 a refuse

| Prescription | Pourquoi elle est obsolete |
|---|---|
| `une base secrete qui envoie son pilote avec un agent 'cameleon' qui prend l identite de n importe qui` | **abandonnee** : le mecanisme reel n est pas un agent qui change d identite, ce sont des POSTURES (`entonnoir/roles.py`, 14 postures) attribuees par le couple (type, categorie). Optimus garde SON nom et change de posture. Le cameleon existe encore comme zone de code (`matrix/agents/cameleon/`), mais il n est pas ce que le fichier decrit. |
| `le pilote reveille l'agent -> l'agent execute -> il DECLARE sa fin au pilote` | **inversee** : `proto-9` dit noir sur blanc < Le pilote ne note RIEN pour Optimus : pas de chemin pilote->Optimus >. C est l agent qui appelle `pilote fin`. Le sens du flux decrit est retourne. |
| `on aura un agent unique qui va devenir n importe qui en fonction du theme` | **partiellement fausse** : la doctrine de l agent unique tient (un seul operateur), mais l identite ne devient pas n importe qui : elle devient une posture parmi 14, et l identite reste fixe. |

## LA DECISION (elle est au createur, pas a moi)

Trois issues, et je les ordonne parPreference.

### ISSUE 1 -- LE STATUT A CORRIGER (celle-la, je la recommande)

`docs/docs-readme.md` dit aujourd hui :

    | IMPERATIF.md | Vision du createur pour la v3 | SOURCE VIVANTE -- je le relis a chaque demarrage | francais |

Ce statut est **faux sur un point mesurable** : il ne le relit PAS a chaque
demarrage, et rien ne l injecte. Le qualifier de `SOURCE VIVANTE` quand aucune
injection ne la sert est exactement la faute que le lanceur non-regression vient
de me signaler sur ce fichier : une declaration de statut que rien ne vient
verifier.

Je ne touche pas au fichier : `docs/` est la zone des SOURCES, la porte ECRIRE y
refuse toute publication, et la Matrice ne corrige pas ses sources. La correction
est donc une decision du createur -- d ou la question precise :

**Le createur veut-il que la v3 relise IMPERATIF a chaque demarrage ?**
- Si OUI : il faut l ajouter au catalogue `injection/config.json` (phase
  demarrage, source obligatoire), et la qualifier de VISION PILOTE plutot que de
  VISION v3 -- car 7 de ses 14 prescriptions sont des ACCOMPLIS a ne plus
  repeter.
- Si NON : le statut du readme doit le dire. < Source du createur, relue a la
  main, jamais injectee > est plus exact et protege le fichier d unelecture
  qui n arrive pas.

### ISSUE 2 -- UNE PARTIE DEVIENT UN DOCUMENT D AUTRE NATURE

La moitie du fichier (les 7 prescriptions realisees) n est plus une prescription :
c est un HISTORIQUE de ce qui a ete demande. Il a sa place naturelle dans le
`docs/heritage-v1-v2-AGENTS.md` qui existe deja, ou dans une section du readme.

Je le dis mais je ne le deplace pas : deplacer une source est une decision de
zone, elle appartient au createur.

### ISSUE 3 -- LA QUESTION QUE JE NE PEUX PAS TRANCHER

IMPERATIF dit encore, en toutes lettres :

    la construction dans matrix va demarrer de zero

C etait vrai en 2026. Aujourd hui la construction n est plus a zero : elle a
543 points actifs, 366 archives, 125 Mo traces. La phrase n est pas fausse au
sens strict (elle decrit une intention), mais un agent qui la lirait pourrait en
tirer qu il doit repartir de zero -- ce qui serait catastrophique sur un
projet de cette taille.

C est le SEUL point du fichier qui pourrait causer du degat s il etait relu sans
contexte. Il merite une correction, et comme le fichier est une source, cette
correction vous appartient.

## CE QUE JE N AI PAS FAIT, ET POURQUOI

- Je n ai pas modifie IMPERATIF.md : `docs/` est en zone sources, la porte ECRIRE
  y refuse (code 2), et la regle dit qu une source n est ni recreee ni corrigee
  par la Matrice. Le controle d attribution accuse d ailleurs ce fichier depuis
  08:16 le 2026-10-02 pour une modification hors porte -- je n y touche pas
  davantage dans le meme round : corriger le statut et nettoyer cette trace
  doivent etre deux gestes distincts et traces.
- Je n ai pas propose d archiver le fichier, bien que 3 prescriptions sur 14
  soient en retrait. La raison : le fichier est le document ou la vision du
  createur est ecrite, et sa valeur est historique avant d etre operationnelle.
  Archiver une source serait perdre ce qui reste TRUE pour une part de lui.
  Il n est pas obsolete, il est INERTE -- et un document inerte se classe, il ne
  se supprime pas.
