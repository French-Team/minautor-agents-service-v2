# Rapport -- Pilote v2 : RELECTURE HONNETE sur Vision (2026-08-26)

## Mission

Repliquer le mecanisme v1 de RELECTURE (QUESTION HONNETE) dans la v2,
avec Vision comme PILOTE : quand le LLM s'incarne un agent, il doit
VRAIMENT lire sa fiche et ses corrections (etre honnete), sinon il
incarne un agent fantome.

## Regle v1 source (template v1, regle absolue)

"Quand je suis active ou reactive, je me pose la question : 'As-tu EN
MEMOIRE ta fiche et tes corrections, capables de les appliquer SANS
relire ?' Je reponds la VERITE. OUI -> continuer ; INCERTAIN ou NON ->
RELIRE corrections puis fiche AVANT de continuer. Seul OUI prouve la
memorisation : 'je viens de les lire' n'est pas une preuve."

## Corrections appliquees (pilote : Vision)

| Fichier | Correction |
|---|---|
| `freelance/vision/vision.md` | REGLE ABSOLUE -- RELECTURE (QUESTION HONNETE) en tete des regles absolues (version v2 : "le LLM doit VRAIMENT lire pour incarner l'agent") |
| `freelance/vision/parcours/arbre-vision.json` | Regle D7 ajoutee (version guidee, meme question honnete) |
| `freelance/vision/corrections.md` | Lecon datee 2026-08-26 en tete de section LECONS (Vision = pilote, generalisation aux autres agents v2 ensuite) |

## Validations

- JSON arbre-vision valide.
- Formats v2 preserves : LF pur (0 CRLF introduit), accents preexistants
  intacts (vision.md 72 non-ascii = preexistants).
- Regle presente aux 3 endroits (fiche 1, arbre 1, corrections 2).

## Prochaine etape

Generaliser la regle aux autres agents v2 (stark, forge, shuri, rogers,
parker, jarvis...) apres validation du pilote Vision.
