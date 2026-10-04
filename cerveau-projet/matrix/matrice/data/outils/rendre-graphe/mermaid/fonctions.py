"""Fonctions du verbe `mermaid` : une SOURCE -> un MODELE -> du TEXTE Mermaid.

LE MODELE EST LE PIVOT (noeuds + aretes + formes), et le TEXTE MERMAID est ce que
l agent lit et ce que le rendu SVG RELIT : le SVG ne consomme JAMAIS le modele, il
reparse le texte -- c est ce qui prouve que la chaine < n importe quoi -> mermaid ->
svg > tient de bout en bout (et c est l architecture de la v1, memoire citee).

CE QUE LE MODELE PORTE AUSSI : les INCOHERENCES mesurees (un renvoi vers un fichier
absent, une case introuvable, un theme orphelin). Elles ne sont pas seulement
ACCUSEES : elles deviennent des NOEUDS DE LA VUE, relies a la case fautive -- une
incoherence cachee est une incoherence qu on ne repare pas.
"""
import re

from commun import charger_json, charger_module, domicile_vivier
from constants import (
    CHEMIN_FINS,
    CHEMIN_INDEX_PARCOURS,
    FORME_DEFAUT,
    MARQUE_COMMENTAIRE,
    NOM_OUTIL,
    REPERTOIRE_OPERATEUR,
    REPERTOIRE_THEMES,
    TETE_FLUX,
    VERSION,
)
from verifier.fonctions import (
    incoherences_parcours,
    incoherences_vivier,
    resoudre_renvoi,
)

FORME_ERREUR = "erreur"
MARQUE_INCOHERENCE = "INCOHERENCE"

# Les libelles restent COURTS : une vue se lit d un coup d oeil, et une case dont
# le titre fait trois lignes cache les suivantes.
LARGEUR_LIBELLE = 60
LARGEUR_ETIQUETTE = 34


def modele_vide(titre, sous_titre=""):
    """Un modele neuf : le pivot que tous les adaptateurs remplissent."""
    return {"titre": titre, "sous_titre": sous_titre, "noeuds": [], "aretes": [],
            "index": {}}


def _net(texte):
    """Un libelle d une seule ligne, sans guillemet (le texte Mermaid en porte)."""
    plat = " ".join(str(texte or "").split())
    return plat.replace('"', "'").replace("`", "'")


def _court(texte, largeur):
    """Le debut d un libelle, avec une marque quand il a ete coupe (jamais un mensonge)."""
    plat = _net(texte)
    return plat if len(plat) <= largeur else plat[:largeur - 3] + "..."


def slug(texte):
    """Un identifiant Mermaid : lettres, chiffres, tiret, souligne. Jamais un espace."""
    propre = re.sub(r"[^A-Za-z0-9_-]+", "-", str(texte or "").strip()).strip("-")
    return propre or "N"


def noeud(modele, identifiant, label=None, forme=None):
    """Le noeud <identifiant> (cree au premier appel, complete ensuite). Rend son id.

    Deux appels avec le meme identifiant NE FONT PAS deux cases : c est ce qui
    permet de relier une arete a une case deja posee.
    """
    identifiant = slug(identifiant)
    if identifiant in modele["index"]:
        existant = modele["index"][identifiant]
        if label and not existant.get("label"):
            existant["label"] = _court(label, LARGEUR_LIBELLE)
        if forme and not existant.get("forme"):
            existant["forme"] = forme
        return identifiant
    modele["index"][identifiant] = {
        "id": identifiant,
        "label": _court(label, LARGEUR_LIBELLE) if label else identifiant,
        "forme": forme or FORME_DEFAUT,
    }
    modele["noeuds"].append(modele["index"][identifiant])
    return identifiant


def arete(modele, source, cible, label=""):
    """Ajoute l arete source -> cible (une seule fois : la vue ne double pas un lien)."""
    source, cible = slug(source), slug(cible)
    etiquette = _court(label, LARGEUR_ETIQUETTE)
    for existante in modele["aretes"]:
        if existante["src"] == source and existante["tgt"] == cible \
                and existante["label"] == etiquette:
            return
    modele["aretes"].append({"src": source, "tgt": cible, "label": etiquette})


def _poser_incoherences(modele, incoherences, ancres):
    """Rend VISIBLES les incoherences : un noeud ROUGE relie a la case fautive.

    `ancres` associe une incoherence a l identifiant de sa case (mesure au moment du
    jugement) : une incoherence sans case reste au noeud INCOHERENCE general -- elle
    est DITE, jamais perdue.
    """
    modele["incoherences"] = list(incoherences)
    for rang, incoherence in enumerate(incoherences, 1):
        noeud_id = "INCOHERENCE-" + str(rang)
        noeud(modele, noeud_id,
              incoherence.get("code", MARQUE_INCOHERENCE) + " : "
              + _court(incoherence.get("detail", ""), 70), FORME_ERREUR)
        source = ancres.get(incoherence.get("cle", ""))
        if source:
            arete(modele, slug(source), noeud_id, "INCOHERENT")
    return modele


# ---------------------------------------------------------------------------
# LES ADAPTATEURS : chaque source a SA maniere de devenir un modele
# ---------------------------------------------------------------------------

def modele_parcours_index():
    """La VUE du parcours : l ordre des themes, et ce qui ne tient pas debout."""
    index = charger_json(CHEMIN_INDEX_PARCOURS)
    modele = modele_vide("Parcours d Optimus -- les themes, dans leur ordre",
                         "index-parcours.json (theme courant : "
                         + str((index or {}).get("theme_courant", "?")) + ")")
    if index is None:
        return modele, [{"code": "index-absent", "cle": "",
                         "detail": "index-parcours.json ILLISIBLE : " + str(CHEMIN_INDEX_PARCOURS)}]
    incoherences, ancres = incoherences_parcours(index)
    noeud(modele, "START", "Demande du createur", "stadium")
    for entree in index.get("parcours", []):
        identifiant = noeud(modele, "THEME-" + str(entree.get("theme", "")),
                            str(entree.get("ordre", "?")) + ". " + str(entree.get("theme", ""))
                            + "  [" + str(entree.get("statut", "?")) + "]")
        arete(modele, "START", identifiant, "ordre " + str(entree.get("ordre", "?")))
        ancres.setdefault("theme:" + str(entree.get("theme", "")), identifiant)
    courante = str(index.get("theme_courant", ""))
    if courante and "THEME-" + courante in modele["index"]:
        modele["index"]["THEME-" + courante]["forme"] = "diamond"
        noeud(modele, "COURANT", "THEME COURANT", "stadium")
        arete(modele, "COURANT", "THEME-" + courante, "en cours")
    _poser_incoherences(modele, incoherences, ancres)
    return modele, incoherences


