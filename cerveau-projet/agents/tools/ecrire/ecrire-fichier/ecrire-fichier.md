---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# ecrire-fichier

**Version :** 0.3.3
**Statut :** prepare
**Categorie :** Ecrire
**Chemin :** `agents/tools/ecrire/ecrire-fichier/`
**Proprietaire :** outil partage

## Description

Ecrire ou ecraser le contenu d'un fichier. Supporte l'ecriture depuis un argument ou depuis stdin.

## Utilisation

**MODE ANTI-HEREDOC (v0.3.3)** : pour un contenu long, l ecrire dans un fichier
puis : `python3 ecrire-fichier.py fichier.md --contenu-chemin source.txt` (jamais de
ligne bash geante - decision D6/D7 2026-08-21).

```bash
# Ecrire du contenu
ecrire-fichier.sh fichier.md "# Nouveau contenu"

# Version Python (recommandee)
python3 ecrire-fichier.py fichier.md "# Nouveau contenu"

# Ecrire depuis stdin
echo "texte" | ecrire-fichier.sh fichier.md -

# Version Python depuis stdin
echo "texte" | python3 ecrire-fichier.py fichier.md -

# Avec sauvegarde
ecrire-fichier.sh --backup fichier.md "# Nouveau"
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--backup` | Creer une sauvegarde .bak avant | false |
| `--dry-run` | Simuler sans ecrire | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie les arguments
2. Cree une sauvegarde si demandee
3. Ecrase le contenu du fichier

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Remplacer tout le contenu | `ecrire-fichier.sh fichier.md "nouveau"` |
| Ecrire depuis un pipe | `commande \| ecrire-fichier.sh fichier.md -` |

## Versionning

| Version | Date | Changements |
|---|---|
| 0.3.3 | 2026-09-02 | MODE ANTI-HEREDOC : option `--contenu-chemin <fichier>` lit le contenu depuis un fichier source (jamais de ligne bash geante, decision D6/D7 2026-08-21). Parite .sh : non concerne (le .sh ne porte pas le mode anti-heredoc - exemption bumper v0.3.2) |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels (ecriture contenu, stdin, --dry-run), promotion prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (ecriture, ecrasement, --backup, --dry-run, stdin) |
| 0.3.0 | 2026-08-12 | Qualite pro : version coherente py/sh (0.3.0), promotion prepare |
| 0.3.1 | 2026-08-12 | SECURITE (round 3) : refus d ecrire a travers un lien symbolique, refus octet nul, backup en copie binaire (shutil) pour ne pas corrompre les fichiers non-UTF-8 |
| 0.3.2 | 2026-08-12 | ROBUSTESSE (round 4) : contenu vide = troncature explicite a zero octet avec message INFO (plus de no-op silencieux) - parite py/sh |

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md
- [x] Le statut est passe de `ebauche` a `prepare`