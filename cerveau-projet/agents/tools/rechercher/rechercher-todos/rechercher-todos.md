# rechercher-todos

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** rechercher
**Chemin :** `agents/tools/rechercher/rechercher-todos/`
**Proprietaire :** Minerve (outil partage)

## Description

Rechercher les todos existants pour eviter les doublons. L'outil liste les fichiers du type `todo-[theme].[id].[class].[statut].md` et detecte les themes identiques ou **proches** (noms legerement differents) avant toute creation.

> **PHILOSOPHIE** : Minerve lance cet outil en **etape 1** de sa mission pour verifier qu'un todo au theme proche n'existe pas deja.

## Utilisation

Version Python (recommandee) :

```bash
# Inventaire complet des todos existants
python3 rechercher-todos.py --tous

# Recherche anti-doublon pour un theme (avant creation)
python3 rechercher-todos.py --theme pipeline

# Avec details de similarite
python3 rechercher-todos.py --theme pipeline --verbose

# Rechercher dans un dossier specifique
python3 rechercher-todos.py --theme pipeline --dossier cerveau-projet/
```

Version bash equivalente : `rechercher-todos.sh` (meme logique).

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
| **[EXACT]** | Le theme est identique au motif | **NE PAS creer** -- doublon |
| **[PROCHE]** | Le theme contient le motif ou l'inverse | **NE PAS creer** -- nom legerement different |
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
| `generateurs-squelette-todo` | A lancer SEULEMENT si aucun doublon n'est detecte |
| `lister-agents` | Voir l'agent Minerve qui utilise cet outil |
| `valider-nommage` | Verifier la convention de nommage avant creation |

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (rechercher-todos.py), basee sur outil-template.py. Inventaire + anti-doublon (EXACT/PROCHE/PARTIEL), exit 1 si doublon |

---
