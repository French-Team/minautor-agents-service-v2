---
identite:
  type: outil
  appartient_a: matrice-data-outils
  commun: true
  liens: matrice/templates/carte-identite/README.md, matrice/data/manuel-outils.md
  version: 1.2.0
  palier: 1 (scan Python + JSON par ENTREE)
---

# Outil RECHERCHER -- Moteur de recherche unifie

## Porte unique

Cet outil est la porte unique pour toute recherche dans le projet.
Il combine **fichiers** (scan Python, aucune dependance externe) et **BDD**
(9 sources JSON/JSONL) en un seul appel.

> **Branchement (EO-112)** : la porte n'est pas un temoin isole -- la vigie-portes
> l'interroge a chaque tour (sonde de cecite, MO-055) et le **cockpit prive
> l'appelle pour de vrai** (route `/chercher`, `cockpit-matrice.py --route chercher
> --requete "<texte>"`) : c'est la qu'Optimus cherchait a la main.

## Verbes

| Verbe | Usage | Codes retour |
|---|---|---|
| `rechercher` | Recherche unifiee fichiers + BDD | 0=succes, 1=aucun resultat, 2=refus |
| `indexer` | Rebuild index (palier 2 futur) | 0=succes |

## Options rechercher

| Option | Defaut | Description |
|---|---|---|
| `--requete` | (requis) | Texte a rechercher : **MOTIF** (regex) si la requete porte un metacaractere, sinon **LANGAGE NATUREL** (mots vides retires, pluriel tolere, termes lies en ET). Un motif INVALIDE est **refuse** (code 2) en nommant le probleme et le remede (MO-424) |
| `--dans` | `tous` | Scope : `fichiers`, `bdd`, `tous` |
| `--tag` | (aucun) | **FILTRE** : ne garde que les entrees qui portent ce tag |
| `--mot-cle` | (aucun) | **FILTRE** : ne garde que les entrees qui contiennent ce texte |
| `--source` | (toutes) | **FILTRE** de source BDD : les sources JSON/JSONL (`lecons`, `modifications`, `historiques`, `historiques-optimus`, `vivier`, `activites`, `usages`, `classeur`, `conservation`) **plus les BDD SQLite DECOUVERTES** dans `matrice/data/` (aujourd'hui `frictions`, source **PRIVEE**) |
| `--periode` | (aucune) | **FILTRE** temporel : `7j`, `30j`, `3m`, `1a` |
| `--json` | (non) | Sortie machine JSON (ASCII pur) |
| `--prive` | (non) | Inclut les zones invisibles L-016 (`_operateur`, `tmp-optimus`, `suivi-optimus`) dans les FICHIERS, ouvre les sources BDD PRIVEES (`frictions`) **et** les BDD JSON declarees invisibles V-003 (`lecons`, `sessions`). Sans lui, le moteur reste etanche au cameleon -- le defaut ne s ouvre jamais tout seul |
| `--limite` | 50 | Nombre max de resultats |

## Contrat de la porte (corrige par MO-069, audit MO-057)

1. **Un filtre filtre.** `--tag`, `--mot-cle`, `--source` et `--periode` RETIRENT
   des resultats ; ils ne se contentent pas de modifier un score.
2. **Une option illisible est refusee** (code 2) : `--source` inconnue nomme les
   sources valides ; `--periode` hors forme `<nombre><j|m|a>` est refusee ;
   `--limite` non entiere est refusee. Aucune option n'est ignoree en silence.
3. **Un filtre hors de son domaine est refuse** : `--tag` / `--source` / `--mot-cle`
   avec `--dans fichiers` (ils ne filtreraient rien).
4. **Une limite est DITE.** Une coupe de lecture (`tronque`) et un ecart faute de
   date (`ecartes_sans_date`) sont rapportes dans les deux sorties : un resultat
   muet sur ses propres limites ment (lecon MO-055).
5. **Les fichiers binaires ne sont pas lus** (`.db`, `.pyc`, `.sqlite`... liste
   fermee `EXTENSIONS_BINAIRES`) : un binaire lu comme du texte produit des U+FFFD
   qui pourrissent les extraits et font crasher une sortie machine (EO-105).
6. **Sortie machine en ASCII pur** (`ensure_ascii`) : aucune console ne peut faire
   echouer la porte.
7. **Un fichier se trouve par son NOM** (EO-126) : chercher `zone_tmp` ne rendait
   RIEN alors que `matrice/data/commun/zone_tmp.py` existait -- le scan ne lisait
   que le contenu. Chaque hit porte desormais `sur` = `nom` ou `contenu` : un nom
   n'est pas une ligne, et un hit de nom porte `ligne` = 0 -- jamais une ligne
   inventee.
8. **Le perimetre du scan est DIT, et il ne s'ouvre que sur demande** (EO-126) :
   `--prive` est le SEUL moyen d'atteindre les zones L-016. Un moteur qui ne peut
   pas lire la maison de son propre operateur n'est pas prudent, il est AVEUGLE --
   et un aveugle qui dit "0 resultat" est indiscernable d'une absence (MO-055). Le
   defaut ne bouge pas d'un pouce ; quand `--prive` est actif, la sortie le
   DECLARE (`prive`) et NOMME les zones ouvertes (`zones_invisibles`).
9. **Une requete-motif INVALIDE est REFUSEE, jamais un crash** (MO-424) : une
   requete qui porte un metacaractere est lue comme un MOTIF (`[`, `(`, `*`, `?`,
   `+`...) et compilee telle quelle ; un motif invalide faisait remonter un
   `re.PatternError` AVEC TRACEBACK. Un crash n'enonce aucun remede -- la seule
   forme interdite. La requete est desormais compilee AVANT tout scan
   (`valider_requete`, domicile `commun.py`) : le refus (code 2) NOMME le probleme
   et le REMEDE (corriger le motif, ou retirer/echapper le metacaractere pour une
   recherche en langage naturel), le MEME en modes `fichiers`, `bdd` et `tous`.

10. **Un `0` sur un champ a VALEURS MULTIPLES NOMME le mode dedie** (MO-450) :
   `--champ cle=valeur` compare la valeur ENTIERE d'un champ. Pour une cle qui
   porte une LISTE -- ses valeurs separent par la virgule, la convention des
   `liens` -- viser UN element rendait un `0` nu, indiscernable d'une absence
   alors que la valeur EXISTE. Le `0` DIT desormais que la valeur figure et que
   `--champ` ne peut pas la trouver, et NOMME le mode dedie (`--lien <valeur>`
   pour le graphe des liens). Le predicat vit au domicile de la carte
   (`carte_identite.valeur_dans_champ_multiple`), jamais recopie ici.

## Granularite

- BDD `.json` : **un hit par ENTREE** (lecon, variable, theme, fichier modifie...),
  jamais une section entiere. La cle est lisible : `lecons/L-054`,
  `fichiers/<chemin>/modifications[3]`, `themes/TH-009`.
- BDD **SQLite** (adaptateur `sqlite3`, **aucun fichier migre**) : les bases de
  `matrice/data/` sont **DECOUVERTES** a chaque scan (stem = nom de source, tables
  lues sur `sqlite_master`) -- jamais declarees une a une. **Un hit par LIGNE**,
  cle = `<table>/<id>`. Une base decouverte est **PRIVEE par DEFAUT** (L-016) :
  servie sous `--prive` seulement, sauf stem declare PUBLIC (`SQLITE_PUBLIQUES`,
  vide aujourd'hui). Les INDEX sont ECARTES (`index-recherche.sqlite`). C'est
  l'exception assumee de `data-readme.md` (2026-09-26), qui vise `frictions.db`.
- BDD `.jsonl` : **un hit par ligne**. Les lignes qui ne peuvent pas correspondre
  sont ecartees avant `json.loads` (pre-filtre documente : motif ASCII sans
  anti-slash) -- c'est ce qui permet de lire les 67k lignes d'`usages` sans
  troncature muette.
- Fichiers : **un hit par NOM de fichier** (`sur` = `nom`, `ligne` = 0) et/ou
  **un hit par LIGNE** de contenu (`sur` = `contenu`) -- un meme fichier peut
  matcher des deux facons, et c'est le champ `sur` qui le dit (EO-126).

## Architecture

```
rechercher/
  constants.py     -- Chemins, sources BDD, limites, extensions binaires
  commun.py        -- Perimetre, scan Python, scan BDD par entree, score, periode
  rechercher/
    entry.py       -- Verbe rechercher (validation + sorties)
  indexer/
    entry.py       -- Verbe indexer (stub palier 2)
  main.py          -- Point d'entree (sac a dos + dispatch + garde d'encodage)
```

## Paliers

- **Palier 1 (actuel)** : scan Python + JSON par entree, ~0,3 s sur les 9 sources
- **Palier 2 (auto-evolution)** : index FTS5 SQLite, <50ms, rebuild atomique

## Garanties

- Perimetre `matrix/` seul (hors = 0 hit)
- Zones invisibles L-016 filtrees PAR DEFAUT ; `--prive` les inclut, et la sortie
  le DIT (EO-126) -- le defaut ne s'ouvre jamais tout seul
- Sortie deterministe (tri score desc, puis ordre d'insertion)
- BDD en lecture seule (jamais d'ecriture)
- Compatible win/linux (pathlib, aucune dependance externe)
