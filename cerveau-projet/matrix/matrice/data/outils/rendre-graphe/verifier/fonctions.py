"""Fonctions du verbe `verifier` : le JUGE des sources (parcours, vivier).

CE QUE CE JUGE CHERCHE (mesure du 2026-09-29, sur les donnees reelles) :
  - un theme LISTE dans l index dont le FICHIER n existe pas -- mesure : AUTO-XXX
    (ordre 12) pointe vers `super-combos/sc-001-auto-xxx/main.py`, ABSENT : le
    parcours porte une case qui ne mene nulle part ;
  - un theme PRESENT sur le disque et ABSENT de l index -- mesure : USER-PROFIL :
    son parcours existe et il est INVISIBLE (rien ne l ordonne) ;
  - un RENVOI (`vers`) vers un fichier absent, ou vers une CASE que le fichier cite
    ne porte pas -- mesure : `theme-auto-evolution.json` case 2 cite la case
    `relire-fiche` de `theme-reprise-mission.json` (INTROUVABLE dans le fichier) et
    sa case 5 cite la case `auditer` de `proto-4-auto-audit-3-axes.md` (INTROUVABLE
    elle aussi) : deux renvois qui ne menent nulle part ;
  - une FIN hors de `fins.json`, un nom double ;
  - au vivier : un id hors forme, une CATEGORIE hors de la liste FERMEE (elle se
    LIT a son domicile, M-076), un nom double, un theme sans but.

CE QU IL NE FAIT PAS, ET C EST LE PLUS IMPORTANT : reparer. Un juge qui repare
cache ce qu il devait montrer.

TROIS REGLES ONT ETE RETIREES APRES MESURE (2026-09-29), et c est une lecon :
elles ACCUSAIENT A TORT. Un `[crochet]` en tete de `besoin` n est PAS la regle --
132 cases sur 150 n en portent AUCUN (seuls CADRAGE et PURIFICATION en usent) ;
27 cases sur 150 n ont AUCUNE etape ; et le `statut` d une entree d index n a AUCUN
vocabulaire ECRIT (les 37 entrees portent `pret`, mais rien ne le declare -- une
liste inventee ici condamnerait le premier statut neuf). Un critere qui rend rouge
ce que la convention n a jamais exige fabrique des fausses accusations en serie
(famille R-008) : une regle ne s ecrit qu apres avoir mesure ce que la donnee porte
VRAIMENT.
"""
import re
from pathlib import Path

from commun import charger_json, domicile_vivier
from constants import (
    CHEMIN_FINS,
    REPERTOIRE_OPERATEUR,
    REPERTOIRE_THEMES,
)

MOTIF_ID_VIVIER = re.compile(r"^TH-\d{3}$")
# LES BASES DE RENVOI, dans leur ordre d essai (mesure du 2026-09-29) : les DEUX
# formes sont en usage dans les donnees reelles -- `theme-reprise-mission.json`
# (nom NU, depuis `parcours/themes/`) et `parcours/themes/theme-contre-analyse.json`
# (chemin COMPLET, depuis la racine de l operateur). Essayer UNE seule base
# accusait a tort la seconde forme : la resolution essaie les deux et DIT celle qui
# a servi.
BASES_RENVOI = (REPERTOIRE_OPERATEUR, REPERTOIRE_THEMES)


def _incoherence(code, detail, cle=""):
    """Une incoherence : son CODE (ferme), son DETAIL (lisible), et sa CLE (sa case)."""
    return {"code": code, "detail": detail, "cle": cle}


def lire_themes():
    """{nom de fichier: donnees} pour tous les `parcours/themes/theme-*.json`."""
    themes = {}
    for chemin in sorted(Path(REPERTOIRE_THEMES).glob("theme-*.json")):
        donnees = charger_json(chemin)
        if donnees is not None:
            themes[chemin.name] = donnees
    return themes


def resoudre_renvoi(vers, nom_theme=""):
    """Resout un renvoi : la cible EXISTE-t-elle, et ou mene-t-elle ?

    Rend {"cible" : id du noeud | "", "label" : etiquette, "resolu" : bool,
    "motif" : pourquoi c est casse, "base" : la base qui a servi}. Une case citee
    est cherchee DANS LE TEXTE du fichier : une case qu on ne peut pas nommer est
    une case qui n existe pas.
    """
    if not isinstance(vers, dict) or not vers:
        return {"cible": "", "label": "", "resolu": True, "motif": "", "base": ""}
    type_cible = str(vers.get("type", "") or "").strip()
    fichier = str(vers.get("fichier", "") or "").strip()
    dossier = str(vers.get("dossier", "") or "").strip()
    case = str(vers.get("case", "") or "").strip()
    if dossier:
        chemin = REPERTOIRE_OPERATEUR / dossier
        if not chemin.exists():
            return {"cible": "", "label": dossier, "resolu": False, "base": "",
                    "motif": "le DOSSIER cite n existe pas : " + dossier}
        return {"cible": "PIECE-" + dossier.strip("/").replace("/", "-"),
                "label": dossier, "resolu": True, "motif": "", "base": "operateur"}
    if not fichier:
        return {"cible": "", "label": type_cible, "resolu": True, "motif": "",
                "base": ""}
    # LES DEUX BASES sont essayees (mesure : les deux formes existent), celle du
    # type cite d abord. On ne devine pas : on cherche, et on DIT ou on a trouve.
    bases = BASES_RENVOI if type_cible != "theme" else tuple(reversed(BASES_RENVOI))
    chemin, base_servie = None, ""
    for base in bases:
        candidat = Path(base) / fichier
        if candidat.is_file():
            chemin, base_servie = candidat, Path(base).name
            break
    etiquette = fichier.split("/")[-1] + ((" > " + case) if case else "")
    if chemin is None:
        return {"cible": "", "label": etiquette, "resolu": False, "base": "",
                "motif": ("le FICHIER cite n existe pas : " + fichier + " (essaye sous "
                          + ", ".join(str(base) for base in bases) + ")")}
    if case:
        try:
            texte = chemin.read_text(encoding="utf-8", errors="replace")
        except OSError:
            texte = ""
        if case not in texte:
            return {"cible": "", "label": etiquette, "resolu": False, "base": base_servie,
                    "motif": ("la CASE citee est INTROUVABLE dans " + fichier + " : " + case)}
    return {"cible": "PIECE-" + fichier.replace("/", "-").replace(".", "-"),
            "label": etiquette, "resolu": True, "motif": "", "base": base_servie}


