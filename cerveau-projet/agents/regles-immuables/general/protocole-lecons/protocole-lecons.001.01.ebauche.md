---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Protocole -- BDD des lecons (memoire longue + courte)

**Version** : 0.1.0
**Statut** : ebauche
**Agent** : Buffy (gouvernance)

---

## Principe

Les lecons des agents vivent dans une BDD SQLite UNIQUE et PARTAGEE
(`cerveau-projet/agents/lecons/lecons.db`) : c est la **memoire longue**.

Les `corrections.md` de chaque agent restent la **memoire courte** (fenetre
glissante des missions proches).

## Pourquoi

- Les `corrections.md` sont devenus illisibles (plusieurs milliers de lignes
  par agent) : ce sont des archives, plus une memoire de travail.
- Une BDD unique et partagee permet la **pollinisation croisee** : chaque
  agent peut consulter les lecons des autres (evolution entre eux).
- C est le **beta-test** de la future BDD du projet.

## Ecriture (enregistrer-lecon)

- Chaque agent n ecrit QUE SES propres lecons via `enregistrer-lecon`.
- **Anti-usurpation** : `--agent` (auteur) doit etre l agent actif de la
  session, sinon refus code 1.
- **ASCII strict** : tout caractere non-ASCII est refuse.
- **Anti-doublon** : meme agent + titre + corps deja present = signale,
  rien n est re-ecrit.

## Lecture (consulter-lecons)

- La consultation croisee se fait via `consulter-lecons`.
- **Verrou** : l usage passe par le verrou d habilitation.
- **Journalisation d activite** : chaque consultation est tracee dans le
  registre (`registre-usages-outils.jsonl`, mode `direct`) avec le filtre.

## Integrite

- La BDD n est touchee QUE par ces 2 outils (jamais `sqlite3` direct
  ailleurs).

## Garde-fou

- test-090-bdd-lecons-garde-fou : verifie la creation, l anti-usurpation,
  l ASCII, l anti-doublon, la consultation, la journalisation et l integrite
  (lecons.db referencee uniquement par les 2 outils).
