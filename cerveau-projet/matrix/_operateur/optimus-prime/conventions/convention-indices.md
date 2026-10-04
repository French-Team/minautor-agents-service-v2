---
identite:
  type: convention
  appartient_a: optimus-prime
  commun: false
---

# CONVENTION -- INDICES (tete de lecture des zones)

> Source : lecon directrice du createur, 2026-09-06. Sans indices, le LLM
> relit des fichiers entiers pour comprendre leur structure : temps perdu,
> risque de derive. L'indice fournit les liens, le contrat fait foi.

## La regle

1. Chaque zone de la Matrice et de l'operateur possede un fichier
   `indices.md` place A LA RACINE de la zone.
2. On lit l'indice AVANT les fichiers de la zone : il dit quel fichier,
   quelle section. JAMAIS de relecture integrale d'une zone pour
   "comprendre".
3. Un doute apres lecture de l'indice = indice incomplet : on l'ameliore
   (petit pas reversible, proto-2), on ne va pas fouiller a la place.

## Format d'un indices.md

- Titre : `# INDICES -- <zone>`
- Ligne d'avertissement : l'indice pointe, le contrat fait foi.
- Table `| Besoin | Lire (fichier, section) |` : les entrees reelles,
  pas de lien mort (verifier les chemins a chaque modification).
- Section `## Conventions de la zone` : 3 a 5 regles de forme a ne pas
  reinventer.

## Le manuel des outils

- Un fichier central : `matrice/data/manuel-outils.md`.
- Une fiche par outil : commandes, protections, quand l'utiliser.
- MIS A JOUR A CHAQUE NAISSANCE OU MODIFICATION D'OUTIL : une mission
  outil ajoute un temps a son ordre de sortie -- tester en reel ->
  relire sur disque -> py_compile global -> METTRE A JOUR LE MANUEL ->
  noter en BDD (porte unique).
- Un outil sans fiche dans le manuel est un outil non livre.

## Templates et duplication

- Le premier moule est EN PLACE : `matrice/templates/outil-bdd/` (jetons,
  modele-mere bdd-lecons) avec l'outil dedie `dupliquer-template`
  (proto-5 : galere native -> outil) -- les sources sont verifiees
  (py_compile + ASCII + jeton residuel) AVANT toute ecriture, jamais
  d'outil a moitie livre.
- Les prochains modeles recurrents (theme, protocole, convention) suivront
  le meme patron : un moule a jetons + un generateur verifiant.
- En attendant un moule dedie : on part d'un outil existant et teste
  comme modele (bdd-lecons est le modele d'outil BDD).
