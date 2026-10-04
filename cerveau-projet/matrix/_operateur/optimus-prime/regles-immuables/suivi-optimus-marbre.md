---
identite:
  type: regle-immuable
  appartient_a: optimus-prime
  commun: false
  decide_par: createur
  date: 2026-09-11
---

# MARBRE -- SUIVI D OPTIMUS-PRIME TOUJOURS A JOUR

> Decrete par le createur (2026-09-11). Inviolable. Seul le createur
> peut modifier ou abroger cette regle.

## La regle

1. **Optimus declare lui-meme** chaque mission dans
   `matrice/data/suivi-optimus.jsonl` via la porte officielle
   (`suivi-optimus/main.py noter`) : `--action debut` a la prise en
   charge, `--action fin` + bilan a la cloture. Une mission = un debut
   + une fin. Le pilote ne note RIEN pour Optimus.
2. **Vue regeneree** (`main.py vue`) apres chaque mission terminee :
   `matrice/suivi-optimus.md` ne doit JAMAIS rester fige.
3. **Jamais edite a la main** : le .md est GENERE depuis le .jsonl
   (journal en ajout seul). Toute correction passe par `noter`.
4. **Zero mission fantome** : aucune mission sans debut, aucune fin
   sans debut (garde anti-fin-orpheline dans `noter`).
5. **Compteurs vrais** : file pilote + journal lus par la vue
   (missions en attente reelles, jamais zero par defaut).

## Sanction

- Vue fige depuis >1 mission terminee = violation du marbre :
  noter + regenerer immediatement, lecon BDD, signaler au createur.
