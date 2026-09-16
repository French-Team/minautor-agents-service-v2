---
identite:
  type: plan-preparation-conservation
  appartient_a: optimus-prime
  commun: false
  mission: MO-094
  statut: valide
---

# MO-094 -- PLAN DE PREPARATION-CONSERVATION

> Mission de preparation validee par le createur le 2026-09-15.
> Cette mission ne deplace, ne reecrit et ne supprime aucune donnee existante.
> Elle prepare la mission CREER-OUTIL qui produira la BDD de conservation.

## 1. Decision et perimetre

- Perimetre principal : toute la Matrice v3 sous `cerveau-projet/matrix/`.
- Flux 2 : analyse, preparation et execution future par Optimus.
- Flux 1 et cameleon : lecture et protection uniquement ; aucune ecriture.
- Fichiers v1/v2 : lecture seule ; aucune migration implicite.
- Suppression : interdite dans cette serie de preparation.
- Anciens correctifs : classer avant de decider.
- Automatisation : routeur-maintenance seulement apres mesure et decision tracee.

Le perimetre de lecture sert a verifier les dependances. Le perimetre
d ecriture de toute operation future reste celui de `matrix/` et de ses
portes officielles.

## 2. Categories de conservation

Chaque element inventorie recoit une categorie unique :

| Categorie | Definition | Action initiale |
|---|---|---|
| VIVANT | Lu ou ecrit par un flux actif | Conserver |
| STRUCTUREL | Necessaire a une porte, un parcours ou un controle | Conserver |
| GENERE | Vue reconstruisible depuis une source | Conserver la source, regenerer la vue |
| HISTORIQUE | Preuve d une action ou d un etat passe | Conserver dans son emplacement ou archive connue |
| OBSOLETE | Remplace et non necessaire au fonctionnement courant | Classer, puis decision |
| COBAYE | Donnee de test isolee et identifiee | Classer, puis decision |
| ORPHELIN | Sans lecteur ou reference mesuree | Ne pas toucher avant contre-analyse |
| HORS-PERIMETRE | Appartient a Flux 1, cameleon ou hors matrix/ | Signaler, aucune ecriture |

Un age ancien ne suffit jamais a classer un element OBSOLETE.

## 3. Statuts de cycle

La future BDD de conservation utilisera des statuts ordonnes :

1. `propose` : element inventorie, aucune decision.
2. `classe` : categorie et preuve d usage etablies.
3. `decide` : verdict rendu par la case decision.
4. `archive` : deplacement execute par une porte et verifie.
5. `conserve` : element confirme dans son emplacement canonique.
6. `repare` : element corrige par sa porte puis recontrole.
7. `dette` : ecart assume, inscrit avec cause et prochaine action.
8. `signale` : hors perimetre ou action non autorisee.
9. `restaure` : element revenu depuis une archive, preuves conservees.

Les transitions interdites sont refusees par la porte. En particulier,
un element ne passe jamais directement de `propose` a `archive`.

## 4. Schema propose pour la BDD conservation

Nom propose de l outil : `bdd-conservation`.
Nom propose de la BDD : `conservation.json`.
Prefixe propose : `K`.
La creation sera faite par `dupliquer-template` dans une mission
CREER-OUTIL separee, apres validation technique du schema.

Structure minimale d une entree :

```text
id, date, mission, source, destination, categorie, statut, verdict,
raison, lecteurs, ecrivains, index, sha_avant, sha_apres,
octets_avant, octets_apres, lignes_avant, lignes_apres,
restaurable, operation, archive, preuve
```

Regles de la BDD :

- une entree par element et par operation de conservation ;
- identifiant unique avec prefixe `K-` ;
- categorie, statut, verdict et operation en listes fermees ;
- chemins relatifs a la racine `matrix/` ;
- `destination` obligatoire pour une archive ;
- `sha_avant` obligatoire avant tout deplacement ;
- `sha_apres` obligatoire apres copie ou deplacement ;
- lecteurs et ecrivains mesures avant decision ;
- `restaurable` ne vaut vrai qu avec une preuve de restauration ;
- ecriture atomique, LF, ASCII et empreinte SHA ;
- aucune entree ne remplace l historique des BDD existantes.

## 5. Portes a creer dans la mission d outillage

La future porte `bdd-conservation` devra fournir au minimum :

- `proposer` : enregistrer un element mesure sans action ;
- `classer` : attribuer une categorie et ses preuves ;
- `decider` : enregistrer un verdict unique ;
- `lire` : filtrer par categorie, statut, mission ou chemin ;
- `verifier` : controler structure, ids, chemins et empreinte ;
- `manifeste` : produire les preuves d une operation ;
- `restaurer` : preparer ou executer une restauration autorisee ;
- `archiver` : deplacer seulement apres un verdict archive ;
- `marquer-obsolete` : conserver l element et sa raison, sans retrait.

