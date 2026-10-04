---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole de Fin de Mission -- Documentation Obligatoire avant Transmission

**Version** : 0.4.0
**Statut** : ebauche
**Categorie** : General
**Agent** : Cerberus
**Date** : 2026-09-05

Impose que CHAQUE maillon d'une chaine documente SON controle (lecon + verdict)
dans SA BDD des lecons AVANT de transmettre au maillon suivant ou de reactiver
Cerberus. Un bilan consolide ne peut jamais affirmer un verdict VALIDE si les
maillons n'ont pas documente leur propre controle.

DEUX TEAMs, DEUX BDD (decision utilisateur 2026-09-05, scission 2-bdd) :
- Agents v1 (cerveau-projet) : BDD v1 `cerveau-projet/agents/lecons/lecons.db`
  via les outils v1 `enregistrer-lecon` / `consulter-lecons` (restaures).
- Agents v2 (freelance) : BDD v2 `cerveau-projet/freelance/tools-commun/bdd-lecons/lecons.db`
  via la commande `bdd-lecons entry.py enregistrer`.
Chaque equipe a SON perimetre et SA zone de memoire collective : aucune lecon
v1 ne doit atterrir dans bdd-lecons v2, et inversement.

---

## Objectif

Garantir qu'aucune mission ne se termine sans trace documentaire de son
controle : chaque agent qui execute une mission enregistre obligatoirement SA
lecon dans SA BDD (avec contexte, actions, verdict) PUIS transmet. Les
corrections.md v1 sont GELEES depuis le 2026-09-04 (historique conserve pour
relecture, AUCUNE nouvelle lecon dedans).

**Pourquoi ce protocole ?**
- Le 2026-08-14, la verification de la chaine Hermes a revele que le bilan
  consolide de Janus affirmait "VOLET 1 Hermes VALIDE" alors que NI Themis NI
  Janus n'avaient documente le moindre controle de la creation d'Hermes
  (aucune lecon, aucun rapport mentionnant hermes dans leurs dossiers).
- Le bilan reprenait les resultats de Morpheus sans controle croise reel :
  c'est la derive "l'agent se contente des resultats des autres".
- Anti-recurrence : la documentation du controle devient OBLIGATOIRE et
  verifiee par un garde-fou (test-048) avant toute transmission.

---

## Prerequis

| # | Condition | Detail |
|---|---|---|
| 1 | Mission attribuee | Un agent a recu une mission (activation via activer-agent-principal) |
| 2 | Travail termine | L'agent a execute les actions de sa mission |
| 3 | Lecon non enregistree | Pas encore de lecon dans SA BDD (v1 ou v2 selon l equipe) pour cette mission |
| 4 | Verdict connu | L'agent connait le resultat de son travail (VALIDE / A REVOIR / CONFORME / KO) |

---

## Etapes

```
TRAVAIL -> LECON (contexte + actions + verdict) -> TRANSMISSION
   1              2                                     3
```

| Etape | Action | Detail | Outils |
|---|---|---|---|
| E1 | Terminer le travail | Executer toutes les actions de la mission, verifier les resultats | outils de la carte |
| E2 | Ecrire SA lecon | **Agents v1** : `enregistrer-lecon` (BDD v1 `cerveau-projet/agents/lecons/lecons.db` - LEUR memoire collective). **Agents v2** : `bdd-lecons entry.py enregistrer` (BDD v2 freelance). Chaque equipe ecrit UNIQUEMENT dans SA BDD (scission 2-bdd, decision utilisateur 2026-09-05). Entree `## [LECON] <date> -- <TITRE> (<Agent>)` avec **Contexte** (mission, origine), **Actions** (ce qui a ete fait), **Lecon** (ce qui est appris). Le verdict (VALIDE / A REVOIR / CONFORME / KO) doit apparaitre dans le titre OU le corps. **Les corrections.md v1 sont GELEES le 2026-09-04 (memoire historique conservee pour relecture) : AUCUN [LECON] supplementaire dedans.** | agents v1 : enregistrer-lecon ; agents v2 : bdd-lecons (enregistrer) |
| E3 | Verifier la lecon | Relire la lecon : date du jour, titre avec le nom de l'agent, verdict present, ASCII strict, LF pur | valider-conformite-ascii |
| E4 | Transmettre | Seulement apres E2+E3 : MA FIN suit MA carte (modele aero R1/R3) - `oracle.py reactiver-fin <agent> "<bilan>" --cible oracle` ; le pilote decide du suivant | oracle.py reactiver-fin |
| E5 | Garde-fou | test-048 verifie que chaque mission recente d'AGENTS-historique a SA lecon + verdict dans SA BDD (agents v1 -> lecons.db v1, agents v2 -> bdd-lecons v2) - les missions pre-migration (avant 2026-09-04) sont verifiees dans l historique gele corrections.md | test-048 |

