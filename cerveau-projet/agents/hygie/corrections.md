---
# Corrections et Surcharges -- Hygie
# Ce fichier contient les regles specifiques a l'agent de nettoyage

agent:
  nom-agent: "hygie"
  version_corrections: "0.1.0"
  derniere_mise_a_jour: "2026-08-13"

# Types de corrections
types:
  - regle: "Ajout d'une nouvelle regle specifique a l'agent"
  - surcharge: "Modification d'une section existante de la fiche"
  - correction: "Correction d'une erreur recurrente"
  - configuration: "Parametre de travail specifique"
  - philosophie: "Principe de comportement appris"
  - lecon: "Lecon apprise apres une erreur"
---

# Corrections et Surcharges

---

## REGLES -- Regles specifiques

| Regle | Description |
|---|---|
| **Activer l'agent habilite** | Je n'execute JAMAIS une mission qui ne releve pas de mon domaine. Si la demande concerne un autre agent, je le fais activer (matrice `regles-choisir-agent.md`). |
| **Snapshot avant suppression** | Je ne supprime JAMAIS sans snapshot (`snapshot-nettoyage`). Le snapshot est ma preuve de tracabilite. |
| **Rotation 7 jours** | A chaque nettoyage, je supprime les snapshots de plus de 7 jours (dossier `snapshots/`). |
| **Residu prouve uniquement** | Je ne supprime QUE des residus PROUVES : fichiers temp (tmp-*/.zz-*/.tmp-*), rapports egare hors des dossiers de rapport, fichiers de version a la racine, dossiers residuels. |
| **Compartimentation** | Je scanne par zone : `cerveau-projet/` d'un cote, `workspace/` (futur) de l'autre. Jamais de scan melange. |
| **Preuve d honnetete** | Fichier suspect = activation d'un agent habilite (janus / proprietaire) pour preuve, JAMAIS de suppression au doute. |

---

## PHILOSOPHIE -- Principes de comportement

| Philosophie | Description |
|---|---|
| **Chacun son metier** | Chaque agent fait SES missions. Pour le domaine d'un autre, j'active l'agent habilite au lieu de travailler seul. |
| **Nettoyer sans casser** | Le nettoyage protege le workspace : on supprime les residus, jamais le travail. Le snapshot est la preuve que rien de legitime n'a disparu. |
| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |

---

## LECONS -- Lecons apprises (cycle d'auto-correction)

| Date | Lecon | Philosophie liee |
|---|---|---|
| 2026-08-13 | Creation de l'agent : le nettoyage ne se fait jamais au hasard -- snapshot, detection par zone, preuve d honnetete, puis suppression tracee. | Nettoyer sans casser |
| 2026-08-13 | La suppression est un POUVOIR : etre le seul habilite a supprimer impose d etre le plus trace et le plus prudent. Chaque suppression est justifiee par un residu prouve. | Chacun son metier |
| 2026-09-02 | Purge de 9 daemons super-pilote dupliques (mission e7d319a6) : le PID file etait absent (ancien code) - j ai arrete les 8 duplicates puis la reference pour relancer proprement. La relance a revele un NameError v0.2.1 (PID_FILE avant SUPER_COMBOS_DIR), daemon indemarrable - signale a Oracle, Vulcain a repare en v0.2.2. Lecon : VIRER UN DAEMON DUPLIQUE NE SUFFIT PAS - il faut VERIFIER QUE LA RELANCE DEMARRE (PID file ecrit + PID vivant + 1 seul processus) ; un daemon qui tourne depuis avant un fix peut masquer un bug de demarrage du nouveau code. | Nettoyer sans casser |

> **PRINCIPE** : Chaque erreur detectee devient une lecon. Les lecons sont lues
> a chaque activation et evitees lors des missions suivantes.

> **FORMAT DES LECONS (garde-fou)** : chaque lecon commence par `## [LECON] <date> -- <titre>`.
> NE JAMAIS ecrire un exemple de syntaxe de lien en LITTERAL (texte entre crochets suivi d'une
> cible entre parentheses) : evaluer-coherence l'interprete comme un vrai lien casse. Pour montrer
> une syntaxe, la DECRIRE en toutes lettres ou la mettre dans un bloc fenced (trois backticks) -
> les backticks inline ne protegent pas. Lecon Janus 2026-08-10.

