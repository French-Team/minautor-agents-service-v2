# editer-parcours

**Categorie** : Editer
**Version** : 0.1.6
**Statut** : ebauche
**Agent** : Vulcain
**Date** : 2026-08-15

Edite les **parcours de decision JSON** (`cerveau-projet/agents/*/parcours/
parcours-*.json`) de maniere **sure** : insertion / retrait de case,
modification de branche / suivant, increment de version. Backup + dry-run
obligatoires avant toute ecriture reelle.

---

## Objectif

Remplacer les **scripts temporaires de manipulation des parcours**
(`.zz-insertion-*.py`, `.zz-fix-version-*.py`, `.zz-fix-suivant-*.py`) qui ont
cause des erreurs connues : `suivant` auto-reference, cases non joignables,
versions non bumpees. Cet outil centralise ces operations avec validation.

## Utilisation

```bash
# Inserer une case (id c15b, cible du suivant c16)
python3 editer-parcours.py --agent cerberus \
  --inserer-case '{"id":"c15b","titre":"Controle","type":"controle","question":"...","branches":[{"reponse":"OUI","vers":"c15c"},{"reponse":"NON","vers":"c16"}],"indices":[{"type":"regle","texte":"..."}]}' \
  --dry-run
# puis --wet pour ecrire

# Retirer une case en re-pointant vers elle (les suivant/branches sont reperes)
python3 editer-parcours.py --agent buffy --retirer-case c42 --vers c22 --wet

# Modifier une branche
python3 editer-parcours.py --agent cerberus --branche c15 --reponse OUI --cible c15b --wet

# Modifier un suivant
python3 editer-parcours.py --agent cerberus --suivant c15c --cible c15b --wet

# Remplacer le contenu complet d une case (v0.1.3)
python3 editer-parcours.py --agent themis --modifier-case c1 \
  --contenu '{"type":"action","titre":"...","texte":"...","indice":"..."}' --wet

# Incrementer la version mineure (x.y.z -> x.y.z+1)
python3 editer-parcours.py --agent vulcain --bump --wet
```

## Options

| Option | Description |
|---|---|
| `--agent <nom>` | Parcours cible (obligatoire) |
| `--inserer-case <json>` | JSON de la case a ajouter (cle `id` ou `cXX`) |
| `--retirer-case <id>` | Supprime une case + re-pointe vers `--vers` (ou elle-meme) |
| `--vers <id>` | Cible de re-pointage (avec `--retirer-case`) |
| `--branche <case> --reponse <r> --cible <id>` | Modifie une branche |
| `--suivant <case> --cible <id>` | Modifie le suivant |
| `--modifier-case <id> --contenu <json>` | Remplace le contenu complet d une case (v0.1.3) |
| `--bump` | Incremente la version mineure |
| `--backup` / `--no-backup` | Backup `.bak` avant ecriture (defaut : oui) |
| `--dry-run` / `--wet` | Simule / ecrit reellement |

## Securite

- **Dry-run par defaut** : aucune ecriture sans `--wet`
- **Backup automatique** : `parcours-*.json.bak` avant toute modification
- **JSON/LF/ASCII preserves** : ecriture en LF pur, `ensure_ascii=True`
- **VERROU DU MARBRE (v0.1.2)** : les cases protegees de l agent edite (manifeste `marbre.json`) ne peuvent pas etre modifiees/supprimees sans protocole (protocole-securite-marbre) - ecriture REFUSEE
- **ANTI-CONTOURNEMENT (v0.1.3)** : `cartes-lock.json` (manifeste des empreintes SHA-256 des cartes, dans `cerveau-projet/agents/regles-immuables/marbre/`). Toute carte dont l empreinte diverge du lock a ete modifiee **HORS editer-parcours** (ecriture directe de script) -> ecriture REFUSEE. Apres chaque ecriture legitime, editer-parcours met a jour l empreinte. Restauration d une carte verrouillee : `git checkout` (retour a l etat enregistre) puis re-synchro.
- Apres modification, lancer `valider-case` pour verifier la joignabilite
## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.5 | 2026-08-17 | MESSAGES INFORMATIONNELS : afficher_messages_info en fin d action reussie (rappel Pattern 14 + valider-cartes + tests pins) - regle immuable v0.3.0 |
| 0.1.3 | 2026-08-15 | ANTI-CONTOURNEMENT : option `--modifier-case <id> --contenu <json>` (remplacer le contenu d une case sans ecriture directe) + verrou `cartes-lock.json` (empreintes SHA-256 des 14 cartes) - une carte modifiee HORS editer-parcours est REFUSEE, editer-parcours resynchronise le lock apres chaque ecriture legitime |
| 0.1.2 | 2026-08-15 | VERROU DU MARBRE : verifier_cases_protegees() compare les cases protegees de l agent edite (manifeste marbre.json) avant d ecrire et REFUSE si une case protegee a ete modifiee/supprimee sans protocole (protocole-securite-marbre) |
| 0.1.1 | 2026-08-13 | GARDE-FOU ANTI-RESIDUS : verifier_residus_racine() detecte les fichiers nommes comme des versions semver a la racine (residus de redirections accidentelles de sortie) et affiche un WARNING - sources de verite de version dans cerveau-projet/agents/clio/, JAMAIS a la racine |
