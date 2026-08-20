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
