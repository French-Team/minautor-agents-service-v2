# detecter-usage-scripts-temporaires

**Categorie** : Detecter
**Version** : 0.1.1
**Statut** : ebauche
**Agent** : Vulcain
**Date** : 2026-08-11

Mesure l'usage des **scripts temporaires** (`.zz-*.py` / `.tmp-*.py`) par les
agents : scripts presents a la racine, scripts qui ont existe (git log),
scripts mentionnes dans les lecons/corrections et rapports. Croise ensuite
avec le **registre d'usage** : un script detecte SANS declaration
(`mode: script-temporaire`) est un contournement a signaler.

---

## Objectif

Repondre a la question de l'utilisateur : "ou et pourquoi nos agents
preferent les scripts temporaires a nos outils ?" Le registre JSONL seul ne
peut pas capturer les scripts temporaires (ils ne passent pas par le
generateur). Cet outil ferme la boucle : il scanne les sources de traces
(fichiers, git, lecons, rapports) et mesure l'ecart avec les declarations.

## Sources scannees

| # | Source | Ce qui est detecte |
|---|---|---|
| 1 | Racine du projet | Fichiers `.zz-*` / `.tmp-*` (.py/.sh) presents |
| 2 | Git (`git log --diff-filter=A`) | Scripts .py/.sh crees un jour (historique) |
| 3 | Corrections/lecons | Mentions `\.zz-` / `\.tmp-` dans les `.md` |
| 4 | Registre d'usage | Declarations `mode: script-temporaire` (registre courant, un seul fichier) |

> **Filtre v0.1.1** : un script temporaire est un FICHIER `.py`/`.sh` dont
> le basename commence par `.zz-` ou `.tmp-`. Les dossiers de tests
> (`.tmp-eol-test/`, `.tmp-gc-test/`) et les fichiers `.md`/`.json` ne sont
> PAS des scripts : ils ne sont plus comptes (faux positifs elimines).

> **Memoire** : le detecteur croise avec le registre courant
> `registre-usages-outils.jsonl` (un seul fichier depuis la decision
> utilisateur 2026-08-14 : plus d archive historique, entrees
> script-temporaire fusionnees dans le registre actif).

## Utilisation

```bash
# Detection complete
python3 detecter-usage-scripts-temporaires.py

# Rapport markdown
python3 detecter-usage-scripts-temporaires.py --rapport rapport-scripts-temp.md

# Detail par source
python3 detecter-usage-scripts-temporaires.py --verbose
```

## Retour

- `0` : aucun ecart (tous les scripts detectes sont declares au registre)
- `1` : au moins un script detecte sans declaration (contournement)

## Historique

| Version | Date | Changement |
|---|---|---|
| 0.1.1 | 2026-08-12 | Round 8 : filtre .py/.sh (faux positifs dossiers de tests elimines) + croisement avec l'historique archive |
| 0.1.0 | 2026-08-11 | Creation : scan racine/git/lecons + croisement registre |

## Le flux voulu (protocole a venir)

1. Un agent a besoin d'une operation ponctuelle : il passe par
   `generateurs-outil-temporaire` (jamais un script jetable a la racine)
2. Tout script temporaire cree est **declare** au registre :
   `enregistrer-usage-outil --mode script-temporaire`
3. Janus / Themis lancent `detecter-usage-scripts-temporaires` a chaque
   controle : l'ecart = scripts non declares = anomalie
