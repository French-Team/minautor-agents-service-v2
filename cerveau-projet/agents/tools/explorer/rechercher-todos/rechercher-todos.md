# rechercher-todos

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** Explorer
**Chemin :** `agents/tools/explorer/rechercher-todos/`

## Description

Rechercher les todos existants pour eviter les doublons. L'outil liste les fichiers du type `todo-[theme].[id].[class].[statut].md` et detecte les themes identiques ou **proches** (noms legerement differents) avant toute creation.

> **PHILOSOPHIE** : Minerve lance cet outil en **etape 1** de sa mission pour verifier qu'un todo au theme proche n'existe pas deja.

## Utilisation

```bash
# Inventaire complet des todos existants
rechercher-todos.sh --tous

# Recherche anti-doublon pour un theme (avant creation)
rechercher-todos.sh --theme pipeline

# Avec details de similarite
rechercher-todos.sh --theme pipeline --verbose

# Rechercher dans un dossier specifique
rechercher-todos.sh --theme pipeline --dossier cerveau-projet/examples/
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--theme <motif>` | Rechercher les themes identiques ou proches du motif | (vide = inventaire) |
| `--tous` | Lister tous les todos existants | false |
| `--dossier <chemin>` | Dossier de recherche | racine du projet |
| `--verbose` | Afficher les details de correspondance | false |
| `--help` | Afficher l'aide | - |

## Niveaux de correspondance

| Niveau | Critere | Action |
|---|---|---|
| **[EXACT]** | Le theme est identique au motif | **NE PAS creer** — doublon |
| **[PROCHE]** | Le theme contient le motif ou l'inverse | **NE PAS creer** — nom legerement different |
| **[PARTIEL]** | Au moins un mot-cle commun (>= 4 lettres) | Verifier avant de creer |
| **[OK]** | Aucune correspondance | Vous pouvez creer le fichier |

## Ce que l'outil fait

1. **Scan** - Trouve tous les fichiers `todo-*.md` (hors templates et index)
2. **Extrait** - Le theme (partie apres `todo-`) et le statut de chaque fichier
3. **Compare** - Le motif avec chaque theme (exact, partiel, mots-cles)
4. **Rapporte** - Les correspondances avec niveau de risque + verdict

## Exemples de sortie

```bash
$ rechercher-todos.sh --theme pipeline

=== Recherche anti-doublon : theme 'pipeline' ===

  [EXACT] pipeline -> todo-pipeline.001.01.ebauche.md

[ATTENTION] 1 correspondance(s) trouvee(s). Verifiez avant de creer.
-> Ne pas creer si un [EXACT] ou [PROCHE] existe deja.
```

```bash
$ rechercher-todos.sh --tous

=== Inventaire des todos ===
Dossier : .

  THEME                                  FICHIER                        STATUT
  -----------------------------------------------------------------------
  pipeline                               todo-pipeline.001.01.ebauche.md  ebauche

Total : 1 todos
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Avant de creer un todo** | Etape 1 OBLIGATOIRE : verifier qu'aucun theme proche n'existe |
| **Audit des todos** | Inventaire complet des fichiers existants |
| **Detection de doublons** | Trouver les todos avec des noms legerement differents |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `squelette-todo` | A lancer SEULEMENT si aucun doublon n'est detecte |
| `lister-agents` | Voir l'agent Minerve qui utilise cet outil |
| `valider-nommage` | Verifier la convention de nommage avant creation |
