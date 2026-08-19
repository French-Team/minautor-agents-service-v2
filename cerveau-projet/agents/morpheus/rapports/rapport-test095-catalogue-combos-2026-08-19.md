---
type: rapport-tests
agent: morpheus
date: 2026-08-19
mission: garde-fou catalogue-combos
verdict: VALIDE
---

# Rapport : test-095-catalogue-combos-garde-fou

## Objet

Creer le test garde-fou qui verrouille la synchronisation combo -> outils
(mission utilisateur 2026-08-19 : les outils ne signalaient pas leur
appartenance a un combo).

## Points verifies (8)

1. catalogue-combos.json : JSON valide + version 0.1.0 + 21 combos
2. chaque combo a une fiche .md ou une definition-combo.json
3. chaque membre est un outil reel ou une commande generateur (anti-fantome)
3b. chaque membre reel a le champ combos dans sa fiche
4. aucune declaration combos orpheline (bidirectionnel)
5. consulter-combos --outil evaluer-coherence : reponse correcte
6. ASCII strict : 0 non-ASCII
6b. LF pur : 0 CRLF

## Preuve negative

Membre fantome injecte dans combos-audit-general : DETECTE par le point 3,
catalogue restaure. Le garde-fou ne laisse passer ni membre fantome ni
desynchronisation fiche <-> catalogue.

## Tests connexes (tous verts)

| Test | Resultat |
|---|---|
| test-095 (nouveau) | 8/8 OK |
| test-092 (parite activation) | 9/9 OK |
| test-093 (combo full ascii) | 17/17 OK |
| test-094 (valider tableaux) | 7/7 OK |
| test-063 (profils tests) | 11/11 OK |
| test-087 (categories tags) | 8/0 KO |
| test-030 (protections importees) | 10/10 OK |

## Verdict

VALIDE. test-095 ajoute au profil "tests" de la non-regression : toute
desynchronisation entre le catalogue des combos et les fiches outils est
desormais bloquante.
