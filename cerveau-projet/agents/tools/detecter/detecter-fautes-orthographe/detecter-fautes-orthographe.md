---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# detecter-fautes-orthographe

**Version :** 0.1.0
**Statut :** ebauche
**Categorie :** detecter
**Chemin :** `agents/tools/detecter/detecter-fautes-orthographe/`
**Proprietaire :** Hermes (outil partage)

---

## Objectif

Detecter les **fautes d'orthographe francaise** les plus courantes commises par
les agents dans les fichiers markdown du cerveau-projet (readme, regles,
protocols, fiches, parcours). C'est le chariot de l'agent **Hermes**, dedie au
vocabulaire et aux fautes.

**Pourquoi cet outil ?**
- Personne ne verifiait l'orthographe : Themis verifie la veracite, Hygie le
  nettoyage, mais les fautes de francais passaient inapercues (ex: la faute
  `enchannements` dans readme-dev, relevee par l'utilisateur le 2026-08-14)
- La regle-emojis-ascii impose le francais **ASCII pur** : les mots corrects
  sont ecrits sans accents (`probleme`, `etre`, `deja`). L outil connait cette
  convention : il ne signale que les fautes repertoriees, jamais les mots
  corrects en ASCII
- Le dictionnaire est extensible : ajouter une entree = elargir la couverture

---

## Utilisation

```bash
# Scanner tout le projet (cerveau-projet/ + readme a la racine)
python3 detecter-fautes-orthographe.py --tous

# Scanner un fichier ou un dossier
python3 detecter-fautes-orthographe.py --fichier <chemin>

# Ecrire un rapport markdown
python3 detecter-fautes-orthographe.py --tous --rapport <fichier>.md

# Lever les exclusions (corrections.md, tests/, rapports/)
python3 detecter-fautes-orthographe.py --tous --tout

# Version
python3 detecter-fautes-orthographe.py --version
```

---

## Parametres

| Parametre | Type | Obligatoire | Description |
|---|---|---|---|
| `--tous` | flag | Non | Scanner tout le projet (defaut si aucun chemin) |
| `--fichier <chemin>` | string | Non | Scanner un fichier ou un dossier precis |
| `--rapport <fichier>` | string | Non | Ecrire le rapport markdown |
| `--verbose` | flag | Non | Afficher le detail des fautes (ligne + contexte) |
| `--tout` | flag | Non | Lever les exclusions par defaut |
| `--version` | flag | Non | Afficher la version |

**Code de sortie** : `0` = 0 faute (OK), `1` = fautes detectees (KO),
`2` = erreur d utilisation.

---

## Exclusions par defaut

| Fichier/dossier | Raison |
|---|---|
| `corrections.md` | Lecons historiques citant d anciennes fautes |
| `tests/` | Les tests verifient des contenus (pas des textes rediges) |
| `rapports*/` et `rapport-*.md` | Documentent l historique |
| `snapshots/` | Etats captures, non rediges |
| `tmp-*/` | Scripts temporaires (deja surveilles par detecter-residus) |

---

## Dictionnaire

Les fautes sont classees par famille :

| Famille | Exemples (fautif -> correct) |
|---|---|
| Double consonne manquante | `apel` -> `appel`, `comande` -> `commande`, `mesage` -> `message` |
| Double consonne au mauvais endroit | `paralelle` -> `parallele`, `coriger` -> `corriger` |
| Lettre confondue | `existance` -> `existence`, `permanant` -> `permanent` |
| Lettre finale manquante | `toujour` -> `toujours`, `neamoins` -> `neanmoins` |
| Fautes relevees dans le projet | `enchannements` -> `enchainements`, `racourci` -> `raccourci` |

> **Regle** : un mot n est signale QUE s il figure dans le dictionnaire
> `FAUTES` de l outil. Les mots ASCII corrects (`probleme`, `parallele`,
> `developpement`, `existant`...) ne sont jamais signales.

---

## Exemple

```bash
python3 detecter-fautes-orthographe.py --fichier cerveau-projet/readme-dev.md
# KO : 1 faute(s) detectee(s) dans 1 fichier(s).
#   cerveau-projet/readme-dev.md : 1 faute(s)
#     L264 : 'enchannements' -> 'enchainements' | Les combos sont des **enchannements...
```

---

## Limites

- Detection par dictionnaire : ne couvre que les fautes **repertoriees**
- Pas de verification grammaticale (accords, conjugaisons)
- Ne signale pas les accents manquants (la regle ASCII les interdit de toute facon)
- L agent Hermes etend le dictionnaire au fil des fautes relevees (lecon dans
  corrections.md + entree FAUTES)

---

## Connexions

| Fichier | Role |
|---|---|
| `detecter-fautes-orthographe.py` | L outil (version Python) |
| `../index-tools.md` | Reference de l outil |
| `../../../../agents/hermes/hermes.md` | Agent proprietaire |
