"""Fonctions du verbe `svg` : du TEXTE MERMAID -> une IMAGE SVG, en Python pur.

PORTAGE DE LA v1 (memoire citee, dans `constants.MEMOIRE_V1`) : le parseur
(l. 526-598), les RANGS (l. 620-649 : BFS depuis START pour casser les cycles, puis
plus long chemin), la MISE EN PAGE (l. 651-681 : rangs centres, ordre stable), le
RENDU des formes, des aretes et des etiquettes (l. 683-807), et l EN-TETE SVG
(l. 776-807 : defs, marqueur de fleche, fond).

TROIS PROPRIETES QUE JE GARDE DE LA v1, ET POURQUOI :
  - AUCUNE DEPENDANCE : pas de navigateur, pas de node, pas de reseau. Un SVG se
    fabrique ici, en Python pur -- il se fabrique donc la ou l outil tourne ;
  - DETERMINISTE : meme texte -> memes octets. Aucun hasard, aucun horodatage, aucun
    ordre de dictionnaire non maitrise : c est ce qui permet de COMPARER deux vues ;
  - ASCII STRICT : les libelles sont deja ASCII (la Matrice l exige) et l XML est
    echappe -- une vue qu on ne peut pas relire ne sert a rien.

CE QUE LE MOTEUR AJOUTE A LA v1 : la forme `erreur` (double crochet `[[...]]`), qui
rend une INCOHERENCE visible dans l image au lieu de la laisser dans un journal.
"""
import re

from constants import (
    COULEUR_ARETE,
    COULEUR_ETIQUETTE,
    COULEUR_FOND,
    COULEUR_TEXTE,
    FONTE,
    FORMES,
    FORME_DEFAUT,
    HAUTEUR_MIN_NOEUD,
    LARGEUR_CARACTERE,
    LARGEUR_CARACTERE_ETIQUETTE,
    LARGEUR_LIBELLE_MAX,
    LARGEUR_PAGE_MAX,
    MARGE_HORIZONTALE_RANG,
    MARGE_PAGE,
    MARGE_VERTICALE_RANG,
    PAS_DE_LIGNE_TEXTE,
    PLANCHE_MIN_NOEUD,
    TAILLE_ETIQUETTE,
    TAILLE_TEXTE,
    NOM_OUTIL,
    VERSION,
)

PAT_NOEUD = re.compile(r"^([A-Za-z0-9_-]+)(.*)$")
MOTIF_ARETE = re.compile(r"^(.*?)\s*(-->|---|-.->|==>)\s*(.*)$")
# LES LIGNES QU ON NE LIT PAS COMME NOEUD NI ARETE, en UN motif DECLARE (et non
# huit `startswith` eparpilles) : le commentaire Mermaid (`%%`, y compris l en-tete
# que CE generateur ecrit lui-meme), l ouverture de flux (`flowchart` / `graph`),
# la fermeture (`end`), et les DECLARATIONS de style ou de sous-graphe
# (`subgraph`, `style `, `classDef`, `linkStyle`). Un motif se lit, se relit et se
# corrige a UN endroit.
MOTIF_LIGNE_IGNOREE = re.compile(
    r"^(%%|flowchart\b|graph\b|end$|subgraph\b|style\b|classDef\b|linkStyle\b)")
# LES FORMES, du delimiteur le PLUS LONG au plus court (sinon `([` se lit comme `(`).
FORMES_MERMAID = (
    ("(((", ")))", "circle"),
    ("((", "))", "circle"),
    ("([", "])", "stadium"),
    ("[[", "]]", "erreur"),
    ("{", "}", "diamond"),
    ("(", ")", "rounded"),
    ("[", "]", "rect"),
)


def _label_net(texte):
    """Le libelle d un noeud : sans ses guillemets ni ses espaces de bord."""
    return str(texte or "").strip().strip('"').strip()


def analyser_noeud(partie):
    """'ID', 'ID["lbl"]', 'ID{"lbl"}', 'ID(["lbl"])', 'ID[["lbl"]]' -> (id, label, forme)."""
    trouve = PAT_NOEUD.match(str(partie or "").strip())
    if not trouve:
        return None
    identifiant, reste = trouve.group(1), trouve.group(2).strip()
    if not reste:
        return (identifiant, None, None)
    for ouverture, fermeture, forme in FORMES_MERMAID:
        if reste.startswith(ouverture) and reste.endswith(fermeture):
            return (identifiant, _label_net(reste[len(ouverture):len(reste) - len(fermeture)]),
                    forme)
    return (identifiant, None, None)


