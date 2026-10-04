"""Categorie surveiller : les DECLENCHEURS de defcon sont-ils remplis ?

Le verbe EVALUE les declencheurs declares (constants.DECLENCHEURS) et POSE le
niveau du plus haut declencheur rempli -- par la PORTE `monter`, jamais par une
ecriture directe : c'est `monter` qui journalise la transition (trace append-only
defcon-historique.jsonl) et qui declenche la pause automatique de defcon 5.

Usage :
    python main.py surveiller            (evalue et pose le niveau)
    python main.py surveiller --evaluer  (evalue, rapporte, et NE POSE RIEN)
"""


import subprocess
import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-416, lot -- fin du residu) -----------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu) : on remonte
# jusqu au dossier `matrix`, et on REFUSE plutot que de deviner (garde-foi L-006).
# Bloc AUTOSUFFISANT : il ne depend ni de l ordre des imports du fichier, ni de la
# presence d un `import subprocess` de module (mesure du 2026-09-25 : deux fichiers
# casses par ces deux pieges, invisibles au py_compile).
_RACINE_LANCEMENT = Path(__file__).resolve().parent
while _RACINE_LANCEMENT.name != "matrix":
    if _RACINE_LANCEMENT.parent == _RACINE_LANCEMENT:
        raise RuntimeError("racine `matrix` introuvable en remontant depuis " + __file__)
    _RACINE_LANCEMENT = _RACINE_LANCEMENT.parent
_REPERTOIRE_COMMUN_LANCEMENT = _RACINE_LANCEMENT / "matrice" / "data" / "commun"
if not (_REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(_REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(_REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(_REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())


def popen_enfant(*arguments, **options):
    """Le lancement DETACHE de cet outil : jamais de fenetre."""
    return subprocess.Popen(*arguments, **options, **drapeaux_popen())

import subprocess
import sys

from commun import charger_classeur, trouver_defcon
from constants import NIVEAU_NORMAL, NOM_OUTIL_MACHINE_DEFCON
from resolution_outils import chemin_outil  # noqa: E402
from surveiller.fonctions import decider, evaluer


def executer(arguments):
    rapport_seul = "--evaluer" in arguments
    donnees = charger_classeur()
    courant, _ = trouver_defcon(donnees)
    niveau_courant = courant if courant is not None else NIVEAU_NORMAL

    verdicts = evaluer()
    for ident, rempli, niveau, motif in verdicts:
        print(("  DECLENCHE  " if rempli else "  ok         ") + ident
              + " (defcon " + str(niveau) + ") -- " + motif)

    niveau, motifs = decider(verdicts, courant)
    if not motifs:
        print("Surveillance : aucun declencheur a poser (niveau courant "
              + str(niveau_courant) + ") -- jamais de baisse, jamais de re-pose.")
        return 0
    if rapport_seul:
        print("(--evaluer : defcon " + str(niveau) + " SERAIT pose -- aucun acte pose)")
        return 0

    raison = "declencheur " + " ; ".join(motifs)
    commande = [sys.executable, str(chemin_outil(NOM_OUTIL_MACHINE_DEFCON)),
                "monter", "--niveau", str(niveau), "--raison", raison]
    resultat = lancer_enfant(commande, capture_output=True)
    sortie = resultat.stdout.decode("utf-8", errors="replace").strip()
    print("Declencheur REMPLI : defcon " + str(niveau) + " pose par la PORTE monter"
          + (" (code " + str(resultat.returncode) + ")." if resultat.returncode else "."))
    if sortie:
        print(sortie)
    return resultat.returncode
