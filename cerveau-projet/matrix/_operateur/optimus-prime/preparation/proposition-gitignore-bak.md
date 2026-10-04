---
identite:
  type: fiche
  appartient_a: operateur
  commun: false
  version: 1
  date: 2026-10-02
  statut: a-jour
  tags: MO-544,gitignore,bak,perimetre
---

# Proposition : arreter de committer les points de restauration

Mission **MO-544**, 2026-10-02. Ce texte est **livre, pas ecrit** : le
`.gitignore` est a la racine du workspace, hors du perimetre d ecriture de la
Matrice (la porte ECRIRE le refuse, code 2, comme elle refuse `docs/`). Meme
regle que pour les sources : la Matrice livre le texte, le createur le pose.

## 1. LE TEXTE A AJOUTER

A la fin du `.gitignore` existant (`Z:\analiste-in-console\.gitignore`) :

```
# Points de restauration (.bak) : ils servent au moment du changement, puis
# deviennent du bruit. Regle MO-544 : on garde les 5 derniers par fichier
# (outil purge-points-restoration) et on ne les commite plus.
*.bak
*.bak.*
```

## 2. CE QUE CELA CHANGE, ET CE QUE CELA NE CHANGE PAS

- Les **nouveaux** points de restauration : desormais absents de l index, donc
  absents des commits. C est le benefice principal.
- Les **548 points deja suivis** : un `.gitignore` ne de-suivit rien. Ils
  resteront dans l index tant qu on ne les aura pas explicitement-retires.
- Les **362 fantomes** (suivis par git, absents du disque) : ils ne
  disparaitront pas d eux-memes non plus. Ils sont la graisse la plus visible.

## 3. LA COMMANDE A JOUER PAR LE CREATEUR

Elle ne supprime aucun fichier du disque : elle retire des chemins de l index
(les fichiers restant exactement la ou ils sont).

```
git rm --cached -q -r --ignore-unmatch "*/*.bak" "*/*.bak.*" "*.bak" "*.bak.*"
```

ou, pour etre explicite sur le perimetre mesure (la Matrice seule) :

```
git rm --cached -q -r --ignore-unmatch "cerveau-projet/matrix/**/*.bak" "cerveau-projet/matrix/**/*.bak.*"
```

Apres verification (`git status` doit montrer uniquement des suppressions
preparees), le createur decide du commit.

## 4. LE CONTRE-TEMOIN

Les motifs `*.bak` et `*.bak.*` sont volontairement larges : ils ne distinguent
pas un point de restauration d un fichier ordinaire nomme `donnees.bak`. C est
acceptable ici -- un `.bak` n a pas a etre distingue, un fichier ordinaire qui
porterait ce nom serait lui-meme un point de restauration mal nomme. En
revanche, l outil `purge-points-restoration` lui EST calibre : il n efface que
les noms `fichier.bak.<horodatage>` (auto-test : quatre noms qui ne sont pas des
points de restauration sont epargnes).
