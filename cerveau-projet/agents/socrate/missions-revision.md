# Missions de Revision -- 2026-09-04

> Revision strategique (mission bb512aac). Demande utilisateur : traiter les
> questions ouvertes Q1-Q8 du plan de migration v1->v2 (perimetre
> corrections/memoire) avant validation. Contexte : plan Buffy v0.1.0
> (attente validation), avis Nemesis (11 PAC, 2 critiques), constat Argus
> (82151e40), decision utilisateur "on passe de v1 a v2, on oublie la v1".
> Portee RESTREINTE aux questions Q1-Q8 (lecon 2026-09-02 : ne pas
> re-synthetiser tout le round).

## Resume

| Niveau | Nombre |
|---|---|
| URGENT | 2 |
| IMPORTANT | 3 |
| MOYEN | 1 |
| BAS | 2 |

---

## PARTIE A -- RECOMMANDATIONS Q1-Q8 (pour decision utilisateur)

> Pour chaque question : RECOMMANDATION + justification + risque si
> decision contraire.

### Q1. Corrections.md v1 geles : conserver ou purger ?

**RECOMMANDATION : CONSERVER en l etat (historique lisible + git).**

- Pourquoi : la memoire v1 est un historique de travail utile a la
  relecture et a la tracabilite des decisions ; le gel suffit a arreter
  l accumulation (bandeau + 0 nouveau [LECON]).
- Risque si purge : perte irreversible d un contexte (lecons anciennes,
  defaillances documentees) sans gain fonctionnel reel (les fichiers ne
  coutent rien une fois geles).
- Alignement : "oublier la v1" ne signifie pas detruire sa memoire, mais
  arreter de l alimenter et basculer la production de lecons sur bdd-lecons.

### Q2. Les [LECON] orphelins (argus 4, hermes 1, promethee 10) : tous a migrer ?

**RECOMMANDATION : MIGRER TOUS les 15, APRES un controle d obsolescence rapide.**

- Pourquoi : les lecons d argus/hermes/promethee sont recentes (aout-sept)
  et coherentes avec le corpus ; aucune evidence d obsolescence dans le
  constat Argus.
- Nuance : avant migration, promethee (10) doit etre verifie par
  echantillon (certaines peuvent etre des doublons de lecons deja dans
  lecons.db v1) - l etape A.2 (anti-doublon PAC-2) le couvre.
- Risque si migration selective : choisir "obsolete" sans critere objectif
  introduit un biais de jugement ; migrer tout puis purger a la relecture
  est plus sur (rien n est perdu).

### Q3. [LECON] restants dans les corrections.md v2 (jusqu au 08-26) : migrer ou conserver ?

**RECOMMANDATION : MIGRER dans bdd-lecons (un seul modele), corrections.md
v2 = regles + contexte + liens, pas d historique.**

