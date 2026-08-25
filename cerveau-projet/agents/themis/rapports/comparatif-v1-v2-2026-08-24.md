---
identite:
  type: rapport
  appartient_a: themis
  date: 2026-08-24
  statut: definitif
  categorie: comparatif-v1-v2
  mise_a_jour: 2026-08-24 (donnees du dossier complet freelance reorganise)
---

# COMPARATIF V1 VS V2 -- SUPER-DETAIL

> **BANDEAU NON NORMATIF** : ce document est une ANALYSE a destination des
> concepteurs. Il n'autorise et n'interdit RIEN aux agents. Les regles
> applicables restent les cartes, fiches, corrections et regles-immuables
> de chaque agent. Localisation : themis/rapports/ -- jamais reference
> dans une carte ou une fiche, pour qu'aucun agent v2 ne puisse le
> traiter comme une autorite.
>
> **MISE A JOUR 2026-08-24** : colonne v2 enrichie avec les donnees RELLES
> du dossier complet freelance reorganise (Atlas, exploration 2026-08-24) :
> **DECISION 2026-08-24 (recommandation Themis, validation utilisateur) :
> les piliers 8 (README v2) et 15 (Education v2) passes de A DECIDER a
> ADAPTER -- voir recommandations-decisions-readme-education-2026-08-24.md**
> atlas/rapports/freelance-2026-08-24/ -- dossier-complet + 16 .md par
> dossier (racine, conventions, docs, protocoles, regles, routines,
> templates, tools-commun, 9 agents). Ces donnees remplacent les
> suppositions sur la v2 par des faits verifies sur disque.
>
> Agent : Themis (evaluation croisee) -- Date : 2026-08-24
> Sources croisees : bilan-strategique-v1-2026-08-22.md,
> synthese-v1-pour-v2-2026-08-22.md, proposition-v2.md (D1-D18),
> lecons.db, dossier complet freelance (Atlas 2026-08-24).

---

## SOMMAIRE

1. Lecons.db (memoire longue)
2. Cartes de decision -> Arbres
3. Cycle Cerberus -> agent -> controles
4. Regles immuables
5. Versionning
6. Habilitations et verrous
7. Outils de validation
8. README public et dev
9. Historique et memoires
10. Gouvernance globale
11. Activations et sessions
12. Tests et non-regression
13. Marbre et protection
14. Inter-rounds
15. Education et formation (Chiron)
16. Freelance et JARVIS

**Colonnes** : v1 (fait concret + probleme) / v2 (ce que la proposition et
le dossier complet prevoyent) / DECISION (garder / adapter / jeter / a
decider) / RISQUE (si mal applique ou oublie) / PREUVE (lecon ou rapport).

---

## 1. LECONS.DB (MEMOIRE LONGUE)

| Colonne | Contenu |
|---|---|
| **v1** | BDD SQLite 212-213 lecons, pollinisation croisee (c0e), flux enregistrer/consulter. PROBLEME : lecons parfois peu classees, difficiles a retrouver au moment du besoin. |
| **v2** | Decision D10 : BDD revue en BIBLE -- lecons classees, categorisees, index, table des 20 dernieres, cases de l'arbre pour consulter par categorie. Donnees reelles : lecons.db toujours active cote v1 ; la bible v2 est prevue mais PAS ENCORE construite dans freelance/ (a noter). |
| **DECISION** | ADAPTER -- garder le principe, appliquer D10 (classification + consultation comme une bible). |
| **RISQUE** | Sans classification, la memoire longue redevient un fourre-tout : les agents ne consultent plus, les erreurs reviennent. |
| **PREUVE** | bilan-strategique-v1 section II.1 (EXCELLENT) ; proposition-v2 D10 ; dossier-complet section 4 (D10 non construit). |

---

## 2. CARTES DE DECISION -> ARBRES

| Colonne | Contenu |
|---|---|
| **v1** | Cartes JSON (parcours) case par case, guider-parcours. PROBLEME : cartes devenues des monstres (30+ cases), branches nombreuses, maintenance lourde (valider-cartes, Pattern 14, lock). |
| **v2** | Decision D1 : ARBRE DES DECISIONS (systeme veineux) -- themes -> categories -> cases -> fins. Decision D5 : redirections vers fichiers pour alleger. Decision D8 : themes concrets (CREER, MODIFIER, LIRE, VALIDER, TESTER, REDIGER, NETTOYER, COORDONNER, EXPLORER). Donnees reelles : 9 agents freelance ont chacun un arbre (racine + themes + fins) dans leur dossier -- structure presente sur disque. |
| **DECISION** | ADAPTER -- le concept de carte est conserve mais transforme en arbre a themes + redirections. |
| **RISQUE** | Si l'arbre garde la complexite des cartes v1 (trop de branches), la v2 reproduit le monstre. Les redirections (D5) sont la cle pour rester leger. |
| **PREUVE** | bilan-strategique-v1 II.2 ; proposition-v2 D1/D5/D8 ; dossier-complet (arbres presents). |

