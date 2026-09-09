# INDICES -- pilote/entonnoir/ (echelons 0-4 de la file de missions)

> Tete de lecture : lire CECI avant les fichiers. L'indice pointe, le contrat fait foi.

| Besoin | Lire (fichier, section) |
|---|---|
| Toutes les commandes, protections | `matrice/data/manuel-outils.md` (fiche 14, entonnoir) |
| Les listes FERMEES (types, categories, urgences, mots-cles, chemins) | `listes.py` (la SEULE source des valeurs) |
| Deposer au vrac (echelon 0) | `vrac/entry.py` (type PROPOSE par mots-cles, reclassable a la main) |
| Classer (echelons 1-2, categorie proposee auto -- M-027) / urgencer (echelon 3) | `classer/fonctions.py` (classer_mission : proposition + gardes) / `urgencer/entry.py` |
| La tresse (echelon 4) : tisser le brin, l'afficher | `tresse/fonctions.py` (paliers d'urgence + round-robin) + `tresse/entry.py` |
| Persistance + garde de racine | `stockage.py` (ecriture atomique, tmp + remplacement) |

## Commandes (details dans le manuel)

    python main.py deposer --theme "..." --objectif "..." [--urgence u] [--source s]
    python main.py classer --id E-XXX --type <dev|reparation|doc|audit|revision> [--categorie c]
    python main.py retirer  --id E-XXX    (sortie PROPRE du vrac -- M-058)
    python main.py urgencer --id E-XXX --urgence <bloquante|haute|normale|basse>
    python main.py tresse tisser / tresse brin / file

## Conventions de la zone

- Listes FERMEES : types, categories, urgences vivent dans `listes.py` seule ; une valeur
  hors liste est REFUSEE (code 2) -- la structure ne derive jamais (decision createur).
- Le classement PROPOSE (mots-cles) est deterministe et reclassable a la main : le
  createur reste souverain.
- ECHELON 4 : le brin se recompose TOUJOURS par `tresse tisser` (deterministe : meme
  contenu = meme sequence) avant lecture ; le pilote consomme la tete (`file consommer`
  ou puisage auto de `injecter`) -- la mission sort du brin ET de sa file-type.
- PORTE OFFICIELLE du tressage : ce dossier est la seule source de verite du brin ;
  le pilote l'appelle en sous-processus (jamais d'import croise -- modules homonymes).
- Modules renommes (`listes.py`/`stockage.py`, jamais constants.py/commun.py) : collision
  avec ceux du pilote, qui importe ce dossier via sous-processus.
- Ecriture atomique obligatoire (tmp + os.replace, LF forces) -- lecon M-018 : sans
  os.replace, le fichier reel n'est jamais mis a jour.
