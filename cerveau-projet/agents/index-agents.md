# Index — Agents
## Principe
## Navigation

### Agents indispensables

| Agent | Fiche | Corrections | Rôle | Statut |
|---|---|---|---|---|
| [Cerberus](cerberus/cerberus.md) | cerberus/cerberus.md | cerberus/corrections.md | Gardien de l'entrée | Disponible (principal) |
| [Buffy](buffy/buffy.md) | buffy/buffy.md | buffy/corrections.md | Développeur principal | Disponible (en attente) |

### Agents secondaires

| Agent | Fiche | Corrections | Rôle | Statut | Note |
|---|---|---|---|---|---|
| [Atlas](atlas/atlas.md) | atlas/atlas.md | atlas/corrections.md | Explorateur | Disponible (en attente) | Créé pendant le dev |
| [Athena](athena/athena.md) | athena/athena.md | athena/corrections.md | Rédactrice de pense-bêtes | Disponible (en attente) | Agent dédié aux pense-bêtes |
| [Promethee](promethee/promethee.md) | promethee/promethee.md | promethee/corrections.md | Rédacteur de specs | Disponible (en attente) | Agent dédié aux specs |
| [Minerve](minerve/minerve.md) | minerve/minerve.md | minerve/corrections.md | Rédactrice de todos | Disponible (en attente) | Agent dédié aux todos |
| [Clio](clio/clio.md) | clio/clio.md | clio/corrections.md | Muse de l'histoire — README | Disponible (en attente) | Agent dédié au README |
| [Janus](janus/janus.md) | janus/janus.md | janus/corrections.md | Contrôleur des statuts | Disponible (sur demande) | Assigné comme contrôleur |
| [Morpheus](morpheus/morpheus.md) | morpheus/morpheus.md | morpheus/corrections.md | Testeur | Disponible (en attente) | Agent dédié aux tests |
| [Vulcain](vulcain/vulcain.md) | vulcain/vulcain.md | vulcain/corrections.md | Constructeur d'outils | Disponible (en attente) | Créé pour construire les outils réels |

### Templates

| Template | Description |
|---|---|
| [fiche-agent-template.md](fiche-agent-template.md) | Modèle pour créer une fiche d'agent |
| [corrections-template.md](corrections-template.md) | Modèle pour les corrections/surcharges |

### Liens

- **Protocole** : [protocole-auto-correction/](../pense-betes/regles-immuables/general/protocole-auto-correction/)
- **Protocole** : [protocole-installer-regles/](../pense-betes/regles-immuables/general/protocole-installer-regles/) -- **IMMUABLE** : installer les regles immuables
- **Protocole** : [protocole-identification/](../pense-betes/regles-immuables/general/protocole-identification/) -- **IMMUABLE** : identification des agents
- **Protocole** : [protocole-recherches-web/](../pense-betes/regles-immuables/general/protocole-recherches-web/) -- **IMMUABLE** : recherches web
- **Regles** : [regles-emojis-ascii.md](../pense-betes/regles-immuables/general/regles-emojis-ascii.md) -- **IMMUABLE** : bannissement des emojis, utilisation de ASCII
- **Regles** : [regles-veracite.md](../pense-betes/regles-immuables/general/regles-veracite.md) -- **IMMUABLE** : ne jamais mentir ou inventer
- **AGENTS.md** : [../../AGENTS.md](../../AGENTS.md) (à la racine du projet futur)

---

## Comment créer sa fiche d'agent

1. Vérifier si `agents/[nom-agent]/` existe déjà
2. Si non, créer le dossier avec :
   ```
   agents/[nom-agent]/
   ├── [nom-agent].md        ← fiche de l'agent
   └── corrections.md         ← surcharges/corrections
   ```
3. Remplir la fiche avec le template `fiche-agent-template.md`
4. Remplir les corrections avec le template `corrections-template.md`
5. Mettre à jour AGENTS.md pour devenir l'agent principal

## Comment mettre à jour ses corrections

1. Lire sa fiche d'agent
2. Identifier une erreur ou un pattern à corriger
3. Ajouter la correction dans `corrections.md`
4. La correction sera appliquée automatiquement lors des prochaines sessions

---

## Règles d'or

| Règle | Description |
|---|---|
| **Un agent = un dossier** | Chaque agent a son propre dossier dans `agents/` |
| **Pas de partage** | Les corrections d'un agent ne s'appliquent qu'à lui |
| **Auto-correction** | L'agent corrige ses propres erreurs dans `corrections.md` |
| **AGENTS.md dynamique** | L'agent principal met à jour AGENTS.md à chaque session |
| **Fiche obligatoire** | Pas de travail sans fiche d'agent préalable |
| **Cycle complet** | Cerberus → Agent → Cerberus (toujours revenir à Cerberus) |
| **Ordre logique** | Fichiers principaux d'abord, agents secondaires ensuite |
