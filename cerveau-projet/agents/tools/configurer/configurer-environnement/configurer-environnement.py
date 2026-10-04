#!/usr/bin/env python3
# -*- coding: ascii -*-
# configurer-environnement.py
# Genere et maintient la configuration d environnement adaptative du lanceur
# de non-regression (config-environnement.json) a partir des ressources
# reelles de la machine (CPU, RAM, disque libre, charge).
# Version : 0.1.0
# Statut : prepare

# ============================================================
# OUTIL : CONFIGURER-ENVIRONNEMENT (fondation, demande utilisateur
# 2026-08-17 : configurations adaptables selon le systeme et les
# ressources disponibles).
#
# Pourquoi : le lanceur avait les workers CODES EN DUR
# (min(os.cpu_count(), 16)) - aucune adaptation a la machine reelle.
# Cet outil mesure les ressources et ecrit une config que le lanceur
# lit pour auto-regler workers et timeouts.
#
# Usage :
#   python3 configurer-environnement.py --generer
#   python3 configurer-environnement.py --afficher
#   python3 configurer-environnement.py --reappliquer
#   python3 configurer-environnement.py --version
#
# Options :
#   --generer       Mesure les ressources et ecrit config-environnement.json
#   --afficher      Affiche la config actuelle (ne modifie rien)
#   --reappliquer   Alias de --generer (mesure a nouveau + reecrit)
#   --dry-run       Simule sans ecrire
#   --verbose       Detail du calcul des workers
#   --version       Affiche la version
#   --aide, -h      Afficher cette aide
#
# Contraintes : ASCII strict, LF, stdlib (psutil en dependance douce),
# protections (nommage, doc, dry-run, chrono), messages informationnels.
# ============================================================

import argparse
import datetime
import io
import json
import os
import sys
import time
from pathlib import Path

VERSION = "0.1.0"
STATUT = "prepare"

try:
    import psutil
    PSUTIL = True
except ImportError:
    psutil = None
    PSUTIL = False

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
    return Path(script_path).with_suffix(".md")


def verifier_nommage(script_path):
    chemin = Path(script_path)
    nom_fichier = chemin.stem
    dossier = chemin.parent.name
    prefixe = dossier.split("-")[0] + "-"
    if not nom_fichier.startswith(prefixe):
        print(_couleur(
            "ERREUR: Le nom '%s' ne commence pas par le prefixe du dossier '%s'"
            % (nom_fichier, prefixe), "rouge"), file=sys.stderr)
        sys.exit(1)


def verifier_doc_presente(script_path):
    doc = _doc_chemin(script_path)
    if not doc.is_file():
        print(_couleur("ERREUR: Documentation manquante : %s" % doc, "rouge"),
              file=sys.stderr)
        sys.exit(2)


def trouver_racine():
    base = Path(__file__).resolve()
    for _ in range(8):
        base = base.parent
        if (base / "AGENTS.md").is_file():
            return base
    return Path.cwd()


def chemin_config(racine):
    return racine / "cerveau-projet" / "agents" / "tools" / "tester" / \
        "tester-lancer-non-regression" / "config-environnement.json"


