---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# corriger-fins-de-ligne

**Version :** 0.1.1
**Statut :** prepare
**Categorie :** corriger
**Chemin :** `agents/tools/corriger/corriger-fins-de-ligne/`
**Proprietaire :** commun (outil partage)

---

## Objectif

Convertir les fins de ligne **CRLF vers LF** sur un fichier ou un dossier.
C'est l'outil de reference de la strategie FIGER LF : il normalise les
fichiers qui portent des fins de ligne Windows (CRLF) pour les aligner sur
la regle immuable (LF = signature de nos outils, detecter-usage-outils-externes).

---

## LIRE AVANT USAGE

- L'outil est **en ecriture** : il modifie les fichiers cibles (sauf `--dry-run`).
- Les fichiers **deja en LF** ne sont pas touches (compte "Deja en LF").
- Les fichiers **binaires** (octet nul) sont ignores automatiquement.
- `--dry-run` est OBLIGATOIRE avant toute conversion reelle (bonne pratique).
- Exclusions du scan recursif : `__pycache__/` et `*.pyc`.

---

## Utilisation

### CLI Python (version 0.1.0-py)

```
python3 corriger-fins-de-ligne.py <chemin> [--recursive] [--dry-run] [--verbose] [--version]
```

### CLI Shell (version 0.1.0 -- wrapper pur)

```
bash corriger-fins-de-ligne.sh <chemin> [--recursive] [--dry-run] [--verbose] [--version]
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `chemin` | string | Oui | Fichier ou dossier a convertir |
| `--recursive` | flag | Non | Traiter les sous-dossiers recursivement |
| `--dry-run` | flag | Non | Simuler sans modifier |
| `--verbose` | flag | Non | Afficher le detail de chaque fichier |
| `--version` | flag | Non | Afficher la version |

---

## Resultat

```
=== corriger-fins-de-ligne 0.1.0 -- EXECUTION ===
---
Fichiers analyses : 12
Convertes (CRLF -> LF) : 5
Deja en LF : 7
Binaires ignores : 0
Erreurs : 0
```

---

## Exemples

### Exemple 1 -- Simuler sur un dossier recursif

```
python3 corriger-fins-de-ligne.py agents/tools/ --recursive --dry-run
```

### Exemple 2 -- Convertir un fichier unique

```
python3 corriger-fins-de-ligne.py AGENTS.md
```

### Exemple 3 -- Convertir tout un dossier (apres dry-run)

```
python3 corriger-fins-de-ligne.py agents/tools/ --recursive
```

---

## Notes

- Strategie FIGER LF (decision utilisateur 2026-08-09) : les outils d'ecriture
  doivent produire du LF directement (`newline=''`), cet outil sert a la
  migration des fichiers deja en CRLF et aux corrections ponctuelles.
- Parite py/sh garantie par construction : le `.sh` est un wrapper pur qui
  execute le `.py` (pattern detecter-impacts, cartographier-parcours).

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.1 | 2026-08-09 | Robustesse : conversion des sequences multi-CR (\r+\n) en une passe |
| 0.1.0 | 2026-08-09 | Creation (strategie FIGER LF) |
