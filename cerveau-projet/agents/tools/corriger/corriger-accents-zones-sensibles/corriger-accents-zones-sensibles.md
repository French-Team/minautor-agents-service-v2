---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# corriger-accents-zones-sensibles

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** corriger
**Chemin :** `agents/tools/corriger/corriger-accents-zones-sensibles/`
**Proprietaire :** Buffy (outil partage)

## Description

Corrige les accents et caracteres non-ASCII dans un fichier ou un dossier. Conformement a la regle immuable `regles-emojis-ascii.md`, **aucun caractere non-ASCII n'est tolere** : le mode standard est `--all` qui purge aussi le texte francais et les titres de sections. Le mode sans `--all` ne corrige que les zones sensibles (frontmatter, noms, blocs, code, liens) et ne doit etre utilise que ponctuellement.

**Mode CORRECTIF :** Cet outil modifie les fichiers (avec sauvegarde et dry-run).

## Les 5 zones sensibles

| Zone | Quoi | Pourquoi elle casse |
|---|---|---|
| `frontmatter` | Blocs `---` en tete des .md (nom, role, version...) | Parsed par les outils : un accent casse la lecture YAML |
| `noms` | Noms de fichiers avec accents (ex: un fichier nomme `prepar[E].md`) | Cassent les liens, les grep et les scripts qui referencent ces chemins |
| `blocs` | Commandes dans les blocs ```...``` des .md | Copier-coller casse, les scripts reutilisent ces commandes |
| `code` | Fichiers de code (.sh, .py, .js...) en entier | Un accent dans un script peut casser son execution |
| `liens` | Liens relatifs `[texte](chemin)` dans les .md | Un accent dans un chemin casse la navigation |

## Utilisation

### CLI Python (version 0.2.0-py)

```
python3 corriger-accents-zones-sensibles.py [OPTIONS] <fichier|dossier>

Options :
  --all             Corriger TOUS les accents (mode standard, regle immuable)
  --dry-run         Simuler sans appliquer
  --zones           Zones a corriger (defaut: frontmatter,noms,blocs,code,liens)
  --recursive       Traiter recursivement les sous-dossiers
  --verbose         Afficher les details
  --extensions      Extensions des fichiers de code
  --exclure         Motifs de chemins a exclure
  --dictionnaire    Chemin vers le dictionnaire
  --version         Afficher la version
```

### CLI bash (version originale)

```bash
# Corriger TOUS les accents (mode standard, regle immuable)
corriger-accents-zones-sensibles.sh --all fichier.md

# Apercu des changements
corriger-accents-zones-sensibles.sh --all --dry-run fichier.md

# Zones specifiques (usage ponctuel)
corriger-accents-zones-sensibles.sh --zones frontmatter,liens fichier.md

# Tout le dossier
corriger-accents-zones-sensibles.sh --recursive --all cerveau-projet/

# Mode cible : zones sensibles uniquement (usage ponctuel)
corriger-accents-zones-sensibles.sh fichier.md
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--dry-run` | Simuler sans appliquer les modifications | false |
| `--all` | Corriger TOUS les accents (texte francais et titres inclus) | **recommandee par la regle immuable** |
| `--zones` | Zones a corriger, separees par des virgules | `frontmatter,noms,blocs,code,liens` |
| `--recursive` | Traiter recursivement les sous-dossiers | false |
| `--verbose` | Afficher les details | false |
| `--extensions` | Extensions des fichiers de code | `sh,py,js,json,yaml,yml,txt` |
| `--exclure` | Motifs de chemins a exclure | `node_modules,.git,.agents,.backup,.tmp,test-,dictionnaire-,exemples` |
| `--help` | Afficher cette aide | - |

## Ce que l'outil fait

1. **[Detection]** - Identifie les zones sensibles dans le fichier
2. **[Analyse]** - Repere les caracteres non-ASCII (texte francais compris en mode `--all`)
3. **[Correction]** - Remplace les accents selon le mode choisi
4. **[Verification]** - Confirme que le fichier est propre
5. **[Rapport]** - Resume des changements effectues

## Exemple de sortie

```bash
$ corriger-accents-zones-sensibles.sh --all --dry-run cerveau-projet/agents/buffy/buffy.md

=== corriger-accents-zones-sensibles ===
Version : 0.1.0-beta
Fichier : cerveau-projet/agents/buffy/buffy.md
Zones : frontmatter,noms,blocs,code,liens

  [frontmatter] Ligne 3: 'Nom' -> 'Nom' (accent supprime)
  [liens] Ligne 15: 'cerveau-projet/agents/buffy/corrections.md' -> 'corrections.md' (accent supprime)
  [texte] Ligne 22: 'description avec accents' -> 'description avec accents' (accent supprime)

=== Resume ===
Zones analysees : 5
Corrections appliquees : 3
Accents francais conserves : 0
Caracteres non-ASCII restants : 0

[INFO] Dry-run : aucun fichier n'a ete modifie.
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Apres la creation d'un fichier** | Purifier tous les accents (`--all`) |
| **Avant de valider un lien** | S'assurer que le chemin cible n'a pas d'accent |
| **Apres l'ecriture d'un script** | Verifier qu'aucune commande ne traine d'accent |
| **Audit de conformite** | Purger tout le fichier (`--all`) pour respecter la regle immuable |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `rechercher-accents-sensibles` | Detecte les problemes, cet outil les corrige |
| `valider-conformite-ascii` | Valide la conformite globale |

## Remplacement de corriger-dictionnaire-accents

Cet outil **remplace** `corriger-dictionnaire-accents`.

| Ancien outil | Nouvel outil |
|---|---|
| `corriger-dictionnaire-accents` | `corriger-accents-zones-sensibles` |
| Supprime tous les accents | Corrige tous les accents (`--all`) |
| Pas de distinction | Zones sensibles + mode `--all` |
| -- | Mode `--all` pour conformite stricte |

## Exceptions volontaires

Les fichiers `dictionnaire-*.txt` sont **exclus automatiquement** : ils contiennent volontairement des caracteres non-ASCII.

Le dossier `cerveau-projet/exemples/` est **exclu automatiquement** : c'est la zone de test dediee aux outils.

## Notes de creation

- [x] L'outil est conforme ASCII (aucun accent, aucun emoji)
- [x] L'outil est reference dans `index-tools.md`
- [ ] Le statut est passe de `ebauche` a `prepare` apres validation RVAV

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-py | 2026-08-07 | Version Python creee (meme dossier, meme nom, base sur outil-template.py, lit le dictionnaire existant) |
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |

---
