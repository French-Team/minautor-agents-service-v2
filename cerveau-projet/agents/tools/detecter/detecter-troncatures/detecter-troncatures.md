---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# detecter-troncatures

**Version :** 0.2.0
**Statut :** ebauche
**Categorie :** detecter
**Chemin :** `agents/tools/detecter/detecter-troncatures/`
**Proprietaire :** Vulcain (outil partage)

## Description

Detecte les elements TRONQUES donc ILLISIBLES au final (demande
utilisateur 2026-08-16, round d amelioration 2026-08-16). Un contenu
tronque est un contenu qu un lecteur (agent LLM, outil, humain) ne peut
pas lire integralement : il devient partiellement illisible et source
d erreurs silencieuses.

Trois types de detection :

| Type | Quoi | Pourquoi c est illisible |
|---|---|---|
| `FICHIER_TROUQUE` | Fichier depassant un seuil de lignes lisible en une lecture (defaut 2000) | Les lecteurs tronquent au-dela : le contenu final est perdu |
| `BLOC_NON_FERME` | Bloc de code markdown non ferme (backticks impairs) OU structure invalide (JSON ne parse pas, Python ne compile pas, bash -n KO) | Un fichier coupe en plein milieu ne se lit pas : le reste est interprete faussement |
| `MARQUEUR_TRONCATURE` | Marqueurs litteraux de coupure dans le CONTENU reel (`[tronque]`, `[cut]`, `[truncated]`, 'coupe ici', 'contenu tronque') | Signe d un contenu coupe volontairement ou accidentellement |

## Pourquoi cet outil ?

- Les fichiers de corrections des agents grossissent (12 depassent deja
  2000 lignes) : ils sont tronques par les lecteurs LLM et deviennent
  partiellement illisibles.
- Les fichiers JSON/Python/bash coupes en plein milieu echouent de facon
  silencieuse (JSON invalide, syntaxe cassee) : les detecter avant qu un
  outil ne les lise evite les erreurs en cascade.
- Completer `detecter-surcharge-fichier` (qui ne couvre que la taille en
  lignes des .md) par une detection structurelle et de marqueurs.

## Utilisation

### CLI Python

```
python3 detecter-troncatures.py [OPTIONS] <fichier|dossier> [autres...]
python3 detecter-troncatures.py --tous
python3 detecter-troncatures.py --tous --exclure snapshots --exclure rapports
python3 detecter-troncatures.py --tous --rapport rapport.md --verbose

Options :
  --tous              Scanne tous les fichiers de cerveau-projet/
  --seuil-lignes <n>  Seuil de lignes pour FICHIER_TROUQUE (defaut 2000)
  --exclure <motif>   Exclut les chemins contenant le motif (repeteble)
  --rapport <fichier> Ecrit le rapport markdown
  --verbose           Detail des detections
  --version           Afficher la version
```

### CLI bash

```
detecter-troncatures.sh [OPTIONS] <fichier|dossier>
detecter-troncatures.sh --tous
detecter-troncatures.sh --tous --exclure snapshots
```

## Exemples

```
# Un fichier sain : rien a signaler
python3 detecter-troncatures.py mon-fichier.md
# Verdict global : PROPRE

# Scanner tout le projet
python3 detecter-troncatures.py --tous
# Verdict global : 13 PROBLEME(S) DE TRONCATURE DETECTE(S)

# Exclure les snapshots Hygie (volumineux mais attendus)
python3 detecter-troncatures.py --tous --exclure snapshots

# Abaisser le seuil pour une revue stricte
python3 detecter-troncatures.py corrections.md --seuil-lignes 500
```

## Sortie

Par fichier : liste des problemes classes par type + compteur + verdict
final (0 probleme = PROPRE, sinon PROBLEME(S) DE TRONCATURE avec nombre) +
resume global. Le rapport `--rapport` produit un markdown complet avec la
date, le nombre de fichiers analyses et le detail par fichier.

## Faux positifs maitrises (v0.2.0)

- **Binaires** : un fichier binaire (octets NUL dans les premiers octets,
  ex : image) n a pas de lignes lisibles -> il n est PAS compte
  FICHIER_TROUQUE (avant v0.2.0, une image de 2613 octets devenait
  '2613 lignes' : faux positif massif).
- **Zones de documentation** : les marqueurs CITES dans une docstring
  Python, un bloc de code markdown, un commentaire, une citation entre
  guillemets, ou une ligne qui documente le motif (lecon, doc de test,
  spec de l outil) ne sont PAS des troncatures. Documenter un marqueur
  n est pas etre tronque : le garde-fou test-077 et les lecons
  corrections.md ne sont plus auto-detectes.
- **Ellipses** : les points de suspension de 3 points en fin de phrase
  (`...`) ne sont PAS des marqueurs ; seuls les marqueurs entre crochets,
  phrases claires ou suites de 6+ points sont signales.

## Performance (v0.2.0)

Le scan `--tous` (976 fichiers, dont ~134 verifications bash -n) est
parallellise (ThreadPoolExecutor, 16 workers) : ~3.7s en v0.1.0 -> ~2.7s
en v0.2.0. Le plafond restant est le CPU-bound (json.loads / compile)
serialise par le GIL : les verifications bash -n (sous-processus) se
parallellisent, pas le parsing JSON/Python.

## Exclusions

- `__pycache__`, `.git`, `node_modules`, `.backup`, `.agents`
- Le dossier de l outil lui-meme (son en-tete et sa doc documentent les
  motifs de marqueurs : auto-detection parasite)
- `--exclure <motif>` : exclusions utilisateur repeteble en plus des
  exclusions par defaut

## Versionning

| Version | Date | Changements |
|---|---|---|
| 0.2.0 | 2026-08-16 | Round amelioration : binaires ignores (FICHIER_TROUQUE), option --exclure, marqueurs des zones de documentation ignores (docstrings/blocs code/commentaires/citations), analyse parallele (16 workers, 3.7s -> 2.7s) |
| 0.1.0 | 2026-08-16 | Creation : FICHIER_TROUQUE (seuil lignes), BLOC_NON_FERME (backticks + JSON/Python/bash structurels), MARQUEUR_TRONCATURE (crochets + phrases + 6+ points) |