def juger_index(index):
    """(incoherences, ancres) de l INDEX du parcours : fichiers, doublons, orphelins."""
    incoherences, ancres = [], {}
    entrees = index.get("parcours", []) if isinstance(index, dict) else []
    vues = set()
    for entree in entrees:
        nom = str(entree.get("theme", ""))
        if nom in vues:
            incoherences.append(_incoherence(
                "nom-double", "le theme " + nom + " est liste DEUX fois (ordre "
                + str(entree.get("ordre", "?")) + ")", "theme:" + nom))
        vues.add(nom)
        fichier = str(entree.get("fichier", ""))
        if not (REPERTOIRE_OPERATEUR / "parcours" / fichier).is_file():
            incoherences.append(_incoherence(
                "fichier-absent", "le theme " + nom + " (ordre "
                + str(entree.get("ordre", "?")) + ") pointe vers un fichier ABSENT : "
                + fichier, "theme:" + nom))
    listes = {str(entree.get("fichier", "")).split("/")[-1] for entree in entrees}
    for nom_fichier in sorted(lire_themes()):
        if nom_fichier not in listes:
            incoherences.append(_incoherence(
                "theme-orphelin", "le theme " + nom_fichier + " existe sur le disque et"
                " n est PAS liste dans l index : il est invisible", "orphelin:" + nom_fichier))
    return incoherences, ancres


def juger_theme(theme, nom_theme):
    """(renvois, incoherences, ancres) d UN theme : ses renvois et sa fin."""
    renvois, incoherences, ancres = {}, [], {}
    for rang, redirect in enumerate(theme.get("redirects", []), 1):
        cle = "case:" + nom_theme + ":" + str(rang)
        resolution = resoudre_renvoi(redirect.get("vers"), nom_theme=nom_theme)
        renvois[rang] = resolution
        if not resolution.get("resolu"):
            incoherences.append(_incoherence(
                "renvoi-casse", "la case " + str(rang) + " du theme " + nom_theme
                + " renvoie ailleurs et " + str(resolution.get("motif", "")), cle))
    fin = theme.get("fin", {}) if isinstance(theme, dict) else {}
    case_fin = fin.get("case") if isinstance(fin, dict) else None
    if case_fin:
        fins = charger_json(CHEMIN_FINS) or {}
        connues = {str(candidat.get("case", "")) for candidat in (fins.get("fins") or [])}
        if str(case_fin) not in connues:
            incoherences.append(_incoherence(
                "fin-inconnue", "le theme " + nom_theme + " se termine sur la case "
                + str(case_fin) + ", qui n est PAS declaree dans " + str(CHEMIN_FINS),
                "fin:" + nom_theme))
    return renvois, incoherences, ancres


def incoherences_parcours(index, theme=None, nom_theme=""):
    """(incoherences, ancres) : l INDEX toujours, et UN theme quand il est vise."""
    incoherences, ancres = juger_index(index)
    if theme is not None:
        _, celles_du_theme, ancres_theme = juger_theme(theme, nom_theme)
        incoherences.extend(celles_du_theme)
        ancres.update(ancres_theme)
    return incoherences, ancres


def incoherences_vivier(donnees, categories=None):
    """(incoherences, ancres) du vivier : ids, categories FERMEES, doublons, buts vides."""
    if categories is None:
        _, categories = domicile_vivier()
    incoherences, ancres = [], {}
    vus = set()
    for theme in donnees.get("themes", []) if isinstance(donnees, dict) else []:
        identifiant = str(theme.get("id", ""))
        nom = str(theme.get("nom", ""))
        cle = "theme:" + nom.upper()
        if not MOTIF_ID_VIVIER.match(identifiant):
            incoherences.append(_incoherence(
                "id-invalide", "le theme " + nom + " porte un id hors forme (TH-NNN) : "
                + repr(identifiant), "id:" + identifiant))
        if nom in vus:
            incoherences.append(_incoherence(
                "nom-double", "le theme " + nom + " est declare DEUX fois", cle))
        vus.add(nom)
        if categories and str(theme.get("categorie", "")) not in categories:
            incoherences.append(_incoherence(
                "categorie-inconnue", "le theme " + nom + " porte une categorie hors de"
                " la liste FERMEE : " + repr(theme.get("categorie", "")), cle))
        if not str(theme.get("but", "")).strip():
            incoherences.append(_incoherence(
                "but-vide", "le theme " + nom + " n a AUCUN but", cle))
    return incoherences, ancres
