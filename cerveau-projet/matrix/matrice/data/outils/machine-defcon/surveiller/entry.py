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
    resultat = subprocess.run(commande, capture_output=True)
    sortie = resultat.stdout.decode("utf-8", errors="replace").strip()
    print("Declencheur REMPLI : defcon " + str(niveau) + " pose par la PORTE monter"
          + (" (code " + str(resultat.returncode) + ")." if resultat.returncode else "."))
    if sortie:
        print(sortie)
    return resultat.returncode
