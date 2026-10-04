---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# REVISION MO-304 -- LA REVISION VERIFIEE, ET SON CINQUIEME VERDICT

> Item EO-300 (demande createur, [revision]) : "verifier le fonctionnement des
> rotations, des .bak, des archives, des audits et des constats. Pourquoi
> vivent-ils si longtemps, si les informations importantes sont dans les BDD ?"
> Livrable attendu : la mesure de ce qui existe (qui cree quoi, qui survit
> combien de temps, ou c est lu), puis la politique proposee, avec preuve et garde.
>
> MO-305 a livre la MESURE (rapport-revision-MO-305.md) et la politique P1-P4 ;
> MO-306 a MO-311 les ont implementees. Ce round RE-MESURE chaque piece au lieu
> de la croire -- et nomme ce que la revision avait laisse dehors.

## 1. Les cinq objets, re-mesures le 2026-09-20

| Objet | Qui cree | Combien de temps il vit | Ou c est lu | Mesure du jour |
|---|---|---|---|---|
| `.bak` (points de restauration) | la porte `ecrire`, AVANT chaque publication | jusqu a la rotation : le plus recent reste EN PLACE, tout point remplace part a l archive | `revert-fichier.py`, le balayage, la rotation | 669 fichiers, 8,4 Mo (MO-305 : 1191 / 17,1 Mo le meme jour) |
| la ROTATION | `balayer` (decisions) puis `archiver --lot oui` (acte) | une famille ne garde qu UN point en place | `controler-borne`, `controler-plafond`, le revert | BORNE N=1 TENUE : 334 EN PLACE pour 351 familles ; 0 acte en attente (plafond 8) |
| les ARCHIVES | la rotation, au domicile `purification/archives` (zone invisible) | jusqu a la PREUVE de recouvrabilite (P3) -- sinon elle reste | `restaurer`, `controler-archives` | 343 fichiers, 7,3 Mo (897 / 18 Mo avant la purge MO-308 ; 115 / 3,2 Mo juste apres : l archive REGROSSIT, et c est mesure) |
| les AUDITS | les missions d audit, par la porte | tant qu ils sont CITES | les missions suivantes, les conventions | 4 documents, 2 jours, cites par 3, 5, 8 et 5 documents : ils vivent parce qu on les lit, pas par inertie |
| les CONSTATS | personne : il n y a PAS de famille `constat` | la duree de vie de leur document PORTEUR | la ou leur document est lu | aucun fichier ni dossier `*constat*` : le constat est une SECTION (audits, conventions, rapports) |

## 2. La politique, verifiee piece par piece (pas recopiee)

| Piece | La promesse | Comment elle est verifiee | Verdict |
|---|---|---|---|
| P1 (MO-306) | la fin du pilote JOUE la rotation au lieu de la declarer | `fin/fonctions.py` appelle `archiver_famille_conservation` ; mesure : 0 acte en attente | TENUE |
| P2 (MO-309) | hors le dernier point par famille, les `.bak` ages sortent du disque | `controler-borne` mesure la MEME borne des DEUX cotes (registre + disque) | TENUE (334 / 351, aucun exces) |
| P3 (MO-308) | une archive n est supprimee que RECOUVRABLE, preuve citee | `purger --lot oui` joue a chaque cloture ; 828 archives purgees, 0 anomalie | TENUE |
| P4 (MO-309) | un garde accuse au-dela d un plafond declare | `controler-plafond` : plafond 8, en attente 0 | TENUE |
| perimetre (MO-311) | chaque entree du registre est MESUREE ou DECLAREE avec son motif | `controler-archives` nomme 9 entrees hors perimetre declare | TENUE |

## 3. V5 -- ce que la revision avait laisse dehors

**(1) La purge de la zone jetable fabriquait des disparitions non declarees.**
La cloture vide `tmp-optimus` (regle immuable `perimetre-tmp`) -- et toute
ecriture faite dans cette zone a cree un POINT DE RESTAURATION enregistre. Le
fichier disparait donc avec la zone, mais le registre le gardait NON-ARCHIVE :
`controler-archives` le comptait en ECART (mesure : 7 points, 8 ecarts) et RIEN
ne pouvait le solder -- `archiver` exige un fichier a deplacer, `purger` exige
une archive. Ce n est pas un accident isole : 17 disparitions du meme genre
avaient ete DECLAREES A LA MAIN a EO-276, ou la porte `declarer-disparition` est
nee ; le stock s etait reconstitue tout seul, round apres round.

