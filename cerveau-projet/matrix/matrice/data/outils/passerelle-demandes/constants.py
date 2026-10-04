"""Constantes de l'outil passerelle-demandes.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
"""
import sys
from pathlib import Path

REPERTOIRE_OUTIL = Path(__file__).resolve().parent
REPERTOIRE_PARENT = REPERTOIRE_OUTIL.parent
if REPERTOIRE_PARENT.name != "outils" or REPERTOIRE_PARENT.parent.name != "data":
    raise RuntimeError(
        "Structure inattendue : " + str(REPERTOIRE_OUTIL) + " n'est pas dans data/outils/"
    )
REPERTOIRE_MATRICE = REPERTOIRE_PARENT.parent
REPERTOIRE_DATA = REPERTOIRE_PARENT

# LE CANAL. Sa source de verite est passerelle_user.est_passerelle_user (M-076) :
CHEMIN_CANAL = REPERTOIRE_MATRICE.parent / "user-demandes" / "user-demandes.md"

# Le LANCEUR : le depot passe par la PORTE officielle, jamais par une ecriture
CHEMIN_CANAL = REPERTOIRE_MATRICE.parent.parent / "user-demandes" / "user-demandes.md"
# auto-validation, ni role, ni trace dans la BDD -- ce serait un item fantome.
LANCEUR = REPERTOIRE_MATRICE.parent.parent / "lancer.py"

# La LECTURE du canal et son RETRAIT vivent au domicile partage
# (data/commun/passerelle_user.py) : cet outil ne les recopie pas, il les consomme.
CIRCUIT = REPERTOIRE_DATA.parent / "commun"
if not (CIRCUIT / "passerelle_user.py").is_file():
    raise RuntimeError("passerelle_user.py introuvable : " + str(CIRCUIT))
if str(CIRCUIT) not in sys.path:
    sys.path.insert(0, str(CIRCUIT))

# LES TYPES AJOUTES (decision createur 2026-09-30 : "creer les type manquante").
# Quatre types, un par INTENTION, mesures sur les crochets du user :
#   [question] -> question : le user attend une REPONSE, pas une construction ;
#   [???]      -> cadrage  : "construire la liste des actions AVANT de resoudre" ;
#   [cablage]  -> cablage  : un cycle de controle sur le CABLAGE d une ancienne ;
#   [preparer] -> preparer : un travail de preparation (le mot est celui du user).
# ILS N EXISTENT QUE COTE OPTIMUS (decision createur). Le flanc cameleon garde
# ses cinq types : le cameleon n a pas de passerelle user, donc lui donner ces
# types rendrait faux un type qu il ne peut jamais recevoir. La divergence est
# DECLAREE, avec sa raison, dans verifier-contrat-fondamental (NOMS_LIBRES_MIROIR) :
# elle est donc visible, jamais muette.

# LA TABLE crochet -> type. C est la SEULE traduction du vocabulaire du user vers
# celui de la Matrice ; elle est ecrite ENTIERE ici, pour qu une relecture puisse
# la contester d un seul regard. Un crochet INCONNU n est PAS devine : la demande
# est DITEE et laissee au canal. Deposer une demande du user sous un type choisi
# a sa place serait une decision prise a son detriment, qu il decouvrirait plus
# tard dans son entonnoir sans savoir pourquoi.
# LA TABLE crochet -> type : elle est lue a son DOMICILE, pas reecrite ici
# (MO-562, M-076). Elle avait deux consommateurs -- cet outil, et la porte
# `deposer` de l entonnoir, qui doit reconnaitre le crochet ecrit dans le
# titre -- et une copie chez chacun derivait silencieusement. Mesure :
# EO-482, une demande [question] saisie a la main, classee `dev`.
#
# Elle reste ecrite ENTIERE et contestable d un seul regard, au fichier
# passerelle_user.py -- on a deplace le DOMICILE, pas la regle.
from passerelle_user import CROCHETS_TYPES  # noqa: E402  (domicile commun)

ENCODAGE = "utf-8"
NOM_SOURCE = "user-demande"
SOURCE_ENTONNOIR = "createur"
URGENCE_DEFAUT = "normale"
INDENTATION_JSON = 2
NOM_ENTONNOIR_BRIQUE = "entonnoir"
NOM_CONFIRMER = "confirmer"
VERBE_DEPOT = "deposer"
APPELANT = "operateur"

# --- LE GARDE ANTI-DOUBLE-DEPOT (demande createur 2026-09-30) ---------------
# Deposer deux fois la meme demande gonflerait l entonnoir de 35 items fantomes.
# L etat de l entonnoir est ici lu en LECTURE SEULE, jamais ecrit : la seule
# ecriture passe par la porte.
CHEMIN_ENTONNOIR = (REPERTOIRE_MATRICE.parent.parent / "_operateur"
                     / "optimus-prime" / "pilote" / "entonnoir-files-optimus.json")

# La TRACE est la reconnaissance EXACTE : elle porte le numero de LIGNE de la
# demande dans le canal. Elle survit a une reecriture du texte par le createur,
# ce qu une comparaison de texte ne survit pas.
PREFIXE_TRACE = "canal"

# Les items deposes AVANT la trace (les 35 premiers) sont reconnus par le
# TEXTE. Le repli est dit comme tel : une correspondance de texte peut se
# tromper, une trace non.
MOTIF_TRACE = "ASCII : item depose par la passerelle"
