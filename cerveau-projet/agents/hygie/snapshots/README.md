---
identite:
  type: dossier
  appartient_a: hygie
  commun: false
---
# Snapshots de nettoyage -- Hygie

Ce dossier contient les **snapshots** pris par Hygie avant chaque nettoyage
du workspace (regle absolue snapshot avant suppression).

## Format

Chaque snapshot est un fichier JSON : `snapshot-<date>.json` (ex :
`snapshot-2026-08-13-2155.json`).

Contenu du snapshot :

| Cle | Role |
|---|---|
| `date` | Date et heure du snapshot |
| `zone` | Zone scannee (cerveau-projet / workspace / tous) |
| `fichiers` | Inventaire des fichiers presents (chemin + taille) |
| `residus_detectes` | Liste des residus detectes avant suppression |
| `suppressions` | Liste des suppressions effectuees (justifiees) |
| `verdict` | Propre / Residus supprimes / A verifier |

## Rotation 7 jours

Les snapshots de plus de **7 jours** sont supprimes au nettoyage suivant
(commande `snapshot-nettoyage rotation`). Le snapshot precedent est
consulte a chaque nettoyage pour comparer l etat du workspace.

## Regle

Jamais de suppression sans snapshot. Le snapshot est la **preuve de
tracabilite** : il montre ce qui etait present et ce qui a ete supprime.
