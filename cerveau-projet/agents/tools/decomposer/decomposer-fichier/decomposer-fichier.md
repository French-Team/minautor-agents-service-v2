---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# decomposer-fichier

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** decomposer
**Chemin :** `agents/tools/decomposer/decomposer-fichier/`
**Proprietaire :** Atlas (outil partage)

---

## Objectif

Decomposer les fichiers markdown pour permettre aux agents de voir uniquement ce dont ils ont besoin.

---

## Utilisation

### CLI Python (version 0.2.0-py)

```
python3 decomposer-fichier.py <fichier> [options]

Actions :
  --lister              Lister les sections
  --extraire [section]  Extraire une section
  --filtrer [type]      Filtrer par type (titres|regles|tableaux|code|liens)
  --resume              Afficher le resume
  --compter             Compter le contenu

Options :
  --json                Sortie JSON
  --verbose             Details supplementaires
  --version             Afficher la version
```

### CLI bash (version originale)

```bash
decomposer-fichier.sh <fichier> [options]
```

---

## Actions

| Action | Description | Exemple |
|---|---|---|
| `--lister` | Lister les sections | `decomposer-fichier.sh fichier.md --lister` |
| `--extraire [section]` | Extraire une section | `decomposer-fichier.sh fichier.md --extraire "Regles"` |
| `--filtrer [type]` | Filtrer par type | `decomposer-fichier.sh fichier.md --filtrer regles` |
| `--resume` | Afficher le resume | `decomposer-fichier.sh fichier.md --resume` |
| `--compter` | Compter le contenu | `decomposer-fichier.sh fichier.md --compter` |

---

## Types de contenu

| Type | Description |
|---|---|
| `titres` | Titres (##, ###) |
| `regles` | Lignes avec REGLE, JAMAIS, TOUJOURS |
| `tableaux` | Tableaux Markdown |
| `code` | Blocs de code |
| `liens` | Liens Markdown |

---

## Exemples

### Lister les sections

```bash
$ decomposer-fichier.sh cerveau-projet/agents/regles-immuables/general/protocole-outils/protocole-outils.001.01.ebauche.md --lister

=== Sections de protocole-outils.001.01.ebauche.md ===

4. ## Principe Fondamental
7. ## Pourquoi ?
18. ## Structure
56. ## Regles
   58. ### Regle 1
   71. ### Regle 2
...
```

### Extraire une section

```bash
$ decomposer-fichier.sh cerveau-projet/agents/regles-immuables/general/protocole-outils/protocole-outils.001.01.ebauche.md --extraire "Regles"

=== Section: Regles ===

## Regles

### Regle 1 -- Chaque outil est documente
...
```

### Filtrer par type

```bash
$ decomposer-fichier.sh cerveau-projet/agents/regles-immuables/general/protocole-outils/protocole-outils.001.01.ebauche.md --filtrer regles

4: > **Ne jamais utiliser une commande sans la transformer en outil reutilisable.**
58: ### Regle 1 -- Chaque outil est documente
71: ### Regle 2 -- Chaque outil est teste
...
```

### Resume

```bash
$ decomposer-fichier.sh cerveau-projet/agents/regles-immuables/general/protocole-outils/protocole-outils.001.01.ebauche.md --resume

=== Resume de protocole-outils.001.01.ebauche.md ===

Lignes       : 110
Sections     : 8
Sous-sections: 12
Tableaux     : 4
Blocs de code: 6
```

---

## Extensibilite

L'outil est prepare pour de futurs ajouts :

| Fonctionnalite | Description |
|---|---|
| `--comparer` | Comparer deux fichiers |
| `--detecter-doublons` | Trouver les sections similaires |
| `--suggerer-condenser` | Proposer des reductions |
| `--filtrer definitions` | Lignes avec "est", "signifie" |
| `--filtrer exemples` | Blocs avec "Exemple" |
| `--filtrer erreurs` | Lignes avec "ERREUR" |

---

## Dependances

- Aucune dependance externe
- Utilise uniquement bash, grep, sed, wc

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-py | 2026-08-07 | Version Python creee (meme dossier, meme nom, base sur outil-template.py) |
| 0.1.0-beta | 2026-08-05 | Creation initiale |

---
