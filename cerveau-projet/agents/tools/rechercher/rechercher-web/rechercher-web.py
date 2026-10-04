#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
rechercher-web.py

Rechercher sur le web et/ou lire une page web (acces web reel pour les
agents du cerveau - demande utilisateur 2026-08-16 : souvenirs vrais et
d actualite, la memoire factuelle des agents est recherches-web/).

Deux modes :
  1. RECHERCHE  : rechercher-web.py --agent <nom> "<requete>"
                  (moteur HTML simple, ex DuckDuckGo Lite) -> titres + URLs
  2. LECTURE    : rechercher-web.py --agent <nom> --url <url>
                  (lecture d une page, extraction du texte lisible)

Options:
  --agent <nom>      OBLIGATOIRE (verrou d habilitation : l outil doit
                     etre dans la carte de l agent)
  --url <url>        Lire une page web (mode lecture)
  --max <n>          Nombre max de resultats (defaut 8)
  --rapport <fich>   Ecrire un rapport markdown
  --verbose          Afficher les details (requetes, durees)
  --version          Afficher la version
  --aide             Afficher cette aide (alias de -h)
  --chrono           Afficher le chrono (defaut actif)

Protections : verrou d habilitation, triplet chrono (template v0.3.0),
timeout reseau interne (jamais de timeout exterieur), ASCII strict + LF.
Le verrou journalise l usage dans registre-usages-outils.jsonl
(verrou-auto) : l agent n a rien a declarer.

