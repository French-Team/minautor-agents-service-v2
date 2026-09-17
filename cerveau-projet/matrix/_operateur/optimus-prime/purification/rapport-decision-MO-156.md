---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
  mission: MO-156
  statut: valide
---

# MO-156 -- RAPPORT DE DECISION (CASES 5 ET 6)

> Sujet : la famille des points de restauration `.bak.*` de la Matrice.
> Cases 5 (contre-analyse contradictoire) et 6 (un verdict par element).
> Lecture seule sur les donnees : RIEN n a ete deplace, RIEN n a ete supprime.
> L acte est la case 7, et il n est pas execute ici.

## 1. CASE 5 -- CONTRE-ANALYSE (3 axes, chaque mais MESURE)

Document : `analyse-nemesis-rotation-MO-156.md` (ecrit par la porte d ecriture).

Ce que la mesure a change dans la doctrine :

| Attaque | Mesure | Consequence sur le contrat |
|---|---|---|
| Le nombre N n a pas de fondement | les DEUX portes de revert prennent le `.bak` LE PLUS RECENT (`glob` puis `max` sur la date) | **N = 1** : le contrat des portes n exige qu un point. Garder plus n ajoute aucune capacite |
| Cout de N | N=1 libere 73 points (1,45 Mo, 69 %) ; N=2 n en libererait que 41 (41 familles n ont qu UNE version) | la politique "garder les N plus recents" est un chiffre sans proprietaire |
| Gain reel | parc = 2,11 Mo : le disque n est pas le sujet ; le sujet est le BRUIT de surface + une REGLE au lieu d une accumulation (102 points ecrits le 16/09 seul) | borner chez le PRODUCTEUR (la porte d ecriture), pas chez l observateur |
| Le parc est deja froid | 36 familles sur 75 ont leur point le plus recent vieux de plus de 24 h (mediane 23,6 h, max 255 h) | l argument "on en a encore besoin" ne tient plus pour la moitie du parc |
| L archive deplacerait le bruit | un dossier ordinaire sous `matrix/` est indexe par le moteur | l archive doit etre une ZONE INVISIBLE declaree, et elle contient du CONTENU INTERNE : jamais lisible par le cameleon |
| Une rotation est une course | la surete existe deja dans `data/commun/rotation_journal.py` (MO-101 : archiver d abord, archive dans le deja connu, course refusee, borne chez le proprietaire) | la porte d archive CONSOMME ce moteur, elle ne le reinvente pas |

**5 refus verses au contrat de la porte d archive (entree de la case 7)** :
jamais un point plus recent que sa source ; jamais le dernier point d une source
absente ; jamais une forme non conforme (SIGNALER, ne pas absorber) ; jamais une
zone hors perimetre (SIGNALER) ; jamais deux fois le meme element (idempotence).

**Reserve assumee** : aucune mesure du jour ne montre de perte possible
(0 orphelin, 0 ecriture interrompue, 0 forme non conforme). Le risque est
PROSPECTIF : il porte sur ce que la porte fera quand ces cas se presenteront --
d ou l interet de l ecrire dans le contrat AVANT l acte.

## 2. CASE 6 -- LES VERDICTS (155 elements, 0 sans preuve)

Une preuve est OBLIGATOIRE pour decider (la porte la refuse vide) : les 155
entrees en portent une, mesuree au moment de la decision.

| Categorie | Nb | Verdict | Mesure qui le fonde |
|---|---|---|---|
| STRUCTUREL | 73 | **conserver** | la famille de cette source compte N versions et CELLE-CI porte l horodate maximale : c est le point que les portes de revert servent encore |
| VIVANT | 2 | **conserver** | lecture REELLE mesuree dans le code (`pilote/injection/cycle.py` pour l historique du cycle, `pilote/commun.py` + `suivi-optimus/constants.py` pour la file archivee) |
| HISTORIQUE | 2 | **conserver** | aucune lecture reelle : 1 citation, et c est un COMMENTAIRE de `pilote/constants.py` (memoire du renommage) ; ce sont des archives, pas des residus |
| OBSOLETE | 73 | **archiver** | une version PLUS RECENTE du meme fichier existe : cette version n a plus d usage EN PLACE |
| HORS-PERIMETRE | 2 | **signaler** | `tmp-cameleon/` est la zone JETABLE du cameleon (regle immuable `perimetre-tmp.md`) : aucune ecriture de la Matrice n y va |
| ORPHELIN | 1 | **dette** | 0 citation en code, 0 en document : orphelin CONFIRME a la re-mesure ; aucune porte d archive n existe pour un orphelin (ecart E3) |
| COBAYE | 2 | **dette** (K-001, K-002) | entrees de FORME, aucun element reel sur disque : il n y a rien a archiver |

Repartition des 148 points de restauration classes :
**146 dans le perimetre** (73 conserver + 73 archiver) et **2 hors perimetre**
(la zone jetable du cameleon). C est exactement le perimetre annonce.

**Reparations par la porte** : `reparer` n a ete rendu a personne, et aucun
element n a ete touche -- les verdicts sont des DECISIONS, pas des actes.

## 3. LA DESTINATION DES 73 ARCHIVES

```
_operateur/optimus-prime/purification/archives/<chemin source en miroir>
```

