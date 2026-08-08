---
identite:
  type: index
  appartient_a: commun
  commun: true
---
# Index -- Agents
## Principe
## Navigation

### Agents indispensables

| Agent | Fiche | Corrections | Role | Statut |
|---|---|---|---|---|
| [Cerberus](cerberus/cerberus.md) | cerberus/cerberus.md | cerberus/corrections.md | Gardien de l'entree | Disponible (principal) |
| [Buffy](buffy/buffy.md) | buffy/buffy.md | buffy/corrections.md | Developpeur principal | Disponible (en attente) |

### Agents secondaires

| Agent | Fiche | Corrections | Role | Statut | Note |
|---|---|---|---|---|---|
| [Atlas](atlas/atlas.md) | atlas/atlas.md | atlas/corrections.md | Explorateur | Disponible (en attente) | Cree pendant le dev |
| [Athena](athena/athena.md) | athena/athena.md | athena/corrections.md | Redactrice de pense-betes | Disponible (en attente) | Agent dedie aux pense-betes |
| [Promethee](promethee/promethee.md) | promethee/promethee.md | promethee/corrections.md | Redacteur de specs | Disponible (en attente) | Agent dedie aux specs |
| [Minerve](minerve/minerve.md) | minerve/minerve.md | minerve/corrections.md | Redactrice de todos | Disponible (en attente) | Agent dedie aux todos |
| [Clio](clio/clio.md) | clio/clio.md | clio/corrections.md | Muse de l'histoire -- README | Disponible (en attente) | Agent dedie au README |
| [Janus](janus/janus.md) | janus/janus.md | janus/corrections.md | Controleur des statuts | Disponible (sur demande) | Assigne comme controleur |
| [Morpheus](morpheus/morpheus.md) | morpheus/morpheus.md | morpheus/corrections.md | Testeur | Disponible (en attente) | Agent dedie aux tests |
| [Vulcain](vulcain/vulcain.md) | vulcain/vulcain.md | vulcain/corrections.md | Constructeur d'outils | Disponible (en attente) | Cree pour construire les outils reels |
| [Themis](themis/themis.md) | themis/themis.md | themis/corrections.md | Evaluatrice croisee | Disponible | 4 evaluateurs + 1 combo |

### Templates

| Template | Description |
|---|---|
| [fiche-agent-template.md](fiche-agent-template.md) | Modele pour creer une fiche d'agent |
| [corrections-template.md](corrections-template.md) | Modele pour les corrections/surcharges |

### Liens

- **Protocole** : [protocole-auto-correction/](../pense-betes/regles-immuables/general/protocole-auto-correction/)
- **Protocole** : [protocole-installer-regles/](../pense-betes/regles-immuables/general/protocole-installer-regles/) -- **IMMUABLE** : installer les regles immuables
- **Protocole** : [protocole-identification/](../pense-betes/regles-immuables/general/protocole-identification/) -- **IMMUABLE** : identification des agents
- **Protocole** : [protocole-recherches-web/](../pense-betes/regles-immuables/general/protocole-recherches-web/) -- **IMMUABLE** : recherches web
- **Regles** : [regles-emojis-ascii.md](../pense-betes/regles-immuables/general/regles-emojis-ascii.md) -- **IMMUABLE** : bannissement des emojis, utilisation de ASCII
- **Regles** : [regles-veracite.md](../pense-betes/regles-immuables/general/regles-veracite.md) -- **IMMUABLE** : ne jamais mentir ou inventer
- **AGENTS.md** : [../../AGENTS.md](../../AGENTS.md) (a la racine du projet futur)

---

## Comment creer sa fiche d'agent

1. Verifier si `agents/[nom-agent]/` existe deja
2. Si non, creer le dossier avec :
   ```
   agents/[nom-agent]/
   |-- [nom-agent].md        <- fiche de l'agent
   ``-- corrections.md         <- surcharges/corrections
   ```
3. Remplir la fiche avec le template `fiche-agent-template.md`
4. Remplir les corrections avec le template `corrections-template.md`
5. Mettre a jour AGENTS.md pour devenir l'agent principal

## Comment mettre a jour ses corrections

1. Lire sa fiche d'agent
2. Identifier une erreur ou un pattern a corriger
3. Ajouter la correction dans `corrections.md`
4. La correction sera appliquee automatiquement lors des prochaines sessions

---

## Regles d'or

| Regle | Description |
|---|---|
| **Un agent = un dossier** | Chaque agent a son propre dossier dans `agents/` |
| **Pas de partage** | Les corrections d'un agent ne s'appliquent qu'a lui |
| **Auto-correction** | L'agent corrige ses propres erreurs dans `corrections.md` |
| **AGENTS.md dynamique** | L'agent principal met a jour AGENTS.md a chaque session |
| **Fiche obligatoire** | Pas de travail sans fiche d'agent prealable |
| **Cycle complet** | Cerberus -> Agent -> Cerberus (toujours revenir a Cerberus) |
| **Ordre logique** | Fichiers principaux d'abord, agents secondaires ensuite |
