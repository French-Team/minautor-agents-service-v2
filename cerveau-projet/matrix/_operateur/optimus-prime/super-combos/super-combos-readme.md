---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

### definition d un super-combos:
    un super-combos peut etre composer de plusieurs missions differentes qui pourront etre confie a l'agent.

## CONTRAT DE NOMMAGE (obligatoire, convention CV-008 -- BDD conventions-matrice)

> Decision createur 2026-09-13 : **un super-combo et un combo portent TOUJOURS
> un numero, visible dans le nom.** Le numero est la cle de reference et
> l'adresse sur le disque.

| Regle | Valeur |
|---|---|
| Prefixe super-combo | `sc` (dossier `sc-001-<slug>/`, id `sc-001`) |
| Prefixe combo | `c` (dossier `c-001-<slug>/`, id `c-001`) |
| Largeur du numero | 3 chiffres, zero-paddes |
| Reutilisation d'un numero | **JAMAIS** (le compteur ne redescend pas, meme apres suppression) |
| Source de verite | `registry.json` (section `super-combos`, compteur `sc`) -- **une source par famille** : les combos ont la leur dans `combos/registry.json` |
| Outils (`combos/outils/`) | ne sont PAS des combos : aucun numero |

Le prefixe dit la NATURE de l'objet : `sc-` = super-combo, `c-` = combo.
C'est ce qui leve l'ambiguite de l'ancien nommage (les deux vivaient cote a
cote sous des noms libres, sans moyen de les distinguer).

## Super-combos disponibles

| Numero | Nom | Description | Themes associes |
|---|---|---|---|
| `sc-001` | `super-combos/sc-001-auto-xxx/` | Enchainement intelligent des themes AUTO-XXX (6 phases) | AUTO-XXX |
| `sc-002` | `super-combos/sc-002-auto-evolution/` | Orchestration complete du cycle auto-evolution (detecter -> qualifier -> cibler -> modifier -> valider) | AUTO-EVOLUTION |

Lancement par numero : `python lancer-super-combos.py --numero sc-001` (le lanceur
vit ICI, avec ses objets : il lit le `registry.json` pose a cote de lui)
(la casse d'entree est libre : `SC-001`, `sc-001`, `#1` et `1` sont normalises
vers `sc-001` -- la forme canonique est en minuscules, regle CV-009)

## CONTRAT DE LANCEMENT (obligatoire, MO-071 / EO-114)

> Decision (2026-09-13) : **le VERBE de lancement vit dans le REGISTRE**, pas
> dans le code du lanceur. Chaque entree de `registry.json` declare :
>
> | Champ | Sens |
> |---|---|
> | `verbe` | le verbe lance par DEFAUT ; **vide** = l'objet n'a pas d'entree unique (cycle a phases) |
> | `verbes` | la liste des verbes ACCEPTES -- la seule source de verite |
>
> Le lanceur LIT ce contrat ; s'il manque, ou si le verbe demande n'y est pas, il
> **REFUSE en le nommant** (code 2) : jamais un verbe invente, jamais un echec
> muet. La porte (`creer-combo.py verifier`, et `lister`) EXIGE le contrat : un
> objet ne peut donc plus naitre **inlancable par construction**.
>
> Pourquoi pas "tout le monde expose `executer`" : les deux super-combos ne font
> pas le meme metier. `sc-001` a UNE entree (`executer`) ; `sc-002` est un cycle a
> phases dont "executer" ne veut rien dire -- imposer ce verbe aurait fabrique un
> verbe FAUX (le contrat doit dire la verite de l'objet).

Lancement :

```
python lancer-super-combos.py --numero sc-001 [--verbe status] [--fichier <f>] [--mission <id>]
python lancer-super-combos.py --numero sc-001 --verbe auto-test
python lancer-super-combos.py --numero sc-002 --verbe detecter "Quand X, Y, car Z" --type outil --gravite mineure --frequence ponctuelle
```

### sc-001 : ce qu'une phase TESTE vraiment (reparation 2026-09-14)

> Une phase de sc-001 **teste son theme par la porte officielle**
> (`combos/outils/tester-theme.py`, la meme que sc-002 emploie deja) et n'est
> declaree reussie que sur **TEMOIN** positif : `code 0` **et** la phrase de
> succes du testeur. Un `code 0` muet est ACCUSE, parce qu'un testeur muet ne
> distingue pas "le theme est bon" de "je n'ai rien regarde".
>
> POURQUOI : l'ancienne version lancait le theme par `python theme-X.json`. Or
> un theme n'est **pas un programme**, c'est l'ARBRE DE DECISION (JSON) que
> l'agent lit -- donc un simple **litteral de dictionnaire** en Python : une
> expression valide, sans effet, qui sort en `code 0`. Mesure : la commande
> `--fichier /chemin/qui/n/existe/pas.py --mission MO-999` rendait
> "6/6 themes, 0 echec, TOUS LES THEMES ONT REUSSI". **Un controle qui ne peut
> pas echouer ne dit rien.**
>
> Trois refus NOMMES remplacent ce faux vert : une cible `--fichier` absente,
> un theme introuvable, un testeur absent (les deux derniers = NON TESTABLE).
> Le verbe `auto-test` **prouve** que la chaine sait accuser : la decision pure
> sur des cas pieges, **l'ancien mecanisme rejoue** (code 0 muet) et un cobaye
> en dossier jetable ou un theme corrompu, puis un theme absent, doivent etre
> ACCUSES ET NOMMES.

- Tout argument NON reconnu par le lanceur est **transmis tel quel** au
  super-combo : c'est ainsi qu'on lui donne ses propres options.
- `--verbe` hors contrat -> refus code 2 avec la liste des verbes acceptes.
- Objet sans entree unique et sans `--verbe` -> refus code 2 (avec la liste).

## Rangement (corrige le 2026-09-13, MO-067)

```
super-combos/                 <- les SUPER-combos (cette famille)
  registry.json               <- SA source de verite (section super-combos, compteur sc)
  lancer-super-combos.py      <- SON lanceur
  sc-001-auto-xxx/  sc-002-auto-evolution/
  combos/                     <- la famille INFERIEURE (modele createur :
    registry.json                un super-combo peut contenir des combos)
    c-001-lecons/ ... c-007-frictions/
    outils/                   <- la boite a outils transverses, non numerotee
```

Avant cette date les `sc-` vivaient DANS `combos/`, avec les `c-` : le dossier
nomme `super-combos/` ne contenait aucun super-combo. Consequence MESUREE de ce
rangement : la remorque etiquetait `sc-001` et `sc-002` en type `combo` -- le
prefixe qui dit la nature etait nie par l'emplacement.

> `combos/outils/` n'est PAS un super-combo, ni un combo : c'est la boite a
> outils transverses (BDD, validation, generation), non numerotee.
    