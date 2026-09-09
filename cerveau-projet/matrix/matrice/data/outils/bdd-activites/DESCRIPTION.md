# OUTIL bdd-activites

> Outil de la Matrice (plan des 7 BDD, 6/7) : la BDD activites-recentes.json,
> revue des activites PAR SECTIONS a emplacements precis (JAMAIS "a la suite").
> Modele-mere : AGENTS-activite-recente.md (les 50 dernieres activites de la session v1).

## Ce qu'il fait

- `noter` : depose UNE activite dans UNE section (--section --detail --tags "a,b").
  Les sections sont PRE-DECLAREES dans constants.py (emplacements precis) :
  une section inconnue est REFUSEE (code 2). Chaque section garde ses
  TAILLE_SECTION dernieres entrees (rotation automatique, les plus anciennes sortent).
- `lire` : affiche les activites, toutes sections ou une seule (--section), filtrables par tag.
- `verifier` : integrite structurelle (cles requises, tailles de rotation respectees)
  + empreinte SHA-256 (convention-integrite-sha256.md).

## Regles respectees

1. Sections fermees : la structure du registre ne derive jamais au fil des notes.
2. Rotation : la section reste petite par conception (revue RECENTE, pas archive).
3. Ecriture ATOMIQUE (tmp + remplacement, fins de ligne LF forcees) ; empreinte a chaque ecriture.
4. Tags obligatoires (tri et injection).
