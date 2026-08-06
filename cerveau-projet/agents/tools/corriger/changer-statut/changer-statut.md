# Outil — Changer le Statut d'un Fichier

**Catégorie** : Corriger
**Version** : 0.1.0
**Statut** : beta
**Date création** : 2026-08-05
**Propriétaire** : Vulcain (outil partagé)

---

## Objectif

Changer le statut d'un fichier en le renommant selon la convention.

**Pourquoi cet outil ?**
- Le changement de statut se fait via un renommage
- L'outil automatise l'incrémentation du `class` et le changement de `statut`
- Il vérifie les liens avant de renommer pour éviter les cassures

---

## Utilisation

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
| `--force` | Forcer le changement même si des liens pointent vers le fichier |
| `--verbose` | Afficher les détails |
| `--aide` | Afficher l'aide |

### Exemples

```bash
# Passer un ebauche au statut prepare
./changer-statut.sh protocole-xxx.001.01.ebauche.md prepare

# Voir le résultat sans appliquer
./changer-statut.sh --dry-run protocole-xxx.001.01.ebauche.md prepare

# Forcer même si des liens pointent vers le fichier
./changer-statut.sh --force protocole-xxx.001.01.ebauche.md prepare
```

---

## Résultat

### Exemple de sortie

```
=== Changement de statut ===
Fichier : protocole-xxx.001.01.ebauche.md
Nouveau statut : prepare

--- Détails ---
Nom actuel : protocole-xxx.001.01.ebauche.md
Nom nouveau : protocole-xxx.001.02.prepare.md
Class : 01 -> 02
Statut : ebauche -> prepare

--- Vérification des liens ---
[OK] Aucun lien trouvé

[OK] Fichier renommé avec succès
  protocole-xxx.001.01.ebauche.md -> protocole-xxx.001.02.prepare.md

=== Terminé ===
```

---

## Ce que fait l'outil

| Étape | Description |
|---|---|
| 1. Vérifier le fichier | Le fichier existe-t-il ? |
| 2. Vérifier le statut | Le nouveau statut est-il valide ? |
| 3. Extraire les parties | Nom, id, class, statut actuel |
| 4. Incrémenter le class | class += 1 |
| 5. Construire le nouveau nom | [nom].[nouveau_class].[nouveau_statut].md |
| 6. Vérifier les liens | Des liens pointent-ils vers le fichier ? |
| 7. Renommer | Appliquer le changement |

---

## Sécurité

### Vérification des liens

L'outil vérifie si des liens pointent vers le fichier avant de le renommer.

| Situation | Résultat |
|---|---|
| Aucun lien | [OK] Renommage autorisé |
| Liens trouvés | [ERREUR] Renommage refusé (sauf avec `--force`) |

### Vérification du nom existant

L'outil vérifie que le nouveau nom n'existe pas déjà.

---

## Relation avec le workflow RVAV

Cet outil est utilisé à l'étape **[Valider]** du workflow RVAV :

```
1. [Rechercher] -> lister-statuts pour voir les fichiers
2. [Vérifier]   -> valider-ebauche pour chaque fichier
3. [Analyser]   -> Lire le contenu des fichiers
4. [Valider]    -> changer-statut pour appliquer le changement
5. [Purifier]   -> purifier-fichier ou condenseur
```

---

## Qui devrait utiliser cet outil ?

| Agent | Quand l'utiliser |
|---|---|
| **Buffy** | Après avoir validé un fichier ebauche |
| **Janus** | Après avoir validé un contrôle de statut |
| **Tout agent** | Après avoir complété une boucle RVAV |

---

## Dépendances

- `bash` — pour exécuter les commandes
- `grep` — pour extraire les informations du nom
- `mv` — pour renommer le fichier

---

## Notes

- L'outil ne modifie pas le contenu du fichier, seulement le nom
- Le `class` est toujours incrémenté de 1
- Utiliser `--dry-run` pour vérifier avant d'appliquer
- Utiliser `--force` pour ignorer les liens (attention !)

---

## Liens

- **Workflow** : `rvav-workflow.md` — processus de validation
- **Convention** : `convention-renommage.md` — format de nommage
- **Outil similaire** : `corriger-nommage` — corriger le nommage sans changer le statut