---

## 3. CYCLE CERBERUS -> AGENT -> CONTROLES

| Colonne | Contenu |
|---|---|
| **v1** | Cycle CERBERUS -> AGENT -> CERBERUS, chaines lineaires (Pattern 13), audit Themis + controle Janus en fin de mission. PROBLEME : chaines parfois disproportionnees pour des petites taches ; Cerberus goulet d'etranglement. |
| **v2** | JARVIS route les agents (D16), Cerberus garde l'entree/sortie. Fin de mission : la fin suit SA carte, dernier maillon reactive Cerberus. Donnees reelles : JARVIS v0.9.0 distribue les missions (~600 messages inbox/outbox) ; les fins d'arbres freelance documentent chaque type de fin. |
| **DECISION** | ADAPTER -- garder le cycle et les controles, remplacer le routage manuel par JARVIS. |
| **RISQUE** | Si JARVIS tombe en panne ou que les agents contournent le hub, on retombe sur le routage manuel et la perte d'information. |
| **PREUVE** | bilan-strategique-v1 III.3 ; proposition-v2 D16 ; dossier-complet (JARVIS actif). |

---

## 4. REGLES IMMUABLES

| Colonne | Contenu |
|---|---|
| **v1** | regles-immuables/ (general, marbre, hierarchie), relues a chaque activation. PROBLEME : beaucoup de regles, certaines contradictoires, corrections interminables. |
| **v2** | Regles M1-M7 (immuables), V1-V4 (veracite), P1-P10 (principes) + philosophie/ (le pourquoi). Donnees reelles : regles/regles-immuables.md present avec M1-M7, V1-V4, P1-P10, D1-D18, grades, medailles. |
| **DECISION** | ADAPTER -- garder les regles fondamentales, reorganisees (M/V/P) avec philosophie. |
| **RISQUE** | Sans philosophie, les regles redeviennent des interdictions sans sens : contournees ou oubliees. |
| **PREUVE** | bilan-strategique-v1 IV (fondations) ; dossier-complet section regles. |

---

## 5. VERSIONNING

| Colonne | Contenu |
|---|---|
| **v1** | Version dans chaque outil/carte/fiche, bump manuel (rituel de 10 min a chaque modif), pins de tests. PROBLEME : fardeau disciplinaire, bump oublie, Pattern 14 a verifier. |
| **v2** | Versionning allige -- l'utilisateur veut automatiser. Donnees reelles : les outils freelance portent des versions (jarvis.py v0.9.0, jarvis-server.py v0.9.0) mais sans le rituel de bump v1. |
| **DECISION** | ADAPTER -- garder le principe, automatiser le bump (pas de rituel manuel). |
| **RISQUE** | Sans version, impossible de savoir quelle version tourne ; regression silencieuse. |
| **PREUVE** | bilan-strategique-v1 II.6 / V (fardeau) ; dossier-complet (versions v2). |

---

## 6. HABILITATIONS ET VERROUS

| Colonne | Contenu |
|---|---|
| **v1** | Verrou d'habilitation par outil, qui peut l'utiliser, inter-rounds de reparation. PROBLEME : CATASTROPHE -- la restriction excessive a paralyse les agents (lecon 2026-08-22). |
| **v2** | GRADES (copper -> diamond) + cartes d'identite enrichies (D17 : grade, medaille, notation, mots-cles). Donnees reelles : grades presents (Stark gold, JARVIS gold, Shuri/Forge/Rogers/Vision silver, Parker copper, EDITH/Fury silver) ; securite/ avec lecteur-de-carte + verrou-outils dans tools-commun. |
| **DECISION** | ADAPTER -- remplacer les verrous par les grades (faire confiance, pas restreindre). |
| **RISQUE** | Si les grades ne sont pas appliques coherentment, les agents sans grade bloquent ou depassent leur perimetre. |
| **PREUVE** | bilan-strategique-v1 III.2 / lecon 2 ; proposition-v2 D17 ; dossier-complet (grades, securite). |

---

## 7. OUTILS DE VALIDATION

