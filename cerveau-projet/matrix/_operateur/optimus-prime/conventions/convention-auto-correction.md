---
identite:
  type: convention
  appartient_a: optimus-prime
  commun: false
---

# CONVENTION -- AUTO-CORRECTION (doctrine du createur)

> Source : decision du createur, 2026-09-06. Le LLM ecrit avec des accents,
> etc. La Matrice corrige les petites erreurs mecaniques SANS interrompre
> le travail du LLM.

## La doctrine

1. On ACCEPTE que le LLM ecrive avec des accents : la perfection n'est pas
   exigee a la saisie.
2. La Matrice verifie et corrige en ARRIERE-PLAN (routine de veille) les
   fichiers modifies et sauvegardes : accents, fins de ligne, syntaxe.
3. Le LLM n'est PAS informe des micro-corrections : il continue son travail,
   il ne perd pas de temps pour des petites erreurs.
4. Chaque auto-correction est NOTE en BDD (porte unique) : silencieuse pour
   le flux, jamais pour l'audit.
5. Probleme PLUS GRAVE (caractere inconnu, syntaxe Python cassee, ecart de
   marbre non convertible) : PAS d'auto-correction -> alerte intercom ->
   mission de reparation (le pilote decide).

## Les acteurs

| Acteur | Role |
|---|---|
| corriger-ascii | convertit les non-ASCII convertibles (hors BDD empreintees) |
| verifier-conventions / -regles / -protocoles | signalent les ecarts de marbre (lecture seule) |
| py_compile | attrape la syntaxe Python cassee |
| espion-integrite | surveillance des BDD empreintees (ne repare JAMAIS) |
| veille-flux (a construire, M-012) | declenche les combos sur les fichiers modifies, en arriere-plan |

## Frontiere absolue

- Un fichier sous etalon .sha256 n'est JAMAIS reecrit par l'auto-correction.
- L'histoire (fichiers .jsonl en ajout seul) n'est jamais reecrite.
- La reparation d'un probleme grave reste une MISSION (jamais une routine silencieuse).
