# Missions de Revision -- 2026-08-22

## Resume

| Niveau | Nombre |
|---|---|
| URGENT | 1 |
| IMPORTANT | 2 |
| MOYEN | 3 |
| BAS | 1 |

## Contexte

Decision utilisateur : evolution du processus de coordination des rounds.
Le garde-fou historique "si l agent n a pas fini sa mission, il doit reactiver
Cerberus" est OBSOLETE : il contredit le deroulement normal actuel.

### Le nouveau processus voulu (decision utilisateur)

1. Cerberus lance le round en activant le premier agent habilite.
2. Chaque agent active l agent suivant selon SA carte : le round va BOUT EN BOUT,
   sans retomber sur Cerberus au milieu. UN ROUND LANCE DOIT ETRE FINI.
3. Si un agent detecte une ERREUR HORS-PERIMETRE pendant son round :
   - il n INTERROMPT PAS le round et ne reactive PAS Cerberus ;
   - il active l AGENT HABILITE pour la reparation, avec le rapport de l erreur.
4. La fin de cette INTER-ROUND (mission secondaire) reactive l AGENT QUI L AVAIT
   ACTIVE, qui REPREND son round principal exactement ou il l avait laisse.
5. Une erreur ne doit JAMAIS rester "seulement detectee" : elle doit etre
   CORRIGEE par l agent habilite exclusivement - lui seul sait precisement quoi
   faire, c est sa mission exclusive.

## Missions

### [URGENT] M1 - Reviser les regles de fin de round et creer le concept d INTER-ROUND

**Agent habilite** : Buffy (regles immuables + cartes = SON domaine)
**Quoi** :
- Reviser Pattern 8 / Pattern 13 dans spec-guider-parcours et protocole-fin-mission :
  ajouter explicitement le flux INTER-ROUND (erreur hors-perimetre ->
  activation de l agent habilite avec rapport -> fin de l inter-round qui
  reactive l agent appelant -> reprise du round principal).
- Corriger toutes les formulations du type "si l agent n a pas fini, reactiver
  Cerberus" (AGENTS.md section Fin de mission, fiches, cases c15b...).
- Definir le vocabulaire : ROUND (mission principale bout-en-bout),
  INTER-ROUND (mission secondaire de reparation), REPRISE DE ROUND.
- Regle a graver : une erreur detectee est TOUJOURS suivie d une reparation
  par l agent habilite exclusivement (jamais "seulement detectee").
**Justification URGENT** : les regles actuelles se contredisent - un agent qui
suit litteralement le garde-fou obsolete casse le round au lieu de le reparer.

### [IMPORTANT] M2 - Aligner les messages de activer-agent-principal sur le nouveau flux

