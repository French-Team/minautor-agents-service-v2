# Controle -- Template fiche-agent v0.2.0 (Buffy) 2026-08-07

**Objet controle** : fiche-agent-template.md (v0.2.0) -- standard parcours = source de verite
**Mission controlee** : mettre a jour le template selon le standard v0.2.0 (modele morpheus.md)
**Agent auteur** : Buffy (developpeur principal -- fichiers du cerveau)
**Date du controle** : 2026-08-07

---

## Mission de controle

Verifier independamment (je ne fais pas confiance) :

| # | Point a verifier | Methode |
|---|---|---|
| 1 | Frontmatter allege : version 0.2.0, carte_decision SUPPRIMEE | inspection |
| 2 | Section PARCOURS (SOURCE DE VERITE DU GUIDAGE) avec commande guider-parcours + lien spec | inspection |
| 3 | 0 mission detaillee (pas de tableaux de missions dans la fiche) | inspection |
| 4 | REGLE ABSOLUE PARCOURS + REGLE IMMUABLE ASCII presentes | inspection |
| 5 | REGLE ABSOLUE 5 mise a jour : indice outil de la CASE (pas colonne de tableau) | inspection |
| 6 | Outils de base P0 incluant guider-parcours | inspection |
| 7 | Connexions : parcours JSON + guider-parcours references | inspection |
| 8 | Historique : ligne v0.2.0 ajoutee | inspection |
| 9 | Conformite ASCII du template | valider-conformite-ascii |
| 10 | Aucune trace d'outil externe | detecter-usage-outils-externes |

---

## Verdict

- **Verdict** : VALIDE (10/10 points)
- **Points valides** : 10/10
- **Problemes detectes** : aucun
- **Detail** : frontmatter allege (carte_decision supprimee, version 0.2.0),
  section PARCOURS (SOURCE DE VERITE) avec commande exacte + lien spec v0.2.0,
  0 mission detaillee, REGLE ABSOLUE PARCOURS + REGLE IMMUABLE ASCII presentes,
  REGLE ABSOLUE 5 mise a jour (indice outil de la CASE du parcours),
  guider-parcours dans les outils P0, connexions parcours JSON + guider-parcours,
  historique v0.2.0, ASCII 0 non-conforme, traces externes 0.

---

## Lecons

1. Le template est desormais aligne sur le standard v0.2.0 : tout nouvel agent
   cree a partir de ce template naitra avec le parcours (jeu de piste) comme
   source de verite, sans carte de decision obsolete.
2. La REGLE ABSOLUE 5 a ete mise a jour en coherence avec le parcours : l'indice
   outil vient de la CASE (pas de la colonne d'un tableau) -- le template doit
   reflete l'outil de guidage, pas l'ancienne fiche.
3. Le rappel ASCII est integre au template (REGLE IMMUABLE ASCII + rappel dans
   le paragraphe A CONSTRUIRE) : les nouveaux agents sont formes a la regle
   des la creation.