def analyser_mmd(texte):
    """(noeuds, index, aretes) dans l ORDRE D APPARITION (l ordre est stable)."""
    noeuds, index, aretes = [], {}, []

    def poser(identifiant, label, forme):
        if identifiant in index:
            # index porte la POSITION (un entier), pas le noeud : le relire
            # comme un dict plantait sur TOUT diagramme qui RE-DECLARE un noeud
            # deja pose -- c'est-a-dire sur la forme la plus naturelle d'un
            # diagramme de flux, ou un noeud est announce par une arete puis
            # decrit. Cobaye MO-543 ; contre-temoin : ids uniques, inchange.
            existant = noeuds[index[identifiant]]
            if label and existant.get("label") in (None, identifiant):
                existant["label"] = label
            if forme and not existant.get("forme"):
                existant["forme"] = forme
            return
        index[identifiant] = len(noeuds)
        noeuds.append({"id": identifiant, "label": label or identifiant,
                       "forme": forme or FORME_DEFAUT})

    for brute in str(texte or "").splitlines():
        ligne = brute.strip()
        if not ligne or MOTIF_LIGNE_IGNOREE.match(ligne):
            continue
        if MOTIF_LIGNE_IGNOREE.match(ligne):
            continue
        arete = MOTIF_ARETE.match(ligne)
        if arete:
            gauche, droite = arete.group(1), arete.group(3).strip()
            etiquette = ""
            if "--" in gauche:
                tete, reste = gauche.split("--", 1)
                etiquette = _label_net(reste)
                gauche = tete
            source = analyser_noeud(gauche)
            if source is None:
                continue
            cible = analyser_noeud(droite)
            poser(source[0], source[1], source[2])
            if cible is None:
                continue
            poser(cible[0], cible[1], cible[2])
            aretes.append({"src": source[0], "tgt": cible[0], "label": etiquette})
            continue
        seul = analyser_noeud(ligne)
        if seul:
            poser(seul[0], seul[1], seul[2])
    return noeuds, index, aretes


def decouper_lignes(texte, largeur_max=LARGEUR_LIBELLE_MAX):
    """Un libelle en lignes de <= largeur_max caracteres (decoupe sur les espaces)."""
    mots = str(texte or "").split()
    if not mots:
        return [""]
    lignes, courante = [], ""
    for mot in mots:
        if not courante:
            courante = mot
        elif len(courante) + 1 + len(mot) <= largeur_max:
            courante += " " + mot
        else:
            lignes.append(courante)
            courante = mot
    if courante:
        lignes.append(courante)
    return lignes or [""]


def calculer_rangs(noeuds, aretes):
    """Le rang de chaque noeud : BFS depuis START (cycles casses), puis plus long chemin."""
    rang = dict((element["id"], None) for element in noeuds)
    if not noeuds:
        return rang
    depart = "START" if "START" in rang else noeuds[0]["id"]
    rang[depart] = 0
    file = [depart]
    while file:
        courant = file.pop(0)
        for arete in aretes:
            if arete["src"] == courant and rang.get(arete["tgt"]) is None:
                rang[arete["tgt"]] = rang[courant] + 1
                file.append(arete["tgt"])
    for element in noeuds:
        if rang.get(element["id"]) is None:
            rang[element["id"]] = 0
    for _ in range(len(noeuds)):
        change = False
        for arete in aretes:
            if rang.get(arete["tgt"], 0) <= rang.get(arete["src"], 0):
                continue
            if rang[arete["tgt"]] < rang[arete["src"]] + 1:
                rang[arete["tgt"]] = rang[arete["src"]] + 1
                change = True
        if not change:
            break
    return rang


def _replier(groupe):
    """Un rang -> les LIGNES qui tiennent dans LARGEUR_PAGE_MAX (ordre conserve).

    Le repli ne change PAS le rang : deux noeuds d une meme ligne restent au meme
    niveau, et leurs aretes gardent leur sens. Sans repli, le vivier reel (12
    themes, 4 categories, mesure 2026-09-29) rendait une image de 6866 px de large.
    """
    lignes, courante, largeur_courante = [], [], 0.0
    for element in groupe:
        ajout = element["w"] + (MARGE_HORIZONTALE_RANG if courante else 0)
        if courante and largeur_courante + ajout > LARGEUR_PAGE_MAX:
            lignes.append((courante, largeur_courante))
            courante, largeur_courante = [element], element["w"]
        else:
            courante.append(element)
            largeur_courante += ajout
    if courante:
        lignes.append((courante, largeur_courante))
    return lignes


