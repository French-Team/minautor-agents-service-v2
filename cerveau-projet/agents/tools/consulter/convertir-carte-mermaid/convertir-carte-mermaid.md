---
identite:
  type: fiche-outil
  appartient_a: vulcain
  commun: true
---
# convertir-carte-mermaid

Convertit les cartes de decision des agents (`parcours-<agent>.json`, source
de verite) en graphes **Mermaid** (fichiers `.mmd`) ET en **images SVG**
(fichiers `.svg`), pour visualiser le parcours de chaque agent.

**Categorie** : consulter (lecture/conversion, ne modifie aucune carte)

## Role

Repond a la question " a quoi ressemble la carte de decision de l agent X ? "
en produisant une vue graphique lisible par l humain, generee depuis le JSON
(source de verite) et toujours synchronisee avec lui.

## Sortie

- Un fichier `cartes-vues/mermaid/<agent>.mmd` par agent (16 agents)
- Un fichier `cartes-vues/mermaid/<agent>.svg` par agent (16 images, rendu
  100% local en Python pur, aucune dependance externe)
- Un `cartes-vues/mermaid/index.md` (tableau agent / parcours / version /
  vue / image)
- Le dossier de sortie est **toujours dans `cerveau-projet/`** (jamais a la
  racine du projet ni ailleurs)

## Regles de rendu (.mmd)

| Element de la carte | Rendu Mermaid |
|---|---|
| `case_depart` | noeud `START` (stadium) |
| case avec `branches` non vides (question, controle, action a choix) | losange `{...}`, chaque branche etiquetee par la reponse |
| case avec `suivant` (action, controle, indice) | rectangle `[...]` |
| case `suivant: null` (reactiver l appelant) | arete vers `FIN-APPELANT` |
| case type `fin` | double cercle `([...])`, terminaison |

Contraintes : titres echappes, **ASCII strict, LF pur**, commentaire d entete
`%%` avec agent + version du parcours.

## Regles de rendu (.svg)

- Rendu **deterministe** : meme carte -> memes octets (le garde-fou verifie
  la synchronisation octet a octet)
- Mise en page par etages : rang = chemin le plus long depuis `START`
  (cycles casses par BFS, aretes arriere exclues de la propagation)
- Aretes : droite (rang adjacent), coudee (plusieurs rangs), courbe
  (retour en arriere), arc (boucle sur soi-meme), etiquette sur fond blanc
- Couleurs : rectangle = action, losange = decision, stadium bleu =
  `START`/fin, stadium rose = `FIN-APPELANT`

## Usage

```bash
# Une seule carte (.mmd)
python3 cerveau-projet/agents/tools/consulter/convertir-carte-mermaid/convertir-carte-mermaid.py --agent chiron

# Une seule carte + son image SVG
python3 cerveau-projet/agents/tools/consulter/convertir-carte-mermaid/convertir-carte-mermaid.py --agent chiron --svg

# Toutes les cartes : .mmd + .svg + index.md
python3 cerveau-projet/agents/tools/consulter/convertir-carte-mermaid/convertir-carte-mermaid.py --tous

# Verifier la synchronisation cartes <-> .mmd <-> .svg (rc=0 si OK, 1 sinon)
python3 cerveau-projet/agents/tools/consulter/convertir-carte-mermaid/convertir-carte-mermaid.py --verifier
```

## Garde-fou

L option `--verifier` compare le contenu genere depuis chaque JSON avec le
fichier `.mmd` ET le fichier `.svg` existants : toute carte modifiee sans
regenerer la vue est signalee. La non-regression (test dedie) l utilise pour
exiger 0 ecart.

## Notes

- Le suffixe de type sur les noeuds n est pas utilise (la forme du noeud
  suffit : losange = decision, rectangle = action, stadium = fin).
- La validation structurelle integree verifie : header `flowchart TD`,
  presence du noeud `START`, balises connues, cibles d aretes connues.
- Le rendu SVG est autonome (aucun `node`, aucune bibliotheque) : il se
  visualise dans n importe quel navigateur ou visionneuse d images.

**Version** : 0.2.0
