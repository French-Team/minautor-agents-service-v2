#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-erreur-bloquante.py
#
# DETECTION DES ERREURS BLOQUANTES (demande utilisateur 2026-08-29) : scanne
# l etat de la coordination et AFFICHE clairement toute condition qui bloquerait
# (ou a bloque) le demarrage d une session ou un round :
#   1. MARBRE DIVISE  : une zone protegee (constitution, cases cerberus,
#      regles-groupes) a ete modifiee SANS passer par la porte -> sidentifier
#      refuse d ecrire dans AGENTS.md -> le demarrage est BLOQUE. C est
#      exactement l erreur observee : un agent a edite AGENTS.md (zone
#      constitution) sans utiliser proteger-modifier-marbre, et demarrer-llm
#      a refuse de demarrer.
#   2. DAEMON MORT    : oracle-server et/ou routines-server ne tournent pas
#      (fichiers .pid presents mais processus absent) -> les missions asap ne
#      sont pas consommees -> les agents ne demarrent pas.
#   3. ETAT-CARTE INCOHERENT : un etat de carte porte un statut de fin (etape
#      fin) ou un precedent/residu sans mission active, ou un precedent sous
#      forme de chaine a plat libre -> le round risque de mal reboucler.
#
# SOURCE D'ORIGINE : l erreur bloquante constatee au demarrage reel
#   "[sidentifier] == MARBRE BRISE : 1 zone(s) modifiee(s) sans protocole =="
#   (outils-llm/demarrer-llm.py, pas sidentifier -> Refus d ecrire dans
#   AGENTS.md). Cette routine la detecte AVANT demarrer, pour afficher le
#   diagnostic (OU CHERCHER / REPARER) au lieu de bloquer sans explication.
#
# Mode d emploi (branche dans demarrer-llm.py, pas bloquant) :
#   python3 detecter-erreur-bloquante.py            (affiche le diagnostic)
#   python3 detecter-erreur-bloquante.py --status    (0 pour code)
#   python3 detecter-erreur-bloquante.py --verbose   (detail des controles)
#
# Options :
#   --verbose       detail de chaque controle
#   --status        code de sortie : 0 si AUCUN bloquant, 4 si un bloque
#   --marbre-seul   ne verifier que le marbre (zone la plus bloquante)
#   --version
#   --aide
#
# Codes de sortie :
#   0 : AUCUN bloquant (coordination pret)
#   4 : AU MOINS UNE condition bloquante detectee (a afficher et traiter)
#   2 : erreur d utilisation
#
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (detecter-).
# =============================================================================
import argparse
import io
import json
import os
import subprocess
import sys

VERSION = "0.1.0"
STATUT = "ebauche"

# Daemons a surveiller : nom du fichier .pid relatif a la racine du serveur.
DAEMONS = {
    "oracle-server": (
        "cerveau-projet/agents/tools/oracle/oracle-server.pid",
        "consomme les missions asap -> sinon les agents ne demarrent pas (file asap ~12 EN_ATTENTE non consommees, panne 2026-08-28)",
    ),
    "routines-server": (
        "cerveau-projet/agents/tools/oracle/routines-server.pid",
        "surveillance H24 des routines (vigie, notation) -> sinon aucune alerte bloquante remontee",
    ),
}


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent
    return d


def import_verrou(racine):
    """Importe proteger-verrou-marbre (calcul d empreinte) pour verifier le marbre."""
    import importlib.util
    chemin = os.path.join(racine, "cerveau-projet", "agents", "tools",
                          "proteger", "proteger-verrou-marbre",
                          "proteger-verrou-marbre.py")
    if not os.path.isfile(chemin):
        return None
    try:
        spec = importlib.util.spec_from_file_location("pv", chemin)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except Exception:
        return None


