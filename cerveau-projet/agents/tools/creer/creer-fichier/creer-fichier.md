---
identite:
  type: outil
  appartient_a: commun
  commun: true
  combos:
    - combo-controle-buffy
    - combo-creer-agent
    - combo-creer-fichier-cerveau
    - combo-creer-protocole
    - combo-tester-outil
---
# creer-fichier

**Version :** 0.3.3
**Statut :** prepare
**Categorie :** Creer
**Chemin :** `agents/tools/creer/creer-fichier/`
**Proprietaire :** outil partage

## Description

Creer un nouveau fichier avec verification. L'outil verifie si le fichier existe deja avant de creer (refus explicite si present, sauf `--forcer`). `--backup` sauvegarde l'existant en .bak avant ecrasement.

## Utilisation

**MODE ANTI-HEREDOC (v0.3.3)** : pour un contenu long, l ecrire dans un fichier
puis : `python3 creer-fichier.py fichier.md --contenu-chemin source.txt` (jamais de
ligne bash geante - decision D6/D7 2026-08-21).

### CLI Python (version 0.2.0-py)

```
python3 creer-fichier.py [OPTIONS] <fichier> [contenu]

Options :
  --forcer     Ecraser si le fichier existe
  --dry-run    Simuler sans creer
  --verbose    Afficher les details
  --version    Afficher la version
```

### CLI bash (version originale)

```bash
# Creer un fichier vide
creer-fichier.sh nouveau-fichier.md

# Creer avec du contenu
creer-fichier.sh nouveau-fichier.md "# Titre"

# Ecraser un fichier existant
creer-fichier.sh --forcer fichier.md
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--forcer` | Ecraser si le fichier existe | false |
| `--backup` | Sauvegarder l'existant en .bak avant ecrasement | false |
| `--dry-run` | Simuler sans creer | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie si le fichier existe
2. Cree le repertoire parent si necessaire
3. Cree le fichier (vide ou avec du contenu)

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Creer un nouveau fichier | `creer-fichier.sh fichier.md` |
| Creer avec du contenu initial | `creer-fichier.sh fichier.md "# Titre"` |
| Remplacer un fichier | `creer-fichier.sh --forcer fichier.md` |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.3.3 | 2026-09-02 | MODE ANTI-HEREDOC : option `--contenu-chemin <fichier>` lit le contenu depuis un fichier source (jamais de ligne bash geante, decision D6/D7 2026-08-21). Parite .sh : non concerne (le .sh ne porte pas le mode anti-heredoc - exemption bumper v0.3.2) |
| 0.3.2 | 2026-08-17 | MESSAGES INFORMATIONNELS : rappels apres creation (outil -> index-tools+catalogue+doc+assignation ; rapport -> dossier agent jamais racine) - regle immuable v0.3.0 |
| 0.2.0-py | 2026-08-07 | Version Python creee (meme dossier, meme nom, base sur outil-template.py) |
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels (fichier vide, contenu, refus si existe, --forcer, --dry-run), promotion prepare |
| 0.3.0 | 2026-08-12 | Qualite pro : option --backup avant ecrasement, promotion prepare, version coherente py/sh |
| 0.3.1 | 2026-08-12 | SECURITE (round 3) : refus si chemin est un lien symbolique, refus octet nul, lecture robuste utf-8-sig + fallback latin-1 |

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md
- [x] Le statut est passe de `ebauche` a `prepare`