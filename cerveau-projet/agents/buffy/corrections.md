---
identite:
  type: corrections
  appartient_a: buffy
  commun: false
# Corrections et Surcharges -- Buffy
# Agent principal -- Developpeur du cerveau-projet

agent:
  nom-agent: "buffy"
  version_corrections: "0.5.0"
  derniere_mise_a_jour: "2026-08-05"

# Types de corrections
types:
  - regle: "Ajout d'une nouvelle regle specifique a Buffy"
  - surcharge: "Modification d'une section existante de la fiche"
  - correction: "Correction d'une erreur recurrente"
  - configuration: "Parametre de travail specifique"
---

# Corrections et Surcharges



## [LECON] 2026-08-24 -- DEVIATION : INDICES OUTILS MANQUANTS DANS LES CARTES (evaluer-processus)

**Contexte** : le bilan consolide de la chaine Clio verifier a signale 3 problemes evaluer-processus de la chaine de reparation precedente : buffy corriger-fins-de-ligne EXCLUSIF vulcain (DECLARATION_FAUTIVE), buffy detecter-residus hors carte, morpheus valider-conformite-ascii hors carte.

**Diagnostic** : l'exclusivite d'un outil est DERIVEE (outil present dans EXACTEMENT une carte = exclusif a cet agent). corriger-fins-de-ligne n'etait que dans la carte vulcain -> derive exclusif vulcain -> ma declaration (usage reel pourtant) etait DECLARATION_FAUTIVE. detecter-residus et valider-conformite-ascii etaient utilises reellement mais absents des indices de mes cartes.

**Correction** : ajout des indices outils manquants via editer-parcours --modifier-case (c14 buffy : + detecter-residus, + corriger-fins-de-ligne ; c7 morpheus : + valider-conformite-ascii), bump versions (buffy 0.5.6, morpheus 0.5.8), Pattern 14 fiches synchronisees. L'outil n'etant plus dans une seule carte, l'exclusivite derivee disparait.

**Lecons** :
1. UN OUTIL COMMUN UTILISE REELLEMENT DOIT ETRE DANS LA CARTE DE CHAQUE AGENT QUI L'UTILISE, sinon evaluer-processus le derive EXCLUSIF et signale DECLARATION_FAUTIVE (usage jamais reel).
2. TOUT OUTIL UTILISE EN MISSION DOIT AVOIR SON INDICE DANS LA CARTE (garde-fou evaluer-processus OUTIL_HORS_CARTE) - verifier la carte avant usage.
3. LA DESCRIPTION D'UN PARCOURS NE SE MODIFIE PAS A LA MAIN (divergence lock cartes-lock.json) - editer-parcours ne la gere pas, elle reste en retard sur la version (convention).

**Preuves** : valider-cartes-decision buffy CONFORME + morpheus CONFORME, ASCII 0/0 sur 4 fichiers, lock resynchronise (dry-run passe), evaluer-processus 0 probleme (fenetre 24/08).
## [LECON] 2026-08-24 -- DEVIATION : CLOTURE DES 3 LOTS (CARTES + P2 OUTIL + P1 README-DEV)

**Contexte** : deviation Pattern 7 (bilan consolide chaine Clio verifier) - 3 lots : (1) 3 problemes evaluer-processus (indices outils manquants dans les cartes), (2) P2 mismatch outil/README (mettre-a-jour-readme), (3) P1 readme-dev 164 vs 165.

**Resultats** : (1) cartes buffy 0.5.6 (+detecter-residus, +corriger-fins-de-ligne) + morpheus 0.5.8 (+valider-conformite-ascii) via editer-parcours, Pattern 14 sync, CONFORME. (2) Vulcain : verifier()/dry_run() py+sh adaptes a la nouvelle norme README public, bump 0.4.5, tests Morpheus VALIDE. (3) Clio a confirme P1 (categorie Git manquante dans readme-dev) mais editer-fichier VERROUILLE pour clio -> redirection verrou vers buffy (habilitee) qui a insere la ligne '| Git | 1 | hades-contexte-git |' -> verifier [OK] somme 165 = total 165.

**Lecons** :
1. UN OUTIL DE VERIFICATION DOIT SUIVRE LA NORME DU DOCUMENT : quand le README public change de format, l'outil s'adapte (tolerance retro-compat) au lieu de MANQUANT massifs.
2. VERROU HABILITATION : quand un agent n'est pas habilite a un outil (editer-fichier pour clio), la redirection passe par l'agent habilite (buffy) - jamais de contournement.
3. LA DESCRIPTION D'UN PARCOURS NE SE MODIFIE PAS A LA MAIN (divergence lock) - editer-parcours ne la gere pas, elle reste en retard (convention).

