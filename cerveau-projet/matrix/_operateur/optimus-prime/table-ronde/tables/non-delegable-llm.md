---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
  maj: 2026-10-02
---

# TABLE RONDE REELLE 1 -- non-delegable-llm (MO-549)

> La premiere table ronde jouee sur un sujet reel, le 2026-10-02. 15 analyses
> deposees par la porte `bdd-raisonnement`, 3 rounds complets, arbitrage rendu.

## LE TEMOIN : OU SONT LES ANALYSES

Les 15 analyses sont des SEGMENTS, tags `table-ronde`, slug `non-delegable-llm`
dans le champ `source` :

| Round | Segments |
|---|---|
| R1 | RS-095 BESOIN, RS-096 VIVANT, RS-097 DUREE, RS-099 KARPATHY, RS-100 NEMESIS |
| R2 | RS-101 BESOIN, RS-102 VIVANT, RS-103 DUREE, RS-105 KARPATHY, RS-106 NEMESIS |
| R3 | RS-107 BESOIN, RS-108 VIVANT, RS-109 DUREE, RS-110 KARPATHY, RS-111 NEMESIS |

Trois segments ont ete RETIRES et traces (le outil ne se rejoue pas) :
RS-098 et RS-104 pour un texte corrompu a la generation, RS-104 pour un accent
la ou le projet impose l ASCII.

## L ARBITRAGE

    sc-007-table-ronde arbitrer --table non-delegable-llm <synthese>
    -> Profils nommes dans la synthese : 5/5
    -> Verdicts prononces : 3 (d accord, reserve, opposition)
    -> Analyses inexpliquees hors boucle : 0

La synthese integralement prononcee est dans ce fichier, section par profil.

## CE QUE LA TABLE A TRANCHE

1. Il n y a PAS de "socle non-delegable" a ecrire. Six controles existent ; trois
   sont reellement protecteurs (attribution, perimetre/ASCII, coherence de file).
   Head-coherent controle un visuel, bdd-modifications est un journal, et
   registre-outils a un angle mort mesure. Pas de septieme domicile.
2. LE NON-DELEGABLE tient en une ligne : une affirmation de travail doit etre
   rattachee a un fait mesure sur le disque, sinon elle est declarative.
3. LA SURFACE est le verdict de fin de round : une ligne, formulee par la
   Matrice, jamais par l agent qui affirme.
4. L opposition de NEMESIS est RETENUE COMME CONDITION, pas levee : le controle
   doit etre joue hors de la mission, sinon il produit un vert qui ment.
5. Tout le reste reste DELEGABLE : redaction, analyse, code, synthese, methode.
   L agent decide quoi faire ; il ne decide pas si c est fait.

## LA SYNTESE PRONONCEE

- BESOIN -- d accord : une surface, pas une liste ; la seule question du createur
  est "puis-je fermer mon poste, ou dois-je verifier ?".
- VIVANT -- d accord : sur six controles, trois ne contraignent pas l agent ; le
  couplage existe entre un bilan et une identite, pas entre un bilan et un fait.
- DUREE -- reserve : le triage a un seul trou est accepte, mais son critere de
  selection est un jugement de valeur ; dix lignes molles coutent plus cher que
  deux lignes dures, a cause du bruit.
- KARPATHY -- d accord : un controle de plus, pas dix ; si le controle n est pas
  joue dans le round qui suit, cette table aura produit de la prose.
- NEMESIS -- opposition : la note de modification est ecrite par l agent qui
  affirme, donc le couplage lie l affirmation a une seconde affirmation, pas a
  un fait.

## LA SUITE : TROIS MISSIONS DEPOSEES PAR LA PORTE

| Mission | Objet |
|---|---|
| EO-555 | coupler une affirmation de travail a un fait sur le disque, joue hors de la mission |
| EO-556 | cabler les trois BDD declarees vivantes et joignables par aucun nom |
| MO-548 | le verbe `pilote rouvrir` (deja depose en EO-553, non duplique ici) |

## CE QUE LA TABLE A COUTE, ET CE QU ELLE A APPRIS

Trois segment(s) ont du etre retires et rejoues : une trace corrompue dans une
deliberation ne peut pas rester, parce qu elle ferme une decision. Le garde qui a
protege les depots a lui-meme produit un faux positif (frictions.db lu comme une
soudure) et a arrete le travail -- un garde qui bloque sur une heuristique est
plus cher que la faute qu il traque. Il a ete repare par LISTE BLANCHE
d extensions, contre-temoin joue.

COUT EN SEGMENTS : 18 (15 analyses, 3 retraits traces).
