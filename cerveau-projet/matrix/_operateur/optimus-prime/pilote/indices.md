---
identite:
  type: index
  appartient_a: optimus-prime
  commun: false
---

# INDICES -- pilote OPTIMUS (Flux 2, MO-001)

> Pilote dedie _operateur/optimus-prime/pilote/ (Flux 2, invisible cameleon).
> Miroir du pilote cameleon (matrice/pilote/) mais isole : file/historique/entonnoir/intercom dedies.
> Tete de lecture : lire CECI avant les fichiers. L'indice pointe, le contrat fait foi.

| Besoin | Lire (fichier, section) |
|---|---|
| Toutes les commandes, options, protections | `matrice/data/manuel-outils.md` (fiche pilote) |
| Etat de la file Optimus | `file-missions-optimus.json` (via l'outil, jamais a la main) |
| Architecture (main -> categories -> fonctions) | `DESCRIPTION.md` + table architecture |
| Priorite d'injection + puisage auto (tresse) | `commun.py` (tisser_tresse, puiser_tresse) + `injection/fonctions.py` (preparer_injection) |
| Consommation manuelle de la tresse (echelon 4) | `commun.py` (consommer_tete_tresse) + `file/entry.py` |
| Checklist par type (auto a l'injection) | `checklist/listes.py` (listes fermees) + `checklist/entry.py` |
| ROLE d'une mission : QUI conduit (posture) + QUOI toucher (chantier) | `personnalites.py` (POSTURE_PAR_TYPE, mappage ferme) + `injection/fonctions.py` (charger_role_mission) + `README-roles.md` |
| Les echelons 0-4 de la file | `entonnoir/indices.md` (indices dedies de l'entonnoir) |

## Commandes (memorisees vite fait, details dans le manuel)

    file / charger --theme --objectif / lot --lot --theme t1,t2 --objectif o1|o2
    transformer --id --theme --objectif / statut / injecter / enchainer / fin --bilan
    enregistrer --id --theme --objectif --bilan (mission DEJA TERMINEE menee hors file :
              ecrit la FILE et le JOURNAL -- debut + fin notes par la porte noter)
    retiqueter --id --theme [--motif] (corrige le theme, tout statut, trace conservee)
    file consommer (echelon 4 : tete du brin -> file du pilote)
    checklist --id MO-XXX

## Conventions de la zone

- SERIE STRICTE : au maximum une mission en cours ; le refus de double injection est normal.
- CHAMP THEME FERME : charger / lot / transformer valident le theme contre le
  vivier (valider_theme dans commun.py) -- refus code 2 + liste si hors vivier,
  canonisation a la porte (casse ignoree) ; la TRESSE reste ouverte (le vrac
  accepte le brut, c'est son role). EXCEPTION : `enregistrer` ne valide PAS le
  theme -- il enregistre un FAIT historique, et le vivier d'aujourd'hui n'a pas
  a juger une mission deja faite (sinon un theme retire du vivier plus tard
  rendrait sa mission inenregistrable).
- COMPTEUR : c'est le seul qui attribue les ids (prochain_id). Une mission menee
  HORS file laisse le compteur en arriere -> la charge suivante reprendrait un
  id DEJA PRIS. `enregistrer` fait avancer le compteur : c'est sa raison d'etre
  au moins autant que la tracabilite (MO-045 / MO-046, 2026-09-13).
- DEUX TRACES (2026-09-13, MO-054) : la FILE (pilote) et le JOURNAL
  (suivi-optimus) consignent la MEME mission, et le controle de coherence les
  croise. Un verbe qui ecrit l'une doit ecrire l'autre : `enregistrer` note donc
  lui-meme debut + fin au journal (par la porte `noter`) au lieu de laisser a
  l'agent le soin d'y penser -- oublier ce pas fabriquait un ECART de coherence
  a chaque enregistrement.
- CHAMP THEME A L'INJECTION (2026-09-13) : l'entonnoir accepte un theme en texte
  libre, l'injection ne verifiait que le defcon -- un theme hors vivier entrait
  donc dans le flux (erreur passee : 'MATRICE' sur 9 missions). Le garde est
  desormais pose a l'injection (`garder_theme_et_checklist`), point de passage
  UNIQUE des deux chemins (mission simple ET lot) : plus aucune porte derobee,
  et pas de deuxieme lecture du vivier a maintenir.
- ROLE DE L'ITEM D'ENTONNOIR (2026-09-13, L-061 / MO-076) : le garde ci-dessus
  etait juste, mais l'identite manquait en AMONT -- un item portait son TITRE en
  texte libre, aucun ROLE. A la relance automatique (fin -> tete du brin -> file),
  l'injection refusait donc le titre et la mission attendait un retiquetage a la
  main (4 blocages mesures : MO-070, MO-071, MO-072, MO-075). Un item porte
  desormais DEUX champs : `theme` (titre libre) et `role` (theme du VIVIER, pose
  au classement -- propose par la table `entonnoir/roles.py`, complete et verifiee
  au chargement -- ou corrige par `--role`). `consommer_tete_tresse` fait du ROLE
  le `theme` de la mission et conserve le titre en `titre` ; sans role, il REFUSE
  et NE consomme PAS la tete, en nommant la porte qui repare (`entonnoir
  retiqueter --id EO-XXX --role <THEME>`). Le refus de l'injection nomme lui aussi
  cette porte (selon l'origine de la mission).
- CHECKLIST JAMAIS VIDE (2026-09-13) : `fabrique_checklist` rend les garde-fous
  COMMUNS quand le type est inconnu (avant : liste vide -> mission sans aucun
  garde-fou, silencieusement). Le specifique du type reste ferme a 5 types.
- PRIORITE CREATEUR de `injecter` : 1) le lot arme, 2) la file des missions chargees,
  3) la TRESSE (puisage automatique). La tresse est toujours TISSEE avant le puisage
  (brin frais et deterministe), via la PORTE OFFICIELLE de l'entonnoir : sous-processus
  `python entonnoir/main.py tresse tisser` -- JAMAIS d'import croise (modules homonymes,
  lecon L-009).
- Un lot = plusieurs rounds dans la meme boucle : `enchainer` lance la 1re, chaque `fin`
  enchaine la suivante (DEBUT/FIN annonces), RETOUR consolide a la Matrice a la fin du lot.
- Apres un `fin` SANS lot : la mission suivante DEMARRE automatiquement (priorite
  lot -> file -> tresse, E-008) -- la boucle ne meurt jamais ; quand tout est vide,
  le fin se termine proprement (message d'etat, jamais d'erreur).
- Modules homonymes interdits dans les sous-outils du pilote : `listes.py`/`stockage.py`
  (jamais constants.py/commun.py -- collision avec ceux du pilote).
- ISOLEMENT : file `file-missions-optimus.json`, entonnoir `entonnoir-files-optimus.json`, historique
  `_operateur/historiques-missions-optimus.jsonl`, intercom prive `_operateur/intercom/` (MO-001, jamais M-).
- VIVIER : partage (data/vivier-themes.json) + prive (_operateur/parcours/themes/*.json) fusion dedupliquee.
- Traces : historique dedie Optimus + boites intercom privees.
