#!/usr/bin/env python3
# -*- coding: ascii -*-
"""consulter-lecons.py
Consulte la BDD portable des lecons (SQLite, unique et partagee :
cerveau-projet/agents/lecons/lecons.db). Permet la pollinisation croisee :
chaque agent peut lire les lecons des autres (evolution entre eux).

La lecture est verrouillee (verrou d habilitation) et JOURNALISEE (controle
d activite : qui a consulte quoi). L ecriture est faite par enregistrer-lecon.

Usage:
  python3 consulter-lecons.py --agent <lecteur> [FILTRES]

Options:
  --agent <lecteur>      Agent qui consulte (OBLIGATOIRE)
  --toutes               Lister toutes les lecons
  --auteur <agent>       Filtrer par auteur
  --domaine <d>          Filtrer par domaine
  --tags <t>             Filtrer par tag (LIKE)
  --recent <N>           N lecons les plus recentes
  --recherche <motif>    Recherche dans titre/lecon/mission (LIKE)
  --rapport <fichier>    Ecrire un rapport markdown
  --version              Affiche la version
  --aide                 Affiche cette aide

Version : 0.1.0
"""
import argparse
import datetime
import io
import json
import os
import re
import sqlite3
import subprocess
import sys
import time

VERSION = "0.1.0"

T_START = time.monotonic()
CHRONO_ACTIF = True


def detecter_racine():
    """Detecte la racine du projet (dossier contenant AGENTS.md)."""
    courant = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(courant, "AGENTS.md")):
            return courant
        parent = os.path.dirname(courant)
        if parent == courant:
            break
        courant = parent
    sys.stderr.write("ERREUR : racine du projet introuvable (AGENTS.md absent).\n")
    sys.exit(2)


def chemin_bdd(racine):
    """Chemin de la BDD unique des lecons."""
    return os.path.join(racine, "cerveau-projet", "agents", "lecons",
                        "lecons.db")


def init_db(db_path):
    """Initialise la BDD si absente (idempotent)."""
    dossier = os.path.dirname(db_path)
    if not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS lecons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                agent TEXT NOT NULL,
                domaine TEXT DEFAULT '',
                tags TEXT DEFAULT '',
                titre TEXT DEFAULT '',
                lecon TEXT NOT NULL,
                mission TEXT DEFAULT '',
                outils TEXT DEFAULT '',
                verdict TEXT DEFAULT ''
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_lecons_agent "
                    "ON lecons(agent)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_lecons_date "
                    "ON lecons(date)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_lecons_domaine "
                    "ON lecons(domaine)")
        conn.commit()
    finally:
        conn.close()


def agent_actif_session(racine):
    """Retourne l agent actif REEL de la session."""
    chemin = os.path.join(racine, "AGENTS.md")
    try:
        with io.open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()
    except IOError:
        return None
    m = re.search(r"## Sessions connues\n(.*?)(?=\n## |\Z)", contenu, re.S)
    if not m:
        return None
    lignes = []
    for ligne in m.group(1).splitlines():
        ligne = ligne.strip()
        if not ligne.startswith("| session-"):
            continue
        cellules = [c.strip() for c in ligne.strip("|").split("|")]
        if len(cellules) >= 4:
            lignes.append(cellules)
    if not lignes:
        return None
    lignes.sort(key=lambda c: c[3], reverse=True)
    actif = lignes[0][2].strip()
    return actif if actif and actif != "-" else None


