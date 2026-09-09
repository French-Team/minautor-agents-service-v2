# MANUEL DES OUTILS -- Matrice et operateur

> Une fiche par outil : commandes, protections, quand l'utiliser.
> MIS A JOUR A CHAQUE NAISSANCE OU MODIFICATION D'OUTIL (convention-indices).
> Pour l'architecture d'un outil : lire son DESCRIPTION.md.

## 1. bdd-modifications -- `matrice/data/outils/bdd-modifications/`

| Commande | Usage |
|---|---|
| `noter` | `python main.py noter --fichier <chemin> --action <cree\|modifie\|corrige\|supprime> --detail "..." --tags "a,b"` |
| `lire` | `python main.py lire [--fichier X] [--tag Y]` (filtres combinables, reponse vide = aucun resultat) |
| `verifier` | `python main.py verifier` (empreinte reelle vs etalon) |

**Protections** : actions en vocabulaire ferme (cree/modifie/corrige/supprime), ecriture atomique LF, empreinte SHA-256 dans un fichier separe, garde-fou structurel sur `data/`.
**Quand** : APRES chaque modification d'un fichier de la Matrice (anti-surcharge : jamais de commentaire de modification dans le fichier).

## 2. bdd-lecons -- `matrice/data/outils/bdd-lecons/`

| Commande | Usage |
|---|---|
| `ajouter` | `python main.py ajouter --lecon "..." --tags "a,b" [--source "..."]` |
| `lire` | `python main.py lire [--tag X]` |
| `verifier` | `python main.py verifier` |

**Protections** : porte unique des lecons (corrections.md est supprime), tags obligatoires, ecriture atomique LF, empreinte.
**Quand** : fin d'une evolution validee (proto-2), apres chaque lecon reelle ; le pilote consomme ces lecons taguees dans ses injections.

## 3. pilote -- `matrice/pilote/`

| Commande | Usage |
|---|---|
| `file` | `python main.py file` (affiche la file) |
| `charger` | `python main.py charger --theme <nom> --objectif "..."` |
| `lot` | `python main.py lot --lot "nom" --theme "t1,t2" --objectif "o1\|o2"` (plusieurs missions, lot arme) |
| `transformer` | `python main.py transformer --id M-00X --theme <nom> --objectif "..."` (en attente seulement) |
| `statut` | `python main.py statut` |
| `injecter` | `python main.py injecter` (mission suivante, serie stricte ; puisage AUTO dans la tresse si lot et file vides : tisser, puis tete du brin) |
| `enchainer` | `python main.py enchainer` (demarre le lot : rounds dans la meme boucle) |
| `fin` | `python main.py fin --bilan "..."` (cloture ; avec lot : enchainement + RETOUR consolide ; sans lot : la suivante (file ou tresse) demarre automatiquement, sortie propre si tout est vide) |
| `file consommer` | `python main.py file consommer` (echelon 4 : tete du brin tresse -> file du pilote, garde serie stricte) |
| `checklist` | `python main.py checklist --id M-XXX` (checklist de la mission selon son type) |

**Protections** : refus de double injection (serie stricte), CHAMP THEME FERME (charger / lot / transformer refusent un theme hors vivier vivier-themes.json, code 2 + liste, canonisation a la porte casse-ignoree ; la tresse reste ouverte), lot -> chaque `fin` enchaine la suivante + RETOUR consolide a la Matrice, traces en BDD + intercom.
**Quand** : toute mission passe par le pilote -- jamais de travail hors mission.

## 4. espion-integrite -- `matrice/routines/espion-integrite/`

| Commande | Usage |
|---|---|
| `tour` | `python main.py tour` (une passe : integrite + presence des 7 BDD) |
| `boucle` | `python main.py boucle` (surveillance a intervalle, refus de double lancement) |
| `boucle arret` | `python main.py boucle arret` (arret cooperatif par drapeau) |

**Protections** : ne repare JAMAIS (signale ECART, code 1), a-construire = INFO (pas de fausse alerte), PID + drapeau (zero processus fantome), journal en ajout seul.
**Quand** : `tour` apres chaque mission (passe finale) ; `boucle` en surveillance continue si demande.

## 5. verifier-conventions -- `matrice/data/outils/verifier-conventions/`

| Commande | Usage |
|---|---|
| `verifier` | `python main.py verifier` (3 controles : ASCII strict, front-matter identite, index synchronise) |

