# Controle -- Doc guider-parcours.md v0.2.0 (Vulcain) 2026-08-07

**Objet controle** : guider-parcours.md (v0.2.0) -- reference spec v0.2.0 + 2 patterns
**Mission controlee** : mettre a jour la documentation de l'outil guider-parcours
**Agent auteur** : Vulcain (constructeur d'outils)
**Date du controle** : 2026-08-07

---

## Mission de controle

Verifier independamment (je ne fais pas confiance) :

| # | Point a verifier | Methode |
|---|---|---|
| 1 | Version 0.2.0 en tete + lien spec-guider-parcours.001.01.ebauche.md (v0.2.0) | inspection |
| 2 | Section Patterns (spec v0.2.0) : Pattern 1 multi-missions + Pattern 2 rappel ASCII, conformes a la spec | inspection croisee |
| 3 | Regles 5-6 ajoutees (rappel ASCII + multi-missions) coherentes avec la spec regles 6-7 | inspection croisee |
| 4 | Liste des parcours complete : vulcain, morpheus, clio, janus (pas seulement le prototype) | inspection |
| 5 | Tableau Versionning : ligne 0.2.0 ajoutee, distincte de 0.1.0 | inspection |
| 6 | CLI restent 0.1.0-py / 0.1.0-sh (distinction version outil vs version doc) | inspection |
| 7 | Exemple reel cite (parcours-janus.json) existe | verification |
| 8 | Conformite ASCII de la doc | valider-conformite-ascii |
| 9 | Coherence globale : la doc ne contredit pas la spec v0.2.0 | inspection croisee |
| 10 | Aucune trace d'outil externe | detecter-usage-outils-externes |

---

## Verdict

- **Verdict** : VALIDE (10/10 points)
- **Points valides** : 10/10
- **Problemes detectes** : aucun
- **Detail** : version 0.2.0 en tete + lien spec-guider-parcours (v0.2.0), section
  Patterns conforme a la spec (Pattern 1 multi-missions + Pattern 2 rappel ASCII),
  regles 5-6 de la doc coherentes avec les regles 6-7 de la spec, liste des parcours
  complete (vulcain, morpheus, clio, janus), tableau Versionning 0.2.0 distinct,
  CLI restent 0.1.0-py/-sh (distinction version outil vs version doc), exemple reel
  parcours-janus.json verifie, ASCII 0 non-conforme, traces externes 0.

---

## Lecons

1. Distinction version OUTIL vs version DOC : la doc passe en 0.2.0 mais les CLI
   restent 0.1.0-py/-sh (l'outil lui-meme n'a pas change) -- le tableau Versionning
   documente cette distinction correctement.
2. La doc et la spec doivent etre SYNCHRONISEES : section Patterns + regles 5-6 de
   la doc = regles 6-7 de la spec v0.2.0 (verification croisee).
3. La liste des parcours de la doc doit couvrir tous les parcours existants, pas
   seulement le prototype -- verifier l'exhaustivite a chaque evolution.