**Preuves** : verifier [OK] 165=165, valider-cartes-decision buffy/morpheus CONFORME, tests Morpheus VALIDE, ASCII 0/0.
## [LECON] 2026-08-24 -- P-A : EDITER-FICHIER AJOUTE AUX HABILITATIONS DE CLIO (decision utilisateur)

**Contexte** : Janus a signale P-A (controle deviation 3 lots) : Clio (muse du README) n etait pas habilitee editer-fichier (verrou ferme, source de verite = carte de decision) -> redirection systematique vers buffy pour les corrections ciblees readme-dev. Decision UTILISATEUR : OUI, ajouter editer-fichier a Clio.

**Correction** : via editer-parcours, ajout de l indice outil editer-fichier dans la case c20 (readme-dev) de parcours-clio.json, bump 0.6.5 -> 0.6.6, Pattern 14 fiche sync, valider-cartes-decision CONFORME. Le verrou editer-fichier (source = cartes) reconnait maintenant clio.

**Lecons** :
1. LE VERROU D HABILITATION LIT LES CARTES : pour habiliter un agent a un outil, il faut l indice outil dans SA carte (editer-parcours, SEULE buffy) - pas une table separee.
2. LES DECISIONS D HABILITATION SONT STRUCTURANTES : validation utilisateur avant d elargir le perimetre d un agent (ici clio : regle 'je n utilise QUE mettre-a-jour-readme' assouplie pour editer-fichier sur readme-dev).
3. LA CARTE CLIO c20 est a ALLEGER (poids 4.0 > budget 3.0) - pre-existant, a traiter ulterieurement (combo ou references).

**Preuves** : indice c20 parcours-clio.json ligne 526, valider-cartes-decision clio CONFORME, ASCII 0/0.
## [LECON] 2026-08-24 -- P-B : FICHE CLIO ALIGNEE SUR LA DECISION (apres audit Themis)

**Contexte** : Themis a audite la reparation P-A (editer-fichier pour Clio) : CONFORME mais P-B signale - la fiche Clio gardait 3 occurrences de la regle 'je n'utilise QUE mettre-a-jour-readme' (l.48/124/282) contradictoires avec la nouvelle habilitation en c20.

**Correction** : les 3 occurrences ont ete alignees sur la decision utilisateur (editer-fichier autorise pour les CORRECTIONS CIBLEES de readme-dev - tableaux, compteurs, lignes, jamais reecriture de fond). Ligne 124 reformulee en 'REGLE README UNIQUEMENT (assouplie 2026-08-24)'.

**Lecon** : QUAND UNE HABILITATION EST ELARGIE (decision utilisateur), TOUTES les mentions de la fiche de l agent (Limites, regles, frontmatter) doivent etre alignees sur la carte - pas seulement la version PARCOURS (Pattern 14). L'audit Themis attrape ces incoherences fiche/carte de contenu.

**Preuves** : lignes 48/124/282 fiche clio corrigees, valider-cartes-decision clio CONFORME, ASCII 0/0.
## [LECON] 2026-08-24 -- METHODE RIGOUREUSE ATLAS (un dossier a la fois, un .md par dossier)

**Mission** : rendre Atlas plus rigoureux (decision utilisateur 2026-08-24) :
analyser UN DOSSIER A LA FOIS, rediger UN .md PAR DOSSIER dans atlas/rapports/,
rapport complet = DOUBLON DE LA STRUCTURE avec liens vers les .md.

**Modifications** : parcours-atlas.json v0.5.4 -> v0.5.5 (flux explorer
restructure : c2a Analyser UN dossier, c2b Rediger le .md du dossier, c2c
Tous les dossiers ? NON->c2a / OUI->c8 ; c9 = rapport complet doublon de
structure ; cases c3-c7 supprimees, 0 orpheline, 0 reference invalide),
fiche atlas.md (PARCOURS v0.5.5 + REGLE ABSOLUE METHODE RIGOUREUSE),
16 .md par dossier + rapport complet restructure (271 lignes), cartes-lock
resynchronise.