**REGLE : AUCUNE TRANSMISSION SANS LECON + VERDICT.** Si la lecon n'est pas
ecrite, l'agent n'est pas autorise a rendre sa fin (reactiver-fin --cible
oracle). Le bilan consolide ramene par le pilote a Cerberus en fin de round ne
peut affirmer VALIDE que si chaque maillon precedent a documente son controle.

---

## RVAV

| Etape RVAV | Action pour ce protocole |
|---|---|
| Rechercher | Verifier l'etat des lecons des agents avant une mission (derniere lecon = mission precedente ?) |
| Verifier | Toute mission recente dans AGENTS-historique a-t-elle sa lecon + verdict ? |
| Analyser | Si une mission n'a pas de lecon : la mission etait-elle reelle ? le travail a-t-il ete verifie ? |
| Valider | Le protocole est respecte quand chaque mission a sa lecon + verdict avant transmission |
| Purifier | Corriger les missions sans lecon (ajouter la lecon manquante) avant de continuer |

---

## Exemples

### Exemple 1 : chaine conforme

```
Buffy execute MISSION BUFFY (creation Hermes)
  -> enregistre LECON "CREATION AGENT HERMES (Buffy)" avec verdict VALIDE dans lecons.db v1 (enregistrer-lecon)
  -> MA FIN vers ORACLE (reactiver-fin buffy --cible oracle) ; le pilote largue Clio
Clio execute MISSION CLIO (README)
  -> enregistre LECON "README HERMES (Clio)" avec verdict VALIDE dans lecons.db v1 (enregistrer-lecon)
  -> MA FIN vers ORACLE (reactiver-fin clio --cible oracle) ; le pilote largue Morpheus
...
Janus execute MISSION JANUS (controle croise final)
  -> enregistre LECON "CONTROLE HERMES (Janus)" avec verdict VALIDE dans lecons.db v1 (enregistrer-lecon)
  -> MA FIN vers ORACLE (reactiver-fin janus --cible oracle) ; le pilote ramene
     le bilan consolide a Cerberus en fin de round
```

### Exemple 2 : chaine NON conforme (derive a eviter)

```
Themis est activee pour MISSION THEMIS (audit Hermes)
  -> ne documente AUCUNE lecon sur Hermes
  -> transmet a Janus
Janus reprend les resultats de Morpheus sans controle reel
  -> affirme "Hermes VALIDE" dans son bilan SANS lecon de controle
=> test-048 fait KO : mission themis sans lecon, mission janus sans verdict
```

---

## Pieges courants

| Piege | Consequence | Protection |
|---|---|---|
| Transmettre sans ecrire la lecon | Le bilan affirme sans preuve | E2 obligatoire + test-048 |
| Ecrire sa lecon dans la BDD de l'autre equipe | Fusion des memoires (violation du perimetre 2-bdd) | E2 : chaque equipe ecrit UNIQUEMENT dans SA BDD |
| Recopier les resultats d'un autre agent sans controle | Faux verdict VALIDE | Lecon doit decrire SON controle, pas celui des autres |
| Verdict absent de la lecon | Impossible de savoir si le travail a reussi | E2 : verdict obligatoire |
| Lecon ecrite mais pas relue (accents, CRLF) | Normes violees | E3 : valider-conformite-ascii |

---

## Liens

- [index-regles-general.md](../index-regles-general.md) -- referencement
- [regles-veracite.md](../regles-veracite.md) -- ne jamais mentir, supposer, inventer
- [test-048-fin-mission-documentation](../../../tools/tester/tests/test-048-fin-mission-documentation/test-048-fin-mission-documentation.py) -- garde-fou



---

## Le flux ROUND / INTER-ROUND / REPRISE (modele aero, decision utilisateur 2026-08-30)

### Vocabulaire

| Terme | Definition |
|---|---|
| **ROUND** | La mission principale : CERBERUS reeoit la demande USER -> ORACLE (l aeroport) configure le PILOTE -> le pilote LARGUE les agents un a un et les RECUPERE -> retour a ORACLE -> cerberus cloture. Chaque agent suit SON arbre ; le pilote suit SON arbre de mission. UN ROUND LANCE DOIT ETRE FINI. |
| **INTER-ROUND** | Mission secondaire de REPARATION declenchee quand un agent detecte une ERREUR HORS-PERIMETRE pendant son round. |
| **REPRISE DE ROUND** | A la fin de l'inter-round, le PILOTE renvoie l'AGENT QUI AVAIT LANCE l'inter-round, qui reprend son round principal exactement ou il l'avait laisse. |

### Le flux d'erreur hors-perimetre

`
ROUND en cours (AGENT_N detecte une erreur hors-perimetre)
   -> AGENT_N SIGNALE le besoin a ORACLE : oracle.py mission-ajouter --agent <habilite> "<rapport>"
   -> MA FIN vers ORACLE : oracle.py reactiver-fin AGENT_N "<bilan>" --cible oracle
      [INTER-ROUND : reparation exclusive de l'habilite]
   -> le PILOTE LARGUE l'agent habilite (qu il pilote via SON arbre)
   -> fin de l'inter-round : l'habilite revient vers ORACLE ; le pilote RENVOIE AGENT_N
   -> AGENT_N REPREND son round principal
`

