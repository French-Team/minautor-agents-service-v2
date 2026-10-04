---
identite:
  type: rapport-janus
  date: 2026-08-13
  objet: controle croise regle seul janus lance la non-regression
---

# Controle Janus : regle seul-janus-lance-non-regression (Buffy + Morpheus)

**Contexte** : mission Janus (dernier maillon, active par Themis) - controle
croise final de la regle de gouvernance SEUL JANUS LANCE LA NON-REGRESSION
(demande utilisateur) + principe d identite des agents.

## Verifications (J1-J5)

| Check | Resultat |
|---|---|
| J1. test-037 present + vert + integre | 5/5 OK, serie d, DUREES_OK |
| J2. Seul janus reference l outil (11 cartes) | ['janus'] uniquement |
| J3. Cartes morpheus/vulcain + fiches Pattern 14 | morpheus v0.4.5, vulcain v0.4.6, fiches OK, regle NON-REGRESSION JANUS presente |
| J4. Normes | 0/0 sur tous les fichiers modifies |
| J5. Non-regression complete | 37/37 OK (42.4 s, chrono ameliore) - apres relance directe sans script temporaire |

## Analyse

1. La regle est pleinement appliquee : seul janus c4 garde
   tester-lancer-non-regression. Morpheus execute des tests individuels
   uniquement (python3 test-XXX.py + protections) ; la non-regression
   complete est le role de Janus en fin de chaine - c est d ailleurs ce que
   ce controle vient de faire : Janus a lance la non-regression finale.
2. Le test-037 verifie aussi le principe d identite : 11 cartes a signatures
   de contenu distinctes. Le trio athena/promethee/minerve partage la meme
   structure d ids (meme construction, voulu) avec des contenus differents
   (identites distinctes) - conforme a la philosophie utilisateur.
3. Le KO test-024 observe en J5 etait l artefact classique (non-regression
   lancee depuis un script .tmp-* encore present a la racine). Relance
   directe : 37/37 OK. Aucun vrai ecart.

## Verdict : VALIDE

Mission conforme : test-037 5/5 OK, cartes corrigees, normes 0/0,
non-regression complete 37/37 OK. Fin de chaine : reactivation Cerberus.
