---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Spec -- generateurs-ligne

**Version** : 0.3.0
**Statut** : ebauche
**Date creation** : 2026-08-09
**Agent** : Vulcain (outil)
**Historique** : v0.1.0 (creation, 2026-08-09) -- suite des generateurs de cartes de decision (carte -> ligne -> case). v0.2.0 (2026-08-09) -- gabarits EXTERNALISES dans gabarits-ligne.json (une place pour chaque chose) + sous-commande ajouter-config (validation + dry/wet) pour ajouter une config reutilisable sans toucher au code de l'outil (Pattern 12). v0.3.0 (2026-08-09) -- sous-commande copier (demande utilisateur validee par le questionnaire ameliorer-outil) : dupliquer une LIGNE existante d une carte (2 sources : --source case avec 3 modes complet/branche/suite, ou --config gabarit) pour faciliter la composition de nouvelles lignes ; generateurs-case assure ensuite l edition fine du clone.

---

## 1. Objectif

Completer la suite des generateurs de cartes de decision avec le maillon du
milieu : `generateurs-ligne` ajoute une LIGNE (chemin de bout en bout :
point d'entree -> fin) a une carte, construite a partir de GABARITS de
groupes de cases (configs) predefinis. Avant toute edition, il verifie que
la carte cartographique d'Atlas (`cartographie-<agent>.md`) existe et est a
jour (mtime), et bloque sinon avec une invite a activer Atlas. Dry/wet pour
valider l'ajout. Les gabarits sont EXTERNALISES dans `gabarits-ligne.json`
et extensibles via `ajouter-config` (config reutilisable, sans modifier le
code de l'outil).

## 2. Contexte

### 2.1 Origine

Decision utilisateur (2026-08-09) : completer la suite `generateurs-carte`
(carte complete) + `generateurs-case` (une case) avec un generateur de LIGNE
qui permette d'editer facilement la carte de decision d'un agent sans faire
le travail soi-meme (le travail d'edition fine reste a l'agent habilite via
SA carte).

### 2.2 Concept valide par l'utilisateur

1. **LIGNE** = un chemin de bout en bout (scenario : point d'entree -> fin),
   insere comme un flux.
2. **CONFIGS** = gabarits de groupes de cases predefinis : defaut (decision
   2 branches + rejoint), config-1 (decision + deviation + rejoint, Pattern 7
   complet), config-2 (controle RVAV + branches), config-3 (action simple).
3. **CARTE A JOUR** = `cartographie-<agent>.md` existe ET mtime plus recent
   que le parcours JSON ; sinon -> bloquer + inviter a activer Atlas.
4. **DRY/WET** = `--dry-run` simule l'ajout ; wet ecrit + valide.

## 3. Interface

```
generateurs-ligne.py <parcours.json> verifier
generateurs-ligne.py <parcours.json> lister-configs
generateurs-ligne.py <parcours.json> config <nom>
generateurs-ligne.py <parcours.json> ajouter --config <nom> [options]
generateurs-ligne.py ajouter-config <nom> --description "<texte>" --gabarit <fichier.json> [--force] [--dry-run]
generateurs-ligne.py <parcours.json> copier --source <case> [--mode complet|branche|suite] [--branche <reponse>] [options]
generateurs-ligne.py <parcours.json> copier --config <nom> [options]
```

Options de `ajouter` : `--point-attache <case>` (defaut case_depart),
`--reponse <reponse>` (defaut NON), `--rejoint <case>`, `--titre <texte>`,
`--force`, `--dry-run`, `--verbose`.

Options de `ajouter-config` : `--description <texte>` (obligatoire),
`--gabarit <fichier.json>` (obligatoire, structure `{cases: [...]}`),
`--force` (ecrase une config existante), `--dry-run`.

Options de `copier` : `--source <case>` OU `--config <nom>` (une des deux
obligatoire), `--mode complet|branche|suite` (defaut complet), `--branche
<reponse>` (mode branche), `--point-attache`, `--reponse`, `--rejoint`,
`--titre`, `--force`, `--dry-run`, `--verbose`.

## 4. Sous-commandes

### 4.1 verifier

Verdict CARTE A JOUR / CARTE A REGENERER (existence + mtime).

### 4.2 lister-configs / config

Liste les gabarits / detail d'un gabarit.

### 4.3 ajouter

1. Verifie la carte Atlas (sauf `--force`) : si absente/perimee -> bloque
   avec invite a activer Atlas (case c31 Cartographier de sa carte).
2. Determine le point d'attache (defaut case_depart).
3. Determine la case de rejoint (defaut : ancien suivant pour une
   action/indice ; obligatoire pour une question/controle).
4. Construit le bloc de cases (ids `c<numero>`, `c<numero>a`, ... conformes
   a la convention `c<numero>[a-z]?`).
5. Cable le point d'attache : branche ajoutee (question/controle) OU suivant
   recable (action/indice).
6. Dry-run : affiche sans ecrire. Wet : ecrit + validation auto
   (guider-parcours --liste + valider-case --modele --references).

### 4.4 ajouter-config

1. Lit le fichier gabarit (`--gabarit`) de structure `{cases: [...]}` (format
   JSON externe identique aux cases de `gabarits-ligne.json`).
2. VALIDE le gabarit : nom conforme (lettres minuscules/chiffres/tirets),
   description non vide, types dans (question, controle, action), branches
   min 2 pour une decision avec destinations resolvables, suivants d'action
   resolvables, case REJOINT presente.
3. Verifie le conflit de nom (existe deja sans `--force`).
4. Dry-run : simule sans ecrire. Wet : insertion programmatique (json.load ->
   ajout -> json.dumps) + reecriture triee (jamais de concatenation), puis
   la config est utilisable par `ajouter --config <nom>`.

### 4.5 copier

1. Determine la source : `--source <case>` (avec `--mode`) OU `--config
   <nom>` (gabarit de gabarits-ligne.json).
2. DETECTION du groupe depuis une case source :
   - mode `complet` (defaut) : si la source est une decision, elle est le
     point d entree de la ligne -> copie toute sa suite jusqu au REJOINT ; si
     c est une action, remonte aux predesseurs jusqu a la 1re decision
     (point d entree) puis copie tout le sous-chemin.
   - mode `branche` : copie UNIQUEMENT la branche choisie d une decision
     (`--branche <reponse>`), sinon erreur.
   - mode `suite` : copie le chemin qui part de la source jusqu au REJOINT.
3. Le groupe exclut les cases REJOINT (remplacees par la cible de rejoint
   externe) ; les liens internes sont re-mappes sur de NOUVEAUX ids conformes
   `c<numero>[a-z]?` (groupes jusqu a 27 cases : cX + suffixes lettres ; plus
   grands : numeros sequentiels c<base+i>).
4. Memes garde-fous que `ajouter` : carte Atlas a jour (existence + mtime,
   blocage + invite Atlas sauf `--force`), cablage du point d attache
   (branche sur question/controle, suivant sur action/indice), rejoint par
   defaut = ancien suivant, dry/wet, validation auto CONFORME.
5. Cas d usage : copier une ligne existante pour composer une nouvelle ligne,
   puis `generateurs-case` edite les cases du clone finement.

## 5. Gabarits

Les gabarits vivent dans `gabarits-ligne.json` (externalises).

## 5. Gabarits

| Config | Cases | Sorties |
|---|---|---|
| defaut | cX (question) + cXa, cXb (actions) + REJOINT | branches OUI/NON -> rejoint |
| config-1 | cX (question) + cXa (principal) + cXb/cXc (deviation) + REJOINT | Pattern 7 complet |
| config-2 | cX (controle) + cXa (OUI) + cXb (NON) + REJOINT | RVAV |
| config-3 | cX (action) + REJOINT | enchainement sans question |

## 6. Regles

1. ASCII strict (100%), LF pur.
2. 100% stdlib Python.
3. Nommage prefixe `generateurs-` controle au demarrage.
4. Ids de cases conformes `c<numero>[a-z]?` (valider-case).
5. Validation auto apres ecriture (guider-parcours + valider-case).
6. Insertion JSON programmatique (jamais de concatenation de lignes).
7. Chaine Morpheus (tests) -> Janus (controle) OBLIGATOIRE apres creation.

## 7. Critere d'acceptation

1. `verifier` distingue CARTE A JOUR / A REGENERER (existence + mtime).
2. `ajouter` bloque sans carte a jour (invite Atlas), `--force` passe outre.
3. Chaque config ajoute son bloc en une commande, cablage correct
   (branche ou suivant), rejoint correct, ids conformes.
4. `--dry-run` ne modifie rien ; wet ecrit + validation CONFORME.
5. Parite py/sh (--version identiques).
6. ASCII + LF sur les 6 fichiers (py, sh, md, spec, gabarits-ligne.json, test).
7. `ajouter-config` valide le gabarit avant insertion et gere dry/wet + conflit de nom.
8. `copier` : 2 sources (--source/--config), 3 modes (complet/branche/suite),
   clone conforme (ids uniques c<numero>[a-z]?), dry/wet, blocage carte Atlas.

## 8. Emplacement des fichiers

| Fichier | Chemin |
|---|---|
| Outil python | `agents/tools/generateurs/generateurs-ligne/generateurs-ligne.py` |
| Outil bash | `agents/tools/generateurs/generateurs-ligne/generateurs-ligne.sh` |
| Documentation | `agents/tools/generateurs/generateurs-ligne/generateurs-ligne.md` |
| Gabarits (configs) | `agents/tools/generateurs/generateurs-ligne/gabarits-ligne.json` |
| Spec (ce document) | `agents/tools/generateurs/generateurs-ligne/spec/spec-generateurs-ligne.001.01.ebauche.md` |
| Catalogue | `agents/tools/generateurs/generateurs-commande/catalogue-commandes.json` |
| Index | `agents/tools/index-tools.md` |