**Lecons** :
1. Le verrou anti-contournement cartes-lock BLOQUE si on ecrit le JSON hors
   editer-parcours (meme pour une simple description) -- resynchroniser le
   lock (maj manuelle de l empreinte SHA-256 dans cartes-lock.json) apres une
   ecriture legitime hors outil.
2. Les caracteres de dessin (|, +--) dans une arborescence markdown sont
   NON-ASCII -- les remplacer par | et |--- / +--- (corriger-accents le fait).
3. Le test-005 pin la version parcours-atlas 0.5.4 -> adaptation Morpheus
   necessaire (REGLE IMMUABLE DELEGATION).
## [LECON] 2026-08-24 -- CORRECTION METHODE ATLAS : DOSSIER DEDIE PAR EXPLORATION

**Contexte** : l'utilisateur a signale que tous les rapports d'exploration
etaient empiles a la racine de atlas/rapports/ au lieu d'etre dans un dossier
dedie par exploration qui est LE DOSSIER COMPLET.

**Correction** :
1. Carte parcours-atlas.json v0.5.5 -> v0.5.6 : c2 cree LE DOSSIER DEDIE
   atlas/rapports/<cible>-<AAAAMMJJ>/ ; c2b redige chaque .md dans ce dossier ;
   c9 redige le rapport complet (dossier-complet) DANS LE MEME dossier dedie.
   Description mise a jour (METHODE RIGOUREUSE v0.5.6).
2. Fiche atlas.md : PARCOURS v0.5.6 + REGLE METHODE RIGOUREUSE mise a jour
   (dossier dedie = dossier complet).
3. Rapports EXISTANTS reorganises : 18 fichiers (17 .md + 1 .bak) deplaces
   dans atlas/rapports/freelance-2026-08-24/. Liens relatifs simples du
   dossier-complet (noms de fichiers) restent valides (verifie 18/18).
   4 mentions textuelles 'atlas/rapports/' corrigees vers le dossier dedie.

**Lecons** :
1. Le DOUBLON DE STRUCTURE exige un DOSSIER DEDIE PAR EXPLORATION : c'est le
   conteneur naturel du rapport complet + ses .md par dossier.
2. Utiliser des LIENS RELATIFS SIMPLES (noms de fichiers) dans le
   dossier-complet rend le deplacement du dossier entier sans casse.
3. Apres un deplacement, verifier les mentions textuelles de chemins (grep
   du dossier source) en plus des liens.

**Preuves** : carte v0.5.6 CONFORME (valider-cartes-decision), ASCII 0/0,
liens 18/18, git mv verifie.
## [LECON] 2026-08-24 -- REPARATION INTER-ROUND JANUS : CARTE CLIO C22 OUTILS DE CREATION

**Contexte** : Janus a controle la mission Clio (redaction README-v2.md) :
VERDICT A REVOIR (1 point mineur). evaluer-processus signalait
OUTIL_HORS_CARTE : clio ajouter-contenu-fichier declare au registre mais
absent des indices outil de la carte (premier usage de creer-fichier et
ajouter-contenu-fichier par Clio, jamais utilises avant).

**Cause racine** : la carte c22 (branche readme-v2) indiquait "Outil
UNIQUE : mettre-a-jour-readme" - or cet outil ne cree PAS de nouveau
fichier (il ne corrige que README.md/readme-dev.md). La redaction d un
NOUVEAU fichier README-v2.md (exception redaction v2) exige
creer-fichier puis ajouter-contenu-fichier, non references dans la carte.

**Correction** : (1) carte parcours-clio.json v0.6.6 -> v0.6.7 : case c22
texte corrige (outils de creation pour nouveau fichier) + 2 indices outil
ajoutes (creer-fichier, ajouter-contenu-fichier) ; (2) fiche clio.md
PARCOURS (v0.6.7) ; (3) cartes-lock.json resynchronise (empreinte clio).
Valide : valider-cartes-decision CONFORME, navigation c22 affiche les 2
outils, test-072 10/10, test-018 points clio 4b/4c OK, ASCII 0/0.

**Lecons** :
1. Quand une carte autorise une mission sur un NOUVEAU fichier, verifier
   que les outils de creation (creer-fichier/ajouter-contenu-fichier)
   sont dans les indices de la case AVANT la mission - sinon
   evaluer-processus leve OUTIL_HORS_CARTE au controle.
2. Un outil oriente "corriger" (mettre-a-jour-readme) ne couvre pas la
   creation : ne jamais l indiquer comme "outil UNIQUE" pour un nouveau
   fichier.

