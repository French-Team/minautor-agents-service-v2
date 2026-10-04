# auditer-conformite-arbre + reconstruire-arbre

Deux outils jumeles pour la reparation des arbres des agents v1, **un agent a
la fois** (chaque arbre est different et doit etre traite seul) :

1. **auditer-conformite-arbre** : AUDIT (lecture seule) - detecte les
   problemes et incoherences structurelles de l'arbre d'un agent contre la
   liste de reference `besoins-v2.json`.
2. **reconstruire-arbre** : RECONSTRUCTION (ecriture ciblee) - reconstruit
   les fins de l'arbre selon le **modele round aero** (spec
   `spec-modele-round-avion-parachutiste.001.01.ebauche.md`, decision
   utilisateur 2026-08-30) : toute fin d'agent va vers **ORACLE**, jamais
   vers cerberus, jamais vers un autre agent.

## Usage

```bash
# 1. AUDIT : identifier les incoherences de l'arbre d'un agent
python3 .../auditer-conformite-arbre.py --agent <nom>

# 2. RECONSTRUIRE : dry-run d'abord (ne modifie rien), puis --ecrire
python3 .../reconstruire-arbre.py --agent <nom>            # dry-run
python3 .../reconstruire-arbre.py --agent <nom> --ecrire   # applique

# Aide / liste des besoins
python3 .../auditer-conformite-arbre.py --liste
```

## Verdict (audit)

| Verdict | Signification |
|---|---|
| **OK** | le besoin est satisfait |
| **BLOQUANT** | casse le pilotage ou la chaine (a corriger) |
| **AVERTISSEMENT** | risque non structurant (a examiner) |
| **INFO** | a evaluer selon le role de l'agent |

## Les besoins verifies (besoins-v2.json)

| Categorie | Besoins | Ce qu'ils garantissent |
|---|---|---|
| **schema-arbre** | A1-A6 | identite, appartenance, racine.branches, fins.fichier |
| **schema-theme** | T1-T6 | redirects, besoins, etapes, lien vers fins |
| **schema-fins** | F1-F3 | fins non vides, cases existantes, pas de cible placeholder |
| **schema-fins (aero)** | **F4** | **aucune fin ne cible cerberus (modele aero R1) - EXCEPTION : fin-coordination d ORACLE atterrit sur CERBERUS (fin de round, decision utilisateur 2026-09-02)** |
| **schema-fins (aero)** | **F5** | **aucune fin n'active un autre agent (vestige v1, R3)** |
| **coherence** | C1-C3 | themes existants, pas de fin morte, couverture des types deduits |
| **coherence (aero)** | **C4** | **separation montant/descendant (R4) : pas d activation directe dans les themes** |

## Ce que reconstruit reconstruire-arbre.py

| Transformation | Besoin | Mode |
|---|---|---|
| fin reactiver cible cerberus -> **oracle** (sauf oracle/fin-coordination, exception 2026-09-02) | F4 (R1) | --ecrire |
| fin activer un agent nomme -> **supprimee** + theme reoriente vers retour oracle | F5 (R3) | --ecrire |
| activation directe dans un theme -> **signalement a ORACLE** (mission-ajouter + fin reactiver-fin --cible oracle) | C4 (R4, v0.2.0) | --ecrire |
| theme-inter-round : reactivation de l'appelant -> **fin vers ORACLE** (le pilote reactive l'appelant depuis l'etat de carte) | C4 inter-round (R2, v0.2.0) | --ecrire |

Securite : dry-run par defaut ; `.bak` de fins.json ET de chaque theme
modifie avant ecriture ; ASCII strict + LF pur ; ne touche jamais les
branches de la racine ni les commandes de travail non-activantes.

## Source de verite

Le contrat pilote (pilote.py `_resoudre_racine`, `_piloter_theme`,
`_extraire_commandes_arbre`) + les templates v2 + la spec modele round aero
(2026-08-30) definissent ce qu'un arbre doit respecter pour etre pilote de
bout en bout sans cassure du round.

Note v1 vs v2 (2026-08-30) : la v1 a des themes vagues (sans couche
d'intention), des fins mortes et des fins vers cerberus / activations
vestiges ; le modele aero les remplace par des fins vers oracle.