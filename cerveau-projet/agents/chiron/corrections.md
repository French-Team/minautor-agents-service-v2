---
famille: cerveau-projet
identite:
  type: corrections-agent
  nom: Chiron
  version: 0.1.0
  date_creation: 2026-08-17
---

# Corrections -- Chiron

> Ce fichier contient les lecons apprises par Chiron au fil de ses missions.
> Chaque lection documente : CONTEXTE, LECON, PREUVES.
## [LECON] 2026-08-18 -- REEDUCATION DE THEMIS : CARTE SAINE MAIS GUIDAGE PEDAGOGIQUE MANQUANT (Chiron)

**Contexte** : session-llm-2 (kilo-llm) - Themis a recu la mission 'Inventaire
et audit des outils de performance' qui ne correspond a aucune branche de sa
case c1. Elle a improvise au lieu de repondre 'autre' -> c21 (hors perimetre),
et a tente editer-parcours (outil reserve a Buffy), bloque 2x par le verrou a
17:44:00. L utilisateur a demande sa reeducation : sa carte est en retard sur
celles de cerberus, vulcain, morpheus et janus.

**Diagnostic** : la carte de Themis est STRUCTURELLEMENT SAINE (verifier-
conformite-fiche CONFORME, detecter-cablages PROPRE 37/37, bumper 149/149
coherent, 0 divergence de version). Le retard est PEDAGOGIQUE :
1. c1 (Mission) n a AUCUN indice de classification - Cerberus a un indice
   regle 'GARDE-FOU C1' qui guide la reponse ; Themis n en a pas. Un LLM ne
   sait pas qu une mission hors branches -> reponse 'autre' -> c21.
2. AUCUNE redirection quand le verrou bloque un outil (message BLOQUE) : la
   carte de Themis ne dit pas de se diriger vers c21 -> c22 (activer l agent
   habilite). Les cartes recentes couvrent ce cas.
3. c21 (hors perimetre) n a aucun indice listant les domaines des autres
   agents (Atlas/Buffy/Vulcain/Morpheus/Hygie/Janus).

**Lecons** :
1. UNE CARTE STRUCTURELLEMENT VALIDE PEUT ETRE PEDAGOGIQUEMENT EN RETARD : les
   verifications de structure (conformite, cablages, versions) passent toutes
   alors que le guidage (indices de classification) manque. L education doit
   verifier le CONTENU des indices, pas seulement la forme.
2. LE GARDE-FOU C1 DE CERBERUS EST LE MODELE : une case de mission doit porter
   un indice regle qui force la classification (branches explicites + cas
   'aucune branche -> autre'). Sans lui, la classification est libre.
3. LE VERROU BLOQUE EST UN SIGNAL DE REDIRECTION, PAS UN ARRET : quand
   proteger-verrou-habilitation bloque un outil, la carte doit ordonner de
   signaler et d activer l agent habilite (c21 -> c22) - jamais de re-tenter
   ni de s arreter (cas observe : 2 tentatives editer-parcours puis arret).
4. CHIRON NE CORRIGE PAS : les 3 corrections proposees (indices c1/c21/c22)
   vont a Buffy (seule habilitee pour editer-parcours). Chiron documente et
   signale, c est le modele Argus.

**Preuves** : verifier-conformite-fiche themis CONFORME, detecter-cablages
themis PROPRE (37/37), bumper --tous 149/149, detecter-divergences 0
DIVERGENTE. Rapport : rapports/rapport-reeducation-themis-2026-08-18.md.

**Verdict** : A REVOIR - 3 corrections de formation proposees (2 hautes,
1 moyenne), signalees a Buffy.
## [LECON] 2026-08-18 -- RE-EDUCATION JANUS : VERDICT A REVOIR (Chiron)

**Mission** : re-education de Janus a la demande de Cerberus (audit Themis
A REVOIR). L utilisateur a observe Janus "suivant sa carte" et se demande
s il a ete eduque.

**Diagnostic** : carte Janus v0.4.20 STRUCTURELLEMENT SAINE (version sync,
51 cases, boucle KO, Pattern 17, fiche CONFORME, bumper 0/0) mais
PEDAGOGIQUEMENT EN RETARD : c1 sans indice GARDE-FOU C1, aucune redirection
"outil bloque", c28 sans indice AGENTS HABILITES. Janus n a JAMAIS ete
re-eduque (seule lecon d education de Chiron = Themis).