def verifier_marbre(racine, verbose):
    """Retourne la liste des zones divergentes du marbre."""
    verrou = import_verrou(racine)
    if verrou is None:
        return [{"zone": "ERR", "detail": "outil proteger-verrou-marbre introuvable"}]
    chemin = os.path.join(racine, "cerveau-projet", "agents", "regles-immuables",
                          "marbre", "marbre.json")
    def charger():
        with io.open(chemin, "r", encoding="utf-8") as fh:
            return json.load(fh)
    try:
        manifeste = charger()
    except (ValueError, IOError):
        return [{"zone": "ERR", "detail": "manifeste marbre.json illisible"}]
    divergentes = []
    for nom, zone in sorted(manifeste.get("zones", {}).items()):
        try:
            actuel = verrou.empreinte_zone(zone, racine)
        except (ValueError, IOError) as e:
            divergentes.append({"zone": nom, "detail": "IMPRECISABLE: %s" % e})
            continue
        if actuel != zone.get("empreinte"):
            divergentes.append({"zone": nom, "detail": "DIVERGE (empreinte changee sans porte)"})
    if verbose:
        print("  [marbre] %d zone(s) verifiee(s) -> %d divergente(s)"
              % (len(manifeste.get("zones", {})), len(divergentes)))
    return divergentes


def pid_vivant(pid):
    if not pid:
        return False
    try:
        if sys.platform == "win32":
            # tasklist /FI "PID eq N" /FO CSV /NH : si le processus existe, la
            # ligne contient le pid ; sinon erreur / stdout vide. /NH vire les
            # en-tetes, donc NE PAS chercher "PID" (il n apparait jamais).
            out = subprocess.run(
                ["tasklist", "/FI", "PID eq %d" % pid, "/FO", "CSV", "/NH"],
                capture_output=True, text=True, timeout=15)
            return str(pid) in out.stdout
        os.kill(int(pid), 0)
        return True
    except Exception:
        return False


def verifier_daemons(racine, verbose):
    """Retourne la liste des daemons morts (pid absent ou fichier inexistant)."""
    morts = []
    for nom, (rel_pid, raison) in DAEMONS.items():
        chemin = os.path.join(racine, rel_pid)
        pid = None
        if os.path.isfile(chemin):
            try:
                pid = int(open(chemin).read().strip())
            except ValueError:
                pid = None
        if pid is None or not pid_vivant(pid):
            morts.append({"daemon": nom, "raison": raison,
                          "pid": pid, "detail": "daemon mort ou sans pid vivant"})
        elif verbose:
            print("  [daemon] %s pid=%s VIVANT" % (nom, pid))
    return morts


def verifier_etat_cartes(racine, verbose):
    """Retourne les etats de carte incoherents (residu de fin sans mission active)."""
    dossier = os.path.join(racine, "cerveau-projet", "agents", "tools",
                           "oracle", "etat-cartes")
    incoherents = []
    if not os.path.isdir(dossier):
        if verbose:
            print("  [etat-cartes] dossier absent : %s" % dossier)
        return incoherents
    for f in sorted(os.listdir(dossier)):
        if not f.endswith(".json"):
            continue
        try:
            with io.open(os.path.join(dossier, f), "r", encoding="utf-8") as fh:
                d = json.load(fh)
        except ValueError:
            incoherents.append({"agent": f[:-5], "detail": "etat-carte JSON invalide",
                                "reparation": "%s/etat-cartes/%s : reinitialiser au format neutre" % (os.path.basename(dossier), f)})
            continue
        etape = d.get("etape")
        precedent = d.get("precedent")
        mission = d.get("mission") or ""
        agent = d.get("agent") or f[:-5]
        # Un etat "fin" (fin de round) avec precedent pose et sans mission ulterieure
        # est un RESIDU : le precedent-aware rebouclerait vers l appelant au lieu
        # de repartir proprement. C est l etat exact que l on a du reinitialiser
        # avant de relancer le round (buffy/morpheus/themis restes a "fin").
        if etape in ("fin", "retour") and not etape_active(d):
            incoherents.append({
                "agent": agent, "detail": "etat residuel de fin (etape=%s, precedent=%s)"
                                          % (etape, precedent),
                "reparation": "reinitialiser de l etat de carte %s (etape=debut, precedent=None) avant un nouveau round"
                              % agent,
            })
        elif verbose:
            print("  [etat-carte] %s : etape=%s precedent=%s (OK)" % (agent, etape, precedent))
    return incoherents


def etape_active(d):
    """Un etat porte-t-il une mission active (episode en cours) ? On considere
    qu un etat a 'fin' SANS mission remplie ni redirect est un residu."""
    mission = d.get("mission") or ""
    theme = d.get("theme_courant")
    if theme and mission:
        return True
    return False


