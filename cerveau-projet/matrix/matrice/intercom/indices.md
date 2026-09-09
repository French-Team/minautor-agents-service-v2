# INDICES -- intercom/ (communication organisee)

> Tete de lecture : lire CECI avant les fichiers. L'indice pointe, le contrat fait foi.

| Besoin | Lire (fichier, section) |
|---|---|
| Boites, format, direction des messages | `intercom-readme.md` (contrat) |
| Messages du pilote (injections, debut/fin) | `pilote/outbox.jsonl` |
| Messages vers la Matrice (fins, retour-lot) | `matrice/inbox.jsonl` |

## Conventions de la zone

- Format jsonl en AJOUT SEUL : une ligne = un message JSON, jamais de reecriture.
- Message type : {type, date, mission, ...} -- ASCII strict.
- Les annonces debut/fin de mission sont deposees par le pilote (pas a la main).
- Le retour-lot (bilan consolide) arrive dans matrice/inbox a la fin d'un lot.