def modele_parcours_theme(nom):
    """La VUE d UN theme : sa suite de cases, ses renvois, et sa fin."""
    nom = str(nom or "").strip().upper()
    index = charger_json(CHEMIN_INDEX_PARCOURS) or {}
    entree = None
    for candidate in index.get("parcours", []):
        if str(candidate.get("theme", "")).upper() == nom:
            entree = candidate
            break
    modele = modele_vide("Parcours d Optimus -- theme " + (nom or "?"),
                         "les cases du theme, dans leur ordre, et leurs renvois")
    if entree is None:
        return modele, [{"code": "theme-absent", "cle": "",
                         "detail": "le theme " + (nom or "?") + " n est PAS dans l index"}]
    chemin = REPERTOIRE_OPERATEUR / "parcours" / str(entree.get("fichier", ""))
    donnees = charger_json(chemin)
    if donnees is None:
        incoherence = {"code": "fichier-absent", "cle": "theme:" + nom,
                       "detail": "le fichier du theme est ABSENT : " + str(entree.get("fichier", ""))}
        modele = modele_vide("Parcours d Optimus -- theme " + nom + " (FICHIER ABSENT)",
                             str(entree.get("fichier", "")))
        noeud(modele, "START", "Theme " + nom, "stadium")
        _poser_incoherences(modele, [incoherence], {"theme:" + nom: "START"})
        return modele, [incoherence]
    theme = donnees.get("theme", {}) if isinstance(donnees, dict) else {}
    modele["sous_titre"] = _net(theme.get("but", ""))[:120]
    incoherences, ancres = incoherences_parcours(index, theme=theme, nom_theme=nom)
    noeud(modele, "START", "Theme " + nom, "stadium")
    precedent = "START"
    for rang, redirect in enumerate(theme.get("redirects", []), 1):
        besoin = str(redirect.get("besoin", ""))
        # L IDENTIFIANT EST LE RANG (mesure 2026-09-29 : 132 cases sur 150 ne portent
        # AUCUN `[crochet]` -- en faire une part de l id fabriquait 132 ids
        # `sans-crochet` et un noeud qui ne dit rien). Le rang est stable, unique, et
        # l etiquette PORTE le besoin tel quel (le crochet, quand il existe, s y
        # trouve deja).
        identifiant = noeud(modele, "CASE-" + str(rang), str(rang) + ". " + besoin)
        arete(modele, precedent, identifiant, "case " + str(rang))
        ancres.setdefault("case:" + nom + ":" + str(rang), identifiant)
        condition = redirect.get("condition")
        renvoi = resoudre_renvoi(redirect.get("vers"), nom_theme=nom)
        if isinstance(renvoi, dict) and renvoi.get("cible"):
            arete(modele, identifiant, renvoi["cible"],
                  _court(condition or renvoi.get("etiquette", ""), LARGEUR_ETIQUETTE))
        elif renvoi:
            ancres["renvoi:" + str(rang)] = identifiant
        precedent = identifiant
    fin = donnees.get("fin", {}) if isinstance(donnees, dict) else {}
    case_fin = fin.get("case") if isinstance(fin, dict) else None
    fins = charger_json(CHEMIN_FINS) or {}
    nom_fin = "FIN"
    for candidate in (fins.get("fins") or []):
        if candidate.get("case") == case_fin:
            nom_fin = "FIN-" + slug(str(case_fin))
            noeud(modele, nom_fin, _court(candidate.get("nom", "FIN"), LARGEUR_LIBELLE),
                  "stadium")
            break
    else:
        nom_fin = "FIN"
        noeud(modele, nom_fin, "FIN : " + str(case_fin or "(aucune)"), "stadium")
    arete(modele, precedent, nom_fin, "fin")
    _poser_incoherences(modele, incoherences, ancres)
    return modele, incoherences


def modele_vivier():
    """La VUE du vivier : les categories, leurs themes, et ce qui cloche."""
    chemin, categories = domicile_vivier()
    donnees = charger_json(chemin) if chemin else None
    modele = modele_vide("Le vivier -- les themes par categorie",
                         "le domicile du vivier (M-076) : " + str(chemin))
    if donnees is None:
        return modele, [{"code": "vivier-absent", "cle": "",
                         "detail": "la BDD du vivier est ILLISIBLE : " + str(chemin)}]
    incoherences, ancres = incoherences_vivier(donnees, categories)
    noeud(modele, "START", "Vivier", "stadium")
    for theme in donnees.get("themes", []):
        categorie = str(theme.get("categorie", "") or "(SANS CATEGORIE)")
        groupe = noeud(modele, "CAT-" + categorie, categorie, "diamond")
        arete(modele, "START", groupe)
        identifiant = noeud(modele, "THEME-" + str(theme.get("nom", "")),
                            str(theme.get("id", "?")) + " " + str(theme.get("nom", ""))
                            + " -- " + _court(theme.get("but", ""), LARGEUR_LIBELLE))
        arete(modele, groupe, identifiant)
        ancres.setdefault("theme:" + str(theme.get("nom", "")).upper(), identifiant)
        ancres.setdefault("id:" + str(theme.get("id", "")), identifiant)
    _poser_incoherences(modele, incoherences, ancres)
    return modele, incoherences


