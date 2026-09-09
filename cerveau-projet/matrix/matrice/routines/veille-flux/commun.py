"""Fonctions communes de la routine veille-flux : une seule tache chacune."""
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

from constants import (
    CHEMIN_BOITE_MATRICE_IN,
    CHEMIN_ENTONNOIR,
    CHEMIN_ETAT_ALERTES,
    CHEMIN_JOURNAL,
    CHEMIN_PID,
    ENCODAGE,
    REPERTOIRE_MATRIX,
    TIMEOUT_COMBO_SECONDES,
    THEME_REPARATION,
    URGENCE_VEILLE,
    chemin_python,
    env_console_sure,
)


def horodater():
    """Retourne la date-heure locale au format du journal."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def journaliser(entree):
    """Ajoute UNE ligne au journal (en ajout seul, jamais modifie a posteriori)."""
    entree = dict(entree)
    entree["date"] = horodater()
    with open(CHEMIN_JOURNAL, "a", encoding=ENCODAGE) as flux:
        flux.write(json.dumps(entree, ensure_ascii=True) + "\n")


def ecrire_pid(pid):
    """Note le PID de la boucle dans veille-flux.pid."""
    CHEMIN_PID.write_text(str(pid) + "\n", encoding=ENCODAGE)


def lire_pid():
    """Retourne le PID de la boucle, ou None si absent."""
    if not CHEMIN_PID.exists():
        return None
    contenu = CHEMIN_PID.read_text(encoding=ENCODAGE).strip()
    return int(contenu) if contenu else None


def supprimer_pid():
    """Retire veille-flux.pid (arret propre)."""
    if CHEMIN_PID.exists():
        os.remove(CHEMIN_PID)


def cible_fichier_morte(signature):
    """True si la signature porte une cible fichier qui n'existe plus (M-051/M-052).

    Seules les signatures python-compile portent une cible fichier ; toute
    autre signature (ou cible non-fichier comme 'py_compile') n'est jamais
    declaree morte.
    """
    if not signature.startswith("python-compile:"):
        return False
    cible = signature.split(":", 1)[1]
    if not ("\\" in cible or "/" in cible):
        return False
    return not Path(cible).exists()


def purger_signatures_mortes():
    """Retire les signatures dont la cible n'existe plus (M-051).

    Une signature morte bloquerait la future alerte si la cible etait recreee.
    Seules les signatures python-compile portent une cible fichier ; les autres
    sont conservees telles quelles. Jamais bloquant : tout incident est
    journalise et la passe continue.
    """
    try:
        etat = charger_alertes_emises()
    except Exception as erreur:
        journaliser({"type": "incident-purge", "detail": str(erreur)})
        return
    vivantes = {}
    for signature, date in etat.items():
        if cible_fichier_morte(signature):
            continue
        vivantes[signature] = date
    if len(vivantes) == len(etat):
        return
    purges = len(etat) - len(vivantes)
    try:
        CHEMIN_ETAT_ALERTES.write_text(
            json.dumps(vivantes, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
            encoding=ENCODAGE,
        )
    except Exception as erreur:
        journaliser({"type": "incident-purge", "detail": str(erreur)})
        return
    journaliser({"type": "purge-signatures", "purgees": purges})


def purger_alertes_fantomes():
    """Retire les alertes-grave fantomes de la boite Matrice (M-052).

    Une alerte-grave python-compile dont le fichier cible n'existe plus est
    un fantome : son incident est deja resolu ou sans objet. Les AUTRES
    messages de la boite (fin-mission, retour-lot, incident, alertes vivantes)
    sont INTOUCHABLES. Jamais bloquant : tout incident est journalise.
    """
    if not CHEMIN_BOITE_MATRICE_IN.exists():
        return
    try:
        lignes = CHEMIN_BOITE_MATRICE_IN.read_text(encoding=ENCODAGE).splitlines()
        messages = [json.loads(ligne) for ligne in lignes if ligne.strip()]
    except Exception as erreur:
        journaliser({"type": "incident-purge-boite", "detail": str(erreur)})
        return
    vivantes = []
    purges = 0
    for message in messages:
        if message.get("type") == "alerte-grave" and cible_fichier_morte(
            message.get("etat", "") + ":" + str(message.get("cible", ""))
        ):
            purges += 1
            continue
        vivantes.append(message)
    if purges == 0:
        return
    try:
        CHEMIN_BOITE_MATRICE_IN.write_text(
            "".join(json.dumps(m, ensure_ascii=True) + "\n" for m in vivantes),
            encoding=ENCODAGE,
        )
    except Exception as erreur:
        journaliser({"type": "incident-purge-boite", "detail": str(erreur)})
        return
    journaliser({"type": "purge-boite", "purgees": purges})


def charger_alertes_emises():
    """Retourne l'etat des alertes deja emises {signature: date} (ou {})."""
    if not CHEMIN_ETAT_ALERTES.exists():
        return {}
    return json.loads(CHEMIN_ETAT_ALERTES.read_text(encoding=ENCODAGE))