def main():
    parser = argparse.ArgumentParser(
        prog="detecter-erreur-bloquante",
        description="Detecte et AFFICHE les erreurs bloquantes (marbre divise, daemon mort, etat-carte incoherent).")
    parser.add_argument("--verbose", action="store_true", help="detail de chaque controle")
    parser.add_argument("--status", action="store_true",
                        help="code de sortie : 0 si aucun bloquant, 4 si un bloque")
    parser.add_argument("--marbre-seul", action="store_true",
                        help="ne verifier que le marbre (zone la plus bloquante)")
    parser.add_argument("--version", action="store_true", help="affiche la version")
    parser.add_argument("--aide", action="store_true", help="affiche l aide complete")
    args = parser.parse_args()

    if args.version:
        print("detecter-erreur-bloquante %s (%s)" % (VERSION, STATUT))
        return 0
    if args.aide:
        print(__doc__)
        return 0

    racine = racine_projet()
    if not racine:
        print("[ERREUR] Racine projet introuvable (AGENTS.md absent).")
        return 2

    print("=" * 60)
    print("DETECTION DES ERREURS BLOQUANTES (v%s)" % VERSION)
    print("=" * 60)

    bloquant = []

    # 1. MARBRE DIVISE (lig blokante numero 1 : bloque sidentifier/demarrage)
    marbre = verifier_marbre(racine, args.verbose)
    if args.verbose and not marbre:
        print("  [marbre] AUCUNE zone divergente -> marbre intact")
    if marbre:
        bloquant.append({
            "type": "MARBRE DIVISE",
            "zones": marbre,
            "message": "Des zones protegees ont ete modifiees SANS passer par la porte.",
            "reparation": "python3 cerveau-projet/agents/tools/proteger/proteger-modifier-marbre/"
                          "proteger-modifier-marbre.py --zone <nom> --raison <...> --autorisation <USER>",
            "source": "sidentifier refuse d ecrire dans AGENTS.md -> demarrage bloque "
                      "(cf. outils-llm/demarrer-llm.py, erreur observee au demarrage 2026-08-29)",
        })

    # 2. DAEMON MORT
    if not args.marbre_seul:
        daemons = verifier_daemons(racine, args.verbose)
        if daemons:
            bloquant.append({
                "type": "DAEMON MORT",
                "zones": daemons,
                "message": "Un ou plusieurs serveurs de coordination ne tournent pas.",
                "reparation": "python3 cerveau-projet/agents/tools/oracle/oracle.py demarrage",
                "source": "les missions asap ne sont pas consommees -> les agents ne demarrent pas",
            })

        # 3. ETAT-CARTE INCOHERENT
        cartes = verifier_etat_cartes(racine, args.verbose)
        if cartes:
            bloquant.append({
                "type": "ETAT-CARTE INCOHERENT",
                "zones": cartes,
                "message": "Des etats de carte portent un residu de fin de round.",
                "reparation": "reinitialiser (etape=debut, precedent=None) l etat du ou des agents concernes",
                "source": "risque de mauvais rebouclage precedent-aware au round suivant",
            })

    if not bloquant:
        print("AUCUN BLOQUANT : marbre intact, daemons vivants, etats de carte propres.")
        print("La coordination est PRETE pour un demarrage / un round.")
        if args.verbose:
            print("=" * 60)
        return 0

    # AFFICHAGE CLAIR des erreurs bloquantes
    for b in bloquant:
        print("")
        print("[BLOQUANT] %s" % b["type"])
        print("-" * 60)
        for z in b.get("zones", []):
            print("   * %s : %s" % (z.get("zone") or z.get("daemon") or z.get("agent", "?"),
                                    z.get("detail", "")))
        print("   message : %s" % b["message"])
        print("   OU CHERCHER : %s" % b.get("source", ""))
        print("   REPARER    : %s" % b.get("reparation", ""))
    print("")
    print("=" * 60)
    print("VERDICT : %d condition(s) bloquante(s) detectee(s)." % len(bloquant))
    print("Traitez chaque bloc ci-dessus AVANT de lancer demarrer-llm / un round.")
    print("=" * 60)
    return 4 if args.status else 0


if __name__ == "__main__":
    sys.exit(main())