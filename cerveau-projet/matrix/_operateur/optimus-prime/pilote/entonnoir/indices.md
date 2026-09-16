---
identite:
  type: index
  appartient_a: optimus-prime
  commun: false
---

# INDICES -- pilote/entonnoir/ (echelons 0-4 de la file de missions)

> Tete de lecture : lire CECI avant les fichiers. L'indice pointe, le contrat fait foi.

| Besoin | Lire (fichier, section) |
|---|---|
| Toutes les commandes, protections | `matrice/data/manuel-outils.md` (fiche 14, entonnoir) |
| Les listes FERMEES (types, categories, urgences, mots-cles, chemins) | `listes.py` (la SEULE source des valeurs) |
| Deposer au vrac (echelon 0) | `vrac/entry.py` (type PROPOSE par mots-cles, reclassable a la main) |
| Classer (echelons 1-2, categorie proposee auto -- M-027) / poser le ROLE / urgencer (echelon 3) | `classer/fonctions.py` (classer_mission : proposition + gardes + role) / `retiqueter/entry.py` (role d'un item existant) / `urgencer/entry.py` |
| La table (type, categorie) -> ROLE (vivier) | `roles.py` (table COMPLETE, verifiee au chargement) |
| La tresse (echelon 4) : tisser le brin, l'afficher | `tresse/fonctions.py` (paliers d'urgence + round-robin) + `tresse/entry.py` |
| Persistance + garde de racine | `stockage.py` (ecriture atomique, tmp + remplacement) |

## Commandes (details dans le manuel)

    python main.py deposer --theme "..." --objectif "..." [--urgence u] [--source s] [--role THEME]
    python main.py classer --id EO-XXX --type <dev|reparation|doc|audit|revision> [--categorie c] [--role THEME]
    python main.py retiqueter --id EO-XXX --role <THEME du vivier>  (pose le ROLE + retisse)
    python main.py retirer  --id EO-XXX   (sortie PROPRE du vrac -- M-058)
    python main.py urgencer --id EO-XXX --urgence <bloquante|haute|normale|basse>
    python main.py tresse tisser / tresse brin / file

## Conventions de la zone

- PREFIXE PROPRE : les items de CET entonnoir sont **`EO-NNN`** (`listes.py
  PREFIXE_ITEM`, jamais recopie dans le code). `E-NNN` appartient a l'entonnoir du
  CAMELEON (Flux 1, `matrice/pilote/`) : les deux entonnoirs partageaient le prefixe
  `E-` avec deux compteurs separes, donc le meme id designait deux items differents
  (meme maladie que `M-` pour les missions d'Optimus). Un id hors famille est
  REFUSE (code 2) par les portes classer / retirer / urgencer.
- DEUX CHAMPS D'IDENTITE SUR UN ITEM (L-061/MO-076) : **`theme` = le TITRE** de la
  demande (texte libre, inchange) et **`role` = le ROLE de la mission**, choisi dans le
  VIVIER (champ FERME). Un item atteignant le brin SANS role fait REFUSER l'injection
  (le champ `theme` d'une mission est ferme, c'est le vivier) : c'est le ROLE qui devient
  le `theme` de la mission, le titre etant conserve en `titre`. Le role est POSE au
  classement (propose par la table `roles.py`, confirme ou corrige par `--role`), et
  `retiqueter` repare un item ne avant ce champ. Mesure de la panne fermee : 4 missions
  bloquees en attente d'un retiquetage a la main (MO-070, MO-071, MO-072, MO-075).
- Listes FERMEES : types, categories, urgences vivent dans `listes.py` seule ; un role vit
  dans le VIVIER (le pilote, source unique `commun.valider_theme` -- `roles.py` ne relit
  jamais le vivier, il interroge la porte) ; une valeur hors liste est REFUSEE (code 2)
  -- la structure ne derive jamais (decision createur).
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