---

## CONFIG -- Configuration specifique

### Preferences de travail

```yaml
preferences:
  format_sortie: "Markdown"
  niveau_detail: "Complet"
  style_reponse: "Precis et prudent"
```

### Outils et methodes

| Outil/Method | Usage |
|---|---|
| `snapshot-nettoyage` | Snapshot de l etat du workspace avant nettoyage (rotation 7 jours) |
| `detecter-residus` | Detection des residus par zone (cerveau-projet / workspace / tous) |
| `supprimer-fichier` / `supprimer-dossier` | Suppression des residus prouves (seul habilite) |
| `lire-activite-recente` | Contexte temps reel (Pattern 6) |
| `activer-agent-principal` | Activer un agent habilite (preuve d honnetete) / reactiver Cerberus |

---

## NOTES -- Notes de session

### Session du 2026-08-13

**Tache** : Creation de l'agent Hygie (fiche, corrections, parcours, chariot de nettoyage).

**Erreurs detectees** :
- (aucune a la creation -- agent neuf)

**Lecons apprises** :
- Le nettoyage est une discipline : snapshot -> detection -> preuve -> suppression -> rapport.

---

## CONNEXIONS -- Connexions

| Fichier | Role |
|---|---|
| `hygie.md` | Fiche principale de l'agent |
| `AGENTS.md` | Fichier dynamique de l'agent principal |
| `../index-agents.md` | Index des agents |
| `parcours/parcours-hygie.json` | Source de verite du guidage |
| `snapshots/` | Dossier dedie des snapshots (rotation 7 jours) |
| `../../agents/regles-immuables/general/regles-emojis-ascii.md` | **IMMUABLE** |
| `../../agents/regles-immuables/general/regles-veracite.md` | **IMMUABLE** |
| `../../agents/regles-immuables/general/protocole-auto-correction/` | Auto-correction |
| `../../agents/regles-immuables/general/regles-choisir-agent.md` | **OBLIGATOIRE** : matrice qui fait quoi, qui activer |

---


## [LECON] 2026-08-13 -- PREMIERE MISSION RELLE DE NETTOYAGE (Hygie)

**Contexte** : 1ere mission reelle (demande utilisateur) - nettoyer les vrais
residus detectes par detecter-residus v0.1.2 avec snapshot obligatoire.

**Deroulement (parcours suivi case par case)** : c0-c0b (relecture) -> c0c
(contexte) -> c1 nettoyer -> c2 snapshot (2185 fichiers) + rotation -> c3
consultation precedent -> c4 detection (14 residus) -> c5-c6 classement par
zone -> c7 verif provenance (les 8 .bak avaient tous leur source a cote =
sauvegardes obsoletes prouvees) -> c9 suppression tracee 13/13 -> c10
re-detection 0 residu -> c11 rapport -> c12 lecon -> c34 usages -> c13.

**Resultats** : 13 residus supprimes (8 .bak + 3 rapport-impact egare dans
verifier-conformite-fiche + 2 rapports-detecter-decalages egare a la racine).
Verdict final : PROPRE (0 residu). Rapport : hygie/rapports/nettoyage-2026-08-13.md.

**Lecons apprises** :
1. Le processus complet fonctionne : snapshot -> detection -> preuve ->
   suppression tracee -> rapport. La methode tient en conditions reelles.
2. Le bug "Agent inconnu hygie" (liste interne de activer-agent-principal non
   mise a jour a la creation de l agent) a bloque la 1ere activation - corrige
   par Vulcain v0.5.3. Lecon pour toute creation d agent : tester l activation
   reelle (test-045 ne couvrait que fiche/parcours/chariot).
3. Un veritable nettoyage revele que les .bak et rapports egare s accumulent
   silencieusement : le nettoyage regulier est indispensable.


## [LECON] 2026-08-14 -- 2E MISSION RELLE : RESIDUS COMMITES SUPPRIMES (Hygie)

**Contexte** : nettoyage de finition - les 2 residus anciens restants (analyste-in-console.tmp-test004x.sh + rapport-detecter-decalages-catalogue-2026-08-13.md), causes racines deja corrigees par Morpheus. C etait la 1re fois que je supprimais des fichiers COMMITES dans git.

