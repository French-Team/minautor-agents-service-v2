---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# evaluer-progression

**Categorie** : Evaluer
**Version** : 0.1.0
**Statut** : ebauche
**Chemin** : `agents/tools/evaluer/evaluer-progression/`
**Proprietaire** : Vulcain (constructeur d'outils)

---

## Description

Evalue la **progression** du cerveau-projet en temps reel et son **evolution** :

1. **PROGRESSION jusqu a 100%** : un ensemble de **criteres definissables**
   (fichier JSON `progression-criteres.json`) mesure chacun la progression
   d un axe du projet (outils, lecons, tests verts, missions, agents).
   Chaque critere porte sa **source de verite reelle**, une **cible** (la
   valeur qui vaut 100%) et un **poids** dans la progression globale.
2. **AUTO-AMELIORATION en %** : la vitesse d amelioration est comparee entre
   **deux fenetres de temps** (les derniers N jours vs les N precedents) pour
   les indicateurs d activite (usages d outils, lecons, tests). Le score est
   **NON PLAFONNE** : une croissance qui s accelere peut depasser 100%, donc
   devenir exponentielle.

L outil lit les registres **en temps reel** a chaque execution : le rapport
reflete toujours l etat actuel du projet. Il est **lecture seule** (aucune
ecriture sauf un rapport explicitement demande avec `--rapport`).

---

## Utilisation

```bash
# Evaluation complete (progression + auto-amelioration)
python3 evaluer-progression.py --confirme-doc

# Avec un fichier de criteres personnalise
python3 evaluer-progression.py --criteres mon-fichier.json --confirme-doc

# Ecrire un rapport markdown (chemin ABSOLU obligatoire, jamais la racine)
python3 evaluer-progression.py --rapport C:/chemin/absolu/rapport.md --confirme-doc

# Simuler sans ecrire le rapport
python3 evaluer-progression.py --dry-run

# Afficher la documentation
python3 evaluer-progression.py --doc

# Afficher la version
python3 evaluer-progression.py --version
```

## Options

| Option | Description |
|---|---|
| `--criteres <chemin>` | Fichier de criteres JSON (defaut : `progression-criteres.json` a cote de l outil) |
| `--rapport <chemin>` | Chemin ABSOLU d un rapport markdown a ecrire (defaut : rien n est ecrit) |
| `--dry-run` | Simuler sans ecrire le rapport |
| `--verbose` | Afficher les details (sources mesurees, calculs) |
| `--version` | Afficher la version |
| `--chrono` | Mesurer la duree d execution de l outil lui-meme |
| `--doc` | Afficher le .md complet et sortir |
| `--confirme-doc` | Confirmer la lecture de la doc (requis en mode reel) |

---

## Fichier de criteres (`progression-criteres.json`)

Chaque critere de la liste `criteres` a la structure suivante :

| Champ | Type | Role |
|---|---|---|
| `id` | texte | Identifiant unique du critere |
| `nom` | texte | Nom lisible du critere |
| `source` | texte | Source de verite reelle (voir ci-dessous) |
| `cible` | nombre | La valeur qui represente **100%** pour ce critere |
| `poids` | nombre | Ponderation dans la progression globale (la somme des poids = 100) |
| `explicatif` | texte | Commentaire documentaire |

### Sources de verite reelles

| Source | Mesure reelle |
|---|---|
| `catalogue` | Nombre de commandes dans `catalogue-commandes.json` (les outils) |
| `lecons` | Nombre de lecons dans `lecons.db` (la capitalisation) |
| `tests_ok` | % de tests OK sur le run le plus recent de `registre-tests.jsonl` |
| `missions` | Nombre d interventions d agents terminees dans `chronos.jsonl` |
| `agents` | Nombre de fiches agents (`type: fiche-agent`) dans `agents/` |

### Indicateurs d auto-amelioration

La section `auto_amelioration` contient `fenetre_jours` (largeur des fenetres
de comparaison) et `indicateurs` :

| Indicateur | Source | Mesure |
|---|---|---|
| `usages_par_jour` | `registre-usages-outils.jsonl` | Usages d outils par jour |
| `lecons_par_jour` | `lecons.db` | Lecons enregistrees par jour |
| `tests_par_jour` | `registre-tests.jsonl` | Tests lances par jour |

Le score d un indicateur = `100 * taux_recent / taux_precedent`. Le score
global est la moyenne ponderee. **Non plafonne** : si l activite s accelere,
le score depasse 100% (croissance exponentielle autorisee).

---

## Sortie

```
=== evaluer-progression v0.1.0 ===
Objectif : ...

PROGRESSION :
<critere>                   <valeur>  <cible>  <Prog %>  <Poids>
outils                        185      200     92.5      20
...

PROGRESSION GLOBALE : XX.X %

AUTO-AMELIORATION (score % non plafonne) :
Fenetre : les derniers 7 jours vs les 7 jours precedents
<indicateur>   <taux precedent>  <taux recent>   <score %>

SCORE AUTO-AMELIORATION : XX.X %
  (score NON PLAFONNE : une croissance acceleree peut depasser 100%)
```

Code de retour : 0 en cas de succes, 1/2 en cas d erreur (fichier de criteres
absent, source inconnue, documentation manquante).

---

## Regles

1. **Lecture seule** : l outil ne modifie aucun registre, il les lit.
2. **`--rapport` exige un chemin ABSOLU** : JAMAIS un chemin relatif (lecon
   sortie-rapport-racine - rien ne sort de `cerveau-projet/` sans reflexe).
3. Le rapport ecrit se refere aux registres du moment de l execution (temps reel).
4. Les criteres sont **definissables** : le fichier JSON est la source de
   verite des cibles et des poids - l utilisateur le cree/adapte librement.

---

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.1.0 | 2026-08-19 | Creation : progression temps reel (criteres definissables /100) + auto-amelioration en % non plafonnee (croissance exponentielle permise). |

---

## Notes

- Outil **lecture seule** par conception : aucune auto-journalisation au
  registre-usages (comme surveiller-usages) - les registres lus sont la source.
- Voir aussi : `evaluer-processus` (derives de processus), `evaluer-rating`
  (note de qualite /100), `chronometrer-duree` (durees des interventions).