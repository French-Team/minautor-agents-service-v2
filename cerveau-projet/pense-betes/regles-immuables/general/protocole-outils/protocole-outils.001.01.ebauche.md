# Protocole Immuable -- Boite a Outils

> **Ce protocole est immuable.** Les agents doivent CONSTRUIRE leurs outils, pas juste les utiliser.

---

## Principe Fondamental

> **Ne jamais utiliser une commande sans la transformer en outil reutilisable.**

| Probleme | Solution |
|---|---|
| Chaque agent recree les memes commandes | Outils reutilisables |
| Les erreurs se repetent | Outils qui verifient |
| Pas de tracabilite | Outils historises |

---

## Structure

```
agents/tools/[categorie]/[nom-outil]/
|-- [nom-outil].md        <- documentation
|-- [nom-outil].sh        <- implementation
``-- spec/                 <- specifications
```

---

## Regles

### Regle 1 -- Chaque outil est documente

```markdown
# [Nom de l'outil]
## Objectif
## Utilisation
## Parametres
## Dependances
```

### Regle 2 -- Chaque outil est teste

```
Creer -> Tester en --dry-run -> Valider le resultat -> Appliquer
```

**Regle obligatoire** :
- TOUJOURS tester avec --dry-run d'abord
- Verifier que le resultat est acceptable
- NE JAMAIS appliquer sans verification
- Si probleme -> corriger l'outil avant d'appliquer

### Regle 3 -- Chaque outil est partage

```
Creer dans agents/tools/ -> Documenter dans index-tools.md -> Accessible a tous
```

### Regle 4 -- Pas de references aux outils tiers

```
JAMAIS : read_files, list_directory, glob, code_searcher, write_file, str_replace
TOUJOURS : Decrire CE QUE L'OUTIL FAIT
```

### Regle 5 -- Chaque fichier a un role unique

| Type | Role | JAMAIS |
|---|---|---|
| `index-*.md` | Navigation | Suivi, TODO |
| `convention-*.md` | Conventions | Suivi |
| `protocole-*.md` | Processus | Historique |
| `corrections.md` | Lecons | Navigation |

### Regle 6 -- Chaque outil est assigne a un agent

> **Un outil est assigne a l'agent dont les MISSIONS utilisent cet outil.**

Un outil qui n'est assigne a personne risque de n'etre jamais utilise. Pour assigner un outil, se poser les questions dans l'ordre :

```
1. Cet outil est-il utilise dans une MISSION existante ?
2. Quelle est la NATURE de l'outil ? (structure / fonctionnalite / exploration...)
3. Quel agent est responsable de cette nature de tache ?
4. Si aucun agent ne l'utilise -> outil de support -> Buffy (gestion du cerveau)
```

**Repartition par nature** (liste NON exhaustive, les autres agents peuvent recevoir des outils adaptes a leurs missions) :

| Nature de l'outil | Agent responsable | Exemples |
|---|---|---|
| Coordination, activation | Cerberus | `mettre-a-jour-modifier-agents-md`, `lister-agents` |
| Controle, analyse, structure du cerveau | Buffy | `valider-*`, `corriger-*`, `verifier-documents-manquants` |
| Exploration | Atlas | `lister-*`, `rechercher-*` |
| Statuts et validation | Janus | `lister-statuts`, `changer-statut`, `valider-ebauche` |
| Construction d'outils | Vulcain | `verifier-systeme`, `outil-template`, `corriger-accents-zones-sensibles` |
| Tests fonctionnels | Morpheus | `template-test`, `protection-*` |
| Pense-betes | Athena | `generateurs-squelette-pense-bete`, `creer-remplir-pense-bete`, `valider-pense-bete` |
| Specs | Promethee | `generateurs-squelette-spec`, `creer-remplir-spec`, `valider-spec` |
| Todos | Minerve | `generateurs-squelette-todo`, `creer-remplir-todo`, `valider-todo` |
| README et chronique | Clio | `mettre-a-jour-readme` |
| Evaluation et combos | Themis | `evaluer-*`, `combos-audit-general`, `combos-corriger-non-ascii` |

