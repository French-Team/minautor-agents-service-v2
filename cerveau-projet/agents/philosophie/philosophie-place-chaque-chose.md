---
identite:
  type: philosophie
  appartient_a: commun
  commun: true
---
# Philosophie : Une place pour chaque chose et chaque chose a sa place

## Proverbe

> Une place pour chaque chose et chaque chose a sa place.

## Principe (POURQUOI)

Chaque element du cerveau-projet a une place DETERMINEE par sa nature : un
outil vit dans `agents/tools/<categorie>/<outil>/`, une convention dans
`agents/conventions/`, une regle immuable dans `agents/regles-immuables/`,
une philosophie dans `agents/philosophie/`. Rien n'est cree a la volee hors
de sa place : la place PREEXISTE a l'element. C'est cette place stable qui
rend la recherche fiable : si l'on cherche un generateur, on sait qu'il est
dans `tools/generateurs/` -- pas besoin de chercher ailleurs.

## Mise en pratique (COMMENT)

1. Avant de creer un fichier, un dossier ou un outil, se demander : OU est
   sa place ? (la categorie correspondante qui existe deja : generateurs/,
   valider/, combos/, lire/, ecrire/...)
2. Un element nouveau REJOINT la categorie existante, jamais un emplacement
   improvise : si la categorie n'existe pas encore, la creer avec son index
   (ex: `agents/philosophie/` cree avec son index).
3. Le chemin EST la recherche (convention-structures R7) : connaitre la
   categorie, c'est savoir ou chercher sans exploration.
4. Un element mal place est REPLACE, jamais duplique (la duplication cree
   deux verites).

## Quand (QUAND)

- A la creation de tout fichier, dossier, outil ou combo.
- A la migration : deplacer vers la bonne place, puis reverifier les liens.
- A la recherche : chercher d'abord dans la categorie naturelle de l'element.

## Liens

| Cible | Chemin |
|---|---|
| Convention structures (R7 : les chemins = la recherche) | [agents/conventions/structures/convention-structures.md](../conventions/structures/convention-structures.md) |
| Regles de hierarchie | [agents/regles-immuables/hierarchie/](../regles-immuables/hierarchie/) |
| Index des philosophies | [index-philosophie.md](index-philosophie.md) |
