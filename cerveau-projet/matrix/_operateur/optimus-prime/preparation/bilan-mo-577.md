---
identite:
  type: journal
  appartient_a: optimus-prime
  commun: false
---

# BILAN MO-577 -- LA CHAINE PENSE-BETE AVAIT TROIS ETATS ET UN TRAVAIL A RENDRE

> Enonce (EO-557) : "la chaine pense-bete n a pas d etat d execution, ses 4 objets
> sont bloques a todo". Arbitrage du createur : (a) l etat `execute` est ajoute
> mais CONDITIONNE A UNE PREUVE ; (b) le declencheur est traite dans cette mission.

## LE CONSTAT, ET SA CORRECTION

L enonce est exact sur un point et faux sur un autre.

Exact : la chaine ne connaissait que trois etats -- `pense-bete`, `spec`, `todo` --
et rien ne pouvait dire "ce travail est fait". Le mot `execute` n existait nulle
part dans le parc.

Faux : les quatre objets n etaient pas "bloques". Les quatre taches de PB-003
etaient LIVREES, mesurees :

| tache | livre | taille mesuree |
|---|---|---|
| T1 | `suivi-pilote/pannes-declarees.json` | 32 Ko |
| T2 | `suivi-pilote.py` + sa vue + son journal | 92 Ko |
| T3 | les templates, dans `suivi-pilote/templates/` (**pas** `_operateur/optimus-prime/templates/`) | -- |
| T4 | deux maillons de non-regression | -- |

La chaine disait `todo` parce que `todo` signifiait "le livrable de la todo-list
est produit", et rien d autre. Il n y avait pas de place pour "le travail
lui-meme est termine" : ce n etait pas un blocage, c etait une case manquante.
C est aussi la lecture de MO-538 : les trois etats modelisaient la PRODUCTION d un
document, jamais l ACCOMPLISSEMENT d un travail.

## LA DECISION, ET POURQUOI ELLE EST CONTRAINTE

Un `execute` pose sans fait atteste serait une **declaration** : la machine
ecrirait "c est fait" sur la seule foi d un ordre humain, et elle ne pourrait
jamais distinguer un travail livre d un travail annonce. Donc la preuve est la
CONDITION, pas une option.

Trois refus distincts, parce que trois manieres de ne rien prouver ne se
confondent pas :

- `REFUS_PREUVE_NON_NOMMEE` -- aucun fichier nomme ;
- `REFUS_PREUVE_INTROUVABLE` -- fichier nomme, absent du disque ;
- `REFUS_PREUVE_VIDE` -- fichier present, **vide** : un fichier sans contenu ne
  prouve rien.

Le troisieme refus est celui qu on n ecrit jamais et qui evite le piege : un
`README.md` cree par le robot et laisse vide attesterait sa propre existence.

## CE QUI A ETE FAIT

`matrice/data/outils/chaine-pense-bete/` :

- `constants.py` -- `ETAPE_EXECUTE`, `PREFIXE_EXECUTE = "EX"`, `CHAMP_PREUVE`,
  `CHAMP_EXECUTE_LE`, `ETAPES` et `PREFIXES` et `CHAMPS_ETAPE` ports a **4**
  entrees, les sept messages de refus, `MESSAGE_EXECUTE`, `MESSAGE_RETOUR`.
  `ETAPES_AVANCEMENT` reste a trois : l avancement de production et l execution
  sont deux gestes distincts, `executer` a son propre verbe.
- `commun.py` -- `retirer_champ()` (le retrait que `poser_champ` n avait pas) et
  re-export de `horodater` : le `sys.path` vers `data/commun` n est pose que dans
  ce module, donc `etape/fonctions.py` ne peut pas l importer directement.
- `etape/fonctions.py` -- `_preuve_constatee()` (les trois refus),
  `executer()`, `revenir()`, `_etape_suivante()` qui parcourt desormais
  `ETAPES_AVANCEMENT` ; la preuve et la date apparaissent dans `etat`.
- `etape/entry.py`, `main.py` -- les deux verbes dans le parseur, `COMMANDES`,
  l usage du docstring.
- `revenir()` retire les trois champs (`execute`, `execute le`, `preuve`) : le
  retour est un retour **complet**, sinon un objet porterait une preuve orpheline.

Le declencheur : `pilote/injection/modes_emploi.py` rappelle la chaine dans la
carte des briques, via `_declarations_de_la_chaine()` qui remonte jusqu au
**marqueur** de la racine (L-013), jamais par `parents[N]`.

## LA FAMILLE `EX` N ETAIT PAS COSMETIQUE

`verifier-chaines.py` lit **chaque champ d etape comme un identifiant** et verifie
son prefixe et son compteur. Sans la famille `EX`, `execute: EX-002` aurait ete
accuse comme un identifiant sans prefixe. La famille a donc du etre declaree
reellement -- c est ce que le controle a mesure, pas une precaution de style.

## LES TESTS, Y COMPRIS CEUX QUI ONT MENTI

Cinq refus distincts joues : etat **inchange** a chaque fois. Nominal :
`executer --id PB-003 -- preuve _operateur/optimus-prime/suivi-pilote/README.md`
-> `TRAVAIL CONSTATE : PB-003 -> execute (EX-001)`, preuve et date posees. Sens
inverse : `revenir` -> `RETOUR A TODO`, trois champs retires, controle OK. Rejeu :
`EX-002`, et le compteur d historique n est pas ecrase (`EX: 2`).
Declencheur : parle depuis les cinq domiciles ; contre-temoin hors workspace ->
"porte absente". `modes_emploi.py --auto-test` : 14/14.

Cinq defauts ont ete trouves **par ces tests**, pas par relecture :

1. `ETAPE_TODO` importe partout sauf dans `etape/fonctions.py` ;
2. `revenir` empruntait le message de refus de `executer` -- il mentait sur le
   sens du verbe ;
3. guillemets manquants dans `REFUS_PAS_TODO` et `REFUS_PAS_EXECUTE` (les deux
   messages cassaient sur un objet non conforme) ;
4. `NL` non importe dans `commun.py` ;
5. la remontee de racine par `joinpath` ne marchait qu a la racine.

## LE CONTROLE A ACCUSE CE QUI AVAIT ECRIT -- ET ON L A VRAIMENT ECRIT

Avant la non-regression, le controle d attribution a designe trois fichiers :
`chaine-compteurs.json`, `chaine-suivi-du-pilote-d-optimus.md`,
`index-chaine.md`. Ce sont les trois vues **que la porte chaine-pense-bete
ecrit** a chaque avancement. Ils sont des productions declarees : la porte les
repose sur chaque passage, donc une note anterieure est perimee des le passage
suivant. Ils ont ete notes.

C est le meme schema que le vice revele par MO-576 (une porte qui pose CINQ vues
n etait declaree que pour une) : ici les trois vues sont ecrites par une porte
**du parc outil**, dont la declaration de productions reste a poser. Ce n est pas
un blocage, c est une dette nommee.

## NON-REGRESSION

**VERTE.** `VERDICT OK : non-regression verte (zone + flux).` Les trois echecs du
premier passage (attribution sur les trois vues, residus dans la zone jetable,
`vues-fraiches`) sont tous des consequences de mon propre travail de la mission ;
aucun n etait un vice du parc.
