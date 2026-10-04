"""Constantes de la routine chien -- squelette du moule routine.

declenche sur changement : observe, compare, lance le combo de correction en arriere-plan, puis se tait
"""
import sys
from pathlib import Path

REPERTOIRE_ROUTINE = Path(__file__).resolve().parent

# data/commun (motif unique M-076) : l'insertion montait d'UN CRAN DE TROP
# (`matrice/routines/data/commun`, dossier inexistant) : elle etait MORTE depuis
# toujours. Rien ne le voyait parce que chien n'avait jamais eu besoin du
# module partage ; la premiere tentative d'import l'a revele.
REPERTOIRE_COMMUN = REPERTOIRE_ROUTINE.parent.parent / "data" / "commun"
if not (REPERTOIRE_COMMUN / "attente.py").is_file():
    raise RuntimeError(
        "Motif attente introuvable : " + str(REPERTOIRE_COMMUN / "attente.py")
    )
sys.path.insert(0, str(REPERTOIRE_COMMUN))

INTERVALLE_SECONDS = 300
# Nom CANONIQUE de la cadence declaree, lu par `vie etat` : on LIT la cadence
# au lieu de l'attendre (attendre n'est pas verifier). Meme valeur, meme objet.
INTERVALLE_DECLARE_SECONDES = INTERVALLE_SECONDS
ENCODAGE = "utf-8"

# --- LE CHIEN (MO-564) : ce qu il surveille, et le SEUL domaine de la correction -
# La cadence vit au PLANNING (decision createur D1, MO-429), comme toute routine
# de fond : elle est LUE, pas comptee a la main. On ne fige donc pas 300 ici --
# le chien doit tourner bien plus vite que la veille, sinon il ne raccourcit rien.
from planning_routines import cadence_planning  # noqa: E402

NOM_ROUTINE = "chien"
# La forme LITERAL est exigee par le controle de cadence : il veut lire
# `cadence_planning('chien')` dans le texte, pas un nom passe par une variable. Il
# a raison : une constante interposee luirierait de voir d ou vient la cadence,
# et c est precisement ce que le controle vient verifier.
INTERVALLE_SECONDS = cadence_planning('chien')
INTERVALLE_DECLARE_SECONDES = INTERVALLE_SECONDS

# CE QUE LE CHIEN SURVEILLE : les memes reperes que `corriger-ascii` (constantes.py
# de cet outil). Le chien ne possede pas sa propre liste -- une liste qui derive de
# celle du corriger est une liste qui oublie la moitie du perimetre. Mais il ne
# l IMPORTE pas non plus : un outil ne s importe pas dans une routine. La liste est
# donc ecrite ici, et ce commentaire dit d ou elle vient -- si l outil bouge, il le
# montre. Mesure du 2026-10-03 : 990 fichiers observes en 68 ms.
DOSSIERS_SURVEILLES = (
    REPERTOIRE_ROUTINE.parent.parent,
    REPERTOIRE_ROUTINE.parent.parent.parent / "_operateur",
)
EXTENSIONS = (".md", ".py", ".json")
DOSSIERS_EXCLUS = ("__pycache__",)

# LE COMBO QUE LE CHIEN DECLENCHE. LE CHIEN NE CORRIGE PAS : il appelle le combo,
# qui est le seul domaine de la correction (convention-auto-correction.md, point 2).
# Un chien qui corrigerait lui-meme aurait deux cartes ASCII, donc deux conversions
# qui divergent en silence.
CHEMIN_LANCEUR = REPERTOIRE_ROUTINE.parent.parent.parent / "lancer.py"
COMBO_CORRECTION = "corriger-ascii"
VERBE_CORRECTION = "corriger"
OPTION_APPLIQUER = "--appliquer"

# LE JOURNAL des corrections : une ligne par intervention, avec ce qui a bouge. Un
# geste qu on ne trace pas ne se mesure pas -- et le chien muet doit pouvoir etre
# distingue du chien endormi.
NOM_JOURNAL = "journal-chien.jsonl"

