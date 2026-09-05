# Memoire des corrections -- transition v1 -> v2 (2026-09-04, scission 2-bdd 2026-09-05)

> DOCUMENT DE TRANSITION (plus une doctrine active). Decisions utilisateur :
> 1) 2026-09-04 : "on passe de v1 a v2, on oublie ce que faisait la v1 pour
>    passer en v2" (portee : corrections/memoire) - plan 0.2.0.
> 2) 2026-09-05 : **SCISSION 2-BDD** - correction du plan 0.2.0 : les deux
>    equipes (v1 cerveau-projet, v2 freelance) sont DISTINCTES et gardent
>    chacune LEUR perimetre et LEUR zone de memoire collective. Pas de fusion.

## Etat actuel (depuis la scission 2026-09-05)

- **BDD v1** (`cerveau-projet/agents/lecons/lecons.db`, 279 lecons) : memoire
  collective des agents v1 (cerveau-projet). Outils v1 RESTAURES le
  2026-09-05 : `enregistrer-lecon` / `consulter-lecons` (catalogue 0.2.18).
- **BDD v2** (`cerveau-projet/freelance/tools-commun/bdd-lecons/lecons.db`,
  6 lecons) : memoire collective des agents FREELANCE uniquement.
  Commande : `bdd-lecons entry.py enregistrer|lister|chercher|compter`.
- **corrections.md v1** (cerveau-projet/agents/*/corrections.md) : GELES le
  2026-09-04 (bandeau en tete). Historique conserve pour relecture - AUCUN
  [LECON] supplementaire.
- **corrections.db + corrections-db.py** : SUPPRIMES le 2026-09-04 (etape
  B.5) - .bak verifies conserves (`corrections.db.bak-2026-09-04`,
  `socrate/corrections.db.bak-2026-09-04`, md5 identiques).

## Ce qui s est passe (chronologie)

1. **2026-09-04 (plan 0.2.0)** : migration v1->v2 lancee. Les 256 lecons v1 +
   16 orphelines + 7 lecons du round ont ete copiees dans bdd-lecons v2 (279
   au total). Les outils v1 ont ete retires du catalogue et archives (B.4).
2. **2026-09-05 (scission 2-bdd)** : l utilisateur a clarifie que les deux
   equipes gardent LEUR memoire. Les 279 lecons v1 ont ete RETIREES de
   bdd-lecons v2 (backup `lecons.db.bak-scission-2bdd-2026-09-05`) et
   REINTEGREES dans lecons.db v1 (qui n avait jamais perdu ses 256, + 23
   reintegrees = 279). Les outils v1 ont ete RESTAURES et recatalogues.

## Regles actuelles

- Chaque equipe ecrit UNIQUEMENT dans SA BDD (regle 2-bdd, violation de
  perimetre sinon).
- Protocole E2 (protocole-fin-mission) : agents v1 -> `enregistrer-lecon`
  (BDD v1) ; agents v2 -> `bdd-lecons entry.py enregistrer` (BDD v2).
- `bdd-lecons migrer-v1` est OBSOLETE depuis la scission : les lecons v1
  vivent dans la BDD v1, jamais dans bdd-lecons v2.

## Rappel du modele v1 (historique, avant le 2026-09-04)

Avant la decision v1->v2, l infra v1 reposait sur :
- `corrections.md` : memoire courte (regles + ~10 dernieres lecons).
- `cerveau-projet/agents/lecons/lecons.db` : memoire longue officielle, geree
  par `enregistrer-lecon` et `consulter-lecons` (archives le 2026-09-04,
  restaures le 2026-09-05).
- `cerveau-projet/agents/corrections.db` : index/import de compatibilite des
  corrections Markdown de tous les agents v1 (outil `corrections-db.py`).

## References

- Plan de migration : `cerveau-projet/docs-dev-cerveau-projet/plan-migration-corrections-v1-v2-2026-09-04.md`
- Outil v2 : `cerveau-projet/freelance/tools-commun/bdd-lecons/` (doc : bdd-lecons.md)
- Protocole de fin de mission : `cerveau-projet/agents/regles-immuables/general/protocole-fin-mission/`
- Protocole lecons : `cerveau-projet/agents/regles-immuables/general/protocole-lecons/`
- Archive B.4 : `cerveau-projet/agents/archive-outils-v1-lecons-2026-09-04/`