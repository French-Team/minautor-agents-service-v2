#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
convertir-carte-mermaid.py

Convertit les cartes de decision des agents (parcours-<agent>.json, source
de verite) en graphes Mermaid (.mmd) ET en images SVG par agent, dans le
dossier versionne cerveau-projet/cartes-vues/mermaid/ (toujours DANS
cerveau-projet).

Regles de rendu (.mmd) :
  - case_depart -> noeud START (stadium)
  - case avec branches non vides (question, controle, action a choix)
    -> losange, chaque branche devient une arete etiquetee par la reponse
  - case avec 'suivant' (action, controle, indice) -> rectangle
  - case 'suivant: null' (reactiver l appelant) -> arete vers FIN-APPELANT
  - case type 'fin' -> double cercle, terminaison du graphe

Regles de rendu (.svg) :
  - rendu 100% local en Python pur (aucune dependance externe) et
    DETERMINISTE : meme carte -> memes octets, ce qui permet au garde-fou
    de verifier la synchronisation octet a octet
  - mise en page par etages : rang = chemin le plus long depuis START,
    ordre d apparition stable dans le rang, rangs centres
  - aretes : droite (rang suivant), coudee (plusieurs rangs), courbe
    (retour en arriere), arc (boucle sur soi-meme), etiquette sur fond blanc
  - couleurs : rectangle = action, losange = decision, stadium = START/fin,
    rose = FIN-APPELANT (retour a l appelant)

Usage:
  python3 convertir-carte-mermaid.py --agent <nom>
  python3 convertir-carte-mermaid.py --agent <nom> --svg
  python3 convertir-carte-mermaid.py --tous [--sortie <dossier>]
  python3 convertir-carte-mermaid.py --verifier
  python3 convertir-carte-mermaid.py --version | --aide

Options:
  --agent <nom>    Convertir la carte d un seul agent (.mmd)
  --svg            Ajouter le rendu SVG (avec --agent)
  --tous           Toutes les cartes : .mmd + .svg + index.md
  --sortie <d>     Dossier de sortie (defaut: cerveau-projet/cartes-vues/mermaid)
  --verifier       Verifier la synchronisation cartes <-> .mmd <-> .svg (rc=0 si OK)
  --version        Affiche la version
  --aide           Affiche cette aide

