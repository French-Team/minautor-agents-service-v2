---
identite:
  type: convention
  appartient_a: optimus-prime
  commun: false
  liens:
    - _operateur/optimus-prime/parcours/themes/theme-depot-git.json
---

# La doctrine du depot git

> Demande createur **EO-529** (2026-09-30). Theme d execution :
> `parcours/themes/theme-depot-git.json`.
>
> Cette convention dit **quand** sauver et **quand refuser**. Elle ne dit pas
> comment git fonctionne -- elle dit ce que le depot doit signifier pour nous.

---

## 1. Ce que le depot est

Le depot git est une **sauvegarde vivante partagee**.

Ce n'est pas un cahier de route, ni un journal de bord, ni une archive du travail.
C'est l'etat du projet **au moment ou l on a decide qu il fallait pouvoir y revenir**.

Une source de verite n'est vraie que dans une seule condition :

> le travail en cours est **mort**, et il faut revenir a un etat fonctionnel.

Tant que le travail vit, le depot est un **outil de retour**, pas une reference.
Des qu il sert de reference, c'est qu il doit etre irrachepe.

---

## 2. La regle unique

**On sauvegarde AVANT un risque. Jamais APRES un doute.**

| | Quand | Pourquoi |
|---|---|---|
| **OUI** | Une mission **critique** commence | Garantir le retour juste avant |
| **NON** | Une mission se termine, non verifiee | Contamine la sauvegarde |

La ligne du bas est une **tres mauvaise pratique**, et c'est celle que nous avons
le plus employee : un commit de fin de mission y entre du travail qui peut encore
casser, et le depot cesse d etre un etat ou l on peut revenir.

Un depot contamine ne se rattrape pas. Il perd son sens, et personne ne peut plus
dire s il est vrai ou faux.

---

## 3. Ce qui rend une mission CRITIQUE

Le critere n est pas le nombre de fichiers. C'est le **risque couvert**.

**CRITIQUE** -- le commit est justifie par defaut :

- un fichier **partage** : convention, `cible.py`, une liste fermee, un routeur ;
- une **BDD** : une entree perdue ne se revoit pas ;
- une **porte d attribution** : elle decide ce qui est ecrit ;
- une **suppression d octets** : archive purgee, fichier retire ;
- une **migration** qui deplace des donnees.

**COURANT** -- le commit n est pas justifie :

- une note, un bilan, un segment de raisonnement ;
- une mesure, un rapport, un tableau de bord ;
- un fichier de travail jetable (`tmp-*/`) ;
- une trace de runtime qui change a chaque tour.

> L interet se mesure par le risque qu il couvre, jamais par le volume.
> Cent fichiers de mesure ne valent pas un fichier de convention.

---

## 4. Ce qui contamine le depot

Quatre familles, ecartees **par nom**, jamais en bloc :

1. **Les points de restauration `.bak.*`** -- ils doublent l historique sans le
   servir. Notre parc en compte plus d un millier de suivis par git : c est la
   contamination nommee par EO-529, et elle est **mesurable**.
2. **Les jetables** -- `tmp-*/`, zone jetable du round, `__pycache__`.
3. **Les traces de runtime** -- journaux, boites d intercom, registres d espions :
   elles changent a chaque tour, donc leur presence dans un commit n apprend rien.
4. **Les residus** -- ce que le maillon `residus` signale.

Ce qui reste : le **code livre**, les **BDD a sens**, les **conventions**, les
**docs de preuve**.

---

## 5. Ce que le commit doit dire

Le message dit le **pourquoi**. Le quoi est dans le diff.

Un message qui recite le diff a waste un voyage au depot.

```
MO-578 : les 98 archives ressuscitees ne pouvaient plus etre purgees
```

se relit dans six mois. `mise a jour de purge.py` ne se relit pas.

---

## 6. Les outils a lister, trier, evaluer, bloquer

| Outil | Role | Etat |
|---|---|---|
| `git status --porcelain` | lire l etat **avant** la mission | a utiliser |
| `git diff` | voir ce que le commit contient | a utiliser |
| `git log -1` | relire son propre message | a utiliser |
| `git fsck` | verifier que le depot est sain avant d y croire | **bloquant** avant restauration |
| `git add -A` | tout accepter sans lire | **bloquant** -- interdit |
| `git push` | publier ailleurs | **hors perimetre**, jamais sans demande du createur |

`git add -A` est **interdit** : c'est un aveu qu on n a pas lu la liste.

---

## 7. Les scenarios a couvrir

Le theme `theme-depot-git.json` porte six cas, dont quatre qui interdisent :

| Scenario | Verdict |
|---|---|
| Mission critique qui commence | **commiter avant**, pour pouvoir revenir |
| Mission terminee non verifiee | **ne pas commiter** -- deposer le constat en item |
| Fichiers de restauration `.bak.*` presents | **ecarter et nommer** chacun |
| restauration apres incident | **restaurer, puis prouver** que l outil reparle |

---

## 8. L evaluation de l interet

Une seule question, posee avant chaque commit :

> Le prochain geste peut-il casser le travail en cours ?

- **oui** -> on commit, pour garder le retour ;
- **non** -> on ne commit pas, et on ne laisse pas trainer une envie.

Un commit sans motif ecrit est un commit qui ne sera pas lu. La trace d une
decision de depot vaut autant que le depot lui-meme.

---

## 9. Ce qui reste ouvert, et dit

- La **liste des outils git** ci-dessus est une premiere version : elle dit ce qui
  est **bloquant** et ce qui ne l est pas, mais aucun maillon de la non-regression
  ne les applique encore. C'est le meme schema que le vice `or True` corrige le
  2026-10-03, et le meme que `nonsens_publies` : **un instrument juste et non lu
  reste un tiers du travail**.
- Les **points de restauration** deja suivis par git n'etaient PAS retires par
  cette convention : elle les nommait, elle ne les supprimait pas. Ils ont ete
  **desindexes** le 2026-10-04 (voir section 10) -- un acte reversible et trace,
  decide par le createur, qui n'a retire aucun octet.
- Le maillon `depot-git` (non-regression) applique desormais la famille
  **point de restauration** et la famille **jetable** : il mesure l etat reel du
  depot au lieu de le decrire. Tant que des points de restauration restent
  SUIVIS par git, il doit dire KO -- c'est un constat, pas une panne du maillon.

---

## 10. Ce qui a et fait le 2026-10-04 (MO-579)

La convention ne se contente pas de nommer : l etat a ete **ramene**.

| Geste | Effet |
|---|---|
| 697 points de restauration **desindexes** (`git rm --cached`) | 0 `.bak.` suivi par git |
| motif `*.bak.*` ajoute au `.gitignore` | les prochains n entrent plus |
| les 122 deja absents du disque | constates, pas rattappes |
| les 575 presents | **intacts sur le disque**, blobs vivants dans `HEAD` |

**Aucun octet n'a ete perdu.** Desindexer n'est pas supprimer : `git add <chemin>`
reindexe a la demande, et `git cat-file -e HEAD:<chemin>` retrouve le blob.

Ce qui n'a pas ete fait, et pourquoi : la porte `ecrire` continue de **produire**
ses points de restauration (c'est son filet de securite, il n'est pas en cause) --
seul git les ignore desormais. Desactiver ce filet pour rendre un depot propre
serait echanger une surete contre une estetique.
