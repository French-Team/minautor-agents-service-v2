"""Listes FERMEES des checklists : etapes et verifications PAR TYPE de mission.

Convention zero-valeur-en-dur : la logique CONSOMME ces valeurs, elle ne les contient pas.
NOMMAGE : listes.py (PAS constants.py) -- pas de collision avec les modules du pilote.
"""
# Types fermes de l'entonnoir (doit rester synchronise avec entonnoir/listes.py TYPES).
# revision : nouveau type (decision createur 2026-09-07, mot-crochet [revision]).
TYPES = ("dev", "reparation", "doc", "audit", "revision")

# Etapes communes a TOUTES les missions (toute fin de mission passe par la).
ETAPES_COMMUNES = (
    "tests reels du livrable (nominal + negatif)",
    "py_compile global avant livraison",
    "notes BDD par la porte unique (bdd-modifications)",
    "fin de mission via le pilote",
)

# Verifications communes a TOUTES les missions.
VERIFICATIONS_COMMUNES = (
    "zero valeur en dur (constantes seulement)",
    "ASCII strict hors base acceptee",
    "ecriture atomique (tmp + remplacement, LF forces)",
)

# Etapes PAR TYPE (listes fermees : un type inconnu n'a pas de checklist).
ETAPES_PAR_TYPE = {
    "dev": (
        "lire SA fiche + ses corrections avant de commencer",
        "template existant duplique avant toute nouvelle piece",
        "fiche dans manuel-outils mise a jour",
    ),
    "reparation": (
        "diagnostic D.A.G. AVANT reparation (cause racine, pas symptome)",
        "reparation a la SOURCE (le garde-fou, pas le cas particulier)",
        "test negatif prouvant que le bug est mort",
    ),
    "doc": (
        "index du dossier mis a jour (aucune ligne morte)",
        "liens internes verifies (chemins existants)",
    ),
    "audit": (
        "rapport depose (lecture seule, jamais de reparation par l'auditeur)",
        "ecarts signales a la Matrice (jamais corriges en douce)",
    ),
    "revision": (
        "relire le sujet revisite en entier avant de trancher",
        "decision du createur demandee si la revision change une regle",
    ),
}

# Verifications PAR TYPE.
VERIFICATIONS_PAR_TYPE = {
    "dev": (
        "outil auto-note dans usages-outils-combos si applicable",
        "registre espion-integrite a jour si nouvelle BDD",
    ),
    "reparation": (
        "lecon gravee en BDD (bdd-lecons) si le diagnostic a porte un enseignement",
    ),
    "doc": (),
    "audit": (),
    "revision": (),
}
