> MEMOIRE GELEE le 2026-09-04 - decision utilisateur v1->v2 : les
> nouvelles lecons vont dans bdd-lecons (outil v2). Historique conserve
> pour relecture - AUCUN [LECON] supplementaire.
# Corrections -- Hades

> Fenetre glissante des lecons et corrections de Hades.
> Cree le 2026-08-22 (M8a, decision utilisateur : agent dedie au git).

## Contexte de creation

- **Role** : SEUL habilite aux commandes git (gardien des archives).
- **Regle d anciennete** : git = sauvegarde du passe. Checkout interdit hors
  fichiers tres tres recents (minutes) - au-dela, reparation dans le present
  par l agent habilite (flux INTER-ROUND).
- **Origine** : incident du 2026-08-22 - un checkout sur un commit vieux de
  plusieurs jours aurait ecrase toute la session non commitee.

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |
