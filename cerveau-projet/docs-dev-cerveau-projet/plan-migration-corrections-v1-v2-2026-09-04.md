---  identite:
  type: plan
  nom: plan-migration-corrections-v1-v2
  version: 0.3.0
  cree: 2026-09-04
  statut: a-valider
  appartient_a: buffy
  commun: true
  mot-cles: ["plan", "migration", "corrections", "memoire", "lecons", "v1", "v2", "bdd-lecons", "corrections.jsonl"]
---

# PLAN DE MIGRATION v1 -> v2 -- MEMOIRE DES CORRECTIONS

> Decision utilisateur 2026-09-04 : "on passe de v1 > v2, on doit oublier
> ce que faisait la v1 pour passer en v2."
> Decision utilisateur (portee) : **corrections / memoire UNIQUEMENT**.
> Decision utilisateur (methode) : **PRODUIRE LE PLAN D ABORD, le valider,
> AUCUNE execution avant validation utilisateur.**
> Statut : A VALIDER -- ce document ne modifie rien, il planifie.
> v0.2.0 (2026-09-04) : PAC Nemesis integres (avis 69de4af5) - point de
> coupure / gel avant migration, rejouabilite (transaction + UNIQUE +
> INSERT OR IGNORE), anti-doublon A.1/A.2, parse [LECON] v1, backup
> obligatoire, tracabilite mission/outils, perimetre Vision, comptages
> dynamiques, --verifier integre, questions Q6-Q8 ajoutees.
>
> **v0.3.0 (2026-09-05) : SCISSION 2-BDD -- CORRECTION DU PLAN**
> L utilisateur a clarifie que les deux equipes (v1 cerveau-projet, v2
> freelance) sont DISTINCTES et gardent chacune LEUR perimetre et LEUR zone
> de memoire collective. La fusion des memoires (migrer les lecons v1 dans
> bdd-lecons v2) est ANNULEE :
> - les agents v1 gardent LEUR BDD v1 (`cerveau-projet/agents/lecons/lecons.db`,
>   279 lecons, outils v1 restaures `enregistrer-lecon`/`consulter-lecons`) ;
> - bdd-lecons v2 reste la memoire des agents FREELANCE (6 lecons) ;
> - les 279 lecons v1 ont ete retirees de bdd-lecons v2 le 2026-09-05
>   (backup `lecons.db.bak-scission-2bdd-2026-09-05`) et reintegrees en v1 ;
> - ce qui subsiste du plan : le gel des corrections.md v1 (fait), la
>   suppression de corrections.db/corrections-db.py (fait), la finition du
>   cote v2 (etape C, session-freelance, Vision/JARVIS - hors perimetre v1).

---

## 0. SYNTHESE EXECUTIVE

Deux modeles coexistent sans convergence (constat Argus 82151e40) :
- **v1** : corrections.md par agent = memoires PLEINES (accumulation complete,
  contraire a la doctrine corrections-db.md "fenetre courte ~10") + 3 briques
  d infrastructure partagee peu ou plus utilisees (lecons.db, corrections.db,
  corrections-db.py) + protocole E2 de double ecriture abandonne depuis le
  2026-08-18.
- **v2** : corrections PARTAGEES via `bdd-lecons` (lecons.db unique) et
  `corrections.jsonl` (retro-correction auto JARVIS), corrections.md v2 en
  fenetre glissante. Mais la bascule est INCOMPLETE : bdd-lecons ne contient
  que 6 lecons, le backlog corrections.jsonl (1650 EN_ATTENTE) n est pas
  traite, et les corrections.md v2 contiennent encore des [LECON] jusqu au
  2026-08-26.

Le plan converge la memoire des corrections sur le modele v2 :
1. Migrer les lecons v1 (lecons.db, comptage dynamique - 256 au 09-04 09:52)
   + les [LECON] orphelins v1 vers bdd-lecons v2.
2. Geler les corrections.md v1 comme historique (plus d ecriture de [LECON]
   dedans) puis les retirer du cycle de vie.
