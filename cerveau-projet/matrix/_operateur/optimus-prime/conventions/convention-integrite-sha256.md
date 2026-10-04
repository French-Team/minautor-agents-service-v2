---
identite:
  type: convention
  appartient_a: optimus-prime
  commun: false
---

# CONVENTION -- INTEGRITE DES FICHIERS (SHA-256)

> Source : docs/conversation-unslot-gemma-4.md (bloc "empreinte digitale de l'information").
> Generalisation obligatoire : tout controle d'integrite de la Matrice passe par SHA-256.

## Pourquoi SHA-256

- Un hash n'est pas un chiffrement : c'est une empreinte digitale du contenu.
- Une modification d'UN seul caractere change totalement l'empreinte.
- MD5 et SHA-1 sont casses (collisions possibles) -> INTERDITS pour nos controles.
- SHA-256 est le standard resistant aux collisions -> OBLIGATOIRE.

## Workflow en deux temps

1. **Generation** : a la creation d'un fichier, calculer et enregistrer son SHA-256
   dans des metadonnees separees (ex: <fichier>.sha256).
   Le hash enregistre = etalon-or.
2. **Verification** : avant utilisation, recalculer le hash et comparer a l'etalon.
   - Match : fichier sain.
   - Non-match : fichier altere -> REFUS + signalement du defaut d'integrite.

## Usage dans la Matrice

- Les espions de pistage utilisent le SHA-256 pour prouver qu'un fichier n'a pas derive.
- Toute copie, sauvegarde ou restauration d'un fichier de la Matrice est verify par empreinte.