**Protections** : LECTURE SEULE (signale, ne repare jamais le marbre), index = lignes de tableau seulement (prose ignoree), code 0/1.
**Quand** : apres toute modification d'une convention ou de son index ; integre a la veille (M-012).

## 6. verifier-regles -- `matrice/data/outils/verifier-regles/`

| Commande | Usage |
|---|---|
| `verifier` | `python main.py verifier` (3 controles : ASCII strict, front-matter identite, index synchronise) |

**Protections** : LECTURE SEULE, index = lignes de tableau, code 0/1.
**Racine** : DETECTEE par remontee jusqu'a AGENTS.md (pattern v1) -- tourne depuis n'importe quel repertoire courant, plus aucun chemin compte a la main.
**Quand** : apres toute modification d'une regle immuable ou de son index ; integre a la veille (M-012).

## 7. verifier-protocoles -- `matrice/data/outils/verifier-protocoles/`

| Commande | Usage |
|---|---|
| `verifier` | `python main.py verifier` (3 controles : ASCII strict, front-matter identite, index synchronise) |

**Protections** : LECTURE SEULE, index = lignes de tableau, citations avec chemin relatif acceptees (resolues depuis le dossier), code 0/1.
**Racine** : DETECTEE par remontee jusqu'a AGENTS.md (pattern v1).
**Quand** : apres toute modification d'un protocole ou de son index ; integre a la veille (M-012).

## 8. corriger-ascii -- `matrice/data/outils/corriger-ascii/`

