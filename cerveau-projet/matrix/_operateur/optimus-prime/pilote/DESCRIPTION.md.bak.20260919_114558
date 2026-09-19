---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
  version: 2.2.0
  role: pilote actif (filtrage + routinier + automatisations + missions)
---

# PILOTE OPTIMUS -- Pilote Actif (Flux 2)

> Le pilote est une COUCHE AUTOMATE entre la Matrice et les agents.
> Il fait les taches routinieres que l'agent n'a pas besoin de faire.

## Les 4 piliers du pilote actif

### 1. Filtrage (verbe `filtrer`)
Detecte les `[mot]` et route vers la bonne porte.
8 crochets reconnus : mission, audit, revision, question, alerte, pause, bilan, preparation.

### 2. Routinier (automatique, sans intervention)
- **Vue suivi-optimus DEBUT** : apres `injecter`, le pilote REGENERE la vue
  derivee `matrice/suivi-optimus.md`
- **Vue suivi-optimus FIN** : apres `fin`, le pilote REGENERE la meme vue

> ATTENTION (marbre L-020, 2026-09-11) : le pilote ne note RIEN au JOURNAL.
> Il ne fait que rafraichir la VUE derivee. Les evenements `debut` / `fin` de
> `data/suivi-optimus.jsonl` sont declares par l'AGENT, via la porte
> `python matrice/data/outils/suivi-optimus/main.py noter --mission MO-XXX
> --theme <T> --action <debut|fin> --detail "..."`.
> Un appel automatique du pilote a `noter` creait un 2e fin (doublon MO-030,
> attrape par `verifier` le 2026-09-13) : il a ete retire volontairement.
> Ce paragraphe decrivait l'ancien comportement -- il a induit en erreur
> jusqu'au 2026-09-13.

### 3. Verification post-fin (automatique)
Apres chaque `fin`, le pilote lance :
- **py_compile** sur les .py mentionnes dans le bilan
- Messages `[POST-FIN] py_compile OK/FAIL` en sortie

### 4. Nettoyage intercom (automatique)
Apres chaque `fin`, le pilote purges les messages traites de la boite maintenance.

## Options

```
python main.py file                       -> affiche la file
python main.py charger --theme <t> --objectif "..." -> ajoute une mission
python main.py transformer --id MO-XXX --theme <t> --objectif "..." -> re-etiquette
python main.py enregistrer --id MO-XXX --theme <t> --objectif "..." --bilan "..."
                                       -> enregistre une mission DEJA TERMINEE
                                          menee HORS file (fait avancer le
                                          compteur : aucun id n'est reutilise)
                                          ET note debut + fin au journal par la
                                          porte `noter` (les deux traces d'Optimus
                                          restent d'accord : MO-054)
python main.py retiqueter --id MO-XXX --theme <nom> [--motif "..."]
                                       -> CORRIGE le theme, quel que soit le
                                          statut (trace theme_avant conservee)
python main.py statut                     -> etat mission en cours
python main.py injecter                   -> injection ordonnee (lot > file > tresse)
python main.py fin --bilan "..."          -> cloture + verification + nettoyage + enchainement
python main.py checklist --id MO-XXX [--reconstruire]
                                          -> checklist selon le type ;
                                             --reconstruire l'enregistre si elle
                                             manque (trace : jamais injectee)
python main.py filtrer --message "..."    -> DETECTE [mot] et ROUTE automatiquement
```

## Garde-fous

- **Serie stricte** : 1 mission en cours a la fois (refus injecter si en cours)
- **Doublons** : detection de theme+objectif identique dans la file
- **Pause M-080** : aucune injection/chainement pendant la pause
- **Champ ferme des THEMES (2026-09-13)** : un theme hors vivier ne devient
  JAMAIS du travail. Le garde est pose a l'INJECTION -- point de passage unique
  qui couvre l'entonnoir, `charger` et une file modifiee a la main, sans
  dupliquer la lecture du vivier (une seule source : `commun.valider_theme`).
  La mission reste en attente jusqu'a sa correction : `retiqueter` pour une
  mission, et **`entonnoir retiqueter --id EO-XXX --role <THEME>`** quand elle
  vient d'un item d'entonnoir (le refus NOMME la bonne porte, selon l'origine).
  Le chemin du LOT passe par le meme garde (plus de porte derobee).
- **ROLE DE L'ITEM D'ENTONNOIR (2026-09-13, L-061)** : le garde des themes etait
  juste, mais l'identite manquait en amont -- l'item portait son TITRE en texte
  libre et AUCUN role, donc la relance automatique fabriquait une mission que le
  garde refusait, jusqu'a un retiquetage a la main (4 blocages mesures : MO-070,
  MO-071, MO-072, MO-075). Un item porte desormais `theme` (titre) ET `role`
  (theme du vivier, pose au classement et verifie) : `consommer_tete_tresse` fait
  du role le `theme` de la mission et garde le titre en `titre` ; sans role, il
  refuse et ne consomme pas la tete (rien ne disparait).
- **Checklist JAMAIS vide (2026-09-13)** : le specifique vient du TYPE (liste
  fermee de l'entonnoir), mais les garde-fous COMMUNS valent pour TOUTE
  mission. Avant, un type inconnu rendait une liste vide : 6 missions ont
  tourne sans aucun garde-fou (ni tests reels, ni py_compile, ni ASCII, ni fin
  par le pilote) sans que rien ne le signale. L'injection signale desormais un
  ECART quand le type manque (checklist reduite aux communs).

## Architecture

| Piece | Role |
|---|---|
| main.py | point d'entree global : DIRIGE |
| constants.py | chemins, valeurs |
| commun.py | fonctions communes + **3 automatisations** (verif, nettoyage, garde-fou) |
| file/ | charger + transformer + **retiqueter** (correction) + **enregistrer** (hors file) + afficher |
| injection/ | statut + injecter (**vue DEBUT rafraichie**) |
| fin/ | cloturer (**vue FIN rafraichie** + **verif post-fin** + **nettoyage** + enchainement) |
| checklist/ | checklist par type |
| **filtrer/** | **DETECTION CROCHETS + routage** |