> **Regle** : Chaque outil cree doit etre assigne a un agent dans sa carte de decision avant d'etre reference dans l'index.

### Regle 7 -- Compatibilite Git Bash (interdiction PCRE)

> **REGLE IMMUABLE** : les scripts ne doivent JAMAIS utiliser le mode PCRE de grep
> (`-P`, `-oP`, `-qP`, `-zP`) ni la construction `\K` (fonctionnalite PCRE).

**Pourquoi** : sur Git Bash Windows, `grep -P` echoue avec "supports only unibyte and UTF-8 locales" (code 2).
L'echec est SILENCIEUX : un `if grep -qP ...` considere l'erreur comme "aucun match" et laisse passer
les fichiers fautifs sans alerte. C'est une faille de detection silencieuse.

**Alternatives obligatoires** :

| Interdit | Raison | Alternative |
|---|---|---|
| `grep -P` | PCRE non fiable sur Git Bash | Python ou grep -E |
| `grep -oP` | PCRE non fiable sur Git Bash | sed BRE |
| `grep -qP` | Echec silencieux (faille) | Python (detection) |
| `\K` | Fonctionnalite PCRE, vide avec -E | sed BRE |
| lookahead / lookbehind | PCRE uniquement | Python (regex) |

**Verification obligatoire avant validation** :
```
grep -rn "grep -[a-z]*P" agents/tools/ --include="*.sh"   # doit etre vide
grep -rn "\\K" agents/tools/ --include="*.sh"              # doit etre vide
```

> **Cas Python** : Python est fiable sur Git Bash pour la detection (encodage) et les regex. C'est l'alternative recommandee quand sed/grep ne suffisent pas.

---

## Processus de creation

> **REGLE OBLIGATOIRE** : Toute creation d'outil passe par le **outil-template** (`agents/tools/outil-template.md` + `agents/tools/outil-template.sh`).

```
1. Identifier le besoin (commande frequente)
2. Concevoir l'outil (objectif, parametres)
3. Copier le outil-template vers agents/tools/[categorie]/[nom-outil]/
   (categorie = dossier d'ACTION : ajouter, analyser, corriger, lister, ...)
4. Remplacer les placeholders [nom-outil] dans le script et la documentation
5. Developper la logique dans [nom-outil].sh
6. Completer la documentation dans [nom-outil].md
7. Tester en --dry-run
8. Ajouter dans index-tools.md
9. Assigner l'outil a l'agent concerne (Regle 6)
10. Verifier l'absence de PCRE (grep -P, \K) -- Regle 7
11. Valider la conformite ASCII (valider-conformite-ascii)
```

**Pourquoi le outil-template ?**

| Sans template | Avec outil-template |
|---|---|
| Chaque outil a une structure differente | Structure standard garantie |
| Le --dry-run est parfois oublie | --dry-run integre par defaut |
| Documentation inegale | Sections standard obligatoires |
| Oublis de referencement | Checklist integree au modele |

---

## Utilisation

```
1. Chercher dans index-tools.md
2. Lire la documentation de l'outil
3. Executer avec les bons parametres
4. Verifier le resultat
```

---

## Boucle de retroaction

```
Utiliser -> Si probleme -> Corriger
         -> Si manque -> Creer
         -> Si incomplet -> Completer
```

---

## Liens

- **Index** : `agents/tools/index-tools.md`
- **Outil-template** : `agents/tools/outil-template.md` et `agents/tools/outil-template.sh` -- modele standard de creation (2 fichiers a la racine de `tools/`)
- **Classeur** : `classeur-variables/index-classeur.md` (pour stocker les resultats)
- **Regles** : `regles-veracite.md` -- ne jamais mentir/supposer
