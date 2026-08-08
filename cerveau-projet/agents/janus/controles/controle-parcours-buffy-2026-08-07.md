# Controle -- Parcours Buffy (Buffy) 2026-08-07

**Objet controle** : parcours-buffy.json (36 cases) + fiche buffy.md allegee v0.2.0
**Mission controlee** : construire le parcours (jeu de piste) de Buffy -- developpeur principal
**Agent auteur** : Buffy (developpeur principal -- fichiers du cerveau)
**Date du controle** : 2026-08-07

---

## Mission de controle

Verifier independamment (je ne fais pas confiance) :

| # | Point a verifier | Methode |
|---|---|---|
| 1 | Case Mission avec 6 branches (creer, modifier, agent, protocole, controler, autre) | inspection |
| 2 | Chemin creer : nommage, structure, existence, creer-fichier, index, lecons | navigation |
| 3 | Chemin modifier : lire, dependances, editer, corriger, condenser/nettoyer, RVAV, lecons | navigation |
| 4 | Chemin agent : nom, dossier, template + corrections, AGENTS.md | navigation |
| 5 | Chemin protocole : convention, dossier, creer, RVAV | navigation |
| 6 | Chemin controler : documents manquants, fichiers vides, combo, tableaux | navigation |
| 7 | Delegations : pense-bete -> Athena (c17), outil -> Vulcain (c31) -- branches | navigation |
| 8 | Sous-missions : case c32 avec FLUX ORIENTE | navigation |
| 9 | Rappel ASCII (Pattern 2) dans les cases d'ecriture (creer, modifier, lecons, agent, protocole) | inspection |
| 10 | Fiche allegee : PARCOURS (SOURCE DE VERITE), 0 mission detaillee + ASCII 0 non-conforme | inspection + valider |

---

## Verdict

- **Verdict** : VALIDE (10/10 points)
- **Points valides** : 10/10
- **Problemes detectes** : aucun
- **Detail** : case Mission avec 6 branches (creer/modifier/agent/protocole/controler/autre) ;
  les 6 chemins naviguent jusqu'a PARCOURS TERMINE ; rappel ASCII x6 dans les cases
  d'ecriture (Pattern 2 applique : creer c5, lecons c7, modifier c11, lecons c15,
  agent c20, protocole c25) ; delegations en branches (Athena c17 pense-bete, Vulcain
  c31 outil) ; sous-missions case c32 (FLUX ORIENTE) ; fiche allegee 0 mission
  detaillee avec PARCOURS (SOURCE DE VERITE) ; ASCII 0 non-conforme.

---

## Lecons

1. Le parcours de Buffy est le PLUS RICHE (36 cases, 6 chemins) : c'est l'agent
   qui ecrit le plus de fichiers du cerveau -- le Pattern 2 (rappel ASCII) y est
   applique 6 fois, la principale cible de l'erreur ASCII.
2. Les delegations de Buffy sont des branches : pense-bete -> Athena, outil ->
   Vulcain -- la REGLE DELEGATION (n'ecrire jamais un outil ou un pense-bete
   soi-meme) est incarnee dans la structure du parcours.
3. La sous-mission est une case dediee (c32) avec le FLUX ORIENTE (sauvegarder
   -> sortir -> revenir) -- une sous-mission n'est jamais une fin.