3. Supprimer l infrastructure v1 devenue sans objet (corrections.db,
   corrections-db.py, lecons.db, outils enregistrer-lecon/consulter-lecons
   cote v1) apres migration verifiee.
4. Reecrire la doctrine (corrections-db.md) et le protocole E2 pour le
   modele v2.
5. Traiter/purger le backlog corrections.jsonl et finir la bascule
   bdd-lecons cote v2.
6. Brancher les agents (v1 restants + v2) sur bdd-lecons comme SEULE source
   de lecons.

HORS PERIMETRE (explicite) : le reste du projet v1 (agents, outils,
parcours, conventions hors corrections) reste EN PLACE. Rien de ce plan ne
concerne une bascule plus large tant que l utilisateur ne la decide pas.

---

## 1. INVENTAIRE DES ACTIFS v1 A TRAITER

| # | Actif | Chemin | Etat reel (09-04) | Sortie proposee |
|---|---|---|---|---|
| A1 | corrections.md par agent | `cerveau-projet/agents/*/corrections.md` (22 agents) | Memoires PLEINES : vulcain 27 [LECON]/644 l., morpheus 26/609, themis 12/310, buffy 15/289, janus 11/154, cerberus 10/370, chiron 10/266, clio 10/182, promethee 10/261, atlas 5/190, argus 4, hygie 7... Accumulation depuis 08-24 au moins ; encore alimentes le 09-04. | GELER comme historique apres migration des [LECON] vers bdd-lecons. Ne plus ecrire de [LECON] dedans (lecons -> bdd-lecons). Fichiers conserves (historique git + relecture), marques "GELE - voir bdd-lecons". |
| A2 | lecons.db v1 | `cerveau-projet/agents/lecons/lecons.db` | Base VIVANTE : 256 lecons au 09-04 09:52 (janus 62, buffy 54, themis 49, vulcain 35, morpheus 30, chiron 7, cerberus 4, clio 4, hygie 3, redacteur-v2 3, gardien 2, socrate 2, atlas 1) - une lecon E2 ecrite pendant le round du 09-04. Derniere entree 2026-09-04 09:52. Schema : id/date/agent/domaine/tags/titre/lecon/mission/outils/verdict. | MIGRER vers bdd-lecons v2 (comptage DYNAMIQUE a l execution, marquage source=v1-lecons.db) puis ARCHIVER le fichier (.bak date verifie obligatoire avant suppression definitive). |
| A3 | corrections.db | `cerveau-projet/agents/corrections.db` | 360 lignes / 19 agents. Import UNIQUE le 2026-09-01 09:38, jamais re-importe. | NE PAS migrer (index de compatibilite depasse). ARCHIVER .bak OBLIGATOIRE puis SUPPRIMER apres validation (PAC-9 : AUCUNE suppression sans .bak date verifie). |
| A4 | corrections-db.py | `cerveau-projet/agents/corrections-db.py` | Outil d import/trim : 0 usage declare au registre (2336 entrees). | ARCHIVER .bak OBLIGATOIRE puis SUPPRIMER : sa fonction est remplacee par bdd-lecons + outil de migration dedie (PAC-9). |
| A5 | corrections-db.md (doctrine) | `cerveau-projet/agents/corrections-db.md` | Documente le modele v1 (corrections.md = memoire courte ~10, lecons.db = longue, corrections.db = index, --trim). | REECRIRE : documenter la decision v2 (les lecons vont dans bdd-lecons) et l etat post-migration (fichiers v1 geles, outil de migration, liens). |
| A6 | Outil enregistrer-lecon | `cerveau-projet/agents/tools/enregistrer/enregistrer-lecon/` | Ecrit dans lecons.db v1 (anti-usurpation --agent). Dernier usage reel hors verrou-auto : 2026-08-18. Reference dans 14+ parcours v1 (P0). | RETIRER du catalogue + des parcours v1 (remplace par bdd-lecons enregistrer). Fichier archive (Vulcain). |
| A7 | Outil consulter-lecons | `cerveau-projet/agents/tools/consulter/consulter-lecons/` | Lit lecons.db v1. Dernier usage 2026-08-17/09-02. Reference dans 79 fichiers parcours v1. | RETIRER du catalogue + des parcours v1 (remplace par bdd-lecons chercher/lister). Fichier archive (Vulcain). |
| A8 | Protocole E2 (fin-mission) | `cerveau-projet/agents/regles-immuables/general/protocole-fin-mission/` | E2 impose : lecon dans corrections.md + AUSSI dans lecons.db via enregistrer-lecon. Non respecte depuis 08-18. | REECRIRE E2 : lecon -> bdd-lecons (outil v2), corrections.md v1 gelee ne recoit plus de lecon. |
| A9 | Agents v1 avec [LECON] hors lecons.db | argus (4), hermes (1), promethee (10) | [LECON] presents dans corrections.md, 0 entree lecons.db. | MIGRER ces [LECON] orphelins vers bdd-lecons (meme passe que A1). |
| A10 | Parcours/fiches v1 mentionnant corrections.md comme memoire | fiches v1 (surcharges.fichier_corrections), AGENTS.md (colonne Corrections) | Tous les agents v1 pointent vers leur corrections.md. | Apres migration : garder le POINTEUR (l historique gele reste lisible), mettre a jour la REGLE d usage (ne plus y ecrire). AGENTS.md : pas de changement de pointeur. |
| A11 | Catalogue outils | `cerveau-projet/agents/catalogue/catalogue-commandes.json` (ou equivalent) | Liste enregistrer-lecon/consulter-lecons. | Retirer les 2 entrees apres retrait effectif (Vulcain). |

---

## 2. ETAT DE LA CIBLE v2 (ce qui existe, ce qui manque)

### 2.1 bdd-lecons (cible principale)

| Element | Etat (09-04) | Constat |
|---|---|---|
| Emplacement | `cerveau-projet/freelance/tools-commun/bdd-lecons/` | Existe : bdd-lecons.md + entry.py + fonctions/bdd_lecons.py + lecons.db |
| lecons.db | 6 lecons seulement (forge 1, shuri 2, stark 3) | Bascule INCOMPLETE : quasi vide alors que la doctrine D10 la designe comme SEUL stockage |
| Contrainte UNIQUE | Absente au schema (id/date/agent/categorie/titre/resume/mots_cles/source) | A AJOUTER (PAC-8) : contrainte UNIQUE (agent+titre+date) au niveau SCHEMA pour garantir la rejouabilite (INSERT OR IGNORE) |
| Colonnes mission/outils | Absentes du schema v2 | Q7 OUVERTE (PAC-7) : soit extension du schema (colonnes mission/outils, Vision), soit fusion complete dans resume avec format parseable - JAMAIS de perte silencieuse |
| Schema v2 | id/date/agent/categorie/titre/resume/mots_cles/source | Compatible v1 -> v2 (voir 3.1 mapping) |
| Commandes entry.py | enregistrer / lister / chercher / compter | Pas de commande "migrer" exposee |
| fonctions/bdd_lecons.py | contient `migrer_depuis_corrections(chemins)` | Fonction interne existante MAIS : (a) non exposee dans entry.py, (b) parse le format [LECON] des corrections.md (pas le schema lecons.db v1). A adapter/completer pour migrer DEPUIS lecons.db v1. |
| Doc bdd-lecons.md | Complete (D10) | A completer : section migration v1 + procedure d import |
| Reference dans les cartes v2 | AUCUN parcours v2 ne reference bdd-lecons | Les agents v2 n ont pas l outil en carte : la bascule v2 est inachevee AUSSI cote habilitations |

### 2.2 corrections.jsonl (retro-correction JARVIS)

