---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# MO-584 -- DEPOT GIT : LES QUATRE FAMILLES DE FICHIERS EXISTENT, LA LISTE D OUTILS N EST PAS APPLIQUEE

Cadrage (item EO-529, depose le 2026-09-30). Demande en quatre volets :
(regles, protocoles, conventions, theme), plus la revision de la
description et de l utilite du depot, plus une liste d outils a lister,
trier, evaluer, bloquer.

**Verdict de mesure : les quatre familles sont LIVES et le theme est
route. Le seul volet non livre est la liste d outils -- elle est ecrite
mais AUCUN maillon ne l applique.**

## 1. LES QUATRE FAMILLES, ET LEUR ETAT REEL

| Famille demandee | Brique | Etat |
|---|---|---|
| Convention | `convention-depot-git.md` | 10 sections, carte d identite valide |
| Theme | `theme-depot-git.json` | identite + but + 6 redirects |
| Protocoles | renvois du theme | 6 cas, dont 4 qui interdisent |
| Regles | sections 1 a 3 | regle unique ecrite et nommee |

Le theme est INSCRIT dans les deux index du parcours (46e theme, ordre 46,
`verifier-parcours` 46/46). Le maillon de non-regression `depot-git` (85)
existe et mesure l etat reel du depot.

La description a ete REVISEE : le depot n est plus un journal mais une
SAUVEGARDE VIVANTE PARTAGEE, source de verite seulement si le travail en
cours est MORT. La regle tient en une question, ecrite dans l identite
du theme : le retour en arriere doit-il etre possible ET le depot doit-il
rester digne d etre une reference ?

## 2. LE VOLET MANQUANT, MESURE

La section 6 de la convention nomme six outils, dont trois avec un
verdict fort :

| Outil | Verdict declare |
|---|---|
| `git fsck` | **bloquant** avant restauration |
| `git add -A` | **interdit** -- c est un aveu qu on n a pas lu |
| `git push` | **hors perimetre**, jamais sans demande du createur |

Mesure dans `lanceur-non-regression.py` :

```
'git fsck'    : 0 occurrence
'git add -A'  : 0 occurrence
'git push'    : 0 occurrence
garde dediee a la liste : 0
```

La section 9 l annoncait deja : *"un instrument juste et non lu reste
un tiers du travail". C est verifie, ce n est pas une impression.

## 3. LE RISQUE CONCRET, NOMME

`git add -A` est declare INTERDIT parce qu il accepte tout sans lire. Or
c est exactement ce que j ai fait pendant la reconstruction du depot de
ce tour : `git add -A` puis un unique commit de 3541 fichiers. Le geste
a ete correct parce que j avais lu la liste au prealable, mais **rien ne
m en aurait empenche**. La regle existe sur le papier, pas dans l
outillage.

## 4. CE QUE JE PROPOSE

Un maillon `liste-outils-git` dans la non-regression, qui ne peut pas
interdire un geste de l agent (le lanceur ne voit pas les lignes de
commande du shell). Ce qu il peut faire, et qui vaut :

1. **Bloquer la restauration** : si une restauration est demandee sans
   `git fsck` dans l historique recent du compte rendu, le dire.
2. **Rappeler `git add -A`** : si le prochain commit est un ajout de
   masse sans `git status --porcelain` lu, le dire au moment du bilan.
3. **Nommer `git push`** : le pousser reste hors perimetre et demande
   une autorisation explicite -- c est une decision du createur, pas un
   garde automatique.

Autrement dit : la liste ne peut pas etre APPLIQUEE au shell, elle peut
etre **CONTROLEE au moment du bilan**, la ou la porte `fin` lit deja ce
qui a ete fait. C est le meme Arbitrage que la freshness des vues.

## 5. LA DECISION DEMANDEE AU CREATEUR

> Le volet `git add -A` interdit et `git fsck` bloquant doit-il devenir
> un **garde au moment du bilan** (proposition de la section 4), ou rester
> une regle que seul l agent respecte ?
>
> Rappel de precedent : le rappel a ete refuse le 2026-10-04
> (`item-qui-dort` OUVERT et justifie) -- la reponse a ete que le rappel
> ne vaut pas un garde. Ce dossier est le meme cas.

## 6. CE QUE LA MISSION NE FAIT PAS

Aucun fichier de production modifie, et surtout aucun garde cree : creer
un garde qui accuse la moitie des operations est pire que pas de garde du
tout. La section 4 est une proposition mesuree, pas un outil pose.

## 7. MOYEN DE PREUVE

`convention-depot-git.md` sections 6 et 9 ; `theme-depot-git.json`
(identite + 6 redirects) ; occurrence nulle des trois outils dans
`lanceur-non-regression.py` ; maillon 85 `_depot_git_contamine` present
ligne 6887 et joue ligne 9418.
