---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# detecter-impacts

**Version :** 0.2.1
**Statut :** ebauche
**Categorie :** Detecter
**Chemin :** `agents/tools/detecter/detecter-impacts/`

## Description

Detecter les fichiers **impliques** par la modification d'un fichier du
cerveau-projet, et signaler ceux qui semblent **non mis a jour**.

**Pourquoi cet outil ?**
- Quand on modifie un agent, un outil, un protocole ou une regle, beaucoup
  d'autres fichiers sont concernes (corrections, parcours, indexes, fiches
  qui citent le fichier...).
- Le cerveau grandit : maintenir cette carte des impacts a la main devient
  impossible.
- Cet outil automatise la reponse a la question :
  **"si je modifie X, quels fichiers sont impliques, et sont-ils a jour ?"**

## Concept fondeur : l'identification dans le fichier

> L'identification vit DANS chaque fichier, pas dans un catalogue externe.
> Chaque fichier du cerveau declare son identite en tete du fichier, dans le
> format adapte a son type :

## Schema hybride v0.2.0 (3 formats)

| Type de fichier | Format identite | Exemple |
|---|---|---|
| `.md` | **Frontmatter YAML** entre `---` et `---` | voir ci-dessous |
| `.py` / `.sh` | **Commentaires en tete** (lignes `#`) | voir ci-dessous |
| `.json` | **Cle top-level** `identite` | `"identite": {...}` (format des parcours) |

### Format .md (frontmatter YAML)

```yaml
---
identite:
  type: fiche-agent   # fiche-agent | corrections | parcours | outil |
                      # protocole | regle | convention | pense-bete |
                      # spec | todo | combo | index | commun
  appartient_a: cerberus   # <agent> ou commun
  commun: false            # true si utilise par tous les agents
---
```

### Format .py / .sh (commentaires)

> **CONTRAINTE DE CONVENTION** : le bloc `identite:` doit etre dans les
> **12 premieres lignes** du fichier, juste apres l'en-tete de nommage
> (shebang, nom, version). Cette fenetre restreinte evite les faux positifs
> quand un en-tete documentaire plus bas mentionne `identite:`.

```python
#!/usr/bin/env python3
# -*- coding: ascii -*-
# mon-outil.py
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun   # <agent> ou commun
#   commun: false

import sys
```

### Format .json (cle top-level)

```json
{
  "identite": {
    "type": "combo",
    "appartient_a": "commun",
    "commun": true
  },
  "cases": []
}
```

### Regles de calcul des impacts