Quatre raisons, toutes verifiables :
1. **dans `matrix/`** -- le plan refuse toute operation hors `matrix/` ;
2. **zone invisible par construction** -- `_operateur` est le PLANCHER du
   domicile d invisibilite (MO-152) : l archive n ouvre aucune fuite nouvelle
   (c est la reponse au 3e axe de la contre-analyse) ;
3. **miroir** -- `destination` moins le prefixe = `source` : la provenance reste
   lisible et la restauration devient mecanique (exigence de la case 8) ;
4. **le nom conserve son horodate** -- le motif domicilie continue de designer
   l element comme un point de restauration, et l espion d integrite continue de
   l exclure de son registre.

**Cas particulier assume et justifie** : `agents/cameleon/cameleon.md.bak.*`
est classe DANS le perimetre (K-149 conserver, K-150 archiver) alors que
`tmp-cameleon/` est HORS PERIMETRE. La difference n est pas un gout : la regle
immuable protege la ZONE JETABLE du cameleon, tandis que la FICHE de l agent est
un artefact de la Matrice que j edite moi-meme (mission MO-147 : regle 12
ajoutee a cette fiche).

## 4. LES PREUVES : 152 CORRECTIONS ASSUMEES

**Defaut trouve, et il est de mon fait** : mon releve de famille utilisait
`re.match`, qui ancre au DEBUT de la chaine, alors que le motif domicilie
(`MOTIF_BAK_HORODATE`) est en FIN de nom. Resultat : **0 version comptee dans
toutes les familles** et 146 preuves annoncant "0 version(s)" / "une version PLUS
RECENTE existe (?)".

**Ce qui n etait PAS faux** : les verdicts. Ils venaient de la classification
mesuree en MO-154 (qui, elle, consommait le motif du domicile correctement). On
a donc corrige la PREUVE, jamais le verdict.

**Ce qui manquait pour le faire honnetement** : la porte n avait AUCUN verbe de
correction (friction 78). Il ne restait que porter une preuve fausse ou ecrire le
JSON a la main -- interdit par le plan. Le verbe `preciser` a donc ete ajoute :
il corrige la preuve, trace l operation, et ne touche NI la categorie, NI le
statut, NI le verdict (aucune re-decision).

**152 corrections** passees par la porte, 0 refus definitif. Verification :
`preuves fausses restantes = 0`, `preuves vides = 0`.

## 5. CE QUE LA RE-MESURE A TROUVE (et qui n etait pas dans le plan)

1. **Le parc a grandi PENDANT la mission** : 7 points de restauration neufs,
   nes de MES ecritures (5 de la reparation de la porte de conservation,
   2 du rapport d audit MO-154). Ils n ont AUCUNE decision -> l acte doit les
   refuser et les signaler (jamais agir sans decision).
2. **6 familles ont un plus recent non classe**, dont
   `matrice/data/outils/bdd-conservation/ajouter/fonctions.py` : **K-147**,
   classe STRUCTUREL a 07:48, depasse a 08:08 par ma propre reparation. Son
   verdict `conserver` reste INOFFENSIF (il n est pas deplace) mais l invariant
   "un seul point structurel par famille" est rompu, et la preuve de K-147 le DIT
   desormais (elle etait fausse avant correction, elle est exacte maintenant).
3. **Le delta existe parce que rien ne borne le producteur** : c est la
   demonstration de l ecart E2 (l exemption borne la FORME, pas le VOLUME). Un
   classement est DATE : il se re-mesure avant tout acte (friction 79).
4. **Ma premiere mesure du delta etait fausse** : elle comparait des chemins
   `/` (BDD) a des chemins `\` (scan Windows) et annoncait 153 "nouveaux" et
   155 "disparus". Corrigee par normalisation (`as_posix()`), et corrigee une
   seconde fois : mon scan omettait le dossier `agents/`, ce qui faisait croire
   que K-150 n avait aucun plus recent (danger apparent qui n existait pas).

## 6. LES INVARIANTS QUE L ACTE (CASE 7) DOIT TENIR

Mesures sur le DISQUE, pas sur la BDD :

| Invariant | Mesure du jour |
|---|---|
| Chaque element a archiver a un plus recent qui RESTE en place | **73 / 73** |
| Chaque point STRUCTUREL est le plus recent de sa famille | **72 / 73** (K-147 perime, declare) |
| Tout element present sur disque a une decision | **non** : 7 non classes -> l acte doit REFUSER et SIGNALER |
| L archive est invisible (zone declaree exclue) | a PROUVER apres creation (audit d invisibilite, case 8) |
| `archive + actif = origine` (aucun octet perdu) | a PROUVER par empreintes + manifeste (case 8) |
| Le cameleon ne gagne aucun acces | a PROUVER par l audit d invisibilite (case 8) |

## 7. ETAT DE FIN MO-156

- Elements classes : 155 ; verdicts rendus : 155 ; elements sans preuve : 0.
- Preuves corrigees par la porte : 152.
- Elements deplaces : 0. Elements supprimes : 0. Octets deplaces : 0.
- Porte de conservation reparee : verbe `preciser` ajoute (friction 78),
  verbe documente `lire` rendu executable (ecart E6 de l audit MO-154).
- Frictions : 78 (majeure, ponctuelle, reparee) et 79 (majeure, recurrente).
- Empreinte de la BDD : `e56a87e265cd3cb2...`.
- Prochaine etape : **case 7** (execution par porte), sur les 73 verdicts
  `archiver`, avec les 5 refus et les invariants ci-dessus.
