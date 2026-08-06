# rechercher-accents-sensibles

**Version :** 0.1.0-beta
**Statut :** ebauche
**Categorie :** Explorer
**Chemin :** `agents/tools/explorer/rechercher-accents-sensibles/`

## Description

Recherche les caracteres non-ASCII (accents, emojis, symboles Unicode) dans les **ZONES SENSIBLES** uniquement, la ou ils provoquent de vraies erreurs d'encodage ou de traitement. Il ne scanne PAS tout le fichier ni tous les types : il cible les zones qui cassent les outils, les liens, les scripts et le parsing.

**Mode : RECHERCHE ET RAPPORT UNIQUEMENT.** Cet outil ne modifie jamais un fichier.

## Les 5 zones sensibles

| Zone | Quoi | Pourquoi elle casse |
|---|---|---|
| `frontmatter` | Blocs `---` en tete des .md (nom, role, version...) | Parses par les outils : un accent casse la lecture YAML |
| `noms` | Noms de fichiers avec accents (ex: un fichier nomme `prepar[E].md` -> a renommer en `prepare.md`) | Cassent les liens, les grep et les scripts qui referencent ces chemins |
| `blocs` | Commandes dans les blocs ```...``` des .md | Copier-coller casse, les scripts reutilisent ces commandes |
| `code` | Fichiers de code (.sh, .py, .js...) en entier | Un accent dans un script peut casser son execution selon l'encodage |
| `liens` | Liens relatifs `[texte](chemin)` dans les .md | Un accent dans un chemin casse la navigation et les validateurs |

## Utilisation

```bash
# Rechercher dans toutes les zones sensibles d'un dossier
rechercher-accents-sensibles.sh cerveau-projet/

# Rechercher depuis la racine
rechercher-accents-sensibles.sh .

# Zones specifiques
rechercher-accents-sensibles.sh --zones frontmatter,liens cerveau-projet/

# Zone noms uniquement (toutes les extensions, sans limite)
rechercher-accents-sensibles.sh --zones noms .

# Afficher les lignes exactes avec --verbose
rechercher-accents-sensibles.sh --verbose cerveau-projet/

# Extensions de code personnalisees
rechercher-accents-sensibles.sh --extensions sh,py,txt cerveau-projet/
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--zones` | Zones a scanner, separees par des virgules | `frontmatter,noms,blocs,code,liens` |
| `--extensions` | Extensions des fichiers de code | `sh,py,js,json,yaml,yml,txt` |
| `--exclure` | Motifs de chemins a exclure | `node_modules,.git,.agents,.backup,.tmp,test-,dictionnaire-,exemples` |
| `--verbose` | Afficher les numeros de ligne et le contenu | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. **[Noms]** - Recherche les noms de fichiers contenant des caracteres non-ASCII
2. **[Code]** - Scanne les fichiers de code (liste d'extensions) en entier
3. **[Frontmatter]** - Scanne uniquement le bloc YAML `---...---` en tete des .md
4. **[Blocs]** - Scanne uniquement les lignes a l'interieur des blocs ```...```
5. **[Liens]** - Extrait les chemins des liens `[texte](chemin)` et verifie leur encodage
6. **[Rapport]** - Resume par zone avec compteurs ; exit 1 si des problemes existent

## Exemple de sortie

```bash
$ rechercher-accents-sensibles.sh cerveau-projet/

=== Rechercher accents dans les zones sensibles ===
Version : 0.1.0-beta
Dossier : cerveau-projet/

  [noms] cerveau-projet/pense-betes/.../protocole-activation.001.02.prepar[E].md  (exemple reel, a renommer)
  [frontmatter] cerveau-projet/agents/athena/athena.md
  [frontmatter] cerveau-projet/agents/cerberus/cerberus.md

=== Resume ===
Total fichiers examines : 210
Fichiers avec accent en zone sensible : 18
Detections par zone :
  frontmatter YAML : 15
  noms de fichiers : 1
  blocs de code    : 0
  fichiers de code : 0
  liens relatifs   : 2
  TOTAL            : 18

[INFO] Recherche seule : aucun fichier n'a ete modifie.
```

## Difference avec valider-conformite-ascii

| Outil | Portee | Correction |
|---|---|---|
| `valider-conformite-ascii` | Tout le fichier, toutes les extensions | Oui (`--corriger`) |
| `rechercher-accents-sensibles` | 5 zones sensibles uniquement | **Non, rapport seul** |

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Avant de creer un lien** | Verifier que le chemin cible n'a pas d'accent |
| **Avant d'ecrire un script** | Verifier qu'aucune commande ou fichier de code ne traine d'accent |
| **Apres une correction** | Re-lancer pour confirmer que les zones sensibles sont propres |
| **Audit cible** | Trouver les accents qui cassent, sans etre noye par le bruit du texte |

## Exceptions volontaires

Les fichiers `dictionnaire-*.txt` (dictionnaires des outils `corriger-emojis` et `corriger-accents`) sont **exclus automatiquement** : ils contiennent volontairement des caracteres non-ASCII (c'est leur fonction). Voir `regles-emojis-ascii.md` section "Exceptions volontaires".

Le dossier `cerveau-projet/exemples/` est **exclu automatiquement** : c'est la zone de test dediee aux outils (fichiers avec problemes volontaires).

## Notes de creation

- [x] L'outil a ete renomme en `rechercher-accents-sensibles` (categorie Explorer, prefixe rechercher-)
- [x] L'outil est conforme ASCII (aucun accent, aucun emoji)
- [ ] L'outil est reference dans `index-tools.md`
- [ ] Le statut est passe de `ebauche` a `prepare` apres validation RVAV