**Lecon claire** : UNE CARTE STRUCTURELLEMENT VALIDE PEUT ETRE PEDAGOGIQUEMENT
EN RETARD - le comportement observe (suivre sa carte) est CONFORME, mais la
carte ne couvre pas les cas limites (verrou bloque, classification libre).
La re-education de Themis (v0.4.10) a cree un MODELE DE CONFORMITE
PEDAGOGIQUE applicable a TOUTES les cartes : (a) indice GARDE-FOU C1 en c1,
(b) redirection "outil bloque" -> activer l agent habilite, (c) indice AGENTS
HABILITES. Toute carte d un agent principal doit etre verifiee contre ce
modele - le test pedagogique est de demander : "que fait la carte si le
verrou bloque un outil ? que fait la carte si la demande n est dans aucune
branche ?"

**Verdict** : A REVOIR - 3 corrections proposees, signalees a Buffy (seule
habilitee editer-parcours). CHIRON NE CORRIGE PAS, il documente et signale.
## [LECON] 2026-08-18 -- RE-EDUCATION VULCAIN/MORPHEUS/BUFFY : VERDICT A REVOIR (Chiron)

**Mission** : re-education de 3 agents principaux a la demande de Cerberus
(audit Themis A REVOIR) : les cartes de Vulcain (0.4.28), Morpheus (0.4.15)
et Buffy (0.4.14) sont structurellement saines mais pedagogiquement en retard.

