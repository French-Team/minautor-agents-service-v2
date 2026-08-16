---
identite:
  type: index
  appartient_a: commun
  commun: true
---
# Index -- Regles Generales
## Contenu

### Regles

| Fichier | Description |
|---|---|
| [regles-general-global.md](regles-general-global.md) | Regles globales du projet |
| [rvav-workflow.md](rvav-workflow.md) | Workflow RVAVP (Rechercher-Verifier-Analyser-Valider-Purifier) |
| [regles-choisir-agent.md](regles-choisir-agent.md) | **IMMUABLE** -- Choisir le bon agent |
| [regles-groupes-agents.md](regles-groupes-agents.md) | **IMMUABLE** -- Groupes d'agents et domaines (coordination / cerveau-projet / trio projets futurs) |
| [regles-validation-rigoureuse.md](regles-validation-rigoureuse.md) | **IMMUABLE** -- Validation rigoureuse |
| [regles-emojis-ascii.md](regles-emojis-ascii.md) | **IMMUABLE** -- Bannissement des emojis, utilisation de ASCII (exceptions volontaires documentees dans le fichier) |
| [regles-perimetre-workspace.md](regles-perimetre-workspace.md) | **IMMUABLE** -- Perimetre du workspace : ecriture dans le workspace uniquement, hors workspace en lecture seule |
| [regles-veracite.md](regles-veracite.md) | **IMMUABLE** -- Ne jamais mentir ou inventer |

### Protocoles

| Protocole | Description | Statut |
|---|---|---|
| [protocole-composition/](protocole-composition/) | Composition du squelette de base | ebauche |
| [protocole-demarrer-projet/](protocole-demarrer-projet/) | **IMMUABLE** -- Demarrer un nouveau projet | ebauche |
| [protocole-reprendre-projet/](protocole-reprendre-projet/) | **IMMUABLE** -- Reprendre un projet existant | ebauche |
| [protocole-installer-regles/](protocole-installer-regles/) | **IMMUABLE** -- Installer les regles immuables | ebauche |
| [protocole-identification/](protocole-identification/) | **IMMUABLE** -- Identification des agents | ebauche |
| [protocole-activation/](protocole-activation/) | **IMMUABLE** -- Activation des agents (avec lecture obligatoire + activer-agent-principal) | prepare |
| [protocole-recherches-web/](protocole-recherches-web/) | **IMMUABLE** -- Recherches web | ebauche |
| [protocole-outils/](protocole-outils/) | **IMMUABLE** -- Boite a outils | ebauche |
| [protocole-technologies/](protocole-technologies/) | Choix des technologies pour creer les outils | ebauche |
| [protocole-versionning-outils/](protocole-versionning-outils/) | Versionning des outils (beta -> tests -> production) | ebauche |
| [protocole-tests/](protocole-tests/) | Tests des outils avec protections + REGLE IMMUABLE (protections + options on/off + chrono) | ebauche |
| [protocole-boucles-dynamiques/](protocole-boucles-dynamiques/) | Boucles dynamiques (sous-missions) | ebauche |
| [protocole-auto-correction/](protocole-auto-correction/) | Auto-correction des agents | ebauche |
| [protocole-autoameliorer-cerveau/](protocole-autoameliorer-cerveau/) | Auto-amelioration du cerveau | ebauche |
| [protocole-autoameliorer-agents/](protocole-autoameliorer-agents/) | Auto-amelioration des agents | ebauche |
| [protocole-autoameliorer-outils/](protocole-autoameliorer-outils/) | Auto-amelioration des outils | ebauche |
| [protocole-autoameliorer-conventions/](protocole-autoameliorer-conventions/) | Auto-amelioration des conventions | ebauche |
| [protocole-autoameliorer-protocoles/](protocole-autoameliorer-protocoles/) | Auto-amelioration des protocoles | ebauche |
| [protocole-autoameliorer-regles/](protocole-autoameliorer-regles/) | Auto-amelioration des regles | ebauche |
| [protocole-gestion-defaillances/](protocole-gestion-defaillances/) | Gestion automatique des defaillances | ebauche |
| [protocole-controle-statuts/](protocole-controle-statuts/) | Controle des statuts (Janus) | ebauche |
| [protocole-carte-decision/](protocole-carte-decision/) | Carte de decision pour les agents | ebauche |
| [protocole-creation-combos/](protocole-creation-combos/) | Creation et mise en place des combos (quand/ou/comment, Pattern 3) | ebauche |
| [protocole-creation-scripts-temporaires/](protocole-creation-scripts-temporaires/) | Encadrer l utilisation des scripts temporaires (creer/declarer/supprimer/promouvoir/detecter, anti-regression, commandes spawn_agents sans echappement JSON) | ebauche |
| [protocole-purification/](protocole-purification/) | Purification des fichiers apres validation | ebauche |
| [protocole-nettoyage/](protocole-nettoyage/) | Nettoyage du workspace (Hygie) : snapshot -> detection (detecter-residus par zone) -> verdict -> suppression exclusive -> rapport | ebauche |
| [protocole-securite-marbre/](protocole-securite-marbre/) | **IMMUABLE** -- Securite du code : zones protegees (marbre) verrouillees, modification uniquement via autorisation utilisateur (Gardien propose, utilisateur valide) | ebauche |
| [protocole-controle-buffy/](protocole-controle-buffy/) | Controle croise du travail de Buffy (Janus) | ebauche |
| [protocole-audit-buffy/](protocole-audit-buffy/) | Audit de conformite du travail de Buffy (Themis) | ebauche |
| [protocole-sante-fichiers-agents/](protocole-sante-fichiers-agents/) | Sante periodique des fichiers agents (Janus) | ebauche |
| [protocole-fin-mission/](protocole-fin-mission/) | Fin de mission : CHAQUE maillon documente SON controle (lecon + verdict) AVANT de transmettre (anti-derive bilans sans preuve) | ebauche |
| [protocole-argus-contradictions/](protocole-argus-contradictions/) | Detection et signalement des contradictions (Argus) : 4 elements obligatoires (type, gravite, fichier+ligne, 2 sources croisees), cas types, preuve negative --fichier quand soupcon, cycle signalement -> agent habilite | ebauche |
| [protocole-verification-coherence/](protocole-verification-coherence/) | Verification de coherence des fichiers a compteurs/tables/badges (Themis, lecons re-audit README) | ebauche |

## Navigation

- **Parent** : [index-regles-immuables.md](../index-regles-immuables.md)
- **Conventions** : [conventions/protocoles/](../../conventions/protocoles/index-protocoles.md)
- **Hierarchie** : [hierarchie/](../hierarchie/index-hierarchie.md)

## Creer un nouveau protocole

1. Consulter [convention-protocoles.md](../../conventions/protocoles/convention-protocoles.md)
2. Creer un dossier `protocole-[nom]/` dans ce repertoire
3. Suivre le template du protocole
4. Passer par RVAV
5. Mettre a jour cet index
