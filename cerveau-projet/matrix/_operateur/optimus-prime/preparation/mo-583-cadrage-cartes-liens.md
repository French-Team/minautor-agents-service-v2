---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# MO-583 -- CARTE D'IDENTITE ET LIENS : L OUTILLAGE EST COMPLET, LE CONTENU MANQUE

Cadrage (item EO-511, depose le 2026-09-30). La demande est en deux
volets : (a) une routine qui verifie que les cartes portent leurs liens,
(b) un template de carte d'identite pour le moteur de recherche.

**Verdict de mesure : les deux briques EXISTENT et TOURNENT. Ce qui manque
n est pas un outil, c est le CONTENU des cartes.**

## 1. CE QUI EXISTE DEJA, ET QUI LE FAIT TOURNER

| Besoin demande | Brique existante | Etat mesure |
|---|---|---|
| Routine qui verifie les liens | `matrice/routines/verifier-liens-cartes/` | tourne, rapport du 2026-10-04 17:37 |
| Template de carte | `matrice/templates/carte-identite/carte-complete.modele` | complet, 5 regles de lien |
| Modele minimal | `matrice/templates/carte-identite/carte.modele` | present |
| Grammaire de la carte | `matrice/data/commun/carte_identite.py` | `liens` est un champ reconnu |
| Garde de presence de carte | `verifier-cartes-identite.py` | vert, 246 cartes |
| Pose d une carte | portes `carte-creer` / `carte-editer` / `carte-modifier` | `--liens` accepte |
| Recherche par lien | moteur `--lien <chemin>` | mode dedie (lecon L-055) |

Le modele complet ne se contente pas d avoir la cle : il documente les
CINQ regles de `liens` (chemin canonique, jamais soi-meme, la cible doit
exister, le lien se declare des deux cotes, sous six liens), et fournit
une section `## Ce qui le connecte`.

## 2. LE CONSTAT CHIFFRE (rapport du 2026-10-04 17:37)

```
cartes              : 234      liens              : 55
cartes_avec_liens   :  20      reciproques        : 28
cibles_sans_carte   :  19      egocentriques      :  0
morts               :   0      fautifs            :  0
sans-retour         :   8
```

Autrement dit : **20 cartes sur 234 sont connectees, 214 ne le sont pas.**
La QUALITE est parfaite (0 lien mort, 0 forme fautive, 0 egocentrisme) --
c est la COUVERTURE qui est nulle.

Mesure complementaire sur les `.md` du parc : 254 documents, 246 avec
carte, **225 cartes sans bloc `liens:`**.

## 3. LE VRAI PROBLEME, FORMULE

La grammaire dit noir sur blanc :

> POURQUOI PAS DANS LES CLES OBLIGATOIRES : une carte sans lien est
> NORMALE

Donc le garde ne peut pas exiger `liens` sans une decision du createur :
il rendrait 214 cartes hors contrat du jour au lendemain. C'est la seule
question qui appartient au createur.

## 4. CE QUE JE PROPOSE, ET LE POINT A TRANCHER

**Proposition A (prudente, sans casser)** : rendre `liens` obligatoire
UNIQUEMENT pour les `DESCRIPTION.md` d'outils et les fiches techniques --
ce sont les seuls documents dont on cherche spontanement "qu est-ce que je
dois modifier quand je touche ca". C'est le besoin exprime. Les 20 cartes
qui portent deja des liens sont exactement de ce type : la pratique a
deja converge.

**Proposition B (large)** : `liens` obligatoire partout. Plus beau,
214 cartes a editer, et la regle perd sa portee (un README de zonage
n a pas de voisin naturel).

**Ma lecture** : A. Elle rend le moteur de recherche utile sans exiger un
travail mecanique sur des documents qui n ont pas de voisin.

## 5. LA DECISION DEMANDEE AU CREATEUR

> `liens` devient-il obligatoire pour les SEULES fiches techniques et
> DESCRIPTION.md d'outils (proposition A), ou pour tout document ?
>
> Et dans le cas A : faut-il un garde qui accuse la carte sans lien
> dans cette sous-couche, ou un simple RAPPORT qui compte la couverture
> (comme aujourd hui) ?

## 6. CE QUE LA MISSION NE FAIT PAS

Aucun fichier de production modifie. Un cadrage mesure et propose ; il ne
cree pas la regle, surtout quand la regle engage 214 documents et que la
grammaire la refuse aujourd hui explicitement.

## 7. MOYEN DE PREUVE

`matrice/routines/verifier-liens-cartes/rapport-liens.json` (date
2026-10-04 17:37:56) ; `matrice/templates/carte-identite/carte-complete.modele` ;
`matrice/data/commun/carte_identite.py` (CLES_OBLIGATOIRES et CLE_LIENS) ;
`verifier-cartes-identite.py`.
