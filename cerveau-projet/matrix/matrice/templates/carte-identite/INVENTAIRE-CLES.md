---
identite:
  type: readme
  appartient_a: matrice
  commun: true
  version: 1
  date: 2026-09-23
  statut: a-jour
  tags: carte-identite, inventaire, cles
  liens: matrice/templates/carte-identite/README.md
---

# Inventaire des cles de carte (mesure du 2026-09-23)

Cette annexe est la MESURE du modele. Elle est declaree des DEUX cotes avec la porte
du modele (`README.md`) : le lien va et vient, donc la routine
`verifier-liens-cartes` ne signale aucun `sans retour`. Une annexe que nul document
ne nomme serait un document orphelin -- et un orphelin ne se retrouve pas.

## L INVENTAIRE REEL DES CLES

Perimetre mesure : les **14 cartes de l arbre `matrice/`** (la zone de l operateur en
porte une centaine de plus ; la routine `verifier-liens-cartes` les compte toutes).

| cle | cartes | valeurs vues | obligatoire |
|---|---|---|---|
| `type` | 14/14 | `outil`, `readme`, `fiche` ... | **OUI** (vocabulaire FERME, 18 types) |
| `appartient_a` | 14/14 | `matrice`, `matrice-data-outils`, `matrice-routines` | **OUI** (un NOM, jamais un chemin) |
| `commun` | **8/14** | `true` | **OUI** |
| `version` | 13/14 | `1`, `1.0.0`, `1.2.0` | non |
| `liens` | 7/14 | chemins canoniques | non (c est une LISTE) |
| `date` | 6/14 | `2026-09-23` | non |
| `gravite` | 0/14 | `tres-urgent`, `urgent`, `important`, `normal`, `optionnel` | non (VALEUR fermee : EO-457) |
| `niveau` | 0/14 | `1` a `10` | non (VALEUR fermee : EO-457) |
| `flux`, `nom`, `palier` | 1/14 | -- | non (cles libres : c est le corpus qui fait foi) |

## LES TROIS PIEGES MESURES (et ce qui les empeche)

1. **six cartes sur quatorze n ont PAS `commun`** -- une cle OBLIGATOIRE absente, et
   rien ne s en plaint : le garde ne juge que la zone de l operateur. Une carte sans
   `commun` n est pas < moins complete > : elle est **hors contrat**, et le moteur ne
   peut pas repondre a un `--champ "commun=true"` sur elle.
2. **six `type` hors du vocabulaire ferme** : `outil-dialoguer`, `outil-executer`,
   `outil-maintenir`, `outil-signaler`, `routeur-maintenance`, `routine`. Un type neuf
   se **DECLARE** dans le domicile (`TYPES_RECONNUS`), il ne s invente pas dans une carte.
3. **`liens` n etait porte par AUCUNE carte** avant le 2026-09-23 (**0 sur 113**) : le
   mecanisme existait depuis EO-347 et personne ne s en servait. Un graphe vide ne se
   voit pas ; c est ce constat qui a fait naitre le modele et la routine.

## CE QUE LE MOTEUR PEUT CHERCHER, CLE PAR CLE

| recherche | comment | ce qu on obtient |
|---|---|---|
| par carte | `--champ "type=outil;appartient_a=matrice"` | les DOCUMENTS qui portent ces cles (valeur ENTIERE, sans casse) |
| par lien | `--lien matrice/data/commun/carte_identite.py` | les DOCUMENTS dont la carte DECLARE ce chemin (forme exacte ou fin de chemin) |
| par texte | `--requete <mot>` | les LIGNES (et les noms de fichiers) |
| zone privee | ajouter `--prive` | inclut les zones invisibles L-016 (`_operateur`, ...) |

Une cle a **VALEUR DE LISTE** (`liens`) ne se cherche PAS par `--champ` : comparer
`"a, b"` a `"a"` ne correspond jamais. C est exactement ce que `--lien` sert.

## LA REGLE DE L AUTEUR (en une ligne)

Trois cles obligatoires : `type` (vocabulaire ferme), `appartient_a` (un nom),
`commun` (vrai ou faux). Puis les cles libres qui disent quelque chose, puis les
`liens` -- un CHEMIN CANONIQUE, jamais un nom seul, declare des DEUX cotes.