| Element | Etat | Constat |
|---|---|---|
| Emplacement | `cerveau-projet/freelance/tools-commun/jarvis/files/corrections.jsonl` | 1653 entrees : 1650 EN_ATTENTE + 3 EN_COURS ; 1648 datees de 2026-08, 5 de 2026-09 |
| Outil | `jarvis/fonctions/corrections.py` (marquer/traiter/terminer) | Protocole : JARVIS traite la file EN PRIORITE ; MAX_ECHECS_PAR_AGENT=3 |
| Nature | Retro-correction AUTO (routine detecte erreur -> correction) | Ce n est PAS une base de lecons : c est une file de corrections a appliquer. Backlog aout = probablement artefacts d une epoque (inbox jarvis) OU corrections jamais traitees |
| Sortie proposee | AUDIT cote v2 (Vision) : trier 1650 EN_ATTENTE -> traiter les reelles, purger les artefacts | Etape D, session-freelance (Vision/JARVIS) |

### 2.3 corrections.md v2 (fenetre glissante)

| Element | Etat | Constat |
|---|---|---|
| 9 fichiers | edith 53 l., forge 83, fury 60, jarvis 199, parker 60, rogers 61, shuri 84, stark 199, vision 424 | Contiennent encore des [LECON] jusqu au 2026-08-26 (vision 16 lecons) : la regle "plus de lecons dans corrections.md" n a pas ete appliquee aux existants |
| Sortie proposee | Definir la fenetre : les [LECON] historiques deja presents y restent-ils ou partent-ils dans bdd-lecons ? | Recommendation : migrer les [LECON] v2 encore presents vers bdd-lecons (un seul modele), corrections.md v2 = regles + contexte + liens, pas d historique |

---

## 3. ETAPES DE MIGRATION (ordonnees)

> Principe : AUCUNE suppression avant migration VERIFIEE + validation
> utilisateur a chaque jalon majeur. Les etapes A1-A2 sont independantes de
> la v2 ; A3-A5 dependent de A1-A2 ; D est cote v2.

### Etape A -- Migrer les lecons v1 vers bdd-lecons v2

| Sous-etape | Action | Agent habilite | Critere de succes | Risque |
|---|---|---|---|---|
| A.1 | ETENDRE la fonction existante `migrer_depuis_corrections` en `migrer_depuis_lecons_db` (PAC-4) : lire les lecons de `agents/lecons/lecons.db` (v1) et les inserer dans `freelance/tools-commun/bdd-lecons/lecons.db` avec mapping : date->date, agent->agent, domaine/tags->mots_cles, titre->titre, lecon->resume, source='v1-lecons.db'. Categorie derivee du domaine/verdict (defaut 'correction'). REJOUABILITE (PAC-8) : transaction SQLite (BEGIN/COMMIT, rollback sur erreur) autour de la migration complete + contrainte UNIQUE au schema v2 (agent+titre+date) + INSERT OR IGNORE. COMPTAGES DYNAMIQUES (PAC-5) : SELECT COUNT source puis cible a l execution (aucun nombre fige du document), avec echantillon de controle. COMMANDE --verifier INTEGREE (PAC-6) : comptage source/cible, doublons, echantillon. TRACABILITE (PAC-7) : selon Q7 - colonnes mission/outils ou fusion parseable dans resume, jamais de perte. | Vulcain (outil, session-admin) + Vision (VALIDE et EXECUTE l ecriture dans bdd-lecons, session-freelance - PAC-10 : un outil v1 qui ecrit dans freelance/ sans validation Vision est une violation de perimetre) | Comptage DYNAMIQUE source/cible identique, 0 perte, 0 doublon (UNIQUE schema), --verifier vert, ASCII OK, test crash/re-jeu (D.3) | Doublons si re-joue SANS transaction/UNIQUE ; mapping partiel (champs v1 sans equivalent v2) |
| A.2 | Migrer les [LECON] orphelins v1 (argus 4, hermes 1, promethee 10) non presents dans lecons.db v1. ANTI-DOUBLON (PAC-2) : source UNIQUE par lecon (identifiant stable date+agent+titre) + logique explicite de detection des orphelins (verifier qu une lecon de corrections.md n est PAS deja dans lecons.db v1 avant migration) ; ne lancer `migrer_depuis_corrections` QUE sur les corrections.md des 3 agents orphelins, JAMAIS sur les 22. PARSE (PAC-3) : adapter le parse au format reel v1 (**Contexte**/**Actions**/**Lecon**/**Validations**, pas seulement **Tache**/**Erreur**) OU migrer via lecons.db v1 apres injection (source structuree) ; verifier la categorie derivee (pas seulement le mot ERREUR). | Vulcain/Vision + Buffy (coordination) | 15 lecons orphelines en plus dans bdd-lecons, 0 doublon avec A.1, source = corrections.md (ou lecons.db apres injection) | Format de parse [LECON] variable selon agent (a verifier sur echantillon) |
| A.3 | Verifier l integralite : comptage DYNAMIQUE a l execution (SELECT COUNT lecons.db v1 + orphelins + v2 existantes -> total cible attendu), requete de controle par agent, rapport de migration ; executer la commande --verifier de l outil (PAC-6). | Morpheus (test) ou Janus (controle) - ils EXECUTENT --verifier comme controle croise | Comptage dynamique source/cible identique, 0 doublon, 0 lecon perdue, echantillon documente | Ecart de comptage |
| A.4 | Archiver lecons.db v1 : copie `lecons.db.bak-2026-09-04` conservee, fichier original marque archive. | Hygie (copie/archive) | .bak present, original intact | - |

