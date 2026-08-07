# detecter-usage-outils-externes

**Categorie** : Detecter
**Version** : 0.1.0
**Statut** : prepare
**Date creation** : 2026-08-07
**Proprietaire** : Vulcain (outil partage)

---

## Objectif

Detecter les traces d'utilisation d'outils externes dans les fichiers du cerveau-projet.

**Pourquoi cet outil ?**
- Les agents du cerveau doivent utiliser UNIQUEMENT les outils du cerveau (`agents/tools/`)
- Mais un LLM a naturellement tendance a utiliser ses outils natifs (`read_files`, `write_file`, `bash`...)
- Nos outils laissent des signatures PRECISES : **ASCII strict, fins de ligne LF, pas de BOM**
- Un outil externe laisse des traces differentes : **CRLF, caracteres non-ASCII, BOM**
- Cet outil scanne les fichiers et signale ces traces : la detection est automatique

---

## Utilisation

```bash
# Version Python (recommandee)
python3 detecter-usage-outils-externes.py [CIBLE] [--recursive]

# Version bash equivalente
bash detecter-usage-outils-externes.sh [CIBLE] [--recursive]
```

**Arguments :**
| Argument | Description |
|---|---|
| `CIBLE` | Fichier ou dossier a analyser (defaut: `.`) |
| `--recursive` | Scanner recursivement les sous-dossiers |

**Exit code :**
| Code | Signification |
|---|---|
| `0` | Aucun signe d'outil externe -- conformite OK |
| `1` | Traces detectees (CRLF, non-ASCII, BOM) OU cible introuvable |

---

## Ce que detecte l'outil

| Signe | Detail | Pourquoi c'est suspect |
|---|---|---|
| **CRLF** | Fins de ligne `\r\n` (Windows) | Nos outils ecrivent en LF uniquement |
| **non-ASCII** | Accents, emojis, caracteres Unicode | Nos outils sont ASCII strict (regle immuable) |
| **BOM UTF-8** | Octets `EF BB BF` en tete du fichier | Nos outils n'ecrivent jamais de BOM |
| **encodage non UTF-8** | Fichier binaire ou encodage exotique | Nos outils ecrivent en UTF-8 |

---

## Exemple

```bash
# Analyser tout le cerveau-projet
python3 detecter-usage-outils-externes.py cerveau-projet --recursive

# Analyser un seul fichier
python3 detecter-usage-outils-externes.py AGENTS.md
```

Sortie :

```
PROPRE : AGENTS.md
PROPRE : demarrer.md
SUSPECT: exemples/test-crlf.md
    - CRLF (12 lignes)

=== RESUME ===
Fichiers analyses : 45
Fichiers suspects  : 1
Signes detectes    : 1
VERDICT : traces d'outils externes detectees (CRLF/non-ASCII/BOM)
```

---

## Integration avec le cycle A+B+C

Cet outil est le **levier B** du cycle anti-contournement :

1. **A. Missions structurees** : chaque etape de mission impose l'outil exact (fiches agents)
2. **B. Detection par traces** : `detecter-usage-outils-externes` signale les fichiers modifies
   par un outil externe (CRLF, accents, BOM)
3. **C. Bilan d'outils obligatoire** : l'agent declare les outils utilises en fin de mission,
   Janus/Themis verifient la coherence

Si un fichier porte des traces d'outil externe, l'agent est detecte et doit corriger
(regeneration avec nos outils) + ajouter une lecon dans ses corrections.

---

## Notes

- Cet outil ne peut pas detecter TOUTES les utilisations d'outils externes (ex: lecture seule
  sans ecriture ne laisse pas de trace). Il complemente le bilan d'outils (C) et le
  second controle de Janus.
- Les dossiers `__pycache__` et `.git` sont ignores.
- Extensions analysees : `.md`, `.sh`, `.py`, `.txt`, `.json`.

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-07 | Creation initiale : detection CRLF, non-ASCII, BOM, encodage non UTF-8 (py + sh + md) |
| 0.1.0 | 2026-08-07 | Tests formels Morpheus 41/41 VALIDE (test-001). Correction detection .sh (tr fiabilite au lieu de grep sur caracteres de controle : parite .py/.sh confirmee). Doc test creee. |
