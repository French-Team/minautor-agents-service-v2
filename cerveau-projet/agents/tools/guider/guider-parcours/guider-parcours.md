# guider-parcours

| Champ | Valeur |
|---|---|
| **Version** | 0.2.10 |
| **Statut** | ebauche |
| **Categorie** | guider |
| **Derniere mise a jour** | 2026-08-08 |
| **Spec** | [spec-guider-parcours.001.01.ebauche.md](spec/spec-guider-parcours.001.01.ebauche.md) (v0.2.4) |

---

## Description

**Guide-Parcours (jeu de piste).** Fait avancer l'agent case par case dans un
parcours JSON : chaque case affiche la question + les indices (outil a lancer,
fichier a lire, regle a appliquer), et selon la reponse l'agent suit une
branche vers la case suivante. **L'agent ne lit plus rien d'avance** : il
recoit a chaque etape uniquement ce dont il a besoin, au bon moment.

C'est la reponse au probleme des fiches de 200+ lignes que les agents oublient
de relire : au lieu de memoriser tout avant d'agir, l'agent avance case par
case (1 case en main a chaque instant).

---

## Principe

```
demarrer.md (case 0 : point d'entree)
    |
    v
parcours-<agent>.json   (source de verite du guidage)
    |
    v
guider-parcours.py <parcours.json>
    |
    v
CASE N : question + indices (outil / fichier / regle / controle)
    |  reponse
    v
CASE N+1 : ... jusqu'a la case FIN
```

---

## Utilisation

### CLI Python (version 0.1.0-py)

```
python3 guider-parcours.py <parcours.json> [options]

Options :
  --case <id>       Demarrer a une case precise (ex: c3) au lieu de case_depart
  --reponses <liste> Fournir les reponses d'un coup (separees par |) : mode non-interactif
  --liste           Lister toutes les cases du parcours sans naviguer
  --version         Afficher la version
  --help            Afficher l'aide
```

### CLI bash (version 0.1.0-sh)

```
bash guider-parcours.sh <parcours.json> [options]
```

Memes options que la version Python.

---

## Format du parcours JSON

### Structure generale

```json
{
  "parcours": {
    "nom": "parcours-vulcain",
    "agent": "vulcain",
    "version": "0.1.0",
    "case_depart": "c1",
    "description": "..."
  },
  "cases": {
    "c1": { "titre": "...", "type": "question", "question": "...", "branches": [...] },
    "c2": { "titre": "...", "type": "indice", "indices": [...], "suivant": "c3" },
    "c9": { "titre": "FIN", "type": "fin" }
  }
}
```

### Types de cases

| Type | Comportement |
|---|---|
| `question` | Affiche la question + indices, attend une reponse, suit la branche |
| `indice` | Affiche les indices, sans question : passe automatiquement a `suivant` |
| `controle` | Affiche les indices + question de verification (OUI/NON), suit la branche |
| `fin` | Case terminale : le parcours est termine |

### Indices (tableau `indices`)

| Type | Cles | Role |
|---|---|---|
| `outil` | `nom`, `chemin`, `commande` | L'outil exact a lancer |
| `fichier` | `chemin`, `raison` | Le fichier/protocole a lire a cette etape |
| `regle` | `texte` | LA regle absolue pertinente pour cette case |

### Branches (tableau `branches`)

| Cle | Type | Role |
|---|---|---|
| `reponse` | texte | La reponse attendue (OUI, NON, ou choix exact) |
| `vers` | texte | La case suivante si cette reponse est donnee |

---

## Patterns (spec v0.2.0, v0.2.4)

Les 3 patterns suivants sont documentes dans la spec (v0.2.0 pour les 2 premiers,
v0.2.4 pour le Pattern 3) et sont OBLIGATOIRES pour tout nouveau parcours.
Verifier la conformite avec `--liste` + `--reponses`.

### Pattern 1 -- Multi-missions (une case Mission + chemins convergents)

Quand un agent a PLUSIEURS missions, le parcours demarre par une case `Mission`
(type question) dont chaque branche mene au chemin d'UNE mission. Les chemins
convergent ensuite vers des cases COMMUNES (verdict, lecons, retour) au lieu de
dupliquer ces cases dans chaque chemin.

**Exemple reel** : `agents/janus/parcours/parcours-janus.json` (30 cases,
3 chemins : outil / statut / modification).

### Pattern 2 -- Rappel ASCII obligatoire dans les cases d'ecriture

Toute case qui ECRIT dans un fichier (creer-fichier, ecrire-fichier,
editer-fichier, ajouter-contenu-fichier, rapport de controle, lecons) DOIT
porter en TETE de sa liste `indices` un indice `regle` qui rappelle la regle
ASCII (100%% ASCII, guillemets ASCII, jamais de guillemets francais). L'agent
le voit juste avant d'ecrire.

**Verification** : `grep 'REGLE IMMUABLE ASCII' <parcours.json>` couvre chaque
case d'ecriture du parcours.

### Pattern 3 -- Combo (generateur -> execution)

Une case de parcours peut pointer vers un **COMBO** au lieu d'enchainer une
suite d'outils. Le combo est un orchestrateur declaratif (`definition-combo.json`)
lu par `combos-moteur` (format documente dans
`agents/tools/combos/combos-moteur/spec/spec-combos-moteur.001.01.ebauche.md`).

Le principe du dataflow : chaque case `generateur` appelle
`generateurs-commande --reponses` (mode AUTO) pour composer la commande, la case
`outil` l'execute et stocke le resultat dans une variable, la case `controle`
decide si le resultat est transmis brut ou si un generateur s'intercale.

