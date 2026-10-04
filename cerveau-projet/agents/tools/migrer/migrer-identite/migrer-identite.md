---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# migrer-identite

**Version :** 0.2.3
**Statut :** ebauche
**Categorie :** Migrer
**Chemin :** `agents/tools/migrer/migrer-identite/`
**Proprietaire :** outil partage (Vulcain, decision utilisateur)

## Description

Migrer les fichiers vers le **schema hybride v0.2.0** de detecter-impacts :
ajouter le **bloc identite** (`type` / `appartient_a` / `commun`) dans chaque
fichier du cerveau, dans le format adapte a son type.

**Pourquoi cet outil ?**
- Le cerveau grandit : l'identification doit vivre **dans** chaque fichier.
- Migrer ~300 fichiers a la main est impossible et source d'erreurs.
- Cet outil automatise la migration de maniere **idempotente** et **sure**
  (mode `--dry-run` pour previsualiser avant d'ecrire).

## Format du bloc identite (3 formats)

| Type de fichier | Format |
|---|---|
| `.md` | Frontmatter YAML `---` / `identite:` / `---` en tete |
| `.py` / `.sh` | Commentaires `# identite:` dans les 12 premieres lignes |
| `.json` | Cle top-level `"identite": {...}` |

### Type determine automatiquement (v0.2.0 : extension a tout le cerveau)

| Situation | Type | Appartient_a |
|---|---|---|
| Fichier dans un sous-dossier `spec/` | `spec` | defaut (commun) |
| Nom `definition-combo.json` dans un dossier `combos/` | `combo` | defaut (commun) |
| Nom commencant par `combos-` (outils du dossier combos/) | `outil` | defaut (commun) |
| Nom commencant par `tester-` (fichiers de test) | `test` | defaut (commun) |
| `catalogue-commandes.json` | `outil` | defaut (commun) |
| `exemple-combo.json` | `combo` | defaut (commun) |
| Nom `AGENTS.md` (racine du projet) | `racine` | commun |
| Nom `AGENTS-historique.md` (journal des activations) | `historique` | commun |
| Dossier `classeur-variables/` | `classeur` | commun |
| Dossier `pense-betes/` | `pense-bete` | commun |
| Nom contenant `-template` | `template` | commun |
| `.md` hors `agents/tools/` (missions, resumes, priorites) | `note` | dossier parent (ex: vulcain) |
| Defaut | `outil` | defaut (commun) |

> **REGLE** : un `.md` vivant dans `agents/tools/` reste un `outil` ;
> les templates sont detectes par `-template` dans le nom (priorite).

### Exclusions (perimetre decision utilisateur)

- **Traces historisees (v0.2.0)** : les fichiers des dossiers
  `controles/`, `rapports/` et `retro-actions/` (rapports dates figes qui
  ne seront jamais a jour -> on ne leur ajoute pas d'identite)
- **Dossiers hors perimetre (v0.2.1)** : `exemples/` (fichiers de test
  volontairement pollues), `recherches-web/` (resultats de recherches),
  `sauvegardes/` (artefacts de sauvegarde)
- `outil-template.py`, `outil-template.sh`, `outil-template.md`
- `template-test.md` (template de test)
- Fichiers `.sh` ET `.md` dans un dossier `tests/` (le frontmatter custom
  des docs de test est preserve)
- Dossiers `__pycache__`

### Protection : frontmatter existant sans identite

Si un `.md` commence par un frontmatter `---` qui ne contient PAS
`identite:`, c'est un fichier special (doc de test, template, autre
frontmatter). L'outil le **ignore** (`[IGNORE] ... frontmatter-sans-identite`)
sans rien modifier : il ne colle JAMAIS un 2e frontmatter par-dessus.

## Utilisation

```bash
# Lister les fichiers a migrer
python3 agents/tools/migrer/migrer-identite/migrer-identite.py --liste

# Previsualiser sans rien ecrire (dry-run)
python3 agents/tools/migrer/migrer-identite/migrer-identite.py --dry-run

# Migrer pour de vrai (defaut: agents/tools/, commun:true)
python3 agents/tools/migrer/migrer-identite/migrer-identite.py

# Migrer un autre dossier avec une attribution personnalisee
python3 agents/tools/migrer/migrer-identite/migrer-identite.py --racine /chemin --appartient-a cerberus --commun false

# Reinserer meme si present (rare, a utiliser avec precaution)
python3 agents/tools/migrer/migrer-identite/migrer-identite.py --force
```

Version bash equivalente : `agents/tools/migrer/migrer-identite/migrer-identite.sh`
(meme interface, code Python identique embarque).

## Rapport de sortie

```
=== RAPPORT (REEL) ===
  Migres:        N
  Deja presents:N
  Ignores:      N
  Erreurs:      N
  Total:        N
```

Code de retour : `0` si aucune erreur, `1` sinon.

## Garanties

- **Idempotent** : un fichier deja migre est saute (sauf `--force`).
- **ASCII strict** : un contenu genere avec un caractere non-ASCII est
  rejete en erreur (aucune ecriture).
- **Sans effet de bord** : `--dry-run` et `--liste` n'ecrivent jamais.
- **100% stdlib Python** : aucune dependance externe.

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.2 | 2026-08-08 | CORRECTION REGLE DETECTION (decision utilisateur) : la regle v0.2.1 `combos- OU dossier combos/` etait TROP LARGE -> typait a tort les outils du dossier combos/ (combos-moteur, combos-audit-general, combos-corriger-non-ascii, combos-valider-cerveau) en `combo`. Desormais : `definition-combo.json` = `combo` (uniquement les vraies definitions), `combos-*` = `outil`, `tester-*` = `test` (NOUVEAU TYPE dedie, priorite haute). 12 outils re-types en outil + 2 tests migres manuellement (l outil aurait casse les heredocs de test) + valider-nommage.sh repare. Parite py/sh, idempotence 0 migre. |
| 0.2.1 | 2026-08-08 | CORRECTIONS (decouvertes au dry-run reel avant application vague 3) : type combo pour les definition-combo.json du dossier combos/ (detection par dossier en plus du prefixe) ; exclusions exemples/ (test pollue), recherches-web/ (recherches), sauvegardes/ (artefacts) |
| 0.2.0 | 2026-08-08 | EXTENSION VAGUE 3 : migration possible sur tout le cerveau (pas seulement agents/tools/) - nouveaux types racine (AGENTS.md), classeur (classeur-variables/), pense-bete (pense-betes/), template (-template), note (.md hors outils -> appartient_a = dossier parent) ; exclusions traces historisees (controles/, rapports/, retro-actions/) ; compatibilite retrograde agents/tools/ inchangee |
| 0.1.0 | 2026-08-08 | Creation (vague 2 : migration schema hybride v0.2.0) |
| 0.1.1 | 2026-08-08 | Correction bug : _a_identite_md ne retournait True que sur la fermeture --- (4 fichiers avec frontmatter custom marques DEJA a tort) ; ajout protection frontmatter-sans-identite (ignore, jamais de double frontmatter) ; exclusion elargie aux .md de tests/ + template-test.md |
| 0.1.2 | 2026-08-08 | Correction bug : _migrer_py_sh insere le bloc a la ligne 13 (hors fenetre 12) pour les fichiers a long en-tete documentaire -> desormais s arrete apres l en-tete court (1re ligne vide) ; retire tout bloc existant avant insertion (jamais de doublon) ; mode REPARER (bloc present mais au-dela de la ligne 12 -> deplace sans doublon) ; detecter-impacts peut lire tous les blocs |
| 0.1.3 | 2026-08-08 | Correction bug residuel : en-tete suivi de commentaires documentaires SANS ligne vide (ligne # seul) -> la boucle traversait tout jusqu a l indice 12 ; desormais insertion APRES la ligne # Statut (ou # Version si pas de Statut) dans les 12 premieres lignes, fallback ancienne logique |
