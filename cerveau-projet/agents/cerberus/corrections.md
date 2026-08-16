---
identite:
  type: corrections
  appartient_a: cerberus
  commun: false
# Corrections et Surcharges -- Cerberus
# Point d'entree unique de chaque session

agent:
  nom-agent: "cerberus"
  version_corrections: "0.2.0"
  derniere_mise_a_jour: "2026-08-05"

# Types de corrections
types:
  - regle: "Ajout d'une nouvelle regle specifique au coordinateur"
  - surcharge: "Modification d'une section existante de la fiche"
  - correction: "Correction d'une erreur recurrente"
  - configuration: "Parametre de travail specifique"
---

# Corrections et Surcharges

## Regles specifiques

| Regle | Description |
|---|---|
| **Toujours commencer par l'ecoute** | Ecouter d'abord, decider ensuite |
| **Toujours documenter l'activation** | Chaque activation doit etre documentee dans AGENTS.md |
| **Exiger la fin conforme a la carte** | Chaque agent termine selon SA carte (Pattern 8) : reactiver Cerberus si activation directe, activer le suivant si maillon de chaine |
| **Ne jamais sauter Cerberus** | Aucun agent ne peut etre active sans passer par Cerberus |

---

## Surcharges

| Section | Modification |
|---|---|
| `agent.role_principal` | Toujours actif en debut de session |
| `communication.ton` | Professionnel et accueillant -- premier contact |

---

## Philosophie de relecture

| Philosophie | Description |
|---|---|
| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |

---

## Corrections d'erreurs

| Erreur | Correction | Statut |
|---|---|---|
| Activer sans comprendre | TOUJOURS poser des questions avant de decider | En cours |
| Oublier de documenter | TOUJOURS mettre a jour AGENTS.md AVANT de passer la main | En cours |
| Ne pas exiger le retour | La fin suit SA carte (Pattern 8) : activation directe = reactiver Cerberus, maillon de chaine = activer le suivant, dernier maillon = reactiver Cerberus avec bilan consolide | Corrige (2026-08-09) |
| **Executer seul une mission d'outil (faute grave 2026-08-06)** | **TOUJOURS activer Vulcain pour creer/modifier/tester/optimiser un outil. La mission Optimiser un outil est dans ma carte de decision. Jamais de travail technique solo.** | Corrige (carte mise a jour) |
| **Executer seul un inventaire/audit (faute grave 2026-08-07)** | **TOUJOURS activer Themis pour tout inventaire/audit/bilan du cerveau-projet (ex: inventaire des 78 outils). La mission Inventaire / audit est dans ma carte. Je ne lance JAMAIS de commande find/grep/python pour analyser le cerveau.** | Corrige (carte mise a jour) |

---

## Defaillance grave -- 2026-08-06

**Ce qui s'est passe** : pendant les passages V2 successifs, Cerberus a execute seul la creation, la correction et la promotion de 26 outils (scripts, tests reels, historique) au lieu d'activer Vulcain.

**Pourquoi** : la carte de decision de Cerberus ne contenait pas de mission "Optimiser un outil" -> la demande d'optimisation n'activait aucune ligne, et Cerberus a improvise en executant. `regles-choisir-agent.md` etait obsolet (ere Buffy/Atlas) et ne mentionnait pas Vulcain.

**Consequence** : aucun second controle Janus, aucune mise a jour README par Clio, aucun retour d'agent documente.

**Correction structurelle** :
1. Mission "Optimiser / faire evoluer un outil (activer Vulcain)" ajoutee a ma carte de decision
2. `regles-choisir-agent.md` reecrit avec la matrice complete des agents (Vulcain = outils)
3. Cette defaillance est documentee ici pour rester en memoire

**Regle absolue pour toujours** : je ne travaille jamais seul sur une mission technique. J'active l'agent dedie.

---

## Defaillance grave -- 2026-08-07

**Ce qui s'est passe** : en reponse a une demande d'"inventaire final des 78 outils", Cerberus a lance lui-meme les commandes de recensement (find, py_compile, parite .sh/.py/.md) au lieu d'activer Themis.

**Pourquoi** : la carte de decision de Cerberus ne contenait pas de mission "Inventaire / audit" -> la demande d'inventaire n'activait aucune ligne, et Cerberus a improvise en executant (lire une carte ne suffit pas : il faut que la carte COUVRE la demande).

