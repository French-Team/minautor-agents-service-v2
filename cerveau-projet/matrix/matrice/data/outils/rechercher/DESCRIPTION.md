---
identite:
  type: outil-rechercher
  appartient_a: matrice-data-outils
  version: 1.1.0
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
| `--requete` | (requis) | Texte a rechercher (regex supportee) |
| `--dans` | `tous` | Scope : `fichiers`, `bdd`, `tous` |
| `--tag` | (aucun) | **FILTRE** : ne garde que les entrees qui portent ce tag |
| `--mot-cle` | (aucun) | **FILTRE** : ne garde que les entrees qui contiennent ce texte |
| `--source` | (toutes) | **FILTRE** de source BDD : `lecons`, `modifications`, `historiques`, `historiques-optimus`, `vivier`, `activites`, `usages`, `classeur`, `conservation` |
| `--periode` | (aucune) | **FILTRE** temporel : `7j`, `30j`, `3m`, `1a` |
| `--json` | (non) | Sortie machine JSON (ASCII pur) |
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

## Granularite

- BDD `.json` : **un hit par ENTREE** (lecon, variable, theme, fichier modifie...),
  jamais une section entiere. La cle est lisible : `lecons/L-054`,
  `fichiers/<chemin>/modifications[3]`, `themes/TH-009`.
- BDD `.jsonl` : **un hit par ligne**. Les lignes qui ne peuvent pas correspondre
  sont ecartees avant `json.loads` (pre-filtre documente : motif ASCII sans
  anti-slash) -- c'est ce qui permet de lire les 67k lignes d'`usages` sans
  troncature muette.

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
- Zones invisibles L-016 filtrees
- Sortie deterministe (tri score desc, puis ordre d'insertion)
- BDD en lecture seule (jamais d'ecriture)
- Compatible win/linux (pathlib, aucune dependance externe)
