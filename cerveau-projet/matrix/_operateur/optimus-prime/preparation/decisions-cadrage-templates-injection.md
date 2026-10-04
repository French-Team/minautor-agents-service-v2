---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# DECISIONS DU CADRAGE < templates d injection > (D1 a D5)

> Repondues le 2026-09-26 par l OPERATEUR, a la demande du createur (< repondre aux 5
> decisions D1-D5 du cadrage pour debloquer la mission de construction >). Chaque
> decision s APPUIE sur les mesures de la chaine (MO-428, MO-433, MO-436, MO-439, MO-442,
> MO-459) ; chacune se RE-MESURE par le disque, jamais par la memoire.

## D1 -- FORME ET DOMICILE : ARTEFACT DU PILOTE
Un template d injection vit AVEC le catalogue qu il sert :
`_operateur/optimus-prime/pilote/injection/templates/<categorie>/<nom>.moule`, consomme
par `injecter.py`. RAISON MESUREE : le moule generateur de `matrice/templates/` (CV-014) est
consomme par `dupliquer-template`, qui DUPLIQUE des vivants ; une injection n est pas
DUPLIQUEE, elle est SERVIE par `injecter.py`. Poser les injections sous `matrice/templates/`
creerait un SECOND consommateur et un domicile menteur.

## D2 -- LA FICHE TECHNIQUE RESUME (jamais ne remplace)
Elle PORTE l essentiel BORNE (objectif, checklist, role/type, preuve attendue, outils et
domiciles) ; l injection reste ENTIERE et intacte ; le reste (lecons_utiles, themes_utiles,
modes_emploi, profil) reste joignable A LA DEMANDE. Lecteur : l AGENT, au debut du round
(c est deja `remettre_les_ordres` qui l imprime ; la fiche en est la version BORNEE et
CANONIQUE). < Sans perte > = on ne retire rien de ce qui DECIDE.

## D3 -- LE BRUIT : LES DEUX, priorite au POIDS
(a) POIDS : declarer un PLAFOND GLOBAL d injection (aujourd hui ~10 000 tokens mesures sans
plafond global ; seul PLAFOND_LEGONS_TOKENS = 6000 existe) et le FAIRE RESPECTER.
(b) CONVERSATIONNEL : MESURER ce qui est re-imprime a chaque round et le borner. La mesure
du poids existe deja (`injecter.py <categorie> --peser`).

## D4 -- CHAMPS_PESES : NOYAU OBLIGATOIRE + AJUSTABLES BORNES
NOYAU (jamais retire) : objectif, checklist, role, rappel, auto_validation, recherche.
AJUSTABLES (bornes, ou sur demande) : lecons_utiles, themes_utiles, modes_emploi, profil,
si_j_etais_user.

## D5 -- COUVERTURE : LES QUATRE CATEGORIES
demarrage, avant-mission, pendant-mission, apres-mission. Le DEMARRAGE est le lieu des
patterns (EO-446 : pattern de maintenance injecte au demarrage) : c est la qu un template
apporte le plus.

## CE QUI DEBLOQUE
La < mission de construction > : un OUTIL qui rend (1) les TEMPLATES d injection (D1, D5) et
(2) la FICHE TECHNIQUE DE TRAVAIL bornee (D2, D3, D4), avec un cobaye qui prouve que la fiche
est PLUS LEGERE sans rien perdre de ce qui decide.

## D6 -- LA FORME DU TEMPLATE : UN MOULE DE LA FICHE TECHNIQUE
Tranche le 2026-09-26 (l OPERATEUR decide, a la demande du createur : < tu dois
trancher >). Un template d injection est le MOULE A JETONS de la FICHE TECHNIQUE de
SA categorie, au domicile D1 : `pilote/injection/templates/<categorie>/fiche.moule`.
Il est RENDU par la porte `injecter.py` (verbe `fiche <categorie>`) et n est JAMAIS
execute seul -- meme convention que les gabarits invisibles du pilote. Jetons servis
par le moteur : CATEGORIE, DATE, NB_SOURCES, SOURCES. RAISON : la demande veut une
FICHE TECHNIQUE DE TRAVAIL (alleger sans perte) ; un moule PAR CATEGORIE laisse
chaque phase evoluer seule, et un jeton INCONNU est un REFUS nomme -- jamais un
remplacement muet (L-055). Les QUATRE moules existent (demarrage, avant-mission,
pendant-mission, apres-mission).
PREUVE MESUREE (peseur du domicile partage) : injection 441268 tokens contre fiche
1214 tokens (--99,7 pour cent), le contenu restant joignable a sa porte ; maillon 48
(mordant EN MEMOIRE) ; non-regression VERTE.