**Agent habilite** : Vulcain (outil = SON domaine, sur la spec revisee par Buffy en M1)
**Quoi** :
- Les AVERTISSEMENTS GARDE-FOU (relais de chaine / double activation / "Si
  l agent n a PAS termine sa mission, reactiver Cerberus d abord") doivent
  reflechir le flux INTER-ROUND : l avertissement doit dire "si l inter-round
  est termine, reactiver l agent appelant pour qu il reprenne son round".
- Verifier la coherence des messages informationnels post-reactivation.
**Justification IMPORTANT** : ce sont ces messages que les agents lisent a
l execution ; s ils contredisent la nouvelle regle, la regle reste morte.

### [IMPORTANT] M3 - Mettre a jour les cartes des agents (cases d erreur hors-perimetre)

**Agenthabilite** : Buffy (cartes = SON domaine, apres M1)
**Quoi** :
- Dans chaque carte comportant une case "probleme hors mission detecte"
  (ex c15b cerberus, cases Signaler...) : le chemin devient ACTIVER L AGENT
  HABILITE AVEC LE RAPPORT puis, a la fin de l inter-round, REACTIVER L AGENT
  APPELANT (reprise de round) - plus jamais "rendre la main a Cerberus".
- Chiron re-eduquera les agents apres la migration (M5).

### [MOYEN] M4 - Corriger les 3 KO pre-existants de la non-regression (proves git diff HEAD vide)

- M4a test-071 : case c6 de redacteur-v2 sans outil de correction ->
  **Buffy** (carte redacteur-v2).
- M4b test-078 : 2 non-ASCII dans les sources de generateurs-amelioration ->
  **Vulcain** (outil).
- M4c test-067 : bumper --tous, 2 KO a diagnostiquer -> **Vulcain puis Buffy**
  selon le diagnostic.

### [MOYEN] M5 - Re-education des agents au nouveau flux (apres M1-M3)

**Agent habilite** : Chiron (educateur exclusif)
**Quoi** : re-eduire les agents sur le concept ROUND / INTER-ROUND / REPRISE
une fois les regles, messages et cartes alignes.

### [BAS] M6 - Purger les residus temporaires

**Agent habilite** : Hygie (SEUL a supprimer)
**Quoi** : supprimer tmp-vulcain/zz-patch-valider-relecture.py et
tmp-vulcain/zz-patch2-valider-relecture.py (mission E4 terminee et validee).

## Questions ouvertes (pour affiner avant execution)

1. L inter-round peut-il enchainer PLUSIEURS reparations (un agent habilite qui
   decouvre lui-meme une erreur hors-perimetre pendant sa reparation) ?
   Hypothese proposee : oui, meme mecanique, profondeur non bornee mais tracee.
2. Qui verifie l inter-round ? Hypothese proposee : Themis/Janus restent hors
   des inter-rounds courts ; Janus garde la non-regression finale du round.
3. Le compteur de round (tracabilite) : faut-il marquer dans AGENTS-historique
   qu une activation est une INTER-ROUND et de quel round elle depend ?



## Decision utilisateur 2026-08-22 bis - ROUTAGE DE LA PORTE DU MARBRE

**Decision** : les propositions de modification de zones protegees (marbre)
consideres comme STANDARDS sont derivees vers SOCRATE qui mene la revision et
repond en son nom. La validation UTILISATEUR directe reste reservee aux cas
NON-STANDARDS ou exceptionnels.

**Critere STANDARD (-> Socrate decide et repond)** :
- alignement d une zone protegee sur une regle DEJA validee ailleurs
  (protocole, spec, decision utilisateur existante) ;
- correction de formulation obsolete sans changement de sens ;
- ajout d une precision non contradictoire.

**Critere EXCEPTIONNEL (-> validation utilisateur obligatoire)** :
- changement de perimetre de protection (zone ajoutee/retiree) ;
- suppression ou affaiblissement d une regle noyau ;
- impact sur PLUSIEURS zones ou contradiction avec le marbre existant ;
- toute nouveaute sans precedent valide.

**Redaction proposee a graver** (protocole-securite-marbre + fiche gardien) :
Le Gardien qualifie chaque proposition : STANDARD -> transmission a Socrate
(conversateur de revision strategique) qui repond au nom de l utilisateur et
autorise la porte ; EXCEPTIONNEL -> proposition soumise a l utilisateur.
La qualification de Socrate est journalisee dans marbre-log.jsonl avec la
reference de sa revision (missions-revision.md). L utilisateur garde un droit
de veto a posteriori sur toute porte STANDARD (annulation + re-empreinte).

### M7 - Executer la decision de routage du marbre

| Etape | Agent | Contenu |
|---|---|---|
| M7a | Buffy | Rediger la regle dans protocole-securite-marbre + fiche gardien (qualification STANDARD/EXCEPTIONNEL) |
| M7b | Gardien | Graver la regle par la porte EXCEPTIONNELLE (premiere application : elle modifie elle-meme le protocole marbre) |
| M7c | Chiron | Eduquer Socrate aux mises a jour du jour (INTER-ROUND, R/IR, routage marbre) |



## Decision utilisateur 2026-08-22 ter - GIT N'EST PAS UNE SOURCE DE VERITE RECENTE

**Contexte** : restauration de combos-moteur par git checkout - le commit datait
de plusieurs jours : le checkout aurait ECRASE tout le travail de session non
commite. Evite par chance, jamais plus.

**Regle gravee** : le git est une SAUVEGARDE du passe. Il n'est source de
verite QUE si les fichiers concernes sont tres tres recents (minutes).
Au-dela de quelques dizaines de minutes : git checkout INTERDIT.

**Correctifs decides (M8)** :
1. Creer un agent dedie au git (SEUL habilite aux commandes git) -
   creation = combo creer-agent, domaine Buffy.
2. Lui construire une CAISSE A OUTILS : recuperer nom, mail, nom du projet,
   remote, etat du stash... pour accelerer les appels entrant/sortant vers git -
   creation = domaine Vulcain.
3. En attente : le verrou d execution des combos (essai 1 abandonne proprement,
   a refaire avec lecture complete du main).
