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

> REFERENCE : les regles permanentes de round (reprise apres redemarrage,
> mode single-llm) sont aussi gravees dans **AGENTS.md** (section
> Configuration Active) -- les 2 fichiers se referencent mutuellement.
> Elles s appliquent des le demarrage (ORDRE 4 et ORDRE 5 ci-dessous).

## ORDRE 4 -- APRES UN REDEMARRAGE, REVIENS DANS LE FLUX FORMEL

> REGLE PERMANENTE (decision utilisateur 2026-09-02) : APRES CHAQUE
> redemarrage de session, tu ne repars PAS de zero et tu ne demandes PAS
> "Que souhaitez-vous faire ?" : tu REPRENDS le flux formel interrompu.

1. L outil a traite les erreurs bloquantes (ou dit qu il n y en avait pas) :
   si une condition bloquante etait detectee et PAS encore traitee, traite-la
   AVANT toute autre action (etats-cartes residuels -> init_etat :
   etape=debut, precedent=None ; daemons morts -> oracle-demarrage).
2. Continue le ROUND interrompu : relis TA fiche puis TES corrections, puis
   reprends TON arbre a l endroit ou tu t etais arrete (guider-arbre).
3. Si une mission etait en cours dans la file (asap/normale) ou dans un
   etat-carte, elle EST la premiere chose a traiter : reprends-la.
4. Ensuite seulement, tu peux presenter la suite a l utilisateur.

## ORDRE 5 -- MODE SINGLE-LLM (si l utilisateur le declare)

> REGLE PERMANENTE (decision utilisateur 2026-09-02) : quand l utilisateur
> dit "single-llm" (ou "en single-llm", "mode mono"), TU INCARNES TOUS LES
> MAILLONS DU ROUND TOI-MEME - rien ne se passe en arriere-plan.

- AUCUNE activation ne transfere l execution : apres avoir active un agent
  (documentation du role), tu joues IMMEDIATEMENT son role (relire SA fiche
  puis SES corrections, executer SA mission, rendre SA fin vers ORACLE).
- AUCUNE fin passive n est acceptee : chaque fin reactiver-fin <agent> va
  vers ORACLE, le pilote decide, et TU JOUES le maillon largue.
- Le round continue jusqu a la fin de chaine (bilan consolide -> Cerberus).
- Le mode reste actif jusqu a ce que l utilisateur dise le contraire.

## NETTOYAGE -- SI L UTILISATEUR DEMANDE DE NETTOYER LA SESSION

```
python3 outils-llm/nettoyer-session.py <id> <session>
```

L outil vide l encart, l historique, les inbox/outbox JARVIS (freelance)
et purge la BDD. Sans question, obeit. Apres le nettoyage, le LLM est
dans une session propre (rien dans les encarts/historiques).