### Etape B -- Geler les corrections.md v1 et retirer l infra v1

| Sous-etape | Action | Agent habilite | Critere de succes | Risque |
|---|---|---|---|---|
| B.1 | Geler les 22 corrections.md v1 : ajouter en tete un bandeau "MEMOIRE GELEE le 2026-09-04 - les nouvelles lecons vont dans bdd-lecons (outil v2). Historique conserve pour relecture." AUCUN [LECON] supplementaire. | Buffy (fichiers structurels agents) | 22 bandeaux poses, ASCII OK, 0 nouveau [LECON] apres gel | Agents continuant d ecrire dedans (habitude) -> garde-fou |
| B.2 | Reecrire le protocole E2 (protocole-fin-mission) : la lecon va dans bdd-lecons (commande v2), plus AUCUNE ecriture dans corrections.md v1 gele ; mention du gel pour les agents v1 restants. | Buffy (regles-immuables) | E2 conforme modele v2, test-048 adapte (le garde-fou verifiait corrections.md) | test-048 casse si non adapte -> Morpheus |
| B.3 | Reecrire corrections-db.md : documenter la decision utilisateur (v1 -> v2), l etat post-migration (fichiers v1 geles, lecons.db archive, corrections.db supprime), pointer vers bdd-lecons. | Buffy | corrections-db.md = doc de transition, plus doctrine active | - |
| B.4 | Retirer enregistrer-lecon / consulter-lecons du catalogue + des parcours v1 (14+ fichiers parcours les listent en P0) et archiver les dossiers outils. | Vulcain (outils + catalogue), Buffy (parcours v1 si besoin via editer-parcours) | 0 reference active aux 2 outils, dossiers archives, catalogue a jour | Parcours v1 proteges marbre -> passer par editer-parcours ou archiver les parcours (voir hors perimetre) |
| B.5 | Supprimer (apres A.4) : corrections.db, corrections-db.py. | Hygie (suppression) apres validation | Fichiers supprimes APRES .bak date verifie (PAC-9 : archive OBLIGATOIRE, pas d option - meme pour un index obsolete) | Si des outils/tests les reference -> detecter-impacts avant + .bak |

> NOTE B.4 : les parcours v1 sont des archives protegees par le marbre.
> Deux options : (a) retirer les 2 outils des parcours via editer-parcours
> (Buffy), (b) laisser les parcours v1 tels quels (ils ne pilotent plus, les
> arbres v2 pilotent) et ne retirer que catalogue + fichiers outils. A
> trancher a l execution selon l etat reel des arbres v2 (recommandation :
> (b) d abord, (a) seulement si un parcours v1 pilote encore).

