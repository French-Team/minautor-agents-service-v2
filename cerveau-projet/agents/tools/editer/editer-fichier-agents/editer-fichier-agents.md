# editer-fichier-agents

> Outil d'edition structuree des fiches des agents (.md) : manipule des LIGNES ou des
> BLOCS delimites par titre markdown, avec supprimer/remplacer/ajouter et correcteur
> ASCII integre pour eviter les erreurs d'accent.
> **Version : 0.1.0-beta** | **Statut : beta**

## Description

Edite les fichiers des agents (`cerveau-projet/agents/*/*.md`) de facon fiable :

- **BLOC** : une zone delimitee par un titre markdown (`## X`) jusqu'au prochain titre
  de meme niveau (ex: `## Historique` -> le titre suivant `## ...` ou fin de fichier).
- **LIGNE** : un numero de ligne unique (1-base).
- **Actions** : `--supprimer`, `--remplacer <texte>`, `--ajouter <texte>` (avant/apres).
- **ASCII** : `--ascii` corrige automatiquement les caracteres non-ASCII (accents,
  guillemets francais, tirets cadratins, points de suspension) en reutilisant le
  dictionnaire de `corriger-dictionnaire-accents`.

## Utilisation

```bash
# Supprimer le bloc entier "Historique" (du titre jusqu'au prochain ##)
python3 editer-fichier-agents.py cerveau-projet/agents/buffy/buffy.md --bloc "Historique" --supprimer

# Supprimer en simulant (dry-run) + sauvegarde
python3 editer-fichier-agents.py fiche.md --bloc "Historique" --supprimer --dry-run --backup

# Remplacer une ligne precise
python3 editer-fichier-agents.py fiche.md --ligne 5 --remplacer "> Nouvelle ligne"

# Ajouter une ligne apres la ligne 1
python3 editer-fichier-agents.py fiche.md --ligne 1 --ajouter "> Note" --apres

# Remplacer un bloc + corriger les accents automatiquement
python3 editer-fichier-agents.py fiche.md --bloc "Identite" --remplacer "## Identite\n..." --ascii

# Ajouter un bloc entier avant un titre existant
python3 editer-fichier-agents.py fiche.md --bloc "Corrections" --ajouter "## Nouvelle section\ncontenu"
```

## Options

| Option | Description |
|---|---|
| `--ligne N` | Numero de ligne cible (1-base) |
| `--bloc "Titre"` | Titre du bloc cible (delimite par le prochain titre de meme niveau) |
| `--supprimer` | Supprimer la ligne ou le bloc cible |
| `--remplacer <texte>` | Remplacer la cible par le texte (multiligne avec `\n`) |
| `--ajouter <texte>` | Ajouter du texte avant la cible (ou apres avec `--apres`) |
| `--ascii` | Corriger les caracteres non-ASCII apres l'edition (dictionnaire accents) |
| `--backup` | Creer une sauvegarde `.bak` avant modification |
| `--dry-run` | Simuler sans rien modifier |
| `--verbose` | Afficher les details |
| `--version` | Afficher la version |

## Ce que l'outil fait

1. Verifie le nommage (`editer-` = prefixe de la categorie `editer/`).
2. Lit le fichier en preservant le saut de ligne (LF/CRLF).
3. Localise la cible : bloc par titre markdown (avec detection du niveau) ou ligne par numero.
4. Applique l'action demandee (supprimer/remplacer/ajouter).
5. Optionnellement corrige l'ASCII (dictionnaire de corriger-dictionnaire-accents).
6. Sauvegarde `.bak` si demande, ecrit le fichier (sauf `--dry-run`).

## Quand l'utiliser

- Supprimer un bloc devenu inutile dans une fiche agent (ex: `## Historique` dont
  l'information vit desormais dans `AGENTS-historique.md` et les corrections).
- Modifier une ligne ou un bloc precis sans risquer d'ecraser le reste du fichier.
- Ajouter une section ou une ligne a une position structurelle connue.
- Garantir le respect de la regle ASCII stricte lors des editions de fiches.

## Cas d'usage : bloc "Historique" obsolete

Les 11 fiches agents contiennent un bloc `## Historique` devenu inutile (l'information
vit dans `AGENTS-historique.md` + les fichiers de corrections). Pour le retirer :

```bash
python3 editer-fichier-agents.py cerveau-projet/agents/buffy/buffy.md --bloc "Historique" --supprimer --backup
```

L'outil supprime le titre ET tout son contenu jusqu'au prochain `## ` (6 a 14 lignes
selon les fiches), en une seule operation structurelle.

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-11 | Creation : ligne/bloc + supprimer/remplacer/ajouter + correcteur ASCII |

## Notes de creation

- **100% stdlib** : aucun import externe.
- **ASCII strict** : code et commentaires ASCII purs.
- **Reutilise** le dictionnaire de `corriger-dictionnaire-accents` (meme mecanique
  que `corriger-symboles`) pour le correcteur `--ascii`.
- **Ne duplique pas** `editer-fichier` (remplacement de motif texte) ni
  `supprimer-ligne` (numero de ligne seul) : la valeur ajoutee est le **bloc
  structure par titre** + l'**ASCII integre**.
