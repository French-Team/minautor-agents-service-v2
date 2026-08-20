#!/usr/bin/env python3
# -*- coding: ascii -*-
# evaluer-progression.py
# Evalue la progression du cerveau-projet EN TEMPS REEL et son EVOLUTION :
#   1. PROGRESSION : un ensemble de CRITERES DEFINISSABLES (fichier JSON) qui
#      mesurent la progression jusqu a 100%. Chaque critere lit une source de
#      verite reelle (catalogue, lecons.db, registre-tests, chronos, agents).
#   2. AUTO-AMELIORATION : score en % de la vitesse d amelioration entre deux
#      fenetres de temps (recente vs precedente). NON PLAFONNE : une croissance
#      qui s accelere peut devenir exponentielle (score > 100%).
# Usage :
#   python3 evaluer-progression.py
#   python3 evaluer-progression.py --criteres mon-fichier.json
#   python3 evaluer-progression.py --rapport rapport.md --verbose
# Version : 0.1.0
# Statut : ebauche
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (evaluer-).
# =============================================================================

import argparse
import io
import json
import os
import sqlite3
import sys
import time

VERSION = "0.1.0"
STATUT = "ebauche"

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[1;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    if not sys.stdout.isatty():
        return texte
    return _COULEURS.get(nom, "") + texte + _COULEURS["neutre"]


def _doc_chemin(script_path):
    return os.path.splitext(script_path)[0] + ".md"


def verifier_doc_presente(script_path):
    from pathlib import Path
    doc = Path(_doc_chemin(script_path))
    if not doc.is_file():
        print(_couleur("ERREUR: Documentation manquante : %s" % doc, "rouge"),
              file=sys.stderr)
        print("  Le .md de l outil est OBLIGATOIRE (regle immuable, protocole-outils).",
              file=sys.stderr)
        sys.exit(2)


def afficher_section_utilisation(doc):
    from pathlib import Path
    try:
        texte = Path(doc).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        print("[INFO] Impossible de lire le .md pour afficher la section Utilisation")
        return
    dans_usage = False
    for ligne in texte.splitlines():
        if ligne.strip().startswith("## "):
            dans_usage = ligne.strip().lower().startswith("## utilisation")
            continue
        if dans_usage and ligne.strip():
            print("  " + ligne.rstrip())


def exiger_confirmation_doc(script_path, dry_run, confirme_doc):
    if dry_run or confirme_doc:
        return
    doc = _doc_chemin(script_path)
    verifier_doc_presente(script_path)
    print(_couleur("=== DOCUMENTATION OBLIGATOIRE ===", "jaune"))
    print("  Cet outil exige la lecture de sa documentation avant usage reel.")
    print("  Section Utilisation de %s :" % os.path.basename(doc))
    print("")
    afficher_section_utilisation(doc)
    print("")
    print(_couleur("REFUS: relancez avec --confirme-doc apres lecture de la doc.",
                   "rouge"), file=sys.stderr)
    sys.exit(2)


def afficher_messages_info(messages):
    if not messages:
        return
    print("")
    print(_couleur("=== MESSAGES POUR L AGENT ===", "jaune"))
    for m in messages:
        print("  > %s" % m)


def verifier_nommage(script_path):
    from pathlib import Path
    chemin = Path(script_path)
    nom_fichier = chemin.stem
    if nom_fichier == "outil-template":
        return
    dossier = chemin.parent.name
    prefixe = dossier.split("-")[0] + "-"
    if not nom_fichier.startswith(prefixe):
        print(_couleur(
            "ERREUR: Le nom '%s' ne commence pas par le prefixe du dossier '%s'"
            % (nom_fichier, prefixe), "rouge"), file=sys.stderr)
        sys.exit(1)


def afficher_aide(parser):
    print("=== evaluer-progression v%s ===" % VERSION)
    print("")
    parser.print_help()


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="evaluer-progression",
        description="Evalue la progression du cerveau-projet en temps reel "
                    "(criteres definissables jusqu a 100%) et l auto-amelioration "
                    "(score en % non plafonne, croissance exponentielle permise).",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("--criteres", type=str, default="",
                        help="Chemin d un fichier de criteres JSON (defaut : "
                             "progression-criteres.json a cote de l outil)")
    parser.add_argument("--rapport", type=str, default="",
                        help="Chemin absolu d un rapport markdown a ecrire "
                             "(par defaut : affichage seul, RIEN n est ecrit)")
    parser.add_argument("--verbose", action="store_true",
                        help="Afficher les details (sources, calculs)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simuler sans ecrire le rapport")
    parser.add_argument("--version", action="version",
                        version="evaluer-progression v%s" % VERSION)
    parser.add_argument("--chrono", action="store_true",
                        help="Mesurer la duree d execution (bilan en fin)")
    parser.add_argument("--doc", action="store_true",
                        help="Afficher le .md de documentation complet et sortir")
    parser.add_argument("--confirme-doc", action="store_true",
                        help="Confirmer la lecture de la documentation "
                             "(requis en mode reel)")
    return parser


# ---------------------------------------------------------------------------
# Sources de verite (lecture seule)
# ---------------------------------------------------------------------------

def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def defaut_criteres():
    d = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(d, "progression-criteres.json")


def charger_criteres(chemin):
    p = chemin or defaut_criteres()
    if not os.path.isfile(p):
        raise SystemExit("ERREUR: fichier de criteres introuvable : %s" % p)
    with io.open(p, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data.get("criteres"), list) or not data["criteres"]:
        raise SystemExit("ERREUR: le fichier de criteres doit avoir une liste "
                         "'criteres' non vide")
    return data


def lire_jsonl(chemin):
    entrees = []
    if not os.path.isfile(chemin):
        return entrees
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                entrees.append(json.loads(ligne))
            except ValueError:
                continue
    return entrees


def compter_catalogue(racine):
    chemin = os.path.join(racine, "cerveau-projet", "agents", "tools",
                          "generateurs", "generateurs-commande",
                          "catalogue-commandes.json")
    if not os.path.isfile(chemin):
        return 0
    with io.open(chemin, encoding="utf-8") as fh:
        data = json.load(fh)
    return len(data.get("commandes", []))


def compter_lecons(racine):
    chemin = os.path.join(racine, "cerveau-projet", "agents", "lecons",
                          "lecons.db")
    if not os.path.isfile(chemin):
        return 0
    try:
        conn = sqlite3.connect(chemin)
        cur = conn.execute("SELECT COUNT(*) FROM lecons")
        n = cur.fetchone()[0]
        conn.close()
        return n
    except sqlite3.Error:
        return 0


def pourcentage_tests_ok(racine):
    chemin = os.path.join(racine, "cerveau-projet", "agents", "traces",
                          "registre-tests.jsonl")
    entrees = lire_jsonl(chemin)
    if not entrees:
        return 0.0
    runs = {}
    for e in entrees:
        rid = e.get("run_id")
        if rid:
            runs.setdefault(rid, []).append(e)
    if not runs:
        return 0.0
    dernier_run = max(runs.keys())
    ent = runs[dernier_run]
    if not ent:
        return 0.0
    ok = sum(1 for e in ent if e.get("verdict") == "OK")
    return round(100.0 * ok / len(ent), 1)


def compter_missions_terminees(racine):
    chemin = os.path.join(racine, "cerveau-projet", "agents", "traces",
                          "chronos.jsonl")
    entrees = lire_jsonl(chemin)
    return sum(1 for e in entrees if e.get("date_fin"))


def compter_agents(racine):
    dossier = os.path.join(racine, "cerveau-projet", "agents")
    if not os.path.isdir(dossier):
        return 0
    total = 0
    for nom in os.listdir(dossier):
        sous = os.path.join(dossier, nom)
        fiche = os.path.join(sous, nom + ".md")
        if not os.path.isdir(sous) or not os.path.isfile(fiche):
            continue
        try:
            with io.open(fiche, encoding="utf-8") as fh:
                entete = fh.read(400)
        except (OSError, UnicodeError):
            continue
        if "type: fiche-agent" in entete or "type: fiche" in entete:
            total += 1
    return total


def valeur_critere(source, racine, verbose=False):
    if source == "catalogue":
        val = compter_catalogue(racine)
    elif source == "lecons":
        val = compter_lecons(racine)
    elif source == "tests_ok":
        val = pourcentage_tests_ok(racine)
    elif source == "missions":
        val = compter_missions_terminees(racine)
    elif source == "agents":
        val = compter_agents(racine)
    else:
        raise SystemExit("ERREUR: source de critere inconnue : %s" % source)
    if verbose:
        print("  [source %s] valeur reelle = %s" % (source, val))
    return val


# ---------------------------------------------------------------------------
# Auto-amelioration : vitesse entre deux fenetres (non plafonnee)
# ---------------------------------------------------------------------------

def dates_depuis(source, racine):
    """Retourne la liste des dates (YYYY-MM-DD) des evenements de la source."""
    if source == "usages_par_jour":
        chemin = os.path.join(racine, "cerveau-projet", "agents", "traces",
                              "registre-usages-outils.jsonl")
        vals = [e.get("date") for e in lire_jsonl(chemin)]
    elif source == "lecons_par_jour":
        vals = []
        chemin = os.path.join(racine, "cerveau-projet", "agents", "lecons",
                              "lecons.db")
        if os.path.isfile(chemin):
            try:
                conn = sqlite3.connect(chemin)
                for row in conn.execute("SELECT date FROM lecons"):
                    vals.append(row[0])
                conn.close()
            except sqlite3.Error:
                pass
    elif source == "tests_par_jour":
        chemin = os.path.join(racine, "cerveau-projet", "agents", "traces",
                              "registre-tests.jsonl")
        vals = [e.get("date") for e in lire_jsonl(chemin)]
    else:
        raise SystemExit("ERREUR: source d indicateur inconnue : %s" % source)
    dates = []
    for v in vals:
        if v and len(v) >= 10 and v[4] == "-" and v[7] == "-":
            dates.append(v[:10])
    return dates


def taux_par_jour(dates, debut, fin):
    """Nombre d evenements entre debut et fin (j inclus), ramene a 1 jour."""
    import datetime
    if debut > fin:
        return 0.0
    nb = sum(1 for d in dates if debut <= d <= fin)

    def _parse(m):
        return datetime.date(int(m[:4]), int(m[5:7]), int(m[8:10]))
    jours = max(1, (_parse(fin) - _parse(debut)).days + 1)
    return nb / jours


def fenetres_recente_et_precedente(aujourdhui, fenetre_jours):
    def _decale(j, n):
        import datetime
        d = datetime.date(int(j[:4]), int(j[5:7]), int(j[8:10]))
        d = d - datetime.timedelta(days=n)
        return "%04d-%02d-%02d" % (d.year, d.month, d.day)
    fin_recente = aujourdhui
    debut_recente = _decale(aujourdhui, fenetre_jours - 1)
    fin_prec = _decale(debut_recente, 1)
    debut_prec = _decale(fin_prec, fenetre_jours - 1)
    return (debut_recente, fin_recente), (debut_prec, fin_prec)


def score_amelioration_source(dates, fenetres):
    ((dr, fr), (dp, fp)) = fenetres
    t_recent = taux_par_jour(dates, dr, fr)
    t_prec = taux_par_jour(dates, dp, fp)
    if t_prec <= 0:
        return (100.0 if t_recent <= 0 else 100.0 + 100.0 * t_recent), t_prec, t_recent
    return (100.0 * t_recent / t_prec), t_prec, t_recent


def calculer_auto_amelioration(data, racine, fenetre_jours, verbose=False):
    """Score global pondere (NON PLAFONNE) + detail par indicateur."""
    import datetime
    indicateurs = data.get("auto_amelioration", {}).get("indicateurs", [])
    aujourdhui = datetime.date.today().strftime("%Y-%m-%d")
    fenetres = fenetres_recente_et_precedente(aujourdhui, fenetre_jours)
    scores = []
    total_poids = 0.0
    detail = []
    for ind in indicateurs:
        dates = dates_depuis(ind["source"], racine)
        score, t_prec, t_recent = score_amelioration_source(dates, fenetres)
        poids = float(ind.get("poids", 1))
        total_poids += poids
        scores.append(score * poids)
        detail.append({
            "id": ind["id"],
            "nom": ind.get("nom", ind["id"]),
            "taux_precedent": round(t_prec, 3),
            "taux_recent": round(t_recent, 3),
            "score": round(score, 1),
            "poids": poids,
        })
        if verbose:
            print("  [amelioration %s] precedent=%.3f/j recent=%.3f/j "
                  "score=%.1f%%" % (ind["id"], t_prec, t_recent, score))
    if total_poids <= 0:
        return 0.0, detail
    score_pondere = sum(scores) / total_poids
    return score_pondere, detail


# ---------------------------------------------------------------------------
# Rapport et main
# ---------------------------------------------------------------------------

def ecrire_rapport(chemin, lignes):
    dossier = os.path.dirname(os.path.abspath(chemin))
    if not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lignes) + "\n")


