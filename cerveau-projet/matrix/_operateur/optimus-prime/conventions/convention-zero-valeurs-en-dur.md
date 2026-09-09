---
identite:
  type: convention
  appartient_a: optimus-prime
  commun: false
---

# CONVENTION -- ZERO VALEUR EN DUR

> Source : docs/conversation-unslot-gemma-4.md.
> Regle d'or : le code ne doit jamais CONNAITRE les valeurs, il doit savoir OU ALLER les trouver.

## Hierarchie des solutions

1. **Constantes (immuables)** : valeurs fixes et universelles (codes d'etat, limites)
   -> fichier constants.py, en MAJUSCULES, declarees en tete.
2. **Parametres de configuration (changeables)** : URLs, timeouts, chemins
   -> fichier de config (json/yaml) lu AU DEMARRAGE, jamais code dans la logique.
3. **Variables d'environnement (sensibles)** : cles, mots de passe
   -> .env lu au demarrage, jamais dans le depot.

## Regles

- Interdit : nombre magique ou chaine cachee au milieu d'une fonction.
- Les variables utilisees par un fichier sont listees EN TETE du fichier
  ou dans un fichier separe dedie.
- La logique CONSOMME les variables ; elle n'a pas le droit de les CONTENIR.
- But : eliminer les erreurs recurrentes dues aux valeurs cachees qui perturbent les flux.
