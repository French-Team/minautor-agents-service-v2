---
identite:
  type: analyse
  appartient_a: operateur
  commun: false
  version: 1
  date: 2026-10-02
  statut: a-jour
  tags: MO-544,revision,bak,archives,duree-de-vie
---

# Duree de vie des points de restauration, des archives et des registres

Mission **MO-544** (REVISEUR, EO-503). Mesure et arbitrage, 2026-10-02.

## 1. LA QUESTION POSEE

> on doit verifier le fonctionnement des rotations, les .bak, les archives, les
> audit, les constats, etc.
> pourquoi doivent ils vivre si longtemps, si les informations importantes sont
> dans les bdd ?
> les .bak sont utile au moment des changements, etc (securite 1). par la suite
> quand tout est bon, ils deviennent inutile -> ils doivent etre 'archive'.
> les archives sont utile pendant quelques heures (securite 2) mais en sachant
> que l'on a les bdd et le git. elles doivent etre supprimer avant chaque commit
> (je pense ?)

Une revision ne repond pas en supprimant : elle repond en **mesurant**, puis en
demandant la regle. C est ce que fait ce document.

## 2. CE QUE LE DISQUE DIT

Perimetre mesure : `cerveau-projet/matrix` (la Matrice entiere). ages au
2026-10-02 20:55, sur la serie `dernieres_passes` publiee par chaque etat.

| Population | Nombre | Volume | Age median | Age max |
|---|---|---|---|---|
| Points de restauration (`.bak.<horodatage>`) | **613** | 13,05 Mo (matrice + hors matrice) | 8,1 j | 26,5 j |
| Fichiers d origine distincts | 569 | -- | -- | -- |
| Fichiers de plus de 5 points | **3** (22, 7, 5 points) | -- | -- | -- |
| `archives/` (purification) | 67 fichiers | 6,77 Mo | 9,9 j | 24,9 j |
| `archives/` de plus de 7 jours | **39** | -- | -- | -- |
| `conservation.json` (inventaire declare) | 4253 entrees | -- | -- | -- |
| Fichiers d audit | 25 | -- | -- | -- |

**La distribution dit la regle toute seule** : 556 fichiers d origine ont
exactement UN point de restauration. Le `.bak` ne s accumule pas -- c est le
travail qui change de fichier, pas le fichier qui change. Les 3 outliers
(22, 7, 5 points) sont des fichiers ecrits de nombreuses fois le meme jour.

## 3. CE QUE GIT DIT (le point qui change tout)

| Etat, dans la Matrice | Nombre |
|---|---|
| Points de restauration SUR DISQUE, **suivis par git** | **548** |
| Points de restauration sur disque, **jamais commits** | 65 |
| Points de restauration **suivis par git MAIS ABSENTS du disque** | **362** |

Deux lectures, et elles ne disent pas la meme chose :

1. **548 points de restauration sont dans l index.** Chaque point produit par une
   porte entre dans le commit suivant. C est la que le bruit se paie.
2. **362 sont des fantomes** : git les suit, le disque ne les a plus (ils ont ete
   archives ou purges sans que l index suive). Ils ne peuvent plus rien
   proteger -- ils ne sont que de la graisse dans l historique.

## 4. LA REGLE TRANCHEE

Createur, 2026-10-02 :

- **`.bak`** : garder les **N derniers points de restauration par fichier**, purger
  les plus anciens, et **cesser de committer les `.bak`**. N laisse ouvert (3 ou
  5) : **5** retenu, en une seule constante nommee.
- **archives** : vider avant chaque commit (les BDD et git suffisent).

## 5. CE QUI EST LIVRE

1. `super-combos/combos/outils/purge-points-restoration.py` -- la regle outillee,
   enregistree au registre (184) et joignable par le lanceur sous
   `purge-points-restoration`. Inventaire par defaut, purge exige `--oui`.
   Auto-test 7/7 : cobaye (7 points, 5 conserves -> les 2 plus anciens), contre-
   temoin (5 points -> rien), invariance a l ordre de lecture, epargne calibree
   (4 noms qui ne sont pas des points), ancrage du nom, refus de purger ce que git
   ne suit pas, et refus quand git ne repond pas.
2. `preparation/proposition-gitignore-bak.md` -- le texte `.gitignore`, **livre
   et non ecrit** (voir section 6).

## 6. CE QUI N EST PAS FAIT, ET POURQUOI

- **Le `.gitignore` n est pas ecrit par la Matrice.** Il est a la racine du
  workspace, hors du perimetre d ecriture : la porte ECRIRE le refuse (code 2),
  comme elle refuse `docs/`. Meme regle que pour les sources : la Matrice livre le
  texte, le createur le pose. C est une decision de perimetre, pas une inability.
- **`git rm --cached` n est pas joue.** C est une mutation de l index, pas une
  ecriture de fichier : elle appartient au createur. Le texte est dans la
  proposition.
- **Aucune purge reelle.** Sur les 19 points qui debordent la retenue de 5, les
  19 sont **non suivis par git** : l outil les REFUSE (les supprimer serait une
  perte, pas une retention). Purge reelle : **0 fichier detruit aujourd hui**.
  Les 548 points suivis ne debordent pas la retenue de 5.

## 7. TROIS DEFauts MESURES DANS L OUTIL LUI-MEME

Les trois ont ete joues avant livraison, pas relus :

1. **Un faux zero.** La resolution de racine s arretait a `<matrice>/matrice/` et
   ignorait `_operateur/` -- elle rendait 326 points au lieu de 588. Un inventaire
   qui rend moins parce qu il regarde moins est indiscernable d un inventaire
   complet : c etait un ZERO FAUX.
2. **Une affirmation non mesuree.** L outil annoncait " chaque point reste dans
   l historique git " sans l avoir verifie. Il est desormais couvert par une
   fonction pure (`reparable`) et par deux temoins -- dont le contre-temoin du
   silence : git muet -> rien n est purge.
3. **Un siege suppose.** Le depot est a la racine du WORKSPACE, deux niveaux au
  -dessus de la Matrice ; chercher `.git` sous la matrice rendait git muet a tort
   et faisait refuser une purge legitime. Le siege se DEMANDE maintenant
   (`rev-parse --show-toplevel`), il ne se suppose plus.

## 8. LA LECON

Une regle de duree de vie ne se juge pas au nombre de fichiers qu elle supprimerait
aujourd hui. Celle-ci en supprimerait **zeros** -- et c est sa reponse la plus
utile : le `.bak` n accumule pas, l index, lui, garde. La bonne question n est
donc pas " que purge-t-on " mais " qu est-ce qui entre dans l historique sans y
avoir ete decide ". C est le sujet de l item depose au vrac.
