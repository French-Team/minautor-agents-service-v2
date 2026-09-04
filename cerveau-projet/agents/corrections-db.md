# Memoire des corrections des agents v1

Oui : `corrections.md` ne doit pas rester un historique complet. Il sert de
**memoire courte**, lisible rapidement lors de l'activation d'un agent.

## Repartition

- `corrections.md` : regles indispensables + 10 dernieres lecons de l'agent.
- `cerveau-projet/agents/lecons/lecons.db` : memoire longue officielle, geree
  par `enregistrer-lecon` et `consulter-lecons`.
- `cerveau-projet/agents/corrections.db` : index/import de compatibilite des
  corrections Markdown de tous les agents v1.

Le nouvel outil partage ne doit pas supprimer une ancienne lecon avant son
import dans la memoire longue.

```bash
python3 cerveau-projet/agents/corrections-db.py import
python3 cerveau-projet/agents/corrections-db.py import --trim
```

`--trim` reduit uniquement les blocs explicites `## [LECON] ...`. Les anciens
tableaux de lecons sont importes mais ne sont pas automatiquement tronques,
car leur format varie selon les agents et une troncature aveugle pourrait
supprimer la structure d'un fichier. Leur migration devra etre faite par un
outil dedie, avec test et conservation en BDD.

Socrate n'est pas responsable de cette infrastructure. Il peut la consulter
comme les autres agents, mais il conserve son role de revision strategique.

Le fichier source reste en francais ; toute contribution future doit aussi
rester en francais.