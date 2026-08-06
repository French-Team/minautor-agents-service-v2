# Outil — Valider un Fichier Ebauche

**Catégorie** : Valider
**Version** : 0.2.0
**Statut** : beta
**Date création** : 2026-08-05
**Propriétaire** : Vulcain (outil partagé)

---

## Objectif

Vérifier si un fichier ebauche respecte les **exigences minimales** d'un ebauche.

**Pourquoi cet outil ?**
- Un ebauche est une idée brute, pas un document structuré
- Cet outil vérifie que le fichier est bien un ebauche (et pas un préparé déguisé)
- Il aide à maintenir la cohérence des statuts

---

## Utilisation

```bash
./valider-ebauche.sh <fichier> [OPTIONS]
```

### Options

| Option | Description |
|---|---|
| `--verbose` | Afficher les détails |
| `--aide` | Afficher l'aide |

---

## Ce que vérifie l'outil

### Exigences minimales (obligatoires)

| Vérification | Critère |
|---|---|
| **Statut** | Le fichier est bien un ebauche |
| **Titre** | Présence d'un titre principal (h1) |
| **Contenu** | Au moins 5 lignes |

### Vérifications de cohérence (avertissements)

| Vérification | Critère |
|---|---|
| **Nommage** | Le nom respecte la convention |
| **Frontmatter** | Pas de frontmatter (inutile pour un ebauche) |
| **Tableaux** | Pas de tableaux (peut-être trop structuré) |
| **Sections** | Pas plus de 3 sections (peut-être trop structuré) |

---

## Résultat

### Exemple de sortie (succès)

```
=== Validation du fichier ebauche ===
Fichier : protocole-xxx.001.01.ebauche.md

--- Vérification du nommage ---
--- Vérification de la structure minimale ---
--- Vérification du contenu minimal ---
--- Vérification : pas trop complet pour un ebauche ---

=== Résumé ===
Erreurs : 0
Avertissements : 1

✅ Le fichier ebauche respecte les exigences minimales
⚠️  Cependant, il semble trop structuré pour un ebauche
    Considérez passer au statut 'préparé'
```

### Exemple de sortie (échec)

```
=== Validation du fichier ebauche ===
Fichier : protocole-xxx.001.01.ebauche.md

--- Vérification de la structure minimale ---
❌ Pas de titre principal (h1)

=== Résumé ===
Erreurs : 1
Avertissements : 0

❌ Le fichier ebauche ne respecte pas les exigences minimales
```

---

## Logique de l'outil

| Statut | Ce que l'outil vérifie |
|---|---|
| **ebauche** | Le fichier respecte les exigences **minimales** d'un ebauche |
| **ebauche** | Le fichier **n'est PAS encore** un préparé (sinon → avertissement) |

---

## Relation avec d'autres outils

| Outil | Usage |
|---|---|
| `valider-ebauche` | Vérifier les exigences minimales d'un ebauche |
| `detecter-erreur-statut` | Détecter les fichiers dont le statut ne correspond pas au contenu |
| `valider-nommage` | Vérifier la conformité du nommage |

---

## Notes

- Un ebauche est une **idée brute**, pas un document structuré
- Si un ebauche est "prêt", c'est une **erreur de statut** (devrait être "préparé")
- Utiliser `detecter-erreur-statut` pour vérifier tous les fichiers d'un coup
