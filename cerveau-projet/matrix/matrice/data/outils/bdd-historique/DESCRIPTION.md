# OUTIL bdd-historique

> Outil de la Matrice (plan des 7 BDD, 7/7) : la BDD historique-bdd.jsonl,
> JOURNAL GLOBAL de tous les evenements significatifs de la Matrice, avec filtrage.
> Contrat data-readme : historique global avec filtrage (doublons, obsoletes).

## Ce qu'il fait

- `noter` : verse UN evenement au journal (--type --detail --tags "a,b").
  Journal en AJOUT SEUL : on n'ajoute des lignes, on ne modifie jamais l'histoire.
  Un DOUBLON ACTIF (meme type + meme detail qu'un evenement non obsolete) est REFUSE.
- `lire` : affiche les evenements ACTIFS (par defaut), filtrables par
  --type, --tag, --depuis (date minimale), --tout (y compris obsoletes).
- `marquer-obsolete` : appose le marquage obsolete SUR AJOUT (une nouvelle ligne
  qui vise l'id) -- l'entree originale n'est JAMAIS reecrite.
- `verifier` : integrite structurelle (cles requises, ids uniques, marqueurs
  qui visent un id existant). Sans empreinte (journal ajout seul).

## Regles respectees

1. AJOUT SEUL : l'histoire n'est jamais reecrite (le marquage obsolete est un ajout).
2. Doublons actifs refuses : le journal ne gonfle pas de repetitions.
3. Ecriture LF ; garde-fou structurel sur data/.
4. Tags obligatoires (tri et injection).