def verrouiller_habilitation(agent, outil, racine):
    """Appelle proteger-verrou-habilitation et retourne (code, message)."""
    verrou = os.path.join(racine, "cerveau-projet", "agents", "tools",
                          "proteger", "proteger-verrou-habilitation",
                          "proteger-verrou-habilitation.py")
    if not os.path.isfile(verrou):
        return (2, "[ERREUR] Verrou introuvable : %s" % verrou)
    r = subprocess.run(
        [sys.executable, verrou, "--agent", agent, "--outil", outil],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (r.returncode, (r.stdout + r.stderr).strip())


def journaliser_consultation(racine, agent, filtre):
    """Journalise la consultation (controle d activite : qui a consulte quoi).
    Entree mode 'direct' dans registre-usages-outils.jsonl, triee ensuite."""
    traces = os.path.join(racine, "cerveau-projet", "agents", "traces")
    if not os.path.isdir(traces):
        return
    registre = os.path.join(traces, "registre-usages-outils.jsonl")
    entree = {
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent": agent,
        "outil": "consulter-lecons",
        "mode": "direct",
        "commande": "",
        "contexte": "consultation lecons (filtre: %s)" % filtre,
    }
    try:
        with io.open(registre, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps(entree, ensure_ascii=True,
                                separators=(",", ":")) + "\n")
        trier_registre(registre)
    except (IOError, OSError):
        pass


def trier_registre(registre):
    """Trie un registre JSONL par date, decroissant (le plus recent en
    premier). Idempotent."""
    try:
        with io.open(registre, encoding="utf-8") as fh:
            lignes = [l.rstrip("\n") for l in fh if l.strip()]
    except (IOError, OSError):
        return
    valides = []
    invalides = []
    for l in lignes:
        try:
            e = json.loads(l)
            valides.append((e.get("date", ""), l))
        except ValueError:
            invalides.append(l)
    valides.sort(key=lambda paire: paire[0], reverse=True)
    triees = [l for _, l in valides] + invalides
    try:
        with io.open(registre, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(triees) + "\n")
    except (IOError, OSError):
        pass


def formater(entree):
    """Formate une ligne de lecon pour l affichage."""
    return ("#%d | %s | %s | %s | %s" % (
        entree[0], entree[1], entree[2], entree[3] or "-",
        (entree[5] or "")[:60]))


def afficher_messages_info(messages):
    if not messages:
        return
    print("")
    print("=== MESSAGES POUR L AGENT ===")
    for message in messages:
        print("  > %s" % message)


def main():
    parser = argparse.ArgumentParser(
        prog="consulter-lecons",
        description="Consulte la BDD portable des lecons (SQLite).")
    parser.add_argument("--agent", metavar="NOM",
                        help="agent qui consulte (obligatoire)")
    parser.add_argument("--toutes", action="store_true",
                        help="lister toutes les lecons")
    parser.add_argument("--auteur", default="", help="filtrer par auteur")
    parser.add_argument("--domaine", default="", help="filtrer par domaine")
    parser.add_argument("--tags", default="", help="filtrer par tag (LIKE)")
    parser.add_argument("--recent", type=int, default=0,
                        help="N lecons les plus recentes")
    parser.add_argument("--recherche", default="",
                        help="recherche dans titre/lecon/mission (LIKE)")
    parser.add_argument("--rapport", default="",
                        help="ecrire un rapport markdown")
    parser.add_argument("--version", action="store_true",
                        help="affiche la version")
    parser.add_argument("--aide", action="help",
                        help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    if args.version:
        sys.stdout.write("consulter-lecons v%s\n" % VERSION)
        sys.exit(0)

    if not args.agent:
        sys.stderr.write("ERREUR : --agent est OBLIGATOIRE (qui consulte).\n")
        sys.exit(2)

    racine = detecter_racine()
    actif = agent_actif_session(racine)
    if actif is None:
        sys.stderr.write("ERREUR : agent actif de session indeterminable. "
                         "Activez d abord un agent.\n")
        sys.exit(2)

    # VERROU D HABILITATION + auto-journalisation.
    code_verrou, msg_verrou = verrouiller_habilitation(actif,
                                                       "consulter-lecons",
                                                       racine)
    if code_verrou != 0:
        sys.stdout.write(msg_verrou + "\n")
        sys.exit(code_verrou)

    db_path = chemin_bdd(racine)
    init_db(db_path)

    # Construction de la requete.
    where = []
    params = []
    if args.auteur:
        where.append("agent = ?")
        params.append(args.auteur)
    if args.domaine:
        where.append("domaine = ?")
        params.append(args.domaine)
    if args.tags:
        where.append("tags LIKE ?")
        params.append("%" + args.tags + "%")
    if args.recherche:
        where.append("(titre LIKE ? OR lecon LIKE ? OR mission LIKE ?)")
        motif = "%" + args.recherche + "%"
        params.extend([motif, motif, motif])
    clause = (" WHERE " + " AND ".join(where)) if where else ""
    limite = " LIMIT %d" % args.recent if args.recent > 0 else ""
    sql = ("SELECT id, date, agent, domaine, tags, titre, lecon, mission, "
           "outils, verdict FROM lecons" + clause +
           " ORDER BY date DESC, id DESC" + limite)

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        lignes = cur.fetchall()
    finally:
        conn.close()

    filtre = "tout" if args.toutes else (
        "auteur=%s" % args.auteur if args.auteur else
        "domaine=%s" % args.domaine if args.domaine else
        "recherche=%s" % args.recherche if args.recherche else
        "recent=%d" % args.recent if args.recent else "tout")
    journaliser_consultation(racine, args.agent, filtre)

    print("=== LECONS (%d resultat(s)) ===" % len(lignes))
    for l in lignes:
        print("  " + formater(l))
    if not lignes:
        print("  (aucune lecon pour ces filtres)")

    if args.rapport:
        try:
            with io.open(args.rapport, "w", encoding="utf-8",
                         newline="\n") as fh:
                fh.write("# Rapport de consultation des lecons\n\n")
                fh.write("- Agent : %s\n" % args.agent)
                fh.write("- Filtre : %s\n" % filtre)
                fh.write("- Resultats : %d\n\n" % len(lignes))
                for l in lignes:
                    fh.write("## #%d - %s (%s, %s)\n\n%s\n\n---\n\n"
                             % (l[0], l[5] or "sans titre", l[2], l[1],
                                l[6] or ""))
            print("  Rapport ecrit : %s" % args.rapport)
        except (IOError, OSError) as e:
            sys.stderr.write("ERREUR : ecriture du rapport impossible : "
                             "%s\n" % e)
            sys.exit(2)

    total = time.monotonic() - T_START
    if CHRONO_ACTIF:
        print("")
        print("=== CHRONO consulter-lecons (total %.2fs) ===" % total)

    afficher_messages_info([
        "consultation journalisee (controle d activite : qui a lu quoi)",
        "pour ecrire une lecon : enregistrer-lecon (anti-usurpation : "
        "chaque agent n ecrit que ses lecons)",
    ])
    return 0


if __name__ == "__main__":
    sys.exit(main())