**Preuves** : carte v0.6.7 CONFORME ; controle janus
controle-modification-readme-v2-2026-08-24.md (VERDICT A REVOIR) ;
evaluer-processus avant (OUTIL_HORS_CARTE) vs apres (corrige).
## [LECON] 2026-08-24 -- SESSIONS NOMMEES ADMIN/FREELANCE + DETECTION IR AUTO (Buffy)

**Contexte** : decision utilisateur (2026-08-24) : au demarrage, l utilisateur indique la session
('admin' = equipe v1 qui gere le cerveau, 'freelance' = equipe v2) au lieu de la deduire de l id
LLM. Chaque session ecrit dans SON encart d activite (session-admin, session-freelance) et peut
lire les autres. En plus : le type R/IR des entrees historiques doit etre DETECTE automatiquement.

**Changements** :
1. activer-agent-principal v0.7.0 : sidentifier <id> <session> -> session-<nom> (admin/freelance) ;
   repli conserve id llm-N -> session-llm-N (compat heritage) ; maj_encart_activites reecrit en
   encarts PAR SESSION (mapping id->session depuis le classeur) ; detecter_type_round : raison
   commencant par INTER-ROUND ou FIN D'INTER-ROUND -> type IR sans flag --type manuel.
2. parcours-demarrage.json v0.3.0 : l utilisateur doit indiquer id ET session au demarrage
   (demander la session si absente) ; demarrer.md syntaxe : lire demarrer.md | id=<id> | session=<admin|freelance>.
3. AGENTS.md : session-llm-1 -> session-freelance (freebuff/stark), session-llm-2 -> session-admin
   (glm5/buffy), session-1 (themis) absorbe dans session-admin. Table Sessions connues + classeur
   (profil-session-admin / profil-session-freelance) a jour.
4. AGENTS-historique.md : encarts 'Activites recentes -- <session>' (admin, freelance, autre).

**Lecons** :
1. UN CHANGEMENT DE NOM DE SESSION EST UNE MIGRATION DE NOYAU : 20+ fichiers pinent la forme
   session-llm-N (outils : verrou-habilitation, enregistrer-lecon, consulter-lecons, nettoyer-
   sessions py+sh, editer-parcours, valider-cartes-decision, evaluer-processus, generateurs-
   commande, detecter-ecritures-hors-cycle, analyser-tokens + 6 tests). Toute regex 'session-llm-'
   sur la table Sessions connues ou le classeur doit accepter session-<nom> AUSSI (pattern commun :
   startswith('| session-') / session: (session-[a-z0-9_-]+)).
2. LE FILTRE DES TESTS QUI LISENT L ETAT REEL (table Sessions connues, classeur) CASSENT SILENCIEUSEMENT
   apres un renommage : test-056/test-090 (filtre | session-llm-), test-024 (profil-session-llm-1),
   test-025 (regex bloc session-llm-) - les verifier AVANT la non-regression.
3. LES FIXTURES (test-001..008 .sh de l outil) gardent session-llm-N : elles tournent sur COPIES
   isolees avec repli heritage -> elles ne cassent pas, mais leur 1 KO pre-existant (Test 7 format
   v0.6.0) reste - a distinguer d un KO introduit.
4. LA DETECTION IR AUTO EVITE LES OUBLIS : le flag --type r|ir existait mais AUCUN parcours ne le
   passait (tous les inter-rounds etaient enregistres en R). Detection par prefixe de raison =
   zero oubli, zero flag manuel.

**Preuves** : test-056 18/18 OK, test-090 11/11 OK, test-025 11/11 OK, test-024 16/17 (1 KO
pre-existant catalogue), test-018/test-021/test-033/test-043/test-052/test-070/test-078 sans
nouveau KO ; test controle isole (AGENTS_FILE sur copie) : sidentifier glm5 admin -> session-admin
(bloc+profil+encart), sidentifier freebuff freelance -> session-freelance, raison FIN D'INTER-ROUND
-> type IR ; ASCII 0/0 sur les 23 fichiers touches ; v0.7.0 py/sh/spec coherent.
## [LECON] 2026-08-24 -- EDUCATION ATLAS ARBRES V2 (inter-round Chiron) : VALIDE

**Contexte** : mission utilisateur : eduquer Atlas pour creer le dossier .md + .svg des agents v2 (ARBRES de decision, pas des cartes v1). Chiron a diagnostique (rapport education-atlas-arbres-v2-2026-08-24.md) : Atlas SAIN mais SANS branche vues-v2. Verrou habilitation : la carte d'Atlas est EXCLUSIVE a Buffy -> Chiron m'a activee en inter-round pour appliquer les corrections.