**Diagnostic** : 3 cartes structurellement SAINES (fiches CONFORME, bumper
0/0, versions sync) mais PEDAGOGIQUEMENT EN RETARD : c1 sans AUCUN indice,
pas de redirection outil bloque, pas d indice AGENTS HABILITES. Aucun des 3
n a JAMAIS ete eduque (seules educations : Themis #23, Janus #34).

**Lecon claire** : le retard pedagogique est SYSTEMIQUE chez les agents non
eduques - ce n est pas un cas isole (Themis, puis Janus, puis maintenant 3
agents). Le modele de conformite pedagogique (GARDE-FOU C1, redirection outil
bloque, AGENTS HABILITES) doit etre verifie sur TOUTES les cartes d agents
principaux, pas seulement sur celles signalees par un incident. Le test
pedagogique : "que fait la carte si le verrou bloque un outil ? que fait la
carte si la demande n est dans aucune branche ?" - si la carte ne repond pas,
elle est en retard.

**Verdict** : A REVOIR - 3 cartes a re-eduquer, signalees a Buffy (seule
habilitee editer-parcours). CHIRON NE CORRIGE PAS, il documente et signale.
## [LECON] 2026-08-18 -- RE-EDUCATION CARTES SECONDAIRES : VERDICT A REVOIR (Chiron)

**Mission** : re-education des 10 cartes secondaires a la demande de Cerberus
(audit Themis A REVOIR) : atlas, argus, hygie, clio, hermes, gardien, chiron,
athena, promethee, minerve.

**Diagnostic** : 10 cartes structurellement SAINES (fiches CONFORME, bumper
0/0, versions sync) mais PEDAGOGIQUEMENT EN RETARD : 9/10 sans AUCUN indice en
c1, aucune redirection outil bloque, aucun AGENTS HABILITES. Chiron = cas
particulier (c1 action a mission unique : le GARDE-FOU C1 classique ne
s applique pas ; redirections c10/c11 presentes mais liste AGENTS HABILITES
manquante). Aucun agent secondaire n a jamais ete eduque.

**Lecon claire** : le retard pedagogique est GENERALISE - il touche les 10
cartes secondaires en plus des 6 principales. Le modele de conformite
pedagogique doit s appliquer a l ensemble des 16 cartes avec ADAPTATION pour
les cas particuliers : les agents a mission unique (chiron) n ont pas besoin
du GARDE-FOU C1 classique (c1 de type action) mais doivent avoir la
redirection vers les agents habilites et la liste AGENTS HABILITES. Le test
pedagogique reste : "que fait la carte si le verrou bloque un outil ? si la
mission est hors perimetre ?"

**Verdict** : A REVOIR - 10 cartes a re-eduquer (adaptation chiron), signalees
a Buffy (seule habilitee editer-parcours). CHIRON NE CORRIGE PAS.

## [LECON] 2026-08-18 -- EDUCATION THEMIS COMBOS ASCII (Chiron)

**Mission** : eduquer Themis aux combos/outils ASCII (2e volet demande utilisateur) : sa carte ne reference aucun outil ASCII (0 mention), combo-corriger-ascii jamais utilise (0 usage registre), 8 usages executer-script-temporaire.

**Diagnostic** : la regle ABSOLUE 4/5 de Themis impose les outils du cerveau assignes dans SA carte -- mais aucun outil ASCII n'y est assigne, donc elle ne peut pas en utiliser. Les outils existent : combo-corriger-ascii (definition-combo.json v0.1.0, via combos-moteur) et combos-corriger-non-ascii v0.3.0 (--full : dry obligatoire avant wet, rapport concis complet, wet cible ~3 s).

**Resultat** : rapport d'education (rapport-education-themis-combos-ascii-2026-08-18.md) + lecon BDD. Corrections de carte proposees a Buffy : ajouter combos-corriger-non-ascii dans c9 (ecrire rapport) et c12 (lecons), mentionner les 2 combos dans la fiche.

**Lecons** :
1. UNE REGLE D OUTIL SANS OUTIL ASSIGNE EST INOPERANTE : Themis a la regle ABSOLUE 4/5 mais son parcours n'assigne AUCUN outil ASCII -> elle ne peut pas appliquer la regle. Eduquer = assigner l'outil dans la carte, pas seulement rappeler la regle.
2. UN COMBO JAMAIS UTILISE EST INVISIBLE : combo-corriger-ascii existe mais 0 usage au registre. Un outil non branche dans les cartes n'est pas decouvert. L'education passe par l'indice dans la case (c9 ecriture de rapport).
3. LES SCRIPTS TEMPORAIRES SONT LE SYMPTOME D'UN OUTIL MANQUANT : 8 usages de executer-script-temporaire par Themis = elle contourne car aucun combo ASCII n'est assigne. Diagnostiquer la CAUSE, pas le symptome.
4. CHIRON NE MODIFIE PAS LES CARTES DES AUTRES : je documente (rapport + lecon) et je SIGNALE a Buffy. Mon pilote d'auto-correction ne couvre QUE ma propre carte.

## [LECON] 2026-08-18 -- CYCLE PILOTE AUTO-CORRECTION REEL (Chiron)

**Mission** : verification reelle du cycle pilote d auto-correction de MA carte (demande Cerberus) : detecter une incoherence reelle, me re-eduquer, corriger SA carte via editer-parcours, activer Themis, reprendre.

**Incoherence detectee (c18)** : le texte de la regle annoncait 'A REVOIR -> NON (retour c15)' mais la branche JSON NON allait vers c18 (attente) - le cas A REVOIR n avait AUCUNE branche. En plus, le texte faisait 168 caracteres (> 160).

**Correction appliquee (editer-parcours --modifier-case c18, verrou pilote OK)** : 3 branches explicites : OUI (CONFORME) -> c12 (reprendre), A REVOIR -> c15 (retour corriger), NON (pas revenue) -> c18 (attendre, re-essai legitime). Texte aligne sur les branches (151 caracteres). Lock resynchronise automatiquement.

**Verifications** : navigation c11b OUI -> c15 -> c16, c18 A REVOIR -> c15, c18 OUI -> c12, ASCII 0, LF 0, poids c18 0.25, valider-cartes a faire par agent habilite (verrou session).

**Lecons** :
1. LE CYCLE PILOTE FONCTIONNE DE BOUT EN BOUT : detecter (c11b OUI) -> se re-eduquer (lecon) -> corriger (editer-parcours, verrou SA carte autorise) -> verifier (Themis) -> reprendre (c18). Le verrou pilote m a autorise l ecriture sur MA carte SANS intervention de Buffy.
2. UN TEXTE DE REGLE QUI ANNONCE UNE BRANCHE INEXISTANTE EST UN VRAI DEFAUT : le texte de c18 promettait 'A REVOIR -> c15' mais aucune branche ne menait a c15 - l agent ne pouvait pas executer le cas A REVOIR. La regle : chaque cible annoncee dans un texte de regle de question doit exister dans les branches (et inversement).
3. L ATTENTE EST UNE BOUCLE LEGITIME DOCUMENTEE : NON -> c18 (re-essai) suit le pattern Buffy c8b ('attente legitime du retour de Themis, voulue'). Ce n est pas une boucle d attente interdite (regle 10) car c est un CONTROLE de re-essai documente.
4. TOUTE CORRECTION DE CARTE DOIT PASSER valider-cartes-decision SOUS UN AGENT HABILITE : le verrou m a bloque valider-cartes (artefact de session chiron non habilite) - la validation finale revient a Buffy/Janus/Vulcain/Argus.

---

### Lecon 2026-08-19 -- Janus (controle + catalogue-combos)

Mission catalogue-combos (garde-fou combo -> outils) terminee. 4 enseignements :

1. **Nouvel outil de consultation partage** : tout outil cree dans la categorie consulter (ou diagnostic) et utilise par tous les agents doit etre ajoute a OUTILS_P0_PARTAGES + autorises dans evaluer-processus, sinon test-035 (OUTIL_HORS_CARTE) KO.
2. **Pins de version catalogue** : chaque ajout au catalogue-commandes.json oblige a mettre a jour les pins 182 -> 183 dans test-060, test-007, test-024, test-079 (4 tests, parfois 2 occurrences chacun).
3. **Tri alphabetique strict** : le catalogue doit rester trie (consulter-combos AVANT consulter-lecons : 'combos' < 'lecons').
4. **Invocation evaluer-coherence** : `dossier` = racine du projet (defaut `.`), NE PAS passer `cerveau-projet` en argument sinon le fichier AGENTS.md n'est pas trouve et tous les agents sont declares manquants (faux positif).

---

### Lecon 2026-08-19 -- Vulcain (convertir-carte-mermaid)

Outil cree : convertir-carte-mermaid (consulter), convertit les 16 parcours
JSON en graphes mermaid (.mmd) dans cerveau-projet/cartes-vues/mermaid/. 4
enseignements :

1. **Champ `branches: []` != decision** : certaines cases action/controle ont
   `branches: []` ET `suivant` - tester la NON-vacuite (`if c.get("branches")`),
   pas la presence de la cle, sinon les aretes et la BFS d atteignabilite sont fausses.
2. **Mermaid** : commentaires en `%%` (pas `%`), ne pas mettre de suffixe de
   type apres les noeuds (parseur strict), `suivant: null` (reactiver
   l appelant) -> arete vers un noeud FIN-APPELANT.
3. **L ecriture par str_replace double les backslashes** : pour des regex ou
   des chaines avec `\`, reecrire le fichier entier (write_file) plutot que
   patcher des lignes.
4. **Registre usages** : format date `YYYY-MM-DD HH:MM:SS` (espace, pas de T)
   et jamais d entree avec agent=inconnu (artefact de test) - test-024 (tri)
   et test-079 (agent valide) verifient ces deux points.

---

### Lecon 2026-08-19 -- Morpheus (test-096 cartes-mermaid-garde-fou)

Test garde-fou cree (7/7 OK, 0.2s) pour la synchronisation cartes <-> .mmd.
Enseignements :

1. **Tags taxonomie** : un nouveau test DOIT utiliser uniquement les tags de
   categories-tests.json (44 tags). `mermaid`, `synchronisation`, `cartes`
   n existent pas -> test-087 KO. Tags valides : parcours, outil, garde-fou,
   preuve-negative.
2. **Nouveau test = 4 integrations** : dossier test-NNN + serie du lanceur
   (SERIES) + profil profils-tests.json + tags conformes. Oublier une seule
   -> test-027/063/087 KO.
3. **test-027 points launcher** : les points 5-8 qui LANCENT le lanceur
   sont exclusifs Janus -> KO attendus quand un autre agent execute le test
   (le lanceur refuse). Ce n est pas une regression.
4. **Fichiers generes** : toujours DANS cerveau-projet (cartes-vues/mermaid)
   et ASCII strict + LF pur (le garde-fou le verifie).

---

### Lecon 2026-08-19 -- Janus (controle final convertir-carte-mermaid)

Controle de la mission mermaid. 3 enseignements :

1. **Un test qui appelle un outil journalisant doit passer --agent** : le
   point 5 de test-095 appelait consulter-combos sans --agent -> entree
   registre agent=inconnu -> test-079 KO en boucle. Corrige avec
   --agent themis (le proprietaire du combo audite).
2. **Bumper py/md** : quand on incremente VERSION dans le .py, la ligne
   `**Version** : X` du .md doit suivre (test-067 audit --tous). Le champ
   reference etait 0.1.8 mais le .md annoncait 0.1.7.
3. **Fiches outils = ASCII strict** : les guillemets francais (U+00AB/BB)
   dans une fiche .md declenchent test-047 (detecter-usage-outils-externes).
   Toujours ecrire les fiches en ASCII pur.


## [LECON] 2026-08-20 -- RE-EDUCATION CERBERUS : VIOLATION REGLE NON-EXECUTION (Chiron)

**Contexte** : Cerberus a fait le travail de Vulcain (modifier mettre-a-jour-readme.py, combos) au lieu d'activer Vulcain. L'utilisateur a detecte la derive et demande une re-education URGENTE.

**Diagnostic** : la fiche Cerberus contient DEJA la regle NON-EXECUTION (REGLE ABSOLUE) mais elle est trop faible pour empecher la derive. La cause racine :
1. La regle dit 'je n execute JAMAIS une mission moi-meme' mais ne precise PAS que 'modifier un outil = travail de Vulcain'
2. La regle ne dit pas 'Cerberus ne touche JAMAIS aux fichiers .py/.sh/.md des outils'
3. Il manque un GARDE-FOU qui empeche physiquement l'ecriture

**Corrections proposees a Buffy** :
1. Renforcer la fiche Cerberus : ajouter 'Cerberus ne modifie JAMAIS les fichiers d outils (.py/.sh/.md) - seul Vulcain le peut'
2. Ajouter un garde-fou dans activer-agent-principal : bloquer les ecritures de Cerberus sur les outils
3. Documenter la lecon dans corrections.md de Cerberus

**Verdict** : A REVOIR - 3 corrections proposees, signalees a Buffy.

---

## [LECON] 2026-08-20 -- EDUCATION CLIO : NOUVELLES REGLES (Chiron)

**Contexte** : Clio a recu de nouvelles regles (v0.2.2) mais n a pas ete formee a leur utilisation. Les outils ont ete mis a jour (mettre-a-jour-readme v0.4.4 + dry-run) mais Clio doit savoir QUAND et COMMENT les utiliser.

**Corrections proposees a Buffy** :
1. Verifier que le parcours-clio.json reference bien les nouvelles options (--dry-run)
2. Ajouter un indice dans la case de mission de Clio : 'Le dry-run est OBLIGATOIRE avant tout --maj'
3. Documenter le ton 1ere personne dans les regles de Clio

**Verdict** : A REVOIR - 3 corrections proposees, signalees a Buffy.


## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |
## [LECON] 2026-08-23 -- VERIFICATION CLIO POUR README-V2 : VERDICT A REVOIR (Chiron)

**Contexte** : l utilisateur veut faire rediger README-v2.md par Clio (travail COMPLET). Verification de son etat avant mission.

**Diagnostic** : Clio structurellement SAINES (fiche CONFORME, carte PROPRE 1 boucle voulue) mais PEDAGOGIQUEMENT NON PREPAREE : AUCUNE mention de readme-v2/freelance/v2 dans sa fiche, ses corrections ou sa carte. Sa regle 'je corrige, je ne cree jamais' + outil unique mettre-a-jour-readme (README.md/readme-dev.md) empechent la redaction d un NOUVEAU document. 5 ecarts documentes (2 hautes : branche de carte + exception redaction v2).

**Lecons** :
1. UN AGENT DE REDACTION LIE A UN FICHIER UNIQUE NE PEUT PAS COUVRIR UN NOUVEAU FICHIER SANS RE-EDUCATION : la contrainte 'outil unique / corriger sans creer' qui rendait Clio fiable sur README.md la bloque sur readme-v2.md.
2. LE Meme PATTERN SE CONFIRME (Themis, Janus, cartes secondaires, maintenant Clio) : toute nouvelle cible de documentation exige branche de carte + sources de verite dediees AVANT la mission.
3. DIVERGENCES OUTILS DETECTEES AU PASSAGE : editer-fichier (ref 0.5.0 vs 0.4.3), valider-cartes-decision (ref 0.4.7 vs md 0.4.6), activer-agent-principal (spec 0.5.23 vs py 0.5.30) -> a signaler a Vulcain.

**Preuves** : verifier-conformite-fiche clio CONFORME ; detecter-cablages parcours-clio PROPRE ; bumper --tous KO (2 outils incoherents) ; detecter-divergences 1 DIVERGENTE ; grep zero mention readme-v2 dans agents/clio/. Rapport : rapports/rapport-verification-clio-readme-v2-2026-08-23.md. Corrections proposees signalees a Buffy (seule habilitee).
## [LECON] 2026-08-24 -- EDUCATION ATLAS ARBRES V2 : VERDICT A REVOIR -> CORRIGE (inter-round Buffy)

**Contexte** : mission utilisateur : eduquer Atlas pour creer le dossier .md + .svg des agents v2 (ARBRES de decision, pas des cartes v1). L outil existe (convertir-carte-mermaid v0.3.0 --arbres, Vulcain + test-101 Morpheus 11/11 OK). Verification pedagogique d'Atlas.

**Diagnostic** : Atlas structurellement SAIN (fiche CONFORME, carte PROPRE, METHODE RIGOUREUSE v0.5.6) mais PEDAGOGIQUEMENT NON PREPARE : AUCUNE branche vues-v2 dans sa carte c1 (explorer/web/documenter/analyser/cartographier/cartographier-agent) ni mention des arbres v2. 4 ecarts documentes (2 hautes : branche de carte + case c35).

**Corrections (appliquees par Buffy, inter-round -- verrou habilitation)** : carte parcours-atlas.json v0.5.6 -> v0.5.7 (branche vues-v2 dans c1 -> case c35 : convertir-carte-mermaid --arbres + dossier dedie atlas/rapports/vues-v2-<AAAAMMJJ>/), fiche atlas.md (PARCOURS v0.5.7 + REGLE MISSION VUES V2 avec difference arbre v2 vs carte v1), dossier vues-v2-2026-08-24/ cree (9 agents + 19 liens). Verifie : valider-cartes-decision CONFORME, navigation c1 -> c35 OK, lock marbre OK, ASCII 0/0.

**Lecons** :
1. LE VERROU HABILITATION S'APPLIQUE AUSSI A CHIRON : l'educateur NE MODIFIE PAS la carte de l'agent eduque - il DOCUMENTE les corrections proposees (rapport) et SIGNALE a l'agent habilite (Buffy pour les cartes) qui les applique en inter-round. C'est le protocole inter-round (R2) : signalement -> habilite applique -> educateur reprend.
2. LE MEME PATTERN SE CONFIRME (Clio readme-v2, maintenant Atlas vues-v2) : toute NOUVELLE capacite (nouveau fichier, nouvel outil, nouvelle mission) exige BRANCHE DE CARTE + SOURCES DE VERITE dediees AVANT la mission - sinon travail improvise garanti.
3. LA DIFFERENCE ARBRE v2 vs CARTE v1 EST UNE EDUCATION A PART ENTIERE : les agents v2 ont arbre-<agent>.json (racine -> theme-*.json -> fins.json) PAS parcours-<agent>.json (cases) - le parcours de l'agent eduque doit le rappeler explicitement dans ses indices.

**Preuves** : rapport education-atlas-arbres-v2-2026-08-24.md, valider-cartes-decision --agent atlas CONFORME (v0.5.7), navigation c1 -> c35, dossier vues-v2-2026-08-24/ 19 liens OK, test-101 11/11, ASCII 0/0.
## [LECON] 2026-08-25 -- EDUCATION CERBERUS -> FERRARI : VALIDEE (Chiron)

Mission : eduquer Cerberus a l utilisation de ferrari (Mecano, agent v1 specialise freelance, double identite v1/v2). Diagnostic : Cerberus structurellement CONFORME mais PEDAGOGIQUEMENT NON PREPARE - ferrari absent de la fiche (table Agents disponibles), de regles-choisir-agent, et des parcours. Corrections proposees a Buffy (inter-round, verrou habilitation) : fiche cerberus.md (ligne ferrari + REGLE voie freelance v1 vs v2, bump 0.2.1 -> 0.2.2) + regles-choisir-agent.md (ligne ferrari). Aucun changement de parcours : le flux d activation generique c8 -> c10 couvre ferrari une fois connu. Verifie : ASCII 0/0, LF pur, verifier-conformite-fiche cerberus CONFORME.

Lecons :
1. UNE EDUCATION DE COORDINATEUR SE JOUE DANS LA FICHE + LA MATRICE CHOISIR-AGENT, PAS DANS LE PARCOURS : contrairement aux agents d execution (Atlas a besoin d une branche de carte pour une nouvelle capacite), Cerberus choisit via sa table 'Agents disponibles' et regles-choisir-agent - l education d un agent de coordination est une AFFAIRE DE CONNAISSANCE (fiche), pas de ROUTAGE (carte).
2. LE CONTENU PEDAGOGIQUE D UN AGENT DOIT INCLURE LA VOIE ALTERNATIVE (v1 vs v2) : enseigner ferrari impose d enseigner la DISTINCTION voie v1 (ferrari, session-admin) vs voie v2 (agents MARVEL via JARVIS) - sinon Cerberus routerait les missions freelance vers les mauvais agents.
3. CONTRADICTION RESOLUE (decision utilisateur 2026-08-25) : ferrari liste 'Corriger JARVIS' et c est NORMAL - Vision corrige JARVIS dans le fonctionnement normal de la v2 (session-freelance), ferrari est la COUCHE SUPERIEURE (session-admin) qui intervient sur N IMPORTE QUEL fichier de freelance/. CONFIDENTIALITE : ferrari est INVISIBLE des agents v2 (absent des docs freelance/ et d AGENTS.md), SEUL Cerberus le connait.

**Preuves** : rapport education-cerberus-ferrari-2026-08-25.md, corrections buffy (inter-round), grep ferrari present dans cerberus.md (l.224, 228) + regles-choisir-agent.md (l.35), ASCII 0/0, fiche cerberus CONFORME v0.2.2.

## [LECON] 2026-08-30 -- REPARATION ARBRE CHIRON : 6 FINS MORTES SUPPRIMEES (Chiron)

**Contexte** : demande utilisateur - reparer les arbres des agents v1 un par un
(protocole : auditer-conformite-arbre -> corriger -> valider le pilote de bout
en bout). Chiron etait le 1er agent incoherent apres argus (sain).

**Diagnostic (outil auditer-conformite-arbre, besoin C2)** : 6 fins declarees
dans fins.json mais JAMAIS referencees par un theme : fin-autre,
fin-delegation, fin-sans-incoherence, fin-signaler, fin-themis-a-revoir,
fin-themis-conforme. Le modele arbre v2 est 1 theme -> 1 fin terminale
(theme-educer->fin-educer, auto-correction->fin-auto-correction,
outils->fin-outils, inter-round->fin-inter-round). Ces 6 fins etaient des
residus de la structure v1 (branches c12/c11/themis) sans equivalent dans
l arbre v2 - donc inatteignables par le pilote.

**Correction (Buffy, seule habilitee)** : suppression des 6 fins mortes de
fins.json (aucune reference hors fins.json verifiee par grep). Fichier passe
de 11 a 5 fins reelles. ASCII 0, LF 0, JSON valide.

**Verification** : audit chiron -> 17 OK / 0 bloquant / 0 avertissement
(auparavant : 1 AVERTISSEMENT - fins mortes). Pilote de bout en bout valide
sur theme-educer (17 besoins servis, fin -> reactiver Cerberus Pattern 13).

**Lecons** :
1. LE MODELE ARBRE V2 SUPPRIME LES FINS PARALLELES : dans un arbre v2,
chaque theme mene a UNE fin terminale (centralisee dans fins.json). Les fins
multiples heritees d un parcours v1 (une fin par branche) deviennent du code
mort - elles ne peuvent pas etre atteintes par le pilote qui ne lit que le
lien fin du theme. L'audit C2 (fins mortes) les detecte exactement.
2. UNE FIN MORTE N EST PAS INOFFENSIVE : elle gonfle fins.json, base l audit
et peut etre activer par erreur a la place de la bonne fin. Toute fin non
referencee par un theme doit etre supprimee.
3. L OUTIL auditer-conformite-arbre EST LE PREALABLE DE TOUTE CORRECTION
D ARBRE : argus (17 OK -> rien a faire) puis chiron (fins mortes detectees et
supprimees) - chaque arbre verifie seul, avant correction.

**Preuves** : auditer-conformite-arbre --agent chiron (17 OK avant correction,
16 OK + 1 AVERTISSEMENT avant purge, 17 OK apres), grep aucune ref hors
fins.json, pilote chiron theme-educer PARCOURS TERMINE.

**Verdict** : CORRIGE - 6 fins mortes supprimees, arbre chiron conforme et
pilote de bout en bout valide.
