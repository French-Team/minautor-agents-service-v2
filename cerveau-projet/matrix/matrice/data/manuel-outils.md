---
identite:
  type: readme
  appartient_a: matrice
  commun: true
  version: 1
  date: 2026-09-23
  liens: matrice/templates/routine/README.md, matrice/data/outils/dupliquer-template/DESCRIPTION.md, matrice/data/outils/ecrire/DESCRIPTION.md, matrice/data/outils/rechercher/DESCRIPTION.md, matrice/data/commun/carte_identite.py, matrice/data/commun/cible.py, _operateur/optimus-prime/super-combos/combos/outils/verifier-cartes-identite.py
---

# MANUEL DES OUTILS -- Matrice et operateur

> Une fiche par outil : commandes, protections, quand l'utiliser.
> MIS A JOUR A CHAQUE NAISSANCE OU MODIFICATION D'OUTIL (convention-indices).
> Pour l'architecture d'un outil : lire son DESCRIPTION.md.

## 0. lancer.py -- lanceur UNIQUE (MO-249)

Toute commande d outil passe par le lanceur : le NOM suffit, l interpreteur et le
chemin sont poses par LUI -- la commande n est plus jamais ecrite a la main.

| Commande | Usage |
|---|---|
| lancer un outil | `python3 cerveau-projet/matrix/lancer.py <outil> <verbe> [arguments...]` |
| lancer en SE declarant | `python3 cerveau-projet/matrix/lancer.py --appelant <cameleon\|operateur> <outil> [arguments...]` |
| lister | `python3 cerveau-projet/matrix/lancer.py --lister` |
| aide | `python3 cerveau-projet/matrix/lancer.py --aide` |
| auto-test du controle de porte | `python3 cerveau-projet/matrix/lancer.py --auto-test` |

**Refus NOMME** : nom inconnu = code 2, avec les noms proches. Le lanceur resout
`matrice/data/outils/<nom>/main.py` et `matrice/routines/<nom>/main.py`.

**PORTE COMMUNE / PORTE PRIVEE (MO-434)** : le lanceur APPLIQUE la cle `commun`
de la carte (`DESCRIPTION.md` a cote de la brique), jusque la une declaration
sans consommateur (mesure du 2026-09-23 : le garde verifiait sa presence, le
moteur pouvait la filtrer, personne ne l appliquait).

- `commun: true` : porte COMMUNE -- ouverte a tous les appelants, en silence ;
- `commun: false` : porte PRIVEE -- l appelant SE DECLARE : `--appelant <identite>`
  AVANT le nom de la brique, ou variable d environnement `MATRICE_APPELANT=<identite>`
  (l option gagne si les deux sont la ; la variable, elle, est HERITEE par les
  enfants). Vocabulaire FERME : `cameleon` (flux 1), `operateur` (flux 2) --
  hors liste = code 2 en nommant le vocabulaire. Un flux ETRANGER est REFUSE
  (code 2) quand la carte porte la cle `flux` ; l ANONYMAT n est PAS refuse --
  18 commandes documentees y passent, dont 9 dans le protocole gele proto-12 --
  mais il est NOMME sur la SORTIE D ERREUR a chaque passage ;
- carte absente : rien a juger, et le lanceur le DIT (`[SANS CARTE]`, sortie
  d erreur) -- l appartenance de la carte est celle du cartographe, pas un
  refus d appelant.

Une identite se DECLARE, elle ne se PROUVE pas (meme utilisateur OS, meme
shell) : c est un GARDE (refus nomme + signalement), pas un verrou. Briques
PRIVEES mesurees dans le perimetre du lanceur (4 sur 125 resolubles) :
`dialoguer` (flux 2), `vigie-portes` (flux 1), `vigie-profil` (flux 1), et
`pilote` (sans cle `flux` : les DEUX flux le conduient -- l operateur le
possede, le cameleon conduit son round, donc le flux n y est pas croise).

**Source UNIQUE de resolution (EO-287)** : la resolution et son refus vivent dans
`matrice/data/commun/resolution_outils.py` -- le lanceur les LIT, et les appelants
INTERNES aussi (`from resolution_outils import chemin_outil`) au lieu de recopier
`data/outils/<nom>/main.py` : un chemin recopie ne se plaint JAMAIS quand l outil
disparait, il plante sans dire pourquoi.

**Garde des commandes (P3)** : le maillon 21 quinquies (`verifier-commandes.py`)
accuse, dans les documents, un python -c, un heredoc, un appel sans interpreteur,
un chemin non ancre et un NOM de brique INCONNU -- commandes des blocs de code ET
commandes inline (EO-287 : 77 lignes nommaient `outils`, qui n est pas une brique).

## 1. bdd-modifications -- `matrice/data/outils/bdd-modifications/`

| Commande | Usage |
|---|---|
| `noter` | `python3 cerveau-projet/matrix/lancer.py bdd-modifications noter --fichier <chemin> --action <cree\|modifie\|corrige\|supprime> --detail "..." --tags "a,b"` |
| `lire` | `python3 cerveau-projet/matrix/lancer.py bdd-modifications lire [--fichier X] [--tag Y]` (filtres combinables, reponse vide = aucun resultat) |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py bdd-modifications verifier` (empreinte reelle vs etalon) |

**Protections** : actions en vocabulaire ferme (cree/modifie/corrige/supprime), ecriture atomique LF, empreinte SHA-256 dans un fichier separe, garde-fou structurel sur `data/`.
**Quand** : APRES chaque modification d'un fichier de la Matrice (anti-surcharge : jamais de commentaire de modification dans le fichier).

## 2. bdd-lecons -- `matrice/data/outils/bdd-lecons/`

| Commande | Usage |
|---|---|
| `ajouter` | `python3 cerveau-projet/matrix/lancer.py bdd-lecons ajouter --lecon "..." --tags "a,b" [--source "..."]` |
| `modifier` | `python3 cerveau-projet/matrix/lancer.py bdd-lecons modifier --id L-XXX --lecon "..." [--source "..."]` (correction, garde l'id) |
| `lire` | `python3 cerveau-projet/matrix/lancer.py bdd-lecons lire [--tag X]` |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py bdd-lecons verifier` |

**Protections** : porte unique des lecons (corrections.md est supprime), tags obligatoires, ecriture atomique LF, empreinte.
**Quand** : fin d'une evolution validee (proto-2), apres chaque lecon reelle ; le pilote consomme ces lecons taguees dans ses injections.

## 2bis. bdd-sessions -- `matrice/data/outils/bdd-sessions/`