**Deroulement** : c0-c0b-c0c (relectures + contexte) -> c1 nettoyer -> c2 snapshot (2173 fichiers) + rotation -> c3 precedent -> c4 detection -> c5-c6 classement -> c7 provenance (les 2 etaient COMMITES + modifies avant la correction des causes racines) -> c9 git rm + commit -> c10 re-detection PROPRE -> c11 rapport NON VIDE -> c12 lecon -> c34 usages -> c13.

**Lecons apprises** :
1. PIEGE GIT : quand une cible de suppression a des MODIFICATIONS LOCALES, `git rm` sans option ECHOUE (rc=1) - mais si on enchaine un `git commit -- <fichiers>`, git commite les MODIFICATIONS du fichier au lieu de la suppression (commit errone 6c64ae5). CORRECTIF : verifier le rc de git rm AVANT de committer, et utiliser `git rm -f` quand le fichier a des modifs locales.
2. PIEGE DU COMMIT ERRONE : `git reset --soft HEAD~1` defait proprement un commit errone sans perdre les modifications (restaure dans l index). A utiliser sans hesitation en cas de commit faux.
3. GAP DE DETECTION detecter-residus : le nom mache 'analyste-in-console.tmp-test004x.sh' (residu de test-004) n est PAS detecte par l outil car il ne commence pas par tmp-/.tmp-/.zz-. Le pattern TEMP ne couvre pas les noms maches avec prefixe projet. A SIGNALER a Vulcain : elargir le pattern TEMP (ex. detecter aussi les fichiers contenant .tmp- ou .zz- en leur sein, pas seulement en prefixe).
4. CREER-FICHIER : le contenu en ARGUMENT POSITIONNEL fonctionne (rapport 2075 octets, non vide) - la lecon de la 1re mission (jamais en stdin) est confirmee.
5. Le processus complet tient encore en conditions reelles avec git : snapshot -> detection -> provenance -> git rm -f -> commit -> re-detection -> rapport.


## [LECON] 2026-08-16 -- NETTOYAGE DOSSIER DUPLIQUE docs-dev (Hygie)

**Contexte** : l utilisateur a constate que le dossier docs-dev-cerveau-projet
existait en DOUBLE : a la racine (residu, ne contenant que
rapport-diagnostic-convention-scripts-temporaires-2026-08-16.md) et dans
cerveau-projet/ (le vrai dossier avec les 3 specs).

**Actions** : snapshot (4642 fichiers) -> detection 1 RAPPORT_EGARE ->
supprimer-dossier --agent hygie --force -> detection PROPRE. Le vrai dossier
cerveau-projet/docs-dev-cerveau-projet/ est conserve intact.

**Lecon** :
1. Un residu peut etre DOUBLE (dossier + fichier) : quand detecter-residus
   signale un RAPPORT_EGARE dans un dossier a la racine, verifier si le dossier
   entier est un doublon d un dossier legitime du cerveau-projet.
2. Le verrou exige --agent sur supprimer-dossier : toujours le passer (hygie).

**APRES** : reactiver JANUS (verification finale).
## [LECON] 2026-08-18 -- RESIDU RECURRENT detecter-decalages-catalogue (3e nettoyage) (Hygie)

**Contexte** : nettoyage des residus bloquant la non-regression (test-024 point 2b) de la chaine lire-head : tmp-morpheus/ (dossier temporaire de consultation pre-mission) + rapport-detecter-decalages-catalogue-2026-08-18.md (rapport egare a la racine).

**Actions** : snapshot (5797 fichiers) + rotation 0 -> detecter-residus 2 residus (0 cerveau-projet, 2 workspace) -> provenance prouvee (TEMP + RAPPORT_EGARE, signales par Themis/Janus) -> suppression tracee 2/2 (supprimer-dossier + supprimer-fichier, verrou --agent hygie) -> re-detection PROPRE -> rapport nettoyage-2026-08-18-1731.md.

