"""Fonctions communes de l'outil lire : perimetre, lecture, SHA, tranche.

Chaque fonction fait UNE chose (convention-architecture-outils).
Lecture seule : jamais d'ecriture.
"""
import hashlib
import fnmatch
from pathlib import Path

from constants import (
    ALLOWLIST_PREFIXES,
    ALLOWLIST_RACINE,
    ENCODAGE,
    RACINE,
    REPERTOIRE_MATRIX,
    TAILLE_BLOC_LECTURE,
)


def dans_perimetre(chemin_relatif):
    """True si le chemin est lisible (dans matrix/ ou allowlist racine)."""
    brut = str(chemin_relatif).replace("\\", "/").strip()
    if not brut:
        return False
    # Nettoie ./ et // initiaux.
    while brut.startswith("./"):
        brut = brut[2:]
    while brut.startswith("/"):
        brut = brut[1:]
    # Allowlist racine : AGENTS.md et demarrer-*.md (a la racine du workspace).
    nom = brut.split("/")[-1]
    if "/" not in brut and (nom in ALLOWLIST_RACINE or any(nom.startswith(p) for p in ALLOWLIST_PREFIXES)):
        return True
    # matrix/ (avec ou sans prefixe cerveau-projet/).
    if brut.startswith("matrix/") or brut.startswith("cerveau-projet/matrix/"):
        return True
    # Chemin deja sous REPERTOIRE_MATRIX (absolu ou relatif resolu).
    try:
        p = (RACINE / brut).resolve()
        return str(p).startswith(str(REPERTOIRE_MATRIX.resolve()))
    except (OSError, RuntimeError):
        return False


def resoudre_chemin(chemin_relatif):
    """Retourne le Path absolu du fichier demande (depuis RACINE)."""
    brut = str(chemin_relatif).strip()
    p = (RACINE / brut).resolve()
    return p


def calculer_sha256(chemin_absolu):
    """SHA-256 hex du fichier (lecture binaire, blocs)."""
    h = hashlib.sha256()
    with open(chemin_absolu, "rb") as flux:
        for bloc in iter(lambda: flux.read(TAILLE_BLOC_LECTURE), b""):
            h.update(bloc)
    return h.hexdigest()


def lire_contenu(chemin_absolu):
    """Lecture texte du fichier. Retourne (texte, encodage, bom, fins)."""
    raw = chemin_absolu.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    if b"\x00" in raw[:4096]:
        raise UnicodeDecodeError("utf-8", raw, 0, 1, "octets nuls (binaire ?)")
    # Detecte fins de ligne dominantes (avant decode).
    crlf = raw.count(b"\r\n")
    lf = raw.count(b"\n") - crlf
    fins = "CRLF" if crlf > lf else "LF" if lf > 0 else "aucune"
    # Decode strict (echec = signal, pas de silent replace).
    texte = raw.decode(ENCODAGE)
    if bom:
        texte = texte.lstrip("\ufeff")
    return texte, ENCODAGE, bom, fins


def decoupage_lignes(texte, tranche):
    """Applique --lignes debut:fin (1-indexe, inclusif). Retourne (lignes, total, lu)."""
    lignes = texte.splitlines()
    total = len(lignes)
    if not tranche:
        return lignes, total, total
    # Parse debut:fin.
    tranche = tranche.strip()
    if ":" not in tranche:
        raise ValueError("Format --lignes attendu : debut:fin (ex 1:200)")
    debut_s, fin_s = tranche.split(":", 1)
    try:
        debut = int(debut_s) if debut_s.strip() else 1
        fin = int(fin_s) if fin_s.strip() else total
    except ValueError:
        raise ValueError("Format --lignes attendu : debut:fin (entiers)")
    if debut < 1:
        debut = 1
    if fin < debut:
        raise ValueError("--lignes : fin < debut")
    if debut > total:
        return [], total, 0
    if fin > total:
        fin = total
    return lignes[debut - 1:fin], total, fin - debut + 1


def lister_fichiers(dossier_absolu, filtre, recursif):
    """Liste les fichiers d'un dossier (perimetre deja verifie)."""
    if not dossier_absolu.is_dir():
        raise NotADirectoryError(str(dossier_absolu) + " n'est pas un dossier")
    pattern = filtre.strip() if filtre else "*"
    fichiers = []
    it = dossier_absolu.rglob(pattern) if recursif else dossier_absolu.glob(pattern)
    for p in it:
        if p.is_file() and "__pycache__" not in p.parts and ".git" not in p.parts:
            fichiers.append(p)
    # Tri deterministe : mtime croissant puis nom.
    def cle(p):
        try:
            return (p.stat().st_mtime, str(p))
        except OSError:
            return (0, str(p))
    fichiers.sort(key=cle)
    return fichiers


def extraire_options(arguments, noms_connus):
    """Extrait les options --nom valeur (forme seulement). Flag --recursif et --hash sans valeur."""
    options = {}
    index = 0
    while index < len(arguments):
        morceau = arguments[index]
        if morceau.startswith("--") and morceau[2:] in noms_connus:
            nom = morceau[2:]
            if nom in ("recursif", "hash"):
                options[nom] = "1"
                index += 1
            elif index + 1 < len(arguments):
                options[nom] = arguments[index + 1]
                index += 2
            else:
                index += 1
        else:
            index += 1
    return options