def enregistrer_alerte_emise(signature):
    """Note UNE alerte comme emise (anti-spam : une seule alerte par signature)."""
    etat = charger_alertes_emises()
    etat[signature] = horodater()
    CHEMIN_ETAT_ALERTES.write_text(
        json.dumps(etat, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding=ENCODAGE,
    )


def alerte_grave(etat, cible, detail):
    """Depose UNE alerte grave dans la boite de la Matrice (une seule fois par signature).

    Retourne True si l'alerte est NOUVELLE (emise), False si deja emise avant.
    """
    signature = etat + ":" + cible
    if signature in charger_alertes_emises():
        return False
    message = {
        "type": "alerte-grave",
        "date": horodater(),
        "etat": etat,
        "cible": cible,
        "detail": detail,
        "action": "mission-reparation",
    }
    CHEMIN_BOITE_MATRICE_IN.parent.mkdir(parents=True, exist_ok=True)
    with open(CHEMIN_BOITE_MATRICE_IN, "a", encoding=ENCODAGE) as flux:
        flux.write(json.dumps(message, ensure_ascii=True) + "\n")
    enregistrer_alerte_emise(signature)
    journaliser({"type": "alerte", "etat": etat, "cible": cible})
    deposer_mission_vrac(etat, cible, detail)
    return True


def deposer_mission_vrac(etat, cible, detail):
    """Verse UNE mission-reparation au vrac de l'entonnoir (M-020, echec jamais bloquant).

    L'anti-spam des alertes garantit UN depot par signature (une alerte nouvelle,
    une mission nouvelle). Theme commence par 'reparer' : le classement propose
    de l'entonnoir le rangera en reparation.
    """
    arguments = (
        ["deposer", "--theme", THEME_REPARATION + " " + cible,
         "--objectif", etat + " : " + detail,
         "--urgence", URGENCE_VEILLE, "--source", "veille"]
    )
    try:
        code_depot, sortie = lancer_combo(CHEMIN_ENTONNOIR, arguments)
    except OSError as erreur:
        journaliser({"type": "incident-depot-vrac", "detail": str(erreur)})
        return
    if code_depot != 0:
        journaliser({"type": "incident-depot-vrac", "code": code_depot, "detail": sortie[:200]})
        return
    journaliser({"type": "mission-vrac", "cible": cible})


def charger_base_acceptee():
    """Retourne l'ensemble des codes Unicode acceptes (base-acceptee.json), ou set() vide."""
    from constants import CHEMIN_BASE

    if not CHEMIN_BASE.exists():
        return set()
    donnees = json.loads(CHEMIN_BASE.read_text(encoding=ENCODAGE))
    return set(donnees.get("acceptes", ()))


def lancer_combo(chemin_outil, arguments):
    """Lance UN combo (outil Python de la Matrice). Retourne (code, sortie).

    Garde E-045 : timeout=TIMEOUT_COMBO_SECONDES. Un combo qui depasse le delai
    est tue (TimeoutExpired) et l'incident est journalise : la boucle ne pend
    jamais. Code retourne : 124 (convention unix de kill par timeout).
    """
    commande = [chemin_python(), "main.py"] + list(arguments)
    try:
        termine = subprocess.run(
            commande,
            cwd=str(chemin_outil),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env_console_sure(),
            timeout=TIMEOUT_COMBO_SECONDES,
        )
    except subprocess.TimeoutExpired:
        journaliser({"type": "incident-combo-bloquant", "combo": str(chemin_outil),
                     "arguments": " ".join(arguments), "timeout": TIMEOUT_COMBO_SECONDES})
        return 124, "combo tue par timeout " + str(TIMEOUT_COMBO_SECONDES) + "s"
    return termine.returncode, (termine.stdout or "") + (termine.stderr or "")


def lister_fichiers_python():
    """Retourne la liste triee des .py de matrix/ (hors __pycache__)."""
    fichiers = []
    for racine, dossiers, noms in os.walk(str(REPERTOIRE_MATRIX)):
        dossiers[:] = [d for d in dossiers if d != "__pycache__"]
        for nom in noms:
            if nom.endswith(".py"):
                fichiers.append(os.path.join(racine, nom))
    return sorted(fichiers)


def lancer_py_compile(fichiers=None):
    """Compile les .py de matrix/. Retourne (code, sortie).

    Garde E-045 : meme timeout que les combos (l'incident est journalise).
    """
    if fichiers is None:
        fichiers = lister_fichiers_python()
    commande = [chemin_python(), "-m", "py_compile"] + fichiers
    try:
        termine = subprocess.run(
            commande,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env_console_sure(),
            timeout=TIMEOUT_COMBO_SECONDES,
        )
    except subprocess.TimeoutExpired:
        journaliser({"type": "incident-py-compile-bloquant",
                     "timeout": TIMEOUT_COMBO_SECONDES})
        return 124, "py_compile tue par timeout " + str(TIMEOUT_COMBO_SECONDES) + "s"
    return termine.returncode, (termine.stdout or "") + (termine.stderr or "")


def sortie_en_crash(sortie):
    """Retourne True si la sortie d'un sous-processus porte la signature d'un crash.

    Un code de sortie 1 peut etre LEGITIME (ecarts detectes) : seule la signature
    de crash fait foi pour distinguer un echec du processus d'un verdict d'outil.
    """
    return "Fatal Python error" in sortie or "Traceback (most recent call last)" in sortie


def extraire_codes_unicode(sortie):
    """Retourne les codes U+XXXX cites dans la sortie d'un combo (contrat de nos outils)."""
    return sorted(set(re.findall(r"U\+[0-9A-Fa-f]{4,6}", sortie)))


def extraire_fichiers_python_en_erreur(sortie):
    """Retourne les chemins des fichiers qui ne compilent pas (sortie py_compile)."""
    return sorted(set(re.findall(r'File "([^"]+\.py)"', sortie)))