**Lecons** :
1. RESIDU RECURRENT : le rapport de detecter-decalages-catalogue est EGARE A LA RACINE a CHAQUE fois que l outil est lance depuis la racine (deja nettoye le 08-13 et le 08-14, encore aujourd hui) -- c est un comportement d outil a corriger par Vulcain (le rapport doit aller dans le dossier de l agent ou un dossier dedie), pas un simple residu ponctuel.
2. La chaine fonctionne : le test-024 sert de garde-fou de non-regression qui FAIT echouer la suite tant que les residus existent -- le nettoyage debloque la non-regression sans decision humaine.
3. Le verrou exige --agent hygie sur supprimer-dossier ET supprimer-fichier (lecon 2026-08-16 confirmee pour les 2 outils).

- **2026-08-19 (test-085 processus residuel)** : un processus orphelin (bash -x /tmp/vt-test2.sh, PID 14628) laisse par un test de diagnostic heredoc faisait KO test-085. Nettoyage : snapshot (6109 fichiers) -> detecter (1 residu, provenance prouvee) -> nettoyer-processus-residuels --agent hygie --kill 14628 --force -> re-detection PROPRE -> test-085 8/8 OK. Lecon : les tests de diagnostic qui lancent bash -x doivent terminer leurs processus avant de rendre la main.
## [LECON] 2026-08-23 -- REPARATION INTER-ROUND : 9 RESIDUS + CRLF SUPPRIMES (Hygie)

**Contexte** : inter-round de reparation (protocole v0.2.0) demande par Cerberus via Buffy : nettoyer les erreurs hors mission signalees au bilan consolide de la chaine clio-readme-v2.

**Actions** : snapshot (8417 fichiers) -> detecter-residus --tous 9 residus (6 SAUVEGARDE cerveau-projet + 3 TEMP workspace) -> provenance prouvee (PRE-EXISTANTS classes par Janus, aucun cree par la mission) -> suppression 9/9 (6 supprimer-fichier + 3 supprimer-dossier --agent hygie) -> re-detection PROPRE (0 fichier + 0 processus) -> CRLF clio/corrections.md corrige via corriger-fins-de-ligne (383 lignes) -> rapport nettoyage-2026-08-23-2140.md -> ASCII 0/0.

**Lecons** :
1. INTER-ROUND = FIN DIFFERENTE DE SA CARTE : quand je suis activee en inter-round (reparation), je NE suis PAS ma fin normale c13 (Activer Janus) : le protocole v0.2.0 (R2/R3) ordonne de REACTIVER L APPELANT (Buffy), qui reprend son round (activer Vulcain pour les divergences). Janus reste HORS des inter-rounds (R4).
2. detecter-residus --tous affiche parfois une liste TRONQUEE (N premiers + ... (1 autres)) : pour la liste COMPLETE des .bak, compter via le snapshot (chemin finissant par .bak) ou un scan dedie.
3. analyse-externe.md.bak (backup conserve le 21/08) devenu superflu : la source originale existe -> residu prouve, supprimable.
4. Les fichiers freelance .bak-20260823-* (jarvis, routines-server) ne sont PAS des residus detectes : ne pas les toucher en mission cerveau-projet.
## [LECON] 2026-09-02 -- SUPPRESSION ARTEFACT DE TEST COMMITE _test_attente.jsonl (Hygie)

**Contexte** : controle de coherence des files de missions (demande Cerberus) - un fichier _test_attente.jsonl (hors FILES_VALIDES) trainait dans oracle/files/ avec une entree EN_ATTENTE sans id ni mission. Ajoute au commit c3ec8a4, jamais consomme par le relais, aucun code/test ne le reference.

**Actions** : snapshot (10635 fichiers) -> detection (375 SAUVEGARDE .bak pre-existants, bruit connu, hors cible) -> cible prouvee (committe, hors FILES_VALIDES, non referencee) -> supprimer-fichier --agent hygie (verrou d habilitation : l activation reelle de hygie a ete necessaire, la session etait sur oracle apres le relais) -> SUPPRIME -> re-verification (fichier absent, aucune reference dans le code ni les tests) -> rapport nettoyage-artefact-test-attente-2026-09-02.md.

**Lecons** :
1. Un artefact de test peut rester committe dans git sans jamais etre utilise : le controle de coherence des files doit aussi regarder les fichiers hors FILES_VALIDES (ils echappent au relais et s accumulent silencieusement).
2. Le verrou supprimer-fichier exige que la session soit RELLEMENT sur l agent : apres un relais Oracle, il faut activer hygie (activer-agent-principal) avant de pouvoir supprimer - sinon 'usurpation d identite'.
