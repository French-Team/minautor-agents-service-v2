---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# detecter-residus

**Version :** 0.1.2
**Statut :** ebauche
**Categorie :** detecter
**Chemin :** `agents/tools/detecter/detecter-residus/`
**Proprietaire :** Hygie (outil partage)

---

## Objectif

Detecter les **residus** du workspace, en **compartimentant par zone**
(cerveau-projet / workspace) comme demande l'utilisateur pour l'agent de
nettoyage Hygie. Chaque zone ne voit que SES residus : aucun chevauchement,
**aucun double comptage** entre les deux zones (v0.1.2). Un residu est un fichier ou dossier qui ne devrait pas etre
la : temporaire, version egaree, sauvegarde, rapport egare, cache.

**Pourquoi cet outil ?**
- Les agents laissent parfois des residus (fichiers temp, rapports egare,
  fichiers de version a la racine)
- Hygie est le SEUL agent habilite a supprimer : il doit d'abord DETECTER
  proprement, zone par zone
- La compartimentation evite de melanger le cerveau (cerveau-projet/) et le
  workspace (futur dossier workspace/)

---

## Utilisation

Version Python (recommandee) :

```bash
python3 detecter-residus.py [--zone <cerveau-projet|workspace|tous>] [options]
```

Version bash equivalente : `detecter-residus.sh` (meme logique).

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `--zone` | choix | Non | Zone a scanner : `cerveau-projet`, `workspace`, `tous` (defaut: `tous`) |
| `--tous` | flag | Non | Scanner les deux zones (alias de `--zone tous`) |
| `--sans-cache` | flag | Non | Ignorer les caches (`__pycache__`/`.pyc`, se regenerent a chaque execution) |
| `--detail` | flag | Non | Afficher le detail par type de residu |
| `--rapport <fichier>` | string | Non | Ecrire le rapport markdown |
| `--verbose` | flag | Non | Afficher les details |
| `--version` | flag | Non | Afficher la version |

---

## Types de residus detectes

| Type | Description | Exemples |
|---|---|---|
| `TEMP` | Scripts/dossiers temporaires | `tmp-*`, `.tmp-*.py`, `.zz-*` |
| `VERSION` | Fichiers de version semver a la racine | `0.2.1`, `v0.2.6` |
| `SAUVEGARDE` | Fichiers de sauvegarde | `*.bak`, `*~`, `*.orig` |
| `RAPPORT_EGARE` | Rapports/audits/controles egare | `rapport-*.md` a la racine |
| `CACHE` | Caches de compilation | `__pycache__/`, `*.pyc` |

---

## Exemple

```bash
# Scanner les deux zones
python3 detecter-residus.py --tous

# Scanner uniquement le cerveau (sans les caches)
python3 detecter-residus.py --zone cerveau-projet --detail --sans-cache

# Scanner uniquement le workspace (futur dossier workspace/)
python3 detecter-residus.py --zone workspace --detail

# Ecrire le rapport
python3 detecter-residus.py --rapport rapport-residus.md
```

---

## Sortie

```
=== detecter-residus v0.1.2 : scan des residus par zone ===
Racine : Z:\analyste-in-console
Date   : 2026-08-13 21:58:00

--- Zone : cerveau-projet ---
  2 residu(s) detecte(s)
    - CACHE (2) : cerveau-projet/agents/tools/tester/tests/test-004-combos-tester-outil/__pycache__; ...

=== RESUME ===
  cerveau-projet : 2 residu(s)
  workspace      : 0 residu(s)

  Verdict : RESIDUS DETECTES (2 residu(s) au total)
```

Le code de retour est 1 si des residus sont detectes, 0 sinon.

---

## Compartimentation stricte (v0.1.1+)

- **zone `cerveau-projet`** : scanne UNIQUEMENT `cerveau-projet/` (fichier par
  fichier, y compris les caches internes)
- **zone `workspace`** : scanne la racine + le dossier `workspace/` mais
  JAMAIS `cerveau-projet/` (ni caches, ni residus internes) - les deux zones
  sont etanches
- **Classification (v0.1.2)** : un rapport `rapport-*/audit-*/controle-*` est
  LEGITIME s il est dans un dossier parent nomme `rapports`/`controles`/
  `rapport`/`controle` (ex. `agents/*/rapports/`, `agents/*/controles/`)
- **Deduplication (v0.1.2)** : un fichier de la racine est compte une seule
  fois (le scan recursif ne le re-detectionne pas)

> Verifie reellement (2026-08-13) : residus factices poses dans les deux
> zones -> chaque zone ne voit que les siens, `--tous` voit les deux sans
> double comptage, et les 171 rapports legitimes des agents ne sont PLUS
> classes a tort en RAPPORT_EGARE.

---

## Dependances

- Python 3 (standard library uniquement)
- Aucune dependance externe

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-13 | Creation initiale (mission Hygie, demande utilisateur) |
| 0.1.1 | 2026-08-13 | Compartimentation stricte (zone workspace ne penetre jamais dans cerveau-projet/) |
| 0.1.2 | 2026-08-13 | Classification des rapports par dossier parent + deduplication (decouverts par le test reel de compartimentation) |

---