**(2) Le garde de la perte n etait joue par PERSONNE.**
La cloture lancait la borne (l EXCES) et le plafond (la MASSE), jamais
`controler-archives` (la PERTE : `archive + actif + disparu + purge = origine`).
Les 8 ecarts vivaient donc sans qu AUCUN instrument ne les voie -- et `/sante`
etait vert (13 portes) pendant ce temps. Un controle que personne ne lance ne
protege rien : c est la lecon d EO-152, vraie une troisieme fois.

**(3) Un nom qui disait une seule de ses trois causes.**
`crier_borne_rompue` servait deja au plafond, et allait servir a la perte : il est
devenu `crier_controle_conservation`.

## 4. La reparation (dans l outil, sur place -- regle immuable)

| # | Acte | Domicile |
|---|---|---|
| 1 | la cloture DECLARE les disparitions qu elle vient de causer, PAR la porte et APRES la purge | `pilote/commun.py` + `pilote/fin/fonctions.py` |
| 2 | la cloture JOUE le garde de la perte, apres les gestes qui doivent le satisfaire | `pilote/commun.py` + `pilote/fin/fonctions.py` |
| 3 | les DEUX chemins de cloture declarent : ils purgent tous les deux | `pilote/file/fonctions.py` |
| 4 | le cri commun aux trois controles porte un nom juste | `pilote/commun.py` |
| 5 | verbes, delais et raison declares UNE fois | `pilote/constants.py` |
| 6 | la doc du domicile dit les 8 gestes de la cloture, et leur ORDRE | `bdd-conservation/DESCRIPTION.md` |

L ORDRE porte la doctrine : on DECLARE le fait, PUIS on le mesure. La declaration
vient APRES la purge parce que la porte REFUSE un point encore PRESENT sur le
disque -- une declaration posee avant serait une intention.

## 5. Les preuves (rejouees, pas recopiees)

| Preuve | Mesure |
|---|---|
| CONTRE-TEMOIN : le defaut est reel et vu | `controler-archives` : 8 ECARTS, `disparu` = 21, code 1 |
| Le fait est CIBLE, pas devine | simulation du lot : POPULATION 7, ARRIVEE 7 / 7, 0 refus qui apprend quelque chose, RIEN ecrit |
| L acte passe par la FABRIQUE REPAREE | `declarer_disparitions_conservation` : 7 / 7 declarees, code 0 |
| Le garde n est pas rendu MUET | `disparu` 21 -> 28 : les memes faits passent d ACCUSES a COMPTES ; `archive + actif + purge + disparu = origine` se referme ; VERDICT OK, code 0 |
| IDEMPOTENCE | le lot rejoue : POPULATION 0, 0 anomalie -- le geste est donc sans cout a chaque cloture |
| py_compile | les 4 fichiers compilent, publies PAR la porte (imports locaux resolus) |
| NON-REGRESSION | VERDICT OK : non-regression VERTE (zone + flux), 32 maillons |
| /sante | OK : 13 portes vertes, 0 ecart, 0 dette |

Les 4 fichiers du pilote ont ete PUBLIES par la porte `ecrire` (empreintes avant
et apres annoncees, point de restauration pose). Leur CONTENU a ete prepare dans
l editeur de l agent : le point de la porte porte donc l etat PUBLIE, et l etat
d avant la modification vit dans les `.bak` anterieurs et dans git -- c est DIT,
pas suppose.

## 6. Ce qui reste, declare

- 109 archives de MO-308 restent SANS preuve de recouvrabilite : la porte REFUSE,
  et c est le contrat. Elles ne sortiront que si la preuve apparait.
- 25 des 28 declarees disparues n ont JAMAIS ete mesurees (le temoin les avait
  deja perdues) : le fait est declare, la mesure est avouee MANQUANTE, aucun
  octet n est invente.
- 9 entrees du registre vivent hors du perimetre declare (critere : `bak` absent
  des tags) : mesurees, nommees, non comptees dans l origine.
- L archive REGROSSIT entre deux preuves (115 -> 343 fichiers en un jour) : la
  purge ne peut pas aller plus vite que la preuve, c est la politique P3 -- mais
  la courbe est desormais mesuree a chaque cloture.

## 7. Suite

La revision est CLOSE : mesure (MO-305), politique (P1-P4), gardes (P1-P4 + la
perte), preuves et verification sont la. La question du createur -- "pourquoi
vivent-ils si longtemps ?" -- a une reponse MESUREE : les `.bak` vivent longtemps
par ABSENCE d acte (le stock repart de zero a chaque cloture depuis P1 et P2),
les archives par ABSENCE de preuve (P3), les audits et les constats parce qu on
les CITE -- et le constat n a pas de vie propre : c est une section de son
document porteur.