Version : 0.2.1
"""
import argparse
import glob
import io
import json
import os
import re
import sys

VERSION = "0.2.1"
STATUT = "prepare"

GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
NC = "\033[0m"

# ---------------------------------------------------------------------------
# Constantes du rendu SVG (deterministes)
# ---------------------------------------------------------------------------
FONTE = "Arial, Helvetica, sans-serif"
TAILLE_TEXTE = 11.5
TAILLE_ETIQUETTE = 10.5
COULEUR_FOND = "#ffffff"
COULEUR_TEXTE = "#0f172a"
COULEUR_ARETE = "#64748b"
COULEUR_ETIQUETTE = "#1e293b"
FORME_RECT = {"fond": "#f8fafc", "bord": "#334155"}
FORME_LOSANGE = {"fond": "#fef3c7", "bord": "#b45309"}
FORME_STADIUM = {"fond": "#e0f2fe", "bord": "#1d4ed8"}
FORME_APPELANT = {"fond": "#fce7f3", "bord": "#be185d"}


def racine_projet():
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def lister_parcours(racine):
    motif = os.path.join(racine, "cerveau-projet", "agents", "*",
                         "parcours", "parcours-*.json")
    return sorted(glob.glob(motif))


def charger_parcours(chemin):
    with io.open(chemin, encoding="utf-8") as fh:
        return json.load(fh)


def agent_du_parcours(donnees):
    ident = donnees.get("identite", {})
    return ident.get("appartient_a", ident.get("agent", "?"))


def nom_fichier_parcours(chemin, donnees):
    """Nom de sortie unique par parcours (source de verite : fichier).

    Parcours principal : parcours-<agent>.json -> <agent>. Les sous-parcours
    (ex: parcours-revision-audit.json de socrate) sont prefixes par l agent
    pour eviter les collisions : <agent>-<sous>.
    """
    base = os.path.basename(chemin)
    stem = base.replace("parcours-", "").replace(".json", "")
    agent = agent_du_parcours(donnees)
    if stem == agent:
        return agent
    return "%s-%s" % (agent, stem)


def echapper(texte):
    """Echappe un titre pour un libelle mermaid (entre guillemets)."""
    t = (texte or "").replace("\\", "\\\\").replace('"', '\\"')
    t = t.replace("\n", " ").replace("\r", " ").strip()
    return t


def convertir(donnees):
    """Convertit un parcours en texte mermaid. Retourne (texte, avertissements)."""
    parcours = donnees.get("parcours", {})
    cases = donnees.get("cases", {})
    depart = parcours.get("case_depart", "c0")
    avertissements = []

    lignes = []
    lignes.append("flowchart TD")
    lignes.append('    START(["Debut"]) --> %s' % depart)

    # Declarer d'abord tous les noeuds (pour un ordre stable)
    for cid in sorted(cases.keys()):
        c = cases[cid]
        titre = echapper(c.get("titre", cid))
        if c.get("branches"):
            lignes.append('    %s{"%s"}' % (cid, titre))
        elif c.get("type") == "fin":
            lignes.append('    %s(["%s"])' % (cid, titre))
        else:
            lignes.append('    %s["%s"]' % (cid, titre))

    # Puis les aretes
    for cid in sorted(cases.keys()):
        c = cases[cid]
        if c.get("branches"):
            for b in c.get("branches", []):
                vers = b.get("vers")
                reponse = echapper(b.get("reponse", "?"))
                if vers:
                    lignes.append('    %s -- "%s" --> %s' % (cid, reponse, vers))
                else:
                    lignes.append('    %s -- "%s" --> FIN-APPELANT' % (cid, reponse))
                    avertissements.append("%s: branche sans vers -> FIN-APPELANT" % cid)
        elif "suivant" in c:
            suiv = c.get("suivant")
            if suiv:
                if suiv not in cases:
                    avertissements.append("%s: cible inconnue '%s'" % (cid, suiv))
                lignes.append("    %s --> %s" % (cid, suiv))
            else:
                lignes.append("    %s --> FIN-APPELANT" % cid)
                avertissements.append("%s: suivant null (reactiver appelant)" % cid)
        elif c.get("type") == "fin":
            pass  # terminaison
        else:
            avertissements.append("%s: ni suivant ni branches ni fin" % cid)

    # Cases injoignables depuis le depart (propagation BFS sur suivant + branches)
    atteintes = set([depart])
    a_explorer = [depart]
    while a_explorer:
        cid = a_explorer.pop()
        c = cases.get(cid, {})
        if c.get("branches"):
            for b in c.get("branches", []):
                v = b.get("vers")
                if v and v not in atteintes:
                    atteintes.add(v)
                    a_explorer.append(v)
        elif "suivant" in c and c.get("suivant"):
            v = c["suivant"]
            if v not in atteintes:
                atteintes.add(v)
                a_explorer.append(v)
    orphelines = sorted(set(cases.keys()) - atteintes)
    if orphelines:
        avertissements.append("cases injoignables: %s" % ", ".join(orphelines))

    entete = "%%%% Carte de decision de %s (parcours v%s)" % (
        agent_du_parcours(donnees), parcours.get("version", "?"))
    return entete + "\n" + "\n".join(lignes) + "\n", avertissements


def verifier_syntaxe(texte, cases):
    """Valide structurellement le texte mermaid genere (pas de regex fragile).

    Verifie : premiere ligne 'flowchart TD', chaque balise est un id de case
    connu (ou START/FIN-APPELANT), chaque arete pointe vers un id connu.
    """
    erreurs = []
    lignes = texte.splitlines()
    # ignorer les commentaires %% en tete, puis header + START obligatoires
    corps = [l for l in lignes if not l.startswith("%%")]
    if len(corps) < 2 or corps[0] != "flowchart TD":
        erreurs.append("header != flowchart TD")
    if len(corps) < 2 or not corps[1].lstrip().startswith("START"):
        erreurs.append("ligne START absente ou malformee")
    ids = set(cases.keys()) | set(["START", "FIN-APPELANT"])
    for l in corps[2:]:
        if not l or l.startswith("%%"):
            continue
        t = l.strip()
        if not t:
            continue
        # premiere balise = id de noeud (jusqu a un separateur de forme)
        balise = t.split(" ")[0]
        for sep in ("([", "[", "{"):
            if sep in balise:
                balise = balise.split(sep)[0]
                break
        if balise not in ids:
            erreurs.append("balise inconnue : %r" % t[:70])
            continue
        if "-->" in t:
            # arete simple ou etiquetee : la cible est le dernier token
            cible = t.split(" --> ")[-1]
            cible = cible.replace('"', "").strip()
            if cible not in ids:
                erreurs.append("cible inconnue : %r" % t[:70])
    return erreurs


# ---------------------------------------------------------------------------
# Moteur SVG : parseur .mmd -> layout par etages -> SVG deterministe
# ---------------------------------------------------------------------------

PAT_NOEUD = re.compile(r"^([A-Za-z0-9_-]+)(.*)$")


def analyser_noeud(partie):
    """Parse 'ID', 'ID["lbl"]', 'ID{"lbl"}', 'ID(["lbl"])'.
    Retourne (id, label|None, forme|None)."""
    m = PAT_NOEUD.match(partie.strip())
    if not m:
        return None
    nid, reste = m.group(1), m.group(2)
    if not reste:
        return (nid, None, None)
    if reste.startswith('(["') and reste.endswith('"])'):
        return (nid, reste[3:-2], "stadium")
    if reste.startswith("[") and reste.endswith("]"):
        return (nid, reste[1:-1], "rect")
    if reste.startswith("{") and reste.endswith("}"):
        return (nid, reste[1:-1], "diamond")
    return (nid, None, None)


def analyser_mmd(texte):
    """Parse le .mmd genere. Retourne (noeuds, idx, aretes) dans l ordre
    d apparition (ordre stable)."""
    noeuds = []
    idx = {}
    aretes = []

    def ajouter_noeud(nid, label, forme):
        if nid in idx:
            return
        idx[nid] = len(noeuds)
        noeuds.append({"id": nid, "label": label, "forme": forme})

    for ligne in texte.splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("%%") or ligne == "flowchart TD":
            continue
        if "-->" in ligne:
            source, cible = ligne.split(" --> ", 1)
            etiquette = ""
            if ' -- "' in source:
                source, etiquette = source.split(' -- "', 1)
                etiquette = etiquette.rstrip('"')
            src = analyser_noeud(source)
            if src is None:
                continue
            nid, label, forme = src
            cible = cible.strip()
            if label is not None:
                ajouter_noeud(nid, label, forme)
            else:
                ajouter_noeud(nid, nid, "rect")
            if cible not in idx:
                if cible == "FIN-APPELANT":
                    ajouter_noeud(cible, "FIN-APPELANT", "appelant")
                else:
                    ajouter_noeud(cible, cible, "rect")
            aretes.append({"src": nid, "tgt": cible, "label": etiquette})
        else:
            n = analyser_noeud(ligne)
            if n:
                nid, label, forme = n
                if label is not None:
                    ajouter_noeud(nid, label, forme)
                else:
                    ajouter_noeud(nid, nid, "rect")
    return noeuds, idx, aretes


def decouper_lignes(texte, largeur_max):
    """Decoupe un libelle en lignes de <= largeur_max caracteres (sur espaces)."""
    mots = (texte or "").split()
    if not mots:
        return [""]
    lignes = []
    courante = ""
    for m in mots:
        if not courante:
            courante = m
        elif len(courante) + 1 + len(m) <= largeur_max:
            courante += " " + m
        else:
            lignes.append(courante)
            courante = m
    if courante:
        lignes.append(courante)
    return lignes or [""]


def calculer_rangs(noeuds, aretes):
    """Rangs : BFS depuis START pour casser les cycles (aretes arriere), puis
    chemin le plus long sur le DAG restant (layout compact et sans arete
    montante autre que les retours)."""
    rang = dict((n["id"], None) for n in noeuds)
    rang["START"] = 0
    file = ["START"]
    while file:
        cid = file.pop(0)
        for a in aretes:
            if a["src"] == cid and rang[a["tgt"]] is None:
                rang[a["tgt"]] = rang[cid] + 1
                file.append(a["tgt"])
    for n in noeuds:
        if rang[n["id"]] is None:
            rang[n["id"]] = 0  # cases injoignables (signalees par ailleurs)
    # Relaxation du plus long chemin, sans propager a travers les aretes
    # arriere (niveau cible <= niveau source) : elles cassent les cycles.
    for _ in range(len(noeuds)):
        change = False
        for a in aretes:
            if rang[a["tgt"]] <= rang[a["src"]]:
                continue
            if rang[a["tgt"]] < rang[a["src"]] + 1:
                rang[a["tgt"]] = rang[a["src"]] + 1
                change = True
        if not change:
            break
    return rang


def calculer_mise_en_page(noeuds, aretes, rang):
    """Calcule x/y/w/h de chaque noeud (rangs centres, ordre stable).
    Retourne (largeur_totale, hauteur_totale)."""
    for n in noeuds:
        lignes = decouper_lignes(n["label"], 26)
        n["lignes"] = lignes
        lm = max(len(l) for l in lignes) if lignes else 1
        n["w"] = max(64, lm * 6.4 + 30)
        n["h"] = max(36, len(lignes) * 14 + 20)
    par_rang = {}
    for n in noeuds:
        par_rang.setdefault(rang[n["id"]], []).append(n)
    rangs = sorted(par_rang.keys())
    largeur_max = 0
    for r in rangs:
        groupe = par_rang[r]
        largeur_rang = sum(n["w"] for n in groupe) + 40 * (len(groupe) - 1)
        largeur_max = max(largeur_max, largeur_rang)
    y_courant = 40
    for r in rangs:
        groupe = par_rang[r]
        hauteur_rang = max(n["h"] for n in groupe)
        largeur_rang = sum(n["w"] for n in groupe) + 40 * (len(groupe) - 1)
        x = (largeur_max - largeur_rang) / 2.0 + 50
        for n in groupe:
            n["x"] = x
            n["y"] = y_courant
            x += n["w"] + 40
        y_courant += hauteur_rang + 90
    return largeur_max + 100, y_courant


def echapper_xml(texte):
    t = (texte or "").replace("&", "&amp;").replace("<", "&lt;")
    t = t.replace(">", "&gt;").replace('"', "&quot;")
    return t.replace("'", "&apos;")


def rendu_texte(n, xml):
    """Bloc <text> centre du noeud (multilignes via tspan)."""
    cx = n["x"] + n["w"] / 2.0
    cy = n["y"] + n["h"] / 2.0
    lignes = n.get("lignes") or [n["label"]]
    debut = cy - (len(lignes) - 1) * 7.0 + 4
    xml.append('    <text x="%.1f" y="%.1f" text-anchor="middle" '
               'font-size="%s" fill="%s">'
               % (cx, debut, TAILLE_TEXTE, COULEUR_TEXTE))
    for i, l in enumerate(lignes):
        dy = "0" if i == 0 else "14"
        xml.append('      <tspan x="%.1f" dy="%s">%s</tspan>'
                   % (cx, dy, echapper_xml(l)))
    xml.append("    </text>")


def rendu_forme(n, xml):
    x, y, w, h = n["x"], n["y"], n["w"], n["h"]
    forme = n["forme"]
    if forme == "diamond":
        style = FORME_LOSANGE
        cx = x + w / 2.0
        cy = y + h / 2.0
        xml.append('    <path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f Z" '
                   'fill="%s" stroke="%s" stroke-width="1.3"/>'
                   % (cx, y, x + w, cy, cx, y + h, x, cy,
                      style["fond"], style["bord"]))
    elif forme == "appelant":
        style = FORME_APPELANT
        xml.append('    <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
                   'rx="%.1f" fill="%s" stroke="%s" stroke-width="1.3"/>'
                   % (x, y, w, h, h / 2.0, style["fond"], style["bord"]))
    else:  # rect ou stadium
        style = FORME_STADIUM if forme == "stadium" else FORME_RECT
        rx = h / 2.0 if forme == "stadium" else 6
        xml.append('    <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
                   'rx="%.1f" fill="%s" stroke="%s" stroke-width="1.3"/>'
                   % (x, y, w, h, rx, style["fond"], style["bord"]))


def rendu_etiquette(x, y, texte, xml):
    """Etiquette d arete sur fond blanc (largeur estimee depuis le texte)."""
    if not texte:
        return
    largeur = max(18, len(texte) * 5.6 + 12)
    xml.append('    <rect x="%.1f" y="%.1f" width="%.1f" height="15" rx="3" '
               'fill="%s" stroke="none"/>'
               % (x - largeur / 2.0, y - 10, largeur, COULEUR_FOND))
    xml.append('    <text x="%.1f" y="%.1f" text-anchor="middle" font-size="%s" '
               'fill="%s">%s</text>'
               % (x, y + 2, TAILLE_ETIQUETTE, COULEUR_ETIQUETTE,
                  echapper_xml(texte)))


def rendu_arete(a, noeuds, idx, xml):
    src = noeuds[idx[a["src"]]]
    tgt = noeuds[idx[a["tgt"]]]
    sx = src["x"] + src["w"] / 2.0
    sy = src["y"] + src["h"]
    tx = tgt["x"] + tgt["w"] / 2.0
    ty = tgt["y"]
    d = None
    ex = ey = None  # position de l etiquette
    if a["src"] == a["tgt"]:
        # boucle sur soi-meme : arc a droite du noeud
        d = "M %.1f %.1f C %.1f %.1f, %.1f %.1f, %.1f %.1f" % (
            sx, sy, sx + 95, sy + 15, sx + 95, ty - 15, sx, ty)
        ex, ey = sx + 98, (sy + ty) / 2.0
    elif ty > sy:  # vers le bas (rangs suivants)
        if ty - sy <= 90:  # rang adjacent : droite
            d = "M %.1f %.1f L %.1f %.1f" % (sx, sy, tx, ty)
            ex, ey = (sx + tx) / 2.0, (sy + ty) / 2.0
        else:  # plusieurs rangs : coudee
            my = (sy + ty) / 2.0
            d = "M %.1f %.1f V %.1f H %.1f V %.1f" % (sx, sy, my, tx, ty)
            ex, ey = (sx + tx) / 2.0, my
    else:  # retour en arriere : courbe vers la droite
        my = (sy + ty) / 2.0
        d = "M %.1f %.1f C %.1f %.1f, %.1f %.1f, %.1f %.1f" % (
            sx, sy, sx + 90, my, tx + 90, my, tx, ty)
        ex, ey = (sx + tx) / 2.0 + 90, my
    xml.append('    <path d="%s" fill="none" stroke="%s" stroke-width="1.2" '
               'marker-end="url(#fleche)"/>' % (d, COULEUR_ARETE))
    if ex is not None:
        rendu_etiquette(ex, ey, a["label"], xml)


def rendre_svg(texte_mmd, agent, version_parcours):
    """Convertit le .mmd en SVG deterministe. Retourne la chaine SVG."""
    noeuds, idx, aretes = analyser_mmd(texte_mmd)
    rang = calculer_rangs(noeuds, aretes)
    largeur, hauteur = calculer_mise_en_page(noeuds, aretes, rang)

    xml = []
    xml.append('<?xml version="1.0" encoding="UTF-8"?>')
    xml.append("<!-- Carte de decision de %s (parcours v%s) - genere par "
               "convertir-carte-mermaid v%s -->" % (agent, version_parcours, VERSION))
    xml.append('<svg xmlns="http://www.w3.org/2000/svg" width="%.0f" height="%.0f" '
               'viewBox="0 0 %.0f %.0f" font-family="%s">'
               % (largeur, hauteur, largeur, hauteur, FONTE))
    xml.append("  <defs>")
    xml.append('    <marker id="fleche" viewBox="0 0 10 10" refX="9" refY="5" '
               'markerWidth="7" markerHeight="7" orient="auto-start-reverse">')
    xml.append('      <path d="M 0 0 L 10 5 L 0 10 z" fill="%s"/>'
               % COULEUR_ARETE)
    xml.append("    </marker>")
    xml.append("  </defs>")
    xml.append('  <rect width="%.0f" height="%.0f" fill="%s"/>'
               % (largeur, hauteur, COULEUR_FOND))
    for a in aretes:
        rendu_arete(a, noeuds, idx, xml)
    for n in noeuds:
        rendu_forme(n, xml)
        rendu_texte(n, xml)
    xml.append("</svg>")
    return "\n".join(xml) + "\n"


def generer(racine, agent, dossier_sortie, avec_index=False, avec_svg=False):
    """Genere le .mmd (et .svg si demande) d un agent. Retourne le compte."""
    os.makedirs(dossier_sortie, exist_ok=True)
    parcours = lister_parcours(racine)
    nb = 0
    for p in parcours:
        donnees = charger_parcours(p)
        agent_parcours = agent_du_parcours(donnees)
        if agent and agent_parcours != agent:
            continue
        nom = nom_fichier_parcours(p, donnees)
        texte, avis = convertir(donnees)
        erreurs_syntaxe = verifier_syntaxe(texte, donnees.get("cases", {}))
        chemin = os.path.join(dossier_sortie, nom + ".mmd")
        with io.open(chemin, "w", encoding="ascii", newline="\n") as fh:
            fh.write(texte)
        ligne = "  %s.mmd : %d lignes%s%s" % (
            nom, len(texte.splitlines()),
            " (%d avis)" % len(avis) if avis else "",
            " (%d SYNTAXE KO)" % len(erreurs_syntaxe) if erreurs_syntaxe else "")
        if avec_svg:
            version_parcours = donnees.get("parcours", {}).get("version", "?")
            svg = rendre_svg(texte, nom, version_parcours)
            chemin_svg = os.path.join(dossier_sortie, nom + ".svg")
            with io.open(chemin_svg, "w", encoding="ascii", newline="\n") as fh:
                fh.write(svg)
            ligne += "  + %s.svg : %d octets" % (nom, len(svg.encode("ascii")))
        print(ligne)
        for a in avis[:5]:
            print("      - %s" % a)
        for e in erreurs_syntaxe[:5]:
            print("      [SYNTAXE] %s" % e)
        nb += 1
    if avec_index:
        lignes = ["# Cartes de decision - vues Mermaid", "",
                  "Genere par convertir-carte-mermaid (source de verite : "
                  "parcours-<agent>.json).", "",
                  "| Agent | Parcours | Version | Vue | Image |",
                  "|---|---|---|---|---|"]
        for p in parcours:
            donnees = charger_parcours(p)
            agent_parcours = agent_du_parcours(donnees)
            if agent and agent_parcours != agent:
                continue
            nom = nom_fichier_parcours(p, donnees)
            parc = donnees.get("parcours", {})
            lignes.append("| %s | %s | %s | [%s.mmd](%s.mmd) | "
                          "[%s.svg](%s.svg) |"
                          % (agent_parcours, parc.get("nom", "?"),
                             parc.get("version", "?"), nom, nom, nom, nom))
        chemin = os.path.join(dossier_sortie, "index.md")
        with io.open(chemin, "w", encoding="ascii", newline="\n") as fh:
            fh.write("\n".join(lignes) + "\n")
        print("  index.md ecrit")
    return nb


def verifier(racine, dossier_sortie):
    """Verifie la synchronisation cartes <-> .mmd <-> .svg. Retourne rc."""
    erreurs = []
    parcours = lister_parcours(racine)
    for p in parcours:
        donnees = charger_parcours(p)
        nom = nom_fichier_parcours(p, donnees)
        texte, _ = convertir(donnees)
        chemin = os.path.join(dossier_sortie, nom + ".mmd")
        if not os.path.isfile(chemin):
            erreurs.append("%s: .mmd manquant" % nom)
        else:
            with io.open(chemin, encoding="ascii") as fh:
                existant = fh.read()
            if existant != texte:
                erreurs.append("%s: .mmd non synchronise avec la carte" % nom)
        version_parcours = donnees.get("parcours", {}).get("version", "?")
        svg = rendre_svg(texte, nom, version_parcours)
        chemin_svg = os.path.join(dossier_sortie, nom + ".svg")
        if not os.path.isfile(chemin_svg):
            erreurs.append("%s: .svg manquant" % nom)
        else:
            with io.open(chemin_svg, encoding="ascii") as fh:
                existant_svg = fh.read()
            if existant_svg != svg:
                erreurs.append("%s: .svg non synchronise avec la carte" % nom)
    if erreurs:
        print(RED + "==> %d incoherence(s) :" % len(erreurs) + NC)
        for e in erreurs:
            print("  - " + e)
        return 1
    print(GREEN + "==> %d cartes synchronisees avec leur .mmd et .svg : OK"
          % len(parcours) + NC)
    return 0


def construire_parser():
    parser = argparse.ArgumentParser(
        prog="convertir-carte-mermaid.py",
        description="Convertit les cartes de decision en graphes Mermaid "
                    "(.mmd) et images SVG.",
        add_help=False,
    )
    parser.add_argument("--agent", default="",
                        help="Carte d un seul agent (nom du dossier)")
    parser.add_argument("--svg", action="store_true",
                        help="Generer aussi le rendu SVG (avec --agent)")
    parser.add_argument("--tous", action="store_true",
                        help="Convertir toutes les cartes : .mmd + .svg + index")
    parser.add_argument("--sortie", default="",
                        help="Dossier de sortie (defaut: cartes-vues/mermaid)")
    parser.add_argument("--verifier", action="store_true",
                        help="Verifier la synchronisation cartes <-> .mmd <-> .svg")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    parser.add_argument("--aide", "-h", action="store_true",
                        help="Afficher cette aide")
    return parser


def main():
    args = construire_parser().parse_args()
    if args.version:
        print("convertir-carte-mermaid.py v%s (%s)" % (VERSION, STATUT))
        return 0
    if args.aide:
        print(__doc__)
        return 0
    if not (args.agent or args.tous or args.verifier):
        print("[ERREUR] Fournir --agent <nom>, --tous ou --verifier (--aide)")
        return 2

    racine = racine_projet()
    sortie = args.sortie or os.path.join(racine, "cerveau-projet",
                                         "cartes-vues", "mermaid")

    if args.verifier:
        return verifier(racine, sortie)

    if args.agent:
        generer(racine, args.agent, sortie, avec_index=False,
                avec_svg=args.svg)
    else:
        generer(racine, "", sortie, avec_index=True, avec_svg=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
