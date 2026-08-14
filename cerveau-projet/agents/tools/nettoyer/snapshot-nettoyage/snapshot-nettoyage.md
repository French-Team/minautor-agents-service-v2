---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# snapshot-nettoyage

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** nettoyer
**Chemin :** `agents/tools/nettoyer/snapshot-nettoyage/`
**Proprietaire :** Hygie (outil partage)

---

## Objectif

Prendre un **snapshot** de l etat du workspace avant chaque nettoyage (agent
Hygie). Le snapshot est la **preuve de tracabilite** : il inventorie tous les
fichiers presents (chemin + taille + hash) avant toute suppression. Le
snapshot precedent est **consulte au nettoyage suivant**, et les snapshots de
plus de **7 jours** sont supprimes (rotation, decision utilisateur).

**Pourquoi cet outil ?**
- Hygie est le SEUL agent habilite a supprimer sans demande prealable : il
  doit prouver ce qui etait present avant de supprimer
- La comparaison avec le snapshot precedent montre ce qui a change depuis le
  dernier nettoyage
- La rotation 7 jours evite l accumulation de snapshots

---

## Utilisation

Version Python (recommandee) :

```bash
python3 snapshot-nettoyage.py <commande> [options]
```

Version bash equivalente : `snapshot-nettoyage.sh` (meme logique).

---

## Sous-commandes

| Commande | Role |
|---|---|
| `creer` | Prend un snapshot de l etat actuel (inventaire complet : chemin, taille, hash) dans `agents/hygie/snapshots/snapshot-<date>.json` |
| `consulter` | Affiche le snapshot le plus recent (etat avant le dernier nettoyage) |
| `rotation` | Supprime les snapshots de plus de 7 jours |
| `liste` | Liste les snapshots existants |

---

## Emplacement des snapshots

```
cerveau-projet/agents/hygie/snapshots/
  snapshot-2026-08-13-215500.json
  snapshot-2026-08-06-090000.json   (supprime par la rotation 7 jours)
```

---

## Exemple

```bash
# 1. Prendre un snapshot AVANT de nettoyer
python3 snapshot-nettoyage.py creer

# 2. Consulter le snapshot precedent (avant d agir)
python3 snapshot-nettoyage.py consulter

# 3. Apres le nettoyage : appliquer la rotation 7 jours
python3 snapshot-nettoyage.py rotation
```

---

## Contenu d un snapshot

| Cle | Role |
|---|---|
| `date` | Date et heure du snapshot |
| `zone` | Zone scannee (tous par defaut) |
| `nb_fichiers` | Nombre de fichiers inventories |
| `rotation_jours` | Duree de retention (7) |
| `fichiers` | Inventaire : chemin + taille + hash md5 de chaque fichier |
| `suppressions` | Liste des suppressions effectuees apres ce snapshot |
| `verdict` | SNAPSHOT PRIS / Suppressions effectuees / ... |

---

## Dependances

- Python 3 (standard library uniquement)
- Aucune dependance externe

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-13 | Creation initiale (mission Hygie, demande utilisateur) |

---
