---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# DEMARRAGE OBLIGATOIRE -- SUIS LES ORDRES, SANS QUESTION

> ACTION IMPERATIVE : tu es au demarrage d une session LLM. Tu suis les
> ordres ci-dessous COMME UN SOLDAT : sans chercher a savoir, sans poser
> de question, sans proposer d alternative, sans attendre de confirmation.
> L'utilisateur va te fournir les informations. Tu les passes a l outil.

## ORDRE 1 -- DEMANDE LES INFORMATIONS

Demande a l'utilisateur (une seule fois, pas de blabla) :

```
id=<ton id> session=<admin|freelance>
```

Exemple : `id=glm5 session=admin` ou `id=freebuff session=freelance`.

> Si l'utilisateur les a deja fournies dans sa phrase, passe directement
> a l'ORDRE 2. NE POSE AUCUNE AUTRE QUESTION.

## ORDRE 2 -- EXECUTE L'OUTIL DE DEMARRAGE (obligatoire, immediat)

```
python3 outils-llm/demarrer-llm.py <id> <session>
```

L'outil fait TOUT le reste : verifier/creer l'id, t'activer dans la bonne
session, synchroniser les sources, historiser ton demarrage, afficher ton
parcours.

## ORDRE 3 -- SUIS LE RESULTAT DE L'OUTIL

L'outil te dit QUI tu es (agent actif), TA fiche, TES corrections et TON
parcours. Execute exactement ce qu'il affiche : relis TA fiche puis TES
corrections, puis suis TON parcours/arbre.

REGLE : NE DEMANDE JAMAIS "Que souhaitez-vous faire ?" -- la seule action
possible a ce stade est d executer l outil de demarrage. Execute-le.
