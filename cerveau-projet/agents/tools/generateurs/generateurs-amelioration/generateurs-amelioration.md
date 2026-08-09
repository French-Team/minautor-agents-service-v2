# generateurs-amelioration

> Generateur d'amelioration et d'optimisation : pose des **listes de questions
> par theme** avant toute mission d'amelioration (outil, combo, generateur,
> carte de decision, case, regle...).
>
> Concept (demande utilisateur 2026-08-09) : quand une demande d'amelioration
> arrive, l'agent lance ce processus de questions pour garantir qu'il va etre
> le plus coherent et fournir de meilleures analyses et resultats. Les listes
> de questions vivent dans `themes-amelioration.json` : faciles a editer
> (modifier une question, un ensemble de questions, ajouter un theme).

## Version

- **1.0.0** (2026-08-09) : creation. Theme `ameliorer-outil` (10 questions).
- **2.0.0** (2026-08-09) : theme `ameliorer-outil` reformule (14 questions) : 5 RAPPELS STRATEGIQUES en tete (diagnostic de l existant, horloge, formats, ameliorer vs evoluer, perimetre) + 9 questions techniques. Les premiers rappels poussent l agent a reflechir a CE qui doit etre ameliore et a anticiper l EVOLUTION plutot que de patcher puis refondre (ex : une horloge pensee heure+minute doit anticiper secondes/chronometre ; une fonction mp3 doit penser aux autres formats).
- Compatibilite : Python 3, Bash (wrapper pur). Parite py/sh par construction.

## Pourquoi cet outil ?

| Probleme | Solution |
|---|---|
| L'amelioration d'un outil se fait sans questionnement prealable | Checklist de questions par theme, posee AVANT d'agir |
| Les cartes de decision se chargent de toutes les reflexions | La reflexion est deplacee dans l'outil (cartes allegees) |
| Les questions a se poser sont dispersees dans les lecons | Listes centralisees dans un JSON facile a editer par theme |

## Utilisation

```bash
# Lister les themes disponibles
python3 generateurs-amelioration.py --liste

# Aide / usage
python3 generateurs-amelioration.py --aide

# Poser la checklist d'un theme (mode interactif)
python3 generateurs-amelioration.py --theme ameliorer-outil

# Mode non-interactif (testable) : reponses fournies (14 questions)
python3 generateurs-amelioration.py --theme ameliorer-outil --reponses "q1=...;q2=...;q3=...;q4=...;q5=..."

# Version
python3 generateurs-amelioration.py --version
```

Le `.sh` est un wrapper pur (`exec python3 ... "$@"`) : meme comportement que
le `.py`.

## Fichier de themes (themes-amelioration.json)

```json
{
  "version": "2.0.0",
  "themes": [
    {
      "nom": "ameliorer-outil",
      "description": "...",
      "questions": [
        { "id": "q1", "question": "...", "raison": "..." }
      ]
    }
  ]
}
```

- `nom` : identifiant du theme (utilise avec `--theme <nom>`).
- `questions` : chaque question a un `id` unique, le texte `question`, et une
  `raison` (pourquoi cette question) affichee en mode interactif.
- Le theme `ameliorer-outil` a 14 questions : 5 RAPPELS STRATEGIQUES en tete
  (q1 diagnostic, q2 horloge - extensions naturelles, q3 formats - famille de
  cas, q4 ameliorer vs evoluer - eviter patch puis refonte, q5 perimetre) puis
  9 questions techniques (index/catalogue, interface, 5 fichiers, parite,
  ASCII/LF, tests, impacts, garde-fous, lecon).

## Regles

1. **AUCUN fichier cree** : l'outil est une reflection en session (checklist
   parcourue + recapitulatif) -- il ne modifie ni ne cree rien.
2. **ASCII strict** : code et fichiers de themes en ASCII (regle immuable).
3. **LF** : tous les fichiers de l'outil en LF (standard projet).
4. **Parite py/sh** : wrapper pur, memes resultats sur les memes arguments.
5. **Mode non-interactif** (`--reponses`) : indispensable pour les tests
   formels (Morpheus) sans saisie interactive.
6. **Regle des 5 fichiers** : py, sh, md, spec -- plus l'enregistrement dans
   index-tools.md et le catalogue generateurs-commande.

## Emplacement des fichiers

| Fichier | Chemin |
|---|---|
| Outil python | `agents/tools/generateurs/generateurs-amelioration/generateurs-amelioration.py` |
| Outil bash | `agents/tools/generateurs/generateurs-amelioration/generateurs-amelioration.sh` |
| Documentation | `agents/tools/generateurs/generateurs-amelioration/generateurs-amelioration.md` |
| Spec | `agents/tools/generateurs/generateurs-amelioration/spec/spec-generateurs-amelioration.001.01.ebauche.md` |
| Themes | `agents/tools/generateurs/generateurs-amelioration/themes-amelioration.json` |
