---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# changer-statut

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** changer
**Chemin :** `agents/tools/changer/changer-statut/`
**Proprietaire :** Janus (outil partage)

---

## Objectif

Changer le statut d'un fichier en le renommant selon la convention.

**Pourquoi cet outil ?**
- Le changement de statut se fait via un renommage
- L'outil automatise l'incrementation du `class` et le changement de `statut`
- Il verifie les liens avant de renommer pour eviter les cassures

---

## Utilisation

### CLI Python (version 0.2.0-py)

```
python3 changer-statut.py <fichier> <nouveau-statut> [OPTIONS]

Options :
  --dry-run     Afficher les changements sans les appliquer
  --force       Forcer le changement meme si des liens pointent vers le fichier
  --verbose     Afficher les details
  --version     Afficher la version
```

### CLI bash (version originale)

```bash
./changer-statut.sh <fichier> <nouveau-statut> [OPTIONS]
```

### Statuts valides

| Statut | Ordre |
|---|---|
| `ebauche` | 1 |
| `prepare` (ASCII pur) | 2 |
| `dev` | 3 |
| `test` | 4 |
| `valide` | 5 |

### Options

| Option | Description |
|---|---|
| `--dry-run` | Afficher les changements sans les appliquer |
| `--force` | Forcer le changement meme si des liens pointent vers le fichier |
| `--verbose` | Afficher les details |
| `--aide` | Afficher l'aide |

### Exemples

```bash
# Passer un ebauche au statut prepare
./changer-statut.sh protocole-xxx.001.01.ebauche.md prepare

# Voir le resultat sans appliquer
./changer-statut.sh --dry-run protocole-xxx.001.01.ebauche.md prepare

# Forcer meme si des liens pointent vers le fichier
./changer-statut.sh --force protocole-xxx.001.01.ebauche.md prepare
```

---

## Resultat

### Exemple de sortie

```
=== Changement de statut ===
Fichier : protocole-xxx.001.01.ebauche.md
Nouveau statut : prepare

--- Details ---
Nom actuel : protocole-xxx.001.01.ebauche.md
Nom nouveau : protocole-xxx.001.02.prepare.md
Class : 01 -> 02
Statut : ebauche -> prepare

--- Verification des liens ---
[OK] Aucun lien trouve

[OK] Fichier renomme avec succes
  protocole-xxx.001.01.ebauche.md -> protocole-xxx.001.02.prepare.md

=== Termine ===
```

---

## Ce que fait l'outil

| Etape | Description |
|---|---|
| 1. Verifier le fichier | Le fichier existe-t-il ? |
| 2. Verifier le statut | Le nouveau statut est-il valide ? |
| 3. Extraire les parties | Nom, id, class, statut actuel |
| 4. Incrementer le class | class += 1 |
| 5. Construire le nouveau nom | [nom].[nouveau_class].[nouveau_statut].md |
| 6. Verifier les liens | Des liens pointent-ils vers le fichier ? |
| 7. Renommer | Appliquer le changement |

---

## Securite

### Verification des liens

L'outil verifie si des liens pointent vers le fichier avant de le renommer.

| Situation | Resultat |
|---|---|
| Aucun lien | [OK] Renommage autorise |
| Liens trouves | [ERREUR] Renommage refuse (sauf avec `--force`) |

### Verification du nom existant

L'outil verifie que le nouveau nom n'existe pas deja.

---

## Relation avec le workflow RVAV

Cet outil est utilise a l'etape **[Valider]** du workflow RVAV :

```
1. [Rechercher] -> lister-statuts pour voir les fichiers
2. [Verifier]   -> valider-ebauche pour chaque fichier
3. [Analyser]   -> Lire le contenu des fichiers
4. [Valider]    -> changer-statut pour appliquer le changement
5. [Purifier]   -> nettoyer-fichier ou condenser-fichier
```

---

## Qui devrait utiliser cet outil ?

| Agent | Quand l'utiliser |
|---|---|
| **Buffy** | Apres avoir valide un fichier ebauche |
| **Janus** | Apres avoir valide un controle de statut |
| **Tout agent** | Apres avoir complete une boucle RVAV |

---

## Dependances

- `bash` -- pour executer les commandes
- `grep` -- pour extraire les informations du nom
- `mv` -- pour renommer le fichier

---

## Notes

- L'outil ne modifie pas le contenu du fichier, seulement le nom
- Le `class` est toujours incremente de 1
- Utiliser `--dry-run` pour verifier avant d'appliquer
- Utiliser `--force` pour ignorer les liens (attention !)

---

## Liens

- **Workflow** : `rvav-workflow.md` -- processus de validation
- **Convention** : `convention-renommage.md` -- format de nommage
- **Outil similaire** : `corriger-nommage` -- corriger le nommage sans changer le statut

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0-py | 2026-08-07 | Version Python creee (meme dossier, meme nom, base sur outil-template.py) |
| 0.1.0 | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
