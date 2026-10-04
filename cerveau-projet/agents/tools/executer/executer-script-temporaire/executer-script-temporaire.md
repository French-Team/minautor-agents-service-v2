# executer-script-temporaire

**Categorie** : Executer
**Version** : 0.1.3
**Statut** : ebauche
**Agent** : Cerberus
**Date** : 2026-08-14

**ENTONNOIR** : point d entree unique pour l execution des scripts
temporaires. Quand un agent ecrit un script (`tmp-<agent>/<script>.py`), il le
passe par l entonnoir au lieu de lancer `python3` directement. L entonnoir
**normalise automatiquement** (BOM retire, CRLF -> LF, accents corriges via le
dictionnaire de `corriger-dictionnaire-accents`), **controle systematiquement**
(compilation Python) puis **execute** le script. Tout est **transparent pour
l agent** : il n a pas a penser a la conformite, l entonnoir fait le reste.

---

## Objectif

La boucle ideale du fichier temporaire (demande utilisateur) :
`creer -> entonnoir -> executer`. Un agent ecrit un script avec des accents,
des retours Windows, un BOM : au lieu de le corriger a la main ou de lancer un
script non conforme, il passe par l entonnoir qui le normalise, verifie la
syntaxe et l execute. Si le script est deja conforme, l entonnoir l execute
tel quel (0 modification). La regle : **on ne change pas le comportement de
l agent, on adapte le parcours** - le passage par l entonnoir devient le
chemin naturel.

## Utilisation

```bash
# Executer un script temporaire (normalisation + controle + execution)
python3 executer-script-temporaire.py tmp-<agent>/mon-script.py

# Avec arguments passes au script
python3 executer-script-temporaire.py tmp-<agent>/mon-script.py --arg1 val1

# Verifier sans rien modifier ni executer (normalisation en dry-run)
python3 executer-script-temporaire.py --dry-run tmp-<agent>/mon-script.py

# Dictionnaire alternatif + verbose
python3 executer-script-temporaire.py --dictionnaire <chemin> --verbose tmp-<agent>/mon-script.py

# Chrono (duree totale)
python3 executer-script-temporaire.py --chrono tmp-<agent>/mon-script.py

# Version
python3 executer-script-temporaire.py --version
```

## Etapes (le parcours de l entonnoir)

| Etape | Action | Sortie |
|---|---|---|
| 1. **NORMALISER** | BOM retire, CRLF -> LF, accents corriges via dictionnaire | Rapport des corrections (ou CONFORME si 0) |
| 2. **CONTROLER** | Compilation Python (`py_compile`) | CONTROLE OK / CONTROLE KO (blocage) |
| 2b. **CONTROLER TRIPLET** | Presence du triplet (protections `--dry-run`, options `--isoler`/`--desactiver`, chrono `--no-chrono`/`chrono_etape`/`bilan_chrono`) | `[TRIPLET] WARNING` (regle immuable v0.2.6) |
| 3. **EXECUTER** | Lancement du script avec ses arguments | Code retour du script |

En `--dry-run`, les etapes 1-2 sont realisees mais rien n est ecrit ni execute.

## Controle systematique

- **Compilation** : un script avec une erreur de syntaxe est **bloque** avant
  toute execution (CONTROLE KO, code retour 1) - l agent ne lance jamais un
  script qui ne compile pas.
- **Encodage non UTF-8** : un fichier non decodable est refuse avec un message
  clair.
- **Caracteres non couverts** : les caracteres non-ASCII non presents dans le
  dictionnaire sont signales en ATTENTION (jamais bloquants, l outil corrige
  ce qu il peut).

## Exemples

**Exemple 1 - script conforme** :
```
$ python3 executer-script-temporaire.py tmp-buffy/analyse.py
[ENTONNOIR] tmp-buffy/analyse.py
[CONFORME] script deja normalise (0 modification)
[CONTROLE OK] compilation valide
<sortie du script>
```

**Exemple 2 - script corrompu (BOM + CRLF + accents)** :
```
$ python3 executer-script-temporaire.py tmp-buffy/analyse.py
[ENTONNOIR] tmp-buffy/analyse.py
[BOM] BOM UTF-8 retire
[CRLF] 2 CRLF -> LF
[ACCENTS] 4 accents/caracteres corriges via dictionnaire
[ECRIT] fichier re-ecrit normalise
[CONTROLE OK] compilation valide
<sortie du script>
```

**Exemple 3 - erreur de syntaxe (blocage)** :
```
$ python3 executer-script-temporaire.py tmp-buffy/ko.py
[ENTONNOIR] tmp-buffy/ko.py
[CONTROLE KO] erreur de syntaxe - execution bloquee
SyntaxError: invalid syntax
(exit 1 - rien n est execute)
```

## Protection de sortie LF (v0.1.1)

> **REGLE** : l entonnoir ne normalise pas seulement le script AVANT
execution : apres l execution, il **re-scanne les fichiers du projet modifies
pendant la fenetre d execution** (mtime >= depart) et les re-normalise
(CRLF -> LF, BOM, accents).
>
> **Cause racine (lecon 2026-08-15)** : un append direct dans un script
temporaire (`io.open(f, "a")` sans `newline=""`) traduit LF en CRLF sur
Windows - l outil du projet `ajouter-contenu-fichier` est protege
(`newline=""`) mais les scripts temp ne l etaient pas. Cette protection
ferme la boucle : meme si un script ecrit des CRLF, le fichier cible est
re-normalise en LF pur des la fin de l execution.
>
> Exemple de sortie : `[SORTIE-LF] 1 fichier(s) re-normalise(s) en LF pur`.

## Pieges

1. **Dictionnaire** : l outil utilise par defaut le dictionnaire de
   `corriger-dictionnaire-accents` (fichier volontairement non-ASCII, exclu
   des controles de conformite). Ne pas le purger.
2. **Le script est modifie sur disque** : apres le passage dans l entonnoir,
   le script est re-ecrit normalise (ASCII + LF). C est voulu : le fichier
   devient conforme pour toute utilisation ulterieure.
3. **Timeout** : l execution est limitee a 600s (protection anti-blocage).

## Liens

- [corriger-dictionnaire-accents](../../corriger/corriger-dictionnaire-accents/corriger-dictionnaire-accents.md)
- [protocole-creation-scripts-temporaires](../../../regles-immuables/general/protocole-creation-scripts-temporaires/protocole-creation-scripts-temporaires.001.01.ebauche.md)
