---
identite:
  type: regle-immuable
  appartient_a: optimus-prime
  commun: false
---

# REGLE IMMUABLE -- L'ATTENTE NE PROUVE RIEN

> Grave le 2026-09-14 (GO createur). Sources : createur 2026-09-13
> ("attendre n'est pas verifier"), MO-062 / MO-064 (garde des routines,
> lecon L-049), incident du 2026-09-14 (deux attentes de ~10 min dans la
> session alors que la preuve se lisait en une commande).

## La regle

**Une preuve se LIT, elle ne s'ATTEND pas.**

- La cadence d'une routine se lit : ses constantes DECLAREES + son etat
  court PUBLIE. On ne patiente JAMAIS une cadence pour voir des passes
  s'accumuler.
- Un temoin qui a besoin de PLUSIEURS passes pour parler s'annonce
  `recul insuffisant` et s'appuie sur la valeur DECLAREE. Il ne demande
  JAMAIS a l'agent d'attendre que la serie se remplisse : elle se remplit
  SEULE, entre deux missions.
- Toute attente reellement necessaire est DECOUPEE : un drapeau se voit en
  quelques secondes, jamais au bout d'un `time.sleep(cadence)` d'un bloc
  (garde `verifier-sans-attendre.py`).

## Ce que la regle ne dit PAS

- Elle n'interdit pas d'attendre la FIN d'un processus court (un test de
  2 s, un sous-processus a lancer).
- Elle interdit d'attendre une CADENCE pour OBTENIR une preuve : si la
  preuve demande une attente, c'est que le temoin est mal concu.

## Ou la regle se LIT (le garde la surveille)

1. Ce fichier (regle immuable, relu a chaque demarrage).
2. `regles-immuables-readme.md` : l'index des regles immuables.
3. `optimus-prime.md` : la fiche (REGLES ABSOLUES).
4. `protocoles/proto-1-reprise-mission.md` : le protocole injecte au
   demarrage.

Le garde `verifier-sans-attendre.py` (controle `regle-lue-a-l-allumage`)
ACCUSE si l'un de ces quatre emplacements perd la regle : une regle que
personne ne relit ne protege rien.
