# Protocole Immuable — Installer les Règles Immuables
---

## Principe Fondamental
---

## Règles à installer

### Règles obligatoires (IMMUABLE)

| # | Règle | Fichier | Description |
|---|---|---|---|
| 1 | Choisir le bon agent | `regles-choisir-agent.md` | Matrice de décision pour chaque tâche |
| 2 | Validation rigoureuse | `regles-validation-rigoureuse.md` | Contrôle derrière contrôle |
| 3 | Bannissement des emojis | `regles-emojis-ascii.md` | Seuls les caractères ASCII sont autorisés |
| 4 | Véracité | `regles-veracite.md` | Ne jamais mentir ou inventer |

### Workflow fondamental

| # | Règle | Fichier | Description |
|---|---|---|---|
| 4 | Workflow RVAV | `rvav-workflow.md` | Rechercher-Vérifier-Analyser-Valider |

### Structure fondamentale

| # | Règle | Fichier | Description |
|---|---|---|---|
| 5 | Hiérarchie par niveau | `regles-hierarchie-par-niveau.md` | Structure L0-L6 du cerveau |

---

## Étape 1 — Vérifier l'existence des règles

```
1. Lister regles-immuables/general/
2. Vérifier que chaque fichier de règle existe
3. Si une règle manque → la créer à partir du cerveau source
```

### Checklist

- [ ] `regles-choisir-agent.md` existe
- [ ] `regles-validation-rigoureuse.md` existe
- [ ] `regles-emojis-ascii.md` existe
- [ ] `regles-veracite.md` existe
- [ ] `rvav-workflow.md` existe
- [ ] `regles-hierarchie-par-niveau.md` existe

---

## Étape 2 — Copier les règles depuis le cerveau source

```
1. Identifier le chemin du cerveau source
2. Copier chaque règle dans le bon emplacement
3. Vérifier que le contenu est identique
```

### Emplacements

| Règle | Emplacement cible |
|---|---|
| `regles-choisir-agent.md` | `regles-immuables/general/` |
| `regles-validation-rigoureuse.md` | `regles-immuables/general/` |
| `regles-emojis-ascii.md` | `regles-immuables/general/` |
| `regles-veracite.md` | `regles-immuables/general/` |
| `rvav-workflow.md` | `regles-immuables/general/` |
| `regles-hierarchie-par-niveau.md` | `regles-immuables/hierarchie/` |

---

## Étape 3 — Vérifier les dépendances

Chaque règle a des dépendances qui doivent aussi être présentes :

### Dépendances de `regles-choisir-agent.md`

- [ ] `agents/` dossier existe
- [ ] `agents/index-agents.md` existe
- [ ] `agents/fiche-agent-template.md` existe
- [ ] `agents/corrections-template.md` existe
- [ ] `AGENTS.md` existe à la racine

### Dépendances de `regles-validation-rigoureuse.md`

- [ ] `rvav-workflow.md` existe

### Dépendances de `regles-emojis-ascii.md`

- [ ] Aucune dépendance spécifique

### Dépendances de `regles-veracite.md`

- [ ] `recherches-web/` dossier existe
- [ ] `protocole-recherches-web/` existe

### Dépendances de `rvav-workflow.md`

- [ ] `conventions/renommage/convention-renommage.md` existe

### Dépendances de `regles-hierarchie-par-niveau.md`

- [ ] `conventions/structures/convention-structures.md` existe

---

## Étape 4 — Mettre à jour les index

```
1. Mettre à jour regles-immuables/index-regles-immuables.md
2. Mettre à jour regles-immuables/general/index-regles-general.md
3. Mettre à jour regles-immuables/hierarchie/index-hierarchie.md
4. Vérifier que tous les liens sont valides
```

---

## Étape 5 — Valider par RVAV

```
1. Lister toutes les règles installées
2. Vérifier que chaque règle est complète
3. Vérifier que les dépendances sont satisfaites
4. Vérifier que les index sont à jour
5. Passer par RVAV complet
```

### Checklist finale

- [ ] 6 règles immuables installées
- [ ] Toutes les dépendances satisfaites
- [ ] Tous les index à jour
- [ ] Tous les liens valides
- [ ] RVAV effectué

---

## Protocoles associés

| Protocole | Description |
|---|---|
| `protocole-demarrer-projet` | Créer un nouveau projet complet |
| `protocole-reprendre-projet` | Reprendre un projet existant |
| `protocole-identification` | Identification des agents |
| `protocole-recherches-web` | Recherches web |
| `protocole-auto-correction` | Auto-correction des agents |

---

## Résumé

| Étape | Action | Résultat |
|---|---|---|
| 1 | Vérifier l'existence | Règles identifiées |
| 2 | Copier les règles | Règles installées |
| 3 | Vérifier les dépendances | Dépendances satisfaites |
| 4 | Mettre à jour les index | Index à jour |
| 5 | Valider par RVAV | Règles validées |

---