- Pourquoi : c est la doctrine D10 de la v2 elle-meme ("plus de lecons dans
  corrections.md"). Garder des [LECON] historiques dans les corrections.md
  v2 maintient DEUX sources de memoire (contradiction avec la cible unique
  bdd-lecons).
- Risque si conserve : le modele reste hybride, les agents v2 continueront
  de chercher les lecons dans corrections.md.
- Condition : migration des [LECON] v2 AVANT ou pendant A.1 (source
  supplementaire), avec anti-doublon contre les lecons deja migrees depuis
  lecons.db v1 (PAC-2).

### Q4. Backlog corrections.jsonl (1650 EN_ATTENTE) : traiter ou purger ?

**RECOMMANDATION : AUDIT VISION D ABORD (obligatoire), puis TRAITER les
reelles et PURGER les artefacts, avec .bak avant purge.**

- Pourquoi : 1648 entrees datees de 2026-08 (artefacts probables d une
  epoque), 5 de 2026-09 (potentiellement reelles). Purger sans audit =
  supprimer une correction reelle sans preuve ; traiter sans trier = 1650
  entrees inutiles consomme JARVIS.
- Risque : une correction reelle purgee par erreur (d ou le .bak + audit
  avec echantillon prouve, PAC-11).
- Alignement : la retro-correction automatique reste un mecanisme de la v2 ;
  seul le BACKLOG historique est a assainir.

### Q5. Validation en 2 vagues ou globale ?

**RECOMMANDATION : 2 VAGUES (session-admin A+B+D puis session-freelance C),
avec validation utilisateur a CHAQUE jalon majeur.**

- Pourquoi : A+B+D (v1) et C (v2) ont des dependances faibles (C.1 doit
  preceder toute nouvelle lecon v2, mais A/B n attendent pas C) ; separer
  permet de valider la migration v1 avant de toucher la v2, et de corriger
  a la lumiere des resultats reels.
- Risque si validation globale : un blocage cote v2 (Vision indisponible,
  backlog) retarde toute la migration v1.
- Condition : jalon 1 = validation du plan ajuste (0.2.0) ; jalon 2 =
  validation de la migration A (comptages, .bak) avant B ; jalon 3 =
  validation C cote v2.

### Q6. (Nemesis) Gel avant migration ou point de coupure ?

**RECOMMANDATION : GEL AVANT MIGRATION (B.1/B.2 AVANT A) - option la plus
sure ; alternative : cutoff horodate + verification de fermeture.**

- Pourquoi : lecons.db v1 est VIVANTE (256 lecons le 09-04, une lecon
  ecrite pendant le round precedent). Migrer une source qui s ecrit
  pendant la migration = fuite de donnees certaine (PAC-1, critique).
- Le gel doit inclure la coupure E2 (bloquer enregistrer-lecon v1) : sans
  cela, les agents v1 continuent d ecrire dans lecons.db pendant A.
- Risque si on garde l ordre actuel (A avant B) : perte des lecons ecrites
  entre le snapshot et la fin de la migration.

### Q7. (Nemesis) Colonnes mission/outils au schema v2 ou fusion texte ?

**RECOMMANDATION : EXTENSION DU SCHEMA v2 (colonnes mission + outils),
validee par Vision.**

- Pourquoi : la tracabilite (quelle mission, quels outils) est la valeur de
  la base de lecons : elle sert aux evaluations croisees, aux statistiques
  par outil et a la verification E2. La fusion texte (resume) rend ces
  donnees non requetables et non verificables.
- Cout : extension du schema bdd-lecons (Vision, session-freelance) +
  adaptation de l outil de migration - cout borne, valeur durable.
- Risque de la fusion : perte silencieuse (PAC-7) - les lecons migrees
  perdent leur contexte operationnel.

### Q8. (Nemesis) corrections.db : archive ou suppression sans archive ?

**RECOMMANDATION : ARCHIVE OBLIGATOIRE (.bak date verifie avant
suppression), meme pour un index obsolete.**

- Pourquoi : la regle de securite doit etre SANS exception (PAC-9) ; un
  .bak ne coute rien et permet un re-traitement si un outil/tests
  reference encore corrections.db.
- Risque de la suppression directe : un outil qui lit corrections.db casse
  sans possibilite de retour (detecter-impacts avant, mais le .bak reste la
  ceinture de securite).

---

## PARTIE B -- LISTE DE MISSIONS POUR CERBERUS (a lancer apres decisions)

### [URGENT] Integrer les PAC Nemesis dans le plan de migration (Buffy) - EN COURS

- **Agent habilite** : buffy
- **Description** : mettre a jour plan-migration-corrections-v1-v2-2026-09-04.md
  vers 0.2.0 avec les 8 PAC (coupure, rejouabilite, anti-doublon, parse,
  backup, tracabilite, perimetre v2, optimisations) + ajouter Q6/Q7/Q8 a la
  section 7.
- **Raison** : le plan ne doit pas etre valide en l etat (2 critiques).
- **Dependances** : avis Nemesis (fait, 69de4af5).
- **Critere de succes** : plan 0.2.0, ASCII strict, aucune execution.

### [URGENT] Troncher les decisions Q1-Q8 avec l utilisateur (Cerberus)

- **Agent habilite** : cerberus (routeur, retour utilisateur)
- **Description** : presenter les recommandations Q1-Q8 (Partie A) a
  l utilisateur et recueillir ses decisions.
- **Raison** : aucune execution possible avant decisions (plan non valide).
- **Dependances** : ce rapport + plan 0.2.0 (Buffy).
- **Critere de succes** : decisions utilisateur explicites Q1-Q8.

### [IMPORTANT] Migrer les lecons v1 (A.1) avec rejouabilite et anti-doublon (Vulcain + Vision)

- **Agent habilite** : vulcain (outil) + vision (ecriture bdd-lecons v2)
- **Description** : apres decisions (Q6 gel d abord) : outil de migration
  (etendre migrer_depuis_corrections en migrer_depuis_lecons_db),
  transaction SQLite, contrainte UNIQUE, INSERT OR IGNORE, comptages
  dynamiques, --verifier integre.
- **Raison** : lecons.db v1 vivante (256) ; PAC-1/8/4/5/6.
- **Dependances** : decisions Q6/Q7 + gel (B.1/B.2) + plan 0.2.0.
- **Critere de succes** : 0 perte, 0 doublon, comptage source/cible, .bak.

### [IMPORTANT] Adapter test-048 + nouveaux garde-fous (Morpheus)

- **Agent habilite** : morpheus
- **Description** : adapter test-048 (lecon dans bdd-lecons au lieu de
  corrections.md), garde-fou anti-ecriture post-gel, test de migration
  (fixture, crash/re-jeu), non-regression complete.
- **Raison** : E2 change (B.2) ; PAC-8 (test rejouabilite) ; D.1-D.4.
- **Dependances** : plan 0.2.0 + decisions + execution A/B.
- **Critere de succes** : tests verts sur le nouveau modele.

### [IMPORTANT] Finir la bascule cote v2 (Vision) - C.1-C.4

- **Agent habilite** : vision (exclusif JARVIS/bdd-lecons v2)
- **Description** : brancher bdd-lecons dans les cartes v2 + flux JARVIS,
  migrer les [LECON] v2 restants, traiter/purger corrections.jsonl (audit +
  .bak), mettre a jour bdd-lecons.md.
- **Raison** : bascule v2 inachevee (6 lecons seulement, backlog 1650).
- **Dependances** : decisions Q3/Q4 + jalon 1 valide.
- **Critere de succes** : outil en carte v2, backlog assaini, doc complete.

### [MOYEN] Archive et retrait infra v1 (Hygie + Vulcain) - A.4/B.4/B.5

- **Agent habilite** : hygie (archive/suppression) + vulcain (retrait
  catalogue/parcours)
- **Description** : .bak lecons.db v1 (A.4), retrait enregistrer-lecon/
  consulter-lecons du catalogue + parcours (B.4), suppression corrections.db
  et corrections-db.py apres .bak (B.5).
- **Raison** : PAC-9 (backup obligatoire) ; retrait de l infra v1 sans objet.
- **Dependances** : A verifie (comptages) + decisions Q8 + plan 0.2.0.
- **Critere de succes** : .bak presents, 0 reference active aux outils retires.

### [BAS] Reecrire la doctrine et E2 (Buffy) - B.2/B.3

- **Agent habilite** : buffy
- **Description** : reecrire protocole-fin-mission E2 (lecon -> bdd-lecons)
  et corrections-db.md (doc de transition, plus doctrine active).
- **Raison** : le modele v1 documente n est plus la cible.
- **Dependances** : decisions + execution A.
- **Critere de succes** : E2 et corrections-db.md conformes v2.

### [BAS] Gel des corrections.md v1 (Buffy) - B.1

- **Agent habilite** : buffy
- **Description** : bandeau "MEMOIRE GELEE" sur les 22 corrections.md v1 +
  arret des ecritures de [LECON].
- **Raison** : PAC-1 (couper la source vivante avant migration).
- **Dependances** : decision Q1 (conserver).
- **Critere de succes** : 22 bandeaux, 0 nouveau [LECON] apres gel.

---

## Verdict de la revision

8/8 questions traitees avec recommandation. Le plan v0.1.0 n est PAS
validable en l etat : attendre plan 0.2.0 (PAC integres, Buffy) et les
decisions utilisateur Q1-Q8 avant toute execution. Priorite : decisions
(URGENT) > gel+migration (IMPORTANT) > v2 (IMPORTANT) > retrait infra
(MOYEN) > doctrine (BAS).