**Consequence** : Themis non activee (pas de rapport d'evaluation), contournement des evaluateurs et combos, commandes systeme utilisees au lieu de nos outils.

**Correction structurelle** :
1. Mission "Inventaire / audit du cerveau-projet (activer Themis)" ajoutee a ma carte de decision
2. `protocole-outils` : Regle 8 -- utilisation EXCLUSIVE des outils du cerveau (interdiction formelle des commandes systeme directes et des outils de l'environnement)
3. `protocole-technologies` : Etape 6 -- choix de la version d'un outil (.py si Python dispo, sinon .sh) via le profil systeme stocke dans le classeur
4. Cette defaillance est documentee ici pour rester en memoire

**Regle absolue pour toujours** : je ne travaille jamais seul sur un inventaire ou un audit. J'active Themis.

---

## Configuration

```yaml
preferences:
  format_sortie: "Markdown"
  niveau_detail: "Standard"
  style_reponse: "Ecoute puis decision"
  toujours_ecouter: true
  documenter_activations: true
  exiger_retour: true
```

---

## [LECON] 2026-08-08 -- demarrer.md devient un LANCEUR (parcours de demarrage)

**Tache** : corriger le probleme du 2e LLM (Kilo) qui lisait demarrer.md mais n'executait PAS sidentifier (il restait au resume au lieu d agir).
**Lecons** :
1. PROBLEME : demarrer.md etait un fichier PASSIF (a lire) alors que l identification est une ACTION (a executer). Un LLM tiers fait ce qu'on lui demande litteralement : lire -> il resume. La transition instructions lues -> commande lancee ne se fait pas automatiquement.
2. SOLUTION (decision utilisateur) : demarrer.md doit avoir une CARTE DE DECISION comme le reste du cerveau -> creation du PARCOURS DE DEMARRAGE (cerveau-projet/demarrage/parcours-demarrage.json, 8 cases, identite parcours commun) : c0 question honnete -> c0b relire -> c0c contexte temps reel -> c1 S'identifier (sidentifier <mon-id>) -> c2 verifier son bloc dans AGENTS.md (controle OUI/NON) -> c3 devenir Cerberus -> c4 attendre mission -> c5 fin active (lancer le parcours de l agent).
3. demarrer.md devient un LANCEUR : il NE SE LIT PAS, il SE LANCE. Son contenu = la commande guider-parcours.py parcours-demarrage.json + l explication des 5 etapes.
4. PATTERN 4 respecte : case_depart=c0, question avec memoire + SANS relire (majuscules comme les 11 parcours), branches OUI->c0c / INCERTAIN->c0b / NON->c0b, c0b->c0c->c1. PATTERN 2 : regle ASCII en tete des indices de c1 (case qui ecrit dans AGENTS.md). PATTERN 5 : fin c5 ACTIVE (message = action de relais), pas de fin passive.
5. La boucle de validation : navigation OUI (PARCOURS TERMINE), navigation NON (relire puis TERMINE), --liste 8 cases, ASCII 0, detecter-impacts lit l identite, migrer-identite le marque DEJA (schema hybride operationnel sur le nouveau fichier).
6. PIEGE TEST : les greps sensibles a la casse faussent l audit des patterns (MEMOIRE vs memoire) -- toujours comparer en minuscule pour verifier les mots de la spec.
7. PIEGE ACTIVATION : les caracteres () dans la raison de reactiver-agent-principal cassent le parsing (Parametres manquants) -- utiliser des raisons sans parentheses.

---

## [LECON] 2026-08-08 -- Verifier la carte de l agent avant d accepter sa reactivation (chaine Pattern 8)

**Tache** : corriger la violation de la carte de Vulcain (mission etendre verifier-documents-manquants v0.3.0) : Vulcain a reactive Cerberus directement au lieu d activer Morpheus comme l ordonnait sa fin c15 (MORPHEUS ACTIVE pour les tests).
**Lecons** :
1. PROBLEME : quand un agent delegue termine et reactive Cerberus, je n ai PAS verifie que cette reactivation etait conforme a SA carte. Or le Pattern 8 (chaine bout-en-bout) ordonne que le maillon ACTIVE le suivant a SA fin (Vulcain -> Morpheus -> Janus -> Cerberus). La reactivation directe de Cerberus par un maillon dont la carte dit ACTIVER LE SUIVANT est une ANOMALIE qui coupe la chaine (le maillon suivant ne fait rien).
2. LA CARTE EST LA SOURCE DE VERITE DE LA FIN : avant d accepter le retour d un agent, verifier QUELLE fin sa carte ordonne pour la mission executee (grep fin du parcours-<agent>.json ou --liste) : fin = reactiver Cerberus (activation directe, conforme) OU fin = J ACTIVE <suivant> (chaine, la reactivation directe est alors une violation).
3. PIEGE DOUBLE FAUTE : en reactivant Cerberus, j ai fait d une pierre deux coups : (a) j ai accepte la violation de la carte de Vulcain, (b) j ai court-cuite Morpheus et Janus. La reparation = reactiver la chaine au maillon manquant (activer Morpheus) et documenter l ecart.
4. REGLE POUR TOUJOURS : a CHAQUE reactivation d un agent delegue, verifier la fin de SA carte pour la mission executee avant de considerer la mission terminee. Si la carte ordonne d activer le suivant, relancer la chaine (activer le maillon) au lieu de clore.

---

## Connexions

| Fichier | Role |
|---|---|
| `cerberus.md` | Ma fiche principale |
| `AGENTS.md` | Fichier dynamique -- je le maintiens |
| `../../index-cerveau.md` | Point d'entree du cerveau |
## [LECON] 2026-08-09 -- ARRET TECHNIQUE D'AGENT : commandes bash trop complexes dans les spawns

**Constat** : pendant la mission Morpheus (correction du test generateurs-case), Morpheus
s'est arrete avant d'activer Janus. L'activation a ETE RETROUVEE au tour suivant (22:53,
trace AGENTS-historique) -- la chaine Vulcain -> Morpheus -> Janus -> Cerberus a ete
completee sans coupure. Mais l'arret apparent etait reel : 3 appels d'outils consecutifs
ont echoue avec 'Invalid parameters for spawn_agents ... JSON Parse error'.

**Cause racine** : les commandes bash de verification etaient trop complexes pour le
parametrage des outils de spawn :
- guillemets imbriques : python3 -c "...open('...')..." dans une commande bash
- chemins MSYS (/tmp/...) a l'interieur du CODE python (non convertis par bash)
- echappements multiples (guillemets + backslashes + apostrophes) qui cassent le JSON
  du parametre 'command'

Ces echecs repetes ont coupe le tour de l'assistant AVANT qu'il ne termine la mission
(lecon + activation de l'agent suivant).

**Regle operationnelle** : quand une commande bash contient des guillemets imbriques,
des chemins MSYS dans du python inline, ou des echappements multiples :
1. NE PAS inliner la commande dans le spawn : ecrire un SCRIPT .py temporaire
   (.zz-*.py) et ne lancer que 'python3 .zz-script.py' dans le spawn.
2. Pour les chemins /tmp dans du python, convertir via cygpath -m en variable
   (BASE_WIN=$(cygpath -m "$BASE")) AVANT, jamais en dur dans le code.
3. Apres 1 echec de spawn, changer de methode immediatement (script .py) au lieu de
   re-tenter la meme forme : 3 echecs = arret du tour.

**Preuve** : le tour suivant (continue utilisateur) a complete la mission avec succes
en utilisant la methode script .py. Le piege cygpath est aussi documente dans la lecon
Morpheus (TEST GENERATEURS-CASE CORRIGE 28/28).

## [LECON] 2026-08-09 -- GARDE-FOU RELECTURE FICHE : RAISON D'ACTIVATION (Cerberus, parcours v0.3.1)

**Constat utilisateur** : quand je passe le relais a un agent, il relit SES corrections mais SAUTE la fiche et la question c0 (relecture). La regle AGENTS.md ("SA fiche ET SES corrections") et le protocole-activation l'exigent, mais rien ne le FORCAIT dans la RAISON d'activation.

**Cause racine** : le defaut est dans l'EXECUTION - quand je joue l'agent, je m'arrete a "je relis mes corrections" et je vais directement a la mission sans naviguer c0 (question honnete) ni lire la fiche.

**Correction (garde-fou choisi par l'utilisateur)** :
1. Parcours cerberus c6 (Activer l'agent habilite) + c10 (Activer l'agent) : nouvel indice regle "GARDE-FOU RELECTURE : ordonner dans la RAISON d'activation : RELIS TA FICHE PUIS TES CORRECTIONS avant de commencer." (116 car, 3 indices max respecte).
2. Protocole-activation : garde-fou documente a 2 endroits (Etape 3 Relecture + section La mission) : la RAISON commence TOUJOURS par la mention relecture fiche.
3. Version parcours cerberus 0.3.0 -> 0.3.1 + fiche cerberus.md mise a jour (Pattern 14).

**Lecon technique** : generateurs-case editer --indice-regle REMPLACE les indices au lieu de les AJOUTER (j'ai ecrase c6/c10 a 1 indice, restaure depuis HEAD puis ajout manuel en append). Toujours verifier le nombre d'indices apres un editer.

**A partir de maintenant** : CHAQUE activation (script .tmp-activer-*.py) doit inclure dans la RAISON : "RELIS TA FICHE PUIS TES CORRECTIONS avant de commencer." - et quand je joue l'agent, je commence par c0 (question honnete) puis fiche + corrections.

## [LECON] 2026-08-12 -- CERBERUS A COURT-CIRCUITE SA PROPRE CARTE c15b/c15c : PROBLEMES SIGNALES MAIS PAS CORRIGES (Cerberus)

**Constat utilisateur** : apres la chaine detecter-cablages-manquants (Vulcain -> Morpheus -> Janus -> Cerberus), le rapport Janus signalait 2 problemes a resoudre (regenerer-catalogue bloque par generateurs-ligne cles dupliquees ; badge README reecrit a 126 par concurrence multi-session). Cerberus a rendu le bilan a l utilisateur et attendu sa prochaine mission au lieu d activer l agent habilite - exactement le comportement que la lecon Janus du jour condamnait (activer immediatement quand un rapport signale un ecart).

**Cause racine (3 couches)** :
1. CLASSIFICATION ERRONEE : j ai etiquete les 2 problemes "hors perimetre de la mission" -> donc "plus tard". Or la case c15b de MA carte dit explicitement "defauts hors mission, observations, corrections demandees" - la carte ne distingue PAS perimetre/non-perimetre. Probleme signale = OUI = activation immediate.
2. REFLEXE DE PASSIVITE : en fin de chaine j ai rendu la main a l utilisateur ("en attente de ta prochaine mission") au lieu de suivre le flux de controle de ma carte (c15 -> c15b -> c15c).
3. RECEPTION FAIBLIE : la transmission etait parfaite (rapport ecrit, lecons, bilan) - c est la RECEPTION qui a failli : Cerberus a recu le rapport mais n a pas execute sa propre case.

**GARDE-FOU A GRAVER** : a chaque retour de Janus (ou de tout agent de controle), je lis le rapport PUIS je reponds a la question de la case c15b : "problemes a resoudre ?" - si OUI, j active l agent habilite TOUT DE SUITE (c15c), meme si les problemes sont "hors perimetre" de la mission initiale. Le cycle ne se referme que si CERBERUS execute SA carte - pas seulement si les agents transmettent bien. Un probleme signale qui reste "a corriger plus tard" est un ecart pre-existent en train de naitre.
## [LECON] 2026-08-12 -- GARDE-FOU C1 : DECLENCHEUR AMELIORATION (Cerberus)

**Contexte** : demande utilisateur d ameliorer la qualite pro des outils simples (editer-fichier et al.). Le parcours avait deja la branche ameliorer (c1 -> c1b -> generateurs-amelioration) mais elle ne s est JAMAIS declenchee : la case c1 n avait AUCUN indice -> classification libre -> demande classee inventaire (autre -> c18) au lieu d ameliorer.

**Cause racine** : meme trou que c15b - la case existe mais rien ne force l execution. c1.indices = [] (vide). Le generateur d amelioration (generateurs-amelioration, theme ameliorer-outil 14 questions) existait deja.

**Garde-fou ajoute (carte v0.4.3)** : indice GARDE-FOU C1 (151 car) : toute demande d ameliorer/optimiser un outil -> branche ameliorer -> c1b -> generateurs-amelioration AVANT d activer l agent habilite. Une demande qui commence par une liste mais vise une amelioration = ameliorer, PAS autre.

**Complement** : themes-amelioration.json - le theme ameliorer-outil n avait pas de champ agent_habilite (pourtant attendu par c19d) -> ajoute : agent_habilite=vulcain (constructeur d outils).

**Lecon a graver** : a chaque demande utilisateur, verifier SI la carte a une branche dediee (lire c1 et ses branches AVANT de classer). Ne jamais classer par defaut en autre/inventaire si une branche specifique existe.

## [LECON] 2026-08-13 -- CERBERUS N EXECUTE JAMAIS LES TESTS LUI-MEME (derive du gardien)

**Contexte (demande utilisateur)** : l utilisateur a remarque que j avais lance la non-regression complete moi-meme pour mesurer le nouveau temps (round performance, 43.8s) alors que ce n est pas mon role. Question : probleme dans ma carte ?

**Diagnostic (veridique)** : MA CARTE EST CORRECTE. Aucun outil de test n y est assigne (0 occurrence de tester-lancer-non-regression, chrono, reference dans mes cases). Mes outils sont : lire-fichier, lire-activite-recente, lister-agents, activer-agent-principal, generateurs-amelioration, enregistrer-usage-outil. La carte prevoit EXACTEMENT ce cas : c5 Identifier l agent habilite -> c6 Activer l agent habilite. La derive vient de MON EXECUTION : j ai utilise un outil hors carte (tester-lancer-non-regression = domaine Morpheus ; modification du lanceur = domaine Vulcain/Morpheus) au lieu de suivre ma carte c5/c6.

**Bonne chaine** : demande de mesure -> c5 identifier -> MORPHEUS (testeur dedie : ecrire et EXECUTER des tests) lance la non-regression -> Morpheus active JANUS (controle) -> Janus reactiver Cerberus avec le bilan.

**Lecon a graver** : CERBERUS COORDONNE, IL N EXECUTE PAS. Toute operation de test (lancer la non-regression, chrono, reference, mesurer) est le domaine de MORPHEUS (creation/execution de tests) et JANUS (controle croise). Si un besoin ne correspond a aucun de mes outils assignes, c est que l agent habilite doit etre active (c5/c6), jamais que je dois contourner avec un outil hors carte. Meme derive que Morpheus (la fin suit la carte, jamais la consigne) mais cote gardien : l outil suit la carte, jamais le reflexe.

## [LECON] 2026-08-13 -- AUDIT COMMANDES COMBOS : AUCUN ECART (Cerberus)

**Audit** (demande utilisateur) : verifier les 52 commandes des combos et corriger celles qui ne quotent pas leurs variables. RESULTAT : AUCUN ECART - les 8 commandes non conformes avaient deja ete corrigees par la mission test-042.

**Observations** :
- 51 commandes outil dans 14 definitions (22 commandes entieres {var} legitimes, 21 sans variable, 8 corrigees -> 0 non quote restante).
- Les {BLUE}/{RED}/{NC} des .sh sont des variables bash ${...} (couleurs ANSI), PAS des interpolations de combos - ne pas les quoter.
- Les entrees des cases generateur passent par composer_valeur qui quote si espace ou quoter:true - le mecanisme existe deja (5 parametres quotes).

**Lecon** : avant de corriger, VERIFIER si le travail a deja ete fait - l audit confirme que la mission precedente (test-042) avait boucle le cycle documenter/corriger/surveiller. Un garde-fou de non-regression rend ce type d audit trivial : si test-042 est vert, il n y a rien a corriger.


## [LECON] 2026-08-14 -- BILAN CONSOLIDE SANS PREUVES DOCUMENTAIRES : THEMIS/JANUS N ONT PAS DOCUMENTE L AUDIT HERMES (Cerberus)

**Contexte** : demande utilisateur "verifier que Themis a audite et Janus a valide la creation de Hermes".
Verification documentaire : AGENTS-historique contient bien le bilan consolide (19:45, Cerberus actif), mais
NI Themis NI Janus n ont documente le moindre audit/controle de la creation d Hermes (aucune lecon, aucun
rapport mentionnant hermes dans leurs dossiers). Le bilan consolide que Janus a redige reprenait les resultats
de Morpheus (test-046 10/10, README 13 agents) SANS controle croise reel : c est exactement la derive deja
denoncee ("Themis se contente de resultats").

**Action corrective** : verification reelle faite par Cerberus point par point (J1-J9) :
- J1 fiche hermes CONFORME (verifier-conformite-fiche) + parcours v0.1.0 CONFORME (valider-cartes-decision)
- J2 README public 1x Hermes + readme-dev 13 agents / 13 parcours / 132 outils + outil reference 3x
  (readme-dev, index-tools, catalogue)
- J3 test-046-hermes-fautes : 10 OK / 0 KO
- J5 registre actif seul (historique absent) avec 12 entrees script-temporaire
- J6 detecter-usage-scripts-temporaires : les 3 mentions "historique" sont des commentaires de suppression
  (pas de reference au fichier supprime)
- J7 lanceur : purger_registre present, archiver_registre SUPPRIME
- J4 non-regression 47 OK / 0 KO (lancee en tant que Janus, tour precedent)
=> VERDICT : les FAITS sont tous verts, mais le PROCESSUS documentaire etait absent.

**Lecon** : un bilan consolide ne doit JAMAIS affirmer un verdict VALIDE sans les preuves documentaires des
maillons (lecon + rapport + verdict dans les corrections de chaque agent). Cerberus, a la reception d un bilan,
doit verifier que chaque maillon a documente son controle AVANT d accepter le verdict. Si les preuves manquent,
faire le controle reel avant de valider (ou renvoyer la mission).


## [LECON] 2026-08-14 -- BANNISSEMENT OUTILS TIERS MECANISE (test-047) + RESIDUS CRLF CORRIGES (Cerberus)

**Contexte** : demande utilisateur "mecaniser le bannissement des outils tiers : detecter-usage-outils-externes
systematique en fin de mission avec KO si traces". La REGLE ABSOLUE 4 (utiliser UNIQUEMENT les outils du cerveau)
etait DECLAREE mais pas MECANISEE : l outil detecter-usage-outils-externes existait mais aucun test ne le
lancait, et de vrais residus CRLF etaient restes (buffy/corrections.md 3035 lignes CRLF, clio 316, rapports,
version-readme.txt) -- traces de mes propres ecritures Python sous Windows.

**Actions** :
1. CORRECTION des 6 residus CRLF reels (corriger-fins-de-ligne) : buffy/clio corrections.md, 2 rapports
   maj-readme-massive, version-readme.txt, analyse-externe.md
2. OUTIL v0.1.1 : liste EXCLUSIONS_PAR_DEFAUT (fichiers volontairement non conformes : dictionnaires d accents/
   emojis, exemples de tests pedagogiques, docs-dev externes fournis par l utilisateur) + option --exclure MOTIF
   (python). Parite .sh + doc a jour.
3. GARDE-FOU test-047 (10 points, template v0.3.0, protections importees, triplet chrono) : outil au catalogue +
   index-tools, scan cerveau-projet -> 0 suspect (KO si traces), exclusions couvrent les fichiers volontaires,
   anciens residus propres, ASCII + LF.
4. LANCEUR : test-047 reference en serie e (48 tests). Non-regression complete 48 OK / 0 KO, chrono 47.3s
   (reference mise a jour).

**Lecon** : une regle n existe que mecanisee. La REGLE ABSOLUE 4 etait connue de tous et pourtant des traces
d outils externes dormaient dans les fichiers depuis des jours : c est le test qui attrape, pas la volonte.
Tout outil de detection doit avoir son garde-fou dans la non-regression (sinon il n est jamais lance). Et toute
ecriture Python sur Windows doit verifier LF/ASCII immediatement (les CRLF reviennent vite).


## [LECON] 2026-08-14 -- PROTOCOLE FIN-MISSION + GARDE-FOU TEST-048 (lecon + verdict obligatoires) (Cerberus)

**Contexte** : demande utilisateur "renforcer le protocole de fin de mission : chaque maillon doit documenter
son controle avant de transmettre (lecon + verdict obligatoires)". Suite directe de la derive decouverte le
meme jour : le bilan consolide de Janus affirmait "Hermes VALIDE" alors que NI Themis NI Janus n avaient
documente le moindre controle (aucune lecon mentionnant hermes dans leurs dossiers).

**Actions** :
1. PROTOCOLE protocole-fin-mission v0.1.0 (regles-immuables/general/) : 7 sections, regle AUCUNE TRANSMISSION
   SANS LECON + VERDICT, reference dans index-regles-general.
2. GARDE-FOU test-048 (8 points, template v0.3.0, protections importees, triplet chrono) : protocole existe +
   reference + regle presente, chaque mission recente d AGENTS-historique a sa lecon dans corrections.md,
   chaque lecon recente contient un verdict (VERDICT/VALIDE/CONFORME/A REVOIR/PROPRE/KO, insensible casse),
   missions TEST / entrees Cerberus exclues, ASCII + LF.
3. CORRECTIONS REVELEES PAR LE TEST : les lecons Clio du 2026-08-14 n avaient AUCUN verdict (5 lecons) ->
   completees avec **Verdict** : VALIDE. Les lecons Hygie contenaient deja "Verdict final : PROPRE" mais le
   regex initial ne les matchait pas -> elargi (insensible casse + PROPRE).
4. LANCEUR : test-048 reference en serie e (49 tests). Non-regression complete 49 OK / 0 KO, chrono 46.0s.

**Lecon** : la mecanisation revele les vraies lacunes (les lecons Clio du 14 etaient incompletes et personne
ne l avait remarque). Un protocole sans garde-fou reste une intention ; le test-048 rend la documentation du
controle verifiable a chaque non-regression. Desormais toute mission recente sans lecon ou sans verdict fait
KO avant que le bilan consolide ne soit accepte.


## [LECON] 2026-08-14 -- VERIFICATION CARTES : CASE LECON OBLIGATOIRE AVANT TRANSMISSION (Cerberus)

**Contexte** : demande utilisateur "verifier que les cartes des agents incluent une case lecon+verdict
obligatoire avant transmission" (suite du protocole-fin-mission + test-048).

**Scan des 13 cartes** : 12 cartes avaient deja une case "Lecons et retour" / "Ajouter les lecons dans
corrections.md" avant la fin. VULCAIN etait le SEUL agent SANS AUCUNE case lecon (53 cases, 0 mention).

**Actions** :
1. PARCOURS VULCAIN v0.4.6 -> v0.4.7 : insertion de 2 cases action "Ajouter les lecons dans corrections.md"
   - c9h (chemin construire : c22 usages -> c9h lecon -> c9b ameliorations)
   - c15h (chemin modifier : c23 usages -> c15h lecon -> c15b ameliorations)
   Chaque case porte : pattern-2, regle PROTOCOLE FIN-MISSION (lecon + verdict avant transmission,
   test-048 le verifie), outil ajouter-contenu-fichier vers vulcain/corrections.md.
2. FICHE vulcain.md : Pattern 14 PARCOURS v0.4.6 -> v0.4.7.
3. DECOUVERTE CONNEXE (auto-verification) : ma propre declaration d usage `cerberus -> tester-lancer-
   non-regression` (faite lors de la mission test-048) VIOLAIT la regle "seul Janus lance la non-regression"
   (test-037). Retiree du registre -> evaluer-processus 0 probleme, test-035 reverdi 8/8.

**Validations** : valider-case vulcain OK, valider-cartes CONFORME (v0.4.7), detecter-cablages PROPRE
(55 cases atteignables), test-026 10/10, test-035 8/8, non-regression 49 OK / 0 KO (45.9s).

**Lecon** : le scan systematique des cartes a revele que la regle etait appliquee partout SAUF chez un agent -
et que la regle du protocole-fin-mission n existait que depuis aujourd hui. Une verification ciblee (les cases
lecon des cartes) complete le garde-fou test-048 (qui verifie les LECONS ECRITES, pas la PRESENCE de la case
dans la carte). Les deux sont complementaires : la case oblige l agent a suivre le chemin, le test verifie le
resultat. Et un garde-fou m a attrape MOI : j avais declare un usage non conforme (tester-lancer-non-regression
par Cerberus) - la mecanisation fonctionne meme contre l agent qui la cree.


## [LECON] 2026-08-14 -- TEST-037 RENFORCE : SEUL JANUS LANCE LA NON-REGRESSION, MEME DANS LE REGISTRE (Cerberus)

**Contexte** : confirmation utilisateur "themis ne doit pas lancer le test de non-regression, seul janus a ce
pouvoir". La verification a revele un TROU dans le garde-fou : test-037 verifiait les CARTES (aucune carte
hors janus ne contient tester-lancer-non-regression) mais PAS le REGISTRE des usages. C est exactement comme
ca que MA declaration fautive cerberus -> tester-lancer-non-regression (mission test-048) est passee : elle
ne touchait pas les cartes, seul evaluer-processus (test-035) l a attrapee indirectement.

**Actions** :
1. TEST-037 renforce : nouveau point 2b - le registre ne doit contenir AUCUNE declaration de
   tester-lancer-non-regression par un agent autre que janus.
2. PREUVE NEGATIVE (verification reelle) : fausse declaration themis inseree au registre -> point 2b KO
   (5 OK / 1 KO), declaration retiree -> 6 OK / 0 KO. La mecanisation fonctionne.
3. Non-regression complete 49 OK / 0 KO (45.9s, +0% vs reference).

**Lecon** : un garde-fou qui verifie la REGLE (cartes) mais pas les TRACES (registre) laisse passer les
violations declarees : la regle "seul janus" doit etre verifiee sur les DEUX (la carte = le droit, le
registre = l usage reel). Toute regle de gouvernance doit avoir son invariant sur le registre en plus des
cartes. Et la preuve negative (inserer une violation temporaire, constater le KO, la retirer) est la seule
facon de prouver qu un garde-fou attrape vraiment ce qu il doit attraper.


## [LECON] 2026-08-14 -- REGLES DE GOUVERNANCE VERIFIEES SUR LE REGISTRE (test-045 8b/8c) (Cerberus)

**Contexte** : demande utilisateur "verifier que les autres regles de gouvernance (ex: seul Themis audite)
sont aussi verifiees sur le registre, pas seulement les cartes". Apres le colmatage de la regle "seul Janus
lance la non-regression" (test-037 point 2b), audit de TOUTES les regles de gouvernance.

**Cartographie des regles "seul X"** :
1. "SEUL JANUS lance la non-regression" (tester-lancer-non-regression) -> deja couvert carte + registre
   (test-037 point 2b, tour precedent).
2. "SEUL HYGIE est habilite a SUPPRIMER" (supprimer-fichier, supprimer-dossier) : regle documentee dans la
   fiche hygie.md (REGLE ABSOLUE) mais AUCUN garde-fou ne verifiait ni les cartes ni le registre.
3. "Themis audite" : pas de regle "seul Themis" formelle (les outils d evaluation sont partages :
   evaluer-processus est aussi chez janus/vulcain) -> pas de garde-fou a ajouter, l audit n est pas une
   exclusivite.

**Actions** :
1. TEST-045 renforce (10 -> 12 points) :
   - 8b (cartes) : aucun autre agent n a supprimer-fichier/supprimer-dossier dans SA carte
   - 8c (registre) : aucune declaration supprimer-* par un agent autre que hygie
2. PREUVE NEGATIVE (verification reelle) : carte atlas polluee (supprimer-fichier ajoute a c0) -> 8b KO ;
   declaration themis -> supprimer-fichier au registre -> 8c KO (10 OK / 2 KO). Pollution retiree -> 12 OK / 0 KO,
   atlas restaure CONFORME.
3. Non-regression complete 49 OK / 0 KO (45.7s, reference mise a jour).

**Lecon** : chaque regle de gouvernance "seul X fait Y" doit avoir SON invariant double : (1) la carte = le
droit (seul X a l outil dans sa carte), (2) le registre = l usage reel (seul X declare l outil). La regle
Janus/non-regression avait deja ete mecanisee ; la regle Hygie/suppression ne l etait pas et est maintenant
couverte. La preuve negative (inserer une violation, constater le KO, retirer) prouve que chaque invariant
attrape reellement sa violation.


## [LECON] 2026-08-14 -- PREUVE NEGATIVE SYSTEMATIQUE DANS PROTOCOLE-TESTS v0.3.2 (Cerberus)

**Contexte** : demande utilisateur "ajouter une preuve negative systematique au protocole de creation des
garde-fous (inserer une violation, constater le KO)". Les preuves negatives realisees aux tours precedents
(test-037 point 2b, test-045 points 8b/8c) ont prouve leur valeur : un garde-fou qui passe sur l etat sain
peut ne RIEN detecter.

**Actions** :
1. PROTOCOLE-TESTS v0.3.1 -> v0.3.2 : nouvelle etape 4 "Preuve negative OBLIGATOIRE" dans le processus de
   test (inserer UNE violation reelle du type surveille -> constater le KO sur le point dedie -> retirer ->
   constater le vert) + REGLE IMMUABLE PREUVE NEGATIVE + exemple test-037 point 2b + point ajoute a la
   checklist de validation.
2. TEST-044 adapte (point 11 : protocole-tests v0.3.2 + triplet + PREUVE NEGATIVE) -> 14/14 OK.
3. Non-regression complete 49 OK / 0 KO (46.0s, +1% vs reference).

**Lecon** : la preuve negative est la SEULE facon de prouver qu un garde-fou attrape reellement ce qu il doit
attraper. Elle est desormais OBLIGATOIRE (etape 4 du processus de test) : tout garde-fou cree ou renforce
sans preuve negative documentee est considere NON VERIFIE. Les 3 preuves de cette session (janus/non-
regression, hygie/suppression cartes+registre) sont les references a suivre pour tous les futurs garde-fous.


## [LECON] 2026-08-14 -- REGISTRE CUMULATIF (ROTATION 100) : LA MEMOIRE DES USAGES RESTAUREE (Cerberus)

**Contexte** : demande utilisateur "probleme avec l enregistrement des utilisations d outils : soit les
agents ne les utilisent pas, soit il ne sont pas enregistres ? on doit verifier !". L investigation a
revele la VERITE : les agents DECLARAIENT bien leurs usages (l historique supprime contenait 216 usages sur
2 jours : janus 66, morpheus 58, themis 28, buffy 26, vulcain 24, cerberus 11, clio 3) MAIS le lanceur
non-regression purgeait le registre courant a CHAQUE lancement (design round 8 : les usages partaient a
l historique, puis la suppression de l historique a fait que la memoire a disparu). Le registre semblait
vide a l utilisateur alors que les agents faisaient leur travail.

**Decision utilisateur** : (1) registre CUMULATIF jusqu a 100 utilisations (la memoire des usages vit),
(2) les usages historiques hors carte actuelle sont IGNORES (faits passes avant les changements de regles).

**Actions** :
1. LANCEUR : purger_registre remplace par rotation_registre (cumul <= 100 usages normaux, les plus anciens
   retires au-dela ; entrees script-temporaire TOUJOURS preservees, hors plafond). Preuve reelle : registre
   simule 108 lignes (105 normales + 3 scripts) -> rotation -> 100 normales + 3 scripts, anciennes sorties
   (outil-000 retire, outil-104 conserve). Doc .md a jour.
2. RESTAURATION de la memoire : les 216 usages de l historique supprime recuperes depuis git et fusionnes
   dans le registre courant -> apres rotation : 100 usages normaux + 12 scripts (2 jours de memoire : 27
   janus, 29 morpheus, 23 buffy, 21 themis, 3 clio, 2 vulcain, 1 cerberus + 12 scripts hygie/vulcain/
   morpheus/buffy).
3. EVALUER-PROCESSUS v0.1.1 -> v0.1.2 : fenetre de verification = jour courant (FENETRE_JOURS=1, date
   calendaire) : les usages historiques (avant les regles de gouvernance, ex tester-lancer-non-regression
   par buffy/themis/morpheus le 2026-08-13) sont ignores -> test-035 8/8 OK, scan global 0 probleme.
4. TEST-037 point 2b : filtre de date ajoute (jour courant uniquement) pour la regle "seul janus declare
   la non-regression" -> 6/6 OK.
5. Non-regression complete 49 OK / 0 KO (45.5s). Normes 0 non-ASCII / 0 CRLF.

**Lecon** : un registre d usage est une SOURCE DE VERITE : il doit CUMULER (memoire) avec un plafond, jamais
etre vide a chaque passe. La purge totale rendait la journalisation invisible et faussait le diagnostic
("les agents n enregistrent pas" alors qu ils enregistraient). Le cumul a plafond + fenetre de verification
recente repond aux deux besoins : la memoire vit (consultable) et les controles ne verifient que le present
(les faits historiques ne sont pas re-juges avec les regles d aujourd hui).


## [LECON] 2026-08-14 -- MISSION ENTONNOIR : EXECUTER-SCRIPT-TEMPORAIRE (Cerberus)

**Contexte** : demande utilisateur "mission entonnoir : normalisation
transparente des scripts temp avec controle systematique". La boucle ideale
du fichier temporaire : creer -> entonnoir -> executer. Un agent ecrit son
script avec des accents, des retours Windows, un BOM, sans y penser ; le
passage par l entonnoir le normalise automatiquement avant execution. On ne
change pas le comportement de l agent, on adapte le parcours.

**Actions** :
1. OUTIL CREE : executer-script-temporaire v0.1.0 (categorie Executer, 3
   fichiers py/sh/md). ENTONNOIR = 1. NORMALISER (BOM retire, CRLF -> LF,
   accents corriges via le dictionnaire de corriger-dictionnaire-accents),
   2. CONTROLER (compilation Python systematique avant execution - une
   erreur de syntaxe BLOQUE le lancement), 3. EXECUTER (code retour
   transmis). Options : --dry-run (rien n est ecrit ni execute), --dictionnaire,
   --verbose, --chrono, --version. Transparent : script deja conforme =
   execute tel quel (0 modification).
2. CATALOGUE 153 -> 154 (entree executer-script-temporaire, triee) + INDEX
   TOOLS 171 -> 172 (categorie Executer) + test-007 adapte (153/171 -> 154/172)
   + test-024 adapte (153 -> 154).
3. PROTOCOLE creation-scripts-temporaires v0.2.4 -> v0.2.5 : REGLE ENTONNOIR
   (TOUT script temp passe par executer-script-temporaire, jamais de python3
   direct sur un script de tmp-<agent>/) + section dediee + etape EXECUTER.
4. GARDE-FOU test-049 (11 points, protections importees + triplet chrono) :
   catalogue + index + protocole + script sain CONFORME + script corrompu
   normalise (preuve reelle BOM/CRLF/accents) + erreur de syntaxe bloquee +
   --dry-run + --version + PREUVE NEGATIVE (python3 direct laisse la
   non-conformite, l entonnoir corrige) + normes.
5. OUTIL CRITIQUE : executer-script-temporaire integre verifier_residus_racine
   (test-041 passe de 4 a 5 outils critiques, 22/22 OK).
6. FICHE cerberus : executer-script-temporaire ajoute aux P0 (outil de
   support commun, assigne via protocole-outils Regle 6).
7. BUG DECOUVERT : KO intermittent test-038 en pool. Cause racine : le lanceur
   mettait TOUS les tests en parallele, or test-020 (combos-clio) MODIFIE le
   README en reel pendant que test-038 lit le badge -> course. Correction :
   TESTS_SERIE_EXCLUSIFS = [test-020] lances en serie finale avec les
   garde-fous globaux (jamais en parallele avec les lecteurs du README).
8. Non-regression complete : 50 OK / 0 KO (46.6s, +2%, dans la tolerance).

**Lecon** : un point d entree unique (entonnoir) transforme la contrainte de
conformite en automatisme : l agent n a plus a penser aux accents/CRLF/BOM, le
parcours s en charge. La transparence (0 changement de comportement) est plus
efficace que la discipline. Second enseignement : en pool parallele, deux
tests qui touchent le MEME fichier partage (l un ecrit, l autre lit)
produisent des KO intermittents - les tests qui ecrivent doivent etre exclus
du pool et lances en serie finale.


## [LECON] 2026-08-14 -- VERIFICATION DETECTER-RESIDUS + PROTOCOLE-NETTOYAGE (Cerberus)

**Contexte** : demande utilisateur "Verifier que detecter-residus (outil de
detection de Hygie) est bien exclusif et documente dans le protocole de
nettoyage". La verification a revele : (1) la DETECTION n est PAS exclusive
(janus utilise detecter-residus en c21 "Verifier les impacts" - c est un
CONTROLE legitime, il detecte sans supprimer), (2) la SUPPRESSION est bien
exclusive (test-045 8b/8c : seul hygie a supprimer-fichier/supprimer-dossier
dans SA carte et dans le registre), (3) AUCUN protocole de nettoyage global
n existait - protocole-purification ne couvre que les contenus, pas les
residus du workspace.

**Actions** :
1. PROTOCOLE-NETTOYAGE v0.1.0 cree : chaine complete snapshot ->
   detection (detecter-residus par zone) -> verdict -> preuve d honnetete
   (delegation Pattern 5) -> suppression (seul Hygie) -> verification ->
   rapport + rotation. 5 regles immuables dont "DETECTION PARTAGEE,
   SUPPRESSION EXCLUSIVE" (clarifie le cas janus c21). Reference dans
   index-regles-general.md.
2. TEST-045 renforce (12 -> 13 points) : point 8d verifie que
   protocole-nettoyage existe + reference detecter-residus +
   snapshot-nettoyage + "SEUL HYGIE SUPPRIME" + est dans l index.
3. PREUVE NEGATIVE reelle : protocole masque temporairement -> 8d KO
   (12 OK / 1 KO) -> restaure -> 13/13 OK.
4. Non-regression complete : 50 OK / 0 KO (46.5s, +1%).

**Lecon** : une regle de gouvernance documentee uniquement dans la fiche de
l agent n est pas verifiable par les autres. Le protocole global (chaine
complete) + le garde-fou mecanise (point 8d) rendent la regle lisible et
controlee. La distinction detection/suppression est fondamentale : un outil
de DETECTION peut etre partage (controle par d autres agents) sans violer
l exclusivite qui porte uniquement sur la SUPPRESSION.


## [LECON] 2026-08-14 -- REGLE IMMUABLE SEUL HYGIE SUPPRIME DANS REGLES-GROUPES-AGENTS (Cerberus)

**Contexte** : demande utilisateur "Ajouter la regle seul Hygie supprime dans
regles-groupes-agents.md (niveau regle immuable, pas seulement fiche)". La
regle vivait dans la fiche Hygie et le protocole-nettoyage, mais pas au
niveau REGLE IMMUABLE generale - c etait le niveau manquant.

**Actions** :
1. REGLES-GROUPES-AGENTS.md : nouvelle section "Regles de gouvernance
   exclusives (IMMUABLE)" documentant 2 regles au niveau regle immuable :
   a. SEUL HYGIE SUPPRIME (fichiers/dossiers, exclusivite cartes + registre,
      residus PROUVES uniquement, nuance detection vs suppression) avec lien
      protocole-nettoyage + garde-fou test-045.
   b. SEUL JANUS LANCE LA NON-REGRESSION (complementaire, meme niveau) avec
      garde-fou test-037 - coherence de gouvernance.
2. TEST-045 renforce (13 -> 14 points) : point 8e verifie que
   regles-groupes-agents.md contient "SEUL HYGIE SUPPRIME" + "supprimer-
   fichier" + reference au garde-fou test-045.
3. PREUVE NEGATIVE reelle : regle masquee temporairement (HXXIE) -> 8e KO
   (13 OK / 1 KO) -> restauree -> 14/14 OK.
4. Non-regression complete : 50 OK / 0 KO (46.8s, +2%).

**Lecon** : une regle de gouvernance a TROIS niveaux qui doivent etre
synchronises : la fiche de l agent (comportement), le protocole (processus) et
la REGLE IMMUABLE generale (reference pour tous). Le niveau regle immuable est
le seul qui s applique a TOUS les agents : le documenter la rend opposable
au-dela du proprietaire. La mecanisation (point 8e) verifie que le niveau
existe, la preuve negative prouve qu il est controle.


## [LECON] 2026-08-14 -- REGLES EXCLUSIVES CLIO (README) + MORPHEUS (TESTS) AU NIVEAU REGLE IMMUABLE (Cerberus)

**Contexte** : demande utilisateur "Verifier que les autres regles exclusives
potentielles (seul Clio met a jour le README, seul Morpheus ecrit les tests)
sont documentees au niveau regle immuable". La verification a revele :
(1) "SEUL MORPHEUS ECRIT LES TESTS" existait dans protocole-tests (REGLE
IMMUABLE DELEGATION, ligne 217) mais PAS dans regles-groupes-agents.md ;
(2) "SEUL CLIO MET A JOUR LE README" etait une exclusivite de FAIT (outils
combos-maj-readme-massive / combo-maj-readme presents UNIQUEMENT dans la
carte clio) mais AUCUNE regle formelle - ni protocole, ni regle immuable.
Themis c30 ne fait que CONTROLER la veracite (nuance controle vs action).

**Actions** :
1. REGLES-GROUPES-AGENTS.md : section "Regles de gouvernance exclusives"
   completee avec 2 nouvelles regles immuables :
   a. SEUL MORPHEUS ECRIT ET EXECUTE LES TESTS : seul agent a creer/adapter/
      executer les test-XXX.py (delegation Vulcain -> Morpheus -> Vulcain).
   b. SEUL CLIO MET A JOUR LE README : outils de MAJ exclusifs a SA carte ;
      nuance controlee (Themis c30 verifie la veracite, ne met pas a jour).
2. TEST-045 renforce (14 -> 15 points) : point 8f ANTI-RECURRENCE qui
   verifie que TOUTES les regles exclusives (hygie/janus/morpheus/clio)
   sont documentees au niveau regle immuable - une exclusivite vivant
   uniquement dans une fiche ou un protocole n est pas opposable a tous.
3. PREUVE NEGATIVE reelle : regle CLIO masquee temporairement (CLXXO) ->
   8f KO (14 OK / 1 KO, manquante listee) -> restauree -> 15/15 OK.
4. Non-regression complete : 50 OK / 0 KO (47.7s, +4%).

**Lecon** : l audit des exclusivites potentielles a confirme que le NOMBRE de
regles exclusives est maintenant de 4 (hygie supprime, janus non-regression,
morpheus tests, clio readme) - un contre-verite utile : Themis ne met PAS a
jour le README (elle controle), et Vulcain lance test-023 uniquement pour
valider SON outil (il n ECRIT pas la suite). Toute nouvelle exclusivite doit
etre ajoutee a la liste du point 8f pour etre verifiee a chaque
non-regression.


## [LECON] 2026-08-14 -- LIEN CROISE PROTOCOLE-NETTOYAGE <-> REGLES-GROUPES-AGENTS (Cerberus)

**Contexte** : demande utilisateur "Ajouter la reference aux
regles-groupes-agents.md dans le protocole-nettoyage (lien croise
fiche/protocole/regle)". Le protocole documentait la chaine de nettoyage mais
ne referencait pas la REGLE IMMUABLE (regles-groupes-agents.md) qui porte la
regle "SEUL HYGIE SUPPRIME" - la triple synchro fiche/protocole/regle etait
incomplete.

**Actions** :
1. PROTOCOLE-NETTOYAGE : regle immuable 6 ajoutee ("NIVEAU REGLE IMMUABLE" :
   la regle SEUL HYGIE SUPPRIME est documentee au niveau regle immuable dans
   regles-groupes-agents.md, les 3 niveaux sont synchronises) + lien ajoute
   dans la section Liens.
2. TEST-045 point 8e renforce : verifie aussi que le protocole-nettoyage
   referencie regles-groupes-agents.md (lien croise).
3. PREUVE NEGATIVE (2 essais) : le 1er masquage (regles-groupes-agents.mdXX)
   a ECHOUE - la sous-chaine .md restait presente donc "in" retournait Vrai
   (faux negatif de la preuve). Le 2e masquage (regles-groupes-agentsX.md,
   sous-chaine cassee) a fait 8e KO (14 OK / 1 KO) -> restaure -> 15/15 OK.
   Lecon de la preuve : pour masquer une reference, casser la SOUS-CHAINE
   (deplacer le point/extension), pas seulement modifier le nom.
4. Non-regression complete : 50 OK / 0 KO (47.2s, +3%).

**Lecon** : la triple synchro fiche (comportement) + protocole (processus) +
regle immuable (reference pour tous) est complete uniquement quand chaque
niveau REFERENCHE les deux autres. Le lien croise est mecanise par le
test-045 point 8e. Et une preuve negative n est valable que si le masquage
casse reellement la chaine recherchee (sous-chaine, pas nom modifie).


## [LECON] 2026-08-14 -- TRIPLE SYNCHRO FICHE HYGIE COMPLETEE (fiche <-> protocole <-> regle) (Cerberus)

**Contexte** : demande utilisateur "Verifier que la fiche Hygie reference
aussi la regle immuable (triple synchro fiche + protocole + regle)". La
verification a revele que la fiche hygie.md ne referencait NI
regles-groupes-agents.md (niveau regle immuable) NI protocole-nettoyage (son
protocole de reference) - la triple synchro etait incomplete : la regle etait
documentee dans la regle et le protocole, mais la FICHE (le niveau que l
agent lit en premier) ne pointait vers aucun des deux.

**Actions** :
1. FICHE HYGIE.md : section "Protocoles applicables" enrichie avec
   regles-groupes-agents.md (IMMUABLE : regle SEUL HYGIE SUPPRIME) +
   protocole-nettoyage (chaine snapshot -> detection -> suppression, mon
   protocole de reference).
2. TEST-045 point 8e renforce (TRIPLE SYNCHRO) : verifie maintenant les 3
   liens - regle documentee dans regles-groupes-agents.md, protocole qui
   reference la regle, ET fiche qui reference protocole + regle.
3. PREUVE NEGATIVE : 1er essai faux negatif (masquage suffixe X gardait la
   sous-chaine), 2e essai valide (mot remplace par 'autres') -> 8e KO
   (14 OK / 1 KO) -> restaure -> 15/15 OK.
4. Conformite fiche hygie : 1 CONFORME / 0 ECARTS. Carte : CONFORME.
5. Non-regression complete : 50 OK / 0 KO (47.7s, +4%).

**Lecon** : la triple synchro fiche/protocole/regle n est complete que si la
FICHE reference les deux autres niveaux - c est le niveau que l agent lit en
PREMIER, donc le point d entree de la synchro. Le test-045 point 8e verifie
desormais les 3 directions (regle -> protocole, protocole -> regle, fiche ->
protocole + regle). Confirme la regle de preuve negative : pour masquer une
reference, REMPLACER LE MOT (casser la sous-chaine), pas ajouter un suffixe.


## [LECON] 2026-08-14 -- TRIPLET GENERALISE DANS LES OUTILS TEMPORAIRES (Cerberus)

**Contexte** : demande utilisateur "on doit generaliser les protections et les
chrono dans les outils temporaires". Avant : le template genere par
generateurs-outil-temporaire etait un simple main() sans protections ni
chrono - un script temporaire pouvait tourner sans dry-run, sans options
on/off, sans mesure de duree. Le triplet (regle immuable) etait reserve aux
TESTS (template-test v0.3.0) et aux OUTILS DURABLES (protocole-outils Regle 9),
pas aux outils temporaires.

**Actions** :
1. GENERATEURS-OUTIL-TEMPORAIRE v0.1.0 -> v0.2.0 : le template genere
   embarque le TRIPLET complet - PROTECTIONS (verifier_nommage anti-
   renommage, --dry-run, gestion erreur), OPTIONS ON/OFF (--isoler N,
   --desactiver 1,3,5), CHRONO (par defaut, --no-chrono, chrono_etape +
   bilan_chrono). Preuve reelle : script genere 106 lignes avec triplet,
   execution + chrono OK, --dry-run OK, --no-chrono OK, normes 0/0.
   Bug de format corrige : les operateurs % du code GENERE (%.2fs) doivent
   etre doubles (%% %%) pour survivre au formatage du generateur.
2. PROTOCOLE-creation-scripts-temporaires v0.2.5 -> v0.2.6 : REGLE TRIPLET
   (un outil temporaire SANS triplet doit etre regenere avec le generateur
   v0.2.0, jamais ecrit a la main sans protections/chrono).
3. GARDE-FOU test-050 (11 points, protections importees + triplet) :
   version generateur + fonctions template + options + PREUVE REELLE
   (generation + execution + chrono) + --dry-run + --no-chrono + protocole
   v0.2.6 + doc v0.2.0 + normes.
4. PREUVE NEGATIVE (2 essais) : 1er essai (logique interne masquee) n a pas
   touche les points verifies - il fallait retirer une FONCTION du template ;
   2e essai (bilan_chrono -> bilan_chronoX) a fait point 5 KO (10 OK / 1 KO,
   le script genere n affichait plus CHRONO) -> restaure -> 11/11 OK.
5. Doc + spec generateur v0.2.0, versions alignees (detecter-divergences
   ALIGNE). Non-regression complete : 51 OK / 0 KO (46.8s, base 51).

**Lecon** : le triplet n est pas une option des tests - c est la signature de
qualite de TOUT script Python du cerveau, y compris les temporaires. La
generalisation amont (le generateur) vaut mieux que la discipline aval :
un agent qui REGENERE un outil temporaire obtient gratuitement protections +
options + chrono, sans y penser. Preuve de preuve negative : pour montrer
qu un garde-fou attrape sa violation, il faut retirer reellement ce qui est
verifie (une fonction), pas seulement en degrader la logique.


## [LECON] 2026-08-14 -- AUTO-AMELIORATION DU GENERATEUR : string.Template AU LIEU DU FORMATAGE % (Cerberus)

**Contexte** : retour utilisateur "si pour les % tu as du les doubler, il faut
logiquement lancer le parcours auto-amelioration des outils ; si ta commande
devient compliquee, on doit ameliorer notre outil avant tout, c est
imperatif". Le signal : j avais du doubler les %% dans le template du
generateur (formatage % {...}) pour que les operateurs % du code GENERE
survivent - 2 bugs rencontres (docstrings, operateurs non doubles). C etait
une fragilite de l OUTIL, pas une contrainte a contourner.

**Actions (protocole-autoameliorer-outils : diagnostiquer -> ameliorer ->
documenter -> valider RVAV)** :
1. DIAGNOSTIC : le template utilisait `contenu = """...""" % {...}` ->
   tout % du code genere devait etre double (%%), sinon le formatage du
   generateur l interpretait. Fragile (2 bugs) et illisible.
2. AMELIORATION : remplacement par `string.Template` (from string import
   Template) : placeholders $nom/$description/$date substitues par
   .substitute(nom=..., description=..., date=...). Les operateurs % du code
   genere restent LITTERAUX - plus AUCUN echappement, plus AUCUN doublement.
   Verif prealable : aucun $ dans le code genere (string.Template sur).
3. PREUVE REELLE : generation d un outil temporaire -> 0 placeholder
   residuel, execution + CHRONO OK, --dry-run OK, nom de fichier correct,
   normes 0/0. Le code genere est IDENTIQUE au template avant refactor.
4. VALIDATION : test-050 11/11 OK (garde-fou triplet), test-024 14/14,
   non-regression complete 51 OK / 0 KO (48.1s, +3%). Versions alignees
   (detecter-divergences ALIGNE, toujours 0.2.0 - interface inchangee).
5. DOC : le principe du template reste documente (la doc .md ne change pas -
   le triplet etait deja documente en v0.2.0).

**Lecon** : un echappement necessaire (doubler des caracteres) est un SIGNAL
que l outil doit etre ameliore, pas une convention a apprendre. string.Template
est la bonne primitive quand le code genere contient des % (formats) mais pas
de $ : les placeholders ne collisionnent pas avec le code cible. L auto-
amelioration a SUPPRIME la complexite (aucun doublement) au lieu de la
documenter - c est la regle : si l outil devient complique, on ameliore
l outil AVANT de continuer.


## [LECON] 2026-08-14 -- REGLE 10 STRING.TEMPLATE DOCUMENTEE DANS PROTOCOLE-OUTILS (Cerberus)

**Contexte** : demande utilisateur "Documenter la lecon string.Template dans
le protocole-outils (choix de primitive quand le code genere contient des
%)". La lecon de l auto-amelioration du generateur (doublement des %% evite
par string.Template) devait devenir une REGLE IMMUABLE du protocole-outils,
pas seulement une lecon dans corrections.md.

**Actions** :
1. PROTOCOLE-OUTILS : Regle 10 ajoutee "Choix de primitive de template
   (IMMUABLE)" - tableau de decision : code genere contient % ->
   string.Template (les % restent litteraux) ; contient $ -> str.format ;
   ni l un ni l autre -> % {...}. SIGNAL D ALERTE : si la construction
   exige d ECHAPPER des caracteres du code cible (doubler %%, echapper les
   triple-guillemets), c est que la primitive est mal choisie - ameliorer
   l OUTIL, jamais documenter l echappement comme convention. Exemple vecu :
   generateurs-outil-temporaire (%% doubles, 2 bugs) -> string.Template a
   supprime toute la complexite en une operation.
2. TEST-044 renforce (14 -> 15 points) : point 12b verifie que le
   protocole-outils contient la Regle 10 + mention de string.Template.
3. PREUVE NEGATIVE reelle : Regle 10 masquee (10X) -> 12b KO (14 OK / 1 KO)
   -> restauree -> 15/15 OK.
4. Non-regression complete : 51 OK / 0 KO (46.9s, +0%).

**Lecon** : une lecon technique n est durable que si elle devient une REGLE
du protocole de reference (ici protocole-outils) et qu un garde-fou la
verifie. Le tableau de decision (contenu du code genere -> primitive) est la
forme la plus actionnable : l agent choisit la bonne primitive SANS reflechir.
L auto-amelioration du generateur (mission precedente) a fourni la matiere ;
cette mission l a institutionnalisee.


## [LECON] 2026-08-14 -- PARITE .SH DU GENERATEUR : TRIPLET COTE BASH (Cerberus)

**Contexte** : apres la generalisation du triplet (protections + options on/off +
chrono) dans generateurs-outil-temporaire v0.2.0 (cote .py), verification de la
parite .sh : le wrapper bash etait reste en v0.1.0 avec l ANCIEN template
(simple main() sans triplet) - la parite etait CASSEE.

**Corrections** :
1. generateurs-outil-temporaire.sh v0.1.0 -> v0.2.0 : template bash embarque le
   MEME triplet que le .py (verifier_nommage, --dry-run, --isoler, --desactiver,
   --no-chrono, chrono_etape, bilan_chrono).
2. Substitution via environnements (heredoc quote) + normalisation LF (tr -d
   CR) : le heredoc bash produisait des CRLF sur Windows - corrige.
3. test-050 renforce (11 -> 13 points) : point 12 (parite .sh v0.2.0 + triplet
   dans le template bash) + point 13 (PARITE REELLE : script genere par le .sh
   identique a celui du .py, hors date).

**Preuve reelle** : generation .sh -> execution du script genere (CHRONO affiche,
--dry-run, --no-chrono, --isoler) + diff .py vs .sh = PARITE PARFAITE (hors date).

**Preuve negative** : fonction bilan_chrono masquee dans le template .sh ->
points 12 ET 13 KO (11/2) -> restaure -> 13/13 OK.

**Lecon** : a chaque bump de version du generateur, verifier la parite .sh ET
comparer reellement les scripts generes (pas seulement le template) - le garde-fou
test-050 le mecanise desormais.

**Validations** : test-050 13/13, test-044 15/15, non-regression 51 OK / 0 KO
(47.3s, +1%), normes 0/0.


## [LECON] 2026-08-14 -- PARITE .PY/.SH DES GENERATEURS : AUDIT + REGISTRE (Cerberus)

**Contexte** : apres la correction de parite generateurs-outil-temporaire,
verification etendue aux autres generateurs avec parite .py/.sh
(activer-agent-principal, editer-parcours, valider-cartes) + audit general.

**Resultats de l audit** :
1. WRAPPERS (16 outils) : le .sh delegue au .py (exec python3) -> parite
   GARANTIE par construction (valider-cartes-decision, guider-parcours,
   generateurs-ligne, generateurs-regenerer-catalogue, ...). 9/10 --version
   identiques.
2. editer-parcours : PAS de .sh (fichier .py seul) -> pas de parite a verifier.
3. activer-agent-principal : derivee CORRIGEE - le .sh omettait le statut
   dans --version (py affichait "(prepare)", sh non) -> STATUT="prepare"
   ajoute + echo avec le statut. Parite --version retablie.
4. CAS SYSTEMIQUE : 34 .sh AUTONOMES (logique bash dupliquee, pas wrapper)
   avec primaut documentee en .sh dans leur .md. Les 5 outils de fichiers ont
   derive : creer-fichier (py 0.3.1 / sh 0.3.0, interface differente : le .sh
   ne comprend ni --force ni --aide), editer-fichier (0.4.1/0.3.0),
   lire-fichier (0.4.2/0.3.0), ecrire-fichier (0.3.2/0.3.0),
   ajouter-contenu-fichier (0.2.0/0.3.0). Le catalogue (154 commandes) pointe
   100% .py : les .sh ne sont pas utilises par les agents.
5. REGISTRE : 2 declarations fautives retirees (cerberus -> tester-lancer-
   non-regression et cerberus -> generateurs-outil-temporaire, outil absent
   de la carte cerberus) - le point 2b anti-recurrence de test-037 et
   evaluer-processus les signalaient.

**Preuves** : parite reelle squelette-pense-bete .py vs .sh = squelettes
IDENTIQUES (versions 0.2.0/0.2.0-py INTENTIONNELLES, documentees dans la doc);
generateurs-ligne/regenerer-catalogue = wrappers purs; activer --version
identiques apres correction.

**Validations** : test-037 6/6, test-035 8/8, test-024 14/14, test-013 11/11,
non-regression 51 OK / 0 KO (47.7s, +2%), normes 0/0, 0 residu.

**Recommandation** : traiter les 34 .sh autonomes a risque (conversion en
wrapper ou deprecation) dans une mission dediee - le catalogue ne les
utilisant pas, la priorite est basse mais le risque de derive est reel.
## [LECON] 2026-08-16 -- CHRONO EN PREMIERE LIGNE DE L ENTONNOIR (Cerberus)

**Contexte** : demande utilisateur - le chrono des scripts temporaires doit
etre ACTIVE et affiche TOUT EN HAUT de la reponse pour etre vu a chaque
execution. Verification de fonctionnalite.

**Etat reel** : executer-script-temporaire (entonnoir) affichait deja le
chrono PAR DEFAUT en premier dans le code, MAIS avec une sortie piped
(lancement depuis mes outils), le buffer du sous-processus passait DEVANT
et le chrono disparaissait en bas de la reponse.

**Correction** (v0.1.2 -> 0.1.3) : flush immediat (flush=True) apres
l impression du chrono - il est maintenant la PREMIERE ligne visible,
meme en sortie piped. --no-chrono le coupe toujours.

**Preuve reelle** : sortie piped -> premiere ligne = '[CHRONO] 0.00s
(entonnoir)' avant le corps du script.

**Lecon** : 'affiche par defaut en haut' ne suffit pas : sans flush
immediat, l ordre reel des lignes depend du buffering de stdout quand la
sortie est piped. Tout outil qui veut garantir l ordre de ses messages
doit flush() avant de lancer un sous-processus.

## [LECON] 2026-08-16 -- PARCOURS D AMELIORATION NON SUIVI (Cerberus)

**Controle utilisateur** : avant d activer Vulcain pour le round
d amelioration de detecter-troncatures, devais-je passer par le parcours
d amelioration de MA carte ? REPONSE : OUI - et je ne l ai PAS fait.

**Preuves de l ecart** :
1. Ma carte a la case c19c (Pattern 17 : GENERATEUR D ABORD) : lancer
   generateurs-amelioration AVANT d activer l agent habilite.
2. La case c1b porte la regle : 'toute demande d ameliorer/optimiser un
   outil declenche la checklist du generateur d amelioration AVANT
   d activer l agent habilite'.
3. Registre : generateurs-amelioration = 0 occurrence (jamais declare).
4. Le round a ete fait correctement (diagnostic Cerberus, mission Vulcain,
   garde-fou Morpheus, non-regression Janus) MAIS sans la checklist.

**Checklist a posteriori (theme ameliorer-outil, 14 questions)** : 12/14
couverts par le round, 2 non couverts :
- q8 NON : l outil n a PAS de spec/ (les 5 fichiers py/sh/md/spec/catalogue
  ne sont pas tous couverts).
- q2/q3 (anticipation) : non verifies a priori (le round a bien pense aux
  binaires et aux zones de documentation, mais via le diagnostic, pas via
  la checklist).

**Lecon** : pour TOUTE demande d amelioration d outil, lancer
generateurs-amelioration --theme ameliorer-outil AVANT d activer l agent
(Pattern 17, case c19c). La checklist force l anticipation (q2/q3) et la
completude des 5 fichiers (q8). Le generateur a ete lance a posteriori
pour ce round : q8 (spec manquante) est le seul vrai residu.
