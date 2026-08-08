---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
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
| Coordination, activation | Cerberus | `activer-agent-principal`, `lister-agents` |
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

### Regle 8 -- Utilisation EXCLUSIVE des outils du cerveau (IMMUABLE)

> **REGLE ABSOLUE** : pour TOUTE operation (lire, ecrire, editer, chercher, lister, analyser, valider, corriger, purifier...), un agent utilise UNIQUEMENT les outils de `agents/tools/`. Jamais de commande systeme directe, jamais d'outil de l'environnement.

**Interdits formellement** (liste non exhaustive) :

| Interdit | Pourquoi | Alternative |
|---|---|---|
| `cat`, `ls`, `find`, `grep`, `sed`, `awk` en commande directe | Contourne nos outils, pas trace, pas de nos standards | Outils `lire-*`, `rechercher-*`, `lister-*` |
| `python -c "..."` ponctuel | Contourne nos outils, pas de versionnage | Version `.py` de l'outil |
| `bash -c "..."` ponctuel | Contourne nos outils | Version `.sh` de l'outil |
| `read_files`, `write_file`, `str_replace`, `basher` (outils de l'environnement) | Ce ne sont PAS nos outils | Nos outils dans `agents/tools/` |
| Les outils d'un autre agent que le sien | Chaque agent a SES outils assignes | Les outils assignes a SA carte de decision |

**Processus obligatoire** :

```
1. J'ai besoin de faire X -> je cherche l'outil dans index-tools.md (ou mes outils assignes)
2. L'outil existe ? -> je l'execute (version .py si Python dispo, sinon .sh -- voir protocole-technologies)
3. L'outil n'existe pas ? -> je NE contourne PAS avec une commande directe
   -> je signale le besoin (boucle de retroaction) -> Vulcain cree l'outil
4. Je n'utilise JAMAIS l'outil d'un autre agent a la place du mien
```

> **Exception** : `activer-agent-principal` et `verifier-systeme` sont des outils PARTAGES (assignes a plusieurs agents). Tout le reste appartient a un agent precis.
>
> **Application verifiable** : cette regle est renforcee par le cycle A+B+C ci-dessous
> (missions structurees + detection par traces + bilan outils obligatoire).

---

## Cycle anti-contournement A+B+C (IMMUABLE)

> **REGLE ABSOLUE** : la regle declarative ne suffit pas (un LLM utilise naturellement ses outils natifs).
> Le cycle A+B+C rend l'utilisation exclusive VERIFIABLE et SANCTIONNEE.

| Levier | Nom | Mecanisme | Outil |
|---|---|---|---|
| **A** | Missions structurees | Chaque etape de mission impose L'OUTIL EXACT a utiliser (colonne Outil du tableau) : l'agent n'a plus de decision a prendre | REGLE ABSOLUE 5 (fiches agents) |
| **B** | Detection par traces | Les fichiers modifies sont scannes : CRLF, accents, BOM = trace d'outil externe | `detecter-usage-outils-externes` |
| **C** | Bilan outils obligatoire | En fin de mission, l'agent declare la liste EXACTE des outils utilises dans son message de reactivation | REGLE ABSOLUE 6 (fiches agents) |

**Deroulement du cycle :**

```
1. L'agent execute sa mission en utilisant L'OUTIL de chaque etape (levier A)
2. Avant de reactiver Cerberus, l'agent declare son BILAN OUTILS (levier C)
3. Le controleur (Janus/Themis) lance detecter-usage-outils-externes sur les fichiers modifies (levier B)
4. Aucune trace -> mission validee
5. Trace detectee (CRLF, accents, BOM) -> l'agent est sanctionne :
   a. Corriger les fichiers avec NOS outils (regeneration)
   b. Ajouter une lecon dans corrections.md
   c. Le controleur re-verifie
```

**Pourquoi la detection par traces fonctionne :**

| Signature de NOS outils | Trace d'un outil EXTERNE |
|---|---|
| ASCII strict (regle immuable) | Caracteres non-ASCII (accents, emojis) |
| Fins de ligne LF | CRLF (Windows) |
| Pas de BOM | BOM UTF-8 |

**Limite connue** : la lecture seule ne laisse pas de trace. C'est pourquoi le bilan (C)
complemente la detection (B) : la declaration de l'agent est croisee avec les traces reelles.

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
