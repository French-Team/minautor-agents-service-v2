---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# editer-fichier

**Version :** 0.4.1
**Statut :** prepare
**Categorie :** Editer
**Chemin :** `agents/tools/editer/editer-fichier/`
**Proprietaire :** outil partage

## Description

Remplacer une chaine par une autre dans un fichier. Version generique de corriger-liens et corriger-nommage.

**Echec explicite** : si AUCUNE occurrence n'est trouvee, l'outil retourne un code non nul (1) avec un message clair - jamais 0 silencieux. L'agent ne continue jamais en croyant a tort que l'edition a eu lieu.

## Utilisation

```bash
# Remplacer la premiere occurrence
editer-fichier.sh fichier.md "ancien" "nouveau"

# Remplacer toutes les occurrences
editer-fichier.sh --global fichier.md "texte" "remplacement"
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--global` | Remplacer toutes les occurrences | false (premiere seule) |
| `--backup` | Creer une sauvegarde .bak | false |
| `--dry-run` | Simuler sans modifier | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |

## Ce que l'outil fait

1. Verifie que le fichier existe
2. Compte les occurrences
3. Remplace selon le mode (premiere ou global)

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| Corriger un mot | `editer-fichier.sh f.md "faux" "vrai"` |
| Tout remplacer | `editer-fichier.sh --global f.md "X" "Y"` |

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0-beta | 2026-08-05 | Creation initiale |
| 0.2.0 | 2026-08-06 | Passage V2 : tests reels (premiere occurrence, --global, --dry-run, fichier inexistant), promotion prepare |
| 0.3.0 | 2026-08-12 | Qualite pro : echec explicite (0 occurrence -> code 1, jamais 0 silencieux), protection nommage, message d'aide enrichi |
| 0.4.0 | 2026-08-12 | PERFORMANCE (round 2) : une seule passe (test d'existence + replace, plus de double scan count puis replace) |\n| 0.4.1 | 2026-08-12 | SECURITE (round 3) : refus de modifier a travers un lien symbolique, refus octet nul, lecture robuste utf-8-sig + fallback latin-1 (plus de crash sur BOM/latin-1) |

## Notes de creation

- [x] L'outil est conforme ASCII
- [x] L'outil est reference dans index-tools.md
- [x] Le statut est passe de `ebauche` a `prepare`