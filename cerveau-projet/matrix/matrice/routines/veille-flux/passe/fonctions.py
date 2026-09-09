"""Fonctions simples de la categorie passe : une seule tache chacune."""
import time

from commun import (
    charger_base_acceptee,
    extraire_codes_unicode,
    extraire_fichiers_python_en_erreur,
    lancer_combo,
    lancer_py_compile,
    sortie_en_crash,
)
from constants import (
    CHEMIN_CORRIGER_ASCII,
    PAUSE_REPRISE_SECONDES,
    VERIFIERS_MARBRE,
)


def passer_corriger_ascii():
    """Etape 1 : corriger-ascii (scan + correction auto). Retourne les detections.

    Les caracteres deja acceptes (base-acceptee.json) ne sont jamais des detections.
    Un CRASH du sous-processus n'est jamais confondu avec le code 1 legitime
    (non-convertibles) : la signature de crash fait foi.
    """
    try:
        code, sortie = lancer_combo(CHEMIN_CORRIGER_ASCII, ["corriger", "--appliquer"])
    except OSError as erreur:
        return [{"etat": "incident-combo", "cible": "corriger-ascii", "detail": str(erreur)}]
    if sortie_en_crash(sortie):
        return [{"etat": "incident-combo", "cible": "corriger-ascii", "detail": "crash du sous-processus (signature de crash)"}]
    if code not in (0, 1):
        return [{"etat": "incident-combo", "cible": "corriger-ascii", "detail": "code de sortie inattendu : " + str(code)}]
    base = charger_base_acceptee()
    nouveaux = [c for c in extraire_codes_unicode(sortie) if c not in base]
    return [
        {
            "etat": "ascii-non-convertible",
            "cible": code,
            "detail": "caractere non convertible (decision du createur requise)",
        }
        for code in nouveaux
    ]


def passer_py_compile():
    """Etape 2 : compilation globale des .py. Un echec est RE-TESTE apres pause.

    Un fichier vient peut-etre d'etre sauvegarde a l'instant : si la re-test
    passe, l'echec etait transitoire (pas de fausse alerte).
    """
    code, sortie = lancer_py_compile()
    if code == 0:
        return []
    fichiers = extraire_fichiers_python_en_erreur(sortie)
    time.sleep(PAUSE_REPRISE_SECONDES)
    code, sortie = lancer_py_compile(fichiers or None)
    if code == 0:
        return []
    if sortie_en_crash(sortie):
        return [{"etat": "incident-combo", "cible": "py_compile", "detail": "crash du sous-processus (signature de crash)"}]
    if not fichiers:
        return [{"etat": "python-compile", "cible": "py_compile", "detail": sortie[:200]}]
    return [
        {"etat": "python-compile", "cible": fichier, "detail": "ne compile pas (confirme apres re-test)"}
        for fichier in fichiers
    ]


def passer_marbre():
    """Etape 3 (VIGILE seulement) : les 3 verifiers du marbre."""
    detections = []
    for nom, chemin in VERIFIERS_MARBRE:
        try:
            code, sortie = lancer_combo(chemin, ["verifier"])
        except OSError as erreur:
            detections.append({"etat": "incident-combo", "cible": nom, "detail": str(erreur)})
            continue
        if code == 1:
            detections.append({"etat": "marbre", "cible": nom, "detail": "ecart de marbre detecte (voir verifier-" + nom + ")"})
        elif code != 0:
            detections.append({"etat": "incident-combo", "cible": nom, "detail": "code de sortie inattendu : " + str(code)})
    return detections


def executer_passe(vigile):
    """Orchestre UNE passe : corriger-ascii + py_compile (+ marbre si VIGILE)."""
    detections = []
    detections.extend(passer_corriger_ascii())
    detections.extend(passer_py_compile())
    if vigile:
        detections.extend(passer_marbre())
    return detections
