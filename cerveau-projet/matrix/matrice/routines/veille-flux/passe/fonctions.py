"""Fonctions simples de la categorie passe : une seule tache chacune."""
import time

from commun import (
    charger_base_acceptee,
    extraire_codes_unicode,
    extraire_fichiers_python_en_erreur,
    journaliser,
    lancer_combo,
    lancer_py_compile,
    relativiser,
    sortie_en_crash,
)
from constants import (
    CHEMIN_CORRIGER_ASCII,
    CHEMIN_JOURNAL_MULTI_ENCARTS,
    CHEMIN_MACHINE_DEFCON,
    CHEMIN_VISUEL_RELATIF,
    CIBLE_VISUEL,
    PAUSE_REPRISE_SECONDES,
    REPERTOIRE_MATRIX,
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
    MO-035 : symetrie avec passer_corriger_ascii -- un OSError de lancement
    devient une DETECTION. C'est l'absence de cette garde qui a laisse la passe
    mourir en silence (aucun passe-fin) pendant 11 heures.
    """
    try:
        code, sortie = lancer_py_compile()
    except OSError as erreur:
        return [{"etat": "incident-py-compile", "cible": "py_compile", "detail": str(erreur)}]
    if code == 0:
        return []
    fichiers = extraire_fichiers_python_en_erreur(sortie)
    time.sleep(PAUSE_REPRISE_SECONDES)
    try:
        code, sortie = lancer_py_compile(fichiers or None)
    except OSError as erreur:
        return [{"etat": "incident-py-compile", "cible": "py_compile", "detail": str(erreur)}]
    if code == 0:
        return []
    if sortie_en_crash(sortie):
        return [{"etat": "incident-combo", "cible": "py_compile", "detail": "crash du sous-processus (signature de crash)"}]
    if not fichiers:
        return [{"etat": "python-compile", "cible": "py_compile", "detail": sortie[:200]}]
    # PORTABILITE : on PERSISTE la cible RELATIVE (matrix/...) et non le chemin
    # absolu cite par py_compile. Ce chemin part dans la signature anti-spam ET
    # dans le theme de la mission de reparation : en absolu, un projet deplace
    # rendrait la signature fausse et la mission sans objet.
    return [
        {"etat": "python-compile", "cible": relativiser(fichier),
         "detail": "ne compile pas (confirme apres re-test)"}
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


def passer_declencheurs():
    '''Etape 4 (VIGILE seulement) : les DECLENCHEURS de defcon (voie A, EO-181).

    C'est ICI qu'un declencheur cesse d'etre un mot : la veille EVALUE les
    conditions declarees chez machine-defcon et POSE le niveau -- par la PORTE
    monter, qui journalise la transition et, a 5, met la session en pause.
    Un non-zero n'est JAMAIS avale : une surveillance qui echoue se DIT.
    '''
    try:
        code, sortie = lancer_combo(CHEMIN_MACHINE_DEFCON, ['surveiller'])
    except OSError as erreur:
        return [{'etat': 'incident-combo', 'cible': 'machine-defcon', 'detail': str(erreur)}]
    if code == 0:
        return []
    if sortie_en_crash(sortie):
        return [{'etat': 'incident-combo', 'cible': 'machine-defcon',
                 'detail': 'crash du sous-processus (signature de crash)'}]
    return [{'etat': 'defcon', 'cible': 'machine-defcon',
             'detail': 'surveillance non nulle (code ' + str(code) + ') : ' + sortie[:160]}]


def age_visuel_secondes():
    """L AGE du journal visuel, en secondes (None s il est absent).

    L age est MESURE, jamais suppose : c est lui qui DIT ce que la passe vient de
    reparer -- un visuel a jour rend 0 s, un visuel de trois jours rend son retard.
    """
    try:
        return int(time.time() - (REPERTOIRE_MATRIX / CHEMIN_VISUEL_RELATIF).stat().st_mtime)
    except OSError:
        return None


def passer_visuel():
    """Etape 4 : REGENERER le journal visuel de la Matrice (MO-366, voie a).

    LE DEFAUT MESURE : le journal visuel se declare GENERE depuis les BDD et donne
    son remede (construire) -- mais AUCUN appelant ne l appliquait. Mesure du
    2026-09-23 : trois jours de retard, sans un signe. Un visuel qui declare un etat
    passe se lit comme l etat courant (classe L-055).

    POURQUOI REGENERER PLUTOT QUE SURVEILLER : le cout est MESURE, pas suppose --
    370 ms pour les neuf encarts (377, 382, 369 sur trois passes), negligeable
    devant toute cadence. Un document GENERE se regenere ; le surveiller laisserait
    la phrase fausse en place et n ajouterait qu un voyant ailleurs.

    POURQUOI ICI : le passant EXISTE deja (la veille est activee en permanence).
    Une routine neuve aurait duplique toute la machinerie PID/cadence/drapeau pour
    370 ms de travail (M-076 : un seul domicile par geste).

    Le geste est TRACE au journal (retard REPARE + duree, un geste invisible ne se
    mesure pas) et un refus de la porte devient une DETECTION : jamais un silence,
    jamais une exception qui tue la passe.
    """
    retard_avant = age_visuel_secondes()
    debut = time.time()
    try:
        code, sortie = lancer_combo(CHEMIN_JOURNAL_MULTI_ENCARTS, ["construire"])
    except OSError as erreur:
        journaliser({"type": "visuel", "code": "os-error", "retard_avant_s": retard_avant,
                     "detail": str(erreur)})
        return [{"etat": "incident-combo", "cible": "journal-multi-encarts",
                 "detail": str(erreur)}]
    duree_ms = int((time.time() - debut) * 1000)
    if sortie_en_crash(sortie):
        journaliser({"type": "visuel", "code": "crash", "duree_ms": duree_ms,
                     "retard_avant_s": retard_avant})
        return [{"etat": "incident-combo", "cible": "journal-multi-encarts",
                 "detail": "crash du sous-processus (signature de crash)"}]
    journaliser({"type": "visuel", "code": code, "duree_ms": duree_ms,
                 "retard_avant_s": retard_avant})
    if code != 0:
        return [{"etat": "visuel-perime", "cible": CIBLE_VISUEL,
                 "detail": "regeneration REFUSEE (code " + str(code) + ") : " + sortie[:160]}]
    return []


def executer_passe(vigile):
    """Orchestre UNE passe : corriger-ascii + py_compile + visuel (+ marbre si VIGILE)."""
    detections = []
    detections.extend(passer_corriger_ascii())
    detections.extend(passer_py_compile())
    detections.extend(passer_visuel())
    if vigile:
        detections.extend(passer_marbre())
        detections.extend(passer_declencheurs())
    return detections
