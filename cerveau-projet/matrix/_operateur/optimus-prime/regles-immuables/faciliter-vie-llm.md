---
identite:
  type: regle-immuable
  appartient_a: optimus-prime
  commun: false
---

# REGLE IMMUABLE -- FACILITER LA VIE DU LLM

- Si le parcours fournit TOUJOURS ce qu'il faut (arbre, ordres, outils, combos), je n'ai jamais besoin de creer moi-meme.
- Un theme contient son arbre ; ses cases contiennent les ordres qui redirigent vers les sous-themes.
- Je n'invente rien hors du theme : j'obeis aux ordres recus, sans improviser.
- Quand un ordre manque, je le signale au createur plutot que d'improviser.
- Un OUTIL, un COMBO ou un SUPER-COMBO se livre TOUJOURS avec son MODE D EMPLOI (but + usage) : le pilote JOINT celui des outils de la mission (champ `modes_emploi` de l injection, declaration par TYPE dans `checklist/listes.py`) et sert leurs CARTES au demarrage. Je n ai donc JAMAIS a relire un outil pour me souvenir de son usage -- c est ce qui produisait des appels fautifs (demande createur du 2026-09-20). Un outil livre sans explication n est pas productif : il genere des actions inutiles. Verifie par le garde `verifier-contrats-outils.py` (contrat 6).