> **L agent N ACTIVe JAMAIS l'agent habilite (R3)** : il le SIGNALE a ORACLE
> et le PILOTE decide du largage. Seul cerberus est 'avant' oracle ; tous
> les autres agents reviennent vers ORACLE (l aeroport).

### Regles immuables

| # | Regle |
|---|---|
| R1 | Une erreur detectee n'est JAMAIS laissee 'seulement detectee' : elle est TOUJOURS suivie d'une reparation par l'agent habilite EXCLUSIVEMENT (lui seul sait precisement quoi faire). |
| R2 | Un agent qui detecte une erreur hors-perimetre n'interrompt PAS le round et ne reactive PAS Cerberus : il SIGNALE le besoin a ORACLE (`mission-ajouter --agent <habilite>`) puis sa fin va vers ORACLE (`reactiver-fin --cible oracle`). Le pilote largue l'habilite. |
| R3 | L agent n'ACTIVE JAMAIS un autre agent (modele aero) : toute activation directe dans ses themes est un vestige v1 (audit C4), a remplacer par le signalement a ORACLE. C est le PILOTE qui decide du largage. |
| R4 | CASCADE : si l'erreur concerne l'agent habilite lui-meme, OU si sa reparation revele une autre erreur hors-perimetre, l'inter-round s'enchaine en cascade (le pilote largue les habilites en sequence) ; sinon la reparation est DECOMPOSEE et les agents habilites s'enchainent DANS l'inter-round. |
| R5 | Themis et Janus restent HORS des inter-rounds courts. Janus garde uniquement la non-regression finale du round. |
| R6 | Tracabilite R/IR : les entrees d'AGENTS-historique (et l'encart Activites recentes) portent une colonne d'indicateur : R pour round, IR pour inter-round. |

### Ce qui change vs l'ancien garde-fou (OBSOLETE)

L'ancienne fin 'reactiver Cerberus' et l'activation directe de l'habilite sont
SUPPRIMEES : elles cassaient le round en le faisant retomber sur Cerberus au
milieu. La fin d'un maillon suit desormais le modele aero :
- round normal -> MA FIN vers ORACLE (reactiver-fin --cible oracle), le pilote decide du suivant ;
- erreur hors-perimetre -> SIGNALER a ORACLE (mission-ajouter, R2), puis REPRISE DE ROUND via le pilote.

---

## Fin vers ORACLE via reactiver-fin --cible (modele aero, 2026-08-30)

### Contexte

Le modele aero (spec modele-round-avion-parachutiste) : ORACLE est
l aeroport qui configure DESTINATION + liste d agents et fait larguer les
parachutistes UN A UN par le pilote. Toute fin d agent va vers ORACLE --
jamais vers cerberus au milieu, jamais vers un autre agent.

### Le mecanisme : cible oracle dans la fin

Chaque fin d agent de `fins.json` porte `cible: oracle` et la commande :

```
python3 cerveau-projet/agents/tools/oracle/oracle.py reactiver-fin <agent> "<bilan>" --cible oracle
```

Elle :
1. pose le FIN sur l agent qui sort (colonne Debut/Fin) ;
2. reactiver ORACLE (l aeroport) -- jamais le precedent/cerberus directement ;
3. le PILOTE d oracle decide de la suite : larguer le maillon suivant ou retour a Cerberus en fin de round (bilan consolide).

### Regle fin modele aero

| # | Regle |
|---|---|
| R7 | La fin d un agent porte TOUJOURS `cible: oracle` : `reactiver-fin <agent> <bilan> --cible oracle`. L agent ne connait PAS le suivant (R3) - le pilote decide. Seul cerberus (qui est AVANT oracle) n'applique pas cette regle. |
| R8 | Un agent active en INTER-ROUND signale le besoin a ORACLE puis revient vers ORACLE ; le pilote renvoie SON APPELANT (reprise de round). C est une REGLE DEMARCATION : chaque arbre a une branche/theme INTER-ROUND oriente vers ORACLE. |
| R9 | Les arbres migres (argus, janus, buffy, morpheus, vulcain, trio, ...) ont leurs fins vers oracle (audit F4/F5 + reconstruction) et leurs themes sans activation directe (audit C4). |

### Conformite attendue des arbres

Pour que le round / inter-round fonctionne (modele aero), chaque agent doit posseder :
- une branche `INTER-ROUND` dans la racine de son arbre -> theme-inter-round ;
- ses fins de mission en `reactiver-fin <agent> "<bilan>" --cible oracle` (retour vers ORACLE) ;
- pour les agents qui font tester (ex: un dev comme Buffy), une etape de
test qui SIGNALE le besoin a ORACLE (`mission-ajouter --agent morpheus`) en
inter-round plutot que d activer directement Morpheus ou de tester eux-memes.

