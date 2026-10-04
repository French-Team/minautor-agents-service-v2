---
identite:
  type: analyse
  appartient_a: optimus-prime
  commun: false
---

# AUDIT -- LE MOTEUR DE RECHERCHE : LA CARTE PAR TYPE, ET LES 0 DU LANGAGE NATUREL

> Consigne (mission MO-368, EO-321) : MESURER (a) si les missions dev et reparation
> recoivent la carte de mode d emploi du moteur de recherche, et (b) le taux de 0 du
> moteur sur des requetes en langage naturel, avec la CAUSE de chaque 0.
> AUDIT = lecture seule : aucun fichier de service modifie, aucun ecart repare ici. Chaque
> ligne porte son domicile (fichier:ligne) ou sa mesure.

## A. LA CARTE PAR TYPE -- LA PREMISSE EST PERIMEE (mesure)

Domiciles : checklist/listes.py (OUTILS_TOUJOURS, OUTILS_COMMUNS, OUTILS_PAR_TYPE) ;
injection/fonctions.py (_noms_des_outils, _avec_plancher, charger_modes_emploi).

MESURE des 5 types (charger_modes_emploi sur une mission {type: t}) :

| type | outils | 1er outil | carte du moteur | introuvables | ecartes_par_plafond |
|---|---|---|---|---|---|
| dev | 7 | rechercher | OUI (3 994 o) | [] | [] |
| reparation | 7 | rechercher | OUI | [] | [] |
| doc | 6 | rechercher | OUI | [] | [] |
| audit | 5 | rechercher | OUI | [] | [] |
| revision | 6 | rechercher | OUI | [] | [] |

La liste reelle pour `dev` : rechercher, bdd-modifications, suivi-optimus,
lanceur-non-regression.py, creer-outil.py, ecrire, verifier-contrats-outils.py -- le moteur
est le PREMIER, et sa carte (mode d emploi EXTRAIT de la brique, 563 o) est servie.

VERDICT : la premisse est PERIMEE. Le defaut qu elle decrit a ete REPARE le 2026-09-21, et
le code le DIT lui-meme : _avec_plancher (injection/fonctions.py:337) porte la mesure
d origine -- < le moteur de recherche etait absent de dev et reparation, donc l agent
cherchait avec son outil natif -- qui ne connait ni les cartes, ni les BDD, ni les zones
invisibles >. La reparation est le PLANCHER (OUTILS_TOUJOURS = rechercher), place EN TETE
et non a la fin : le plafond coupe par la FIN, donc un outil essentiel place dernier
aurait pu etre ecarte en silence.

CE QUE LA PREMISSE APPREND : une mesure PERIMEE se lit comme un fait (L-055, la meme classe
que le visuel perime de MO-366). Le remede n est pas de < reparer > une seconde fois : il
est de MESURER AVANT de croire. Rien n a donc ete repare ici -- il n y avait rien a
reparer.

DETAIL utile : `introuvables` et `ecartes_par_plafond` sont VIDES pour les 5 types. Les
deux champs sont servis par la porte (une brique declaree introuvable se DIT) : leur
vacuite est une mesure, pas une supposition.

## B. LE MOTEUR ET LE LANGAGE NATUREL -- 5 ZEROS SUR 12 REQUETES REELLES

MESURE (rechercher --requete <q> --dans tous) :

| requete | resultats |
|---|---|
| outil natif | 0 |
| outils natifs | 0 |
| injection des lecons | 0 |
| carte de mode emploi | 0 |
| le chemin du bilan | 0 |
| plafond des actes en attente | 10 |
| cause racine | 2 |
| natif | 25 |
| lecon | 35 |
| defcon | 85 |
| rechercher | 49 |
| ecrire | 345 |

TAUX : 5 zeros sur 12 requetes (42 %). Les 5 zeros sont TOUS des requetes a PLUSIEURS MOTS
dont la phrase n existe pas litteralement ; les requetes a UN mot rendent toujours quelque
chose (25 a 345), et une phrase qui existe telle quelle rend un peu (10, 2).

CAUSE RACINE, MESUREE DANS LE CODE : la requete est compilee comme un MOTIF REGEX, jamais
decoupee en TERMES.
  - matrice/data/outils/rechercher/commun.py:171 : pattern = re.compile(requete, re.IGNORECASE) (fichiers) ;
  - matrice/data/outils/rechercher/commun.py:318 : idem (BDD).
Consequence 1 : une phrase ne trouve que les lignes qui la CONTIENNENT ; < outil natif >
ne rend rien alors que < natif > en rend 25 -- le disque contient bien des < outils
natifs >, mais jamais cette suite de mots.
Consequence 2 : un METACARACTERE change le SENS de la requete (la requete n est pas du
texte, c est un motif) -- voir l ecart EC-B2.

EC-B2 (GRAVE, mesure) : un motif INVALIDE fait CRASHER le moteur. `--requete "["` rend
`re.PatternError: unterminated character set at position 0` et un TRACEBACK Python, pas un
refus nomme. Un refus de porte doit NOMMER le probleme et le remede ; un crash n enonce
aucun remede, et il est la seule forme que la doctrine interdit sans exception. Mesure de
la meme famille a prevoir : tout caractere de motif ( [ ( * ? + ) rejetterait ou
deformerait de la meme facon.

## C. ECARTS DEPOSES (signales a la Matrice, jamais corriges ici)

EC-B1 (MOYENNE) -- les requetes en langage naturel rendent 0 : le moteur ne decoupe pas la
requete en termes (regex unique). 5 zeros sur 12 mesures, dont la requete qui DECRIT ce
qu on cherche (< carte de mode emploi >). Depose.
EC-B2 (HAUTE) -- un motif invalide CRASHE le moteur au lieu de le REFUSER en le nommant.

## D. LIMITES DITES

- Les 12 requetes sont MESUREES mais choisies par moi : elles sont representatives du
  langage naturel, pas un echantillon aleatoire.
- La cause est etablie par la LECTURE du code (les deux compilations) ET par la mesure
  (les 5 zeros) ; je n ai pas instrumente l execution du moteur pour compter les
  comparaisons.
- Cet audit ne tranche PAS la forme du remede (decouper en termes ? requete exacte par
  defaut avec une option motif ? refuser un motif invalide ?) : c est une DECISION, hors du
  perimetre d un AUDITEUR.
