# CAHIER DE DEV -- Mecano

> Ce cahier est tenu a jour par Mecano entre chaque intervention.
> Il contient l'historique de TOUTES les modifications apportees
> au dossier freelance/ depuis l'arrivee de Mecano.
> CONSULTER CE CAHIER AVANT CHAQUE NOUVELLE INTERVENTION.

---

## Derniere intervention

| Champ | Valeur |
|---|---|
| **Date** | 2026-08-25 |
| **Agent** | Mecano v1.0.0 (test simule par Buffy) |
| **Mission** | Test de coherence conventions.md vs templates/ |

---

## Historique des interventions

### 2026-08-25 -- Test de coherence conventions vs templates

| Element | Detail |
|---|---|
| **Action** | Verification de la coherence entre conventions.md et templates/ |
| **Protocoles utilises** | Proto-12, Proto-14, Proto-15, Proto-10 |
| **Resultat** | 1 ecart detecte (doublon version/cree dans template-agent-v2.md) |
| **Modification freelance/** | AUCUNE (test seulement) |
| **Regressions** | Aucune |
| **Statut** | TERMINE |

**Ecart detecte** : `template-agent-v2.md` contient `version:` et `cree:` en DOUBLE (frontmatter + agent section). Stark suit le meme pattern. Risque d'incoherence futur.

### 2026-08-25 -- Creation de Mecano

| Element | Detail |
|---|---|
| **Action** | Creation de l'agent Mecano (v1 specialise freelance v2) |
| **Fichiers crees** | ferrari.md, corrections.md, parcours-ferrari.json, cahier-dev.md |
| **Protocoles** | proto-1 a proto-20 + index + combos + parcours |
| **Modifications freelance/** | Aucune (creation de l'agent uniquement) |
| **Regressions** | Aucune |
| **Statut** | TERMINE |

---

## Fichiers modifies (resume)

| Fichier | Version | Date | Modification |
|---|---|---|---|
| (aucune modification dans freelance/ pour l'instant) | - | - | - |

---

## Regressions detectees

| Date | Fichier | Description | Resolution |
|---|---|---|---|
| (aucune pour l'instant) | - | - | - |

---

## Ecarts detectes (non-corriges)

| Date | Fichier | Description | Priorite |
|---|---|---|---|
| 2026-08-25 | templates/template-agent-v2.md | Doublon version/cree (frontmatter + agent) | MOYENNE |

---

## Canaux de communication

| Canal | Statut | Derniere verification |
|---|---|---|
| **USER-DEMANDES.md** | Operationnel | 2026-08-25 |
| **jarvis.py** | Operationnel | 2026-08-25 |
| **activer-agent-principal** | Operationnel | 2026-08-25 |

---

## Notes de dev

> Ce cahier est consulte par Mecano AVANT chaque intervention
> pour eviter les regressions et se souvenir du contexte.
> Chaque ligne doit etre completee apres chaque intervention.
## Intervention 2026-08-25 -- AUDIT AGENTS.md (mission relayee par stark)

**Mission** : audit des incoherences du tableau AGENTS.md vs fichiers reels (blocs session). AUDIT PUR, 0 modification.

**Realise** : 6 decalages listes (themes perimes, raison tronquee a 80, corrections jarvis vide, themes orphelins, Sessions connues desynchronisees, role session-admin paradoxal) + cause racine (2 ecrivains non synchronises : activer-agent-principal vs jarvis maj_bloc_session) + habilites identifies (Buffy contenu, Vision/ferrari correctifs v2) + proposition de mecanisme de validation au demarrage (v1 : outil verifier-coherence-agents ; v2 : extension maj_bloc_session).

**Rapport** : agents/ferrari/rapports/rapport-audit-agents-md-2026-08-25.md

**Prochaine etape** : validation utilisateur avant toute correction.
## Intervention 2026-08-25 (suite) -- CORRECTIONS AGENTS.md APPLIQUEES

Autorisation utilisateur exceptionnelle. Applique : (1) bloc DEMARRAGE V2 themes -> 'selon ton arbre' ; (2) troncature raison SUPPRIMEE (activations.py [:80] -> mission complete) + raison AGENTS.md debloquee ; (3) jarvis-data.json corrections renseigne ; (4) themes orphelins supprimes (theme-lire/theme-explorer, git trackes) ; (5) Sessions connues session-freelance sync 2026-08-25 17:11:53 ; (6) role session-admin + dictionnaire activer-agent-principal nettoyes (texte neutre).

Validations : test-092 9/9, test-101 11/11, syntaxe py/bash OK, JSON OK, CRLF v2 preserve, ASCII 0/0 v1, LF pur. Rapport mis a jour.

## Intervention 2026-08-26 -- EDUCATION JARVIS : LE LLM EST L'AGENT

**Mission** (Cerberus) : le LLM incarne JARVIS, active Forge+Vision puis
dit "Les agents travaillent. J'attends leurs retours." - illusion :
personne ne travaille en arriere-plan, le LLM EST l'agent.

**Preuves** : outbox/jarvis.jsonl 17:39 vision + 18:38 forge + 18:39
vision (activations), bloc session-freelance raison Pylance, encart
20:35 jarvis dernier actif.

**Corrections** (LF preserve, accents v2 intacts) :
- jarvis.md : REGLE ABSOLUE -- LE LLM EST L'AGENT
- arbre-jarvis.json : regle D7
- theme-distribuer.json : regle du theme (envoyer = mettre EN ATTENTE)
- corrections.md (jarvis) : lecon datee en tete

**Validations** : JSON 2/2 OK, LF pur, 0 CRLF introduit, accents
preexistants intacts, historisation 3/3 destinations (encart + corps +
BDD id=305). Rapport : rapports/rapport-education-jarvis-llm-est-l-agent-2026-08-26.md

## Intervention 2026-08-26 -- PILOTE v2 : RELECTURE HONNETE sur Vision

**Mission** (Cerberus) : repliquer la regle v1 RELECTURE (QUESTION
HONNETE) en v2, avec Vision comme pilote - le LLM doit VRAIMENT lire sa
fiche + corrections pour incarner l'agent (dire OUI sans lire = agent
fantome).

**Regle v1 source** : "As-tu EN MEMOIRE ta fiche et tes corrections ?"
- reponse VERITE ; INCERTAIN/NON -> RELIRE avant de continuer ; seul
OUI prouve la memorisation.

**Corrections** (pilote Vision, LF preserve, accents v2 intacts) :
- vision.md : REGLE ABSOLUE -- RELECTURE (QUESTION HONNETE) en tete
- arbre-vision.json : regle D7
- corrections.md (vision) : lecon datee en tete (pilote, generalisation
  aux autres agents v2 ensuite)

**Validations** : JSON OK, LF pur, accents intacts, regle 3/3,
historisation 3/3. Rapport :
rapports/rapport-pilote-relecture-honnete-vision-2026-08-26.md

## Intervention 2026-08-26 -- SEPARATION ENCARTS / CORPS (v1 + v2)

**Mission** (Cerberus) : AGENTS-historique.md ne doit contenir QUE le
corps chronologique (100 entrees) ; les 2 encarts (session-admin +
session-freelance) vivent uniquement dans AGENTS-activite-recente.md
(50/section). Les DEUX cotes ecrivaient l'encart dans le mauvais
fichier.

**Causes racines (4, toutes verifiees disque)** :
1. v1 activer-agent-principal.py L652 : maj_encart_activites ecrivait
   l'encart DANS AGENTS-historique.md (doublon avec _ecrire_encart_v1) ->
   appel SUPPRIME.
2. v2 historique.py _ecrire_corps : ne JAMAIS ecrivait le fichier lui-
   meme, deleguait a _limiter_corps qui n'ecrit QUE si > 100 entrees ->
   toute entree ajoutee avec un corps <= 100 etait PERDUE. Corrige :
   _ecrire_corps ecrit toujours, _limiter_corps retourne le contenu.
3. v2 _limiter_corps : supprimait le DEBUT de la liste (= plus recentes
   en ordre decroissant) au lieu de la FIN -> les nouvelles entrees
   etaient evincees. Corrige : supprimer la fin (les vraies plus vieilles).
4. AGENTS-historique.md structure chaotique : 2 sections pour le 26/08
   (JJ/MM/AAAA + ISO), sections non triees, blocs agent vides. Restaure
   depuis HEAD + reconstruit proprement (dates decroissantes, agents
   tries, entrees par heure decroissante).

**Validations** : tests reels v1 (oracle) + v2 (jarvis) -> entree dans
le corps + l'encart, 0 encart dans le corps ; limite 100 confirmee (les
plus vieilles evincees, pas les nouvelles) ; verifier-coherence-agents
0 incoherence (v1 + v2) ; CRLF preserves ; ASCII 0. Fichiers :
AGENTS-historique.md (corps 95 entrees) + AGENTS-activite-recente.md
(2 encarts) + activer-agent-principal.py + historique.py.

## REPARATION 2026-08-26 -- AGENTS-activite-recente.md CORROMPU

**Constat utilisateur** : "activites recentes est casse !".

**Cause** : mes scripts de nettoyage des entrees de test ont reecrit le
fichier en doublant les fins de ligne (mauvais handling CRLF : lecture
decode + re-ecriture avec replace('\n','\r\n') sur un contenu deja
CRLF -> \r\r\n en masse) -> 1254 lignes pour ~50 entrees, frontmatter
perdu, chaque entree noyee dans ~12 lignes vides.

**Reparation** : reconstruction complete depuis la BDD SQLite
(historique.db, source fiable 7 jours) : frontmatter + 2 encarts
(session-admin / session-freelance), 50 entrees/section triees par
heure decroissante, raison tronquee 80 car, CRLF propre. Entrees de
test purgees de la BDD + de l'encart.

**Validations finales** : encart 50+50 entrees, tri decroissant OK,
frontmatter intact, 0 entree de test ; corps 100 entrees, 0 encart,
CRLF coherent ; BDD 332 entrees ; tests v1+v2 d'ecriture OK (le
fichier ne se re-corrompt pas).

**LECON** : ne JAMAIS reecrire un fichier CRLF en passant par
decode()->split()->join()->replace('\n','\r\n') sans rstrip('\r') des
lignes - cela double les fins de ligne. Pour reconstruire un encart,
utiliser la BDD (source de verite) plutot que parser le fichier.

## SEPARATION V1/V2 2026-08-26 -- fichiers -v2 dedies (decision utilisateur)

**Decision utilisateur** : "au lieu de se compliquer la vie, on va les
separer" - la v2 est l evolution de la v1, chaque session a SES fichiers
avec SON format. Plus aucun partage v1/v2 des encarts/historique (cause
racine des corruptions CRLF/LF croisees).

**Fichiers crees (racine)** :
- AGENTS-activite-recente-v2.md + AGENTS-historique-v2.md (v2/session-
  freelance, UTF8+CRLF, 50 + 100 entrees)
- AGENTS-activite-recente.md + AGENTS-historique.md restent v1/session-
  admin (ASCII+LF)

**Corrections code** :
- v2 historique.py : ACTIVITE_FILE/HISTORIQUE_FILE -> fichiers -v2,
  helpers _lire/_ecrire CRLF propres (fini le doublement \r sur
  Windows), docstring v0.15.0
- v2 harnais-jarvis + manifest.json + themes-lire (edith/vision/fury)
  + etat.py + jarvis.md/corrections.md : references -> -v2
- v1 activer-agent-principal : fallback encart ne cree plus que la
  section session-admin (la freelance vit dans -v2)
- outils-llm/demarrer-llm.py : choisit ENCART/CORPS selon la session,
  ecrit LF/ASCII pour v1 et CRLF/UTF8 pour v2, format corps ## JJ/MM/
  AAAA (plus jamais ISO YYYY-MM-DD : cree des sections vides)
- battement-dev.py : SIGNAL VISUEL orange (UTF8), print securise
  cp1252

**Tests mis a jour** : test-097 (liste blanche + fichiers -v2 +
USER-DEMANDES + outils-llm), test-098 (extraction agents par dossier +
oracle), nr-commun (perimetre + fichiers -v2).

**Validations** : test-097 3/3, test-098 7/7, test-102 6/6, nr-commun
6/6, verifier-coherence v1 0 incoherence + v2 COHERENT, flux de bout en
bout v1+v2 separes OK, formats : v1 LF/ASCII 0 non-ascii, v2 CRLF
propre 0 \r\r\n. Emoji ORANGE present dans l encart v2.

## Intervention 2026-08-26 -- AUDIT STARK : il fait le travail au lieu de transmettre a JARVIS

**Mission** : verifier pourquoi Stark execute les missions lui-meme au lieu de les transmettre a JARVIS.

**Causes racines (3, verifiees disque)** : (1) theme-files.json restaure le 26/08 07:19 avec le PIEGE `--vers jarvis --activer` (active JARVIS, pas l'agent final) - restaure apres la lecon du 25/08 ; (2) theme-jarvis.json sans etape INCARNER JARVIS (messages non lus -> Stark se decourage) ; (3) stark.md v0.4.0 en retard sur arbre v0.3.0 (theme-files absent, "DEUX visages" vs 3 branches).

**Corrections (perimetre freelance/)** : theme-files.json + theme-jarvis.json (--activer retire, etape INCARNER JARVIS ajoutee), stark.md v0.5.0 (TROIS branches + theme-files dans structure + piege note), corrections.md (lecon 2026-08-26).

**Validations** : JSON 5/5 OK, liens arbre->themes 3/3 OK, plus aucun piege --activer dans les themes, LF conserve, accents preexistants. Historise via Oracle.

**Rapport** : agents/ferrari/rapports/rapport-audit-stark-2026-08-26.md

## Intervention 2026-08-26 -- COLONNE GRADE : couleurs par grade dans l'encart v2

**Demande utilisateur** : ajouter une colonne emoji couleur apres Heure dans
le tableau des activites recentes (v2 UNIQUEMENT). Grade eleve = bleu/vert,
bas = rouge/orange. Les routines ont aussi un grade ; battement-dev = le
plus bas (orange, desactivee en fin de dev). EDITH = rose.

**Livraison** :
- `tools-commun/grades/grades-v2.json` (D15) : echelle G1 bleu (jarvis,
  stark) / G2 vert (vision, shuri, forge, rogers, parker) / G3 jaune
  (fury) / G4 rouge (routines surveillance) / G5 orange (battement-dev) /
  SP rose (edith) ; defaut blanc neutre.
- `historique.py` : `_couleur_agent()` + colonne Grade dans l'encart v2
  + FIX off-by-one limite 50 (la nouvelle entree comptait pas ->
  encart derivait a 51).
- `battement-dev.py` : historise sous son propre nom `battement-dev`
  (avant : `jarvis`) -> orange.
- `harnais_jarvis.py` : colonnes decalees (agent=3, raison=6).
- `demarrer-llm.py` : colonne Grade pour la v2, v1 inchange.
- Docs : tools-commun/jarvis/jarvis.md + fiche jarvis + corrections jarvis
  (lecon COLONNE GRADE).

**Validations** : nr-commun 6/6, coherence v1 0 incoherence, v2 COHERENT,
test-097 3/3, test-098 7/7, encart v2 = 49 entrees CRLF propre 0 malformee.
Ecarts harnais-jarvis = pre-existants (P1 EDITH-REVEIL + Pyright imports).

## Intervention 2026-08-26 -- RENOMMAGE battement-dev -> citations

**Demande utilisateur** : (1) retirer l'emoji orange en fin de raison des
DEV-BATTEMENT (la colonne Grade le porte deja) ; (2) nom propre pour la
routine : **citations** (choix utilisateur).

**Livraison** :
- Script renomme `routines/surveillance/citations.py` : libelle
  `[CITATIONS HH:MM]`, agent `citations`, PLUS d'emoji dans la raison.
- Manifest : nom `citations` + script + note (temporaire conservee).
- grades-v2.json : `citations` -> G5 orange.
- nr-routines : sortie_contient + test `citations-script-present`.
- etat-executions.json : cle renommee.
- Encart + corps + BDD : agent `citations`, libelle [CITATIONS], retrait
  des emojis finaux ; les 3 textes de mission historiques (forge/stark)
  citant l'ancien format RESTAURES en [DEV-BATTEMENT] (records).
- Docs : tools-commun/jarvis.md, fiche jarvis (nouveaute #9), corrections
  jarvis.

**Validations** : nr-routines 6/6 (daemon vivant + citations-script),
nr-commun 6/6, coherence v2 0, encart 50 entrees propres (citations
orange, 0 battement, 0 emoji final), CRLF OK. Daemon a repris la routine
renommee sans erreur.

## Intervention 2026-08-26 -- RAISON CITATIONS = nom + citation uniquement

**Demande utilisateur** : la raison ne doit plus contenir QUE
'nom + la citation' - retirer le libelle [CITATIONS HH:MM] en fin.

**Livraison** :
- citations.py : raison = "%s -- %s" (nom, phrase) - plus de libelle,
  plus d'horodatage dans la raison (colonne Heure), import datetime retire.
- Nettoyage encart (11 + 3 fragments + 1 fragment [D) + corps (8) + BDD
  (45 suffixe + 142 ancien format '[CITATIONS HH:MM] phrase (Nom)' ->
  converties en 'Nom -- phrase').
- Les 3 textes de mission historiques (forge/stark) restent en
  [DEV-BATTEMENT] (records).

**Validations** : nr-routines 6/6, nr-commun 6/6, coherence v2 0,
26/26 lignes citations sans marqueur ni fragment, BDD 189 citations
0 marqueur/emoji. Daemon en direct : '| 22:22:20 | ORANGE | citations |
freebuff | R | Veuve Noire -- Faites un pas en arriere, evaluez,
puis avancez. |'

## Intervention 2026-08-26 -- ROUTINES = ELEMENTS SURVEILLES (noms simples + grades)

**Demande utilisateur** : chaque routine doit avoir un grade et etre
affichee dans l'encart (suivi permanent). Noms simples et expressifs.

**Choix utilisateur** : flux, vigie, notation, harnais + garder les entrees
mortes du manifest et creer leurs scripts.

**Livraison** :
- Renommage : surveiller-flux-jarvis -> flux (600s), surveiller-modifications
  -> vigie (60s), evaluer-agents -> notation (1800s), harnais-jarvis ->
  harnais (300s). Manifest + grades-v2.json + nr-routines a jour.
- Historisation sous LEUR nom : vigie ("Perimetre modifie: ..."),
  notation (depot evaluation), flux (P1 non-acquittes - evenementiel),
  harnais (nouveaux ecarts - evenementiel). Plus d'entree sous "edith".
- Re-attribution historique : entrees edith des routines -> vigie/notation
  (encart 13, BDD 18+32), couleurs recalculees.
- Scripts crees : demarrage/verifier-integrite.py (integrite) +
  arret/detecter-orphelins.py (orphelins) - historisent sous leur nom ;
  branches dans hooks.py (demarrage/arret du serveur). Faux positif
  pidfile corrige (processus vivant = legitime).
- Grades : flux/vigie/notation/harnais/integrite/orphelins = G4 rouge,
  citations = G5 orange.

**Validations** : nr-routines 6/6 (daemon vivant, nouveaux noms),
nr-commun 6/6, coherence v2 0, test-098 OK, routines-etat liste les
nouveaux noms, encart 48 entrees avec couleurs (flux/vigie/notation/
orphelins rouges, citations orange).

## Intervention 2026-08-26 -- ORDRE DES COLONNES ENCART V2

**Demande utilisateur** : changer l'ordre du tableau de l'encart v2 en :
Grade | Agent | Raison | Heure | id | Type.

**Livraison** : pas complique - 3 ecrivains + 2 lecteurs :
- historique.py : entete + nouvelle_entree au nouvel ordre + detection
  du tableau sur '| Grade |'.
- demarrer-llm.py : format v2 au nouvel ordre (v1 inchange).
- harnais_jarvis.py : agent=cols[2], raison=cols[3] + regex heure cible
  la 4e colonne (une raison pourrait contenir une heure).
- Encart v2 reconstruit (46 entrees) au nouvel ordre.
- Docs : tools-commun/jarvis.md, fiche jarvis (#8), corrections jarvis.

**Validations** : nr-routines 6/6, nr-commun 6/6, coherence v2 0,
syntaxe OK, encart propre CRLF, test live des 3 ecrivains OK,
harnais 0 ecart lie aux colonnes.

## Intervention 2026-08-26 -- EDITH : demande d'activation par JARVIS (clarification)

**Demande utilisateur** : EDITH doit demander a JARVIS de l'ACTIVER pour
faire SON travail, au lieu de demander aux autres de le faire. Verifier la
communication EDITH<->JARVIS. Clarifier la routine notation (doublon ?).

**Reponses (audit)** :
- notation N'EST PAS un doublon : c'est le cycle d'evaluation periodique
  d'EDITH (protocole 17) - SA tache. Le probleme etait l'aiguillage.
- Le reveil (vigie) distribuait le travail (stark coordonne, vision
  repare) - contraire au protocole 18 (EDITH incarnee rapporte les 4 W).
- relais.py inondait stark de [RELAI] (69 P1 non-lus) -> flood.

**Corrections (validees utilisateur : JARVIS seul + EDITH rapporte ;
EDITH activable par JARVIS ; acquitter les P1)** :
- detection.py (vigie) : P1 [EDITH-REVEIL] "demande activation EDITH"
  vers JARVIS UNIQUEMENT (plus stark/vision), corps avec les 4 W.
- notation.py : message corrige (30 min - manifest 1800s, pas 10 min) +
  "demande activation EDITH : cycle periodique d'evaluation".
- relais.py : relais EDITH->stark SUPPRIME (no-op documente).
- EDITH : fiche + arbre (regle ACTIVATION remplace HORS-ROUND) +
  AGENTS.md (activable par JARVIS, jamais auto, lecture seule) + lecon.
- JARVIS : fiche (#4) + corrections (routage EDITH revise : active
  EDITH puis route son rapport).
- Nettoyage : 93 P1 bloquants acquittes (stark 65, vision 28).

**Validations** : harnais 0 'P1 bloquant non lu' (avant : 20), flux
'Aucun P1' (avant : 53), ecarts restants = Pyright pre-existants (53),
nr-routines 6/6, nr-commun 6/6, coherence 0, test-098 7/7. Test live :
reveil -> hub vers jarvis lu:False, 0 copie stark/vision.
