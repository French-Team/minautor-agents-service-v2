---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# generateurs-commande

**Version :** 0.2.5
**Statut :** ebauche
**Categorie :** Generateurs
**Chemin :** `agents/tools/generateurs/generateurs-commande/`

## Description

**Generateur de commandes complexes.** L'agent ne compose plus lui-meme les commandes avec les bons parametres : il lance ce generateur, repond aux questions (ou fournit les reponses en une fois), et obtient la commande exacte a lancer, sans erreur de syntaxe ni parametre oublie.

C'est un menu interactif concu pour un agent (sans interface graphique) : l'outil pose une question par parametre, valide chaque reponse, puis compose la commande.

**Source de verite** : chaque commande du catalogue (`catalogue-commandes.json`) est un copier-coller d'un appel d'outil **deja ecrit, corrige et valide** dans `agents/tools/`. Le generateur ne reinvente jamais une commande : il reutilise les modeles valides.

**Catalogue v0.2.9** : **146 commandes** couvrant les outils reels du cerveau-projet (outils + combos + tests). Chaque entree contient le script, le modele compose et les parametres (texte, choix, flag) avec leurs questions.

## Correctif v0.2.5 (2026-08-15, lecon Janus)

**Journalisation du registre** : le generateur journalise son PROPRE NOM (`generateurs-commande`) dans le registre des usages, et non plus le nom de la COMMANDE du catalogue (ex `activer-activer`). Avant v0.2.5, chaque activation via le generateur creait une entree `activer-activer` (OUTIL_HORS_CARTE artificiel, garde-fou test-035) que Janus corrigeait manuellement a chaque tour. La commande generee complete reste dans le champ `commande` du registre (veracite preservee).

## REGLE IMMUABLE : prefixe du dossier

Le nom de l'outil DOIT commencer par le prefixe du dossier de categorie : dossier `generateurs/` -> nom `generateurs-xxx`. La fonction `verifier_nommage` controle cela au demarrage.

## Utilisation

```bash
# Lister les commandes disponibles du catalogue
python3 generateurs-commande.py --liste

# Mode interactif : menu de choix + une question par parametre
python3 generateurs-commande.py

# Generer directement une commande precise (interactif)
python3 generateurs-commande.py --commande activer-activer

# Mode non-interactif : reponses fournies en une fois (tests, automatisation)
python3 generateurs-commande.py --commande remplir-pense-bete --reponses "fichier=pb.md;section=idee;contenu=Mon idee"

# Version bash equivalente
bash generateurs-commande.sh --liste
bash generateurs-commande.sh --commande activer-activer --reponses "session=session-llm-1;agent=Buffy;raison=Corriger un fichier"
```

## Options

| Option | Description | Defaut |
|---|---|---|
| `--liste` | Lister les commandes du catalogue | false |
| `--commande NOM` | Generer une commande precise du catalogue | - |
| `--reponses 'a=b;c=d'` | Reponses fournies en une fois (mode non-interactif) | - |
| `--catalogue CHEMIN` | Chemin du catalogue | a cote du script |
| `--dry-run` | Afficher la commande sans l'executer | false |
| `--verbose` | Afficher les details | false |
| `--help` | Afficher l'aide | - |
| `--version` | Afficher la version | - |

## Ce que l'outil fait

1. **Charge** - Le catalogue `catalogue-commandes.json` (source de verite)
2. **Choisit** - L'agent choisit la commande (numero ou nom)
3. **Interroge** - Pose une question par parametre, avec choix et defaut
4. **Valide** - Verifie chaque reponse (obligatoire, choix, oui/non)
5. **Compose** - Assemble la commande exacte (echappement des guillemets si besoin)
6. **Affiche** - La commande prete a copier-coller et a lancer

## Exemples de sortie

```bash
$ python3 generateurs-commande.py --commande activer-activer --reponses "session=session-llm-3;agent=Vulcain;raison=CREER un outil de test"

=== activer-activer ===
Activer un agent principal dans une session LLM

=== COMMANDE A LANCER ===
python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py activer session-llm-3 Vulcain "CREER un outil de test"
```

## Quand l'utiliser

| Situation | Utilisation |
|---|---|
| **Commande complexe a lancer** | Avant tout appel d'outil a plusieurs parametres, generer la commande |
| **Renommages massifs** | `--commande remplacer-texte` + paires ancien=nouveau |
| **Activation d'agent** | `--commande activer-activer` (session + agent + raison) |
| **Creation de pense-bete** | `--commande generer-squelette-pense-bete` |
| **Audit du cerveau** | `--commande audit-general` |

## Etendre le catalogue

Pour ajouter une commande, editer `catalogue-commandes.json` :

```json
{
  "nom": "mon-nouvel-outil",
  "description": "Description courte",
  "interpreteur": "python3",
  "script": "cerveau-projet/agents/tools/[categorie]/[outil]/[outil].py",
  "modele": "--opt {param1} {param2}",
  "parametres": [
    { "cle": "param1", "question": "Question ?", "type": "texte", "obligatoire": true },
    { "cle": "param2", "question": "Question ?", "type": "choix", "choix": ["a", "b"], "obligatoire": false, "defaut": "a" }
  ]
}
```

**Regle** : le `modele` doit reproduire EXACTEMENT l'appel valide de l'outil (voir sa documentation .md). Ne jamais inventer un appel.

### Types de parametres

| Type | Question | Valeur | Placeholder |
|---|---|---|---|
| `texte` | Question libre | texte | `{cle}` |
| `choix` | Question avec liste | une valeur de `choix` | `{cle}` |
| `flag` | Oui/Non | ajoute `flag` si oui, vide sinon | `{cle}` |
| `quoter: true` | - | entre guillemets `"..."` | `{cle}` |

## Relation avec les autres outils

| Outil | Complement |
|---|---|
| `lister-outils` | Liste les outils disponibles (source du catalogue) |
| `activer-agent-principal` | Premier candidat du catalogue (cycle des sessions) |
| `remplacer-texte` | Renommages massifs (renommage + references) |

## Notes de creation

- [ ] L'outil a ete teste en mode non-interactif (`--reponses`) sur les commandes du catalogue
- [ ] L'outil est conforme ASCII (aucun accent, aucun emoji) -- valider avec `valider-conformite-ascii`
- [ ] L'outil est reference dans `index-tools.md`
- [ ] Le statut est passe de `ebauche` a `prepare` apres validation RVAV
