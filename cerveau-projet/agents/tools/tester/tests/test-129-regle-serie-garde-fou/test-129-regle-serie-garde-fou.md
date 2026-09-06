---
identite:
  type: test
  appartient_a: commun
  commun: true
---
# test-129-regle-serie-garde-fou

**Version :** 0.1.0
**Statut :** valide
**Serie :** e (garde-fous specifiques)
**Profil :** outils

## Objet

Garde-fou du contenu de la regle **TRAVAIL EN SERIE OBLIGATOIRE**
(decision utilisateur 2026-09-05) : en mode single-llm, le travail en
parallele n existe PAS -- un seul agent est incarne a la fois, jamais 2
missions relayees simultanement.

La regle est ancre dans 3 fichiers (double/triple ancrage) :
- `AGENTS.md` (regle 3, zone MARBRE constitution, ajoutee par Gardien,
  mission ab5d3ca4 -- validation utilisateur)
- `demarrer.md` ORDRE 5 (MODE SINGLE-LLM, ajoutee par Buffy,
  mission 666bec53)
- `COMMENT-DEMARRER.md` (reformule par Buffy, mission 666bec53 :
  l'ancienne instruction 'demarrer un second llm en parallel' a ete
  supprimee)

## Points verifies (12)

| # | Verification |
|---|---|
| 1-3 | Les 3 fichiers sont presents |
| 4 | COMMENT-DEMARRER.md ne contient PLUS 'second llm en parallel' |
| 5 | COMMENT-DEMARRER.md contient 'TRAVAIL EN SERIE' |
| 6 | demarrer.md contient 'TRAVAIL EN SERIE OBLIGATOIRE' |
| 7 | demarrer.md contient 'JAMAIS 2 missions relayees simultanement' |
| 8 | AGENTS.md contient la regle 3 'TRAVAIL EN SERIE OBLIGATOIRE' |
| 9 | Coherence croisee 3/3 : les 3 marqueurs cles sont dans les 3 fichiers (comparaison insensible a la casse) |
| 10-11 | Normes ASCII 0/0 + LF pur 0 CRLF sur COMMENT-DEMARRER.md et demarrer.md |
| 12 | Preuve negative : une fixture sans la regle serie est DETECTEE |

## Pieges couverts (lecons)

1. **Marqueurs coupes par la mise en page markdown** : 'JAMAIS 2 missions
   relayees simultanement' est coupe par un retour a la ligne dans
   demarrer.md -> le test normalise le texte (espaces/retours ignores)
   avant la recherche.
2. **Casse differente selon le fichier** : COMMENT-DEMARRER.md ecrit
   'un seul' en minuscules, demarrer.md/AGENTS.md 'un SEUL' en majuscules
   -> la coherence croisee compare en minuscules (l'essence de la regle
   est identique).
3. **La raison d'activation dans AGENTS.md (bloc Session) cite
   l'ancienne formulation** : c'est une METADONNEE d'historique, pas une
   instruction -- le test cible COMMENT-DEMARRER.md pour l'absence de
   l'ancien texte, jamais AGENTS.md.

## Execution

```bash
python3 cerveau-projet/agents/tools/tester/tests/test-129-regle-serie-garde-fou/test-129-regle-serie-garde-fou.py
```

Resultat attendu : `RESULTAT : 12 OK / 0 KO (sur 12 points)`

## Historique

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-09-05 | Creation (mission 81f0f16d Morpheus, inter-round suite 666bec53 Buffy) |