# LE TEMOIN DE CADENCE (MO-479) : le fait que `verifier-cadence` lit pour mesurer
# le battement reel de la routine. Meme forme que veille-flux : le genre du temoin,
# le nom du journal, et le type d evenement qu il cherche dedans. Sans cette
# declaration, `verifier-cadence` ne peut pas mesurer une cadence declaree qu
# personne ne temoigne : un oubli n est pas un temoin.
TEMOIN_CADENCE = ("journal", NOM_JOURNAL, "passe-debut")

CHEMIN_JOURNAL = REPERTOIRE_ROUTINE / NOM_JOURNAL

NOM_PID = "chien.pid"
CHEMIN_PID = REPERTOIRE_ROUTINE / NOM_PID

# LES PRODUCTIONS DE LA ROUTINE : les fichiers qu'elle ECRIT et qui ne sont PAS
# des sources -- ni ses etats courts de forme CONVENTIONNELLE (etat, journal,
# cadence, PID : le controle les reconnait par leur FORME), ni un fichier ecrit a
# la main. Un rapport, un inventaire, la MEMOIRE d'une passe. Une PRODUCTION n'est
# pas une SOURCE : sa porte est CETTE routine.
# Un fichier dont le NOM echappe a la convention se declare ICI (mesure du
# 2026-09-23 : `veille-flux/alertes-emises.json`, un etat anti-spam anterieur a la
# convention, juge comme une source) : c'est le SEUL endroit ou le controle peut
# l'apprendre.
# Le controle d'attribution LIT cette declaration (M-076) : une production NON
# declaree est accusee a CHAQUE passe, comme une ecriture hors de sa porte.
# Declarer ici ce que la routine ecrit -- la liste est vide au premier tour.
PRODUCTIONS = (NOM_JOURNAL,)
NOM_DRAPEAU_ARRET = "chien.arret"
CHEMIN_DRAPEAU_ARRET = REPERTOIRE_ROUTINE / NOM_DRAPEAU_ARRET

# ETAT COURT DE LA PASSE (friction 28, 2026-09-14) : le BATTEMENT d'une routine
# est un ETAT, pas une histoire -- il s'ecrit ICI, a chaque passe et ECRASE.
# Sans ce temoin, chien etait la SEULE routine dont le rythme reel n'etait
# mesurable nulle part : ni journal, ni etat de passe (elle n'ecrit que son PID,
# une fois). `verifier-cadence` le lit et le compare a la cadence DECLAREE
# ci-dessus -- c'est la troisieme jambe : declarer, publier, MESURER.
NOM_ETAT = "chien-etat.json"
CHEMIN_ETAT = REPERTOIRE_ROUTINE / NOM_ETAT
# Combien de dernieres passes l'etat garde : assez pour un ecart MEDIAN (une
# passe en retard ou un redemarrage ne doivent pas faire croire a une derive),
# et borne pour que l'etat reste un etat (une poignee d'horodatages).
# La FABRIQUE de l'anneau (ajout + borne) et sa LECTURE (ecart median) sont le
# moteur PARTAGE `data/commun/battement.py` : la routine ne declare QUE sa
# longueur, elle ne recopie pas le decoupage (L-029 : un moteur recopie quatre
# fois diverge quatre fois).
PASSES_GARDEES_ETAT = 5
# Clef de l'anneau DANS l'etat : un seul nom, ecrit ET relu par sa constante.
CLE_ANNEAU_PASSES = "dernieres_passes"
# Format UNIQUE des horodatages (journal + etat) : le temps s'ecrit a un seul
# endroit, le meme des deux cotes (ecriture et relecture du battement).
FORMAT_HORODATAGE = "%Y-%m-%d %H:%M:%S"
ENCODAGE_ETAT = "utf-8"

