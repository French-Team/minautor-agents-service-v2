"""Categorie passe : orchestre une passe de veille (RELAX ou VIGILE).

Interface entre main.py et les fonctions simples (passe/fonctions.py).
Chaque passe se NOTE elle-meme dans la BDD usages-outils-combos (bdd-usages)
et se DEPOSE dans la section passes des activites-recentes (bdd-activites).
"""
import time

from commun import (
    alerte_grave,
    journaliser,
    lancer_combo,
    purger_alertes_fantomes,
    purger_signatures_mortes,
    purger_signatures_resolues,
)
from constants import CHEMIN_BDD_ACTIVITES, CHEMIN_BDD_USAGES, SECTION_PASSES, TAGS_PASSE
from passe.fonctions import executer_passe


def noter_passe(mode, code, duree_ms, nombre_detections):
    """Note UNE passe dans la BDD usages (un echec de notation n'arrete jamais la passe)."""
    arguments = (
        ["noter", "--outil", "veille-flux", "--commande", "passe-" + mode,
         "--code", str(code), "--duree", str(duree_ms),
         "--detail", str(nombre_detections) + " detection(s)",
         "--tags", TAGS_PASSE]
    )
    try:
        code_note, sortie = lancer_combo(CHEMIN_BDD_USAGES, arguments)
    except OSError as erreur:
        journaliser({"type": "incident-notation", "detail": str(erreur)})
        return
    if code_note != 0:
        journaliser({"type": "incident-notation", "code": code_note, "detail": sortie[:200]})


def deposer_passe(mode, detections, nouvelles):
    """Depose UNE passe dans la section passes des activites (echec jamais bloquant)."""
    detail = (
        "Passe " + mode + " : " + str(len(detections)) + " detection(s), "
        + str(nouvelles) + " nouvelle(s) alerte(s)"
    )
    arguments = (
        ["noter", "--section", SECTION_PASSES, "--detail", detail,
         "--tags", TAGS_PASSE]
    )
    try:
        code_depot, sortie = lancer_combo(CHEMIN_BDD_ACTIVITES, arguments)
    except OSError as erreur:
        journaliser({"type": "incident-depot", "detail": str(erreur)})
        return
    if code_depot != 0:
        journaliser({"type": "incident-depot", "code": code_depot, "detail": sortie[:200]})


def executer(arguments):
    vigile = "--vigile" in arguments
    mode = "vigile" if vigile else "relax"
    purger_alertes_fantomes()
    purger_signatures_mortes()
    journaliser({"type": "passe-debut", "mode": mode})
    debut = time.time()
    detections = executer_passe(vigile)
    duree_ms = int((time.time() - debut) * 1000)
    # Une signature re-testee et non re-detectee est RESOLUE : anti-spam reconcilie
    # (sinon une alerte morte bloque pour toujours la suivante de meme signature).
    purger_signatures_resolues(mode, detections)
    nouvelles = 0
    for detection in detections:
        if alerte_grave(detection["etat"], detection["cible"], detection["detail"]):
            nouvelles += 1
    code = 1 if detections else 0
    journaliser({"type": "passe-fin", "mode": mode, "detections": len(detections), "alertes": nouvelles})
    noter_passe(mode, code, duree_ms, len(detections))
    deposer_passe(mode, detections, nouvelles)
    print(
        "Passe " + mode + " terminee : "
        + str(len(detections)) + " detection(s), "
        + str(nouvelles) + " nouvelle(s) alerte(s)."
    )
    return code
