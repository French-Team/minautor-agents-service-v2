# -*- coding: ascii -*-
# routine : orphelins (arret) -- detecte les fichiers orphelins (temporaires,
# sauvegardes, pidfiles perimes) a l'arret du serveur de routines et
# historise le resultat sous son nom (decision utilisateur 2026-08-26 :
# les routines sont des elements surveilles avec LEUR propre nom/grade -
# rouge G4).
# Creee 2026-08-26 (les entrees verifier-integrite/detecter-orphelins du
# manifest etaient mortes : scripts inexistants).
import os
import sys
from pathlib import Path

# P10 : racine DETECTEE en remontant jusqu'a AGENTS.md (jamais compte)
_d = os.path.dirname(os.path.abspath(__file__))
while not os.path.isfile(os.path.join(_d, "AGENTS.md")):
    _p = os.path.dirname(_d)
    if _p == _d:
        break
    _d = _p
RACINE = Path(_d)

SUFFIXES_ORPHELINS = (".tmp", ".bak", ".orig", ".rej", ".ag-", ".pyc")


def detecter():
    """Retourne la liste des fichiers orphelins trouves (vide si aucun)."""
    orphelins = []
    # racine : fichiers temporaires a la traine
    try:
        for f in RACINE.glob(".*.tmp"):
            orphelins.append(str(f.name))
        for f in RACINE.glob("*.tmp"):
            orphelins.append(str(f.name))
    except OSError:
        pass
    # pidfile du serveur : orphelin UNIQUEMENT si le processus est mort
    # (a l'arret, le daemon vit encore quand cette routine tourne : son
    # pidfile est legitime et ne doit PAS etre signale).
    pid_file = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / \
        "jarvis" / "routines-server.pid"
    if pid_file.is_file():
        try:
            pid = int(pid_file.read_text(encoding="utf-8").strip())
            vivant = False
            if os.name == "nt":
                import ctypes
                h = ctypes.windll.kernel32.OpenProcess(0x1000, False, pid)
                if h:
                    ctypes.windll.kernel32.CloseHandle(h)
                    vivant = True
            else:
                try:
                    os.kill(pid, 0)
                    vivant = True
                except OSError:
                    pass
            if not vivant:
                orphelins.append(pid_file.name + " (pid mort)")
        except (ValueError, OSError):
            orphelins.append(pid_file.name)
    # fichiers de sauvegarde dans le workspace freelance
    base = RACINE / "cerveau-projet" / "freelance"
    for suffixe in (".bak", ".orig", ".rej"):
        for f in base.rglob("*" + suffixe):
            orphelins.append(str(f.relative_to(base)))
    return orphelins


def main():
    try:
        orphelins = detecter()
        _fo = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / \
            "os_path" / "fonctions"
        _fj = RACINE / "cerveau-projet" / "freelance" / "tools-commun" / \
            "jarvis" / "fonctions"
        for p in (_fo, _fj):
            if str(p) not in sys.path:
                sys.path.insert(0, str(p))
        from historique import historiser
        if orphelins:
            raison = "%d orphelin(s): %s" % (len(orphelins),
                                             orphelins[0][:60])
        else:
            raison = "Aucun fichier orphelin detecte"
        historiser("orphelins", raison, "R", session="session-freelance")
        print("[ORPHELINS] %s" % raison)
    except Exception as e:
        print("[ROUTINE] ERREUR orphelins : %s" % e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
