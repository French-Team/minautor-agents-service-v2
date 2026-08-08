---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# nettoyer-fichier

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** nettoyer
**Chemin :** `agents/tools/nettoyer/nettoyer-fichier/`
**Proprietaire :** Buffy (outil partage)

---

## Objectif

Purifier un fichier en supprimant le contenu non essentiel.

**Pourquoi cet outil ?**
- Les fichiers contiennent trop de remarques et blockquotes
- Les agents sont faineants a la lecture
- Un fichier pur est plus facile a lire et a maintenir

---

## Utilisation

Version Python (recommandee) :

```bash
python3 nettoyer-fichier.py <fichier> [options]
```

Version bash equivalente : `nettoyer-fichier.sh` (meme logique).

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `fichier` | string | Oui | Chemin du fichier a purifier |
| `--dry-run` | flag | Non | Afficher les changements sans les appliquer |
| `--verbose` | flag | Non | Afficher les details |
| `--backup` | flag | Non | Conserver une copie de sauvegarde (fichier.backup) |
| `--aide` | flag | Non | Afficher l'aide |

---

## Ce que fait l'outil

### 1. Supprimer les lignes vides consecutives

Reduit les suites de lignes vides a une seule (le contenu est preserve).

### 2. Supprimer les notes de rappel

Supprime les blockquotes de rappel : `> Note:`, `> Important:`, `> Rappel:`.

### 3. Supprimer les commentaires YAML inutiles

Supprime les commentaires de frontmatter non essentiels : `# Type:`, `# Convention:`, `# Comment devenir`.

### 4. Reduire les blocs de code vides

Supprime les blocs de code ne contenant qu'un commentaire seul (les fences ``` sont conservees).

> **Conserve volontairement** : les blockquotes informatifs (autres que les rappels), les separateurs `---`, le frontmatter YAML (hors commentaires inutiles) et les commentaires YAML potentiellement importants.

---

## Exemple

### Avant

```markdown
## Regle 1
### Comment verifier

1. Executer verifier-systeme
2. Noter les resultats
3. Utiliser les resultats pour le choix
```

### Apres

```markdown
## Regle 1

VERIFIER le systeme AVANT de choisir une technologie.

| Etape | Action |
|---|---|
| 1 | Executer `verifier-systeme` |
| 2 | Noter les resultats |
| 3 | Utiliser pour le choix |
```

---

## Dependances

- Aucune dependance externe

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (nettoyer-fichier.py), basee sur outil-template.py. Portage fidele : lignes vides consecutives, notes de rappel, commentaires YAML inutiles, blocs de code vides. Bug de portage corrige (prefixes de notes) |

---
