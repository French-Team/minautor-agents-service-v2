# MOULE -- outil-bdd (template d'outil BDD conforme)

> Le modele-mere est `data/outils/bdd-lecons/` : architecture entree ->
> categorie -> fonctions simples, garde de racine, ecriture atomique LF,
> empreinte SHA-256 a chaque ecriture, tags obligatoires.
> Ce dossier en est le MOULE a jetons : il ne s'execute JAMAIS seul --
> il est consomme par l'outil `dupliquer-template`.

## Les jetons (remplaces a la generation)

| Jeton | Signification | Exemple |
|---|---|---|
| `__NOM_OUTIL__` | nom du dossier outil (sous data/outils/) | bdd-remarques |
| `__NOM_BDD__` | nom du fichier BDD (dans data/) | remarques.json |
| `__PREFIXE_ID__` | prefixe des identifiants d'entrees | R |
| `__CLE_LISTE__` | cle de la liste des entrees dans la BDD | remarques |
| `__CHAMP__` | nom de l'option CLI et du champ de contenu | remarque |
| `__HUMAIN__` | libelle humain (minuscules) dans les messages | remarque |
| `__HUMAIN_CAP__` | libelle humain (initiale en majuscule) | Remarque |

## Duplication (l'unique porte : dupliquer-template)

```
python main.py generer --nom bdd-remarques --bdd remarques.json --prefixe R \
       --liste remarques --champ remarque [--humain remarque]
```

Le generateur :
1. lit ce moule (JAMAIS un outil vivant) ;
2. construit les sources du clone EN MEMOIRE (jetons remplaces) ;
3. verifie chaque fichier AVANT d'ecrire : py_compile + ASCII strict
   + aucun jeton residuel ;
4. verifie le clone executable (sans argument : docstring + code 2) ;
5. n'ecrit sur disque QUE si tout est vert (jamais d'outil a moitie livre).

Apres generation : creer la BDD par la porte du clone (`ajouter`), ajouter
la BDD au registre de l'espion-integrite, poser la fiche du manuel.
