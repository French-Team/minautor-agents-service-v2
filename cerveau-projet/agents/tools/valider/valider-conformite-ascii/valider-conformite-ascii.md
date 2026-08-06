# valider-conformite-ascii

**Version :** 0.1.2-beta
**Statut :** ebauche
**Categorie :** Valider
**Chemin :** `agents/tools/valider/valider-conformite-ascii/`

## Description

Valider la conformite ASCII de tous les fichiers du projet. Detecte et corrige automatiquement les caracteres non-ASCII (accents, emojis, symboles Unicode).

## Utilisation

```bash
# Valider tous les fichiers
valider-conformite-ascii.sh

# Valider un dossier specifique
valider-conformite-ascii.sh cerveau-projet/

# Voir les details
valider-conformite-ascii.sh --verbose cerveau-projet/

# Corriger automatiquement
valider-conformite-ascii.sh --corriger cerveau-projet/

# Mode dry-run (sans appliquer)
valider-conformite-ascii.sh --dry-run cerveau-projet/
```

## Options

| Option | Description |
|---|---|
| `--dry-run` | Afficher les erreurs sans corriger |
| `--verbose` | Afficher les details |
| `--corriger` | Corriger automatiquement les fichiers |
| `--extensions` | Filtrer par extensions (ex: md,sh,txt) |
| `--exclure` | Exclure des dossiers (ex: .git,node_modules) |
| `--help` | Afficher l'aide |

## Ce que l'outil fait

1. **Detection** - Trouve les caracteres non-ASCII dans chaque fichier
2. **Analyse** - Identifie le type de caracteres (accents, emojis, symboles)
3. **Correction** - Applique les remplacements via le dictionnaire (via perl pour UTF-8)
4. **Verification** - Confirme que tous les caracteres ont ete remplaces

## Dependances

| Outil | Usage |
|---|---|
| `perl` | Correction UTF-8 (version >= 5.38) |
| `grep -P` | Detection des caracteres non-ASCII |
| `dictionnaire-accents.txt` | Liste des remplacements |

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Avant commit** | Verifier que tous les fichiers sont ASCII |
| **Apres creation** | S'assurer qu'un nouveau fichier respecte la regle |
| **Audit** | Scanner tout le projet pour les incoherences |
| **Nettoyage** | Corriger automatiquement les fichiers problematiques |

## Relation avec les regles

Cet outil est lie a la regle immuable `regles-emojis-ascii.md` :
- Les emojis sont interdits dans le cerveau-projet
- Les caracteres non-ASCII (accents) doivent etre remplaces par leur equivalent ASCII
- Symboles autorises : `[OK]`, `[ERREUR]`, `[ATTENTION]`, `-->`, `<=`, `>=`

## Exemples

### Detecter les fichiers non-ASCII

```bash
$ valider-conformite-ascii.sh --dry-run cerveau-projet/

=== Valider conformite ASCII ===
Version : 0.1.2-beta
Dossier : cerveau-projet/

Fichier : cerveau-projet/agents/test.md
Caracteres non-ASCII detectes :
5: Ceci est un test avec des accents

=== Resume ===
Total fichiers : 150
Fichiers ASCII : 148
Fichiers non-ASCII : 2

[DRY-RUN] Aucune correction appliquee
```

### Corriger les fichiers

```bash
$ valider-conformite-ascii.sh --corriger cerveau-projet/

=== Valider conformite ASCII ===
Version : 0.1.2-beta
Dossier : cerveau-projet/

  [OK] Corrige : cerveau-projet/agents/test.md
  [OK] Corrige : cerveau-projet/agents/autre.md

=== Resume ===
Total fichiers : 150
Fichiers ASCII : 150
Fichiers non-ASCII : 0
```

## Dictionnaire

Le dictionnaire `dictionnaire-accents.txt` contient les remplacements :

| Categorie | Exemples |
|---|---|
| Accents francais | e->e, e->e, a->a, c->c |
| Ligatures | oe->oe, ae->ae |
| Guillemets courbes | '->', " -> " |
| Symboles | ...->..., -->->--> |

## Statut

| Etape | Statut |
|---|---|
| Detection des accents | Termine |
| Detection des emojis | Termine |
| Correction automatique | Termine |
| Integration avec dictionnaire | Termine |
| Tests | Termine |
| Documentation | Termine |

## Notes

- L'outil utilise `perl` pour la correction UTF-8 (plus fiable que `sed` sur Git Bash)
- Les fichiers `.git` et `node_modules` sont exclus par defaut
- Le mode `--corriger` ecrase le fichier original
- L'outil peut traiter n'importe quelle extension de fichier

## Exceptions volontaires

Les fichiers nommes `dictionnaire-*.txt` (dictionnaires des outils `corriger-emojis` et `corriger-accents`) sont **exclus automatiquement** : ils contiennent volontairement des caracteres non-ASCII (c'est leur fonction). Voir `regles-emojis-ascii.md` section "Exceptions volontaires".

Le dossier `cerveau-projet/exemples/` est **exclu automatiquement** : c'est la zone de test dediee aux outils (fichiers avec problemes volontaires).
