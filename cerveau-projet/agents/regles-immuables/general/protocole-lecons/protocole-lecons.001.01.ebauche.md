---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---
# Protocole -- BDD des lecons (2 BDD separees v1 / v2)

**Version** : 0.3.0
**Statut** : ebauche
**Agent** : Buffy (gouvernance)

> **SCISSION 2-BDD (decision utilisateur 2026-09-05)** : correction du plan
> 0.2.0. La migration v1->v2 ne fusionne PAS les memoires : les deux equipes
> sont DISTINCTES et gardent chacune LEUR perimetre et LEUR zone de memoire
> collective.
> - Agents v1 (cerveau-projet) : BDD v1
>   `cerveau-projet/agents/lecons/lecons.db` (outils v1 restaures
>   `enregistrer-lecon` / `consulter-lecons`).
> - Agents v2 (freelance) : BDD v2
>   `cerveau-projet/freelance/tools-commun/bdd-lecons/lecons.db`
>   (`bdd-lecons entry.py enregistrer`).
> Les 279 lecons v1 qui avaient ete copiees dans bdd-lecons v2 ont ete
> RETIREES (backup `lecons.db.bak-scission-2bdd-2026-09-05`) ; les 16
> orphelines et les lecons du round de migration ont ete re-integres dans la
> BDD v1. bdd-lecons v2 ne contient plus QUE les lecons freelance (6).

---

## Principe

Chaque equipe a SA BDD SQLite : c est SA **memoire longue**.

| Equipe | BDD | Outils |
|---|---|---|
| v1 (cerveau-projet) | `cerveau-projet/agents/lecons/lecons.db` (279 lecons) | `enregistrer-lecon` / `consulter-lecons` (v1) |
| v2 (freelance) | `cerveau-projet/freelance/tools-commun/bdd-lecons/lecons.db` (6 lecons) | `bdd-lecons entry.py` (v2) |

Les `corrections.md` v1 de chaque agent sont GELEES (bandeau 2026-09-04) :
archives conservees pour relecture, AUCUN nouveau [LECON].

## Pourquoi

- Deux equipes distinctes = deux perimetres, deux zones de memoire
  collective. Aucune fusion : une lecon v1 ne va JAMAIS dans bdd-lecons v2,
  et inversement (violation de perimetre).
- La **pollinisation croisee** reste possible DANS chaque equipe : un agent
  v1 consulte les lecons v1 des autres agents v1 (consulter-lecons) ; un
  agent v2 consulte les lecons v2 des autres agents v2 (bdd-lecons lister).

## Ecriture / Lecture

- **Agents v1** : `python3 cerveau-projet/agents/tools/enregistrer/enregistrer-lecon/enregistrer-lecon.py
  --agent <nom> --titre <titre> --lecon <texte> --mission <mission> --verdict <verdict>`
  (et `consulter-lecons` pour la lecture). BDD cible : lecons.db v1.
- **Agents v2** : `python3 cerveau-projet/freelance/tools-commun/bdd-lecons/
  entry.py enregistrer --agent <nom> --source <mission>`.
- **E2 (protocole-fin-mission)** : a la fin de mission, chaque agent
  enregistre SA lecon dans SA BDD - plus AUCUNE ecriture dans les
  corrections.md v1 gelees.

## Garde-fou

- test-048 (garde-fou protocole-fin-mission, etape D.1 adaptee) : verifie la
  presence de la lecon dans SA BDD (agents v1 -> lecons.db v1, agents v2 ->
  bdd-lecons v2) - plus corrections.md gelees pour les missions pre-gel.
- test-090 (garde-fou bdd-lecons v2) : verifie l outil v2 (enregistrer,
  lister, compter) et l absence de lecons v1 dedans.
- test-125 (migration) : conserve pour preuve de la migration historique,
  mais la cible du modele courant est la scission 2-bdd (test adapte en D.4).