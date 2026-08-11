# Rapport d'audit Themis -- Pattern 14 (conformite fiche/parcours) sur les 11 fiches

**Date** : 2026-08-11
**Auditrice** : Themis (evaluatrice croisee)
**Objet** : conformite globale du Pattern 14 sur les 11 fiches agents -- volets
PRINCIPAL (REGLE ABSOLUE PARCOURS vX) et SECONDAIRE (bloc FINS REELLES de la
carte + lien Parcours vX), apres la correction Buffy du 2026-08-11 (8 blocs
FINS REELLES + 6 liens Parcours vX).

---

## Verdict

**A REVOIR** -- 1 ecart reel (3 fiches sans bloc FINS REELLES), le reste conforme.

| Point | Verification | Resultat |
|---|---|---|
| P1 | REGLE ABSOLUE PARCOURS (vX) == version reelle du parcours (11 fiches) | CONFORME |
| P2 | Bloc FINS REELLES : version reelle + liste complete des fins (8 fiches avec bloc) | CONFORME |
| P2b | Bloc FINS REELLES PRESENT sur CHAQUE fiche (protocole-sante E5b) | **ECART (3)** |
| P3 | Lien Parcours (vX) == version reelle | CONFORME |
| P4 | Aucune mention de version de parcours stale ailleurs | CONFORME |
| P5 | Normes ASCII + LF sur les 11 fiches | CONFORME (0/0) |
| P6 | valider-cartes-decision --tous + test-018 + test-021 | CONFORME (11/11 + 13/13 + 9/9) |

---

## Detail

### P1 -- REGLE ABSOLUE PARCOURS (vX) : CONFORME (11/11)

Chaque fiche porte la REGLE ABSOLUE avec la version reelle de SON parcours :

| Agent | Parcours reel | Fiche (REGLE ABSOLUE) |
|---|---|---|
| athena | v0.2.4 | v0.2.4 |
| atlas | v0.3.4 | v0.3.4 |
| buffy | v0.3.7 | v0.3.7 |
| cerberus | v0.3.3 | v0.3.3 |
| clio | v0.4.4 | v0.4.4 |
| janus | v0.3.7 | v0.3.7 |
| minerve | v0.2.4 | v0.2.4 |
| morpheus | v0.3.3 | v0.3.3 |
| promethee | v0.2.4 | v0.2.4 |
| themis | v0.3.6 | v0.3.6 |
| vulcain | v0.3.6 | v0.3.6 |

### P2 -- Bloc FINS REELLES (version + fins completes) : CONFORME sur les 8 fiches qui l'ont

Les blocs FINS REELLES (mis a jour par Buffy le 2026-08-11) sont conformes :
version reelle + liste complete des fins du parcours (type fin), y compris
les fins cXe du Pattern 17 et la ligne trio cT6..cT10 de janus.

### P2b -- ECART : le TRIO (athena, minerve, promethee) n'a AUCUN bloc FINS REELLES

Le protocole-sante-fichiers-agents **E5b** (lecon du re-audit 2026-08-10) exige
que la fiche cite les fins REELLES de la carte via leurs identifiants cX
(une mention textuelle sans identifiant reel est INSUFFISANTE). Les 3 fiches
du trio ne citent AUCUNE fin reelle :

| Agent | Fins reelles (parcours v0.2.4) | Citees dans la fiche |
|---|---|---|
| athena | c9e, c10, c20, c20d, c21, c23 | AUCUNE |
| minerve | c9e, c10, c20, c20d, c21, c23 | AUCUNE |
| promethee | c9e, c10, c20, c20d, c21, c23 | AUCUNE |

Le trio a ete migre au format action (v0.2.4) avec une boucle de correction
vers Janus (case c9f CORRIGER selon le rapport), mais le bloc FINS REELLES
n'a jamais ete ajoute a leurs fiches (contrairement aux 8 autres agents).

### P3 -- Lien Parcours (vX) : CONFORME (11/11)

Les 6 liens qui etaient obsoletes (athena, cerberus, minerve, morpheus,
promethee, vulcain) sont corriges. Les 5 autres fiches (atlas, buffy, clio,
janus, themis) n'ont pas de version dans le lien (aucun ecart).

### P4 -- Mentions stale : CONFORME

Aucune version de parcours obsoletes ailleurs dans les fiches.

### P5 -- Normes : CONFORME

11/11 fiches en ASCII strict + LF pur (0/0).

### P6 -- Non-regression : CONFORME

- valider-cartes-decision --tous : 11/11 CONFORME (garde-fou P10 fiche/parcours)
- test-018-fins-reactivation : 13/13 OK
- test-021-ligne-trio : 9/9 OK

---

## Recommandation

**Buffy** (responsable des fiches agents) doit ajouter le bloc FINS REELLES
DE MA CARTE sur les 3 fiches du trio (athena, minerve, promethee), au format
des 8 autres fiches, avec la version v0.2.4 et les 6 fins reelles :

```
> **FINS REELLES DE MA CARTE v0.2.4 (E5b - croisement fiche/parcours)** :
> - `c9e` FIN - Reprise du parcours apres retour de l'agent habilite
> - `c10` FIN - Activer Janus (maillon de la chaine trio -> Janus controle)
> - `c20` Signaler le besoin (fin - relais)
> - `c20d` FIN - Outil temporaire
> - `c21` FIN - Delegation (j'active l'agent habilite)
> - `c23` FIN - Retour de Themis avec son rapport
```

---

## Lecons (Themis)

1. La correction Buffy du Pattern 14 (8 blocs + 6 liens) est efficace : P1, P3,
   P4, P5, P6 tous conformes.
2. Le bloc FINS REELLES etait absent du trio depuis la migration v0.2.4 -- il
   faut un GARDE-FOU : le protocole-sante E5b devrait etre renforce pour exiger
   le bloc sur TOUTES les fiches (pas seulement celles qui en ont deja un).
3. Les IDs cT* (ligne trio) : la regex de scan doit etre `[a-zA-Z]*\d+[a-z]*`
   (une lettre MAJUSCULE au milieu) pour les capturer -- les regex `[a-z]?`
   creent des faux negatifs.