def mesurer_ressources():
    cpu = os.cpu_count() or 1
    ram_totale = -1
    ram_dispo = -1
    charge = -1.0
    if PSUTIL:
        try:
            vm = psutil.virtual_memory()
            ram_totale = int(vm.total // (1024 * 1024))
            ram_dispo = int(vm.available // (1024 * 1024))
            charge = round(float(psutil.cpu_percent(interval=None)), 1)
        except Exception:
            pass
    disque_libre = -1.0
    try:
        import shutil
        usage = shutil.disk_usage(".")
        disque_libre = round(usage.free / (1024 ** 3), 1)
    except Exception:
        pass
    return {
        "cpu_count": cpu,
        "ram_totale_mo": ram_totale,
        "ram_disponible_mo": ram_dispo,
        "disque_libre_go": disque_libre,
        "charge_cpu": charge,
    }


def recommander_workers(cpu_count, ram_dispo_mo):
    """Paliers de workers selon CPU et RAM disponible.

    La memoire disponible est le facteur limitant : si peu de RAM libre, on
    reduit le parallelisme pour eviter le swapping (qui ralentit plus qu il
    n accelere). Bareme :
      - RAM dispo < 2 Go  -> 2 workers max (preserve la RAM)
      - RAM dispo < 8 Go  -> moitie des coeurs (plafonne a 8)
      - sinon             -> min(cpu_count, 16)
    """
    if ram_dispo_mo >= 0 and ram_dispo_mo < 2048:
        return 2
    if ram_dispo_mo >= 0 and ram_dispo_mo < 8192:
        return max(2, min(8, cpu_count // 2))
    return min(cpu_count, 16)


def recommander_timeout(workers):
    """Timeout INTERNE par test : plus de workers = tests plus lents a cause
    de la contention -> timeout plus genereux. Base 120s, +15s par 4 workers."""
    return 120 + 15 * (workers // 4)


def generer(racine, dry_run, verbose):
    res = mesurer_ressources()
    workers = recommander_workers(res["cpu_count"], res["ram_disponible_mo"])
    timeout = recommander_timeout(workers)
    config = {
        "version": "0.1.0",
        "cpu_count": res["cpu_count"],
        "ram_totale_mo": res["ram_totale_mo"],
        "ram_disponible_mo": res["ram_disponible_mo"],
        "disque_libre_go": res["disque_libre_go"],
        "charge_cpu": res["charge_cpu"],
        "workers_recommandes": workers,
        "timeout_test_recommande": timeout,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    if verbose:
        print(_couleur("=== Calcul workers ===", "bleu"))
        print("  cpu_count        : %s" % res["cpu_count"])
        print("  ram_disponible   : %s Mo" % res["ram_disponible_mo"])
        print("  disque libre     : %s Go" % res["disque_libre_go"])
        print("  charge CPU       : %s %%" % res["charge_cpu"])
        print("  -> workers       : %s" % workers)
        print("  -> timeout/test  : %ss" % timeout)
    cible = chemin_config(racine)
    if dry_run:
        print(_couleur("[DRY-RUN] Configuration qui serait ecrite dans %s :" % cible, "jaune"))
        print(json.dumps(config, ensure_ascii=True, indent=1))
        return 0
    with io.open(cible, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(config, fh, ensure_ascii=True, indent=1)
        fh.write("\n")
    print(_couleur("[OK] config-environnement.json ecrit : %s" % cible, "vert"))
    print("  workers_recommandes  : %s" % workers)
    print("  timeout_test         : %ss" % timeout)
    return 0


def afficher(racine):
    cible = chemin_config(racine)
    if not cible.is_file():
        print(_couleur("config-environnement.json absent - lancez --generer.", "jaune"))
        return 1
    data = json.load(io.open(cible, encoding="utf-8"))
    print("=== config-environnement (%s) ===" % cible.name)
    for cle in sorted(data):
        print("  %-22s : %s" % (cle, data[cle]))
    return 0


def afficher_messages_info():
    print("")
    print(_couleur("=== MESSAGES POUR L AGENT ===", "jaune"))
    print("  > config modifiee : le lanceur tester-lancer-non-regression la lit au prochain run")
    print("  > config modifiee : si la machine change (RAM/CPU), relancer --generer")


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="configurer-environnement",
        description="Genere et maintient la configuration d environnement adaptative (workers, timeouts) du lanceur de non-regression.",
        epilog="Version %s (Statut : %s)" % (VERSION, STATUT),
    )
    parser.add_argument("--generer", action="store_true", help="Mesure les ressources et ecrit config-environnement.json")
    parser.add_argument("--afficher", action="store_true", help="Affiche la config actuelle (ne modifie rien)")
    parser.add_argument("--reappliquer", action="store_true", help="Alias de --generer (mesure a nouveau + reecrit)")
    parser.add_argument("--dry-run", action="store_true", help="Simuler sans ecrire")
    parser.add_argument("--verbose", action="store_true", help="Detail du calcul des workers")
    parser.add_argument("--version", action="version", version="configurer-environnement v%s" % VERSION)
    parser.add_argument("--aide", action="help", help="Afficher cette aide (alias de -h)")
    return parser


def main(argv=None):
    verifier_nommage(sys.argv[0])
    verifier_doc_presente(sys.argv[0])
    parser = construire_parser()
    args = parser.parse_args(argv)
    racine = trouver_racine()
    t0 = time.monotonic()

    if args.afficher:
        code = afficher(racine)
        return code

    if args.generer or args.reappliquer:
        code = generer(racine, args.dry_run, args.verbose)
        if not args.dry_run:
            afficher_messages_info()
        print(_couleur("=== Temps ecoule : %.2f s ===" % (time.monotonic() - t0), "bleu"))
        return code

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
