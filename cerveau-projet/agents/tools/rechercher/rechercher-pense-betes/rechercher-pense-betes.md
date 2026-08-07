# rechercher-pense-betes

**Version :** 0.2.0
**Statut :** prepare
**Categorie :** rechercher
**Chemin :** `agents/tools/rechercher/rechercher-pense-betes/`
**Proprietaire :** Athena (outil partage)

## Description

Rechercher les pense-betes existants pour eviter les doublons. L'outil liste les fichiers du type `pense-bete-[theme].[id].[class].[statut].md` et detecte les themes identiques ou **proches** (noms legerement differents) avant toute creation.

> **PHILOSOPHIE** : Athena lance cet outil en **etape 1** de sa mission pour verifier qu'un pense-bete au theme proche n'existe pas deja.

## Utilisation

Version Python (recommandee) :

```bash
# Inventaire complet des pense-betes existants
python3 rechercher-pense-betes.py --tous

# Recherche anti-doublon pour un theme (avant creation)
python3 rechercher-pense-betes.py --theme pipeline

# Avec details de similarite
python3 rechercher-pense-betes.py --theme pipeline --verbose

# Rechercher dans un dossier specifique
python3 rechercher-pense-betes.py --theme pipeline --dossier cerveau-projet/
```

Version bash equivalente : `rechercher-pense-betes.sh` (meme logique).

## Options

| Option | Description | Defaut |
|---|---|---|
| `--theme <motif>` | Rechercher les themes identiques ou proches du motif | (vide = inventaire) |
| `--tous` | Lister tous les pense-betes existants | false |
| `--dossier <chemin>` | Dossier de recherche | racine du projet |
| `--verbose` | Afficher les details de correspondance | false |
| `--help` | Afficher l'aide | - |

## Niveaux de correspondance

| Niveau | Critere | Action |
|---|---|---|
| **[EXACT]** | Le theme est identique au motif | **NE PAS creer** -- doublon |
| **[PROCHE]** | Le theme contient le motif ou l'inverse | **NE PAS creer** -- nom legerement different |
| **[PARTIEL]** | Au moins un mot-cle commun (>= 4 lettres) | Verifier avant de creer |
| **[OK]** | Aucune correspondance | Vous pouvez creer le fichier |

## Ce que l'outil fait

1. **Scan** - Trouve tous les fichiers `pense-bete-*.md` (hors templates et index)
2. **Extrait** - Le theme (partie apres `pense-bete-`) et le statut de chaque fichier
3. **Compare** - Le motif avec chaque theme (exact, partiel, mots-cles)
4. **Rapporte** - Les correspondances avec niveau de risque + verdict

## Exemples de sortie

```bash
$ rechercher-pense-betes.sh --theme pipeline

=== Recherche anti-doublon : theme 'pipeline' ===

  [EXACT] pipeline -> pense-bete-pipeline.001.01.ebauche.md

[ATTENTION] 1 correspondance(s) trouvee(s). Verifiez avant de creer.
-> Ne pas creer si un [EXACT] ou [PROCHE] existe deja.
```

```bash
$ rechercher-pense-betes.sh --tous

=== Inventaire des pense-betes ===
Dossier : .

  THEME                                  FICHIER                        STATUT
  -----------------------------------------------------------------------
  pipeline                               pense-bete-pipeline.001.01.ebauche.md  ebauche

Total : 1 pense-betes
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Avant de creer un pense-bete** | Etape 1 OBLIGATOIRE : verifier qu'aucun theme proche n'existe |
| **Audit des pense-betes** | Inventaire complet des fichiers existants |
| **Detection de doublons** | Trouver les pense-betes avec des noms legerement differents |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `generateurs-squelette-pense-bete` | A lancer SEULEMENT si aucun doublon n'est detecte |
| `lister-agents` | Voir l'agent Athena qui utilise cet outil |
| `valider-nommage` | Verifier la convention de nommage avant creation |

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-06 | Creation initiale |
| 0.2.0 | 2026-08-07 | Passage v2 : frontmatter, VERSION 0.2.0, statut prepare |
| 0.2.0-py | 2026-08-07 | Version Python creee (rechercher-pense-betes.py), basee sur outil-template.py. Inventaire + anti-doublon (EXACT/PROCHE/PARTIEL), exit 1 si doublon |

---