def modele_arbre(chemin):
    """La VUE d un ARBRE generique : {racine, noeuds:[{id,label,fils|vers}]} ou une liste.

    <N IMPORTE QUOI> veut dire quelque chose : un arbre se decrit AUSSI par une
    liste plate de maillons (`id`, `label`, `suivant`) -- la meme forme que celle
    que l entonnoir utilise pour un brin. Les deux formes se rendent.
    """
    donnees = charger_json(chemin)
    modele = modele_vide("Arbre : " + str(chemin or "?"), "source : " + str(chemin))
    if donnees is None:
        return modele, [{"code": "arbre-absent", "cle": "",
                         "detail": "la source est ILLISIBLE : " + str(chemin)}]
    noeud(modele, "START", str(donnees.get("racine", "RACINE")) if isinstance(donnees, dict)
          else "RACINE", "stadium")
    maillons = donnees.get("noeuds") if isinstance(donnees, dict) else donnees
    if not isinstance(maillons, list):
        return modele, [{"code": "arbre-forme", "cle": "",
                         "detail": "forme inattendue : attendu une liste `noeuds`"}]
    for maillon in maillons:
        if not isinstance(maillon, dict):
            continue
        identifiant = noeud(modele, "N-" + str(maillon.get("id", "?")),
                            str(maillon.get("label", maillon.get("id", "?"))))
        arete(modele, str(maillon.get("de", "START")), identifiant)
        for suivant in _suivants(maillon):
            arete(modele, identifiant, "N-" + slug(str(suivant)))
    return modele, []


def _suivants(maillon):
    """Les cibles d un maillon : `suivant`, `suivants`, `fils` ou `vers` (toutes formes)."""
    for cle in ("suivant", "suivants", "fils", "vers"):
        valeur = maillon.get(cle)
        if isinstance(valeur, str):
            return [valeur]
        if isinstance(valeur, list):
            return [element.get("id", element) if isinstance(element, dict) else element
                    for element in valeur]
    return []


def serialiser(modele):
    """Le MODELE -> le TEXTE MERMAID. C est ce texte que l agent lit ET que le SVG relit."""
    lignes = [MARQUE_COMMENTAIRE + " " + _net(modele.get("titre", ""))]
    if modele.get("sous_titre"):
        lignes.append(MARQUE_COMMENTAIRE + " " + _net(modele.get("sous_titre", "")))
    lignes.append(MARQUE_COMMENTAIRE + " genere par " + NOM_OUTIL + " v" + VERSION
                  + " -- " + str(len(modele.get("noeuds", []))) + " noeud(s), "
                  + str(len(modele.get("aretes", []))) + " arete(s)")
    lignes.append(TETE_FLUX)
    for element in modele.get("noeuds", []):
        lignes.append("    " + element["id"] + _forme_mermaid(element))
    for element in modele.get("aretes", []):
        if element.get("label"):
            lignes.append('    ' + element["src"] + ' -- "' + element["label"] + '" --> '
                          + element["tgt"])
        else:
            lignes.append("    " + element["src"] + " --> " + element["tgt"])
    return "\n".join(lignes) + "\n"


def _forme_mermaid(element):
    """La forme Mermaid d un noeud : [rect], {losange}, ([stade]), [[incoherence]]."""
    label = '"' + _net(element.get("label", element["id"])) + '"'
    forme = element.get("forme", FORME_DEFAUT)
    if forme == "diamond":
        return "{" + label + "}"
    if forme == "stadium":
        return "([" + label + "])"
    if forme == FORME_ERREUR:
        return "[[" + label + "]]"
    if forme == "appelant":
        return "([" + label + "])"
    return "[" + label + "]"
