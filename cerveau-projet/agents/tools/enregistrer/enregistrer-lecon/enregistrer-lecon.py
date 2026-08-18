#!/usr/bin/env python3
# -*- coding: ascii -*-
"""enregistrer-lecon.py
Enregistre une lecon dans la BDD portable des lecons (SQLite, unique et
partagee : cerveau-projet/agents/lecons/lecons.db).

La BDD est la MEMOIRE LONGUE des lecons des agents (les corrections.md
restent la memoire COURTE, fenetre glissante des missions proches). Chaque
agent n ecrit QUE ses propres lecons (anti-usurpation) ; la lecture est
faite par consulter-lecons.

Usage:
  python3 enregistrer-lecon.py --agent <auteur> --titre <titre> --lecon <texte> [OPTIONS]

Options:
  --agent <auteur>       Auteur de la lecon (OBLIGATOIRE = agent actif)
  --domaine <d>          Domaine/theme (outil, test, carte, protocole...)
  --tags <t1,t2>         Tags separes par des virgules
  --titre <titre>        Titre court de la lecon
  --lecon <texte>        Corps de la lecon (ou --lecon-fichier)
  --lecon-fichier <f>    Fichier contenant le corps de la lecon
  --mission <contexte>   Contexte de la mission (optionnel)
  --outils <o1,o2>       Outils concernes (optionnel)
  --verdict <v>          Verdict associe (optionnel)
  --version              Affiche la version
  --aide                 Affiche cette aide

Version : 0.1.0
"""
import argparse
import datetime
import io
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
    """Initialise la BDD (idempotent : CREATE TABLE IF NOT EXISTS)."""
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
    """Retourne l agent actif REEL de la session (colonne 'Agent actif' de la
    table '## Sessions connues' d AGENTS.md, session la plus recente)."""
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
        if not ligne.startswith("| session-llm-"):
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


def verifier_ascii(texte):
    """Retourne True si le texte est 100% ASCII (0-127)."""
    return all(ord(c) <= 127 for c in texte)


def afficher_messages_info(messages):
    if not messages:
        return
    print("")
    print("=== MESSAGES POUR L AGENT ===")
    for message in messages:
        print("  > %s" % message)


def main():
    parser = argparse.ArgumentParser(
        prog="enregistrer-lecon",
        description="Enregistre une lecon dans la BDD portable des lecons (SQLite).")
    parser.add_argument("--agent", metavar="NOM",
                        help="auteur de la lecon (obligatoire = agent actif)")
    parser.add_argument("--domaine", default="", help="domaine/theme")
    parser.add_argument("--tags", default="", help="tags separes par des virgules")
    parser.add_argument("--titre", default="", help="titre court de la lecon")
    parser.add_argument("--lecon", default="", help="corps de la lecon")
    parser.add_argument("--lecon-fichier", default="",
                        help="fichier contenant le corps de la lecon")
    parser.add_argument("--mission", default="", help="contexte de la mission")
    parser.add_argument("--outils", default="", help="outils concernes")
    parser.add_argument("--verdict", default="", help="verdict associe")
    parser.add_argument("--version", action="store_true", help="affiche la version")
    parser.add_argument("--aide", action="help",
                        help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    if args.version:
        sys.stdout.write("enregistrer-lecon v%s\n" % VERSION)
        sys.exit(0)

    if not args.agent:
        sys.stderr.write("ERREUR : --agent est OBLIGATOIRE (auteur de la lecon).\n")
        sys.exit(2)

    racine = detecter_racine()
    actif = agent_actif_session(racine)
    if actif is None:
        sys.stderr.write("ERREUR : agent actif de session indeterminable "
                         "(table '## Sessions connues' absente). Activez d abord "
                         "un agent.\n")
        sys.exit(2)

    # ANTI-USURPATION : chaque agent n ecrit QUE ses propres lecons.
    if args.agent.lower() != actif.lower():
        sys.stdout.write(
            "REFUSE (anti-usurpation) : vous ne pouvez ecrire que VOS lecons.\n"
            "  --agent declare : %s\n"
            "  agent actif session : %s\n" % (args.agent, actif))
        sys.exit(1)

    # VERROU D HABILITATION + auto-journalisation.
    code_verrou, msg_verrou = verrouiller_habilitation(actif,
                                                       "enregistrer-lecon",
                                                       racine)
    if code_verrou != 0:
        sys.stdout.write(msg_verrou + "\n")
        sys.exit(code_verrou)

    # Corps de la lecon.
    lecon = args.lecon
    if args.lecon_fichier:
        try:
            with io.open(args.lecon_fichier, "r", encoding="utf-8") as f:
                lecon = f.read()
        except (IOError, OSError) as e:
            sys.stderr.write("ERREUR : lecture du fichier lecon impossible : "
                             "%s\n" % e)
            sys.exit(2)
    if not lecon.strip():
        sys.stderr.write("ERREUR : lecon vide (--lecon ou --lecon-fichier "
                         "obligatoire).\n")
        sys.exit(2)

    # ASCII strict sur tous les champs.
    champs = [args.agent, args.domaine, args.tags, args.titre, lecon,
              args.mission, args.outils, args.verdict]
    for champ in champs:
        if not verifier_ascii(champ):
            sys.stdout.write("REFUSE : caractere non-ASCII detecte (regle "
                             "immuable ASCII strict). Corrigez puis relancez.\n")
            sys.exit(1)

    date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_path = chemin_bdd(racine)
    init_db(db_path)

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        # ANTI-DOUBLON : meme agent + titre + corps deja present.
        cur.execute("SELECT id FROM lecons WHERE agent = ? AND titre = ? "
                    "AND lecon = ?", (args.agent, args.titre, lecon))
        existant = cur.fetchone()
        if existant:
            sys.stdout.write(
                "SIGNALE (doublon) : une lecon identique existe deja (id=%s, "
                "agent=%s, titre='%s'). Rien n a ete re-ecrit.\n"
                % (existant[0], args.agent, args.titre))
            sys.exit(1)
        cur.execute(
            "INSERT INTO lecons (date, agent, domaine, tags, titre, lecon, "
            "mission, outils, verdict) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (date_now, args.agent, args.domaine, args.tags, args.titre, lecon,
             args.mission, args.outils, args.verdict))
        conn.commit()
        nid = cur.lastrowid
    finally:
        conn.close()

    print("=== LECON ENREGISTREE ===")
    print("  id      : %d" % nid)
    print("  date    : %s" % date_now)
    print("  agent   : %s" % args.agent)
    print("  domaine : %s" % (args.domaine or "-"))
    print("  titre   : %s" % (args.titre or "-"))

    total = time.monotonic() - T_START
    if CHRONO_ACTIF:
        print("")
        print("=== CHRONO enregistrer-lecon (total %.2fs) ===" % total)

    afficher_messages_info([
        "lecon ecrite dans la BDD : consulter avec consulter-lecons",
        "corrections.md reste la fenetre glissante des missions proches "
        "(voir protocole lecons)",
    ])
    return 0


if __name__ == "__main__":
    sys.exit(main())
