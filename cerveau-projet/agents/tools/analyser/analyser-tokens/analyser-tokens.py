#!/usr/bin/env python3
# -*- coding: ascii -*-
# analyser-tokens.py
#
# Analyse la consommation de tokens de la session en cours : tokens ENVOYES,
# tokens RECUS et ENCOMBREMENT de la fenetre de contexte.
#
# MODELE HYBRIDE (decision utilisateur 2026-08-15) :
#   (a) REGISTRE LOCAL : estimation a partir des traces du cerveau-projet.
#       Chaque entree des registres (usages d outils, lancements de tests)
#       represente une activite reelle de la session. L estimation convertit
#       la taille des fichiers traces en tokens (heuristique ~4 caracteres
#       par token, valeur usuelle).
#   (b) COMPTEURS API REELS : si des metadonnees de session sont disponibles
#       (variable d environnement ou fichier JSON de metadonnees), l outil
#       les utilise en priorite (prompt_tokens / completion_tokens). Sinon,
#       il bascule sur l estimation locale avec un avertissement clair.
#
# La fenetre de contexte : encombrement = (envoyes + recus) / total.
# Le total par defaut est 200 000 tokens (large fenetre moderne) ; il peut
# etre fourni par les metadonnees API ou par --fenetre-total.
#
# Usage :
#   python3 analyser-tokens.py
#   python3 analyser-tokens.py --session session-llm-1
#   python3 analyser-tokens.py --rapport rapport-tokens.md
#   python3 analyser-tokens.py --verbose
#   python3 analyser-tokens.py --version
#
# Options :
#   --session <nom>     : session analysee (defaut : lue du classeur ou session-llm-1)
#   --fenetre-total <N> : taille totale de la fenetre de contexte (defaut 200000)
#   --rapport <fichier> : ecrit le rapport markdown
#   --verbose           : detail des sources (registres, metadonnees)
#   --dry-run           : affiche sans ecrire le rapport
#   --no-chrono         : coupe le chrono de l outil lui-meme
#   --version
#
# Version : 0.1.4
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (analyser-).
# =============================================================================
"""
analyser-tokens.py
analyser-tokens

Usage:
  analyser-tokens.py [OPTIONS]
"""

import argparse
import glob
import io
import json
import os
import re
import sys
import time


VERSION = "0.1.4"
STATUT = "ebauche"
CARACTERES_PAR_TOKEN = 4.0
FENETRE_TOTALE_DEFAUT = 200000


def _couleur(texte, nom="neutre"):
    codes = {"rouge": 31, "vert": 32, "jaune": 33, "bleu": 34, "neutre": 0}
    if not sys.stdout.isatty():
        return texte
    return "\033[%dm%s\033[0m" % (codes.get(nom, 0), texte)


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def session_par_defaut(racine):
    """MULTI-SESSIONS (v0.1.2) : session de l appelant -- variable
    d environnement SESSION_LLM (ex: session-llm-4) en priorite, sinon
    premiere session du classeur (profil-session-*), sinon session-llm-1 en
    secours. Chaque LLM peut travailler avec les memes agents dans SA session."""
    env = os.environ.get("SESSION_LLM", "").strip()
    if env:
        return env
    classeur = os.path.join(racine, "cerveau-projet", "agents",
                            "classeur-variables", "stockage",
                            "variables-actuelles.md")
    if os.path.isfile(classeur):
        for ligne in io.open(classeur, encoding="utf-8", errors="replace"):
            if "`profil-session-" in ligne and "session:" in ligne:
                m = re.search(r"session: (session-[a-z0-9_-]+)", ligne)
                if m:
                    return m.group(1)
    return "session-llm-1"


def charger_metadonnees_api(racine, session):
    """Cherche des metadonnees API (tokens reels) : d abord la variable
    d environnement TOKENS_SESSION, puis les fichiers metadonnees-session-*.
    Retourne dict ou None."""
    env = os.environ.get("TOKENS_SESSION", "").strip()
    if env:
        try:
            m = json.loads(env)
            if "prompt_tokens" in m or "completion_tokens" in m:
                return m
        except ValueError:
            pass
    motif = os.path.join(racine, "cerveau-projet", "agents", "traces",
                         "metadonnees-session-*.json")
    for chemin in sorted(glob.glob(motif)):
        try:
            m = json.load(io.open(chemin, encoding="utf-8"))
            if isinstance(m, dict) and ("prompt_tokens" in m
                                        or "completion_tokens" in m):
                return m
        except (ValueError, IOError):
            continue
    return None


