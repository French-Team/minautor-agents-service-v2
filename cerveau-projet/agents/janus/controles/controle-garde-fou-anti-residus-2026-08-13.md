---
type: rapport-controle
agent: janus
date: 2026-08-13
objet: garde-fou anti-residus v0.5.2 activer-agent-principal
verdict: VALIDE
---

# Controle croise final -- Garde-fou anti-residus v0.5.2 (activer-agent-principal)

**Objet** : correction de la cause racine des residus 0.2.1/v0.2.6 (sorties
accidentelles de reactiver redirigees vers des fichiers nommes comme des versions).

## Diagnostic racine

- Les fichiers 0.2.1/v0.2.6 (commit b051714) contenaient le stdout integral d une
  reactivation (contenu IDENTIQUE) - creation par la COMMANDE D APPEL (redirection
  > ou tee), pas par l outil.
- Le code .sh + .py (v0.5.1) etait PROPRE : aucune redirection vers un nom de
  version, verifie sur tout l historique git + docs + spec + catalogue.
- Correction decision utilisateur : garde-fou PROACTIF dans l outil (v0.5.2) +
  regle documentee, en complement du garde-fou reactif test-039.

## Verifications

| # | Verif | Resultat |
|---|---|---|
| J1a-c | Garde-fou present py + sh, declenchement actions reelles (pas aide/--version) | 3/3 OK |
| J2a-d | Preuve sandbox : positif/negatif py + sh | 4/4 OK |
| J3a-b | Section doc "Ne jamais rediriger la sortie" + ligne versionning 0.5.2 | 2/2 OK |
| J4a-d | Versions 0.5.2 partout + normes 0/0 + test-007 VALIDE + test-039 4/4 | 4/4 OK |
| J5 | NON-REGRESSION COMPLETE : 40/40 OK (45.2 s, +1% vs reference 44.7 s) | OK |

## Points d attention

- test-024 doit etre lance en COMMANDE DIRECTE (jamais depuis un script temporaire
  .tmp-*.py a la racine) : l artefact d auto-incrimination fait KO (lecon Morpheus).
- detecter-divergences-version : usage reel = --racine (pas --tous).

## Conclusion

VERDICT : VALIDE. Garde-fou proactif operationnel (py + sh), regle documentee,
versions alignees 0.5.2, spec/py ALIGNE, non-regression 40/40. La classe d accident
"redirection de sortie vers fichier semver" est desormais visible immediatement au
point d entree ET surveillee en continu (test-039).
