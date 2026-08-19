---
identite:
  type: outil
  appartient_a: commun
  commun: true
  combos:
    - combo-corriger-fichier
    - combos-corriger-non-ascii
---
# corriger-emojis

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** corriger
**Chemin :** `agents/tools/corriger/corriger-emojis/`
**Proprietaire :** Buffy (outil partage)

---

## Objectif

Detecter et remplacer les emojis par des symboles ASCII dans les fichiers.

**Pourquoi cet outil ?**
- Les emojis sont interdits dans le cerveau-projet (regle immuable)
- Cet outil automatise la detection et le remplacement
- Il utilise un dictionnaire extensible pour les correspondances

---

## Utilisation

### CLI Python (version 0.2.0-py)

```
python3 corriger-emojis.py <fichier|dossier> [OPTIONS]

Options :
  --dry-run     Afficher les changements sans les appliquer
  --verbose     Afficher les details
  --version     Afficher la version
```

### CLI bash (version originale)

```bash
./corriger-emojis.sh <fichier|dossier> [OPTIONS]
```

### Options

| Option | Description |
|---|---|
| `--dry-run` | Afficher les changements sans les appliquer |
| `--verbose` | Afficher les details |
| `--aide` | Afficher l'aide |

### Exemples

```bash
# Corriger un fichier
./corriger-emojis.sh fichier.md

# Voir les changements sans appliquer
./corriger-emojis.sh --dry-run fichier.md

# Corriger tous les fichiers d'un dossier
./corriger-emojis.sh cerveau-projet/

# Voir les changements sans appliquer
./corriger-emojis.sh --dry-run cerveau-projet/
```

---

## Dictionnaire

L'outil utilise un fichier `dictionnaire-emojis.txt` qui contient les correspondances emoji -> texte.

> **EXCEPTION VOLONTAIRE** : ce dictionnaire contient volontairement des emojis (c'est sa fonction). Il est marque du bandeau `EXCEPTION VOLONTAIRE` et exclu des outils de validation ASCII. Voir `regles-emojis-ascii.md` section "Exceptions volontaires". Ne jamais le purger.

### Format du dictionnaire

```
# Commentaire
EMOJI|REMPLACEMENT
```

### Exemples de correspondances

| Emoji | Remplacement |
|---|---|
| `[OK]` | `[OK]` |
| `[ERREUR]` | `[ERREUR]` |
| `[ATTENTION]` | `[ATTENTION]` |
| `[DOCUMENT]` | `[DOCUMENT]` |
| `[CHECKLIST]` | `[CHECKLIST]` |
| `[GRAPHIQUE]` | `[GRAPHIQUE]` |
| `[RECHERCHE]` | `[RECHERCHE]` |
| `[DEMARRER]` | `[DEMARRER]` |
| `[CONFIGURER]` | `[CONFIGURER]` |
| `[FICHIER]` | `[FICHIER]` |
| `[DOSSIER]` | `[DOSSIER]` |
| `[OUTIL]` | `[OUTIL]` |
| `[CLE]` | `[CLE]` |
| `[LIEN]` | `[LIEN]` |

### Ajouter des emojis au dictionnaire

Editer le fichier `dictionnaire-emojis.txt` et ajouter une ligne :

```
NOUVEL_EMOJI|REMPLACEMENT
```

---

## Structure des fichiers

```
corriger-emojis/
|-- corriger-emojis.sh      # Script principal
|-- corriger-emojis.md      # Documentation
`-- dictionnaire-emojis.txt # Dictionnaire des correspondances
```

---

## Resultat

### Exemple de sortie

```
=== Correction des emojis ===
Cible : cerveau-projet/agents/tools/changer/changer-statut/changer-statut.sh
Dictionnaire : cerveau-projet/agents/tools/corriger/corriger-emojis/dictionnaire-emojis.txt

=== Termine ===
```

---

## Qui devrait utiliser cet outil ?

| Agent | Quand l'utiliser |
|---|---|
| **Buffy** | Apres avoir cree des outils ou des fichiers |
| **Janus** | Pour le controle de conformite |
| **Tout agent** | Avant de valider un fichier |

---

## Depenses

- `bash` - pour executer les commandes
- `sed` - pour remplacer les emojis

---

## Notes

- Utiliser `--dry-run` d'abord pour voir les changements
- L'outil cree une copie de sauvegarde (.bak) avant modification
- Le dictionnaire peut etre etendu facilement
- Les fichiers `.md` et `.sh` sont analyses

---

## Liens

- **Regle** : `regles-emojis-ascii.md` - regle immuable sur les emojis
- **Outil similaire** : `nettoyer-fichier` - purifie un fichier
- **Outil similaire** : `condenser-fichier` - condense un fichier

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-py | 2026-08-07 | Version Python creee (meme dossier, meme nom, base sur outil-template.py, lit le dictionnaire-emojis.txt existant) |
| 0.1.0 | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
