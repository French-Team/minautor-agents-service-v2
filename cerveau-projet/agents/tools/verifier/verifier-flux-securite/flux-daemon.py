#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
flux-daemon.py -- Daemon de securite du flux.

Tourne en continu et verifie que le flux Oracle > Agent > Oracle est
respecte. Alertes en temps reel si anomalie detectee.

Lancement :
  python3 flux-daemon.py              # mode normal (toutes les 30s)
  python3 flux-daemon.py --loop 10    # toutes les 10s
  python3 flux-daemon.py --once       # une seule verification

Proprietaire : Buffy (responsable). Version : 0.1.0.
"""

import io
import os
import sys
import time
from datetime import datetime

VERSION = "0.1.0"

# Rechercher verifier-flux-securite.py dans le meme dossier
_DIR = os.path.dirname(os.path.abspath(__file__))
_VFS = os.path.join(_DIR, "verifier-flux-securite.py")


def _timestamp():
    return datetime.now().strftime("%H:%M:%S")


def _lire_derniere_entree():
    """Lire la derniere entree du tableau d activites."""
    ag = os.path.join(_DIR, "..", "..", "..", "..", "..",
                      "AGENTS-activite-recente.md")
    ag = os.path.normpath(ag)
    if not os.path.isfile(ag):
        return None
    try:
        contenu = io.open(ag, "r", encoding="utf-8", errors="replace").read()
        dernieres = [l.strip() for l in contenu.split("\n")
                     if l.strip().startswith("|") and not l.strip().startswith("| Grade")
                     and not l.strip().startswith("|---")]
        if dernieres:
            cols = [c.strip() for c in dernieres[0].split("|")]
            if len(cols) >= 9:
                return {
                    "grade": cols[1], "agent": cols[2], "df": cols[3],
                    "secteur": cols[4], "raison": cols[5], "heure": cols[6],
                }
    except Exception:
        pass
    return None


def _verifier():
    """Executer la verification et retourner (ok, nb_erreurs, msg)."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("vfs", _VFS)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        ok, erreurs = mod.verifier_flux()
        return ok, len(erreurs), erreurs
    except Exception as exc:
        return False, 1, ["Exception: %s" % exc]


def boucle(interval=30):
    """Boucle principale du daemon."""
    print("[%s] FLUX DAEMON demarre (v%s, verification toutes %ds)" % (
        _timestamp(), VERSION, interval))
    print("[%s] Fichier : %s" % (_timestamp(), _VFS))
    print()

    dernier_etat = None
    nb_verif = 0

    while True:
        nb_verif += 1
        ok, nb_err, erreurs = _verifier()
        derniere = _lire_derniere_entree()

        etat = "OK" if ok else "KO"
        agent_dernier = derniere["agent"] if derniere else "?"
        df_dernier = derniere["df"] if derniere else "?"

        # Afficher seulement si changement ou premiere verif
        if etat != dernier_etat or nb_verif == 1:
            if ok:
                print("[%s] FLUX OK (verif #%d) | Dernier: %s %s" % (
                    _timestamp(), nb_verif, agent_dernier, df_dernier))
            else:
                print("[%s] FLUX KO (verif #%d) | %d anomalie(s)" % (
                    _timestamp(), nb_verif, nb_err))
                for e in erreurs[:5]:
                    print("  - %s" % e)
                if nb_err > 5:
                    print("  ... et %d autres" % (nb_err - 5))
            dernier_etat = etat
        else:
            # Meme etat : point silencieux
            sys.stdout.write(".")
            sys.stdout.flush()

        time.sleep(interval)


def main():
    if "--version" in sys.argv:
        print("flux-daemon v%s" % VERSION)
        return 0

    interval = 30
    if "--loop" in sys.argv:
        idx = sys.argv.index("--loop")
        if idx + 1 < len(sys.argv):
            interval = int(sys.argv[idx + 1])

    if "--once" in sys.argv:
        ok, nb_err, erreurs = _verifier()
        if ok:
            print("FLUX OK")
        else:
            print("FLUX KO : %d anomalie(s)" % nb_err)
            for e in erreurs:
                print("  - %s" % e)
        return 0 if ok else 1

    try:
        boucle(interval)
    except KeyboardInterrupt:
        print("\n[%s] FLUX DAEMON arrete." % _timestamp())
    return 0


if __name__ == "__main__":
    sys.exit(main())
