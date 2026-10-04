---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# AUDIT -- L INVENTAIRE DES BESOINS DE TEMPLATE, RE-MESURE (MO-527)

> Pourquoi cet audit existe, et pourquoi il ne reprend pas l analyse : MO-527 a ete
> ROUVRTE puis resservie, et son travail etait deja livre -- par MO-541, qui
> l dit dans son objectif (< Reprise du travail de MO-527 >). On necredite donc
> pas une restitution : on la MESURE (lecon de MO-548). L analyse d origine
> n est ni repetee ni corrigee sur place ; elle est lue, mesuree, et ce document
> dit ce qui tient, ce qui ne tient pas, et ce qui a ete corrige.

## 1. LA LIVRAISON DE MO-541 TIENT (mesure du 2026-10-02, 22 h 50)

| Ce qui est affirme | Ce qui est mesure |
|---|---|
| 3 moles invisibles crees dans le dossier que la porte sait lire | `_operateur/optimus-prime/suivi-pilote/templates/` : `conventions/convention.md.moule`, `regles-immuables/regle-immuable.md.moule`, `protocoles/protocole.md.moule` -- presents, lus par `poser-template-pilote lister` qui publie 6 moles |
| poses reelles | 3 poses REJOUEES ici (9, 9 et 8 jetons) : les trois artefacts naissent, sans jeton residuel |
| contre-temoin nomme | 3 REFUS joues : jeton manquant, jeton recu que le moule ne porte pas, cible deja presente (une pose n ecrase jamais) -- et aucun fichier ecrit dans les trois cas |
| auto-test 4/4 | rejoue : 4/4 |

L inventaire des 8 familles existe (`preparation/inventaire-besoins-template.md`,
94 lignes, RS-070). Le patron visible existe aussi et n attendait rien :
`matrice/templates/` (patron `outil-bdd`, consomme par `dupliquer-template`).

## 2. LES DEUX DEFAUTS TROUVES DANS LE TRAVAIL LIVRE, ET CORRIGES ICI

**2.1 Le patron embarquait son propre chantier dans chaque artefact pose.** Les
trois moles commencaient par une ligne qui affirme < ce fichier est un moule a
jetons > (FAUSSE dans une convention, une regle ou un protocole) et se terminaient
par deux sections de chantier : < LES JETONS > et < POURQUOI UN TEMPLATE >.
Mesures :
- la table < LES JETONS > est DETRUITE par la substitution -- la colonne `Jeton`
  tient alors la VALEUR (`optimus-prime`, `les liens vers les autres pieces`) ;
  elle ne peut donc plus dire ce qu elle pretend dire ;
- < POURQUOI UN TEMPLATE > atterrissait dans chaque document livre, et citait un
  compte perime : < la zone portait 23 regles >, il y en a **19**. Un chiffre faux
  recopie dans chaque enfant du patron est une dette qui se paie plus tard, sans
  que personne ne la voie venir ;
- la porte ECRIRE corrigeait mes guillemets (`< >` -> `< >`) sans le dire : le
  contenu publie n est pas toujours exactement celui qu on a ecrit. A relire apres
  ecriture, toujours.

Corrige : les trois blocs sont NES (deplaces dans le README du dossier, qui est
leur domicile), et les trois moles ne portent plus que la piece a livrer. Mesure
sur les artefacts poses : 0 ligne de chantier, 0 jeton residuel, 4 sections de
fond. Aucun jeton perdu : 9/9, 9/9, 8/8.

**2.2 Seize jetons n etaient documentes dans AUCUN domicile.** Le README du
dossier se declare < Les jetons (remplaces a la pose) > -- et il n en documentait
que 17 sur 33. Les 16 des trois familles invisibles (`__TITRE__`, `__LIENS__`,
`__REGLE__`, `__FORMAT__`, `__SOURCE__`, `__MESURE__`, `__REMPLACE__`,
`__CAS_LIMITES__`, `__CONTRE_EXEMPLE__`, `__PERIMETRE__`, `__EXCEPTION__`,
`__GARDE__`, `__NUMERO__`, `__QUAND__`, `__GESTES__`, `__ARRET__`, `__JUMELLE__`)
n y etaient pas : ils n Vivaient que dans les moles, ou ils ne peuvent pas se
decrire eux-memes. Corrige : chacun gagne sa SIGNIFICATION dans le README, et la
table dit ce qu elle ne dit pas -- quels jetons EXISTENT se lit dans les moles
(`lister` les publie jeton par jeton), donc aucune liste recopiee ne peut taire les
families de demain. C est le meme argument qui fait extraire un identifiant par
FORME plutot que par une liste (`_ids_dans`, MO-548).

