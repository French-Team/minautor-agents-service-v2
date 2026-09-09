# OUTIL bdd-variables

> Outil de la Matrice (plan des 7 BDD, 5/7) : la BDD classeur-variables.json,
> registre des variables vivantes de la Matrice (etats, seuils, config decidee).
> Modele-mere : le classeur v1 (agents/classeur-variables/stockage/variables-actuelles.md).

## Ce qu'il fait

- `definir` : cree ou met a jour UNE variable (--cle --valeur [--source] --tags "a,b").
  Une cle = une valeur courante : re-definir une cle existante la met a jour,
  l'identifiant V-XXX est conserve (jamais de doublon de cle).
- `lire` : affiche les variables, toutes ou une seule (--cle).
- `verifier` : integrite structurelle (cles requises) + empreinte SHA-256
  (convention-integrite-sha256.md).

## Regles respectees

1. Ecriture ATOMIQUE (tmp + remplacement, fins de ligne LF forcees) : jamais de BDD a moitie ecrite.
2. Empreinte SHA-256 enregistree a chaque ecriture (fichier .sha256) ; l'espion-integrite controle.
3. Tags obligatoires (tri et injection).
4. LECTURE SEULE hors de la porte unique : aucune autre modification possible.
