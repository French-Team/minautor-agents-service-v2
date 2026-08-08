# Controle -- Parcours Janus (Buffy) 2026-08-07

**Objet controle** : parcours-janus.json (30 cases) + fiche janus.md allegee v0.2.0
**Mission controlee** : construire le parcours (jeu de piste) de Janus -- 3 missions de controle (outil, statut, modification)
**Agent auteur** : Buffy (developpeur principal -- fichiers du cerveau)
**Date du controle** : 2026-08-07
**Note d'independance** : c'est MON parcours, mais je controle le TRAVAIL DE BUFFY (je n'ai pas participe a la creation) -- je reste objectif (Regle 2).

---

## Mission de controle

Verifier independamment (je ne fais pas confiance) :

| # | Point a verifier | Methode |
|---|---|---|
| 1 | 3 branches de la case Mission (outil, statut, modification, autre) | inspection |
| 2 | Chemin outil : etapes conformes a la fiche (mission AVANT, doc, tests, conventions, ASCII, cartes, verdict) | navigation |
| 3 | Chemin statut : RVAV, lister-statuts, detecter-erreur-statut, changer-statut | navigation |
| 4 | Chemin modification : 12 etapes (ancienne/nouvelle version, impacts, nommage, liens, role, separation, combo, tableaux, surcharge, traces externes, verdict) | navigation |
| 5 | Regles 1 et 4 de Janus presentes en indices (ecrire mission AVANT, signaler sans corriger) | inspection |
| 6 | Rappel ASCII (indice regle) dans chaque case d'ecriture (mission, lecons) | inspection |
| 7 | JSON valide (--liste) + navigation des 3 chemins -> PARCOURS TERMINE | guider-parcours |
| 8 | Fiche allegee : section PARCOURS (SOURCE DE VERITE), 0 mission detaillee, regles absolues conservees | inspection |
| 9 | Conformite ASCII des 2 fichiers | valider-conformite-ascii |
| 10 | Aucune trace d'outil externe | detecter-usage-outils-externes |

---

## Verdict

- **Verdict** : VALIDE (10/10 points)
- **Points valides** : 10/10
- **Problemes detectes** : aucun
- **Detail** : 4 branches de la case Mission (outil c2, statut c11, modification c18,
  autre c27) ; les 3 chemins de controle naviguent jusqu'a PARCOURS TERMINE avec les
  etapes conformes a la fiche ; Regle 1 (ecrire mission AVANT) x3 et Regle 4
  (signaler sans corriger) en indices ; rappel ASCII x4 dans les cases d'ecriture ;
  fiche allegee v0.2.0 (0 mission detaillee, 7 REGLE ABSOLUE conservees) ; ASCII 0
  non-conforme ; traces externes 0.

---

## Lecons

1. Independance du controle : je controle le travail de Buffy sur MON propre
   parcours -- je n'ai pas participe a la creation, donc je reste objectif (Regle 2).
   Controleur != auteur, meme quand le sujet est le controleur lui-meme.
2. Un parcours multi-missions : la case Mission avec 4 branches et 3 chemins qui
   convergent vers les cases communes (verdict c8, lecons c9, retour c10) -- le
   pattern permet de couvrir toutes les missions d'un agent dans un seul parcours.
3. Les regles specifiques de l'agent (Regle 1, Regle 4) sont portees par des
   indices regle dans les cases concernees -- pas de duplication dans la fiche.
