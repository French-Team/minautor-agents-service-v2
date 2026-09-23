---
identite:
  type: convention
  appartient_a: optimus-prime
  commun: false
---

# CONVENTION -- PY_COMPILE AVANT LIVRAISON

> Source : lecon du 2026-09-06 (controle reel : 25/25 fichiers compilent).
> Un fichier Python qui n'a pas compile n'est pas un livrable, c'est un espoir.

## La regle

1. TOUT fichier `.py` de la Matrice passe `python -m py_compile` avant livraison --
   a la creation comme apres chaque modification.
2. On compile l'ENSEMBLE des fichiers Python de la Matrice (pas seulement le
   fichier touche) : le controle est global, il coute quelques secondes et
   attrape les casses transverses (import, renommage, chemin).
3. Exclusion du controle : `__pycache__` (cache, pas du code).
4. Ordre de sortie d'une mission Python : TESTER en reel -> RELIRE sur disque
   (auto-audit, protocole 4) -> COMPILER l'ensemble (py_compile) -> noter en BDD
   (porte unique). La livraison n'est validee qu'au bout des quatre.

## Pourquoi

- La syntaxe casse parfois loin de l'endroit modifie (import rompu, nom deplace).
- Le test prouve que le chemin emprunte marche ; py_compile prouve que TOUT
  le reste charge encore. Les deux ne se remplacent pas.
- Graver ici evite de redescendre la regle au cas par cas : elle vit avec les
  autres conventions, relue au demarrage.
