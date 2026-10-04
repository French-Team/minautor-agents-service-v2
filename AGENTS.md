---
identite:
  type: racine
  appartient_a: commun
  commun: true
---
# Agents du Cerveau-Projet -- v3 / Matrice

> Ce fichier est mis a jour dynamiquement PAR LA MATRICE SEULE, a l interior du
> bloc delimite `session-matrix` (outil `editer-agents-md`). Hors de ce bloc,
> rien ne bouge tout seul.
>
> Le demarrage v3 est `demarrer-optimus-prime.md` (flux 2, maintenance) ou
> `demarrer-cameleon.md` (flux 1, communication). La v3 vit dans
> `cerveau-projet/matrix/`.
>
> Les versions anterieures (v1 session-admin, v2 session-freelance) ont ete
> SUPPRIMEES (decision du createur) : il n en reste aucun vestige dans ce
> depot. Ce fichier ne decrit donc que la v3.

---

## Sessions LLM

Il n y a qu UNE session : `session-matrix`. UN SEUL LLM, UN SEUL agent
(`cameleon`, personnalite fournie par le vivier a chaque mission), UN SEUL flux
actif a la fois (`selecteur-flux`).
<!-- session-matrix:DEBUT (v3, gere par l'outil matrice editer-agents-md) -->

### Session : session-matrix (v3 / Matrice)

| Champ | Valeur |
|---|---|
| **Nom LLM** | glm5 |
| **Agent actif** | cameleon |
| **Role Agent** | agent unique de la Matrice (personnalite fournie par le vivier) |
| **Derniere mise a jour** | 2026-10-04 10:34:37 |
| **Raison** | Bloc unique du depot : la v3 est seule (les versions anterieures ont ete supprimees). Demarrage : demarrer-optimus-prime.md (flux 2) ou demarrer-cameleon.md (flux 1). |

Flux v3 : la Matrice accueille au demarrage -> l'operateur fait sa demande ->
la Matrice lance le cameleon pour sa mission (serial stricte).

<!-- session-matrix:FIN -->

---

## Configuration Active

### Regles permanentes de round (decision utilisateur 2026-09-02)

1. **REPRISE APRES REDEMARRAGE** : apres CHAQUE redemarrage de session, le
   round interrompu REPREND -- l agent ne repart pas de zero et ne demande
   jamais "Que souhaitez-vous faire ?" : il traite les erreurs bloquantes
   restantes puis continue TON arbre a l endroit ou il s etait arrete,
   missions en file comprises.
2. **MODE SINGLE-LLM** : quand l utilisateur dit "single-llm" (ou "mode
   mono"), le LLM incarne TOUS les maillons du round lui-meme : apres chaque
   activation il joue immediatement le role de l agent actif, jusqu a la fin
   de chaine.
3. **TRAVAIL EN SERIE OBLIGATOIRE (decision utilisateur 2026-09-05)** : en
   mode single-llm, un SEUL agent est incarne a la fois. Une seule mission
   est relayee a la fois : elle doit etre TERMINEE avant de relayer la
   suivante. Jamais 2 missions relayees simultanement.

### Limites

- **PERIMETRE D ECRITURE** : la v3 n ecrit QUE dans `cerveau-projet/matrix/`,
  et par les portes officielles (lanceur `lancer.py`, jamais d ecriture a la
  main). `AGENTS.md` n est edite que par la porte `editer-agents-md`.
- **UNE SEULE VERSION** : ce depot ne contient que la v3. Les ancetres (v1,
  v2) ont ete supprimes -- il n y a plus de banque de ressources, plus
  d agents ancetres, plus de serveurs ancetres a arreter.
