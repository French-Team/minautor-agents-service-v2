---
identite:
  type: regle-immuable
  appartient_a: optimus-prime
  commun: false
---

# REGLE IMMUABLE -- ASCII STRICT

- ASCII strict dans tous les fichiers de la Matrice (comme en v1).
- Pas d'accents, pas de caracteres speciaux dans les fichiers .md et .json.
- Les messages vers le createur restent en francais lisible, meme si ASCII.
- EXCEPTION (decision createur) : `docs/` est la zone des SOURCES (vision,
  transcriptions, notes) -- LECTURE SEULE. Elle est EXEMPTEE : accents, degres
  et emojis y sont legitimes, et aucun scan ne doit y lever d alerte. Mesure du
  2026-09-17 : rien de `docs/` n est convertible (hors carte du convertisseur) ;
  la decision etait ecrite dans `garde-ascii` et PAS dans `corriger-ascii`, donc
  deux scans se contredisaient et la veille relancait un arbitrage deja rendu
  (friction 81, EO-135). Une exception qui n est pas ECRITE ici sera re-inventee
  par le prochain scan : c est ce fichier qui fait foi, pas le code.
- EXCEPTION (decision createur, MO-475) : `user-demandes/` est la PASSERELLE USER
  (user <-> optimus) : le user y ecrit ses demandes EN CLAIR, dans SA langue, hors
  de toute porte de la Matrice, et la Matrice les suit puis les EXTRAIT vers
  l entonnoir et le pilote. Elle est EXEMPTEE : accents, apostrophes et crochets y
  sont legitimes, et AUCUN scan ne doit y lever d alerte -- la CORRIGER mutilerait
  la parole du user, et la juger comme une ecriture non attribuee accuserait une
  ecriture LEGITIME. La declaration vit a son domicile unique
  (`matrice/data/commun/passerelle_user.py`) et se CONSOMME (M-076) :
  `controle-attribution` l exclut du jugement, `garde-ascii` la met HORS CHAMP en
  la NOMMANT. Mesure du 2026-09-29 (MO-492) : la decision etait ecrite DANS un seul
  instrument, donc un AUTRE instrument de la maison accusait la MEME zone (code 1,
  DEUX fichiers) et `/sante` portait un rouge pour une ecriture LEGITIME --
  exactement le defaut que la ligne ci-dessus avait annonce.
