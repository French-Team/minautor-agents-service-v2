---
identite:
  type: spec
  appartient_a: commun
  commun: true
---
# Spec -- Evaluer-progression (evaluer la progression et l evolution du cerveau-projet)

**Version** : 0.1.0
**Statut** : ebauche
**Date creation** : 2026-08-19
**Agent** : Vulcain (creation)
**Historique** : v0.1.0 (creation, 2026-08-19)

---

## Objectif

Creer un outil qui evalue la **progression** et l'**evolution** du
cerveau-projet en temps reel :
1. **Progression en temps reel** : lire les registres et sources de verite
   reelles a chaque execution, sans snapshot ni cache.
2. **Criteres definissables** : un fichier JSON de criteres mesure la
   progression jusqu a **100%** (cible = la valeur qui vaut 100%, poids =
   ponderation dans le score global).
3. **Auto-amelioration en %** : score de la vitesse d amelioration entre
   deux fenetres de temps (recente vs precedente). **NON PLAFONNE** : une
   croissance qui s accelere est autorisee a devenir exponentielle (score
   > 100%).

## Pourquoi cet outil ?

| Probleme | Solution |
|---|---|
| On ne sait pas objectivement ou en est le projet | Progression globale en % calculee sur des sources reelles |
| Les criteres de succes ne sont pas definissables | Fichier JSON de criteres : cible + poids + source, libre a l utilisateur |
| On ne mesure pas si le projet s ameliore avec le temps | Score d auto-amelioration (% de vitesse entre 2 fenetres) |
| La croissance acceleree doit etre visible, pas ecrasee | Score non plafonne (exponentiel autorise) |

## Vue d'ensemble

```
sources de verite reelles (catalogue-commandes.json, lecons.db,
registre-tests.jsonl, chronos.jsonl, agents/*.md)
        |
        v
evaluer-progression.py (lecture seule)
        |  1. progression : criteres (fichier JSON) -> % par critere, global
        |  2. auto-amelioration : 2 fenetres -> score % non plafonne
        v
rapport console (+ --rapport <chemin absolu> markdown optionnel)
```

## Interface CLI

```
evaluer-progression.py [options]
  --criteres <chemin>        Fichier de criteres JSON (defaut : progression-criteres.json a cote de l outil)
  --rapport <chemin>         Chemin ABSOLU d un rapport markdown (defaut : RIEN n est ecrit)
  --dry-run                  Simuler sans ecrire le rapport
  --verbose                  Afficher les details (sources mesurees, calculs)
  --version                  Afficher la version
  --chrono                   Mesurer la duree d execution
  --doc / --confirme-doc     Documentation obligatoire (regle immuable)
```

Parite py/sh : le .sh est un wrapper pur (`exec python3 "$PY_SCRIPT" "$@"`) --
aucune divergence de logique possible entre les 2 versions.

## Exigences Fonctionnelles

### 3.1 Exigence 01 -- Criteres definissables

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Un fichier JSON liste les criteres : id, nom, source, cible (la valeur qui vaut 100%), poids (ponderation). L utilisateur le cree/adapte librement avec `--criteres`. |
| **Critere d'acceptation** | Un critere avec une cible et un poids produit un % = min(100, valeur_reelle/cible*100). La progression globale est la moyenne ponderee. |
| **Dependances** | - |

### 3.2 Exigence 02 -- Sources de verite reelles

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Chaque source lit un registre reel : catalogue (nombre de commandes), lecons (compte lecons.db), tests_ok (% OK du dernier run), missions (chronos termines), agents (fiches agents). |
| **Critere d'acceptation** | Chaque source retourne la valeur reelle du moment (temps reel) ; une source absente retourne 0 sans erreur. |
| **Dependances** | - |

### 3.3 Exigence 03 -- Auto-amelioration en % non plafonnee

| Champ | Description |
|---|---|
| **Priorite** | Haute |
| **Description** | Pour chaque indicateur (usages, lecons, tests par jour), comparer le taux des derniers N jours au taux des N jours precedents. Score = 100 * taux_recent / taux_precedent (base <= 0 : 100 si recent nul, sinon 100 + 100*taux_recent). Score global = moyenne ponderee. NON PLAFONNE : > 100% autorise (exponentiel). |
| **Critere d'acceptation** | Une activite acceleree produit un score > 100%. A activite stable, score ~100%. |
| **Dependances** | - |

### 3.4 Exigence 04 -- Lecture seule + rapport optionnel

