---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole de Fin de Mission -- Documentation Obligatoire avant Transmission

**Version** : 0.1.0
**Statut** : ebauche
**Categorie** : General
**Agent** : Cerberus
**Date** : 2026-08-14

Impose que CHAQUE maillon d'une chaine documente SON controle (lecon + verdict)
dans SA fiche de corrections AVANT de transmettre au maillon suivant ou de
reactiver Cerberus. Un bilan consolide ne peut jamais affirmer un verdict VALIDE
si les maillons n'ont pas documente leur propre controle.

---

## Objectif

Garantir qu'aucune mission ne se termine sans trace documentaire de son
controle : chaque agent qui execute une mission ecrit obligatoirement SA lecon
dans `corrections.md` (avec contexte, actions, verdict) PUIS transmet.

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
| 3 | Lecon non ecrite | Pas encore de lecon dans corrections.md pour cette mission |
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
| E2 | Ecrire SA lecon | Ajouter dans `cerveau-projet/agents/<nom>/corrections.md` (memoire COURTE, fenetre glissante) une entree `## [LECON] <date> -- <TITRE> (<Agent>)` contenant : **Contexte** (mission, origine), **Actions** (ce qui a ete fait), **Lecon** (ce qui est appris). Le verdict (VALIDE / A REVOIR / CONFORME / KO) doit apparaitre dans le titre OU le corps. LA MEME lecon part AUSSI dans la BDD (memoire LONGUE, partagee) via `enregistrer-lecon` (anti-usurpation : --agent == agent actif de la session) | editer-fichier + enregistrer-lecon |
| E3 | Verifier la lecon | Relire la lecon : date du jour, titre avec le nom de l'agent, verdict present, ASCII strict, LF pur | valider-conformite-ascii |
| E4 | Transmettre | Seulement apres E2+E3 : activer le maillon suivant (ou reactiver Cerberus si dernier maillon) avec le bilan | activer-agent-principal |
| E5 | Garde-fou | test-048 verifie que chaque mission recente d'AGENTS-historique a SA lecon + verdict dans corrections.md de l'agent | test-048 |

**REGLE : AUCUNE TRANSMISSION SANS LECON + VERDICT.** Si la lecon n'est pas
ecrite, l'agent n'est pas autorise a activer le maillon suivant ni a reactiver
Cerberus. Le bilan consolide du dernier maillon ne peut affirmer VALIDE que si
chaque maillon precedent a documente son controle.

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
  -> ecrit LECON "CREATION AGENT HERMES (Buffy)" avec verdict VALIDE dans buffy/corrections.md
  -> active Clio
Clio execute MISSION CLIO (README)
  -> ecrit LECON "README HERMES (Clio)" avec verdict VALIDE dans clio/corrections.md
  -> active Morpheus
...
Janus execute MISSION JANUS (controle croise final)
  -> ecrit LECON "CONTROLE HERMES (Janus)" avec verdict VALIDE dans janus/corrections.md
  -> reactiver Cerberus avec le bilan consolide
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
| Recopier les resultats d'un autre agent sans controle | Faux verdict VALIDE | Lecon doit decrire SON controle, pas celui des autres |
| Verdict absent de la lecon | Impossible de savoir si le travail a reussi | E2 : verdict obligatoire |
| Lecon ecrite mais pas relue (accents, CRLF) | Normes violees | E3 : valider-conformite-ascii |

---

## Liens

- [index-regles-general.md](../index-regles-general.md) -- referencement
- [regles-veracite.md](../regles-veracite.md) -- ne jamais mentir, supposer, inventer
- [test-048-fin-mission-documentation](../../../tools/tester/tests/test-048-fin-mission-documentation/test-048-fin-mission-documentation.py) -- garde-fou
