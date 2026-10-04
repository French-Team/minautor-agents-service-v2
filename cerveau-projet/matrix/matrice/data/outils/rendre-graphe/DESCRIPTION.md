---
identite:
  type: outil
  appartient_a: matrice-data-outils
  commun: true
---

# OUTIL -- rendre-graphe -- compose un graphe Mermaid et le rend en SVG

> COMPOSER EN MERMAID, CONVERTIR EN SVG (demande du createur 2026-09-26, item
> EO-449, mission MO-493). OPTIMUS lit le MERMAID ; le createur lit le SVG. Les
> deux vues sont le MEME graphe, mesure : ce qui est incoherent y devient VISIBLE
> au lieu de rester cache dans un fichier.

## Options

```
python3 cerveau-projet/matrix/lancer.py rendre-graphe mermaid [--source parcours|vivier|arbre]
                                 [--theme <NOM>] [--arbre <fichier.json>]
                                 [--sortie <fichier>] [--appliquer]
python3 cerveau-projet/matrix/lancer.py rendre-graphe svg
                                 (--mermaid <fichier.mmd> | [--source parcours|vivier|arbre]
                                  [--theme <NOM>] [--arbre <fichier.json>])
                                 [--sortie <fichier>] [--appliquer]
python3 cerveau-projet/matrix/lancer.py rendre-graphe verifier
                                 [--source parcours|vivier|arbre] [--theme <NOM>]
                                 [--arbre <fichier.json>]
```

- `mermaid` : une SOURCE -> le TEXTE Mermaid. Sans `--theme`, la vue est l INDEX du
  parcours (les themes dans leur ordre) ; avec `--theme NOM`, la vue est la suite de
  cases de CE theme, avec ses renvois et sa fin.
- `svg` : du TEXTE Mermaid -> l IMAGE SVG. Le texte vient de `--mermaid <fichier>`
  (un Mermaid ECRIT A LA MAIN : il est LU, jamais reecrit) ou d une source, qui
  passe alors par le meme generateur.
- `verifier` : le JUGE -- LECTURE SEULE. Il ACCUSE (fichiers absents, themes
  orphelins, renvois casses, cases sans etapes, crochets absents, fins inconnues,
  ids et categories hors liste), il ne repare jamais.

## Garanties

- **DRY PAR DEFAUT** : sans `--appliquer`, rien n est ecrit. Une vue qui remplacerait
  la precedente sans le dire serait une vue sans trace.
- Les vues se deposent PAR LA PORTE `ecrire` (perimetre, `.bak`, SHA, ASCII, LF) ;
  les textes passent par des FICHIERS, jamais par la ligne de commande (un accent
  grave y serait EXECUTE -- mesure MO-142).
- **Deterministe** : meme texte -> memes octets. Aucun hasard, aucun horodatage,
  aucun ordre non maitrise : deux vues se COMPARENT.
- **Sans dependance** : le SVG se fabrique en Python pur (ni navigateur, ni node, ni
  reseau). Memoire v1 citee par sa mesure : `constants.MEMOIRE_V1`.
- **ASCII strict** : les libelles sont ASCII et le XML est echappe.
- **Zero valeur en dur** : ma place est DEDUITE et verifiee ; le domicile du vivier
  (nom de BDD, liste FERMEE des categories) se LIT a `theme-vivier/constants.py`
  (M-076).
- Codes : `0` = rendu (ou aucune incoherence), `1` = incoherences (nommees),
  `2` = refus (source inconnue, fichier illisible).

## Architecture (convention-architecture-outils)

| Piece | Role |
|---|---|
| DESCRIPTION.md | la facade (ce fichier) |
| main.py | point d entree global : DIRIGE |
| constants.py | ma place (deduite), les sources, la geometrie, la memoire v1 |
| commun.py | lire une source, ecrire par la porte, lancer un enfant |
| mermaid/ | une source -> un MODELE -> le TEXTE Mermaid (les incoherences y sont des NOEUDS) |
| svg/ | le TEXTE Mermaid -> l IMAGE SVG (moteur porte de la v1) |
| verifier/ | le JUGE des sources (LECTURE SEULE, code 1 = verdict) |

> Le SVG ne consomme JAMAIS le modele : il RELIT le texte Mermaid. C est ce qui
> prouve que la chaine < n importe quoi -> mermaid -> svg > tient de bout en bout.