La porte `archiver` devra refuser :

- un element sans lecteur recense ;
- un element sans SHA avant ;
- un element sans decision ;
- une destination deja occupee par un contenu different ;
- une operation hors `matrix/` ;
- une archive non inscrite au manifeste.

## 6. Manifeste d archive

Chaque operation d archivage produira un manifeste append-only ou un
fichier de preuve associe, sans remplacer les BDD historiques. Il contiendra :

- identifiant `K-XXX` ;
- date et mission ;
- source et destination ;
- categorie et verdict ;
- hash avant et apres ;
- nombre de fichiers, lignes et octets ;
- lecteurs et ecrivains recenses ;
- index et registres mis a jour ;
- preuve de lecture depuis l archive ;
- preuve de restauration sur cobaye ;
- resultat des gardes avant et apres.

Une archive n est pas consideree comme connue tant que son manifeste,
son index et le registre de controle ne la referencent pas.

## 7. Parcours PURIFICATION cible

La chaine cible devient :

```text
demande -> cartographie -> classification -> audit -> contre-analyse
-> decision -> execution-par-porte -> verification -> bilan
```

### Demande

Cadrer le perimetre, l objectif chiffre, la mission et l interdiction de
suppression.

### Cartographie

Inventorier fichiers, BDD, journaux, registres, index, archives, lecteurs,
ecrivains et portes.

### Classification

Attribuer une categorie unique a chaque element, avec une preuve et un
statut `classe`.

### Audit

Passer les gardes existants en lecture seule. Produire un ecart par ligne,
avec fichier, ligne, garde, gravite et preuve.

### Contre-analyse

Appliquer les trois axes Nemesis : cas limites, optimisation, securite.
Recenser les lecteurs avant tout archivage.

### Decision

Rendre un verdict unique par ecart : `conserver`, `archiver`, `reparer`,
`dette` ou `signaler`.

### Execution par porte

Utiliser uniquement la porte de la BDD, de l archive, du fichier ou du
journal concernee. Aucun contournement manuel.

### Verification

Verifier les donnees, index, empreintes, lecteurs, archives, Flux 2 et la
non-modification de Flux 1.

### Bilan

Tracer le resultat dans `bdd-conservation`, `bdd-modifications`,
`bdd-historique`, `suivi-optimus` et `bdd-sessions`.

## 8. Serie de missions proposee

La preparation produit la serie suivante, en serie stricte :

| Ordre | Mission | Objet | Ecriture |
|---|---|---|---|
| 1 | MO-095 | Creer `bdd-conservation` et ses portes | Nouvelle BDD seulement |
| 2 | MO-096 | Cartographier toute la Matrice v3 | Rapport et BDD |
| 3 | MO-097 | Classer les fichiers et correctifs | BDD seulement |
| 4 | MO-098 | Classer les BDD et journaux | BDD seulement |
| 5 | MO-099 | Audit des index, routes et vues | Reparations decidees ensuite |
| 6 | MO-100 | Contre-analyse et decisions par groupes | BDD de decisions |
| 7 | MO-101 | Archiver les elements valides | Portes d archive |
| 8 | MO-102 | Purifier les BDD et journaux | Portes propres a chaque source |
| 9 | MO-103 | Verifier restauration, registres et non-regression | Preuves et bilan |
| 10 | MO-104 | Mesurer le besoin d automatisation du routeur | Aucune routine par defaut |

Les numeros sont une proposition de preparation. Ils ne doivent etre
charges dans le pilote qu apres creation de la BDD et validation des
dependances par le pilote.

## 9. Criteres de validation

La preparation est validee si :

- le schema possede une porte unique et un verifier ;
- les categories, statuts, verdicts et transitions sont fermes ;
- tout deplacement exige un manifeste et deux empreintes ;
- une restauration de cobaye est prouvee ;
- les lecteurs sont recenses avant archivage ;
- les archives restent visibles des controles ;
- Flux 1 et cameleon ne sont jamais ecrits ;
- aucune suppression n est executee par MO-094 ;
- la serie est ordonnee et dependancee ;
- les resultats sont traces dans les BDD existantes.

## 10. Etat de fin MO-094

- Preparation validee par le createur : oui.
- BDD conservation creee : non, mission MO-095.
- Fichier existant deplace : non.
- Fichier existant supprime : non.
- Flux 1 modifie : non.
- Cameleon modifie : non.
- Routine de purification creee : non.
- Prochaine etape : MO-095, creation de `bdd-conservation` par le moule.
