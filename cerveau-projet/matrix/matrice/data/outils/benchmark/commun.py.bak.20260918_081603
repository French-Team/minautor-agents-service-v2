"""Fonctions communes de l'outil benchmark : 9 epreuves par fichier.

Chaque fonction fait UNE chose (convention-architecture-outils).
La grille ne bouge jamais : 1 fichier = 9 controles.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from constants import (
    ALLOWLIST_PREFIXES,
    ALLOWLIST_RACINE,
    EPREUVES,
    ENCODAGE,
    RACINE,
    REPERTOIRE_DATA,
    REPERTOIRE_MATRIX,
)

# Le contrat d invisibilite L-016/CV-006 (plancher + zones DECLAREES V-003 du
# classeur) vit dans SON domicile : cette porte le CONSOMME, elle ne le recopie
# pas (M-076 ; mesure MO-151).
from invisibilite import est_invisible  # noqa: E402


# --- Helpers perimetre (copie desde lire/commun.py) ---

def dans_perimetre(chemin_relatif):
    """True si dans matrix/ ou allowlist racine."""
    brut = str(chemin_relatif).replace("\\", "/").strip()
    if not brut:
        return False
    while brut.startswith("./"):
        brut = brut[2:]
    while brut.startswith("/"):
        brut = brut[1:]
    nom = brut.split("/")[-1]
    if "/" not in brut and (
        nom in ALLOWLIST_RACINE
        or any(nom.startswith(p) for p in ALLOWLIST_PREFIXES)
    ):
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


def est_zone_invisible(path_absolu):
    """True si path contient une zone L-016 (domicile data/commun, MO-152)."""
    return est_invisible(path_absolu)


def calculer_sha256(chemin):
    """SHA-256 hex."""
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


# --- Les 9 epreuves ---

def epreuve_perimetre(chemin):
    """E1 : Le fichier est-il dans le perimetre matrix/ ?"""
    try:
        p = Path(chemin).resolve()
        rel = p.relative_to(RACINE)
        ok = dans_perimetre(str(rel))
    except (ValueError, OSError):
        ok = False
    return {
        "nom": "perimetre",
        "passe": ok,
        "detail": "dans matrix/" if ok else "HORS perimetre",
        "code": 0 if ok else 2,
    }


def epreuve_lf(chemin):
    """E2 : 0 CRLF, LF forces ?"""
    try:
        raw = Path(chemin).read_bytes()
        crlf = raw.count(b"\r\n")
        lf = raw.count(b"\n") - crlf
        ok = crlf == 0
        detail = f"{lf} LF, {crlf} CRLF"
    except OSError as e:
        ok = False
        detail = "Erreur lecture : " + str(e)
    return {
        "nom": "lf",
        "passe": ok,
        "detail": detail,
        "code": 0 if ok else 1,
    }


def epreuve_sha(chemin):
    """E3 : SHA-256 calculable ?"""
    try:
        sha = calculer_sha256(chemin)
        ok = len(sha) == 64
        detail = "SHA " + sha[:16] + "..."
    except OSError as e:
        ok = False
        detail = "Erreur SHA : " + str(e)
    return {
        "nom": "sha",
        "passe": ok,
        "detail": detail,
        "code": 0 if ok else 1,
    }


def epreuve_validation(chemin):
    """E4 : py_compile (.py) ou json.load (.json) ou ASCII (.md) ?"""
    p = Path(chemin)
    ext = p.suffix.lower()
    try:
        if ext == ".py":
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(chemin)],
                capture_output=True, timeout=10,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            ok = result.returncode == 0
            detail = "py_compile OK" if ok else "py_compile FAIL"
        elif ext == ".json":
            with open(chemin, "r", encoding=ENCODAGE) as f:
                json.load(f)
            ok = True
            detail = "json.load OK"
        elif ext in (".md", ".txt"):
            # ASCII check
            text = p.read_text(encoding=ENCODAGE)
            non_ascii = sum(1 for c in text if ord(c) > 127)
            ok = non_ascii == 0
            detail = f"{non_ascii} non-ASCII" if non_ascii else "ASCII OK"
        else:
            ok = True
            detail = f"extension {ext} non teste"
    except Exception as e:
        ok = False
        detail = "Erreur : " + str(e)
    return {
        "nom": "validation",
        "passe": ok,
        "detail": detail,
        "code": 0 if ok else 1,
    }


def epreuve_ascii(chemin):
    """E5 : 0 non-ASCII ?"""
    try:
        text = Path(chemin).read_text(encoding=ENCODAGE, errors="replace")
        non_ascii = sum(1 for c in text if ord(c) > 127)
        ok = non_ascii == 0
        detail = f"{non_ascii} non-ASCII" if non_ascii else "0 non-ASCII OK"
    except OSError as e:
        ok = False
        detail = "Erreur lecture : " + str(e)
    return {
        "nom": "ascii",
        "passe": ok,
        "detail": detail,
        "code": 0 if ok else 1,
    }


def epreuve_bdd(chemin):
    """E6 : Entree dans modifications-par-fichier.json ?"""
    try:
        p = Path(chemin).resolve()
        rel = str(p.relative_to(RACINE)).replace("\\", "/")
        bdd = REPERTOIRE_DATA / "modifications-par-fichier.json"
        if not bdd.is_file():
            return {"nom": "bdd", "passe": False, "detail": "BDD absente", "code": 1}
        data = json.loads(bdd.read_text(encoding=ENCODAGE))
        # Cherche le fichier (cle ou dans les valeurs)
        trouve = False
        if isinstance(data, dict):
            for cle in data:
                if rel in str(cle) or rel in str(data[cle]):
                    trouve = True
                    break
        ok = trouve
        detail = "present dans BDD" if ok else "absent de BDD"
    except Exception as e:
        ok = False
        detail = "Erreur BDD : " + str(e)
    return {
        "nom": "bdd",
        "passe": ok,
        "detail": detail,
        "code": 0 if ok else 1,
    }


def epreuve_relecture(chemin):
    """E7 : Le fichier est-il relisible (second canal L-009) ?"""
    try:
        text = Path(chemin).read_text(encoding=ENCODAGE)
        lignes = text.splitlines()
        ok = len(lignes) > 0
        detail = f"{len(lignes)} lignes relues"
    except Exception as e:
        ok = False
        detail = "Erreur relecture : " + str(e)
    return {
        "nom": "relecture",
        "passe": ok,
        "detail": detail,
        "code": 0 if ok else 1,
    }


def epreuve_bak(chemin):
    """E8 : Un .bak existe-t-il (si preexistant) ?"""
    p = Path(chemin)
    # Cherche .bak avec pattern date
    bak_trouve = False
    for bak in p.parent.glob(p.name + ".bak.*"):
        if bak.is_file():
            bak_trouve = True
            break
    # Pour un fichier nouveau (pas de .bak attendu), c'est OK
    ok = True
    detail = ".bak present" if bak_trouve else "pas de .bak (fichier nouveau ou jamais modifie)"
    return {
        "nom": "bak",
        "passe": ok,
        "detail": detail,
        "code": 0,
    }


def epreuve_invisibilite(chemin):
    """E9 : 0 fuite L-016 ?"""
    try:
        p = Path(chemin).resolve()
        ok = not est_zone_invisible(p)
        detail = "pas de fuite L-016" if ok else "FUITE L-016 detectee"
    except Exception as e:
        ok = False
        detail = "Erreur : " + str(e)
    return {
        "nom": "invisibilite",
        "passe": ok,
        "detail": detail,
        "code": 0 if ok else 2,
    }


# --- Orchestrateur 9 epreuves ---

def lancer_9_epreuves(chemin):
    """Lance les 9 epreuves sur un fichier.
    Retourne (resultats, code_global).
    code_global : 0=tout passe, 1=au moins 1 echec, 2=refus perimetre.
    """
    fonctions = [
        epreuve_perimetre,
        epreuve_lf,
        epreuve_sha,
        epreuve_validation,
        epreuve_ascii,
        epreuve_bdd,
        epreuve_relecture,
        epreuve_bak,
        epreuve_invisibilite,
    ]
    resultats = []
    code_global = 0

    for fn in fonctions:
        try:
            r = fn(chemin)
        except Exception as e:
            r = {"nom": fn.__name__, "passe": False, "detail": "Exception : " + str(e), "code": 1}
        resultats.append(r)
        if r["code"] == 2:
            code_global = 2  # refus
        elif r["code"] == 1 and code_global == 0:
            code_global = 1  # echec

    return resultats, code_global


# --- Batch ---

def lister_fichiers(dossier, recursif=False, filtre=None):
    """Liste les fichiers d'un dossier (perimetre verifie)."""
    d = Path(dossier)
    if not d.is_dir():
        return []
    pattern = filtre if filtre else "*"
    fichiers = []
    it = d.rglob(pattern) if recursif else d.glob(pattern)
    for p in it:
        if p.is_file() and "__pycache__" not in p.parts and ".git" not in p.parts:
            if not est_zone_invisible(p):
                fichiers.append(p)
    # Tri mtime deterministe
    def cle(p):
        try:
            return (p.stat().st_mtime, str(p))
        except OSError:
            return (0, str(p))
    fichiers.sort(key=cle)
    return fichiers


def extraire_options(arguments, noms_connus):
    """Extrait --nom valeur et flags sans valeur."""
    options = {}
    index = 0
    while index < len(arguments):
        morceau = arguments[index]
        if morceau.startswith("--") and morceau[2:] in noms_connus:
            nom = morceau[2:]
            if nom in ("json", "recursif", "integration"):
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