| Commande | Usage |
|---|---|
| `verifier` | `python main.py verifier` (scan seul : ecarts + convertibilite, code 0/1) |
| `corriger` | `python main.py corriger` (rapport, rien n'ecrit) |
| `corriger --appliquer` | `python main.py corriger --appliquer` (convertit, ecriture atomique LF) |

**Protections** : UN FICHIER SOUS ETALON .sha256 n'est JAMAIS reecrit ; .jsonl (histoire) hors cibles ; caracteres inconnus laisses et signales (jamais de perte) ; affichage console = points de code (jamais de caractere non-ASCII brut).
**Racine** : DETECTEE par remontee jusqu'a AGENTS.md.
**Quand** : declenche par la veille-flux (M-012) sur les fichiers modifies ; conversion initiale docs/ effectuee (961 caracteres, 53 emojis signales, validation createur).

## 9. veille-flux -- `matrice/routines/veille-flux/`

| Commande | Usage |
|---|---|
| `veille` | `python main.py veille` (une passe RELAX : corriger-ascii + py_compile) |
| `veille --vigile` | (une passe VIGILE : + les 3 verifiers du marbre) |
| `veille --boucle` | (surveillance continue a intervalle, refus de double lancement) |
| `veille --boucle --vigile --intervalle <s>` | (mode et intervalle combinables) |
| `veille arret` | (drapeau d'arret cooperatif, zero processus tue) |

**Protections** : BDD empreintees intouchables (via corriger-ascii) ; base-acceptee.json (les caracteres acceptes du createur ne produisent JAMAIS d'alerte) ; anti-spam (une seule alerte par signature, `alertes-emises.json`) ; re-test apres pause (fichier en cours d'ecriture = pas de fausse alerte) ; crash de sous-processus JAMAIS confondu avec un verdict (la signature de crash fait foi) ; timeout=120s sur chaque sous-processus (E-045 : un combo bloquant est tue, code 124, incident journalise -- la boucle ne pend jamais) ; alertes graves dans `intercom/matrice/inbox.jsonl` -> missions de reparation.
**Racine** : DETECTEE par remontee jusqu'a AGENTS.md (pattern v1).
**Quand** : `veille` apres chaque mission ; `veille --boucle` en surveillance continue ; VIGILE apres toute modification du marbre (conventions/regles/protocoles). Chaque passe se depose aussi dans la section passes des activites-recentes (M-017).

## 10. bdd-usages -- `matrice/data/outils/bdd-usages/`

| Commande | Usage |
|---|---|
| `noter` | `python main.py noter --outil <nom> --commande <verbe> --code <n> [--duree <ms>] [--detail "..."] --tags "a,b"` |
| `lire` | `python main.py lire [--outil X] [--tag Y]` (filtres combinables, reponse vide = aucun resultat) |
| `verifier` | `python main.py verifier` (structurel : JSON valide, cles requises, tags non vides) |

**Protections** : journal jsonl en AJOUT SEUL (l'histoire jamais reecrite, sans empreinte -- comme historiques-missions) ; tags obligatoires (refus code 2) ; ecriture LF ; garde-fou structurel sur `data/`.
**Quand** : chaque appel d'un outil/combo/routine (espions embarques du sac a dos) ; la veille-flux y note deja ses passes ; le createur peut y lire les stats de tout ce qui tourne.

## 11. bdd-variables -- `matrice/data/outils/bdd-variables/`

| Commande | Usage |
|---|---|
| `definir` | `python main.py definir --cle <nom> --valeur "<valeur>" [--source "..."] --tags "a,b"` |
| `lire` | `python main.py lire [--cle X] [--tag Y]` |
| `verifier` | `python main.py verifier` (structurel + empreinte reelle vs etalon) |

**Protections** : une CLE = une valeur courante (re-definir met a jour, l'identifiant V-XXX est conserve, jamais de doublon) ; tags obligatoires (refus code 2) ; ecriture atomique LF ; empreinte SHA-256 dans un fichier separe ; garde-fou structurel sur `data/`.
**Quand** : toute variable vivante de la Matrice (etats, seuils, config decidee) -- modele-mere : le classeur v1 ; l'espion-integrite controle son integrite.

## 12. bdd-activites -- `matrice/data/outils/bdd-activites/`

| Commande | Usage |
|---|---|
| `noter` | `python main.py noter --section <missions\|alertes\|passes\|decisions> --detail "..." --tags "a,b"` |
| `lire` | `python main.py lire [--section X] [--tag Y]` |
| `verifier` | `python main.py verifier` (structurel + empreinte reelle vs etalon) |

**Protections** : sections PRE-DECLAREES (une section inconnue est refusee, code 2 -- la structure ne derive jamais) ; rotation automatique a 50 entrees par section (les plus recentes, modeles-mere : AGENTS-activite-recente) ; tags obligatoires (refus code 2) ; ecriture atomique LF ; empreinte SHA-256 ; garde-fou structurel sur `data/`.
**Quand** : chaque activite notable de la Matrice (missions, alertes, passes, decisions) -- revue RECENTE par emplacements precis, jamais "a la suite" ; l'espion-integrite controle son integrite.

## 13. bdd-historique -- `matrice/data/outils/bdd-historique/`

| Commande | Usage |
|---|---|
| `noter` | `python main.py noter --type <type> --detail "..." --tags "a,b"` (doublon actif refuse, code 2) |
| `lire` | `python main.py lire [--type X] [--tag Y] [--depuis AAAA-MM-JJ] [--tout]` (actifs par defaut) |
| `marquer-obsolete` | `python main.py marquer-obsolete --id H-XXX [--motif "..."]` |
| `verifier` | `python main.py verifier` (structurel selon le type de ligne, sans empreinte) |

**Protections** : journal jsonl en AJOUT SEUL (l'histoire jamais reecrite) ; obsolete SUR AJOUT (un marqueur vise l'id, l'entree originale intacte) ; doublons ACTIFS refuses (le marquer obsolete pour re-noter) ; cles requises SELON LE TYPE de ligne (evenement vs marqueur) ; ids uniques, cibles verifiees.
**Quand** : tout evenement significatif de la Matrice (mission, reparation, decision, incident) -- filtrage par type/tag/date pour les revues ; l'espion-integrite surveille sa presence.

## 14. entonnoir (echelons 0-3) -- `matrice/pilote/entonnoir/`

| Commande | Usage |
|---|---|
| `deposer` | `python main.py deposer --theme "..." --objectif "..." [--urgence u] [--source s]` (echelon 0 : vrac, type propose par MOTS ENTIERS) |
| `classer` | `python main.py classer --id E-XXX --type <dev\|reparation\|doc\|audit\|revision> [--categorie c]` (echelons 1-2 ; categorie PROPOSEE auto par mots entiers si absente -- gardee si dans les categories du type, sinon defaut ; `--categorie` explicite souveraine mais verifiee) |
| `urgencer` | `python main.py urgencer --id E-XXX --urgence <bloquante\|haute\|normale\|basse>` (echelon 3) |
| `retirer` | `python main.py retirer --id E-XXX` (sortie PROPRE du vrac -- M-058 : la mission sort avec son historique horodate dans le message ; inconnue code 1, usage code 2 ; ne touche JAMAIS une mission deja classee) |
| `file` | `python main.py file` (affiche vrac + files, echelon par echelon) |
| `tresse brin` | `python main.py tresse brin` (affiche le brin tisse) |
| `tresse tisser` | `python main.py tresse tisser` (recompose le brin : urgence d'abord, puis round-robin par palier) |

**Protections** : listes FERMEES (types, categories, urgences -- une valeur hors liste est refusee, code 2) ; classement PROPOSE deterministe par MOTS ENTIERS (module `mots.py` : casse ignoree, pluriel simple tolere -- M-026 : 'preparer' ne propose plus 'reparation'), reclassable a la main (le createur reste souverain) ; au `classer`, la categorie est proposee auto si absente (gardee seulement si elle est dans les categories du type, sinon defaut -- M-027) ; ecriture atomique (tmp + remplacement) ; modules `listes.py`/`stockage.py`/`mots.py` (jamais constants/commun : collision avec le pilote).
**Quand** : tout volume de missions passe par le vrac -- l'echelon 4 (tresse de la file principale) consommera ces files (M-019).

## 15. Outils de l'operateur -- `_operateur/optimus-prime/super-combos/combos/outils/`

Aucun pour l'instant (l'outil ajouter-lecon a ete supprime avant naissance :
sa cible corrections.md est retiree -- proto-5, jamais deux portes).
Les futurs outils operateur s'ajoutent ICI avec leur fiche.

## 16. dupliquer-template -- `matrice/data/outils/dupliquer-template/`

| Commande | Usage |
|---|---|
| `generer` | `python main.py generer --moule <outil-bdd\|theme-bdd> --nom <nom> ...` (outil-bdd : --bdd --prefixe --liste --champ [--humain] ; theme-bdd : --bdd --prefixe [--nom-affiche] ; defaut : outil-bdd) |

**Protections** : le generateur lit le MOULE (jamais un outil vivant) ; sources traduites EN MEMOIRE puis verifiees avant toute ecriture (py_compile + ASCII + aucun jeton residuel, puis clone executable) ; nom ferme PAR MOULE (`bdd-*` pour outil-bdd, `theme-*` pour theme-bdd) et moule inconnu refuse (code 2) ; jamais d'ecrasement (code 2 si l'outil existe) ; un seul ecart = aucune ecriture. Le moule theme-bdd genere un registre de themes a NOM UNIQUE (doublon casse-ignoree refuse code 2) avec SORTIE du registre par `retirer` (par id ou nom).
**Quand** : chaque nouvelle BDD-registre de la Matrice (entrees taguees + empreinte) -- plus jamais de recopie a la main d'un outil existant.
**Suites attendues** : fiche du clone dans ce manuel, BDD au registre de l'espion-integrite, premiere entree par la porte du clone.

## 17. theme-vivier -- `matrice/data/outils/theme-vivier/`

> Registre des THEMES de mission de la Matrice (genere depuis le moule
> templates/theme-bdd). Le vocabulaire canonique que le pilote embarque
> dans ses injections (`themes_utiles`) ; source fondee : themes reels
> de l'historique M-001 a M-038 (les phrases vrac d'avant etaient le
> signal du besoin de canonisation).

| Verbe | Commande |
|---|---|
| `ajouter` | `python main.py ajouter --nom "NOM" --but "..." [--description "..."]` |
| `lire` | `python main.py lire [--nom "NOM"]` |
| `retirer` | `python main.py retirer --id "TH-XXX"` (ou `--nom "NOM"`) |
| `verifier` | `python main.py verifier` |

**Themes poses** : BDD, OUTIL, ROUTINE, INDICES, CONTRATS, PILOTE, TEMPLATES, REPARATION (TH-002 a TH-009, chacun fonde sur ses missions de preuve).
**Consommation pilote** : depuis M-042, le champ theme du pilote est FERME sur ce vivier (charger / lot / transformer refusent hors vivier) -- le vivier devient la source canonique des themes de mission.
**Quand** : avant de charger une mission (choisir SON theme dans le vivier), a chaque nouveau type de mission recurrent (l'ajouter au vivier fonde sur ses preuves).

## 18. machine-defcon -- `matrice/data/outils/machine-defcon/`

> Machine d'etats defcon (M-059) : le niveau courant vit dans le classeur-variables
> (cle `defcon`, id V-002 conserve). Echelle FERMEE : 5 = stop agent unique /
> optimus-prime reveille + session-matrix mise EN PAUSE (M-080 : la pause est
> declenchee AUTOMATIQUEMENT par `monter --niveau 5`, porte pause-session),
> 4 = suivi de bout en bout, 3 = surveiller puis valider, 2 = normal,
> 1 = reserve (jamais atteint). A defcon 5, seules les missions themees DEFCON
> restent injectables (garde posee dans le pilote : charger, transformer, injecter).

| Verbe | Commande |
|---|---|
| `lire` | `python main.py lire` (etat + echelle + dernieres transitions) |
| `monter` | `python main.py monter --niveau <3-5> --raison "..."` (montee libre, sauts permis) |
| `descendre` | `python main.py descendre --niveau <cible> --raison "..."` (stricte : 5->4, 4->3) |
| `valider` | `python main.py valider --raison "..."` (clot def3 : 3 -> 2 uniquement) |

**Protections** : la descente 3 -> 2 passe UNIQUEMENT par `valider` (la validation clot la periode de surveillance) ; descente stricte UN echelon a la fois ; `--raison` obligatoire ; ecriture atomique + empreinte du classeur maintenue ; journal des transitions `defcon-historique.jsonl` (append-only, surveille par l'espion).
**Quand** : a la reception d'une demande `[alerte]` (variante detaillee `[alerte=defcon:N]`, convention des crochets v3), pour suivre la mise en securite (def4 = suivi de bout en bout), et pour clore une periode de surveillance (`valider`).

## 19. bilan-periode -- `matrice/data/outils/bilan-periode/`

> Bilan LECTURE SEULE des BDD horodatees sur une periode fermee (M-061).
> Sources : historiques-missions, usages-outils-combos, activites-recentes,
> defcon-historique. La demande `[bilan]` de la convention des crochets
> passe par cette porte. La section usages porte les stats par outil-commande :
> appels, repartition des codes, duree moyenne et max (sac-a-dos, M-077).

| Verbe | Commande |
|---|---|
| `bilan` | `python main.py bilan --periode <1h|heures|24h|3j|semaine|mois>` (heures = 6 h, mois = 30 jours) |

**Protections** : periode FERMEE (refus code 2 hors liste) ; lecture seule (n'ecrit jamais, aucune empreinte touchee) ; source absente ou cassee = section vide (jamais bloquant) ; lignes cassees des journaux ignorees.
**Quand** : a la reception d'une demande `[bilan]`, avant une revision strategique, pour verifier ce que la Matrice a fait sur une periode.

## 20. editer-agents-md -- `matrice/data/outils/editer-agents-md/`

> L'outil de la session-matrix (v3) : comme la v1 (activer-agent-principal)
> et la v2 (jarvis) ont leurs outils pour modifier AGENTS.md dans leur encart,
> la Matrice a le sien (M-074). Il ne touche JAMAIS au reste du fichier :
> uniquement le bloc delimite `<!-- session-matrix:DEBUT/FIN -->` (garde
> structurelle : hors bloc, octet par octet preserve -- sinon REFUS).

| Verbe | Commande |
|---|---|
| `etat` | `python main.py etat` (encart actuel + empreinte) |
| `definir` | `python main.py definir --nom-llm <id> --agent <nom> --raison "..."` (creation OU maj idempotente) |
| `verifier` | `python main.py verifier` (marqueurs apparies + empreinte reelle vs etalon `data/agents-md-empreinte.txt`) |

**Flux v3 grave dans l'encart** : la Matrice accueille au demarrage -> l'operateur fait sa demande -> la Matrice lance le cameleon pour sa mission (serie stricte). L'outil detecte AGENTS.md par remontee (motif unique `data/commun/racine.py`, L-013) et ecrit de facon atomique (tmp + remplacement, LF).

## 21. Modules partages -- `matrice/data/commun/` (M-076)

> Pas un outil (pas de main.py) : les DEUX briques que tout outil de la Matrice
> consomme. Le motif racine et le sac a dos vivent ICI -- jamais recopies
> (M-076 : 5 duplications supprimees, 15 outils + 2 templates equipes).

| Module | Role | Consommation |
|---|---|---|
| `racine.py` | L'UNIQUE `detecter_racine(depart)` : remonte jusqu'au dossier portant AGENTS.md (pattern v1, L-013) | dans un `constants.py` : `sys.path.insert(0, str(REPERTOIRE_DATA / "commun"))` puis `from racine import detecter_racine` et `RACINE = detecter_racine(REPERTOIRE_OUTIL)` |
| `sac_a_dos.py` | `envelopper(principal, arguments)` : chronometre, execute, puis note l'usage (outil, verbe, code, duree ms) dans la BDD usages PAR L'OUTIL bdd-usages (porte unique). Echec de notation jamais bloquant. Garde : bdd-usages ne se note jamais lui-meme | dans un `main.py` : `sys.exit(envelopper(principal, sys.argv[1:]))` |
| `lancement.py` | `lancer_invisible(chemin, arguments, script="main.py")` : lancement DETACHE SANS AUCUNE FENETRE (E-056 : Windows CREATE_NO_WINDOW + SW_HIDE, POSIX start_new_session), retourne (pid, duree_ms). L'UNIQUE facon de lancer un processus de fond -- fini les fenetres qui clignotent | dans un relanceur : `from lancement import lancer_invisible` (voir routines/vie) |

**Regle de naissance** : tout nouvel outil (y compris via `dupliquer-template`) nait EQUIPE -- le motif et le sac a dos sont dans les moules `templates/outil-bdd` et `templates/theme-bdd`. Une note sans tag `sac-a-dos` dans la BDD usages = ecriture directe hors porte (ecart).

## 22. Activateur de vie + server matrice -- `matrice/routines/vie/` (M-081)

> Le server de demarrage a 2 etages (E-056) : **server matrice**
> (`server_matrice.py`, boucle de fond invisible) possede le lancement de
> toutes les routines -- **server routine** : chaque routine est lancee/
> relancee PAR LUI, jamais en direct. Toute routine morte est relancee
> automatiquement, SANS AUCUNE FENETRE console (motif partage
> `data/commun/lancement.py`), en ~1 ms (preuve M-081).

| Commande | Effet |
|---|---|
| `python routines/vie/main.py etat` | etat des boucles (ARRET / ACTIVE / fantome nettoye) |
| `python routines/vie/main.py activer` | lance les boucles arretees (detache invisible) |
| `python routines/vie/server_matrice.py` | DEMARRE le server matrice (boucle de surveillance, intervalle 60 s) |
| `python routines/vie/main.py server arret` | arret cooperatif du server (drapeau, jamais de kill) |
| `python routines/vie/main.py server etat` | etat du server matrice |

## 23. journal-multi-encarts -- `matrice/data/outils/journal-multi-encarts/` (M-079)

> Le VISUEL des metriques de la Matrice (v3, E-049) : un NOUVEAU fichier
> `matrice/journal-multi-encarts.md`, propre a la v3 -- il ne remplace rien
> et ne touche JAMAIS aux fichiers v1/v2 (regle versions-intangibles).
> Genere depuis les BDD, jamais edite a la main (comme une vue).

| Verbe | Commande |
|---|---|
| `construire` | `python main.py construire` (regenere le journal complet, ordre ferme des encarts) |
| `lire` | `python main.py lire` (journal entier) ; `python main.py lire --encart <nom>` (UN encart ; inconnu -> code 2) |

**Encarts (ordre ferme, jamais en vrac)** : matrice (defcon + boucles), missions (en cours + vrac/files/brin), routines (dernieres passes veille), alertes (veille + intercom), cameleon (messages RECUS par le cameleon, M-080), optimus (8 derniers evenements de la trace, M-084), usages (8 derniers appels), modifications (5 derniers fichiers), lecons (5 dernieres), variables (classeur). Chaque encart est present meme vide -- aucune entree en vrac. Format createur (M-080) : chaque encart porte SA ligne de FLUX (d'ou viennent les infos, vers ou elles vont) + un TABLEAU `| Entree | Heure | Date |` (heure et date separees, format HH:MM:SS JJ/MM/AAAA, jamais en debut de ligne).

## 24. pause-session -- `matrice/data/outils/pause-session/` (M-080)

> Protocole de pause session-matrix (decisions createur) : LA MATRICE UTILISE
> LE CAMELEON, jamais l'inverse (regle `matrice/regles/matrice-utilise-cameleon.md`).
> Pause = cameleon arrete, mission sauvegardee A LA PAUSE SEULEMENT (etat
> serialise `data/session-matrix-etat.json`, sortie de la file du pilote),
> notification "maintenance" (la raison reelle n'est JAMAIS divulguee).
> La reprise restore A L'IDENTIQUE (meme mission, meme place dans la file).

| Verbe | Commande |
|---|---|
| `pause` | `python main.py pause [--raison "..."]` (manuel `[pause]` ou defcon 5 auto) |
| `reprendre` | `python main.py reprendre` (apres maintenance user + optimus ; restore + notifie) |
| `etat` | `python main.py etat` (montre l'etat de pause s'il existe) |
| `perimetre` | `python main.py perimetre --zones "a,b"` (reduit la lecture cameleon ; vide = restaure) |
| `journal` | `python main.py journal` (10 derniers evenements pause/reprise) |

**Protections** : REFUS si pause deja posee (pas de pause double) ; REFUS de reprendre si une mission est en cours (serie stricte) ; pendant la pause, le pilote REFUSE toute injection/enchainement (garde `session_en_pause`) et la fin HORS lot ne relance rien ; defcon 5 declenche la pause AUTOMATIQUEMENT (raccord dans machine-defcon `monter`) ; perimetre tenu dans le classeur-variables (cle `perimetre-cameleon`, ecriture atomique + empreinte) ; journal `data/pauses-session-matrix.jsonl` (append-only). Boite cameleon : `intercom/cameleon/inbox.jsonl` (etancheite : raison "maintenance" seulement).
**Quand** : demande `[pause]` (maintenance manuelle avec optimus), defcon 5 (mise en securite totale), ou reprise apres maintenance.

## 25. trio marbre BDD -- `matrice/data/outils/bdd-{regles,conventions,protocoles}-matrice/` (M-082)

> Domiciliation du marbre Matrice (E-051) : les regles, conventions et protocoles
> DE LA MATRICE vivent en 3 BDD separees (un outil par BDD, nes du moule
> `outil-bdd`). Ecriture : optimus seul (hors session-matrix, en maintenance).
> Lecture : Matrice + cameleon. Les marbres d'optimus restent dans `_operateur/`
> (versions-intangibles, intouchables).

| Outil | BDD | Contenu |
|---|---|---|
| `bdd-regles-matrice` | `data/bdd-regles-matrice.json` | R-001/R-002/R-003 (matrice-utilise-cameleon, perimetre, langue) |
| `bdd-conventions-matrice` | `data/bdd-conventions-matrice.json` | C-001..C-005 (0 valeur en dur, ascii, outils structure, sac-a-dos, crochets) |
| `bdd-protocoles-matrice` | `data/bdd-protocoles-matrice.json` | P-001..P-003 (routes cameleon, protocoles 6-7-8) |

**Interface** (identique pour les 3) : `ajouter --entree "..." --tags "..."` / `lire [--tag ...]` / `verifier`. Espion : les 3 BDD sont surveillees (registre integrite).
**Quand** : toute nouvelle regle/convention/protocole de la Matrice passe par ces outils (plus aucun fichier markdown de marbre dans `matrice/`).

## 26. suivi-optimus -- `matrice/data/outils/suivi-optimus/` (M-084)

> Trace de suivi d'optimus-prime (GO createur) : le createur ne peut pas le
> voir travailler (optimus invisible dans la v3), cette trace note L'AGENT
> (decisions, portes, missions, pourquoi) -- le sac-a-dos note les OUTILS,
> jamais de recouvrement. Trace append-only + etalon SHA-256, ecrite par
> optimus seul (porte unique), le cameleon n'y accede JAMAIS (zone `suivi-optimus`
> exclue du perimetre-cameleon, regle gravee dans sa fiche).

| Verbe | Commande |
|---|---|
| `noter` | `python main.py noter --mission M-XXX --theme SUIVI --action <action> --detail "..." [--fichiers "a,b"] [--portes "a,b"] [--duree-s N]` |
| `lire` | `python main.py lire [--mission M] [--action a] [--n N]` (filtres + n derniers) |
| `verifier` | `python main.py verifier` (integrite SHA-256, etalon-or) |

**Actions fermees (enum, anti-bruit par EVENEMENT)** : `debut`, `fin`, `porte`, `depot`, `decision`, `decouverte`, `bilan` -- hors enum refusee (code 2). Format d'une ligne : `date, mission, theme, action, detail, fichiers[], portes[], duree_s`. Encart `optimus` au journal multi-encarts (8 derniers evenements, vue lecture seule).
**Quand** : a chaque action significative d'optimus (GO/arbitrage, fin de mission, porte utilisee, depot au vrac, decouverte d'audit, bilan).
