---
identite:
  type: index
  appartient_a: optimus-prime
  commun: false
  liens: _operateur/optimus-prime/pilote/entonnoir/indices.md, _operateur/optimus-prime/pilote/MOTS-CLES.md
---

# LEXIQUE DES IDENTIFIANTS (MO-, EO-, RS-, M-, E-, CV-, L-, PB/SP/TD-)

> A quoi sert ce fichier : un identifiant comme `MO-541` ou `EO-546` n est pas
> lisible tant qu on ignore ce que la lettre designe, QUI l attribue, et A QUEL
> RANG elle se tient. Ce lexique est la SEULE table qui repond a ces trois
> questions. Il est mesure (2026-10-02, MO-543) : chaque ligne a ete verifiee
> dans le code ou sur les donnees, pas reprise d une croyance.
>
> UNE SEULE LIGNE PAR FAMILLE, et la regle qui compte : un id n est jamais ecrit
> a la main. C est la PORTE qui l attribue, et elle refuse un id d une autre
> famille (code 2). Un id invente est donc detectable, pas seulement improbable.

## LA REGLE DE LECTURE (les trois questions, dans cet ordre)

1. QUE DESIGNE LA LETTRE ? -- la nature de la chose.
2. QUI L ATTRIBUE ? -- la porte. Jamais l agent, jamais la main.
3. A QUEL RANG ? -- l ordre compte : un `EO-` se transforme en `MO-`, il ne
   fait jamais l inverse. C est ce qui garantit qu une demande ne peut pas
   sauter son audit.

## LES FAMILLES DU FLUX 2 (optimus-prime) -- le chemin d une demande

| Prefixe | Designation | QUI attribue l id | Rang / ordre | Reel |
|---|---|---|---|---|
| `EO-NNN` | **E**ntonnoir **O**perateur -- une DEMANDE, pas encore une mission | `entonnoir/vrac/fonctions.py` (`PREFIXE_ITEM`, `listes.py:244`) + compteur `zfill(3)` | **1** -- echelon 0, le vrac, l etat le plus brut | compteur a 550 ; 10 au vrac |
| `MO-NNN` | **M**aintenance **O**perateur -- une MISSION, tiree du brin | `pilote/constants.py` (`PREFIXE_ID = "MO-"`) | **2** -- la mission est conductible | 91 missions, 6 en attente |
| `RS-NNN` | **R**aisonnement **S**egment -- un segment de raisonnement reutilisable | `bdd-raisonnement/constants.py` (`PREFIXE_ID = "RS"`) | **3** -- produit PAR la mission, jamais avant | 57 segments actifs |

> L ordre est STRICT : `EO-` ne devient `MO-` que par `file consommer` ou
> `conduire`, et `MO-` ne produit un `RS-` qu en mission. Un segment de
> raisonnement qui precede sa mission serait un raisonnement sans experience --
> donc un segment invente.

## LES FAMILLES DU FLUX 1 (cameleon) -- la zone voisine

| Prefixe | Designation | QUI attribue | Reel |
|---|---|---|---|
| `E-NNN` | **E**ntonnoir, flux 1 (cameleon) | `matrice/pilote/entonnoir/listes.py:75` (`PREFIXE_ITEM = "E-"`) | zone voisine |

> POINT DE VIGILANCE, deja mesure et ecrit dans `entonnoir/indices.md` : les deux
> entonnoirs PARTAGEAIENT le prefixe `E-` avec deux compteurs separes, donc le
> meme id designait deux items DIFFERENTS. C est exactement la meme maladie que
> `M-` pour les missions d Optimus. La separation a ete posee : `EO-` pour le
> flux 2, `E-` pour le flux 1. Un id hors famille est refuse a l entree.

## LES FAMILLES DE CONTENU (ce que le flux produit, pas ce qu il consomme)

| Prefixe | Designation | QUI attribue | Reel |
|---|---|---|---|
| `L-NNN` | **L**econ -- un apprentissage reutilisable, non lie a une mission | `matrice/data/lecons.json`, outil `bdd-lecons` | 226 lecons |
| `CV-NNN` | **C**onvention de la **V**ie -- une regle de forme de la Matrice | `matrice/data/conventions-matrice.json` | 14 conventions |
| `PB/SP/TD-NNN` | **P**ense-**B**ete, **S**pec, **T**odo -- les trois maillons d une chaine de preparation | `preparation/`, portes de chaine | l identite d une carte `type: chaine` porte les trois |

> Les trois derniers ne sont pas des missions : ce sont des DOCUMENTS. Ils ne se
> consomment pas, ils se lisent. Les mettre dans la meme colonne que `MO-`
> serait une faute de lecture -- d autant que la chaine `PB-001 / SP-001 / TD-001`
> se lit DANS cet ordre, ce qui en fait une famille a part entiere.

## LA FAMILLE HERITEE -- `M-NNN`

| Prefixe | Designation | Etat |
|---|---|---|
| `M-NNN` | Mission de la v1 (et de la v2) | **HERITAGE** -- encore cite dans `classeur-variables.json`, `activites-recentes.json`, `conventions-matrice.json`, la fiche du cameleon |

> `M-` est le prefixe AVANT que `MO-` existe. Il survit dans des donnees et des
> citations, mais aucune porte ne l attribue encore. Il est donc a lire comme
> une reference historique, jamais comme un identifiant vivant. C est le genre
> de residu que le lexique rend visible au lieu de le laisser trainer dans des
> fichiers sans explication.

## LA LECTURE QUI FAIT TOUT (l ordre du flux)

```
USER ---> EO- (demande)
            |  classer / retiqueter / urgencer / preparer  (echelons 1 a 3)
            v
          BRIN (echelon 4, la file de travail)
            |  file consommer  (la tete part)
            v
          MO- (mission conductible)
            |  le travail produit
            v
          RS- (segment de raisonnement)  +  L- (lecon)  +  CV- (convention)
```

## CE QUE CE LEXIQUE NE FAIT PAS, ET POURQUOI

- Il ne GENERE pas les identifiants : une porte le fait, et une porte qui
  genere refuse aussi les doublons. Un lexique qui attribuerait des ids serait un
  second chemin vers le meme etat -- donc une divergence de plus.
- Il ne remplace pas `MOTS-CLES.md` (qui liste les MOTS et les crochets) ni
  `entonnoir/listes.py` (qui porte les listes FERMES). Il les COMPLETE : la
  grammaire du PREFIXE n etait ecrite nulle part.
- Il n est pas une source de verite pour le code : chaque valeur cite ici a son
  DOMICILE (M-076), et c est lui qui fait foi quand les deux divergent.

## LE TEST QUI JUSTIFIE CE LEXIQUE

Il existe parce qu un audit recent (MO-542) a demande qui lisait un document
precis. La reponse a exige de croiser cinq fichiers pour reconstituer la
chaine. Un identifiant doit pouvoir se lire seul : `EO-546` doit dire tout de
lui qu il est une demande, pas une mission, et qu il n a pas encore ete
conduite. Ce fichier est ce qui rend cette lecture immediate.
