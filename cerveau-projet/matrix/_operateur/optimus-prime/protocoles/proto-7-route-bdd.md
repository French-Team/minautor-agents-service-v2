---
identite:
  type: protocole
  appartient_a: optimus-prime
  commun: false
---

# PROTOCOLE 7 -- ROUTE BDD (la porte unique)

> Source : convention-integrite-sha256 + data-readme + preuves M-013 a M-068
> (zero corruption depuis l'instauration). Toute ecriture de la Matrice suit
> cette route ; le mot [bilan] ne fait que LIRE (bilan-periode), il n'ecrit
> jamais.

## La route (5 etapes)

1. **Identifier la BDD cible et SON outil dedie** : indices data/indices.md
   puis data-readme.md (tableau BDD -> outil + Qui ecrit : les ecrivains
   sont DECLARES -- un ecrivain non declare est un ecart a signaler).
2. **Lire avant d'ecrire** : verbe `lire` et/ou `verifier` de l'outil
   (structure + empreinte). On ne modifie jamais ce qu'on n'a pas lu.
3. **Ecrire UNIQUEMENT par l'outil dedie** : verbe ferme (ajouter / definir /
   noter / deposer...), tags OBLIGATOIRES (refus code 2 sinon), source
   tracee (mission M-XXX). L'outil garantit : ecriture atomique (tmp +
   remplacement), fins de ligne LF, empreinte SHA-256 recalculee a cote.
4. **Verifier apres** : verbe `verifier` de l'outil (structure + empreinte
   reelle vs etalon), puis l'espion-integrite confirme au prochain tour.
5. **Journaliser** : la modification du FICHIER source (outil, protocole...)
   passe par bdd-modifications ; la BDD elle-meme n'est pas re-notee dans
   une autre BDD (pas de doublon).

## Interdits

- Editer un JSON/JSONL de data/ a la main (script ad hoc = ecrire a la main).
- Ajouter un deuxieme ecrivain sans le declarer dans data-readme.
- Ecrire hors du perimetre declare (v1 ecrivains : voir regles-groupes) ;
  les agents v2 (freelance) n'ecrivent QUE dans cerveau-projet/freelance/.
- Confondre journal append-only (.jsonl : on ajoute, jamais on ne reecrit
  l'historique) et registre consulte (.json : on met a jour l'entree).