Proprietaire : Atlas (explorateur - recherche web)
Version : 0.1.0
Statut : ebauche
"""

import argparse
import html
import io
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

VERSION = "0.1.0"
STATUT = "ebauche"

# --- triplet chrono (template v0.3.0) ---
T_START = time.monotonic()
CHRONO_ACTIF = True
ETAPES = []

_COULEURS = {
    "rouge": "\033[0;31m", "vert": "\033[0;32m", "jaune": "\033[1;33m",
    "bleu": "\033[0;34m", "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    return "%s%s%s" % (_COULEURS.get(nom, _COULEURS["neutre"]), texte,
                       _COULEURS["neutre"])


def _affichable(texte):
    """Sanitise le contenu WEB pour la console : le web contient n importe
    quel caractere Unicode (ex U+2318) qui casse l encodage du terminal.
    Remplace tout caractere hors ASCII par '?' (regle ASCII du projet)."""
    return texte.encode("ascii", "replace").decode("ascii")


def chrono_etape(nom, t_debut):
    ETAPES.append((nom, time.monotonic() - t_debut))


def bilan_chrono():
    if not CHRONO_ACTIF:
        return
    total = time.monotonic() - T_START
    print("")
    print("=== CHRONO rechercher-web (total %.1fs) ===" % total)
    for nom, duree in ETAPES:
        print("  [chrono] %-30s %.2fs" % (nom, duree))


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def verrouiller_habilitation(agent):
    """Verrou d habilitation : seul un agent dont la carte contient
    rechercher-web peut l utiliser. Code 0 = OK, 1 = bloque, 2 = erreur."""
    racine = racine_projet()
    verrou = os.path.join(
        racine, "cerveau-projet", "agents", "tools", "proteger",
        "proteger-verrou-habilitation", "proteger-verrou-habilitation.py")
    if not os.path.isfile(verrou):
        return 2, "[ERREUR] Verrou introuvable : %s" % verrou
    r = subprocess.run(
        [sys.executable, verrou, "--agent", agent, "--outil", "rechercher-web"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout + r.stderr).strip()


def _requete_http(url, timeout=20):
    """Requete HTTP simple (stdlib). Retourne (statut, texte). Timeout
    INTERNE (protection) - jamais de timeout exterieur."""
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (compatible; cerveau-projet/1.0)"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        statut = r.getcode()
        brut = r.read()
    for enc in ("utf-8", "latin-1"):
        try:
            return statut, brut.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return statut, brut.decode("utf-8", errors="replace")


def rechercher(requete, max_resultats=8, verbose=False):
    """Recherche web via DuckDuckGo Lite (HTML simple, sans JS).
    Retourne une liste de dicts {titre, url, extrait}."""
    url = "https://lite.duckduckgo.com/lite/?q=" + urllib.parse.quote(requete)
    if verbose:
        print(_couleur("[recherche] %s" % url, "bleu"))
    statut, texte = _requete_http(url)
    resultats = []
    # structure lite : <a ... class='result-link' href="//duckduckgo.com/l/?uddg=<encode>&rut=...">
    # (guillemets SIMPLES cote class, href avant ou apres) + <td class='result-snippet'>
    anchors = re.finditer(
        r"<a(?P<avant>[^>]*?)class=['\"]result-link['\"](?P<apres>[^>]*)>"
        r"(?P<titre>.*?)</a>",
        texte, re.S)
    snippets = re.findall(
        r"<td[^>]*class=['\"]result-snippet['\"][^>]*>(.*?)</td>", texte, re.S)
    resultats = []
    vus = set()
    for i, m_a in enumerate(anchors):
        attrs = m_a.group("avant") + m_a.group("apres")
        m_href = re.search(r'href="([^"]+)"', attrs)
        if not m_href:
            continue
        # dechiffre l URL reelle (redirect DuckDuckGo : uddg=<encode>)
        real = m_href.group(1)
        m_uddg = re.search(r"uddg=([^&]+)", real)
        if m_uddg:
            real = urllib.parse.unquote(m_uddg.group(1))
        if not real.startswith("http"):
            continue
        titre_propre = re.sub(r"<[^>]+>", "", m_a.group("titre"))
        titre_propre = html.unescape(titre_propre).strip()
        if not titre_propre or titre_propre in vus:
            continue
        vus.add(titre_propre)
        extrait = ""
        if i < len(snippets):
            extrait = re.sub(r"<[^>]+>", " ", snippets[i])
            extrait = html.unescape(extrait).strip()
        resultats.append({"titre": titre_propre, "url": real,
                          "extrait": extrait[:220]})
        if len(resultats) >= max_resultats:
            break
    return resultats


def lire_page(url, verbose=False):
    """Lit une page web et extrait (titre, texte lisible)."""
    if verbose:
        print(_couleur("[lecture] %s" % url, "bleu"))
    statut, texte = _requete_http(url)
    m = re.search(r"<title[^>]*>(.*?)</title>", texte, re.S | re.I)
    titre = html.unescape(m.group(1)).strip() if m else "(sans titre)"
    corps = re.sub(r"<script[^>]*>.*?</script>", " ", texte, flags=re.S | re.I)
    corps = re.sub(r"<style[^>]*>.*?</style>", " ", corps, flags=re.S | re.I)
    corps = re.sub(r"<[^>]+>", " ", corps)
    corps = html.unescape(corps)
    corps = re.sub(r"\s+", " ", corps).strip()
    return {"titre": titre, "statut": statut, "texte": corps[:8000]}


def main():
    parser = argparse.ArgumentParser(
        prog="rechercher-web",
        description="Recherche web et lecture de page pour les agents du cerveau.")
    parser.add_argument("requete", nargs="?", default="",
                        help="Requete de recherche (mode recherche)")
    parser.add_argument("--agent", default="", help="Agent appelant (OBLIGATOIRE)")
    parser.add_argument("--url", default="", help="URL a lire (mode lecture)")
    parser.add_argument("--max", type=int, default=8, help="Max resultats (defaut 8)")
    parser.add_argument("--rapport", default="", help="Fichier rapport markdown")
    parser.add_argument("--verbose", action="store_true", help="Details")
    parser.add_argument("--chrono", action="store_true", help="Chrono (defaut actif)")
    parser.add_argument("--version", action="version",
                        version="rechercher-web %s (%s)" % (VERSION, STATUT))
    parser.add_argument("--aide", action="help", help="Afficher cette aide")
    args = parser.parse_args()

    t0 = time.monotonic()
    if not args.agent:
        print(_couleur("[ERREUR] --agent est OBLIGATOIRE (verrou d habilitation).",
                       "rouge"))
        return 2
    code, message = verrouiller_habilitation(args.agent)
    if code != 0:
        print(_couleur(message, "rouge"))
        return 1 if code == 1 else 2
    chrono_etape("verrou habilitation", t0)

    if not args.url and not args.requete:
        print(_couleur("[ERREUR] Fournir une <requete> ou --url <url>.", "rouge"))
        return 2

    lignes_rapport = []
    if args.url:
        t1 = time.monotonic()
        page = lire_page(args.url, args.verbose)
        chrono_etape("lecture page", t1)
        print("")
        print(_couleur("=== PAGE : %s (statut %s) ===" % (_affichable(page["titre"]),
                                                          page["statut"]), "bleu"))
        print(_affichable(page["texte"][:3000]))
        lignes_rapport.append("## Page lue : %s" % _affichable(page["titre"]))
        lignes_rapport.append("- URL : %s" % _affichable(args.url))
        lignes_rapport.append("- Statut : %s" % page["statut"])
        lignes_rapport.append("")
        lignes_rapport.append(_affichable(page["texte"][:6000]))
    else:
        t1 = time.monotonic()
        resultats = rechercher(args.requete, args.max, args.verbose)
        chrono_etape("recherche web", t1)
        print("")
        print(_couleur("=== RECHERCHE : %s (%d resultats) ==="
                       % (args.requete, len(resultats)), "bleu"))
        for i, r in enumerate(resultats, 1):
            print("")
            print("%d. %s" % (i, _affichable(r["titre"])))
            print("   %s" % _affichable(r["url"]))
            if r["extrait"]:
                print("   %s" % _affichable(r["extrait"]))
        lignes_rapport.append("## Recherche : %s" % args.requete)
        for r in resultats:
            lignes_rapport.append("")
            lignes_rapport.append("- **%s**" % _affichable(r["titre"]))
            lignes_rapport.append("  - %s" % _affichable(r["url"]))
            if r["extrait"]:
                lignes_rapport.append("  - %s" % _affichable(r["extrait"]))

    if args.rapport:
        with io.open(args.rapport, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("# Rapport rechercher-web\n\n")
            fh.write("- Date : %s\n" % time.strftime("%Y-%m-%d %H:%M:%S"))
            fh.write("- Agent : %s\n" % args.agent)
            fh.write("- Outil : rechercher-web v%s\n\n" % VERSION)
            fh.write("\n".join(lignes_rapport))
            fh.write("\n")
        print(_couleur("[rapport] %s" % args.rapport, "jaune"))

    bilan_chrono()
    return 0


if __name__ == "__main__":
    sys.exit(main())
