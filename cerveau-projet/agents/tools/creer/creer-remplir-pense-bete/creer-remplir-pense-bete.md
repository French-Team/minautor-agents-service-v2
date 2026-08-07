# creer-remplir-pense-bete

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** Creer
**Chemin :** `agents/tools/creer/creer-remplir-pense-bete/`
**Proprietaire :** outil partage

## Description

Remplit les sections d'un pense-bete **sans ouvrir le fichier**. Athena donne la section et le contenu en arguments, l'outil insere le contenu a la bonne place. Elle peut ainsi travailler relax, sans manipuler le fichier directement.

## Utilisation

### CLI Python (version 0.2.0-py)

```
python3 creer-remplir-pense-bete.py <fichier> <section> <contenu> [--dry-run]

Options :
  --dry-run    Afficher ce qui serait fait sans modifier
  --version    Afficher la version
```

### CLI bash (version originale)

```bash
# Remplir le titre
creer-remplir-pense-bete.sh pense-bete-pipeline.001.01.ebauche.md titre "Concept de Pipeline"

# Remplir l'idee
creer-remplir-pense-bete.sh pense-bete-pipeline.001.01.ebauche.md idee "Le pipeline compose des fonctions de maniere decouplee"

# Remplir le probleme
creer-remplir-pense-bete.sh pense-bete-pipeline.001.01.ebauche.md probleme "Comment communiquer entre fonctions sans les coupler ?"

# Remplir le contexte
creer-remplir-pense-bete.sh pense-bete-pipeline.001.01.ebauche.md contexte "Ce pense-bete s'inscrit dans le developpement du cerveau"

# Remplir les liens (multiligne avec \n)
creer-remplir-pense-bete.sh pense-bete-pipeline.001.01.ebauche.md liens "- Conventions : convention-pipelines.md\n- Regles : rvav-workflow.md"

# Apercu sans modifier
creer-remplir-pense-bete.sh pense-bete-pipeline.001.01.ebauche.md idee "Mon idee" --dry-run
```

## Arguments

| Argument | Description |
|---|---|
| `fichier` | Chemin du pense-bete a remplir |
| `section` | Section a remplir : titre, idee, probleme, contexte, liens |
| `contenu` | Contenu a inserer (entre guillemets) |

## Options

| Option | Description |
|---|---|
| `--dry-run` | Afficher ce qui serait fait sans modifier |
| `--help` | Afficher l'aide |

## Sections disponibles

| Section | Cible | Marqueur |
|---|---|---|
| `titre` | Titre du pense-bete | `# Pense-bete` |
| `idee` | Section 1. Idee | `## 1. Idee` |
| `probleme` | Section 2. Probleme / Question | `## 2. Probleme / Question` |
| `contexte` | Section 3. Contexte | `## 3. Contexte` |
| `liens` | Section 4. Liens | `## 4. Liens` |

## Ce que l'outil fait

1. **Valide** - La section est connue, le fichier existe
2. **Localise** - Trouve le marqueur de la section dans le fichier
3. **Detecte** - La prochaine section (pour delimiter le remplacement)
4. **Remplace** - Insere le contenu entre la section et la suivante
5. **Protege** - Ne modifie que la section visee, le reste est intact

## Exemples de sortie

```bash
$ creer-remplir-pense-bete.sh pense-bete-pipeline.001.01.ebauche.md idee "Le pipeline compose des fonctions"
[OK] Section 'idee' remplie dans pense-bete-pipeline.001.01.ebauche.md
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Mission d'Athena** | Etape 2 apres la creation du squelette |
| **Remplir une section** | Sans ouvrir le fichier, en une commande |
| **Correction d'une section** | Re-remplir une section avec le nouveau contenu |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `generateurs-squelette-pense-bete` | Cree le squelette avant de remplir |
| `valider-pense-bete` | Verifie le fichier apres remplissage |
| `valider-conformite-ascii` | Verifie qu'aucun accent n'a ete introduit |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-py | 2026-08-07 | Version Python creee (meme dossier, meme nom, base sur outil-template.py, interpretation des sequences d'echappement \\n) |