### Etape C -- Finir la bascule cote v2

| Sous-etape | Action | Agent habilite | Critere de succes | Risque |
|---|---|---|---|---|
| C.1 | Brancher bdd-lecons dans les parcours v2 (les agents v2 doivent avoir l outil en carte pour enregistrer/chercher) et dans le flux JARVIS (commande d enregistrement de lecon en fin de mission). | Vision (exclusif JARVIS/bdd-lecons cote v2) | Outil reference dans les cartes v2 + flux fin de mission v2 | Perimetre v2 : tout passe par JARVIS, Vision exclusif |
| C.2 | Migrer les [LECON] encore presents dans les corrections.md v2 (jusqu au 08-26) vers bdd-lecons OU les declarer historiques conserves. | Vision | Decision explicite : migre ou conserve, 0 ambiguite | Doublons avec A.1 si lecons v1 deja migrees |
| C.3 | Traiter/purger le backlog corrections.jsonl (1650 EN_ATTENTE) : AUDIT OBLIGATOIRE D ABORD (PAC-11) avec echantillon prouve (date, origine, contenu), trier reelles vs artefacts (1648 datees 08-2026 = artefacts probables, 5 datees 09-2026 = potentiellement reelles), traiter les reelles via le flux JARVIS, purger les artefacts APRES .bak du fichier. | Vision/JARVIS | 0 EN_ATTENTE fantome, seules les corrections reelles restent, .bak present avant purge, echantillon d audit documente | Purge d une correction reelle -> audit + .bak avant purge |
| C.4 | Mettre a jour bdd-lecons.md : section migration, commande d import exposee, procedure. | Vision | Doc complete | - |

### Etape D -- Garde-fous et tests

| Sous-etape | Action | Agent habilite | Critere de succes | Risque |
|---|---|---|---|---|
| D.1 | Adapter test-048 (garde-fou protocole-fin-mission) : il verifie que chaque mission a sa lecon + verdict dans corrections.md de l agent -> doit verifier la presence dans bdd-lecons (ou dans l historique gele pour les missions pre-migration). | Morpheus | test-048 vert sur le nouveau modele | KO massifs si mal adapte |
| D.2 | Nouveau garde-fou : verifier qu AUCUN [LECON] n est ajoute dans les corrections.md v1 gelees (anti-regression du gel). | Morpheus (+Vulcain si outil) | Detection d une ecriture post-gel | - |
| D.3 | Test de la migration : fixture lecons.db v1 -> bdd-lecons v2, comptage, doublons, mapping. | Morpheus | Test vert | - |
| D.4 | Non-regression complete (tester-lancer-non-regression) apres retrait des 2 outils + reecriture E2. | Morpheus | 0 nouveau KO (hors artefacts documentes) | Parcours v1 references |

### Etape E -- Cloture

| Sous-etape | Action | Agent habilite | Critere de succes |
|---|---|---|---|
| E.1 | Rapport final de migration (comptages, fichiers touches, decisions) | Buffy (coordination) | Document complet |
| E.2 | Bilan consolide a l utilisateur + mise a jour AGENTS.md / activite | Cerberus/Oracle | Validation utilisateur finale |

---

## 4. DEPENDANCES ENTRE ETAPES

