---
identite:
  type: routeur-maintenance
  appartient_a: matrice-routines
  version: 1.0.0
---

# Routeur MATRICE -> MAINTENANCE

## Role

Ce routeur lit la boite `matrice/intercom/matrice/inbox.jsonl`,
detecte les messages de type `signaler`, et les route vers
`_operateur/maintenance/matrice/inbox.jsonl` pour qu'Optimus
les traite.

## Usage

```
python3 routeur.py tour        (une passe)
python3 routeur.py boucle      (veille continue)
python3 routeur.py boucle arret (arret cooperatif)
python3 routeur.py rotation [--racine <matrix>] [--seuil <octets>] [--gardes <n>] [--force]
```

## Flux

```
inbox matrice/ (signaler) -> routeur -> maintenance/matrice/inbox.jsonl -> Optimus
```

## Regles

- Append-only sur maintenance (jamais de reecriture)
- Marque les messages traites dans l'historique
- Ne route QUE les messages de type `signaler`
- Les autres messages restent dans inbox matrice (inchanges)

## Rotation du journal (MO-079)

Le routeur etait le DERNIER journal de routine sans borne : mesure du 2026-09-14,
1919 lignes / 296 Ko en 2 jours (une passe toutes les 30 s).

Le moteur est PARTAGE (`matrice/data/commun/rotation_journal.py`, motif unique
M-076) : cette routine ne declare que SES valeurs. Les trois invariants --
*archiver d'abord / reecrire ensuite / controler apres* -- sont ceux du moteur :

- l'archive DATEE (`routeur-archive-AAAAMMJJ.jsonl`) fait partie du "deja connu"
  (lecon L-040) : une reprise apres un arret n'ecrit aucun jumeau ;
- une COURSE (journal modifie entre la lecture et le remplacement) est REFUSEE en
  la nommant apres 3 essais -- jamais ecrasee ;
- rien ne se supprime jamais : le borner, c'est DEPLACER ses evenements anciens.

Seuils : `SEUIL_OCTETS_JOURNAL` (512 Ko), `EVENEMENTS_GARDES_JOURNAL` (500),
`ESSAIS_ROTATION` (3). Le declenchement se LIT (une taille), et la boucle verifie
la rotation AVANT chaque passe -- un refus ne tue jamais la passe (lecon L-026).

## Etat et histoire (MO-080)

Le routeur ecrivait une ligne d'historique a CHAQUE passe. Mesure du 2026-09-14 :
sur 512 lignes, 510 etaient le MEME tableau a la date pres (99,4 %), une toutes les
30 s, soit ~150 Ko par jour pour rien.

La passe separe desormais DEUX objets, aux durees de vie differentes :

| | |
|---|---|
| `routeur-etat.json` | l'**ETAT** : le tableau COURANT des boites, ecrit a CHAQUE passe et ECRASE |
| `routeur-historique.jsonl` | l'**HISTOIRE** : une suite de FAITS, en ajout seul |

Un FAIT, ici, c'est : du courrier a ete **ROUTE** (chaque message route compte,
meme si le compte se repete d'une passe a l'autre), ou le tableau des **ANOMALIES**
a change (une anomalie apparait, evolue, disparait). L'inbox qui se remplit de
trafic **NORMAL** (`fin-mission`, `retour-lot`) est un ETAT : elle va dans l'etat,
jamais dans l'histoire -- sinon le journal suivrait la boite au lieu des faits.

L'etat porte la date de la passe, la date de la DERNIERE ligne ecrite et le nombre
de passes absorbees depuis : la redondance supprimee est **TRACEE**, jamais
silencieuse, et l'etat distingue "rien a ecrire" de "la routine est morte"
(le nombre de passes absorbees AVANCE a chaque tour).

Garde permanent : `verifier-historique-non-redondant.py` (non-regression, maillon
14) -- il joue la VRAIE passe sur un cobaye et s'AUTOTESTE en rejouant l'ancienne
regle, qu'il doit ACCUSER.

## Cadence publiee (MO-079)

La cadence EFFECTIVE est publiee dans un etat COURT `routeur-cadence.json` (une
ligne, ecriture atomique), EN PLUS de l'evenement `demarrage` du journal.

Pourquoi les deux : le journal est desormais ROTATIONNE, donc un jour l'evenement
de `demarrage` quitte le journal actif pour l'archive -- un controle qui chercherait
la cadence DANS LE JOURNAL deviendrait AVEUGLE, c'est-a-dire neutralise par le
nettoyage qu'il surveille (lecon L-040). Un etat se lit dans un fichier d'etat,
une histoire dans un journal. `verifier-sans-attendre` lit desormais
`routeur-cadence.json`.

## Anneau de passes et cadence MESUREE (friction 28, MO-084)

L'etat de passe (`routeur-etat.json`) porte aussi `dernieres_passes` -- les
`PASSES_GARDEES_ETAT` derniers horodatages de passe, fabriques par le moteur
PARTAGE `data/commun/battement.py` (le routeur ne declare que sa longueur).

DECLARER une cadence, la PUBLIER dans un etat court, et la MESURER sont trois
choses differentes : `verifier-cadence` lit cet anneau et prend l'ecart MEDIAN.
Le routeur est ici le plus fin des temoins -- une passe toutes les 30 s -- donc le
premier chez qui une derive se verrait.

Pourquoi pas une moyenne : `(date - derniere_ecriture) / passes_absorbes` ne
decrit AUCUN intervalle reel des qu'une passe n'est pas a l'heure (redemarrage,
passe a la demande). Mesure sur une vigie jumelle : 450,5 s puis 600,3 s pour une
cadence de 900 s prouvee par le journal. Une valeur fausse mais DANS la tolerance
ne crie pas.