def calculer_mise_en_page(noeuds, aretes, rang):
    """Les x/y/w/h de chaque noeud (rangs centres, ordre stable). Rend (largeur, hauteur)."""
    for element in noeuds:
        lignes = decouper_lignes(element["label"])
        element["lignes"] = lignes
        plus_longue = max(len(ligne) for ligne in lignes) if lignes else 1
        element["w"] = max(PLANCHE_MIN_NOEUD, plus_longue * LARGEUR_CARACTERE + 30)
        element["h"] = max(HAUTEUR_MIN_NOEUD, len(lignes) * PAS_DE_LIGNE_TEXTE + 20)
    par_rang = {}
    for element in noeuds:
        par_rang.setdefault(rang.get(element["id"], 0), []).append(element)
    rangs = sorted(par_rang)
    plan = [(numero, _replier(par_rang[numero])) for numero in rangs]
    largeur_max = 0.0
    for _numero, lignes in plan:
        for _groupe, largeur_ligne in lignes:
            largeur_max = max(largeur_max, largeur_ligne)
    y_courant = 40.0
    for _numero, lignes in plan:
        for groupe, largeur_ligne in lignes:
            hauteur_ligne = max(element["h"] for element in groupe)
            x = (largeur_max - largeur_ligne) / 2.0 + MARGE_PAGE
            for element in groupe:
                element["x"] = x
                element["y"] = y_courant
                x += element["w"] + MARGE_HORIZONTALE_RANG
            y_courant += hauteur_ligne + MARGE_VERTICALE_RANG
    return largeur_max + 2 * MARGE_PAGE, y_courant


def commentaire(texte):
    """Un texte -> un COMMENTAIRE XML VALIDE.

    Mesure du 2026-09-29 (banc d epreuve joue) : la ligne d en-tete portait
    `Parcours d Optimus -- les themes`, et `--` est INTERDIT dans un commentaire
    XML -- `ElementTree` refusait le document (`not well-formed, line 2`). Une
    image qu aucun lecteur XML ne peut ouvrir n est pas une image : les tirets
    doubles se replient donc en UN seul, et un tiret FINAL est retire (il collerait
    au `-->` de fermeture, meme faute).
    """
    propre = str(texte or "")
    while "--" in propre:
        propre = propre.replace("--", "-")
    return propre.rstrip("-").strip()


def echapper_xml(texte):
    """Un libelle -> du XML sur : aucun caractere ne peut casser le document."""
    propre = str(texte or "").replace("&", "&amp;").replace("<", "&lt;")
    propre = propre.replace(">", "&gt;").replace('"', "&quot;")
    return propre.replace("'", "&apos;")


def _style(forme):
    return FORMES.get(forme, FORMES[FORME_DEFAUT])


def rendu_forme(element, xml):
    """La forme du noeud : rectangle, losange, stade, cercle, ou ROUGE d incoherence."""
    x, y, w, h = element["x"], element["y"], element["w"], element["h"]
    forme = element.get("forme", FORME_DEFAUT)
    style = _style(forme)
    if forme == "diamond":
        centre_x, centre_y = x + w / 2.0, y + h / 2.0
        xml.append('    <path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f Z"'
                   ' fill="%s" stroke="%s" stroke-width="1.3"/>'
                   % (centre_x, y, x + w, centre_y, centre_x, y + h, x, centre_y,
                      style["fond"], style["bord"]))
        return
    rayon = h / 2.0 if forme in ("stadium", "appelant", "rounded", "circle", "erreur") else 6
    if forme == "circle":
        rayon = h / 2.0
    xml.append('    <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f"'
               ' fill="%s" stroke="%s" stroke-width="1.3"/>'
               % (x, y, w, h, rayon, style["fond"], style["bord"]))


def rendu_texte(element, xml):
    """Le libelle centre du noeud (une ligne par tspan : la hauteur suit le texte)."""
    centre_x = element["x"] + element["w"] / 2.0
    centre_y = element["y"] + element["h"] / 2.0
    lignes = element.get("lignes") or [element["label"]]
    depart = centre_y - (len(lignes) - 1) * (PAS_DE_LIGNE_TEXTE / 2.0) + 4
    xml.append('    <text x="%.1f" y="%.1f" text-anchor="middle" font-size="%s"'
               ' fill="%s">' % (centre_x, depart, TAILLE_TEXTE, COULEUR_TEXTE))
    for numero, ligne in enumerate(lignes):
        xml.append('      <tspan x="%.1f" dy="%s">%s</tspan>'
                   % (centre_x, "0" if numero == 0 else str(int(PAS_DE_LIGNE_TEXTE)),
                      echapper_xml(ligne)))
    xml.append("    </text>")