```
PAC-1 (CRITIQUE) : lecons.db v1 est VIVANTE (256 lecons le 09-04 09:52,
une lecon E2 ecrite pendant le round precedent) -> OPTION A : B.1+B.2
(gel corrections.md + coupure E2) AVANT A (migration), OU OPTION B : point
DE COUPURE horodate explicite + verification de fermeture (aucune ecriture
entre snapshot et migration). Sans cela, toute lecon ecrite pendant A est
PERDUE. La coupure E2 (bloquer enregistrer-lecon v1) est obligatoire dans
les deux options.

A.1+A.2 (migration lecons, rejouable: transaction+UNIQUE+INSERT OR IGNORE)
--> A.3 (verification, comptages dynamiques + --verifier) --> A.4 (archive
lecons.db .bak) |
                                                          |
B.1 (gel corrections.md) <-- validation A ----------------+---> B.2 (E2) + B.3 (doctrine)
                                                          |
B.4 (retrait outils) <--- B.2 (E2 ne reference plus enregistrer-lecon)
B.5 (suppression corrections.db/corrections-db.py) <--- A.4 + .bak obligatoire + validation
C.1+C.2+C.3+C.4 (v2) : independants de A/B cote files, mais C.1 doit preceder
   toute nouvelle lecon v2 (sinon les agents v2 ecrivent encore dans
   corrections.md). C.3 (backlog) independant, .bak avant purge.
D.1-D.4 (garde-fous) : D.1 doit suivre B.2 (E2 change) ; D.3 doit suivre
   A.1 (migration) + couvrir le cas crash/re-jeu (PAC-8) ; D.4 en fin de chaine.
E.1-E.2 : cloture.
```

- **Session-admin (v1)** : A (sauf ecriture lecons.db v2 -> Vision), B, D.
- **Session-freelance (v2)** : C (Vision exclusif JARVIS/bdd-lecons).
- **Ferrari** (couche v1 sur freelance) : si une intervention v1 dans
  `freelance/` est necessaire hors Vision (ex: ajustement de doc), passer par
  ferrari ; sinon Vision fait le travail v2 directement en session-freelance.
- Le plan peut etre execute en 2 vagues : vague 1 (session-admin : A+B+D,
  apres validation), vague 2 (session-freelance : C, apres validation ou en
  parallele si Vision disponible).

---

## 5. AGENTS HABILITES PAR ETAPE (matrice)

| Agent | Role dans ce plan | Justification (regles-groupes-agents / regles-choisir-agent) |
|---|---|---|
| **Vision** | C.1-C.4 (bdd-lecons, corrections.jsonl, cartes v2) | SEUL habilite a modifier JARVIS et les outils v2 (exclusivite Vision) |
| **Buffy** | B.1-B.3 (gel corrections.md v1, E2, corrections-db.md), coordination du plan | SEULE habilitee a corriger les fichiers structurels des agents (fiches, protocoles, regles) |
| **Vulcain** | A.1-A.2 (outil/methode de migration), B.4 (retrait outils + catalogue) | Constructeur d outils (creer/modifier/retirer un outil) |
| **Morpheus** | A.3 (verif comptage), D.1-D.4 (tests, garde-fous, non-regression) | Testeur dedie (protocole-tests) |
| **Janus** | Controle croise optionnel (A.3 alternative) | Second controle des statuts |
| **Hygie** | A.4 (archive), B.5 (suppression) | SEUL habilite a TOUT le workspace et a supprimer sans demande prealable |
| **Gardien** | Verification des zones protegees (marbre : parcours v1, regles-immuables) | SEUL a proposer la modification des zones protegees (l utilisateur valide) |
| **Oracle/Cerberus** | Routage, historisation, bilan consolide | Coordination |
| **Argus** | (deja fait) constat initial 82151e40 | Detecteur |

---

## 6. CRITERES DE VALIDATION DU PLAN

L utilisateur valide ce plan si :
1. La portee est correcte : corrections/memoire UNIQUEMENT, rien d autre ne
   bouge dans le projet v1.
2. Aucune donnee n est perdue : comptage DYNAMIQUE (PAC-5) a l execution
   (SELECT COUNT source lecons.db v1 + orphelins + v2 existantes -> total
   cible), verifie par comptage avant/apres + echantillon + test - AUCUN
   nombre fige du document.
3. Rien n est supprime avant d etre migre et verifie (.bak date verifie
   OBLIGATOIRE avant TOUTE suppression - PAC-9).
4. Le modele cible est clair : bdd-lecons = SEULE source des lecons ;
   corrections.md (v1 geles, v2 fenetre) ne recoivent plus de [LECON].
5. La migration est REJOUABLE (PAC-8) : transaction SQLite + contrainte
   UNIQUE au schema + INSERT OR IGNORE + test crash/re-jeu (D.3).