| Colonne | Contenu |
|---|---|
| **v1** | valider-cartes-decision, valider-conformite-ascii, evaluer-processus, detecteurs, combos. PROBLEME : 250 outils pour 19 agents -- surcharge, chevauchements, maintenance impossible. |
| **v2** | 20-30 outils max ; outils v2 dans tools-commun (Forge responsable) : os_path, encodage, exec, horloge, jsonl-store, rappel, rating-agents, defcon, securite, jarvis. Donnees reelles : tools-commun present avec ces modules ; proposition-v2 section 6 liste les outils cibles (certains non construits). |
| **DECISION** | ADAPTER -- garder les validations essentielles, reduire drastiquement le nombre d'outils. |
| **RISQUE** | Si la v2 re-multiplie les outils, la maintenance redevient un cauchemar (lecon 1 : moins c'est plus). |
| **PREUVE** | bilan-strategique-v1 III.1 / lecon 1 ; dossier-complet section tools-commun. |

---

## 8. README PUBLIC ET DEV

| Colonne | Contenu |
|---|---|
| **v1** | README public + readme-dev (catalogue), maintenus par Clio (mettre-a-jour-readme). PROBLEME : 3 memoires qui se desynchronisent (AGENTS.md + historique + traces), corrections frequentes. |
| **v2** | README v2 grand public (equipe freelance) prevu ; proposition-v2 D9 : historique par agent + tokens-historique.md (PAS de trace unique). Donnees reelles : README-v2.md n'existe pas encore (mission Clio preparee mais non lancee) ; freelance-historique.md VIDE. |
| **DECISION** | ADAPTER -- README v2 redige par CLIO avec EXCEPTION REDACTION V2 (deja preparee : fiche EXCEPTIONS V2 + carte c22/c23 readme-v2). LANCER la mission (recommendation Themis 2026-08-24, validation utilisateur). |
| **RISQUE** | Sans README v2, les concepteurs n'ont pas de porte d'entree grand public de la v2 ; risque de desynchronisation si l'historique n'est pas tenu (D9). |
| **PREUVE** | bilan-strategique-v1 III.5 (bruit ASCII) ; proposition-v2 D9 ; dossier-complet (historique vide). |

---

## 9. HISTORIQUE ET MEMOIRES

| Colonne | Contenu |
|---|---|
| **v1** | AGENTS.md + AGENTS-historique.md + traces (chronos, registres) : 3 sources. PROBLEME : desynchronisations frequentes, entrees parasites, nettoyage. |
| **v2** | Decision D9 : PAS DE TRACE UNIQUE -- historique par agent/session + tokens-historique.md (activites + tokens). Donnees reelles : jarvis/historique/ + inbox/outbox + files d'attente existent (~600 messages) ; tokens-historique.md non encore construit. |
| **DECISION** | ADAPTER -- historique par agent (comme v1) + tokens-historique.md (nouveau). |
| **RISQUE** | Sans tokens-historique, pas de visibilite sur la consommation ; sans historique par agent, on perd la tracabilite R/IR (D12). |
| **PREUVE** | bilan-strategique-v1 III.3 ; proposition-v2 D9/D12 ; dossier-complet (jarvis/historique). |

---

## 10. GOUVERNANCE GLOBALE

| Colonne | Contenu |
|---|---|
| **v1** | 3 groupes (Coordination / Cerveau-projet / Trio futurs), domaines separes, regles-groupes-agents. PROBLEME : sur-ingenierie de la gouvernance, violations de perimetre frequentes. |
| **v2** | Groupes v2 (Coordination / Freelance / Futurs) ; JARVIS centralise la communication ; grades hierarchiques. Donnees reelles : 9 agents freelance organises autour de Stark (coordinateur) + JARVIS (hub), regles M1-M7. |
| **DECISION** | ADAPTER -- garder la separation des domaines, simplifier la gouvernance (moins de ceremoniaux). |
| **RISQUE** | Si la gouvernance reste lourde, les agents perdent du temps en processus au lieu de produire. |
| **PREUVE** | bilan-strategique-v1 II.4 / III.4 ; dossier-complet (organisation freelance). |

---

## 11. ACTIVATIONS ET SESSIONS

| Colonne | Contenu |
|---|---|
| **v1** | activer-agent-principal, sessions session-llm-N, MODE ID, sidentifier. PROBLEME : activations ecrasees, collisions de sessions, historique melange. |
| **v2** | D3 : activation automatisee et transparente (commande simple cache plusieurs outils) ; D6 : formulaire d'outil declaratif ; sessions v2 (session-admin / session-freelance). Donnees reelles : activation freelance via jarvis.py (envoyer/lire/acquitter/lister/activer) -- les agents freelance n'utilisent PAS activer-agent-principal. |
| **DECISION** | ADAPTER -- activer reste le point d'entree, mais automatise et transparent (D3/D6). |
| **RISQUE** | Si l'activation n'est pas transparente, l'agent ne sait pas ce qui se lance ; si le formulaire (D7) est mal defini, les outils refusent tout. |
| **PREUVE** | bilan-strategique-v1 III.3 ; proposition-v2 D3/D6/D7 ; dossier-complet (jarvis.py). |

---

## 12. TESTS ET NON-REGRESSION

| Colonne | Contenu |
|---|---|
| **v1** | 97 tests, pins, profils, garde-fous, testeur Morpheus. PROBLEME : DEBORDES -- la maintenance des tests prenait plus de temps que le developpement, les tests creaient des problemes. |
| **v2** | Decision D2 : non-regression SEPAREE pour les agents freelance (objectifs differents) ; 10-15 tests max, simples, sans pins. Donnees reelles : tests reels Fury PASSE (inter-round, parallel, protocole 13, rating) -- fury/rapports/ + tools/ (lanceur-scenario). |
| **DECISION** | ADAPTER -- garder le principe, simplifier radicalement (D2, peu de tests, sans garde-fous internes). |
| **RISQUE** | Si on re-multiplie les tests, on reproduit le Far West v1 (lecon 4 : tests simples). |
| **PREUVE** | bilan-strategique-v1 II.3 / III.6 / lecon 4 ; proposition-v2 D2 ; dossier-complet (tests Fury). |

---

## 13. MARBRE ET PROTECTION

| Colonne | Contenu |
|---|---|
| **v1** | Zones protegees (marbre), cartes-lock, Gardien seul habilite. PROBLEME : trop de zones protegees, trop de verrous, ralentissait tout. |
| **v2** | Marbre allige (zones reduites) ; routage porte du marbre (D13 : STANDARD -> Socrate, EXCEPTIONNEL -> utilisateur). Donnees reelles : cartes-lock toujours actif cote v1 ; cote freelance, securite/ avec lecteur-de-carte + verrou-outils (applique les decisions, allige). |
| **DECISION** | ADAPTER -- principe conserve mais allige, routage D13. |
| **RISQUE** | Sans protection minimale, un agent modifie une zone critique par erreur ; avec trop de protection, on re-paralyse (lecon 2). |
| **PREUVE** | bilan-strategique-v1 II.5 / V ; proposition-v2 D13 ; dossier-complet (securite). |

---

## 14. INTER-ROUNDS

| Colonne | Contenu |
|---|---|
| **v1** | Erreur hors-perimetre -> inter-round -> agent habilite repare -> l'appelant reprend. PROBLEME : boucles de reparation interminables quand mal comprises. |
| **v2** | D11 : flux ROUND / INTER-ROUND / REPRISE (round lance = fini, erreur = agent habilite + reprise) ; D12 : tracabilite R/IR + perimetre par agent. Donnees reelles : tests reels Fury inter-round PASSE (scenario-parallel-reel.json). |
| **DECISION** | GARDER -- le principe est sain, le formaliser via D11/D12. |
| **RISQUE** | Sans tracabilite R/IR (D12), on ne sait pas qui a lance l'inter-round ni pourquoi. |
| **PREUVE** | bilan-strategique-v1 IV (protocole de fin) ; proposition-v2 D11/D12 ; dossier-complet (tests Fury). |

---

## 15. EDUCATION ET FORMATION (CHIRON)

| Colonne | Contenu |
|---|---|
| **v1** | Chiron re-eduque les agents quand outils/regles/protocoles changent, verification pedagogique avant mission. PROBLEME : la re-education etait parfois necessaire parce que la formation initiale manquait. |
| **v2** | Formation continue via les arbres et les fiches enrichies (D17 : mots-cles, notation) ; lecons consultables comme une bible (D10). Donnees reelles : le role d'education n'a pas d'equivalent MARVEL dedie dans freelance/ (les agents apprennent via JARVIS + arbres). |
| **DECISION** | ADAPTER -- education v2 = ARBRES + BIBLE DES LECONS (D10, a construire) + ROGERS (veille regles/conventions). Principe Chiron preserve : la consultation des lecons PRECEDE les actions sensibles (recommendation Themis 2026-08-24, validation utilisateur). |
| **RISQUE** | Sans formation, les agents repetent les erreurs v1 ; sans verification avant mission, les agents improvisent (lecon Chiron : la pedagogie PRECEDE l'activation). |
| **PREUVE** | lecon Chiron 2026-08-23 (verification Clio readme-v2) ; proposition-v2 D10/D17. |

---

## 16. FREELANCE ET JARVIS

| Colonne | Contenu |
|---|---|
| **v1** | PAS de hub de communication : messages informels entre rounds, pertes d'information, coordination manuelle par Cerberus. PROBLEME : dependance totale a Cerberus, perte d'information. |
| **v2** | Decision D16 : JARVIS, hub de communication obligatoire -- RIEN NE PASSE SANS JARVIS. Donnees RELLES du dossier complet (2026-08-24) : 9 agents MARVEL (Stark, Shuri, Forge, Rogers, Parker, JARVIS, Vision, EDITH, Fury) avec grades ; jarvis.py v0.9.0 + jarvis-server.py v0.9.0 ; inbox/outbox ~600 messages ; tools-commun/jarvis/ complet (functions, serveur, combos) ; routines EDITH (manifest, etat-executions, surveillance) ; protocoles 1-20 documentes ; templates v2 complets. La v2 est DEJA EN MARCHE, pas une proposition. |
| **DECISION** | GARDER ET PROLONGER -- JARVIS est la colonne vertebrale ; documenter les chantiers restants (historique vide, README tools-commun en retard, outils D9/D10/D18 a construire). |
| **RISQUE** | Si un agent contourne JARVIS, on perd la tracabilite et la coordination ; si JARVIS n'est pas maintenu (Vision exclusif), le hub casse. |
| **PREUVE** | bilan-strategique-v1 III.3 / lecon 7 ; proposition-v2 D16 ; dossier-complet-freelance-2026-08-24.md (toute la section 4). |

---

## SYNTHESE -- 5 PILIERS VITAUX A PROTEGER ABSOLUMENT EN V2

1. **JARVIS (D16)** -- la colonne vertebrale : sans hub, la v2 retombe sur
   la coordination manuelle v1. Deja fonctionnel (~600 messages) : le
   proteger (Vision exclusif, maintenance).
2. **Lecons en BIBLE (D10)** -- la memoire longue classee : le meilleur
   investissement de la v1, a rendre consultable au moment du besoin.
3. **Arbres des decisions (D1/D5/D8)** -- la boussole : plus legers que
   les cartes v1 grace aux redirections ; ne pas les laisser devenir des
   monstres.
4. **Grades plutot que verrous** -- la confiance : la restriction excessive
   a paralyse la v1 (lecon 2) ; les grades (D17) remplacent les
   habilitations.
5. **Tests SEPARES et simples (D2)** -- la securite sans le Far West :
   10-15 tests max, sans pins, sans garde-fous internes.

## SYNTHESE -- 5 PIEGES A EVITER

1. **Re-multiplier les outils** -- 250 outils a tue la maintenance v1 ;
   20-30 max en v2 (lecon 1).
2. **Re-complexifier les tests** -- 97 tests ont deborde ; garder D2
   (lecon 4).
3. **La gouvernance ceremonielle** -- les processus lourds ralentissent ;
   la v2 doit rester simple.
4. **Les verrous qui paralysent** -- chaque verrou ajoute un inter-round ;
   faire confiance aux grades.
5. **Les corrections en spirale** -- corrections.md interminables ;
   courtes, directes, dans la BDD.

---

## CONCLUSION

La v1 a ete un **laboratoire exceptionnel** : en 12 jours, 19 agents, 250
outils, 97 tests, 213 lecons. Elle a prouve les concepts qui fondent la
v2 (lecons, cartes, domaines, protocoles) et revele les pieges (surcharge,
verrous, tests debordes).

La v2, grace au dossier complet freelance (2026-08-24), n'est plus une
proposition : elle est **DEJA EN MARCHE**. Les decisions D1-D18 sont
gravees, les 9 agents MARVEL existent avec leurs arbres et grades, JARVIS
route ~600 messages, les protocoles 1-20 sont documentes, les tests reels
Fury PASSENT.

**Bilan des verdicts** : 2 a garder tels quels (inter-rounds D11/D12,
freelance/JARVIS D16) ; 14 a adapter (lecons, arbres, cycle, regles,
versionning, grades, outils, README, historique, gouvernance, activations,
tests, marbre, education, README v2, education v2) ; 0 a decider. Les
piliers 8 et 15 ont ete tranches par recommandation Themis (2026-08-24,
validation utilisateur) : README v2 = Clio (exception redaction v2) ;
education v2 = arbres + bible D10 + Rogers. Les chantiers documentaires
restants (freelance-historique vide, README tools-commun en retard, outils
D9/D10/D18 a construire) sont identifies dans le dossier complet.

> La simplicite est la sophistication supreme. -- Leonard de Vinci
