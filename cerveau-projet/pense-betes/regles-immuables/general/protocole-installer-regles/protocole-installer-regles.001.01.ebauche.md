# Protocole Immuable -- Installer les Regles Immuables
---

## Principe Fondamental
---

## Regles a installer

### Regles obligatoires (IMMUABLE)

| # | Regle | Fichier | Description |
|---|---|---|---|
| 1 | Choisir le bon agent | `regles-choisir-agent.md` | Matrice de decision pour chaque tache |
| 2 | Validation rigoureuse | `regles-validation-rigoureuse.md` | Controle derriere controle |
| 3 | Bannissement des emojis | `regles-emojis-ascii.md` | Seuls les caracteres ASCII sont autorises |
| 4 | Veracite | `regles-veracite.md` | Ne jamais mentir ou inventer |

### Workflow fondamental

| # | Regle | Fichier | Description |
|---|---|---|---|
| 4 | Workflow RVAV | `rvav-workflow.md` | Rechercher-Verifier-Analyser-Valider |

### Structure fondamentale

| # | Regle | Fichier | Description |
|---|---|---|---|
| 5 | Hierarchie par niveau | `regles-hierarchie-par-niveau.md` | Structure L0-L6 du cerveau |

---

## Etape 1 -- Verifier l'existence des regles

```
1. Lister regles-immuables/general/
2. Verifier que chaque fichier de regle existe
3. Si une regle manque -> la creer a partir du cerveau source
```

### Checklist

- [ ] `regles-choisir-agent.md` existe
- [ ] `regles-validation-rigoureuse.md` existe
- [ ] `regles-emojis-ascii.md` existe
- [ ] `regles-veracite.md` existe
- [ ] `rvav-workflow.md` existe
- [ ] `regles-hierarchie-par-niveau.md` existe

---

## Etape 2 -- Copier les regles depuis le cerveau source

```
1. Identifier le chemin du cerveau source
2. Copier chaque regle dans le bon emplacement
3. Verifier que le contenu est identique
```

### Emplacements

| Regle | Emplacement cible |
|---|---|
| `regles-choisir-agent.md` | `regles-immuables/general/` |
| `regles-validation-rigoureuse.md` | `regles-immuables/general/` |
| `regles-emojis-ascii.md` | `regles-immuables/general/` |
| `regles-veracite.md` | `regles-immuables/general/` |
| `rvav-workflow.md` | `regles-immuables/general/` |
| `regles-hierarchie-par-niveau.md` | `regles-immuables/hierarchie/` |

---

## Etape 3 -- Verifier les dependances

Chaque regle a des dependances qui doivent aussi etre presentes :

### Dependances de `regles-choisir-agent.md`

- [ ] `agents/` dossier existe
- [ ] `agents/index-agents.md` existe
- [ ] `agents/fiche-agent-template.md` existe
- [ ] `agents/corrections-template.md` existe
- [ ] `AGENTS.md` existe a la racine

### Dependances de `regles-validation-rigoureuse.md`

- [ ] `rvav-workflow.md` existe

### Dependances de `regles-emojis-ascii.md`

- [ ] Aucune dependance specifique

### Dependances de `regles-veracite.md`

- [ ] `recherches-web/` dossier existe
- [ ] `protocole-recherches-web/` existe

### Dependances de `rvav-workflow.md`

- [ ] `conventions/renommage/convention-renommage.md` existe

### Dependances de `regles-hierarchie-par-niveau.md`

- [ ] `conventions/structures/convention-structures.md` existe

---

## Etape 4 -- Mettre a jour les index

```
1. Mettre a jour regles-immuables/index-regles-immuables.md
2. Mettre a jour regles-immuables/general/index-regles-general.md
3. Mettre a jour regles-immuables/hierarchie/index-hierarchie.md
4. Verifier que tous les liens sont valides
```

---

## Etape 5 -- Valider par RVAV

```
1. Lister toutes les regles installees
2. Verifier que chaque regle est complete
3. Verifier que les dependances sont satisfaites
4. Verifier que les index sont a jour
5. Passer par RVAV complet
```

### Checklist finale

- [ ] 6 regles immuables installees
- [ ] Toutes les dependances satisfaites
- [ ] Tous les index a jour
- [ ] Tous les liens valides
- [ ] RVAV effectue

---

## Protocoles associes

| Protocole | Description |
|---|---|
| `protocole-demarrer-projet` | Creer un nouveau projet complet |
| `protocole-reprendre-projet` | Reprendre un projet existant |
| `protocole-identification` | Identification des agents |
| `protocole-recherches-web` | Recherches web |
| `protocole-auto-correction` | Auto-correction des agents |

---

## Resume

| Etape | Action | Resultat |
|---|---|---|
| 1 | Verifier l'existence | Regles identifiees |
| 2 | Copier les regles | Regles installees |
| 3 | Verifier les dependances | Dependances satisfaites |
| 4 | Mettre a jour les index | Index a jour |
| 5 | Valider par RVAV | Regles validees |

---

