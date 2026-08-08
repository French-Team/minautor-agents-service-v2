# Controle -- Spec-guider-parcours v0.2.0 (Vulcain) 2026-08-07

**Objet controle** : spec-guider-parcours.001.01.ebauche.md (v0.2.0) -- documentation des 2 patterns
**Mission controlee** : documenter le pattern multi-missions + le rappel ASCII obligatoire dans la spec
**Agent auteur** : Vulcain (constructeur d'outils -- la spec est un fichier de son outil)
**Date du controle** : 2026-08-07

---

## Mission de controle

Verifier independamment (je ne fais pas confiance) :

| # | Point a verifier | Methode |
|---|---|---|
| 1 | Version coherente : titre v0.2.0, champ Version 0.2.0, historique v0.1.0 -> v0.2.0 | inspection |
| 2 | Regle 6 du format : rappel ASCII OBLIGATOIRE dans les cases d'ecriture (indice regle en tete) | inspection |
| 3 | Regle 7 du format : pattern multi-missions (case Mission + branches + chemins convergents) | inspection |
| 4 | Section Patterns valides en production : Pattern 1 (multi-missions) + Pattern 2 (rappel ASCII) avec exemples | inspection |
| 5 | Exemple reel cite : parcours-janus.json (30 cases, 3 chemins) -- le fichier existe | verification |
| 6 | Criteres d'acceptation 9-10 ajoutes (rappel ASCII + multi-missions) | inspection |
| 7 | Statut ebauche conserve (pas de promotion prematuree) | inspection |
| 8 | La spec reste ASCII stricte | valider-conformite-ascii |
| 9 | Coherence : les regles 6-7 du format sont conformes a la section Patterns | inspection croisee |
| 10 | Aucune trace d'outil externe | detecter-usage-outils-externes |

---

## Verdict

- **Verdict** : VALIDE (10/10 points)
- **Points valides** : 10/10
- **Problemes detectes** : aucun
- **Detail** : version 0.2.0 coherente (titre + champ + historique v0.1.0 -> v0.2.0),
  regles 6 (rappel ASCII) et 7 (multi-missions) ajoutees au format, section
  Patterns valides en production avec les 2 patterns documentes + exemples,
  exemple reel parcours-janus.json (30 cases, 3 chemins) verifie existant,
  criteres d'acceptation 9-10 ajoutes, statut ebauche conserve, ASCII 0
  non-conforme, traces externes 0, coherence regles <-> Patterns confirmee.

---

## Lecons

1. La spec est devenue la reference du format : les patterns valides en
   production (multi-missions, rappel ASCII) sont maintenant des REGLES DE FORMAT
   (regles 6-7) + une section dediee + des criteres d'acceptation -- un triple
   ancrage qui rend le non-respect detectable par le controle.
2. Versionner la spec : v0.1.0 -> v0.2.0 dans le .md (pas de dossier versions/),
   statut ebauche conserve (l'outil n'est pas encore en production).
3. La documentation des patterns cite un exemple REEL (parcours-janus.json) --
   verifier que l'exemple cite existe avant de valider.