def rendu_etiquette(x, y, texte, xml):
    """L etiquette d une arete, sur un fond blanc (elle se lit par-dessus le trait)."""
    if not texte:
        return
    largeur = max(18, len(texte) * LARGEUR_CARACTERE_ETIQUETTE + 12)
    xml.append('    <rect x="%.1f" y="%.1f" width="%.1f" height="15" rx="3" fill="%s"'
               ' stroke="none"/>' % (x - largeur / 2.0, y - 10, largeur, COULEUR_FOND))
    xml.append('    <text x="%.1f" y="%.1f" text-anchor="middle" font-size="%s"'
               ' fill="%s">%s</text>'
               % (x, y + 2, TAILLE_ETIQUETTE, COULEUR_ETIQUETTE, echapper_xml(texte)))


def rendu_arete(arete, noeuds, index, xml):
    """Une arete : droite (rang suivant), coudee (plusieurs), courbe (retour), boucle."""
    source = noeuds[index[arete["src"]]]
    cible = noeuds[index[arete["tgt"]]]
    sx = source["x"] + source["w"] / 2.0
    sy = source["y"] + source["h"]
    tx = cible["x"] + cible["w"] / 2.0
    ty = cible["y"]
    chemin = None
    ex = ey = None
    if arete["src"] == arete["tgt"]:
        chemin = "M %.1f %.1f C %.1f %.1f, %.1f %.1f, %.1f %.1f" % (
            sx, sy, sx + 95, sy + 15, sx + 95, ty - 15, sx, ty)
        ex, ey = sx + 98, (sy + ty) / 2.0
    elif ty > sy:
        if ty - sy <= MARGE_VERTICALE_RANG:
            chemin = "M %.1f %.1f L %.1f %.1f" % (sx, sy, tx, ty)
            ex, ey = (sx + tx) / 2.0, (sy + ty) / 2.0
        else:
            milieu = (sy + ty) / 2.0
            chemin = "M %.1f %.1f V %.1f H %.1f V %.1f" % (sx, sy, milieu, tx, ty)
            ex, ey = (sx + tx) / 2.0, milieu
    else:
        milieu = (sy + ty) / 2.0
        chemin = "M %.1f %.1f C %.1f %.1f, %.1f %.1f, %.1f %.1f" % (
            sx, sy, sx + 90, milieu, tx + 90, milieu, tx, ty)
        ex, ey = (sx + tx) / 2.0 + 90, milieu
    xml.append('    <path d="%s" fill="none" stroke="%s" stroke-width="1.2"'
               ' marker-end="url(#fleche)"/>' % (chemin, COULEUR_ARETE))
    if ex is not None:
        rendu_etiquette(ex, ey, arete.get("label", ""), xml)


def rendre_svg(texte_mmd, titre="vue", sous_titre=""):
    """Le TEXTE MERMAID -> le TEXTE SVG. Deterministe, ASCII, sans dependance."""
    noeuds, index, aretes = analyser_mmd(texte_mmd)
    rang = calculer_rangs(noeuds, aretes)
    largeur, hauteur = calculer_mise_en_page(noeuds, aretes, rang)
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           "<!-- %s | %s | genere par %s v%s -->"
           % (commentaire(titre), commentaire(sous_titre), NOM_OUTIL, VERSION),
           '<svg xmlns="http://www.w3.org/2000/svg" width="%.0f" height="%.0f"'
           ' viewBox="0 0 %.0f %.0f" font-family="%s">'
           % (largeur, hauteur, largeur, hauteur, FONTE),
           "  <defs>",
           '    <marker id="fleche" viewBox="0 0 10 10" refX="9" refY="5"'
           ' markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
           '      <path d="M 0 0 L 10 5 L 0 10 z" fill="%s"/>' % COULEUR_ARETE,
           "    </marker>",
           "  </defs>",
           '  <rect width="%.0f" height="%.0f" fill="%s"/>' % (largeur, hauteur, COULEUR_FOND)]
    for arete in aretes:
        rendu_arete(arete, noeuds, index, xml)
    for element in noeuds:
        rendu_forme(element, xml)
        rendu_texte(element, xml)
    xml.append("</svg>")
    return "\n".join(xml) + "\n"