6. La source est FERMEE avant/ pendant la migration (PAC-1) : gel B.1+B.2
   avant A ou cutoff horodate + verif de fermeture - 0 lecon ecrite entre
   snapshot et migration.
7. Aucune perte de tracabilite (PAC-7) : mission/outils/verdict conserves
   (colonnes v2 ou fusion parseable), decide par Q7.
8. Les garde-fous sont adaptes (test-048) et de nouveaux garde-fous empechent
   la regression (ecriture post-gel detectee).
9. La v2 est finie : bdd-lecons branche dans les cartes v2, backlog
   corrections.jsonl audite + .bak avant purge (PAC-11).
10. Les agents habilites par etape sont corrects (Vision exclusif v2 et
    VALIDE l ecriture v2 - PAC-10, Buffy structurel, Vulcain outils,
    Morpheus tests, Hygie suppression).
11. Le plan est executable en vagues (v1 puis v2) sans blocage croise.

CE QUI NE SERA PAS FAIT (hors perimetre) :
- Aucune bascule des agents v1 vers la v2 (pas de suppression d agents v1,
  pas de migration des fiches/parcours/outils v1 hors corrections).
- Aucune modification des conventions/regles/protocoles hors ceux de la
  memoire des corrections (E2, corrections-db.md).
- Aucune decision sur le sort global du projet v1 (session-admin) vs v2
  (session-freelance) : le reste du projet v1 reste en place.
- Aucun changement de JARVIS hors corrections.jsonl/bdd-lecons (Vision
  decide).

---

## 7. QUESTIONS OUVERTES POUR L UTILISATEUR (a trancher avant execution)

1. Les corrections.md v1 geles sont-ils CONSERVES en l etat (recommandation :
   oui, historique lisible + git) ou doivent-ils etre purges une fois migres ?
2. Les 10 [LECON] de promethee et les autres orphelins (argus 4, hermes 1)
   sont-ils tous a migrer, ou certains sont-ils obsoletes (a verifier avant) ?
3. Les [LECON] encore presents dans les corrections.md v2 (jusqu au 08-26) :
   a migrer dans bdd-lecons ou declares historiques conserves tels quels ?
4. Le backlog corrections.jsonl (1650 EN_ATTENTE) : a traiter reellement ou
   a purger comme artefacts (recommandation : audit Vision d abord + .bak) ?
5. Validation du plan en 2 vagues (session-admin A+B+D puis session-freelance
   C) ou une seule validation globale avant tout ?
6. (Nemesis Q6) Le gel (B.1/B.2, incluant la coupure E2) passe-t-il AVANT la
   migration (A) ou un point de coupure horodate est-il defini ? (recommandation :
   gel AVANT - lecons.db v1 vivante, PAC-1)
7. (Nemesis Q7) Le schema v2 recoit-il les colonnes mission/outils (extension
   Vision) ou la tracabilite est-elle fusionnee en texte ? (recommandation :
   colonnes - tracabilite requetable, PAC-7)
8. (Nemesis Q8) corrections.db est-il archive (obligatoire) ou supprime sans
   archive ? (recommandation : archive OBLIGATOIRE, PAC-9)

---

## 8. DECLARATION DE NON-EXECUTION

Ce document est un PLAN. Aucun fichier cible n a ete modifie, supprime ou
migre : constat Argus (82151e40) lu, inventaires mesures (lecons.db v1 256,
corrections.db 360, corrections.md 22, bdd-lecons v2 6, corrections.jsonl
1653), outil bdd-lecons v2 inspecte (entry.py + bdd_lecons.py, fonction
migrer_depuis_corrections existante non exposee), avis Nemesis (69de4af5,
11 PAC) integre en v0.2.0 (gel/coupure avant migration, rejouabilite,
anti-doublon, parse v1, backup obligatoire, tracabilite, perimetre Vision,
comptages dynamiques, questions Q6-Q8). Le plan attend la validation
utilisateur avant toute execution.
