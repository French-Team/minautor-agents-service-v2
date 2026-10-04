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

# --- LES OUTILS QUE LA MISSION VA APPELER (proto-6, etape 2) -----------------
# POURQUOI (revision createur du 2026-09-20, MO-313) : l agent recevait une LISTE
# DE NOMS et devait relire chaque outil pour retrouver son usage -- c est de la que
# viennent les appels fautifs que le createur a constates. Un outil se livre AVEC
# son mode d emploi, qui est EXTRAIT de la brique elle-meme a l injection
# (injection/modes_emploi.py) : jamais une fiche recopiee ici (M-076).
# Un nom est celui d une BRIQUE (un .py, ou un dossier qui porte un main.py) ; les
# douze noms declares ici ont ete MESURES servables avant d entrer (main.py lu).
OUTILS_COMMUNS = (
    "bdd-modifications",
    "suivi-optimus",
    "lanceur-non-regression.py",
)

# --- LE PLANCHER DES OUTILS : servis dans TOUTE mission (2026-09-21) ----------
# MESURE QUI A DECIDE (demande createur) : le moteur de recherche etait declare
# dans `doc`, `audit` et `revision` -- et ABSENT de `dev` et `reparation`, les deux
# types les plus frequents (mesure du jour : MO-333 en `dev` et MO-332 en
# `reparation` recevaient 6 outils, aucun moteur). L agent n avait donc AUCUNE
# raison d utiliser le moteur du projet : il tombait sur son outil de recherche
# natif, qui ne connait ni les cartes d identite, ni les BDD, ni les zones
# invisibles. Un outil qu on veut voir utilise se SERT, il ne se souhaite pas.
# Le plancher est servi EN TETE et par les DEUX voies (repli par type ET liste
# preparee sur l item) : sans cela, une liste preparee (voie `item`, EO-313)
# pourrait encore l ecarter, et le defaut reviendrait par l autre chemin.
OUTILS_TOUJOURS = (
    "rechercher",
)

OUTILS_PAR_TYPE = {
    "dev": ("creer-outil.py", "ecrire", "verifier-contrats-outils.py"),
    "reparation": ("revert-fichier.py", "bdd-lecons", "garde-perimetre-write.py"),
    "doc": ("ecrire", "lister", "rechercher"),
    "audit": ("lire", "rechercher", "bdd-modifications"),
    "revision": ("ecrire", "garde-perimetre-write.py", "rechercher"),
}
