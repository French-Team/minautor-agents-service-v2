---
identite:
  type: analyse
  appartient_a: operateur
  commun: false
  version: 1
  date: 2026-10-02
  statut: a-jour
  tags: MO-545,profil,user-profil,injection,question
---

# Le profil utilisateur voyage-t-il jusqu'a l'agent ?

Mission **MO-545** (ANALYSE / question, EO-506). Reponse mesuree le 2026-10-02.

## LA QUESTION

> est-ce que le pilote de optimus injecte les infos de 'user-profil.md' ?

## LA REPONSE, EN DEUX MOTS

**Oui, il les injecte. Non, l'agent ne les a pas sous les yeux.**

Les deux moities sont vraies, et les separer evite de se tromper dans les deux sens.

## 1. LE VOYAGE : IL EST FAIT, ET IL EST PROUVE

`verifier-profil-injection` (l'instrument dedie) rend **VERDICT OK** :

| Controle | Resultat |
|---|---|
| un seul domicile pour les champs attendus | 1 fichier |
| le profil est PESE avec le sac-a-dos | oui |
| deux chemins d'injection le portent | 2 |
| le plafond est DECLARE | 300 tokens |
| fiche reelle | 8 champs injectes sur 8 attendus, complet |
| rien dans l'ombre | chaque champ attendu est injecte, dit ou ecarte |
| champ obese | ECARTE ET DIT (jamais perdu en silence) |
| fiche introuvable | un avertissement la NOMME |

Le bloc mesure sur l'injection reelle de MO-545 : `present: true`,
`complet: true`, 8 champs, poids 30 tokens pour un plafond de 300, un seul
domicile (`matrix/USER-PROFIL.md`). Rien ne manque, rien n'est coupe en silence.

## 2. LA VISIBILITE : LA OU LA DONNEE EST APPELEE A SERVIR, ELLE N'EST PAS LUE

La decision createur (EO-480 / MO-507, 2026-09-30) est ecrite dans le code :

> Le profil n a de sens qu au moment ou l agent s adresse a l utilisateur, et ce
> moment est le compte-rendu de fin.

C est ce que le maillon 76 garde : le profil est le DERNIER de la phase
`apres-mission`, et il ne s invite nulle part ailleurs.

Mais voici le fait mesure sur la remise **par defaut** -- celle que l'agent lit
effectivement a la cloture (la fiche technique de travail, `MO-471 D2/D3`) :

```
  [ajustables] resumes (joignables : pilote ordres --id <id> --complet) :
    profil : present (506 o)
```

C'est tout. Le bloc profil est un AJUSTABLE, donc il est **resume** ; le resume
d'un dictionnaire, dans `_resume_champ`, est la liste de ses **cles**. Le
pseudo, le fuseau, le style de conversation : **aucune valeur n'est remise**.

Mesure directe :

- `"petit genie"` dans le resume du profil : **absent**
- `"Decontracte"` dans le resume du profil : **absent**

Pour les lire, l'agent doit demander `--complet` -- c'est-a-dire aller chercher
l'information a la main, ce qu'un agent ne fait pas spontanement.

## 3. CE QUI MANQUE COMME GARDE

Le maillon 76 le dit lui-meme, noir sur blanc :

> **Il NE GARDE PAS le contenu du pseudo** : une fiche vide est un etat de la
> fiche, pas un defaut de l injection.

Il garantit donc l'ORDRE (le profil se sert en dernier) et la SOURCE (elle vient
du motif partage), mais pas la **REMISE**. Un controle qui garantit la place
d'une donnee sans garantir qu'elle est livree garantit qu'un etage est vide.

C'est exactement la phrase que le maillon 76 cite comme le fait d'origine :

> la fiche technique rendait `profil : present (506 o)` et s arretait la. Un
> agent qui ne demandait pas `--complet` n avait donc JAMAIS le pseudo sous les
> yeux.

Le defaut a ete **signale** a l occasion, comme le maillon le prescrit
(`on ajustera l injection par la suite, donc ce maillon ne la fait pas a sa
place, il la SIGNALE`). L ajustement n'a pas ete fait. La question qu il pose
est donc la bonne, et sa reponse est : le voyage est fait, la remise ne l'est pas.

## 4. CE QUE JE NE DIS PAS

- Je ne dis pas que la donnee est PERDUE : elle est dans l'injection, complete,
  et joignable par une porte.
- Je ne dis pas que le camouflage est desirable au travail : pendant une reparation,
  le pseudo n aide personne. La question posee porte sur la FIN.
- Je ne dis pas que `si_j_etais_user` est un trou : il est `applique: false` avec
  un motif dit, donc c est une decision tracee, pas un silence.

## 5. LA QUESTION QUI RESTE AU CREATEUR

Rendre les VALEURS du profil dans la remise de cloture coute environ 500
caracteres par round (le bloc complet fait 506 o). C'est une decision de
perimetre de remise, pas une correction : elle engage ce que l'agent a sous les
yeux a chaque fin de mission. Deux directions possibles :

- **servir les valeurs a la cloture** -- la decision EO-480 est alors tenue
  jusqu au bout ;
- **ne pas les servir** -- alors la decision doit etre REECRITE dans le code,
  parce qu elle dit aujourd hui le contraire de ce que le code fait.

Ne pas trancher ici n'est pas une option confortable : dans les deux cas, le code
et la decision doivent dire la meme chose.
