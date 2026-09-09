# intercom : COMMUNICATION DE LA MATRICE

> Communication organisee par la Matrice entre : elle-meme, le pilote, l'agent.
> Rien ne circule hors de ces canaux. A construire avec le pilote multi-missions.

## Canaux prevus (dans le sens du flux unique)

| Canal | Sens | Contenu |
|---|---|---|
| canal-matrice-pilote | Matrice -> pilote -> Matrice | theme + mission(s) a l'aller ; bilan consolide au retour |
| canal-pilote-agent | pilote -> agent -> pilote | injections ordonnees (theme, ordres, lecons utiles, espions) a l'aller ; fin de mission au retour |

## Forme prevue

- Boites par acteur : `<acteur>/inbox.jsonl` + `<acteur>/outbox.jsonl`
  (acteurs prevus : matrice/, pilote/, agent/).
- Message = une ligne json : id, date, expediteur, destinataire, type
  (mission / injection / fin / bilan / alerte), charge utile.
- Lecture + acquittement obligatoires (outil Python dedie).
- Espions de pistage embarques dans les injections : temps d'execution,
  tokens avant/apres (usages-outils-combos.jsonl).

## Regles

1. Les injections du pilote sont ORDONNEES, FILTREES, NORMALISEES
   (regles-immuables/injections-ordonnees.md).
2. Une mission non acquittee = alerte, jamais une repetition a l'aveugle.
3. Intercom ne transporte JAMAIS de contenu hors flux v1/v2 (hors flux formel).
4. Entretien de la boite matrice/ (M-052) : a chaque passe de veille, les
   alertes-grave python-compile dont le fichier cible n'existe plus sont
   retirees (fantomes : incident resolu) ; toute autre ligne est INTOUCHABLE
   (fin-mission, retour-lot, incident, alertes vivantes). Resulte dans le
   journal de la veille (`purge-boite`).

## Statut : EN CONSTRUCTION (2 boites reelles)

Faits (2026-09-06) : `pilote/outbox.jsonl` (injection M-001) et
`matrice/inbox.jsonl` (fin-mission M-001) ecrits par le pilote.
Reste : boite agent/, acquittements, espions embarques dans les injections.