**Benefice** : parcours allege (1 case = 1 combo au lieu de 5-6 cases d'outils),
commande toujours validee par le generateur (modele du catalogue), l'agent lance
un combo et recupere le resultat final.

---

## Exemples

### Lister les cases d'un parcours

```bash
python3 guider-parcours.py agents/vulcain/parcours/parcours-vulcain.json --liste
```

### Naviguer en mode interactif

```bash
python3 guider-parcours.py agents/vulcain/parcours/parcours-vulcain.json
```

### Naviguer avec les reponses fournies d'un coup

```bash
python3 guider-parcours.py agents/vulcain/parcours/parcours-vulcain.json --reponses "construire|OUI|OUI"
```

### Demarrer a une case precise

```bash
python3 guider-parcours.py agents/vulcain/parcours/parcours-vulcain.json --case c5
```

---

## Sortie type d'une case

```
=== [c1/9] Mission ===

[REGLE]  REGLE ABSOLUE : verifier avant d'agir
[OUTIL]  verifier-systeme
         chemin: agents/tools/verifier/verifier-systeme/verifier-systeme.py
         > python3 agents/tools/verifier/verifier-systeme/verifier-systeme.py

QUESTION : Quelle est la mission ?
  [1] construire
  [2] modifier
```

---

## Emplacement des parcours

| Parcours | Chemin |
|---|---|
| Vulcain (constructeur) | `agents/vulcain/parcours/parcours-vulcain.json` |
| Morpheus (testeur) | `agents/morpheus/parcours/parcours-morpheus.json` |
| Clio (muse de l'histoire) | `agents/clio/parcours/parcours-clio.json` |
| Janus (controleur) | `agents/janus/parcours/parcours-janus.json` |
| Cerberus (coordinateur) | `agents/cerberus/parcours/parcours-cerberus.json` |
| Buffy (developpeur principal) | `agents/buffy/parcours/parcours-buffy.json` |
| Themis (evaluatrice croisee) | `agents/themis/parcours/parcours-themis.json` |
| Minerve (redactrice de todos) | `agents/minerve/parcours/parcours-minerve.json` |
| Promethee (redacteur de specs) | `agents/promethee/parcours/parcours-promethee.json` |
| Athena (redactrice de pense-betes) | `agents/athena/parcours/parcours-athena.json` |
| Atlas (explorateur et documentaliste) | `agents/atlas/parcours/parcours-atlas.json` |

Regle : un parcours par agent, dans le dossier de l'agent (`agents/<agent>/parcours/`).
`demarrer.md` est la case 0 commune a tous les parcours (point d'entree).

---

## Regles

1. Le JSON doit etre valide et ASCII strict
2. Toute branche doit pointer vers une case existante (valide a chaque lancement)
3. `demarrer.md` reste la case 0 : le parcours d'un agent demarre apres l'identification
4. Chaque mission de l'agent doit avoir un chemin de cases (couverture verifiable via --liste)
5. Toute case qui ECRIT dans un fichier porte un indice `regle` ASCII en tete de ses `indices` (Pattern 2)
6. Un parcours multi-missions demarre par une case `Mission` avec branches vers les chemins, convergeant vers les cases communes (Pattern 1)
7. AUTONOMIE DES PARCOURS (v0.2.2) : chaque parcours est un fichier INDIVIDUEL, la convergence est uniquement intra-parcours, aucun partage de cases entre parcours, chaque parcours est complet et validable independamment
8. Une case qui pointe vers un COMBO reference `combos-moteur` + la definition du combo (Pattern 3, v0.2.4) -- spec-combos-moteur documentee

---

## Versionning

| Version | Statut | Changements |
|---|---|---|
| 0.2.10 | ebauche | Doc : reference la spec v0.2.4 (Pattern 3 -- combo generateur -> execution) + regle 8 dans la section Regles |
| 0.2.9 | ebauche | Doc : reference la spec v0.2.3 (prototype vulcain documente comme cas legitime assume : fins independantes) |
| 0.2.8 | ebauche | Doc : reference la spec v0.2.2 (ajout de la regle d'autonomie des parcours) + regle 7 AUTONOMIE dans la section Regles |
| 0.2.7 | ebauche | Doc : reference la spec v0.2.1 (ajout de la procedure d'audit des 2 patterns, validee par l'audit des 11 parcours par Themis) |
| 0.2.6 | ebauche | Doc : liste des parcours completee -- ajout de atlas (explorateur et documentaliste) au tableau Emplacement des parcours (11 parcours) -- serie complete |
| 0.2.5 | ebauche | Doc : liste des parcours completee -- ajout de athena (redactrice de pense-betes) au tableau Emplacement des parcours (10 parcours) |
| 0.2.4 | ebauche | Doc : liste des parcours completee -- ajout de promethee (redacteur de specs) au tableau Emplacement des parcours (9 parcours) |
| 0.2.3 | ebauche | Doc : liste des parcours completee -- ajout de minerve (redactrice de todos) au tableau Emplacement des parcours (8 parcours) |
| 0.2.2 | ebauche | Doc : liste des parcours completee -- ajout de themis (evaluatrice croisee) au tableau Emplacement des parcours (7 parcours) |
| 0.2.1 | ebauche | Doc : liste des parcours completee -- ajout de cerberus (coordinateur) et buffy (developpeur principal) au tableau Emplacement des parcours (6 parcours) |
| 0.2.0 | ebauche | Doc : reference la spec v0.2.0, documente les 2 patterns (multi-missions + rappel ASCII obligatoire), liste a jour des parcours (vulcain, morpheus, clio, janus, cerberus, buffy, themis, minerve, promethee, athena) |
| 0.1.0 | ebauche | Creation : navigation case par case, indices (outil/fichier/regle), branches, modes --liste/--reponses/--case, parite py/sh, spec + parcours-vulcain prototype |
