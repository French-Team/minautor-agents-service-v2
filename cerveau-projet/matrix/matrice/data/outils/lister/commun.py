"""Fonctions communes de l'outil lister : perimetre, tri mtime, filtre.

Chaque fonction fait UNE chose (convention-architecture-outils).
"""
import fnmatch
from pathlib import Path

from constants import (
    ALLOWLIST_PREFIXES,
    ALLOWLIST_RACINE,
    RACINE,
    REPERTOIRE_MATRIX,
    ZONES_INVISIBLES,
)


def dans_perimetre(chemin_relatif):
    """True si le chemin est listable (dans matrix/ ou allowlist racine)."""
    brut = str(chemin_relatif).replace("\\", "/").strip()
    if not brut:
        return False
    while brut.startswith("./"):
        brut = brut[2:]
    while brut.startswith("/"):
        brut = brut[1:]
    nom = brut.split("/")[-1]
    if "/" not in brut and (nom in ALLOWLIST_RACINE or any(nom.startswith(p) for p in ALLOWLIST_PREFIXES)):
        return True
    if brut.startswith("matrix/") or brut.startswith("cerveau-projet/matrix/"):
        return True
    try:
        p = (RACINE / brut).resolve()
        for base in (RACINE / "matrix", RACINE / "cerveau-projet" / "matrix"):
            if base.is_dir():
                try:
                    if str(p).startswith(str(base.resolve())):
                        return True
                except OSError:
                    continue
        return str(p).startswith(str(REPERTOIRE_MATRIX.resolve()))
    except (OSError, RuntimeError):
        return False


def resoudre_chemin(chemin_relatif):
    """Retourne le Path absolu (depuis RACINE)."""
    brut = str(chemin_relatif).strip()
    p = (RACINE / brut).resolve()
    return p


def est_zone_invisible(path_absolu):
    """True si path contient une zone L-016 invisible."""
    parts = path_absolu.parts if hasattr(path_absolu, "parts") else str(path_absolu).replace("\\", "/").split("/")
    for zone in ZONES_INVISIBLES:
        if zone in parts:
            return True
    # Check string fallback
    s = str(path_absolu).replace("\\", "/")
    for zone in ZONES_INVISIBLES:
        if "/" + zone + "/" in s or s.endswith("/" + zone):
            return True
    return False


def lister_dossier(chemin_relatif, filtre, recursif, inclure_invisible=False):
    """Liste un dossier (perimetre verifie). Retourne (fichiers, dossiers, code, msg)."""
    if not dans_perimetre(chemin_relatif):
        return [], [], 2, "REFUS : hors perimetre lecture (matrix/ seul, allowlist AGENTS.md/demarrer-*.md) : " + chemin_relatif
    dossier_absolu = resoudre_chemin(chemin_relatif)
    if not dossier_absolu.exists():
        return [], [], 1, "Dossier introuvable : " + chemin_relatif
    if not dossier_absolu.is_dir():
        return [], [], 1, "N'est pas un dossier : " + chemin_relatif

    pattern = filtre.strip() if filtre else "*"

    fichiers = []
    dossiers = []

    try:
        if recursif:
            # Recursif : rglob
            for p in dossier_absolu.rglob(pattern):
                if "__pycache__" in p.parts or ".git" in p.parts:
                    continue
                if not inclure_invisible and est_zone_invisible(p):
                    continue
                if p.is_file():
                    fichiers.append(p)
                elif p.is_dir():
                    dossiers.append(p)
            # Aussi lister les dossiers meme si pattern ne match pas les dossiers (glob pattern matche fichiers)
            # Pour recursif avec filtre, on liste dossiers via iteration separee si filtre contient *
            if pattern != "*":
                for p in dossier_absolu.rglob("*"):
                    if p.is_dir() and "__pycache__" not in p.parts and ".git" not in p.parts:
                        if not inclure_invisible and est_zone_invisible(p):
                            continue
                        if p not in dossiers:
                            # dossiers deja mais on ajoute si non deja
                            dossiers.append(p)
        else:
            # Non recursif : glob direct
            for p in dossier_absolu.glob(pattern):
                if "__pycache__" in p.parts or ".git" in p.parts:
                    continue
                if not inclure_invisible and est_zone_invisible(p):
                    continue
                if p.is_file():
                    fichiers.append(p)
                elif p.is_dir():
                    dossiers.append(p)
            # Si filtre, on veut aussi lister dossiers/fichiers non filtres ? Non, filtre s'applique
            # Mais pour lister simple sans filtre, on veut tout
            if not filtre:
                # Deja fait avec pattern * (tout)
                pass
    except OSError as e:
        return [], [], 1, "Erreur listage : " + str(e)

    # Si pas recursif et filtre vide, on a tout ; si filtre, on filtre par fnmatch sur nom
    # rglob/glob deja filtre, mais pour securite, on re-filtre si pattern contient slash
    # Tri deterministe : mtime puis nom
    def cle(p):
        try:
            return (p.stat().st_mtime, str(p))
        except OSError:
            return (0, str(p))

    fichiers.sort(key=cle)
    dossiers.sort(key=cle)
    return fichiers, dossiers, 0, ""


def extraire_options(arguments, noms_connus):
    """Extrait --nom valeur et flags --recursif/--json sans valeur."""
    options = {}
    index = 0
    while index < len(arguments):
        morceau = arguments[index]
        if morceau.startswith("--") and morceau[2:] in noms_connus:
            nom = morceau[2:]
            if nom in ("recursif", "json"):
                options[nom] = "1"
                index += 1
            elif index + 1 < len(arguments):
                options[nom] = arguments[index + 1]
                index += 2
            else:
                options[nom] = ""
                index += 1
        else:
            index += 1
    return options