| Champ | Description |
|---|---|
| **Priorite** | Moyenne |
| **Description** | L outil n ecrit JAMAIS dans les registres. Seul `--rapport <chemin ABSOLU>` ecrit un rapport markdown. Sans `--rapport`, rien n est ecrit. |
| **Critere d'acceptation** | Sans `--rapport`, aucun fichier cree (lecon sortie-rapport-racine). Le rapport n est ecrit qu avec un chemin absolu. |
| **Dependances** | - |

## Exigences Non-Fonctionnelles

| Categorie | Exigence | Critere de mesure |
|---|---|---|
| **Portabilite** | 100% stdlib Python, ASCII strict, LF pur | py_compile OK, valider-conformite-ascii 0, normes 0/0 |
| **Robustesse** | Sources absentes ou JSON invalides -> 0 ou message clair, jamais de traceback brut | Tests manuels des cas absents |
| **Maintenabilite** | Criteres et indicateurs documentes dans le .md | Doc a jour avec le .py |
| **Secheresse** | Un nouvel outil = +1 catalogue (0.2.16) = pins tests | Compteurs catalogue/index testes par Morpheus |

## Architecture / Structure Technique

### 5.1 Vue d'ensemble

```
evaluer/evaluer-progression/
|-- evaluer-progression.py      # logique principale (lecture seule)
|-- evaluer-progression.sh      # wrapper pur -> .py (parite)
|-- evaluer-progression.md      # documentation du contrat
|-- progression-criteres.json   # criteres par defaut (source de verite des cibles)
```

### 5.2 Composants

| Composant | Role | Dependances |
|---|---|---|
| charger_criteres | Lit le JSON de criteres (defaut ou --criteres) | io, json |
| valeur_critere | Commute le calcul par source | registres reels |
| calculer_auto_amelioration | 2 fenetres -> score % non plafonne | dates_depuis, taux_par_jour |
| ecrire_rapport | Ecrit le rapport markdown (chemin absolu) | io |

### 5.4 Flux / Workflows

1. Lire les criteres (JSON).
2. Pour chaque critere : lire la source reelle, calculer le % de progression.
3. Calculer la progression globale (moyenne ponderee).
4. Pour chaque indicateur : lire les dates des evenements, decouper en 2 fenetres,
   calculer le taux par jour, le score (non plafonne) et la moyenne ponderee.
5. Afficher le rapport (console) ; ecrire le rapport markdown si `--rapport`.

## Contraintes et Risques

### 6.1 Contraintes

| Contrainte | Impact | Mitigation |
|---|---|---|
| Registres JSONL/JSON non tries ou date manquante | Faux taux | Filtre de dates (10 premiers caracteres) + comparaison par chaine YYYY-MM-DD |
| lecture seule | Aucune auto-journalisation | Ne pas appeler enregistrer-usage-outil pour ce type d outil |
| Chemin relatif de --rapport | Fichier egare | Exiger un chemin ABSOLU + os.makedirs sur le dossier |

## Livrables attendus

| Livrable | Format | Destination |
|---|---|---|
| Code Python | `.py` | agents/tools/evaluer/evaluer-progression/ |
| Wrapper bash | `.sh` | idem |
| Documentation | `.md` | idem |
| Criteres par defaut | `.json` | idem |
| Entree catalogue | `.json` | catalogue-commandes.json (0.2.16) |
| Entree index-tools | `.md` | index-tools.md (Evaluer 7, Total 204) |

## Plan de validation

### 8.1 Criteres de succes globaux

- [ ] Progression globale calculee (moyenne ponderee des criteres, plafonne a 100% par critere)
- [ ] Auto-amelioration > 100% quand l activite s accelere
- [ ] Aucun registre modifie ; rapport ecrit seulement avec un chemin absolu
- [ ] py_compile OK, ASCII 0, LF pur, `.sh` wrapper parite, catalogue trie, index a jour

### 8.3 Responsables

| Role | Responsable |
|---|---|
| Redaction | Vulcain (creation) |
| Validation technique | Morpheus (tests dedies) |
| Validation controlee | Janus (non-regression) |

## Liens et References

### 9.4 Regles immuables

- Protocole-outils (protections, --dry-run, --doc/--confirme-doc)
- Convention outil (prefixe dossier `evaluer-`, ASCII, LF)

## Historique des modifications

| Date | Version | Auteur | Description |
|---|---|---|---|
| 2026-08-19 | v0.1.0 | Vulcain | Creation de la spec (progression temps reel + auto-amelioration non plafonnee) |