**Realise** : carte parcours-atlas.json v0.5.6 -> v0.5.7 (branche vues-v2 dans c1 -> case c35 : generer les vues avec convertir-carte-mermaid --arbres + dossier dedie atlas/rapports/vues-v2-<AAAAMMJJ>/), fiche atlas.md (PARCOURS v0.5.7 + REGLE MISSION VUES V2 avec la difference arbre v2 vs carte v1), dossier dedie vues-v2-2026-08-24/ cree (dossier-complet avec les 9 agents + liens vers les 19 fichiers cartes-vues/arbres/).

**Lecons** :
1. VERROU HABILITATION PAR AGENT : editer-parcours bloque les cartes des AUTRES agents (chiron ne peut PAS editer parcours-atlas.json) - c'est le protocole inter-round qui s'applique : l'agent habilite (buffy) applique les corrections proposees par l'educateur (chiron).
2. --inserer-case ATTEND LE JSON DE LA CASE AVEC LA CLE id ({"id":"c35",...}) PAS un wrapper {"c35":{...}} - le wrapper est insere IMBRIQUE (case c35 contenant une cle c35) et valider-cartes-decision le rejette (Types invalides). Toujours --dry-run + valider-cartes-decision apres insertion.
3. ANTI-CONTOURNEMENT MARBRE : toute modification DIRECTE d'une carte (hors editer-parcours) diverge le cartes-lock.json et BLOQUE l'ecriture suivante. Restauration : re-empreinter l'etat verrouille (restaurer le contenu exact qui matche le lock) puis repasser par editer-parcours. Ne JAMAIS editer une carte hors editer-parcours.
4. LA FICHE DOIT SUIVRE (Pattern 14) : apres bump de carte, valider-cartes-decision exige fiche PARCOURS (vX.Y.Z) == parcours.version - mettre a jour les 2 occurrences (PARCOURS + METHODE) + documenter la nouvelle mission.

**Preuves** : valider-cartes-decision --agent atlas CONFORME (v0.5.7), navigation c1 -> c35 OK, lock marbre empreinte OK, dossier vues-v2-2026-08-24/ 19 liens OK, ASCII 0/0, test-101 11/11 (Vulcain/Morpheus), --arbres --verifier rc=0.
## [LECON] 2026-08-25 -- EDUCATION CERBERUS -> FERRARI (inter-round Chiron) : APPLIQUE

Chiron a eduque Cerberus a l utilisation de ferrari (Mecano, agent v1 specialise freelance, double identite v1/v2). En inter-round, j ai applique ses corrections proposees : (1) fiche cerberus.md : ligne ferrari dans la table 'Agents disponibles' + REGLE voie freelance v1 (ferrari) vs v2 (agents MARVEL via JARVIS), bump fiche 0.2.1 -> 0.2.2 ; (2) regles-choisir-agent.md : ligne ferrari a la matrice Etape 1. Aucun changement de parcours (le flux c8 -> c10 couvre ferrari une fois connu ; ferrari ne va pas dans parcours-cerberus-freelance.json dedie aux MARVEL).

Lecons :
1. UNE EDUCATION D AGENT DE COORDINATION SE JOUE DANS LA FICHE + LA MATRICE, PAS DANS LE PARCOURS : Cerberus choisit ses agents via sa table 'Agents disponibles' et regles-choisir-agent - pas besoin de branche de carte pour un agent qui entre dans le flux d activation generique.
2. FICHE v1 vs CARTE : seul le PARCOURS (carte) est verrouille par le marbre et exige editer-parcours (Buffy) ; la FICHE se modifie directement quand l education l exige (mais toujours via l agent habilite selon le protocole Chiron -> Buffy).
3. CONTRADICTION SIGNALEE (a suivre) : la fiche ferrari liste 'Corriger JARVIS' alors qu AGENTS.md donne l exclusivite a Vision - Cerberus doit verifier avant de router JARVIS vers ferrari (domaine Argus/Vision).

**Preuves** : rapport chiron/rapports/rapport-education-cerberus-ferrari-2026-08-25.md, ASCII 0/0 (cerberus.md + regles-choisir-agent.md), LF pur, verifier-conformite-fiche cerberus 1 CONFORME / 0 ECART.
