# Convention -- Outils d'Agent
---

## Principe Fondamental
---

## Pourquoi ?

| Probleme | Solution |
|---|---|
| Outil generique = pas optimise | Outil d'agent = optimise pour nos besoins |
| Impossible d'ameliorer les outils existants | Nos outils evoluent avec nous |
| Copier le cerveau d'un projet a l'autre | Les outils sont transferables |

---

## Regles de creation

### Regle 0 -- Utilisation EXCLUSIVE des outils du cerveau (IMMUABLE)

> **REGLE ABSOLUE** : un agent utilise UNIQUEMENT les outils de `agents/tools/` pour toute operation. Jamais de commande systeme directe (`cat`, `grep`, `sed`, `python -c`...), jamais d'outil de l'environnement (`read_files`, `write_file`, `basher`...), jamais l'outil d'un autre agent.

```
1. Operation necessaire -> chercher l'outil (index-tools.md / outils assignes)
2. Outil existe -> l'executer (.py si Python dispo, sinon .sh -- protocole-technologies)
3. Outil absent -> signaler le besoin, NE PAS contourner (Vulcain cree l'outil)
```

### Regle 1 -- Chaque outil est proprietaire

```
Chaque outil a un proprietaire (l'agent qui l'a cree).
Mais il est partage et ameliorable par tous.
```

### Regle 2 -- Chaque outil est documente

```
Chaque outil a :
- Une description (lister-agents.md)
- Une spec technique (spec/spec-*.md)
- Un historique de versions
```

### Regle 3 -- Chaque outil est teste

```
Avant d'etre utilise :
1. Creer l'outil
2. Ecrire les tests
3. Executer les tests
4. Valider par RVAV
```

### Regle 5 -- Compatibilite Git Bash (interdiction PCRE)

```
REGLE IMMUABLE : les scripts ne doivent JAMAIS utiliser
le mode PCRE de grep (-P, -oP, -qP, -zP) ni la
construction \K (fonctionnalite PCRE).

Pourquoi : sur Git Bash Windows, grep -P echoue avec
"supports only unibyte and UTF-8 locales" (code 2).
L'echec est SILENCIEUX : un "if grep -qP ..." considere
l'erreur comme "aucun match" et laisse passer les
fichiers fautifs sans alerte.

Alternatives obligatoires :
- Python  : detection et traitement de texte fiable
  (ex: verifier_ascii via python -c)
- sed BRE : remplacement et extraction simples
  (ex: sed -n 's/.*\]([^)]*).*/\1/p')
- grep -E / -oE : expressions regulieres etendues
  SANS \K et SANS lookahead/lookbehind
```

| Interdit | Raison | Alternative |
|---|---|---|
| `grep -P` | PCRE non fiable sur Git Bash | Python ou grep -E |
| `grep -oP` | PCRE non fiable sur Git Bash | sed BRE |
| `grep -qP` | Echec silencieux (faille) | Python (detection) |
| `\\K` | Fonctionnalite PCRE, vide avec -E | sed BRE |
| lookahead/lookbehind | PCRE uniquement | Python (regex) |

---

## Structure d'un outil d'agent

```
agents/tools/[categorie]/[nom-outil]/
|-- [nom-outil].md           <- documentation principale
|-- [nom-outil].sh           <- implementation (script)
|-- spec/                    <- specification technique (optionnel, pour les outils complexes)
|   ``-- spec-[nom-outil].md
|-- test-[nom-outil].md      <- fichier de test (optionnel, pour les outils testes)
```

> **Note** : la version est portee par le fichier `.md` (ex: `**Version :** 0.1.0-beta`). Il n'existe pas de dossier `versions/` : un outil reste en place et son numero de version evolue dans la documentation.

---

## Cycle de vie d'un outil

```
1. Besoin detecte -> "J'ai besoin de lister les agents"
2. Creation -> Creer l'outil en beta
3. Test -> Tester l'outil
4. Integration -> L'utiliser dans mes missions
5. Amelioration -> Ajouter des fonctionnalites
6. Stabilisation -> Version 1.0.0
7. Partage -> Les autres agents peuvent l'utiliser
```

---

## Exemple concret

### Besoin

Buffy a besoin de lister les agents frequemment.

### Solution

```markdown
# Outil : lister-agents

## Objectif
Lister tous les agents avec leurs informations.

## Utilisation
lister-agents.sh [options]

## Options
| Option | Description |
|---|---|
| `--format table` | Format de sortie (table, liste, JSON) |
| `--champs nom,role,statut` | Champs a afficher |
| `--filtre statut=actif` | Filtrer par statut/role |

## Avantages
- Retourne uniquement les agents
- Format table/liste/JSON
- Filtre par statut/role
```

---

## Transferabilite

### Principe
### Ce qui evolue

| Element | Evolution |
|---|---|
| **Agents** | Plus d'agents dedies |
| **Outils** | Plus d'outils performants |
| **Protocoles** | Plus de processus optimises |
| **Conventions** | Plus de regles documentees |

### Ce qui reste

| Element | Constant |
|---|---|
| **Structure** | Meme organisation |
| **Principes** | Meme philosophie |
| **Cycle** | Cerberus -> Agent -> Cerberus |

---

## Liens

- **Protocole** : `protocole-outils` -- comment creer des outils
- **Convention** : `convention-structures` -- structure des dossiers
- **Regles** : `regles-validation-rigoureuse` -- comment valider

---

> Les agents doivent TOUJOURS creer leurs propres outils.
