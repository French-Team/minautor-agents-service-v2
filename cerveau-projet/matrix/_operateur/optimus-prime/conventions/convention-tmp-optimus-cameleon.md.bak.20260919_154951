---
identite:
  type: convention
  appartient_a: optimus-prime
  commun: false
---

# CONVENTION -- PERIMETRE SCRIPTS TEMPORAIRES

> Source : modele v1 (tmp-<agent>/ a la racine, suppression fin de
> mission, registre) + mission M-094. Adapte a la Matrice : WRITE =
> matrix/ donc les dossiers tmp vivent dans matrix/.
>
> GRAVEE EN REGLE IMMUABLE le 2026-09-15 (GO createur, MO-104) :
> `regles-immuables/perimetre-tmp.md`. C est la REGLE qui fait foi et qui
> se relit a chaque demarrage ; cette convention n en est que la
> presentation et ne peut JAMAIS la contredire.

## La regle

1. Tout script temporaire, cobaye, preuve ou fichier jetable va dans
   SON dossier dedie, jamais ailleurs :
   - Optimus -> `cerveau-projet/matrix/tmp-optimus/`
   - Cameleon -> `cerveau-projet/matrix/tmp-cameleon/`
2. Interdits : racine projet, dossiers d outils, AppData/Temp,
   tout autre emplacement (contre-exemple : cobaye M-090).
3. La zone est PERMANENTE et porte TOUJOURS son README (decision createur
   du 2026-09-15) : le dossier reste, c est le chemin sur lequel
   s appuient les cobayes et les outils (ex : `dry-run.py`). Le supprimer
   rendait un oubli indiscernable d un etat normal.
4. Fin de mission : le CONTENU est vide (fichiers ET dossiers de cobaye),
   le README seul demeure. La preuve d un cobaye est son RESULTAT, lu a
   l execution ; sa suppression se TRACE (BDD modifications ou marbre).

## Garde

`garde-tmp.py` (appele par la porte du cockpit) accuse un residu hors
`tmp-*` ET une zone `tmp-*` privee de son README ; il INFORME du nombre de
fichiers presents sans accuser. Le contenu vide en fin de mission n est pas
verifiable par la garde : c est une discipline, et le texte de la regle
immuable le dit noir sur blanc.
