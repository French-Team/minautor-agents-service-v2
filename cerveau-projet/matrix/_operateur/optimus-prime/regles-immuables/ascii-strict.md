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