def taille_caracteres(chemin):
    if not os.path.isfile(chemin):
        return 0
    try:
        with io.open(chemin, "rb") as fh:
            return len(fh.read())
    except IOError:
        return 0


def estimer_depuis_registres(racine, session, verbose=False):
    """Estimation locale : la taille des traces de la session (registres +
    fichiers de session) convertie en tokens (caracteres / 4).

    Chaque entree des registres represente une action reelle ; on mesure la
    taille du fichier de traces (proportionnel a l activite) et on estime :
      - tokens envoyes  : 60% de l activite totale (l entree, le contexte)
      - tokens recus    : 40% de l activite totale (les sorties)
    Cette estimation est HONNETEMENT signalee comme heuristique (la seule
    source fiable est l API, utilisee en priorite quand disponible)."""
    traces = os.path.join(racine, "cerveau-projet", "agents", "traces")
    cibles = [
        os.path.join(traces, "registre-usages-outils.jsonl"),
        os.path.join(traces, "registre-tests.jsonl"),
        os.path.join(traces, "registre-tentatives-bloquees.jsonl"),
        os.path.join(racine, "AGENTS.md"),
        os.path.join(racine, "AGENTS-historique.md"),
    ]
    taille_totale = sum(taille_caracteres(c) for c in cibles)
    envoyes = int(taille_totale / CARACTERES_PAR_TOKEN * 0.6)
    recus = int(taille_totale / CARACTERES_PAR_TOKEN * 0.4)
    return {"envoyes": envoyes, "recus": recus,
            "source": "estimation locale (registres + traces, ~%d octets)"
                      % taille_totale,
            "fiable": False}


def afficher(resultat, session, fenetre_total, verbose=False, no_chrono=False):
    t0 = time.monotonic()
    envoyes = resultat.get("envoyes", 0)
    recus = resultat.get("recus", 0)
    total = envoyes + recus
    encombrement = 100.0 * total / fenetre_total if fenetre_total else 0.0
    fiable = resultat.get("fiable", False)
    source = resultat.get("source", "?")
    print("")
    print(_couleur("=== ANALYSE TOKENS DE LA SESSION %s ===" % session, "bleu"))
    print("Tokens ENVOYES       : %d" % envoyes)
    print("Tokens RECUS         : %d" % recus)
    print("Tokens TOTAL         : %d" % total)
    print("Fenetre de contexte  : %d" % fenetre_total)
    print("ENCOMBREMENT         : %.1f%%" % encombrement)
    if fiable:
        print(_couleur("Source : compteurs API reels", "vert"))
    else:
        print(_couleur("Source : %s (ESTIMATION - la source fiable est l API, "
                       "fournie via TOKENS_SESSION ou metadonnees-session-*.json)"
                       % source, "jaune"))
    if verbose:
        print("Detail : envoyes=%d recus=%d total=%d fenetre=%d"
              % (envoyes, recus, total, fenetre_total))
    if not no_chrono:
        print(_couleur("[chrono] analyser-tokens %.2fs"
                       % (time.monotonic() - t0), "neutre"))
    return {"envoyes": envoyes, "recus": recus, "total": total,
            "encombrement_pct": round(encombrement, 1), "fiable": fiable}


def snapshot(racine, session):
    """Retourne un JSON machine des compteurs CUMULATIFS a l instant T
    (utilise pour la difference par intervention) : API reelle si
    disponible, sinon estimation locale (taille des traces, cumulative).

    Format : {"envoyes": int, "recus": int, "fiable": bool, "source": str}
    La difference entre deux snapshots (debut/fin d intervention) = conso
    de l intervention (meme principe que la duree du chrono)."""
    api = charger_metadonnees_api(racine, session)
    if api:
        return {
            "envoyes": int(api.get("prompt_tokens", 0)),
            "recus": int(api.get("completion_tokens", 0)),
            "fiable": True,
            "source": "api",
        }
    est = estimer_depuis_registres(racine, session)
    return {
        "envoyes": int(est.get("envoyes", 0)),
        "recus": int(est.get("recus", 0)),
        "fiable": False,
        "source": "estimation",
    }


def difference_snapshots(debut, fin):
    """Conso d une intervention = fin - debut (compteurs cumulatifs).
    Retourne {"envoyes", "recus", "fiable"} ou None si un snapshot manque."""
    if not debut or not fin:
        return None
    try:
        env = max(0, int(fin.get("envoyes", 0)) - int(debut.get("envoyes", 0)))
        rec = max(0, int(fin.get("recus", 0)) - int(debut.get("recus", 0)))
    except (TypeError, ValueError):
        return None
    return {"envoyes": env, "recus": rec,
            "fiable": bool(debut.get("fiable")) and bool(fin.get("fiable"))}