| Cas du fichier modifie | Fichiers impliques | Methode |
|---|---|---|
| `commun: false` (fichier d'une entite) | Tous les fichiers portant la **meme `appartient_a`** | Lecture du frontmatter de chaque fichier du cerveau |
| `commun: true` (fichier partage) | Tous les fichiers qui **referencent** ce fichier | Nom du fichier ou chemin present dans leur contenu |

### Detection "mis a jour"

Un fichier implique est signale **`NON MIS A JOUR`** si sa date de
modification (mtime) est **plus ancienne** que celle du fichier modifie.
Le detecteur **signale**, il ne juge pas : l'agent decide ensuite si le
fichier devait changer (ou justifie pourquoi il n'a pas change).

### Traces historisees (v0.2.1)

> **REGLE (decision utilisateur)** : les fichiers des dossiers
> `controles/`, `rapports/` et `retro-actions/` sont des **traces
> historisees** : des rapports dates figes (controles de Janus, rapports
> de Themis, retro-actions de Vulcain) qui ne seront **jamais** "a jour".
>
> Elles sont **listees** dans le rapport avec le marqueur **`[HISTORISE]`**
> (transparence : on les voit), mais **exclues du verdict** : elles ne
> comptent ni dans "potentiellement non mis a jour", ni dans le
> `VERDICT`. La synthese affiche leur nombre dans une ligne dediee.

| Statut | Sens | Verdict |
|---|---|---|
| `[A JOUR]` | Plus recent ou egal a la modification | Ne penalise pas |
| `[NON MIS A JOUR]` | Plus ancien que la modification | Penalise (a verifier) |
| `[HISTORISE]` | Trace datee (controles/, rapports/, retro-actions/) | **Exclue du verdict** |

## Utilisation

```bash
# Version Python (recommandee)
python3 detecter-impacts.py <fichier-modifie>

# Version bash (parite)
bash detecter-impacts.sh <fichier-modifie>

# Racine de scan differente (utile pour un mini-cerveau de test)
python3 detecter-impacts.py <fichier-modifie> --racine <dossier>

# Avec details
python3 detecter-impacts.py <fichier-modifie> --verbose
```

### Options

| Option | Description | Defaut |
|---|---|---|
| `fichier` | Chemin du fichier modifie (positionnel, obligatoire) | - |
| `--racine <dossier>` | Racine du scan | `cerveau-projet/` du projet |
| `--verbose` | Afficher les details | false |
| `--version` | Afficher la version | - |
| `--help` | Afficher l'aide | - |

### Codes de retour

| Code | Signification |
|---|---|
| `0` | Aucun impact non traite (ou aucun implique) |
| `1` | Des fichiers impliques sont plus anciens que la modification |
| `2` | Fichier introuvable, sans identite, ou racine invalide |

## Exemple de sortie

```
=== Detecter-impacts v0.1.0 === (Statut : ebauche)
Fichier modifie : cerveau-projet/agents/cerberus/cerberus.md
Identite lue    : type=fiche-agent, appartient_a=cerberus, commun=false

=== Fichiers impliques (3) ===
  [NON MIS A JOUR] cerveau-projet/agents/cerberus/corrections.md (identification)
  [A JOUR] cerveau-projet/agents/cerberus/parcours/parcours-cerberus.json (identification)
  [A JOUR] cerveau-projet/agents/index-agents.md (identification)

=== Synthese ===
Impliques trouves : 3
Potentiellement non mis a jour : 1
VERDICT : des fichiers impliques sont plus anciens que la modification.
```

## Integration

- **Combo** : `combo-controle-impacts` (cerveau-projet/combos/) enchaine
  `detecter-impacts` -> `valider-liens` -> fin.
- **Parcours Buffy** : concretise la case c10 "Verifier les dependances".
- **Utilisateurs** : Buffy (developpeur principal), Vulcain (outils),
  Janus/Themis (controles croises).

## Notes

- L'outil ne modifie **jamais** les fichiers : il lit et signale.
- Un fichier sans frontmatter `identite:` est signale avec le code 2 :
  c'est le point de depart de la **migration par vagues** du cerveau vers
  le schema d'identification (agents, puis outils, puis protocoles...).

## Liens

- **Outil similaire** : `verifier-documents-manquants` -- parite .sh/.md
- **Combo** : `combo-controle-impacts` -- suite de controle des impacts
- **Outil de controle** : `valider-liens` -- references croisees

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.1 | 2026-08-08 | TRACES HISTORISEES (decision utilisateur) : les fichiers des dossiers controles/, rapports/ et retro-actions/ sont marques [HISTORISE] dans le rapport mais EXCLUS du verdict (elles ne seront jamais a jour) - distinction reference vivante vs trace historisee, synthese avec ligne dediee, parite py/sh |
| 0.2.0 | 2026-08-08 | SCHEMA HYBRIDE : lire l'identite dans les 3 formats (md frontmatter YAML, py/sh commentaires en tete fenetre 12 lignes, json cle top-level) - debloque la vague 2 (migration des outils agents/tools/). Faux positif corrige : le parseur py/sh lisait le bloc documentaire d'en-tete (fenetre 60 -> 12 lignes) |
| 0.1.1 | 2026-08-08 | CORRECTION BUG (usage reel) : le fichier modifie apparait dans les impliques quand lance sans --racine (comparaison chemin relatif vs absolu) -> resolution des 2 cotes (.resolve()) avant comparaison |
| 0.1.0 | 2026-08-08 | Creation : concept identification dans le fichier (frontmatter identite:), calcul des impacts (appartient_a / commun), detection par mtime, parite py/sh, codes de retour 0/1/2 |