def main():
    from pathlib import Path
    verifier_nommage(sys.argv[0])
    verifier_doc_presente(sys.argv[0])

    parser = construire_parser()
    args = parser.parse_args()

    if getattr(args, "doc", False):
        doc = Path(_doc_chemin(sys.argv[0]))
        print(doc.read_text(encoding="utf-8"))
        return 0

    exiger_confirmation_doc(sys.argv[0], getattr(args, "dry_run", False),
                            getattr(args, "confirme_doc", False))

    t0 = time.monotonic()
    racine = racine_projet()
    data = charger_criteres(args.criteres)
    fenetre_jours = int(data.get("auto_amelioration", {}).get("fenetre_jours", 7) or 7)

    import datetime
    horodatage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lignes_rapport = [
        "# Rapport evaluer-progression",
        "",
        "**Version outil** : %s" % VERSION,
        "**Date** : %s" % horodatage,
        "",
        "**Objectif** : %s" % data.get("objectif", ""),
        "",
        "## 1. Progression (criteres jusqu a 100%)",
        "",
        "| Critere | Valeur | Cible | Progression | Poids |",
        "|---|---|---|---|---|",
    ]

    print("=== evaluer-progression v%s ===" % VERSION)
    print("Objectif : %s" % data.get("objectif", ""))
    print("")
    print(_couleur("PROGRESSION :", "bleu"))
    print("%s %s %s %s %s" % (
        "Critere".ljust(28), "Valeur".rjust(9), "Cible".rjust(7),
        "Prog %".rjust(9), "Poids".rjust(6)))
    somme_poids = 0.0
    progression_globale = 0.0
    for crit in data["criteres"]:
        valeur = valeur_critere(crit["source"], racine, args.verbose)
        cible = float(crit.get("cible", 100))
        poids = float(crit.get("poids", 1))
        prog = min(100.0, 100.0 * valeur / cible) if cible else 0.0
        somme_poids += poids
        progression_globale += poids * prog
        print(crit["id"].ljust(28) + str(valeur).rjust(9)
              + str(int(cible)).rjust(7) + ("%.1f" % prog).rjust(9)
              + str(int(poids)).rjust(6))
        lignes_rapport.append("| %s | %s | %s | %.1f%% | %s |" % (
            crit["id"], valeur, int(cible), prog, int(poids)))
    if somme_poids > 0:
        progression_globale = progression_globale / somme_poids
    print("")
    print(_couleur("PROGRESSION GLOBALE : %.1f %%" % progression_globale, "vert"))
    lignes_rapport.append("")
    lignes_rapport.append("**Progression globale : %.1f%%**" % progression_globale)

    # 2. AUTO-AMELIORATION (score % non plafonne)
    print("")
    print(_couleur("AUTO-AMELIORATION (score % non plafonne) :", "bleu"))
    print("Fenetre : les derniers %d jours vs les %d jours precedents" % (
        fenetre_jours, fenetre_jours))
    lignes_rapport.append("")
    lignes_rapport.append("## 2. Auto-amelioration (score % non plafonne)")
    lignes_rapport.append("")
    lignes_rapport.append("Fenetre : derniers %d jours vs %d precedents." % (
        fenetre_jours, fenetre_jours))
    lignes_rapport.append("")
    lignes_rapport.append("| Indicateur | Taux precedent (/j) | Taux recent (/j) | Score % |")
    lignes_rapport.append("|---|---|---|---|")

    score_auto, detail = calculer_auto_amelioration(
        data, racine, fenetre_jours, args.verbose)
    for d in detail:
        print(d["nom"].ljust(28)
              + ("%.3f" % d["taux_precedent"]).rjust(20)
              + ("%.3f" % d["taux_recent"]).rjust(16)
              + ("%.1f%%" % d["score"]).rjust(12))
        lignes_rapport.append("| %s | %.3f | %.3f | %.1f%% |" % (
            d["id"], d["taux_precedent"], d["taux_recent"], d["score"]))
    print("")
    print(_couleur("SCORE AUTO-AMELIORATION : %.1f %%" % score_auto, "vert"))
    print("  (score NON PLAFONNE : une croissance acceleree peut depasser 100%)")
    lignes_rapport.append("")
    lignes_rapport.append("**Score auto-amelioration : %.1f%% (non plafonne)**" % score_auto)

    messages = []
    if args.rapport and not args.dry_run:
        ecrire_rapport(args.rapport, lignes_rapport)
        print("")
        print("Rapport ecrit : %s" % args.rapport)
        messages.append("rapport ecrit : referencer le fichier s il est dans le projet")
    elif args.rapport and args.dry_run:
        print("[DRY-RUN] rapport non ecrit (--dry-run) : %s" % args.rapport)

    if args.dry_run:
        print("[DRY-RUN] aucun changement applique")

    messages.append("criteres definissables : --criteres <fichier> (etendre/adapter les cibles)")
    messages.append("source de ce rapport : registres en temps reel, lecture seule")

    if args.chrono:
        print("")
        print("[chrono] evaluer-progression : %.2fs" % (time.monotonic() - t0))
    if messages and not args.dry_run:
        afficher_messages_info(messages)
    return 0


if __name__ == "__main__":
    sys.exit(main())