def formater_tokens(conso):
    """Formate la conso pour le repere ### : '12.4k env / 8.2k recus'.
    Retourne '' si la conso est nulle ou absente."""
    if not conso:
        return ""
    env = conso.get("envoyes", 0) or 0
    rec = conso.get("recus", 0) or 0
    if env == 0 and rec == 0:
        return ""
    def _k(n):
        if n >= 1000:
            return "%.1fk" % (n / 1000.0)
        return str(n)
    return "tokens: %s env / %s recus" % (_k(env), _k(rec))


def ecrire_rapport(chemin, resultat, session, fenetre_total):
    envoyes = resultat.get("envoyes", 0)
    recus = resultat.get("recus", 0)
    total = envoyes + recus
    encombrement = 100.0 * total / fenetre_total if fenetre_total else 0.0
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Rapport tokens de la session %s\n\n" % session)
        fh.write("- Tokens envoyes : %d\n" % envoyes)
        fh.write("- Tokens recus : %d\n" % recus)
        fh.write("- Tokens total : %d\n" % total)
        fh.write("- Fenetre de contexte : %d\n" % fenetre_total)
        fh.write("- Encombrement : %.1f%%\n" % encombrement)
        fh.write("- Source : %s\n" % resultat.get("source", "?"))
        if not resultat.get("fiable", False):
            fh.write("\n> ESTIMATION : la source fiable est l API (TOKENS_SESSION "
                     "ou metadonnees-session-*.json).\n")


def main():
    parser = argparse.ArgumentParser(
        description="Analyse la consommation de tokens de la session "
                    "(envoyes, recus, encombrement de la fenetre)")
    parser.add_argument("--session", type=str, default="",
                        help="Session analysee (defaut : lue du classeur)")
    parser.add_argument("--fenetre-total", type=int, default=FENETRE_TOTALE_DEFAUT,
                        help="Taille totale de la fenetre (defaut %d)"
                             % FENETRE_TOTALE_DEFAUT)
    parser.add_argument("--rapport", type=str, default="",
                        help="Chemin du rapport markdown (optionnel)")
    parser.add_argument("--verbose", action="store_true",
                        help="Detail des sources")
    parser.add_argument("--dry-run", action="store_true",
                        help="Afficher sans ecrire le rapport")
    parser.add_argument("--no-chrono", action="store_true",
                        help="Couper le chrono de l outil")
    parser.add_argument("--snapshot", action="store_true",
                        help="Mode MACHINE : imprime le JSON cumulatif courant "
                             "{envoyes, recus, fiable, source} sur une ligne "
                             "(difference entre deux snapshots = conso d une "
                             "intervention)")
    parser.add_argument("--version", action="version",
                        version="analyser-tokens v%s" % VERSION)
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    racine = racine_projet()
    session = args.session or session_par_defaut(racine)

    # MODE MACHINE --snapshot : une seule ligne JSON (consommee par
    # activer-agent-principal pour la difference par intervention).
    if args.snapshot:
        sys.stdout.write(json.dumps(snapshot(racine, session),
                                    ensure_ascii=True) + "\n")
        return 0

    # 1. Compteurs API reels (source fiable) si disponibles
    api = charger_metadonnees_api(racine, session)
    if api:
        resultat = {
            "envoyes": int(api.get("prompt_tokens", 0)),
            "recus": int(api.get("completion_tokens", 0)),
            "source": "metadonnees API (prompt_tokens/completion_tokens)",
            "fiable": True,
        }
        fenetre = int(api.get("fenetre_tokens", args.fenetre_total))
    else:
        # 2. Repli : estimation locale depuis les registres
        resultat = estimer_depuis_registres(racine, session, verbose=args.verbose)
        fenetre = args.fenetre_total

    res = afficher(resultat, session, fenetre, verbose=args.verbose,
                   no_chrono=args.no_chrono)
    if args.rapport and not args.dry_run:
        ecrire_rapport(args.rapport, resultat, session, fenetre)
        print(_couleur("[OK] Rapport ecrit : %s" % args.rapport, "vert"))
    elif args.rapport and args.dry_run:
        print(_couleur("[DRY-RUN] Rapport NON ecrit (--dry-run) : %s"
                       % args.rapport, "jaune"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
