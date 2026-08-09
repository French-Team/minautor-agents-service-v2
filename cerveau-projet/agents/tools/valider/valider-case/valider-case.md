# valider-case

> Valide une **carte de decision** (parcours JSON) et **ALLEGE les cases** :
> structure, modele compose, surcharge des indices, references, normes.
> Verdict : **CONFORME / A ALLEGER / NON CONFORME** + rapport markdown.
>
> Outil de l'etape 2 de la refonte des cartes de decision
> (spec-refonte-cartes-decision v0.1.1) : il rend les cartes largement plus
> lisibles et suivies.

## Version

- **1.0.1** (2026-08-09) : garde-fou anti-pollution du rapport (lecon : rapport a la racine). Sans `--rapport <fichier>` explicite, aucun fichier n'est cree (jamais de rapport par defaut dans le repertoire courant).
- **1.0.0** (2026-08-09) : creation. Conforme au contrat de la spec section 6.
- Compatibilite : Python 3, Bash (wrapper pur). Parite py/sh par construction.

## Utilisation

```bash
# Valider toutes les cases d'un parcours (defaut)
python3 valider-case.py cerveau-projet/agents/cerberus/parcours/parcours-cerberus.json

# Valider UNE case
python3 valider-case.py <parcours.json> --case c13b

# Verifier uniquement la surcharge des indices
python3 valider-case.py <parcours.json> --surcharge

# Verifier uniquement le modele compose (branches min 2, deviation = rejoint)
python3 valider-case.py <parcours.json> --modele

# Verifier uniquement les references d'indices
python3 valider-case.py <parcours.json> --references

# Simulation sans ecrire le rapport / rapport personnalise
python3 valider-case.py <parcours.json> --dry-run
python3 valider-case.py <parcours.json> --rapport mon-rapport.md

# Version / aide
python3 valider-case.py --version
python3 valider-case.py --aide
```

Le `.sh` est un wrapper pur (`exec python3 ... "$@"`) : meme comportement que
le `.py`.

## Verifications (garde-fous)

| Domaine | Controle |
|---|---|
| **Structure** | ids uniques, types valides (question/controle/indice/action/fin), case_depart existante, fins joignables (BFS) |
| **Modele** | decision (question/controle) = branches min 2 ; indice/action = suivant requis ; aucune boucle directe ; impasses signalees ; deviation sans rejoint visible = avertissement |
| **Allegement** | case avec > 3 indices OU texte de regle > 160 caracteres = SIGNALEE avec proposition de reference |
| **References** | chaque indice `{type: regle, ref: X}` doit resoudre (pattern-N -> spec-guider-parcours ; chemin -> fichier ; protocole-/regle- -> regles-immuables) |
| **Normes** | nommage des cases (c<numero>[a-z]?), titre present, ASCII 0 |

## Verdict

- **CONFORME** : aucune erreur, aucune surcharge
- **A ALLEGER** : surcharges sans erreur (la carte fonctionne mais est a alleger)
- **NON CONFORME** : au moins une erreur (structure/modele/references/normes)

Le rapport markdown est ecrit UNIQUEMENT au chemin fourni par
`--rapport <fichier>`. Sans `--rapport`, aucun fichier n'est cree
(garde-fou v1.0.1 : jamais de rapport par defaut dans le repertoire courant).
Utiliser `--dry-run` pour simuler sans rien ecrire.

## Regles

1. **LECTURE SEULE** : l'outil ne modifie JAMAIS le parcours audite.
2. **ASCII strict** : tout contenu non-ASCII du parcours est signale.
3. **LF** : fichiers de l'outil en LF (standard projet).
4. **Parite py/sh** : wrapper pur, memes resultats sur les memes arguments.
5. **Spec de reference** : spec-refonte-cartes-decision v0.1.1 (etape 2).
6. **Regle des 5 fichiers** : py, sh, md, spec + enregistrements
   (index-tools.md, catalogue generateurs-commande).

## Emplacement des fichiers

| Fichier | Chemin |
|---|---|
| Outil python | `agents/tools/valider/valider-case/valider-case.py` |
| Outil bash | `agents/tools/valider/valider-case/valider-case.sh` |
| Documentation | `agents/tools/valider/valider-case/valider-case.md` |
| Spec | `agents/tools/valider/valider-case/spec/spec-valider-case.001.01.ebauche.md` |
