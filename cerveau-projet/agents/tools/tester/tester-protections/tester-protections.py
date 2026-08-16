#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
tester-protections.py
tester-protections

Usage:
  tester-protections.py [OPTIONS]
"""

"""
tester-protections.py

POINT D ENTREE UNIQUE des protections de tests (format Python canonique).

Regle (audit 2026-08-12, demande utilisateur) : CHAQUE test-0XX DOIT charger
ces protections via le helper `charger_protections()` (template-test.md).
Les anciennes protections autonomes (tester-protection-*) restent disponibles
mais ne sont PAS importables depuis un test .py : ce module les fusionne en
une API unique importable.

API exportee :
  - lancer_protege(cmd, timeout=120)
        Execute une commande SOUS PROTECTION : timeout avec tuer l arbre de
        processus (cross-platform), detection des erreurs silencieuses.
        Si le timeout expire (boucle infinie ou blocage), leve ArretProtection
        au lieu de laisser le test continuer betement.
        Retourne un objet avec .returncode, .stdout, .stderr (compatible
        subprocess.CompletedProcess).
  - verifier_critique(nom, condition, detail="")
        Comme verifier() du template mais PROTECTION STOP : si la condition
        est fausse, affiche [KO] puis LEVE ArretProtection - le test s arrete
        immediatement (fail-fast) au lieu d enchainer les points suivants.
  - ArretProtection(Exception)
        Exception levee par les protections STOP (timeout ou point critique).
        Le test (template) l attrape dans main() pour afficher un bilan propre
        et retourner 1.
  - VERSION, STATUT, PROTECTIONS_ACTIVES

Usage direct (CLI) :
  python3 tester-protections.py --version
  python3 tester-protections.py --help

