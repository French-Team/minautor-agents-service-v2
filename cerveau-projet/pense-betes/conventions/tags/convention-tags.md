---
identite:
  type: convention
  appartient_a: commun
  commun: true
---
# Convention des Tags

## Principe

Les tags sont des **mots-cles de recherche** ajoutes a chaque fichier du
cerveau (agents, outils, parcours, combos, conventions, regles, specs) pour
qu'il soit **retrouvable** quand le cerveau grandit : [tous les outils de
validation], [tous les fichiers lies a l'identification], [tous les
parcours des agents].

Un fichier sans tags est une aiguille dans une botte de foin des 500+ fichiers.

## Emplacement -- cle `tags:` dans le bloc `identite`

Le tag se place dans le **frontmatter YAML**, sous la cle `identite` (a cote
de `type`, `appartient_a`, `commun`) :

```yaml
---
identite:
  type: outil
  appartient_a: commun
  commun: true
  tags:
    - validation
    - nommage
    - ascii
---
```

## Format

| Regle | Detail |
|---|---|
| **Format** | kebab-case : lettres minuscules ASCII + tirets (`validation-nommage`) |
| **Caracteres** | ASCII strict uniquement (aucun accent, emoji ou Unicode) |
| **Nombre** | 2 a 5 tags par fichier (pas plus, pas moins) |
| **Unicite** | Pas de doublon dans la liste |
| **Singulier** | Toujours au singulier (`outil`, pas `outils`) |

## Vocabulaire controle

Les tags proviennent d'un **vocabulaire controle** par categorie. On ne
invente pas un tag : on reutilise un tag existant de la meme categorie.

### Tags transverses (toutes categories)

| Tag | Signification |
|---|---|
| `communs` | Fichier partage entre plusieurs agents |
| `multi-llm` | Concerne le fonctionnement multi-LLM (sessions) |
| `temps-reel` | Concerne l'historique / l'activite en direct |
| `jeu-de-piste` | Concerne les parcours (cartes de decision) |

### Categorie outil

| Tag | Signification |
|---|---|
| `validation` | Valider (nommage, ascii, liens, conventions...) |
| `detection` | Detecter / analyser (impacts, surcharge, usages) |
| `creation` | Creer / generer (fichiers, squelettes, commandes) |
| `lecture` | Lire / lister / afficher |
| `ecriture` | Ecrire / modifier / ajouter / editer |
| `recherche` | Rechercher (texte, fichiers, extensions) |
| `organisation` | Structurer / deplacer / renommer / changer statut |
| `controle` | Controler / verifier / auditer |
| `execution` | Executer des commandes / combos |
| `activation` | Activer / reactiver des agents / sessions |

### Categorie agent

| Tag | Signification |
|---|---|
| `coordination` | Cerberus (gardien, orchestration) |
| `developpement` | Buffy, Vulcain (creation, outils) |
| `exploration` | Atlas (recherche, documentation) |
| `validation-croisee` | Janus, Themis (controle, audit) |
| `tests` | Morpheus (tests, protections) |
| `redaction` | Athena, Promethee, Minerve, Clio (pense-betes, specs, todos, README) |

### Categorie parcours / combo

| Tag | Signification |
|---|---|
| `demarrage` | Parcours de demarrage (demarrer.md) |
| `mission-multiple` | Parcours multi-missions (Pattern 1) |
| `orchestration` | Combo qui enchaine plusieurs outils |

## Regles

1. **Tout fichier du cerveau porte des tags** (2 a 5) des sa creation.
2. **Pilote (2026-08-08)** : la generalisation se fait par vagues -- on tagge
   d'abord un echantillon (outils de validation + fiches agents) pour valider
   la convention avant d'appliquer partout.
3. **Reutilisation** : avant de creer un tag, chercher s'il existe deja dans
   la meme categorie (`rechercher-par-tags` ou grep).
4. **Coherence** : les tags d'un outil refletent ses cas d'usage (ex:
   `valider-nommage` -> `validation`, `nommage`).
5. **Verification** : la conformite des tags (format kebab-case ASCII,
   vocabulaire connu) est verifiee par l'outil dedie lors des audits.

## Exemples

```yaml
# agents/tools/valider/valider-nommage/valider-nommage.md
---
identite:
  type: outil
  appartient_a: commun
  commun: true
  tags:
    - validation
    - nommage
    - communs
---

# agents/cerberus/cerberus.md
---
identite:
  type: fiche-agent
  appartient_a: cerberus
  commun: false
  tags:
    - coordination
    - activation
    - multi-llm
---
```

## Reference croisee

- [convention-renommage.md](../renommage/convention-renommage.md) -- noms des
  fichiers (regle fondamentale : aucun identifiant en mot seul)
- `lister-outils` / `lister-agents` -- options `--tag` pour la recherche par
  tags
- [index-conventions.md](../index-conventions.md) -- index des conventions