## 3. LES 8 FAMILLES, RE-MESUREES (contredit l analyse sur deux points)

| # | Famille | L analyse du 2026-10-02 08 h dit | La mesure du 2026-10-02 22 h 55 dit |
|---|---|---|---|
| 1 | lecons | 52 entrees dans `matrice/data/lecons.json` | **226** entrees : le chiffre a peri, la famille est la |
| 2 | frictions | `frictions.db`, table `frictions`, outil `bdd-frictions` | confirme ; **102 lignes**, une seule base, un seul outil |
| 3 | regles immuables | **23 regles** + 1 readme | **19 regles** + 1 readme (`.bak` exclus) -- le compte est FAUX |
| 4 | conventions | 14 + 1 readme | 14 + 1 readme : confirme |
| 5 | protocoles | 14 numerotes + 1 readme | 14 numerotes + 1 readme : confirme |
| 6 | carte d identite | 4 pieces dans `matrice/templates/carte-identite/` | 4 pieces : confirme |
| 7 | informations systeme | **la famille N EXISTE PAS** (zero fichier, zero porte) | **FAUX** : `matrice/data/systeme-machine.md` (3 209 o, carte `type: fiche`) existe, et l outil `inventaire-systeme` (fiche / mesure / verif) le tient a jour ; l injection en sert la section `RESUME MACHINE` |
| 8 | environnement de travail | la famille n existe pas | confirme : rien de ce nom ; le plus proche est `USER-PROFIL.md` (profil utilisateur, injecte sous le champ `profil`) |

Consequence sur EO-547 (< la zone informations systeme doit-elle exister ? >) : la
question n est plus < existe-t-elle ? > -- elle existe, sous le nom de fiche
machine -- mais < la fiche machine suffit-elle, ou faut-il une zone distincte ? >.
C est une decision de createur, pas d agent ; elle reste donc ouverte, avec la
mesure qui l informe.

## 4. L ERREUR QUI A FAIT ROUVRIR MO-527 (la plus instructive des trois)

Le motif de la rouverture de MO-527 (2026-10-02 22:34:30) affirme : < cette
restitution est MESUREE FAUSSE : l entonnoir ne porte aucun item depose ce
jour-la >. La mesure etait juste, l INFERENCE etait fausse : un item consomme
n est plus dans l entonnoir, donc l absence actuelle ne prouve rien sur une
presence anterieure.

La mesure qui le dit : l item **EO-546** a ete depose le 2026-10-02 **07:15:55** --
cinq secondes apres la declaration du 07:15:50 qui annoncait le re-depot -- et
consomme le 2026-10-02 08:02:17. Il est devenu MO-541. La restitution etait donc
VRAIE, et le travail de MO-527 n a jamais ete perdu : il a ete livre par MO-541.

Ce qui reste justifie dans la rouverture : le bilan de MO-527 portait celui de
MO-539, il etait faux, et le retirer reste la bonne decision -- pour cette seule
raison, et non celle d un porteur manquant. La correction est DECLAREE au journal
(action `decouverte` sur MO-527) et la trace n est pas reecrite.

## 5. CE QUI RESTE OUVERT, ET UNE MESURE QUI EN EST NUE

- **La meme demande est entree deux fois** : EO-519 depose le 2026-09-30 09:43
  (consomme 2026-10-01 20:47 -> MO-527), puis EO-546 depose le 2026-10-02 07:15
  (consomme 08:02 -> MO-541). Deux items, donc deux missions, pour un seul
  travail : c est exactement ainsi qu un bilan d autrui s est installe sous
  MO-527. Aussoit un garde : une demande identique deposee deux fois dans la
  memoire de naissance.
- **La forme des lecons et des frictions** (`matrice/data/lecons.json`,
  `matrice/data/frictions.db`) : pas d artefact a fabriquer, mais une FORME a
  declarer une fois la ou la porte la lit. MO-541 le dit et le renvoie a une autre
  mission ; ce n est pas fait.
- **EO-547**, avec la mesure du point 3.