Proprietaire : Morpheus (outil partage)
Version : 0.2.0
Statut : prepare
"""

import argparse
import os
import signal
import subprocess
import sys
from types import SimpleNamespace

VERSION = "0.2.0"
STATUT = "prepare"

# Les protections actives par ce point d entree (fusion des 3 anciennes)
PROTECTIONS_ACTIVES = [
    "boucles-infinies",
    "erreurs-silencieuses",
    "blocage",
    "stop",
]

# LISTE CENTRALE DES PROTECTIONS (deploiement dynamique, demande utilisateur
# 2026-08-15) : ajouter une protection ICI la deploie automatiquement sur TOUS
# les tests qui importent ce module (template-test.md comme constructeur).
# Chaque entree : nom, type (stop / signal / chrono), deploiement
# (amont = au debut du test, aval = en fin de test), description.
LISTE_PROTECTIONS = [
    {"nom": "boucles-infinies", "type": "stop",
     "deploiement": "amont",
     "description": "Depassement de delai : arret force de l arbre (timeout)"},
    {"nom": "erreurs-silencieuses", "type": "signal",
     "deploiement": "aval",
     "description": "stderr non vide / mots-cles d erreur : signalement (le test juge)"},
    {"nom": "blocage", "type": "stop",
     "deploiement": "amont",
     "description": "Pas de reponse pendant X sec : arret force + STOP"},
    {"nom": "stop", "type": "stop",
     "deploiement": "aval",
     "description": "Point critique en echec : arret immediat du test (fail-fast)"},
    {"nom": "chrono", "type": "chrono",
     "deploiement": "amont+aval",
     "description": "Mesure des durees par etape (point_actif / chrono_etape / bilan_chrono) + option --no-chrono"},
    {"nom": "options-on-off", "type": "outil",
     "deploiement": "amont",
     "description": "--isoler N / --desactiver 1,3,5 : isoler un test ou desactiver des points sans toucher au code"},
    {"nom": "rating", "type": "chrono",
     "deploiement": "aval",
     "description": "Affiche en fin de test le rating GENERAL des tests et le rating du test (evaluer-rating, demande utilisateur 2026-08-15)"},
]

TIMEOUT_DEFAUT = 120
MOTS_CLES_ERREUR = ("error", "erreur", "failed", "echec", "exception", "fatal")


class ArretProtection(Exception):
    """Levee par une protection STOP : le test doit s arreter immediatement."""

    def __init__(self, message, type_protection="stop"):
        super(ArretProtection, self).__init__(message)
        self.message = message
        self.type_protection = type_protection


def tuer_arbre(pid):
    """Tuer un processus et tout son arbre (cross-platform)."""
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(pid)],
            capture_output=True,
            shell=False,
        )
    else:
        try:
            os.killpg(pid, signal.SIGKILL)
        except OSError:
            pass


def _options_lancement(shell, kwargs):
    """Options de lancement : nouvelle session pour pouvoir tuer l arbre."""
    options = dict(kwargs)
    options["shell"] = shell
    options.pop("capture_output", None)
    if "stdout" not in options:
        options["stdout"] = subprocess.PIPE
    if "stderr" not in options:
        options["stderr"] = subprocess.PIPE
    options.setdefault("text", True)
    if sys.platform == "win32":
        options["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        options["start_new_session"] = True
    return options


def lancer_protege(cmd, timeout=TIMEOUT_DEFAUT, **kwargs):
    """Executer une commande SOUS PROTECTION (timeout + tuer l arbre).

    REMPLACEMENT DIRECT de subprocess.run : accepte les memes parametres
    (capture_output, text, encoding, errors, cwd, env, ...) et retourne un
    objet compatible (returncode, stdout, stderr). La difference : le timeout
    tue TOUT l arbre de processus (cross-platform) et leve ArretProtection au
    lieu de laisser le test continuer betement.

    Args:
        cmd: liste de mots (shell=False) ou chaine (shell=True).
        timeout: delai maximum en secondes avant arret force.
        **kwargs: parametres compatibles subprocess.run.

    Leve:
        ArretProtection si le timeout expire (boucle infinie ou blocage) :
        la suite du test doit s arreter immediatement.
    """
    shell = isinstance(cmd, str)

    proc = subprocess.Popen(cmd, **_options_lancement(shell, kwargs))
    try:
        sortie_out, sortie_err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        message = ("[STOP] Protection boucles-infinies/blocage : la commande a "
                   "depasse %ds - arret force de l arbre de processus" % timeout)
        print(message, flush=True)
        tuer_arbre(proc.pid)
        try:
            sortie_out, sortie_err = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            sortie_out, sortie_err = "", ""
        if sortie_out.strip():
            print("  -> Sortie partielle (fin):", flush=True)
            for ligne in sortie_out.splitlines()[-5:]:
                print(ligne, flush=True)
        raise ArretProtection(message, type_protection="boucles-infinies")
    except OSError as e:
        raise ArretProtection(
            "[STOP] Impossible de lancer la commande: %s (%s)" % (cmd, e),
            type_protection="lancement")

    stdout = sortie_out or ""
    stderr = sortie_err or ""

    # Protection erreurs-silencieuses : signaler (sans changer le code retour,
    # c est le test qui juge via verifier_critique / verifier).
    if stderr.strip() and proc.returncode != 0:
        print("[PROTECTIONS] Attention: erreurs dans stderr (code %d):"
              % proc.returncode, flush=True)
        for ligne in stderr.splitlines()[:5]:
            print("  %s" % ligne, flush=True)
    for mot in MOTS_CLES_ERREUR:
        if mot in stdout.lower() and proc.returncode != 0:
            print("[PROTECTIONS] Attention: mot-cle '%s' dans stdout (code %d)"
                  % (mot, proc.returncode), flush=True)
            break

    return SimpleNamespace(returncode=proc.returncode, stdout=stdout,
                           stderr=stderr)


def verifier_critique(nom, condition, detail=""):
    """PROTECTION STOP : verifie un point CRITIQUE du test.

    Si la condition est fausse : affiche [KO] puis LEVE ArretProtection -
    le test s arrete immediatement (fail-fast) au lieu de continuer betement
    les points suivants.

    Args:
        nom: nom du point verifie.
        condition: booleen (True = OK, False = KO -> STOP).
        detail: detail optionnel affiche en cas de KO.

    Leve:
        ArretProtection si la condition est fausse.
    """
    if condition:
        print("  [OK] %s" % nom, flush=True)
        return
    message = "%s %s" % (nom, ("-- " + detail) if detail else "")
    print("  [KO] %s" % message, flush=True)
    raise ArretProtection(
        "[STOP] Point critique en echec: %s" % message,
        type_protection="stop")


def afficher_rating(nom_test, profil="test", verbose=False):
    """Affiche le rating du test courant et le rating general (protection
    'rating', demande utilisateur 2026-08-15). Appelle l outil evaluer-rating
    en sous-processus. No-op silencieux si l outil est introuvable ou en
    echec (jamais bloquant pour le test)."""
    racine = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
    outil = os.path.join(racine, "cerveau-projet", "agents", "tools",
                         "evaluer", "evaluer-rating", "evaluer-rating.py")
    if not os.path.exists(outil):
        return
    try:
        p = subprocess.run([sys.executable, outil, "--profil", profil,
                            "--cible", nom_test, "--no-chrono"],
                           capture_output=True, text=True, timeout=60)
        if p.stdout:
            print(p.stdout.rstrip())
        p2 = subprocess.run([sys.executable, outil, "--profil", "test",
                             "--general", "--no-chrono"],
                            capture_output=True, text=True, timeout=60)
        if p2.stdout:
            print(p2.stdout.rstrip())
    except Exception:
        pass


def charger_protections():
    """Helper pour les tests : charge CE module et retourne le module.

    Usage dans un test-0XX (template-test.md) :
        PROTECTIONS = charger_protections()
        r = PROTECTIONS.lancer_protege(cmd, timeout=60)
        PROTECTIONS.verifier_critique("3. ...", condition, detail)

    Note : ce helper est destine a etre appele depuis un test ; le chemin du
    module est resolu relatif a ce fichier, donc il fonctionne quel que soit
    le repertoire de travail.
    """
    return sys.modules.get(__name__) or __import__(__name__)


def _cli():
    parser = argparse.ArgumentParser(
        prog="tester-protections",
        description="Point d entree unique des protections de tests "
                    "(importable depuis chaque test-0XX).")
    parser.add_argument("--version", action="version",
                        version="tester-protections v%s (%s)"
                                % (VERSION, STATUT))
    parser.add_argument("--liste", action="store_true",
                        help="Affiche la liste des protections actives")
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()
    if args.liste:
        print("LISTE CENTRALE DES PROTECTIONS (%d) :" % len(LISTE_PROTECTIONS))
        for p in LISTE_PROTECTIONS:
            print("  - %-18s [%-6s] %-9s %s" % (p["nom"], p["type"],
                                                p["deploiement"], p["description"]))
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
