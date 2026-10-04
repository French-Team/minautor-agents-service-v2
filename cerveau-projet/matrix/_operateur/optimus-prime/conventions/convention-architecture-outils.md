---
identite:
  type: convention
  appartient_a: optimus-prime
  commun: false
---

# CONVENTION -- ARCHITECTURE DES OUTILS

> Source : docs/conversation-unslot-gemma-4.md (bloc "architecture et responsabilite").
> Tout outil Python de la Matrice suit cette structure. Pas d'exception.

## Structure obligatoire

1. **Fichier explicatif global** : decrit l'outil et ses options (la facade).
2. **Point d'entree global** (main.py) : SEUL point d'acces externe.
   - Role : DIRIGER -- parser les options, router vers la categorie demandee.
   - Interdit : logique metier complexe. Le lobby ne fait pas le travail, il oriente.
3. **Dossier par categorie** : chaque groupe de fonctions a SON dossier (le departement).
4. **Point d'entree de categorie** (<categorie>/entry.py) :
   - Interface entre le global et les fonctions internes du groupe.
   - Orchestre les fonctions simples de son dossier, gere les erreurs du groupe.
5. **Fonctions simples** (<categorie>/*.py) : atomiques, une seule tache, reutilisables.

Flux : description -> point d'entree global -> entry.py de categorie -> fonction simple.

## Regles d'or

- **Isolation** : une categorie ne connait pas les fonctions d'une autre categorie
  (sauf via l'orchestrateur global). Modifier une categorie ne doit jamais casser les autres.
- **Rappel de role** : le point d'entree global DIRIGE, le dossier REGROUPE,
  la fonction simple FAIT UNE chose et une seule.
- **Checklist avant livraison** : description presente / orchestration correcte /
  isolation des categories / fonctions atomiques / hierarchie respectee.