| Commande | Usage |
|---|---|
| `ajouter` | `python3 cerveau-projet/matrix/lancer.py bdd-sessions ajouter --session "..." --tags "a,b" [--source "..."]` |
| `lire` | `python3 cerveau-projet/matrix/lancer.py bdd-sessions lire [--tag X]` |
| `resume` | `python3 cerveau-projet/matrix/lancer.py bdd-sessions resume --derniere` (la DERNIERE session, lecture bornee via `data/commun/derniere_session.py` ; GARDE DE RETARD MO-121 : le retard est DIT des qu'une session FERMEE est plus ancienne que des entrees presentes -- une reponse en retard qui se tait passe pour la verite) |
| `etat` | `python3 cerveau-projet/matrix/lancer.py bdd-sessions etat` (l'ETAT SEUL, une ligne : `SESSION : ouverte\|fermee\|aucune` -- format partage declare dans `data/commun/trace_session.py`, MO-121) |
| `retiqueter` | `python3 cerveau-projet/matrix/lancer.py bdd-sessions retiqueter --id S-0XX [--tags "a,b"] [--horodatage "AAAA-MM-JJ HH:MM:SS"] [--motif "..."]` (CORRIGE les tags ET/OU la DATE d'une entree existante, TRACE conservee : `tags_avant`, `horodatage_avant`, `retiquete_le`/`re_date_le`, `motif_retiquetage` ; le texte n'est jamais touche -- MO-122) ; depuis MO-124 le RE-DATAGE refuse une seconde DEJA OCCUPEE (nommee) et un horodatage illisible -- dans les deux cas RIEN n'est ecrit |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py bdd-sessions verifier` |

**Ordre des entrees (MO-125)** : la recence d'une entree se mesure sur `(horodatage, rang d'append)` -- a la MEME SECONDE, l'entree ECRITE APRES est la plus recente (la BDD est en ajout seul). Le departage est fait par le moteur PARTAGE `data/commun/derniere_session.py` pour `etat`, `resume` et le garde de retard ; il remplace l'ancien "la cloture gagne a la seconde" qui pouvait annoncer l'INVERSE de la verite (accident S-052/S-053). Une entree peut en plus etre RE-DATEE par `retiqueter --horodatage` (MO-124).
**Contrat ECRIT/LU (MO-121)** : le vocabulaire et le format vivent a UN domicile, `data/commun/trace_session.py` -- celui qui ECRIT et celui qui LIT importent le meme module au lieu de se recopier. Mesure d'origine : le pilote notait `travail` quand la reprise ne lisait que `session-*` (19 missions couvertes par le silence, friction 41).
**Quand** : ouverture/fermeture de session, fait notable pendant une mission ; lecture obligatoire a la reprise (proto-1 ETAPE 0).

## 3. pilote -- `matrice/pilote/`

| Commande | Usage |
|---|---|
| `file` | `python3 cerveau-projet/matrix/matrice/pilote/main.py file` (affiche la file) |
| `charger` | `python3 cerveau-projet/matrix/matrice/pilote/main.py charger --theme <nom> --objectif "..."` |
| `lot` | `python3 cerveau-projet/matrix/matrice/pilote/main.py lot --lot "nom" --theme "t1,t2" --objectif "o1\|o2"` (plusieurs missions, lot arme) |
| `transformer` | `python3 cerveau-projet/matrix/matrice/pilote/main.py transformer --id M-00X --theme <nom> --objectif "..."` (en attente seulement) |
| `statut` | `python3 cerveau-projet/matrix/matrice/pilote/main.py statut` |
| `injecter` | `python3 cerveau-projet/matrix/matrice/pilote/main.py injecter` (mission suivante, serie stricte ; puisage AUTO dans la tresse si lot et file vides : tisser, puis tete du brin) |
| `enchainer` | `python3 cerveau-projet/matrix/matrice/pilote/main.py enchainer` (demarre le lot : rounds dans la meme boucle) |
| `fin` | `python3 cerveau-projet/matrix/matrice/pilote/main.py fin --bilan "..."` (cloture ; avec lot : enchainement + RETOUR consolide ; sans lot : la suivante (file ou tresse) demarre automatiquement, sortie propre si tout est vide) |
| `file consommer` | `python3 cerveau-projet/matrix/matrice/pilote/main.py file consommer` (echelon 4 : tete du brin tresse -> file du pilote, garde serie stricte) |
| `checklist` | `python3 cerveau-projet/matrix/matrice/pilote/main.py checklist --id M-XXX` (checklist de la mission selon son type) |

**Protections** : refus de double injection (serie stricte), CHAMP THEME FERME (charger / lot / transformer refusent un theme hors vivier vivier-themes.json, code 2 + liste, canonisation a la porte casse-ignoree ; la tresse reste ouverte), lot -> chaque `fin` enchaine la suivante + RETOUR consolide a la Matrice, traces en BDD + intercom.
**Quand** : toute mission passe par le pilote -- jamais de travail hors mission.

## 4. espion-integrite -- `matrice/routines/espion-integrite/`

| Commande | Usage |
|---|---|
| `tour` | `python3 cerveau-projet/matrix/lancer.py espion-integrite tour` (une passe : integrite des 14 BDD + presence des a-construire, journalisee) |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py espion-integrite verifier` (meme verdict, ZERO ligne ecrite : diagnostic des routes en lecture seule) |
| `rotation` | `python3 cerveau-projet/matrix/lancer.py espion-integrite rotation` (borne le journal en ARCHIVANT ses evenements anciens -- jamais de suppression) |
| `boucle` | `python3 cerveau-projet/matrix/lancer.py espion-integrite boucle` (surveillance a intervalle, refus de double lancement) |
| `boucle arret` | `python3 cerveau-projet/matrix/lancer.py espion-integrite boucle arret` (arret cooperatif par drapeau) |

**Protections** : rotation du journal par le moteur PARTAGE `data/commun/rotation_journal.py` (le meme pour les QUATRE journaux de routines -- espion, veille, vigies -- seuil en constantes, archive datee, jamais de suppression, l'archive est dans le "deja connu" et une course est refusee), ne repare JAMAIS (signale ECART, code 1), a-construire = INFO (pas de fausse alerte, seule source du chapitre 2), chapitres ANNONCES calculees du registre (aucun canal declare sans production), PID + drapeau (zero processus fantome), journal en ajout seul et ROTATIONNE (archive datee, rien ne se perd, l'archive est dans le "deja connu" -- L-040 -- et une course est refusee plutot qu'ecrasee), cadence publiee dans un ETAT COURT (espion-etat.json) pour survivre a une rotation.
**Quand** : `tour` apres chaque mission (passe finale) ; `verifier` pour tout diagnostic (jamais `tour` : une route en lecture seule ne doit pas ecrire) ; `boucle` en surveillance continue si demande (elle verifie la rotation avant chaque passe).

## 5. verifier-conventions -- `matrice/data/outils/verifier-conventions/`

| Commande | Usage |
|---|---|
| `verifier` | `python3 cerveau-projet/matrix/lancer.py verifier-conventions verifier` (3 controles : ASCII strict, front-matter identite, index synchronise) |

**Protections** : LECTURE SEULE (signale, ne repare jamais le marbre), index = lignes de tableau seulement (prose ignoree), code 0/1.
**Quand** : apres toute modification d'une convention ou de son index ; integre a la veille (M-012).

## 6. verifier-regles -- `matrice/data/outils/verifier-regles/`

| Commande | Usage |
|---|---|
| `verifier` | `python3 cerveau-projet/matrix/lancer.py verifier-regles verifier` (3 controles : ASCII strict, front-matter identite, index synchronise) |

**Protections** : LECTURE SEULE, index = lignes de tableau, code 0/1.
**Racine** : DETECTEE par remontee jusqu'a AGENTS.md (pattern v1) -- tourne depuis n'importe quel repertoire courant, plus aucun chemin compte a la main.
**Quand** : apres toute modification d'une regle immuable ou de son index ; integre a la veille (M-012).

## 7. verifier-protocoles -- `matrice/data/outils/verifier-protocoles/`

| Commande | Usage |
|---|---|
| `verifier` | `python3 cerveau-projet/matrix/lancer.py verifier-protocoles verifier` (3 controles : ASCII strict, front-matter identite, index synchronise) |

**Protections** : LECTURE SEULE, index = lignes de tableau, citations avec chemin relatif acceptees (resolues depuis le dossier), code 0/1. Les citations de la ZONE DES SOURCES du createur (docs/) sont MESUREES et DITES (groupe `DIT`, marque imprimee `HORS CHAMP`, cible presente/absente) : jamais accusees, parce que la porte ECRIRE refuse cette zone (zone_sources.py) -- un garde n'exige pas une ecriture que la porte du meme domaine interdit (MO-489). Le reste de la Matrice (dont matrice/docs/) reste juge.
**Racine** : DETECTEE par remontee jusqu'a AGENTS.md (pattern v1).
**Quand** : apres toute modification d'un protocole ou de son index ; integre a la veille (M-012).

## 8. corriger-ascii -- `matrice/data/outils/corriger-ascii/`

| Commande | Usage |
|---|---|
| `verifier` | `python3 cerveau-projet/matrix/lancer.py corriger-ascii verifier` (scan seul : ecarts + convertibilite, code 0/1) |
| `corriger` | `python3 cerveau-projet/matrix/lancer.py corriger-ascii corriger` (rapport, rien n'ecrit) |
| `corriger --appliquer` | `python3 cerveau-projet/matrix/lancer.py corriger-ascii corriger --appliquer` (convertit, ecriture atomique LF) |

**Protections** : UN FICHIER SOUS ETALON .sha256 n'est JAMAIS reecrit ; .jsonl (histoire) hors cibles ; caracteres inconnus laisses et signales (jamais de perte) ; affichage console = points de code (jamais de caractere non-ASCII brut).
**Exemptions VISIBLES (MO-075)** : les fichiers hors du champ de reecriture (BDD sous etalon + journaux .jsonl) sont NOMMES en fin de rapport, chacun avec son motif -- l'exclusion n'est jamais muette (mesure : 546 reecrivables contre 578 vus). Le rapport ne cite aucun point de code pour eux (la veille extrait les U+XXXX de la sortie d'un combo : un code cite pour un exempte deviendrait une fausse alerte).
**Racine** : DETECTEE par remontee jusqu'a AGENTS.md.
**Quand** : declenche par la veille-flux (M-012) sur les fichiers modifies ; conversion initiale docs/ effectuee (961 caracteres, 53 emojis signales, validation createur).

## 9. veille-flux -- `matrice/routines/veille-flux/`

| Commande | Usage |
|---|---|
| `veille` | `python3 cerveau-projet/matrix/lancer.py veille-flux veille` (une passe RELAX : corriger-ascii + py_compile) |
| `veille --vigile` | (une passe VIGILE : + les 3 verifiers du marbre) |
| `veille --boucle` | (surveillance continue a intervalle, refus de double lancement) |
| `veille --boucle --vigile --intervalle <s>` | (mode et intervalle combinables) |
| `veille arret` | (drapeau d'arret cooperatif, zero processus tue) |
| `rotation` | `python3 cerveau-projet/matrix/lancer.py veille-flux rotation` (borne journal-veille.txt en ARCHIVANT ses anciens -- jamais de suppression) |

**Protections** : journal ROTATIONNE (MO-078 : archive datee par le moteur PARTAGE `data/commun/rotation_journal.py`, l'archive fait partie du "deja connu" -- L-040 -- et une course est refusee plutot qu'ecrasee ; la boucle verifie la rotation avant chaque passe) ; BDD empreintees intouchables (via corriger-ascii) ; base-acceptee.json (les caracteres acceptes du createur ne produisent JAMAIS d'alerte) ; anti-spam (une seule alerte par signature, `alertes-emises.json`) ; re-test apres pause (fichier en cours d'ecriture = pas de fausse alerte) ; crash de sous-processus JAMAIS confondu avec un verdict (la signature de crash fait foi) ; timeout=120s sur chaque sous-processus (E-045 : un combo bloquant est tue, code 124, incident journalise -- la boucle ne pend jamais) ; alertes graves dans `intercom/matrice/inbox.jsonl` -> missions de reparation.
**Racine** : DETECTEE par remontee jusqu'a AGENTS.md (pattern v1).
**Quand** : `veille` apres chaque mission ; `veille --boucle` en surveillance continue ; VIGILE apres toute modification du marbre (conventions/regles/protocoles). Chaque passe se depose aussi dans la section passes des activites-recentes (M-017).

## 10. bdd-usages -- `matrice/data/outils/bdd-usages/`

| Commande | Usage |
|---|---|
| `noter` | `python3 cerveau-projet/matrix/lancer.py bdd-usages noter --outil <nom> --commande <verbe> --code <n> [--duree <ms>] [--detail "..."] --tags "a,b"` |
| `lire` | `python3 cerveau-projet/matrix/lancer.py bdd-usages lire [--outil X] [--tag Y]` (filtres combinables, reponse vide = aucun resultat) |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py bdd-usages verifier` (structurel : JSON valide, cles requises, tags non vides) |

**Protections** : journal jsonl en AJOUT SEUL (l'histoire jamais reecrite, sans empreinte -- comme historiques-missions) ; tags obligatoires (refus code 2) ; ecriture LF ; garde-fou structurel sur `data/`.
**Amelioration sac a dos (audit protections 2026-09-09)** : quand un outil REFUSE (code != 0), le message de protection (ligne REFUS) est note en DETAIL dans la BDD et affiche par `lire` -- le sac a dos trace la RAISON de chaque protection declenchee, pas seulement le code. Teste en reel (categorie hors liste fermee -> code 1 + message).
**Quand** : chaque appel d'un outil/combo/routine (espions embarques du sac a dos) ; la veille-flux y note deja ses passes ; le createur peut y lire les stats de tout ce qui tourne.

## 11. bdd-variables -- `matrice/data/outils/bdd-variables/`

| Commande | Usage |
|---|---|
| `definir` | `python3 cerveau-projet/matrix/lancer.py bdd-variables definir --cle <nom> --valeur "<valeur>" [--source "..."] --tags "a,b"` |
| `lire` | `python3 cerveau-projet/matrix/lancer.py bdd-variables lire [--cle X] [--tag Y]` |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py bdd-variables verifier` (structurel + empreinte reelle vs etalon) |

**Protections** : une CLE = une valeur courante (re-definir met a jour, l'identifiant V-XXX est conserve, jamais de doublon) ; tags obligatoires (refus code 2) ; ecriture atomique LF ; empreinte SHA-256 dans un fichier separe ; garde-fou structurel sur `data/`.
**Quand** : toute variable vivante de la Matrice (etats, seuils, config decidee) -- modele-mere : le classeur v1 ; l'espion-integrite controle son integrite.

## 12. bdd-activites -- `matrice/data/outils/bdd-activites/`

| Commande | Usage |
|---|---|
| `noter` | `python3 cerveau-projet/matrix/lancer.py bdd-activites noter --section <missions\|alertes\|passes\|decisions> --detail "..." --tags "a,b"` |
| `lire` | `python3 cerveau-projet/matrix/lancer.py bdd-activites lire [--section X] [--tag Y]` |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py bdd-activites verifier` (structurel + empreinte reelle vs etalon) |

**Protections** : sections PRE-DECLAREES (une section inconnue est refusee, code 2 -- la structure ne derive jamais) ; rotation automatique a 50 entrees par section (les plus recentes, modeles-mere : AGENTS-activite-recente) ; tags obligatoires (refus code 2) ; ecriture atomique LF ; empreinte SHA-256 ; garde-fou structurel sur `data/`.
**Quand** : chaque activite notable de la Matrice (missions, alertes, passes, decisions) -- revue RECENTE par emplacements precis, jamais "a la suite" ; l'espion-integrite controle son integrite.

## 13. bdd-historique -- `matrice/data/outils/bdd-historique/`

| Commande | Usage |
|---|---|
| `noter` | `python3 cerveau-projet/matrix/lancer.py bdd-historique noter --type <type> --detail "..." --tags "a,b"` (doublon actif refuse, code 2) |
| `lire` | `python3 cerveau-projet/matrix/lancer.py bdd-historique lire [--type X] [--tag Y] [--depuis AAAA-MM-JJ] [--tout]` (actifs par defaut) |
| `marquer-obsolete` | `python3 cerveau-projet/matrix/lancer.py bdd-historique marquer-obsolete --id H-XXX [--motif "..."]` |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py bdd-historique verifier` (structurel selon le type de ligne, sans empreinte) |

**Protections** : journal jsonl en AJOUT SEUL (l'histoire jamais reecrite) ; obsolete SUR AJOUT (un marqueur vise l'id, l'entree originale intacte) ; doublons ACTIFS refuses (le marquer obsolete pour re-noter) ; cles requises SELON LE TYPE de ligne (evenement vs marqueur) ; ids uniques, cibles verifiees.
**Quand** : tout evenement significatif de la Matrice (mission, reparation, decision, incident) -- filtrage par type/tag/date pour les revues ; l'espion-integrite surveille sa presence.

## 14. entonnoir (echelons 0-3) -- `matrice/pilote/entonnoir/`

| Commande | Usage |
|---|---|
| `deposer` | `python3 cerveau-projet/matrix/matrice/pilote/main.py deposer --theme "..." --objectif "..." [--urgence u] [--source s]` (echelon 0 : vrac, type propose par MOTS ENTIERS) |
| `classer` | `python3 cerveau-projet/matrix/matrice/pilote/main.py classer --id E-XXX --type <dev\|reparation\|doc\|audit\|revision> [--categorie c]` (echelons 1-2 ; categorie PROPOSEE auto par mots entiers si absente -- gardee si dans les categories du type, sinon defaut ; `--categorie` explicite souveraine mais verifiee) |
| `urgencer` | `python3 cerveau-projet/matrix/matrice/pilote/main.py urgencer --id E-XXX --urgence <bloquante\|haute\|normale\|basse>` (echelon 3) |
| `retirer` | `python3 cerveau-projet/matrix/matrice/pilote/main.py retirer --id E-XXX` (sortie PROPRE du vrac -- M-058 : la mission sort avec son historique horodate dans le message ; inconnue code 1, usage code 2 ; ne touche JAMAIS une mission deja classee) |
| `file` | `python3 cerveau-projet/matrix/matrice/pilote/main.py file` (affiche vrac + files, echelon par echelon) |
| `tresse brin` | `python3 cerveau-projet/matrix/matrice/pilote/main.py tresse brin` (affiche le brin tisse) |
| `tresse tisser` | `python3 cerveau-projet/matrix/matrice/pilote/main.py tresse tisser` (recompose le brin : urgence d'abord, puis round-robin par palier) |

**Protections** : listes FERMEES (types, categories, urgences -- une valeur hors liste est refusee, code 2) ; classement PROPOSE deterministe par MOTS ENTIERS (module `mots.py` : casse ignoree, pluriel simple tolere -- M-026 : 'preparer' ne propose plus 'reparation'), reclassable a la main (le createur reste souverain) ; au `classer`, la categorie est proposee auto si absente (gardee seulement si elle est dans les categories du type, sinon defaut -- M-027) ; ecriture atomique (tmp + remplacement) ; modules `listes.py`/`stockage.py`/`mots.py` (jamais constants/commun : collision avec le pilote).
> **Copie OPTIMUS (EO-) :** l operateur a SA copie de l entonnoir (`_operateur/optimus-prime/pilote/entonnoir/`,
> items `EO-NNN`), et elle porte UN verbe de plus -- `preparer` (EO-313) : il declare la LISTE
> DES OUTILS d une mission sur son item, validee a la pose contre les briques servables a
> l injection. Fiche de la zone : `_operateur/optimus-prime/pilote/entonnoir/indices.md`.

**Quand** : tout volume de missions passe par le vrac -- l'echelon 4 (tresse de la file principale) consommera ces files (M-019).

## 15. Outils de l'operateur -- `_operateur/optimus-prime/super-combos/combos/outils/`

La boite a outils transverses de l'operateur : gardes (ascii, tmp, perimetre
write, flux2), lanceurs de non-regression, generateurs (creer-outil,
creer-combo), outils de BDD de travail (bdd-modifs, bdd-lecons-matrice,
bdd-frictions) et espions annexes. Leur fiche de reference est
`outils/outils-readme.md`, posee A COTE d'eux -- le manuel ne la recopie pas
(jamais deux portes pour la meme verite).

> Cette section annoncait "Aucun pour l'instant" alors que le dossier en
> portait 30 : corrige le 2026-09-13 (MO-067). Les outils ne sont NI des combos
> NI des super-combos : ils ne portent aucun numero (contrat CV-008). Les
> super-combos vivent dans `super-combos/` et les combos dans
> `super-combos/combos/`, chacun avec SON `registry.json`.

## 16. dupliquer-template -- `matrice/data/outils/dupliquer-template/`

| Commande | Usage |
|---|---|
| `generer` | `python3 cerveau-projet/matrix/lancer.py dupliquer-template generer --moule <outil-bdd\|theme-bdd\|routine> --nom <nom> ...` (outil-bdd : --bdd --prefixe --liste --champ [--humain] ; theme-bdd : --bdd --prefixe [--nom-affiche] ; routine : --role "ce que la routine fait" [--cadence N] ; defaut : outil-bdd) |

**Protections** : le generateur lit le MOULE (jamais un outil vivant) ; sources traduites EN MEMOIRE puis verifiees avant toute ecriture (py_compile + ASCII + aucun jeton residuel, puis clone executable : docstring + code 2 sans argument pour un OUTIL, UNE PASSE `--once` pour une ROUTINE (jamais son demon)) ; nom ferme PAR MOULE (`bdd-*` pour outil-bdd, `theme-*` pour theme-bdd, `[a-z][a-z0-9-]*` pour routine) et moule inconnu refuse (code 2) ; jamais d'ecrasement (code 2 si l'outil existe) ; un seul ecart = aucune ecriture. Le moule theme-bdd genere un registre de themes a NOM UNIQUE (doublon casse-ignoree refuse code 2) avec SORTIE du registre par `retirer` (par id ou nom).
**Quand** : chaque nouvelle BDD-registre de la Matrice (entrees taguees + empreinte) -- plus jamais de recopie a la main d'un outil existant.
**Suites attendues** : fiche du clone dans ce manuel, BDD au registre de l'espion-integrite, premiere entree par la porte du clone.

## 17. bdd-conservation -- `matrice/data/outils/bdd-conservation/`

> Registre de conservation de la Matrice v3. Il classe les elements avant toute decision et prepare les archives reversibles. Il ne supprime jamais.

| Verbe | Commande |
|---|---|
| `proposer` | `python3 cerveau-projet/matrix/lancer.py bdd-conservation proposer --source <chemin> --categorie <categorie> --raison <raison> --tags <a,b> [--mission MO-XXX]` |
| `classer` | `python3 cerveau-projet/matrix/lancer.py bdd-conservation classer --id K-XXX --categorie <categorie> --raison <raison>` |
| `decider` | `python3 cerveau-projet/matrix/lancer.py bdd-conservation decider --id K-XXX --verdict <conserver|archiver|reparer|dette|signaler> --preuve <preuve> [--destination <chemin>]` |
| `marquer-legacy` | `python3 cerveau-projet/matrix/lancer.py bdd-conservation marquer-legacy --id K-XXX[,K-YYY...] --motif "<motif>" --mission MO-XXX` (MO-431 : declare qu une disparition a ete posee SANS pesee -- motif et mission obligatoires, refus si la mesure existe ou si l entree n est pas `disparu`, idempotent) |
| `lire` | `python3 cerveau-projet/matrix/lancer.py bdd-conservation lire [--id K-XXX] [--categorie X] [--statut X] [--verdict X] [--tag X]` |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py bdd-conservation verifier` |

**Categories fermees** : VIVANT, STRUCTUREL, GENERE, HISTORIQUE, OBSOLETE, COBAYE, ORPHELIN, HORS-PERIMETRE.
**Statuts** : propose -> classe -> decide -> archive/conserve/repare/dette/signale/restaure.
**Protections** : source, raison et tags obligatoires ; lecteurs et ecrivains conserves ; archivage avec destination et preuve ; ecriture atomique LF ; empreinte SHA ; aucune suppression.
**La mesure LEGACY (MO-431)** : une disparition declaree sans pesee n est ni un ecart ni un zero. `marquer-legacy` pose la decision (motif + mission) sur une carence irrecuperable -- mesure du 2026-09-26 : 25 points declares le 2026-09-20, 0 source encore sur le disque, 0 poids dans les 5 versions sauvegardes du registre, `octets_avant: null` au manifeste. `controler-archives` les compte alors EN UNE SEULE LIGNE (`LEGACY ... : 25`) au lieu de relire 25 ids a chaque passe, et une carence NON marquee reste NOMMEE avec son remede : le controle ne s endort que sur une decision, jamais sur un oubli.
**Quand** : avant toute purification reelle, pour classer et decider sans perdre l historique. Flux 1 et cameleon restent en lecture/protection.

## 18. theme-vivier -- `matrice/data/outils/theme-vivier/`

> Registre des THEMES de mission de la Matrice (genere depuis le moule
> templates/theme-bdd). Le vocabulaire canonique que le pilote embarque
> dans ses injections (`themes_utiles`) ; source fondee : themes reels
> de l'historique M-001 a M-038 (les phrases vrac d'avant etaient le
> signal du besoin de canonisation).

| Verbe | Commande |
|---|---|
| `ajouter` | `python3 cerveau-projet/matrix/lancer.py theme-vivier ajouter --nom "NOM" --but "..." [--description "..."]` |
| `modifier` | `python3 cerveau-projet/matrix/lancer.py theme-vivier modifier --id TH-XXX --but "..."` (correction, garde l'id) |
| `lire` | `python3 cerveau-projet/matrix/lancer.py theme-vivier lire [--nom "NOM"]` |
| `retirer` | `python3 cerveau-projet/matrix/lancer.py theme-vivier retirer --id "TH-XXX"` (ou `--nom "NOM"`) |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py theme-vivier verifier` |

**Themes poses** : BDD, OUTIL, ROUTINE, INDICES, CONTRATS, PILOTE, TEMPLATES, REPARATION (TH-002 a TH-009, chacun fonde sur ses missions de preuve).
**Consommation pilote** : depuis M-042, le champ theme du pilote est FERME sur ce vivier (charger / lot / transformer refusent hors vivier) -- le vivier devient la source canonique des themes de mission.
**Quand** : avant de charger une mission (choisir SON theme dans le vivier), a chaque nouveau type de mission recurrent (l'ajouter au vivier fonde sur ses preuves).

## 19. machine-defcon -- `matrice/data/outils/machine-defcon/`

> Machine d'etats defcon (M-059) : le niveau courant vit dans le classeur-variables
> (cle `defcon`, id V-002 conserve). Echelle FERMEE : 5 = stop agent unique /
> optimus-prime reveille + session-matrix mise EN PAUSE (M-080 : la pause est
> declenchee AUTOMATIQUEMENT par `monter --niveau 5`, porte pause-session),
> 4 = suivi de bout en bout, 3 = surveiller puis valider, 2 = normal,
> 1 = reserve (jamais atteint). A defcon 5, seules les missions themees DEFCON
> restent injectables (garde posee dans le pilote : charger, transformer, injecter).

| Verbe | Commande |
|---|---|
| `lire` | `python3 cerveau-projet/matrix/lancer.py machine-defcon lire` (etat + echelle + dernieres transitions) |
| `monter` | `python3 cerveau-projet/matrix/lancer.py machine-defcon monter --niveau <3-5> --raison "..."` (montee libre, sauts permis) |
| `descendre` | `python3 cerveau-projet/matrix/lancer.py machine-defcon descendre --niveau <cible> --raison "..."` (stricte : 5->4, 4->3) |
| `valider` | `python3 cerveau-projet/matrix/lancer.py machine-defcon valider --raison "..."` (clot def3 : 3 -> 2 uniquement) |

**Protections** : la descente 3 -> 2 passe UNIQUEMENT par `valider` (la validation clot la periode de surveillance) ; descente stricte UN echelon a la fois ; `--raison` obligatoire ; ecriture atomique + empreinte du classeur maintenue ; journal des transitions `defcon-historique.jsonl` (append-only, surveille par l'espion).
**Quand** : a la reception d'une demande `[alerte]` (variante detaillee `[alerte=defcon:N]`, convention des crochets v3), pour suivre la mise en securite (def4 = suivi de bout en bout), et pour clore une periode de surveillance (`valider`).

## 20. bilan-periode -- `matrice/data/outils/bilan-periode/`

> Bilan LECTURE SEULE des BDD horodatees sur une periode fermee (M-061).
> Sources : historiques-missions, usages-outils-combos, activites-recentes,
> defcon-historique. La demande `[bilan]` de la convention des crochets
> passe par cette porte. La section usages porte les stats par outil-commande :
> appels, repartition des codes, duree moyenne et max (sac-a-dos, M-077).

| Verbe | Commande |
|---|---|
| `bilan` | `python3 cerveau-projet/matrix/lancer.py bilan-periode bilan --periode <1h|heures|24h|3j|semaine|mois>` (heures = 6 h, mois = 30 jours) |

**Protections** : periode FERMEE (refus code 2 hors liste) ; lecture seule (n'ecrit jamais, aucune empreinte touchee) ; source absente ou cassee = section vide (jamais bloquant) ; lignes cassees des journaux ignorees.
**Quand** : a la reception d'une demande `[bilan]`, avant une revision strategique, pour verifier ce que la Matrice a fait sur une periode.

## 21. editer-agents-md -- `matrice/data/outils/editer-agents-md/`

> L'outil de la session-matrix : la Matrice a SON outil pour modifier
> AGENTS.md dans SON encart (M-074). Il ne touche JAMAIS au reste du fichier :
> uniquement le bloc delimite `<!-- session-matrix:DEBUT/FIN -->` (garde
> structurelle : hors bloc, octet par octet preserve -- sinon REFUS).

| Verbe | Commande |
|---|---|
| `etat` | `python3 cerveau-projet/matrix/lancer.py editer-agents-md etat` (encart actuel + empreinte) |
| `definir` | `python3 cerveau-projet/matrix/lancer.py editer-agents-md definir --nom-llm <id> --agent <nom> --raison "..."` (creation OU maj idempotente) |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py editer-agents-md verifier` (marqueurs apparies + empreinte reelle vs etalon `data/agents-md-empreinte.txt`) |

**Flux v3 grave dans l'encart** : la Matrice accueille au demarrage -> l'operateur fait sa demande -> la Matrice lance le cameleon pour sa mission (serie stricte). L'outil detecte AGENTS.md par remontee (motif unique `data/commun/racine.py`, L-013) et ecrit de facon atomique (tmp + remplacement, LF).

## 22. Modules partages -- `matrice/data/commun/` (M-076)

> Pas un outil (pas de main.py) : les DEUX briques que tout outil de la Matrice
> consomme. Le motif racine et le sac a dos vivent ICI -- jamais recopies
> (M-076 : 5 duplications supprimees, 15 outils + 2 templates equipes).

| Module | Role | Consommation |
|---|---|---|
| `racine.py` | L'UNIQUE `detecter_racine(depart)` : remonte jusqu'au dossier portant AGENTS.md (pattern v1, L-013) | dans un `constants.py` : `sys.path.insert(0, str(REPERTOIRE_DATA / "commun"))` puis `from racine import detecter_racine` et `RACINE = detecter_racine(REPERTOIRE_OUTIL)` |
| `sac_a_dos.py` | `envelopper(principal, arguments)` : chronometre, execute, puis note l'usage (outil, verbe, code, duree ms) dans la BDD usages PAR L'OUTIL bdd-usages (porte unique). Echec de notation jamais bloquant. Garde : bdd-usages ne se note jamais lui-meme | dans un `main.py` : `sys.exit(envelopper(principal, sys.argv[1:]))` |
| `lancement.py` | `lancer_invisible(chemin, arguments, script="main.py")` : lancement DETACHE SANS AUCUNE FENETRE (E-056 : Windows CREATE_NO_WINDOW + SW_HIDE, POSIX start_new_session), retourne (pid, duree_ms). L'UNIQUE facon de lancer un processus de fond -- fini les fenetres qui clignotent | dans un relanceur : `from lancement import lancer_invisible` (voir routines/vie) |
| `trace_session.py` | Le VOCABULAIRE de la trace de session (MO-121) : tags fermes (`session-ouverte`, `travail`, `session-fermee`), etats (`ouverte`/`fermee`/`aucune`) et FORMAT STABLE (`SESSION : `, `RETARD DE TRACE : `). Un contrat ECRIT/LU se declare a UN domicile (L-029, L-093) : celui qui ECRIT la trace et celui qui la LIT importent ce module | dans un lecteur/ecrivain de session : `from trace_session import ETAT_OUVERTE, MARQUEUR_ETAT` |

**Regle de naissance** : tout nouvel outil (y compris via `dupliquer-template`) nait EQUIPE -- le motif et le sac a dos sont dans les moules `templates/outil-bdd`, `templates/theme-bdd` et `templates/routine`. Une note sans tag `sac-a-dos` dans la BDD usages = ecriture directe hors porte (ecart).

**Couche NATIVE declaree (MO-379)** : la couche native n EST PAS une famille de briques
servables -- un module n a pas de `main.py` et s invoque par un CHEMIN ANCRE, jamais par
le lanceur (qui resout un NOM vers un `main.py`). Elle est donc DECLAREE, pas SERVIE : son
domicile `matrice/data/commun` figure dans les `DOMICILES_SUPPLEMENTAIRES` de
`matrice/data/outils/registre-outils/constants.py` (inventorie, `servi=False`), et la porte
`registre-outils` la LIT (`rafraichir` la mesure, `verifier` la controle). La forme
d invocation DITE est le chemin ancre :
`python3 cerveau-projet/matrix/matrice/data/commun/<module>.py <verbe> ...` (exemple :
`fragment.py extraire ...`). Les portes qui la consomment la CITENT dans leur DESCRIPTION
(M-076) : la couche est visible la ou elle sert, et n entre PAS dans la liste des briques
que l agent appelle par leur nom. UN MODULE N EST PAS UN OUTIL.

## 23. Activateur de vie + server matrice -- `matrice/routines/vie/` (M-081)

> Le server de demarrage a 2 etages (E-056) : **server matrice**
> (`server_matrice.py`, boucle de fond invisible) possede le lancement de
> toutes les routines -- **server routine** : chaque routine est lancee/
> relancee PAR LUI, jamais en direct. Toute routine morte est relancee
> automatiquement, SANS AUCUNE FENETRE console (motif partage
> `data/commun/lancement.py`), en ~1 ms (preuve M-081).

| Commande | Effet |
|---|---|
| `python3 cerveau-projet/matrix/lancer.py vie etat` | etat des boucles (ARRET / ACTIVE / fantome nettoye) |
| `python3 cerveau-projet/matrix/lancer.py vie activer` | lance les boucles arretees (detache invisible) |
| `python3 cerveau-projet/matrix/matrice/routines/vie/server_matrice.py` | DEMARRE le server matrice (boucle de surveillance, intervalle 60 s) |
| `python3 cerveau-projet/matrix/lancer.py vie server arret` | arret cooperatif du server (drapeau, jamais de kill) |
| `python3 cerveau-projet/matrix/lancer.py vie server etat` | etat du server matrice (PID REELMENT sonde ; fantome detecte + nettoye) |

**Correction audit protections 2026-09-09** : `server etat` lisait le fichier
PID sans verifier le processus (faux `ACTIVE` avec un PID mort). Desormais il
SONDE le PID (motif `processus_vivant` partage avec les boucles) : un fantome
est signale et nettoye. Le server matrice a ete demarre et sa relance auto
prouvee en reel : espion tue, relance par le server en ~2 s (nouveau PID).

## 24. journal-multi-encarts -- `matrice/data/outils/journal-multi-encarts/` (M-079)

> Le VISUEL des metriques de la Matrice (v3, E-049) : un NOUVEAU fichier
> `matrice/journal-multi-encarts.md`, propre a la v3 -- il ne remplace rien
> et ne touche JAMAIS aux fichiers v1/v2 (regle versions-intangibles).
> Genere depuis les BDD, jamais edite a la main (comme une vue).

| Verbe | Commande |
|---|---|
| `construire` | `python3 cerveau-projet/matrix/lancer.py journal-multi-encarts construire` (regenere le journal complet, ordre ferme des encarts) |
| `lire` | `python3 cerveau-projet/matrix/lancer.py journal-multi-encarts lire` (journal entier) ; `python3 cerveau-projet/matrix/lancer.py journal-multi-encarts lire --encart <nom>` (UN encart ; inconnu -> code 2) |

**Lecture BORNEE (MO-078)** : l'encart routines lisait `journal-veille.txt` EN ENTIER (mesure du 2026-09-13 : 3,85 Mo / 44 050 lignes) pour n'afficher que 5 evenements ; il lit desormais la QUEUE (256 Ko) par le lecteur PARTAGE `data/commun/rotation_journal.py` -- cout constant quelle que soit la taille du journal.

**Encarts (ordre ferme, jamais en vrac)** : matrice (defcon + boucles), missions (en cours + vrac/files/brin), routines (dernieres passes veille), alertes (veille + intercom), cameleon (messages RECUS par le cameleon, M-080), usages (8 derniers appels), modifications (5 derniers fichiers), lecons (5 dernieres), variables (classeur).
> PAS d'encart optimus (decision createur 2026-09-09) : optimus reste INVISIBLE --
> son suivi vit UNIQUEMENT dans son fichier dedie `_operateur/optimus-prime/suivi-optimus.md`. Chaque encart est present meme vide -- aucune entree en vrac. Format createur (M-080) : chaque encart porte SA ligne de FLUX (d'ou viennent les infos, vers ou elles vont) + un TABLEAU `| Entree | Heure | Date |` (heure et date separees, format HH:MM:SS JJ/MM/AAAA, jamais en debut de ligne).

## 25. pause-session -- `matrice/data/outils/pause-session/` (M-080)

> Protocole de pause session-matrix (decisions createur) : LA MATRICE UTILISE
> LE CAMELEON, jamais l'inverse (regle `matrice/regles/matrice-utilise-cameleon.md`).
> Pause = cameleon arrete, mission sauvegardee A LA PAUSE SEULEMENT (etat
> serialise `data/session-matrix-etat.json`, sortie de la file du pilote),
> notification "maintenance" (la raison reelle n'est JAMAIS divulguee).
> La reprise restore A L'IDENTIQUE (meme mission, meme place dans la file).

| Verbe | Commande |
|---|---|
| `pause` | `python3 cerveau-projet/matrix/lancer.py pause-session pause [--raison "..."]` (manuel `[pause]` ou defcon 5 auto) |
| `reprendre` | `python3 cerveau-projet/matrix/lancer.py pause-session reprendre` (apres maintenance user ; restore + notifie) |
| `etat` | `python3 cerveau-projet/matrix/lancer.py pause-session etat` (montre l'etat de pause s'il existe) |
| `perimetre` | `python3 cerveau-projet/matrix/lancer.py pause-session perimetre --zones "a,b"` (reduit la lecture cameleon ; vide = restaure) |
| `journal` | `python3 cerveau-projet/matrix/lancer.py pause-session journal` (10 derniers evenements pause/reprise) |
| `clore` | `python3 cerveau-projet/matrix/lancer.py pause-session clore --motif "..."` (regularise une pause ORPHELINE : journalise la reprise SANS toucher la file) |

**Protections** : REFUS si pause deja posee (pas de pause double) ; REFUS de reprendre si une mission est en cours (serie stricte) ; pendant la pause, le pilote REFUSE toute injection/enchainement (garde `session_en_pause`) et la fin HORS lot ne relance rien ; defcon 5 declenche la pause AUTOMATIQUEMENT (raccord dans machine-defcon `monter`) ; perimetre tenu dans le classeur-variables (cle `perimetre-cameleon`, ecriture atomique + empreinte) ; journal `data/pauses-session-matrix.jsonl` (append-only). Boite cameleon : `intercom/cameleon/inbox.jsonl` (etancheite : raison "maintenance" seulement).
**Etancheite des sorties (audit protections 2026-09-09)** : aucune sortie console de la Matrice (pause-session, machine-defcon, pilote, verifier-*) ne revele le nom de l'entite interne -- terme neutre "maintenance" uniquement. La zone `perimetre-cameleon` du classeur porte la zone NEUTRE `maintenance` ; `lire_perimetre` la RESOUT vers les chemins reels a exclure (le classeur ne fuit jamais le nom).
**Quand** : demande `[pause]` (maintenance manuelle), defcon 5 (mise en securite totale), ou reprise apres maintenance.

## 26. trio marbre BDD -- `matrice/data/outils/bdd-{regles,conventions,protocoles}-matrice/` (M-082)

> Domiciliation du marbre Matrice (E-051) : les regles, conventions et protocoles
> DE LA MATRICE vivent en 3 BDD separees (un outil par BDD, nes du moule
> `outil-bdd`). Ecriture : optimus seul (hors session-matrix, en maintenance).
> Lecture : Matrice + cameleon. Les marbres d'optimus restent dans `_operateur/`
> (versions-intangibles, intouchables).

| Outil | BDD | Contenu |
|---|---|---|
| `bdd-regles-matrice` | `data/bdd-regles-matrice.json` | R-001/R-002/R-003 (matrice-utilise-cameleon, perimetre, langue) |
| `bdd-conventions-matrice` | `data/bdd-conventions-matrice.json` | CV-001..CV-010 (0 valeur en dur, ascii, outils structure, sac-a-dos, crochets, nommage numerote, prefixes) |
| `bdd-protocoles-matrice` | `data/bdd-protocoles-matrice.json` | P-001..P-003 (routes cameleon, protocoles 6-7-8) |

**Interface** (identique pour les 3) : `ajouter --entree "..." --tags "..."` / `modifier --id R-XXX --entree "..."` (ou `--regle`/`--convention`/`--protocole`, correction qui garde l'id) / `lire [--tag ...]` / `verifier`. Espion : les 3 BDD sont surveillees (registre integrite).
> **bdd-conventions-matrice en plus (MO-045)** : `renommer --id <ancien> --vers <nouveau>`
> (change l'ID seul, trace `ancien_id` + `renomme_le` dans l'entree) et
> `modifier ... [--tags "a,b"]` (corrige aussi les tags). Recette d'une porte de
> BDD : `ajouter` + `renommer` + `modifier` + `lire` + `verifier` (CV-010).
> Prefixe des ids : `CV-` (regle CV-009 : une famille = un prefixe ; `C-` seul
> n'est plus qu'un vestige fige, le champ `constat` de historiques-missions).
> Le verbe `modifier` existe parce que ces BDD gravees sont LUS par le cameleon :
> toute correction de contenu (ex : retirer une mention interdite) passe par la
> porte, jamais par reecriture manuelle (porte unique).
**Quand** : toute nouvelle regle/convention/protocole de la Matrice passe par ces outils (plus aucun fichier markdown de marbre dans `matrice/`).

## 27. suivi-optimus -- `matrice/data/outils/suivi-optimus/` (M-084)

> Trace de suivi d'optimus-prime (GO createur) : le createur ne peut pas le
> voir travailler (optimus invisible dans la v3), cette trace note L'AGENT
> (decisions, portes, missions, pourquoi) -- le sac-a-dos note les OUTILS,
> jamais de recouvrement. Trace append-only + etalon SHA-256, ecrite par
> optimus seul (porte unique), le cameleon n'y accede JAMAIS (zone `suivi-optimus`
> exclue du perimetre-cameleon, regle gravee dans sa fiche).

| Verbe | Commande |
|---|---|
| `noter` | `python3 cerveau-projet/matrix/lancer.py suivi-optimus noter --mission M-XXX --theme SUIVI --action <action> --detail "..." [--fichiers "a,b"] [--portes "a,b"] [--duree-s N]` |
| `lire` | `python3 cerveau-projet/matrix/lancer.py suivi-optimus lire [--mission M] [--action a] [--n N]` (filtres + n derniers) |
| `vue` | `python3 cerveau-projet/matrix/lancer.py suivi-optimus vue` (genere le markdown dedie `_operateur/optimus-prime/suivi-optimus.md`, tous les evenements) |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py suivi-optimus verifier` (integrite SHA-256, etalon-or) |
| `coherence` | `python3 cerveau-projet/matrix/lancer.py suivi-optimus coherence [--racine <matrix>]` (croise la file du pilote et ce journal) |
| `archiver` | `python3 cerveau-projet/matrix/lancer.py suivi-optimus archiver [--racine <matrix>]` (sort du journal les evenements hors perimetre OPTIMUS en les ARCHIVANT dans `suivi-optimus-hors-perimetre.jsonl` ; journal reecrit, empreinte recalculee, idempotent) -- `--doublons` sort les 2e debut / 2e fin d'une meme mission (l'ECART que `verifier` remonte) vers `suivi-optimus-doublons.jsonl`, le PREMIER evenement faisant foi |
| `corriger` | `python3 cerveau-projet/matrix/lancer.py suivi-optimus corriger [--mission MO-XXX] --motif "..." [--simuler oui] [--racine <matrix>]` (corrige EN PLACE une `duree_s` DECLAREE qui CONTREDIT la mesure des bornes : la valeur honnete est VIDE -- le pilote n'a jamais mesure, la VUE calcule -- et l'ancienne valeur reste relisible dans `corrections` AVEC son motif ; aucune ligne supprimee ni ajoutee, empreinte recalculee, idempotent). Decision operateur 2026-09-19 (EO-269) : JAMAIS un bornage du controle par DATE (un bandeau sur les yeux) ; le motif est OBLIGATOIRE |

**Actions fermees (enum, anti-bruit par EVENEMENT)** : `debut`, `fin`, `porte`, `depot`, `decision`, `decouverte`, `bilan` -- hors enum refusee (code 2). Format d'une ligne : `date, mission, theme, action, detail, fichiers[], portes[], duree_s`.
**Vue** : `vue` genere le fichier markdown dedie `_operateur/optimus-prime/suivi-optimus.md` avec UN TABLEAU PAR ACTION (sections fermees dans l'ordre de l'enum) -- decision createur 2026-09-09 : optimus n'a PAS d'encart au journal multi-encarts (il reste invisible), SON fichier est la seule vue de son travail. Le fichier est genere, jamais edite a la main.
**Etancheite (philosophie d'invisibilite, CV-006/L-016)** : le cameleon n'accede JAMAIS a cette trace. MO-235 : son fichier dedie vit desormais dans la zone privee `_operateur/optimus-prime/suivi-optimus.md` -- il est invisible PAR CONSTRUCTION (la zone `_operateur` est exclue), et non plus par une exclusion de NOM ; la zone `suivi-optimus` (journal et archives sous `matrice/data/`) reste exclue du perimetre-cameleon.
**Quand** : a chaque action significative d'optimus (GO/arbitrage, fin de mission, porte utilisee, depot au vrac, decouverte d'audit, bilan).
**Coherence (verbe `coherence`, MO-048)** : le pilote ecrit la FILE, l'agent declare au JOURNAL (marbre L-020 : le pilote ne note RIEN) -- deux traces separees que rien ne compare. Le verbe les croise : un ECART est une divergence a reparer (code 1 : mission close dans la file sans fin declaree, fin declaree sans cloture, mission du journal inconnue de la file, serie stricte violee, COMPTEUR en retard sur le plus grand id utilise -- donc un id sur le point d'etre reattribue) ; une DETTE est un etat transitoire legitime ou un residu hors perimetre (`en-cours` sans debut au journal = fenetre d'injection ; identifiants non `MO-` au journal = residus du cameleon), signalee sans bloquer. Cable comme MAILLON 9 de `lanceur-non-regression-flux.py` : un ecart fait tomber le flux.

## 28. lire -- `matrice/data/outils/lire/` (MO-001)

> Porte unique de lecture (remplace `read_files` natif). Lecture seule, jamais d'ecriture. Annonce `total/lu` a chaque lecture, SHA-256 optionnel, perimetre `matrix/` seul (allowlist `AGENTS.md`/`demarrer-*.md`).

| Verbe | Commande |
|---|---|
| `lire` | `python3 cerveau-projet/matrix/lancer.py lire lire --fichier <chemin> [--lignes debut:fin] [--hash]` |
|  | `python3 cerveau-projet/matrix/lancer.py lire lire --fichiers <c1,c2> [--lignes debut:fin] [--hash]` |
|  | `python3 cerveau-projet/matrix/lancer.py lire lire --dossier <chemin> [--filtre *.py] [--recursif] [--hash]` |

**Protections** : perimetre `matrix/` seul (hors perimetre = code 2, allowlist racine) ; fichier absent = code 1 ; tranche `--lignes` hors bornes = tronquee annoncee ; non-UTF8/binaire = code 1 ; BOM/CRLF detectes et signales ; 2e canal L-009 (relecture croisee si doute) ; lecture seule (jamais de tmp/empreinte).
**Benchmark** : 5000 lignes lues `5000/5000` (0.4ms direct, vs natif tronque a 2000 sans alerte) ; 1000 lignes <1ms.
**Quand** : toute lecture de fichier par Optimus -- remplace `read_files` natif (0.4ms vs 2000 lignes tronquees silencieusement).

## 29. ecrire -- `matrice/data/outils/ecrire/` (MO-002)

> Porte unique d ecriture (remplace `write_file` + `str_replace` natifs). Atomique, LF, .bak, SHA, validation.

| Verbe | Commande |
|---|---|
| `ecrire` | `python3 cerveau-projet/matrix/lancer.py ecrire ecrire --fichier <chemin> --contenu "<texte|@fichier>" [--mode creer|remplacer|ajouter]` |
|  | `python3 cerveau-projet/matrix/lancer.py ecrire ecrire --fichier <chemin> --contenu-fichier <chemin-source> [--mode creer|remplacer|ajouter]` |
|  | `python3 cerveau-projet/matrix/lancer.py ecrire ecrire --fichier <chemin> --contenu-base64 <blob> [--mode creer|remplacer|ajouter]` |
| `editer` | `python3 cerveau-projet/matrix/lancer.py ecrire editer --fichier <chemin> --ancien "<old|@fichier>" --nouveau "<new|@fichier>"` |
|  | `python3 cerveau-projet/matrix/lancer.py ecrire editer --fichier <chemin> --ancien-fichier <chemin> --nouveau-fichier <chemin>` |
|  | `python3 cerveau-projet/matrix/lancer.py ecrire editer --fichier <chemin> --ancien-base64 <blob> --nouveau-base64 <blob>` |

**Protections** : perimetre `matrix/` seul (hors = code 2, allowlist `AGENTS.md`/`demarrer-*.md`) ; `--mode` ferme `creer|remplacer|ajouter` ; `creer` refuse si existe (code 2) ; `editer` exige 1 occurrence unique (0 ou >1 = code 2) ; l EXTRAIT a deux formes (exacte, puis SANS son LF final : `ecrire` en force un, L-001) et la forme retenue est DITE -- si elle perd le LF, le NOUVEAU le perd aussi ; rien ne s execute apres la publication (compte-rendu construit AVANT, MO-173) ; validation `.py` (`py_compile` + garde d ORDRE) et `.json` (`json.load`) -- echec = code 1 et **RIEN n est ecrit** (la cible reste INTACTE, `.bak` de la tentative conserve) ; LF forces (L-001) ; `.bak` horodate ; SHA avant/apres ; ASCII signale ; `@file` anti-heredoc (`--contenu @chemin` ou `--contenu-fichier`) ; ecriture atomique `tmp+os.replace` ; valeur a tirets acceptee (`---` : une carte d identite s ecrit en UNE passe) ; option PRIVEE de valeur = REFUS nomme (code 2, EO-156) -- jamais videe en silence ; les **TROIS sources de contenu sont EXCLUSIVES** (`--contenu`, `--contenu-fichier`, `--contenu-base64`) et seule leur PRESENCE compte ; une source VIDE est REFUSEE (ecrire un fichier vide est une intention, pas un oubli) ; **`--contenu-base64` = transport SANS echappement (MO-173)** : blob base64 STRICT (refus nomme si invalide ou non-UTF8), le MEME contenu traverse la chaine CORROMPU en brut et **BIT-EXACT** en base64 ; les **DEUX textes de `editer` ont le MEME transport** (MO-376) : `--ancien-base64` / `--nouveau-base64` (blob STRICT, refus nomme), **UN SEUL transport par cote** (`--ancien`, `--ancien-fichier`, `--ancien-base64` EXCLUSIFS -- un melange silencieux ferait gagner l un des deux sans le dire) et le bit-exact est GARANTI : un NOUVEAU qui COMMENCE par une arobase est ecrit TEL QUEL, sans relecture comme chemin -- les fichiers OLD/NEW deviennent INUTILES ; garde d ORDRE (EO-159) : un import LOCAL dont le nom n est pas lie par le fournisseur = REFUS avant publication (un ImportError n est pas une SyntaxError : `py_compile` le laisse passer) ; secours DECLARE : le point de restauration `.bak` + `revert-fichier.py` (combos/outils) qui ecrit hors porte EXPRES, quand la porte est la chose cassee.
**Benchmark** : 1000 lignes <30ms ; LF pur verifie (CRLF 0).
**Quand** : toute ecriture ou edition par Optimus -- remplace `write_file`/`str_replace` natifs (non atomiques, pas de revert).
**Domicile partage (EO-158)** : le parseur d options n est plus recopie -- `data/commun/options.py` porte le contrat (valeur a tirets, nom d option connu SEUL arrete, option privee de valeur DITE) et 41 outils le CONSOMMENT.

## 30. lister -- `matrice/data/outils/lister/` (MO-003)

> Porte unique de listage (remplace `glob` + `list_directory` natifs). 1 porte, tri mtime, filtre L-016.

| Verbe | Commande |
|---|---|
| `lister` | `python3 cerveau-projet/matrix/lancer.py lister lister --dossier <chemin> [--filtre <glob>] [--recursif] [--json]` |

**Protections** : perimetre `matrix/` seul (hors = code 2, allowlist `AGENTS.md`/`demarrer-*.md`) ; dossier absent = code 1 ; `__pycache__/.git` exclus ; zones L-016 (`_operateur/tmp-optimus/suivi-optimus`) exclues (0 fuite) ; tri mtime deterministe ; 1 porte couvre `glob+list_directory`.
**Benchmark** : `matrix/` recursif 464 entrees en 174ms ; `outils` recursif `.py` 182 fichiers.
**Quand** : tout listage par Optimus -- remplace `glob`/`list_directory` natifs (exposaient structure privee).

## 31. rechercher -- `matrice/data/outils/rechercher/` (MO-004, corrige MO-069)

> Porte unique de RECHERCHE (fichiers + 8 BDD en un appel). Lecture seule. C'est ici qu'on cherche une mission, une lecon, un fichier -- plus de recherche a la main.

| Verbe | Commande |
|---|---|
| `rechercher` | `python3 cerveau-projet/matrix/lancer.py rechercher rechercher --requete <texte> [--dans fichiers\|bdd\|tous]` |
|  | `[--tag <tag>] [--mot-cle <texte>] [--source <nom>] [--periode 7j\|30j\|3m\|1a]` |
|  | `[--json] [--limite N]` |
|  | `[--prive]` (EO-126 : inclut les zones invisibles L-016 -- FICHIERS seulement) |
| `indexer` | palier 2 (FTS5) -- non implemente |
| `schema` | affiche les options |

**Protections** : perimetre `matrix/` seul ; zones L-016 filtrees ; fichiers BINAIRES exclus par extension (`.db`, `.pyc`...) ; une option illisible est REFUSEE (code 2) : `--source` inconnue nomme les sources valides, `--periode` hors forme `<nombre><j\|m\|a>`, `--limite` non entiere ; `--tag`/`--mot-cle`/`--source` refuses avec `--dans fichiers` (ils ne filtreraient rien), et `--prive` refuse avec `--dans bdd` (meme raison : une option qui ne filtre pas est un affichage) ; sortie `--json` en ASCII pur.
**Contrat (MO-069, etendu MO-126/EO-126)** : un FILTRE filtre (`--tag`, `--mot-cle`, `--source`, `--periode` RETIRENT des resultats) ; **un hit = une ENTREE** (jamais une section : `lecons/L-054`) ; **un hit dit SUR QUOI il a matche** (`sur` = `nom` ou `contenu` -- un fichier se trouve par son NOM, pas seulement par son contenu) ; une coupe ou un ecart est DIT (`tronque`, `ecartes_sans_date`).
**Benchmark** : scan BDD complet ~0,3 s sur les 8 sources (usages 67k lignes lues SANS troncature muette) ; limite 50 resultats par defaut.
**Branchement** : vigie-portes (sonde de cecite a chaque tour) + cockpit prive route `/chercher` (`cockpit-matrice.py --route chercher --requete "<texte>"`), qui l'appelle avec `--prive` -- cette route annonce `zone_perimetre = maintenance,_operateur` : sans le drapeau la promesse etait FAUSSE (EO-126).
**Quand** : des qu'il faut retrouver une mission, une lecon, un fichier ou un usage -- ne jamais chercher a la main ni par le natif (pas de BDD, pas de tags).

## 32. domicilier -- `matrice/data/outils/domicilier/` (MO-172, EO-160)

> Aligne une **CLASSE** de copies sur son **DOMICILE**, conduite par un PLAN qui declare tout (fonction, marqueur, delegation, **exclusions**, **perimetre attendu**). Ecriture DANS la porte, jamais a cote.

| Verbe | Commande |
|---|---|
| `auditer` | `python3 cerveau-projet/matrix/lancer.py domicilier auditer [--plan <chemin>] [--perimetre <dossier>] [--json]` |
| `aligner` | `python3 cerveau-projet/matrix/lancer.py domicilier aligner [--plan <chemin>] [--perimetre <dossier>] [--simuler\|--publier]` |

**Protections** : **`--simuler` est le DEFAUT** (aucune ecriture sans `--publier`) ; la remorque n ecrit JAMAIS elle-meme -- fragments compris, tout passe par la PORTE `ecrire` (garde, validation, `.bak`, SHA), et une validation refusee laisse la cible INTACTE ; plan incomplet / domicile absent / **exclusion qui n exclut rien** = REFUS (code 2) ; une copie que le plan ne LISTE pas (`attendu`) = **TROU** et alignement REFUSE ; une copie attendue qui ne porte plus la fonction = plan **PERIME** (code 1) ; le DOMICILE n est jamais compte comme une copie de lui-meme ; `--json` ne porte QUE le rapport (aucune prose).
**Contrat du plan** : champs fermes `classe`, `fonction`, `domicile`, `marqueur`, `docstring`, `import`, `appel` ; optionnels `exclus` (homonymes declares), `attendu` (perimetre declare), `extras` (le plan gagne sur la deduction), `derive` (deduire le suffixe du texte ANCIEN : drapeaux, sans_tirets). Le TEXTE ANCIEN n est jamais redevine : le bloc de la fonction est LU puis remplace exactement.
**Benchmark** : plan reel (`plans/parseur-options.json`, classe du parseur d options) : **41 copies alignees, 1 exclue, 0 trou** en une passe ; epreuve MO-172 : **18 controles OK** dans un bac a sable (aucune ecriture hors du bac).
**Quand** : quand un motif a ete RECOPIE et qu il faut domestiquer la classe -- mesurer l ecart (`auditer`), puis aligner (`aligner --publier`) ; suite directe de MO-171 (domicile `data/commun/options.py`).
## 33. registre-outils -- `matrice/data/outils/registre-outils/` (EO-314, MO-316)

> Le REGISTRE DES OUTILS : une BDD **UNIQUE** (colonne `proprietaire`) qui dit ce que le
> parc des briques **EST maintenant**, et la **PROPOSITION** d une liste d outils pour une
> mission -- chacun avec **SON MOTIF**. Il ne remplace ni l extracteur
> (`pilote/injection/modes_emploi.py`) ni la porte `entonnoir preparer` : il les relie --
> le registre **propose**, l operateur **decide**, la porte **pose**.

| Verbe | Commande |
|---|---|
| `rafraichir` | `python3 cerveau-projet/matrix/lancer.py registre-outils rafraichir` |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py registre-outils verifier` |
| `lire` | `python3 cerveau-projet/matrix/lancer.py registre-outils lire [--proprietaire <optimus\|matrice\|cameleon>] [--servis]` |
| `proposer` | `python3 cerveau-projet/matrix/lancer.py registre-outils proposer --theme "..." --objectif "..." [--plafond N]` |

**BDD** : `matrice/data/registre-outils.json` (+ son empreinte etalon `.sha256`). Entree =
`nom`, `proprietaire`, `domicile`, `chemin`, `servi_a_l_injection`, `origine`, `but`,
`snippet`, `empreinte_texte`, `statut`. La BDD porte aussi `perimetre` et `homonymes`.
**Penurie de recouvrement** : le journal `usages-outils-combos.jsonl` raconte les APPELS
(des evenements) ; le registre est un ETAT -- aucun recouvrement, aucune duplication.
**Protections** : la BDD est **regeneree**, jamais editee a la main (`rafraichir` repose
l empreinte etalon ; l espion d integrite la declare `integrite verifiee`) ; l usage reste
**extrait de la brique** (M-076/L-032) et l empreinte couvre **ce qui est range**
(`but` + `snippet`) -- une correction de code qui ne change pas le texte servi n est PAS un
ecart ; les **racines servies** sont LUES dans l extracteur (la colonne `servi` dit ce que
l injection sert vraiment) ; **un plafond illisible = REFUS** (une proposition non bornee
se lirait comme un conseil ferme) et les **ecartees par le plafond sont DITES** avec leur
motif ; **la proposition n ecrit RIEN** (elle imprime le geste `entonnoir preparer`) ;
**une brique non servie n est jamais proposee** et **une brique muette est enregistree ET
accusee** ; ecriture atomique LF.
**Contrat de `verifier`** : les QUATRE ecarts -- `perimes` (avec ce qui a change : but,
snippet), `disparus`, `non_enregistres`, `muets` -- et le remede est nomme (`rafraichir`).
**Branchement** : la porte `entonnoir preparer` (la proposition fournit la liste que
l operateur pose) ; registre de l espion-integrite (`BDDS`) ; registre de
conservation (`K-1440`, VIVANT conserver).
**Quand** : avant de poser la liste d outils d une mission (`preparer --outils`), et a
chaque doute sur ce que le parc contient ou sur ce qu il a change.

## 34. inventaire-systeme -- `matrice/data/outils/inventaire-systeme/` (MO-251)

> La FICHE MACHINE : un fichier qui dit sur quelle machine vit la Matrice (OS,
> architecture, hote, session, capacites, reseau, outils installes), et la PORTE
> qui la tient a jour. Modele : la v1 (`agents/tools/verifier/verifier-systeme`).

| Verbe | Commande |
|---|---|
| `mesurer` | `python3 cerveau-projet/matrix/lancer.py inventaire-systeme mesurer` |
| `lire` | `python3 cerveau-projet/matrix/lancer.py inventaire-systeme lire [--resume]` |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py inventaire-systeme verifier` |

**Fiche** : `matrice/data/systeme-machine.md` (carte d identite `type: fiche`), a cote des
autres fiches de la Matrice. Sections : `RESUME MACHINE` (courte, servie a l injection),
`SYSTEME`, `CAPACITES`, `RESEAU`, `OUTILS INSTALLES`, `TENUE A JOUR`.
**Injection** : l entree `contexte-machine` de `avant-mission` (catalogue
`_operateur/optimus-prime/pilote/injection/config.json`) sert la SEULE section
`RESUME MACHINE` -- une fiche entiere deversee a chaque mission serait du poids sans
usage. Mesure du 2026-09-20 : 205 tokens, pour un total avant-mission de 7753.
**Protections** : une mesure NON faite est DITE `-` (dependance absente, mesureur muet),
jamais `0` (0 serait un fait, et il serait faux) ; la **VRAM** est lue au REGISTRE
(`HardwareInformation.qwMemorySize`, 64 bits) et NON par `AdapterRAM` (DWORD signe
plafonne a 4 Go -- mesure du jour : 12272 Mo au lieu de 4095) ; les commandes systeme sont lancees en
LISTE d arguments (aucun shell) et les scripts Windows sont lances par `cmd /c` (mesure
du jour : `npm.CMD` rendait `Version inconnue`) ; ecriture ATOMIQUE (tmp + remplacement,
LF forces) ; **un fait non mesure est un fait qui ment** (L-055).
**Contrat de `verifier`** : la carte d identite, la section servie, les cases du resume,
les champs COMPARES contre une mesure FRAICHE (OS, architecture, hote, versions de
python3, node, git), et l entree du catalogue d injection (declaree, pointant la fiche,
avec SA section) -- code 0 sain, 1 ecart nomme, 2 fiche absente.
**Quand** : au premier demarrage sur une machine, apres un changement de machine ou de
version d outil, et avant toute decision qui depend de ce que la machine SAIT FAIRE.


## 35. fichiers-travail-cameleon -- `matrice/data/outils/fichiers-travail-cameleon/` (MO-378)

LA PORTE JUMELLE DU FLUX CAMELEON : le meme besoin que `fichiers-travail` d Optimus
(nommer, lister, montrer, vider, journaliser les fichiers de travail d une mission),
dans SON domicile -- sa zone `workspace/tmp-cameleon`. Elle CONSOMME les declarations
partagees (`matrice/data/commun/zone_tmp.py` : nom et chemin de la zone) et ne copie
AUCUN code du jumeau ; sa forme de nom est `M-`, celle de son pilote.

| Verbe | Commande |
|---|---|
| `nommer` | `python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon nommer --mission M-378 --libelle bilan [--extension txt]` |
| `lister` | `python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon lister [--mission M-378] [--strict] [--json]` |
| `montrer` | `python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon montrer m-378-bilan.txt` |
| `vider` | `python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon vider [--mission M-378] [--par <qui>]` |
| `journal` | `python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon journal [--n 20]` |
| `--auto-test` | `python3 cerveau-projet/matrix/lancer.py fichiers-travail-cameleon --auto-test` |

**Classes** : `canonique` (forme canonique ET posee par la porte), `canonique-non-journalise`
(forme canonique mais jamais posee par la porte), `residu` (aucune forme canonique -- un
fichier pose a la main, RENDU VISIBLE). **Journal** : `fichiers-travail-cameleon-journal.jsonl`,
en ajout seul, qui DIT ce qui a ete pose et ce qui a ete solde (visibilite : voir sans
fouiller).
**Garde associe** : `garde-residus-zone.py` (`_operateur/optimus-prime/super-combos/combos/outils/`),
MAILLON 42 de la non-regression : il CRIE sur une purge mentie, un residu ou une zone
sans README (`--cloture` accuse tout element restant).
**Preuves** : auto-test 16/16 (cobaye qui MORD sur un residu et une mission de forme
`MO-`, contre-temoin qui EPARGNE).

## 36. bdd-corvees -- `matrice/data/outils/bdd-corvees/` (MO-416)

> Registre des CORVEES : la phase < si j etais user > (protocole 13) inventorie les taches
> ingrates -- celles qu un user ne devrait JAMAIS avoir a refaire pour obtenir un resultat --
> avec leur COUT MESURE, l automatisation proposee et la PREUVE attendue. Genere depuis le
> moule `templates/outil-bdd` (modele-mere `bdd-lecons`).

| Verbe | Commande |
|---|---|
| `ajouter` | `python3 cerveau-projet/matrix/lancer.py bdd-corvees ajouter --corvee "..." --tags "a,b" [--source "..."]` |
| `lire` | `python3 cerveau-projet/matrix/lancer.py bdd-corvees lire [--tag X]` |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py bdd-corvees verifier` |

**Convention de contenu** (mesuree sur les entrees C-001 a C-012) : une corvee dit (1) le GESTE
ingrat, (2) son COUT MESURE, (3) l AUTOMATISATION proposee et (4) la PREUVE attendue -- une
porte et un verdict, jamais une promesse. Une corvee dont l automatisation est faite devient un
FAIT (C-011, C-012) : elle garde son id et sa preuve mesuree, elle ne disparait pas.
**Tags obligatoires** : pas de corvee orpheline.
**Protections** : ecriture atomique (tmp + remplacement, fins de ligne LF forcees), empreinte
SHA-256 recalculee a chaque ecriture, contenu et tags obligatoires.
**Quand** : pendant la phase < si j etais user > du round, et a chaque geste ingrat constate une
DEUXIEME fois (la repetitivite est le signal -- un geste fait une fois n est pas une corvee).
## 37. carte-creer -- `matrice/data/outils/carte-creer/` (MO-430)

> Premiere porte de la SUITE des cartes d identite : poser un front-matter `identite:` en tete
> d un document qui n en a pas. Le bloc vient du MODELE de reference
> (`matrice/templates/carte-identite`) et les regles du DOMICILE partage
> (`matrice/data/commun/carte_identite.py`). Toute ecriture passe PAR LA PORTE `ecrire`
> (decision createur MO-430) : fragments puis cible, donc validation, point de restauration et
> refus a occurrence unique -- le garde de provenance (controle attribution) jauge chaque carte posee.

| Verbe | Commande |
|---|---|
| `creer` | `python3 cerveau-projet/matrix/lancer.py carte-creer creer --fichier <chemin> --type <type> --appartient-a <nom> [--commun true\|false] [--liens "c1, c2"] [--version <n>] [--date AAAA-MM-JJ] [--statut <etat>] [--tags "m1, m2"] [--modele complet\|minimal]` |

**Codes** : 0 carte posee ; 1 ecart (modele illisible, ecriture refusee par la porte) ; 2 refus d usage (option inconnue ou privee de valeur, fichier absent, carte deja presente, carte non conforme) -- le refus NOMME son remede.
**Protections** : un document qui porte DEJA une carte est REFUSE (`carte-modifier` change un champ, `carte-editer` remplace la carte entiere) ; `--type` et `--appartient-a` obligatoires (les deux cles qui ne se devinent pas) ; la carte est validee AVANT ecriture (memes jugements que le garde `verifier-cartes-identite`) ; sans `--modele`, le modele COMPLET sert -- un champ sans valeur est OMIS et DIT, jamais rempli d un placeholder.
**Auto-test** : 8/8 (`carte-creer --auto-test`).
**Quand** : premiere mise en cartes d un document sans carte, ou fabrication d un document retrouvable par `rechercher --champ` / `--lien`.

## 38. carte-editer -- `matrice/data/outils/carte-editer/` (MO-430)

> Remplace le front-matter `identite:` ENTIER d un document par un nouveau bloc fourni par
> fichier. Le bloc est juge par le DOMICILE partage AVANT toute ecriture, puis passe PAR LA PORTE
> `ecrire` : si la porte refuse, la cible reste INTACTE. Le corps du document n est jamais touche.

| Verbe | Commande |
|---|---|
| `editer` | `python3 cerveau-projet/matrix/lancer.py carte-editer editer --fichier <chemin> --nouveau-fichier <chemin du nouveau front-matter>` |

**Codes** : 0 carte remplacee (ou deja identique : RIEN A FAIRE, non pas une erreur) ; 1 ecart (ecriture refusee par la porte) ; 2 refus d usage (options manquantes, document sans carte, bloc non valide ou non conforme).
**Protections** : un document SANS carte est REFUSE (la carte se POSE d abord par `carte-creer`) ; le nouveau bloc est juge par le domicile partage, jamais par l outil (type hors vocabulaire, cle obligatoire vide ou lien mort = arret avant ecriture) ; seul le bloc entre `---` change.
**Auto-test** : 7/7 (`carte-editer --auto-test`).
**Quand** : changer plusieurs champs d un coup, migrer une carte vers une autre forme (minimale -> complete), corriger une carte non conforme apres mesure par `carte-comparer`.

## 39. carte-modifier -- `matrice/data/outils/carte-modifier/` (MO-430)

> Change UNE seule cle de la carte : la valeur est REMPLACEE, une cle absente est INSEREE (avec
> l indentation des voisines), `--supprimer` RETIRE le champ (jamais une cle obligatoire). Le
> vocabulaire des cles vient du MODELE de reference : une cle qui n est ni du modele ni deja dans
> la carte est une faute de frappe, et elle est NOMMEE. Le bloc RESULTAT est valide AVANT ecriture,
> puis passe PAR LA PORTE `ecrire` (si la porte refuse, la cible reste INTACTE).

| Verbe | Commande |
|---|---|
| `modifier` | `python3 cerveau-projet/matrix/lancer.py carte-modifier modifier --fichier <chemin> --cle <nom> --valeur <valeur>` |
| `modifier` (retirer) | `python3 cerveau-projet/matrix/lancer.py carte-modifier modifier --fichier <chemin> --cle <nom> --supprimer` |

**Codes** : 0 champ change (ou deja identique : RIEN A FAIRE) ; 1 ecart (ecriture refusee par la porte) ; 2 refus d usage (gestes absents ou exclusifs, document sans carte, cle inconnue, resultat non conforme).
**Protections** : `--valeur` et `--supprimer` EXCLUSIFS (un seul geste par appel) ; une cle obligatoire n est jamais retiree ; le changement rendu est VALIDE avant ecriture (`--type type-invente` ou `--commun peut-etre` arretent l appel sans rien toucher) ; pour `liens` et `tags`, `--valeur` remplace la LISTE entiere (separateur virgule) -- ajouter un lien, c est relire la liste et la reposer.
**Auto-test** : 10/10 (`carte-modifier --auto-test`).
**Quand** : mettre a jour un champ au fil de l eau (statut, date, version, liens) sans remplacer la carte entiere.

## 40. carte-comparer -- `matrice/data/outils/carte-comparer/` (MO-430)

> Lecture seule : la carte face a SON MODELE de reference (`matrice/templates/carte-identite`).
> Decision createur MO-430 : la reference est le modele -- l outil dit si ses champs sont PRESENTS
> et si la carte est CONFORME (memes jugements que le garde `verifier-cartes-identite`, consommes
> jamais copie : M-076). Aucune porte d ecriture n est utilisee : l outil ne change rien, il REND un rapport.

| Verbe | Commande |
|---|---|
| `comparer` (une carte) | `python3 cerveau-projet/matrix/lancer.py carte-comparer comparer --fichier <chemin> [--modele complet\|minimal]` |
| `comparer` (le corpus) | `python3 cerveau-projet/matrix/lancer.py carte-comparer comparer --corpus [--dans <dossier>] [--modele ...]` |

**Codes** : 0 CONFORME (z ecart, presence dite champ par champ) ; 1 NON CONFORME (les ecarts sont LISTES) ; 2 refus d usage (sujet absent ou double, document sans carte, perimetre vide).
**Rapport** : une carte = presence (`presents 6/8`, `absents : ...`) puis conformite ; le corpus = total des documents, presence PAR CHAMP (`liens : 11/113`), documents sans carte, puis ecarts listes (borne a 8 lignes). Les cles absentes du modele ne sont pas des ecarts (une carte sans `liens` est NORMALE) : elles sont DITES, pas jugees. Sujet par defaut = le corpus de la racine Matrice.
**Combo** : `c-008-cartes` (CV-008, entree `cartes` de la banque -- inventaire du corpus de cartes).
**Auto-test** : 6/6 (`carte-comparer --auto-test`).
**Preuve reel (MO-430)** : 177 documents, 172 cartes, presence `type` 172/172 -- 5 ecarts reels nommes (cameleon.md et USER-PROFIL.md sans `commun`, trois types hors vocabulaire attendu).
**Quand** : avant de livrer une carte (je suis conforme ?), pour mesurer un corpus (ou manque-t-il des champs ?), et pour retrouver ce que le modele exige.

## 41. bdd-raisonnement -- `_operateur/optimus-prime/raisonnement/bdd-raisonnement/` (zone INVISIBLE, MO-482)

> BDD de RAISONNEMENT d OPTIMUS (decision createur 2026-09-27, EO-458) : les SEGMENTS
> de raisonnement deviennent une BDD outillee, DANS LA ZONE INVISIBLE (L-016 -- le
> cameleon ne la lit jamais). Generee par `dupliquer-template generer --moule outil-bdd
> --zone privee` (surcharge privee `templates/outil-bdd-prive`).

| Verbe | Commande |
|---|---|
| `ajouter` | `<outil>/main.py ajouter --segment "..." --tags "a,b" [--source "..."]` |
| `lire` | `<outil>/main.py lire [--tag X]` |
| `corriger` | `<outil>/main.py corriger --id RS-XXX --tags "a,b" [--motif "..."]` |
| `retirer` | `<outil>/main.py retirer --id RS-XXX [--index N] [--motif "..."]` |
| `verifier` | `<outil>/main.py verifier` |

avec `<outil>` = `_operateur/optimus-prime/raisonnement/bdd-raisonnement` (appel par CHEMIN : l outil n est PAS dans le lanceur commun, pour ne pas exposer la zone au cameleon).

**BDD** : `_operateur/optimus-prime/raisonnement/segments.json` (empreinte SHA-256 a cote).
**Moteur** : declaree en SOURCE PRIVEE (`rechercher/constants.py`, `BDD_SOURCES_PRIVEES`) -- servie SEULEMENT sous `--prive` :
`python3 cerveau-projet/matrix/matrice/data/outils/rechercher/main.py rechercher --dans bdd --source segments --prive`.
Sans `--prive`, la source est REFUSEE (L-016).
**Quand** : consigner un SEGMENT de raisonnement (une partie, progressive et tracee), et le retrouver.
**Qui, et a quel moment (MO-500, option C de l audit MO-499)** : c est la CLOTURE du round qui le
DEMANDE -- `pilote fin --segment-fichier <chemin.jsonl>` : OUI, le round le depose (la `source` est
posee par la cloture, jamais declaree par l agent) ; NON, elle le DIT, et le constat part au marbre.
Le geste est ecrit dans la LOI DU ROUND (proto-12, geste 4.7) ; le CHOIX < reutilisable ou non >
reste a l agent, la MESURE est automatique et compte les DEUX cas.
**Deux garde-fous de la porte (EO-537, mesures du 2026-09-30)** : `ajouter` REFUSE le
DOUBLON (meme contenu ET meme source que l entree active) en nommant l id deja present, et
le refus intervient AVANT le compteur -- donc il ne consomme aucun id ; `retirer` sort une
entree fautive de la liste mais la conserve ENTIEREMENT dans `retraits` (date + motif +
entree), donc le retrait est REVERSIBLE. Mesure a l origine : cinq segments deposes deux
fois par un script de depot relance, qu il a fallu marquer a la main faute de porte.
Le meme TEXTE sous une source DIFFERENTE reste accepte : c est la source qui distingue deux
raisonnements identiques, jamais le texte.
## 42. bdd-raisonnement-cameleon -- `agents/cameleon/raisonnement/bdd-raisonnement-cameleon/` (domicile du CAMELEON, PARTAGE, MO-483)

> BDD de RAISONNEMENT du CAMELEON (decision createur 2026-09-27, EO-459) : un
> concept SEMBLABLE a celle d Optimus mais DISTINCT ; elle vit dans le DOMICILE du
> cameleon et est PARTAGEE entre les deux agents (VISIBLE : le moteur la sert SANS
> `--prive`). Generee par `dupliquer-template generer --moule outil-bdd --zone
> cameleon` (surcharge `templates/outil-bdd-cameleon`).

| Verbe | Commande |
|---|---|
| `ajouter` | `<outil>/main.py ajouter --segment "..." --tags "a,b" [--source "..."]` |
| `lire` | `<outil>/main.py lire [--tag X]` |
| `verifier` | `<outil>/main.py verifier` |

avec `<outil>` = `agents/cameleon/raisonnement/bdd-raisonnement-cameleon` (appel par CHEMIN : l outil n est PAS sous `data/outils/`).

**BDD** : `agents/cameleon/raisonnement/segments-cameleon.json` (empreinte SHA-256 a cote).
**Moteur** : declaree en SOURCE PARTAGEE (`rechercher/constants.py`, `BDD_SOURCES_PARTAGEES`) -- servie SANS `--prive` :
`python3 cerveau-projet/matrix/matrice/data/outils/rechercher/main.py rechercher --dans bdd --source segments-cameleon`.
**L-016 a la livraison** : une entree PARTAGEE qui nomme le vocabulaire interdit (optimus, _operateur, ...) est FILTREE par le moteur -- la BDD du cameleon ne doit nommer aucun acteur invisible.
**Quand** : consigner un SEGMENT de raisonnement du cameleon, et le retrouver.
## 43. rendre-graphe -- `matrice/data/outils/rendre-graphe/` (MO-493, EO-449)

> COMPOSER EN MERMAID, CONVERTIR EN SVG (demande du createur 2026-09-26). OPTIMUS
> lit le MERMAID ; le createur lit le SVG : les deux vues sont le MEME graphe. Les
> INCOHERENCES d une source y deviennent des NOEUDS ROUGES -- une incoherence
> cachee est une incoherence qu on ne repare pas.

| Verbe | Commande |
|---|---|
| `mermaid` | `python3 cerveau-projet/matrix/lancer.py rendre-graphe mermaid [--source parcours\|vivier\|arbre] [--theme <NOM>] [--arbre <fichier.json>] [--sortie <fichier>] [--appliquer]` |
| `svg` | `python3 cerveau-projet/matrix/lancer.py rendre-graphe svg (--mermaid <fichier.mmd> \| [--source parcours\|vivier\|arbre] [--theme <NOM>] [--arbre <fichier.json>]) [--sortie <fichier>] [--appliquer]` |
| `verifier` | `python3 cerveau-projet/matrix/lancer.py rendre-graphe verifier [--source parcours\|vivier\|arbre] [--theme <NOM>] [--arbre <fichier.json>]` |

- `mermaid` : une SOURCE -> le TEXTE Mermaid. Sans `--theme`, la vue est l INDEX du
  parcours (les themes dans leur ordre, le theme COURANT marque) ; avec
  `--theme NOM`, la vue est la suite de cases de CE theme, ses renvois et sa fin.
- `svg` : du TEXTE Mermaid -> l IMAGE SVG. Le texte vient de `--mermaid <fichier>`
  (un Mermaid ECRIT A LA MAIN : LU, jamais reecrit) ou d une source, qui passe alors
  par le MEME generateur. Le moteur ne voit donc jamais un modele : il voit du
  TEXTE -- c est ce qui prouve la chaine de bout en bout.
- `verifier` : le JUGE des sources, LECTURE SEULE. Il ACCUSE (fichier de theme
  absent, theme orphelin, renvoi vers un fichier ou une CASE introuvable, fin hors
  de `fins.json`, id de vivier hors forme, categorie hors liste FERMEE, nom double,
  but vide). Il ne repare JAMAIS.

**Garanties** : DRY par defaut (rien ne s ecrit sans `--appliquer`) ; les vues se
DEPOSENT par la porte `ecrire` (perimetre, `.bak`, SHA, ASCII, LF) et les textes
passent par des FICHIERS (un accent grave en argument serait EXECUTE -- MO-142) ;
rendu DETERMINISTE (meme texte -> memes octets) ; AUCUNE dependance (ni navigateur,
ni node, ni reseau) ; ASCII strict et XML ECHAPPE ; ma place DEDUITE et verifiee,
le domicile du vivier LU a `theme-vivier/constants.py` (M-076) ; l ancrage des
chemins CONSOMME `data/commun/cible.py`. Codes : `0` rendu (ou aucune incoherence),
`1` incoherences (nommees une par une), `2` refus (source inconnue, fichier illisible).

**Vues** : `_operateur/optimus-prime/vues/mermaid/*.mmd` et `vues/svg/*.svg`.
**Memoire v1** : `agents/tools/consulter/convertir-carte-mermaid/convertir-carte-mermaid.py`
(parseur l. 526, rangs l. 620, mise en page l. 651, rendu SVG l. 683, en-tete l. 776).
**Deux ecarts DECLARES a la v1** : un RANG SE REPLIE au-dela de `LARGEUR_PAGE_MAX`
(mesure 2026-09-29 : le vivier reel rendait 6866 px de large sur une seule ligne),
et le commentaire d en-tete ne porte plus de `--` (INTERDIT en XML : `ElementTree`
refusait le document entier).
**Quand** : rendre un parcours ou le vivier lisible des deux cotes, ou VERIFIER
qu une source tient debout avant de s y fier.

## 44. Les briques du parc sans fiche individuelle (MO-566)

> Ces 19 briques etaient au registre et dans aucune liste. Le maillon 81
> (les trois listes du parc se comparent) rend le compte visible sans le
> rendre faute ; il ne montrait ni QUI, ni OU. Chaque ligne porte le but lu au
> registre, a sa source. Les briques de cette zone `matrice/data/commun/` ne
> sont PAS ici : la fiche de groupe `## 22. Modules partages` les couvre
> toutes, et une mention de groupe vaut une mention.
>
> Une fiche complete reste preferable a une mention : celle-ci dit ce que la
> brique fait, pas tous ses verbes ni ses protections.

| Brique | Domicile | Ce qu elle fait |
|---|---|---|
| `commun.py` | `_operateur/optimus-prime/pilote` | fonctions communes du pilote : file de missions, intercom, historique, chaine (lot) |
| `personnalites.py` | `_operateur/optimus-prime/pilote` | roles d Optimus : la table FERMEE qui associe un type de mission a une PERSONNALITE du vivier |
| `verifier-profil.py` | `_operateur/optimus-prime/pilote` | verificateur du profil utilisateur : la fiche du createur est-elle complete, et les valeurs attendues y sont-elles ? |
| `lancer-super-combos.py` | `_operateur/optimus-prime/super-combos` | lanceur des super-combos PAR NUMERO : sc-001, sc-002... plutot que par leur nom long |
| `sc-002-auto-evolution` | `_operateur/optimus-prime/super-combos` | super-combo auto-evolution : le cycle qui fait progresser une mission depuis une idee jusqu a son livrable |
| `sc-003-auto-suivi` | `_operateur/optimus-prime/super-combos` | super-combo auto-suivi : fait le point sur l avancement d un travail a partir des traces deja produites |
| `sc-004-auto-diagnostic` | `_operateur/optimus-prime/super-combos` | super-combo auto-diagnostic : diagnostique les outils et PREPARE leurs reparations |
| `sc-005-moules` | `_operateur/optimus-prime/super-combos` | super-combo garde des MOULES (`matrice/templates/`) : verifie qu un moule n a pas derive de son gabarit |
| `sc-006-lacunes` | `_operateur/optimus-prime/super-combos` | super-combo des lacunes : retrouver ce qui manque dans la v3 et le combler (demande createur MO-530) |
| `sc-007-table-ronde` | `_operateur/optimus-prime/super-combos` | super-combo de la TABLE RONDE : 5 facons de penser, 3 rounds, 1 arbitrage |
| `benchmark` | `matrice/data/outils` | mise a l epreuve d un fichier ou d un dossier par 9 epreuves (perimetre, LF, sha, validation, ASCII, BDD, relecture, bak, invisibilite) ; toute mission qui touche un fichier passe benchmark avant la fin |
| `chaine-pense-bete` | `matrice/data/outils` | Point d'entree global de l'outil chaine-pense-bete -> spec -> todo-list (EO-215, MO-224). |
| `maintenir` | `matrice/data/outils` | porte des signalements de maintenance : lister ceux qui attendent, traiter le plus critique, et dire l etat de la maintenance |
| `passerelle-demandes` | `matrice/data/outils` | extrait les demandes en langage naturel du canal du createur, les type par leur CROCHET et les depose dans l entonnoir (le WET exige --confirmer) |
| `commun.py` | `matrice/pilote` | fonctions communes du pilote : file de missions, intercom, historique, chaine (lot) |
| `detecteur-mots-cles.py` | `matrice/pilote` | detecteur de mots-cles de la Matrice : transforme les themes declares en signaux qu une demande peut faire remonter |
| `chien` | `matrice/routines` | routine de fond : le declencheur sur changement -- il observe le perimetre ASCII, et lance le combo de correction en arriere-plan des qu un fichier bouge |
| `suivi-sync` | `matrice/routines` | routine de fond : resynchronise le suivi-optimus (journal et tete) et regenere sa tete quand elle est perimee |
| `verifier-liens-cartes` | `matrice/routines` | routine de fond : verifie que les liens et les cartes d identite du projet pointent des cibles qui existent, et publie son rapport |
