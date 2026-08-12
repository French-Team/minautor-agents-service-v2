#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
# =============================================================================
# generateurs-regenerer-catalogue.py
#
# Regenerer / synchroniser le catalogue-commandes.json du generateur de commandes.
#
# POURQUOI :
#   - Le catalogue est un fichier DERIVE : chaque commande (modele) doit
#     correspondre a un outil reel de agents/tools/.
#   - Lors de la piste A, une regeneration a ete faite avec un script
#     TEMPORAIRE qui a capture des fragments d'aide comme descriptions
#     (63 entrees cosmetiques sur 105, corrigees a la main).
#   - Ce script est l'outil PERMANENT pour regenerer sans re-corriger.
#
# COMMENT :
#   - Mode par defaut (SYNCHRONISATION) : lit le catalogue existant, preserve
#     les entrees deja presentes (descriptions corrigees), et AJOUTE les outils
#     reels manquants (description extraite de l'en-tete du .py).
#   - Option --force : reconstruit tout depuis les outils reels.
#   - Option --dry-run : affiche ce qui serait fait sans rien ecrire.
#
# SOURCE DESCRIPTIONS :
#   Format A (docstring) :   """\n nom.py\n\n Description...\n """
#   Format B (commentaires): # nom.py\n # Description...   (outils convertis)
#   Translitteration ASCII (NFKD), limite ~90 caracteres, jointure des phrases.
#
# REGLES DE SECURITE :
#   - JAMAIS git checkout/restore/reset sur un fichier non commite.
#   - GARDE-FOU : verification des cles dupliquees dans parametres avant
#     toute ecriture (collision de placeholder) - refus si doublon.
#   - ECRITURE : indentation 2 espaces + LF pur (standard projet,
#     .gitattributes eol=lf) - piege CRLF parasite evite.
#   - ASCII strict sur toute sortie.
# =============================================================================

import io
import json
import os
import re
import subprocess
import sys
import unicodedata

VERSION = "1.1.1"
STATUT = "ebauche"

CATALOGUE = "cerveau-projet/agents/tools/generateurs/generateurs-commande/catalogue-commandes.json"
RACINE_TOOLS = "cerveau-projet/agents/tools"

# Les 13 commandes ORIGINALES (liste de reference : ne jamais les regenerer)
COMMANDES_ORIGINALES = [
    "activer-sidentifier", "activer-activer", "activer-reactiver", "activer-sessions",
    "generer-squelette-pense-bete", "remplir-pense-bete", "corriger-accents",
    "remplacer-texte", "audit-general", "valider-nommage-recursif",
    "combos-valider-cerveau", "combos-corriger-non-ascii", "detecter-impacts",
]

# Entrees SPECIALES (modele manuel - parsing d'aide imperfectible)
ENTREES_SPECIALES = {
    "generateurs-carte": {
        "nom": "generateurs-carte",
        "description": "Creer, analyser ou dupliquer une carte de decision (parcours JSON)",
        "interpreteur": "python3",
        "script": "cerveau-projet/agents/tools/generateurs/generateurs-carte/generateurs-carte.py",
        "modele": "{action} {fichier}",
        "parametres": [
            {"cle": "action", "question": "Action (creer, analyser, dupliquer) ?", "type": "choix",
             "choix": ["creer", "analyser", "dupliquer"], "obligatoire": True},
            {"cle": "fichier", "question": "Chemin du parcours JSON ?", "type": "texte", "obligatoire": True},
        ],
    },
    "combos-moteur": {
        "nom": "combos-moteur",
        "description": "Executer un combo declaratif (definition-combo.json) via le moteur",
        "interpreteur": "python3",
        "script": "cerveau-projet/agents/tools/combos/combos-moteur/combos-moteur.py",
        "modele": "{combo}",
        "parametres": [
            {"cle": "combo", "question": "Chemin du definition-combo.json a executer ?",
             "type": "texte", "obligatoire": True},
        ],
    },
    "verifier-restauration-sure": {
        "nom": "verifier-restauration-sure",
        "description": "Detecter les fichiers non commites avant restauration git (regle Restauration securisee)",
        "interpreteur": "python3",
        "script": "cerveau-projet/agents/tools/verifier/verifier-restauration-sure/verifier-restauration-sure.py",
        "modele": "--fichier {fichier}",
        "parametres": [
            {"cle": "fichier", "question": "Chemin du fichier a verifier (optionnel - mode global si vide) ?",
             "type": "texte", "obligatoire": False, "defaut": ""},
        ],
    },
}

MOTS_META = ("version", "statut", "identite", "usage", "options", "arguments", "exemples",
             "synopsis", "description :", "auteur", "date", "raccourci")


# ---------------------------------------------------------------------------
# Extraction de la description depuis l'en-tete du .py
# ---------------------------------------------------------------------------

def ascii_only(texte):
    """Translitteration ASCII stricte (regle immuable : aucun accent)."""
    norm = unicodedata.normalize("NFKD", texte)
    return norm.encode("ascii", "ignore").decode("ascii").strip()


def ligne_est_description(ligne):
    """Une ligne est une vraie description si elle n'est ni meta ni trop courte."""
    l = ligne.strip().lstrip("#").strip()
    if not l or len(l) < 12:
        return None
    if l.lower().startswith(MOTS_META):
        return None
    return l


def limiter(texte, max_len=90):
    """Limite a max_len caracteres en coupant a la derniere phrase."""
    if len(texte) <= max_len:
        return texte
    coupe = texte[:max_len]
    derniere_phrase = max(coupe.rfind(". "), coupe.rfind(", "), coupe.rfind(" - "))
    if derniere_phrase > 40:
        return coupe[:derniere_phrase + 1]
    return coupe


def extraire_description(chemin_abs, nom_script):
    """Extrait la description depuis l'en-tete du .py (2 formats).
    Joint les lignes descriptives consecutives (phrase coupee par ':' ou ',') jusqu'a ~90 car."""
    try:
        with io.open(chemin_abs, encoding="utf-8", errors="replace") as fh:
            txt = fh.read()
    except Exception:
        return None
    lignes = txt.split("\n")
    base = nom_script.replace(".py", "").replace(".sh", "")

    def est_ligne_nom(l):
        return base in l and (".py" in l or ".sh" in l)

    def joindre(seq):
        """Joint les lignes descriptives jusqu'a une phrase (~90 car)."""
        parties = []
        for l2 in seq:
            st = l2.strip()
            if not st:
                if parties:
                    break
                continue
            bas = st.lower()
            if bas.startswith(("usage", "options", "arguments", "exemples", "synopsis")):
                break
            d = ligne_est_description(st)
            if not d:
                break
            parties.append(d)
            if len(" ".join(parties)) > 90:
                break
        if not parties:
            return None
        return limiter(ascii_only(" ".join(parties)))

    # --- Format B : commentaires (# nom.py puis # Description) ---
    for i, l in enumerate(lignes[:15]):
        if l.strip().startswith("#") and est_ligne_nom(l):
            d = joindre(lignes[i + 1:i + 6])
            if d:
                return d
    # --- Format A : docstring triple-quote ---
    m = re.search(r'"""\n(.*?)"""', txt, re.DOTALL)
    if m:
        contenu = m.group(1)
        lignes_doc = contenu.split("\n")
        for idx, l in enumerate(lignes_doc):
            if est_ligne_nom(l):
                return joindre(lignes_doc[idx + 1:idx + 10])
        # pas de ligne nom : prendre la 1re description du docstring
        return joindre(lignes_doc[:10])
    return None


# ---------------------------------------------------------------------------
# Parsing de l'aide (usage:) pour le modele et les parametres
# ---------------------------------------------------------------------------

def parser_aide(chemin_abs):
    """Lance 'python3 outil --aide' et parse usage: -> (modele, parametres)."""
    try:
        proc = subprocess.run([sys.executable, chemin_abs, "--aide"],
                              capture_output=True, text=True, timeout=20,
                              encoding="utf-8", errors="replace")
        sortie = proc.stdout or ""
    except Exception:
        return None, []
    lignes = sortie.split("\n")
    usage_lignes = []
    en_usage = False
    for l in lignes:
        if l.strip().startswith("usage:") or l.strip().startswith("Usage:"):
            en_usage = True
            usage_lignes.append(l)
            continue
        if en_usage:
            if l.strip() and (l.startswith(" ") or l.startswith("\t")):
                usage_lignes.append(l)
            else:
                break
    if not usage_lignes:
        return None, []
    usage = " ".join(l.strip() for l in usage_lignes)
    usage = re.sub(r"^[Uu]sage:\s*", "", usage)
    usage = re.sub(r"\S+\.py\s*", "", usage, count=1)
    tokens = usage.split()
    modeles = []
    parametres = []
    for tok in tokens:
        m_flag = re.match(r"\[?--([a-z0-9-]+)", tok)
        if m_flag:
            cle = m_flag.group(1)
            if cle not in [p["cle"] for p in parametres]:
                parametres.append({
                    "cle": cle,
                    "question": "Valeur pour %s ?" % cle.replace("-", "_"),
                    "type": "texte", "obligatoire": False, "defaut": "",
                })
            modeles.append("--" + cle + " {" + cle.replace("-", "_") + "}")
            continue
        m_pos = re.match(r"\[?([A-Z_]+)\]?", tok)
        if m_pos:
            cle = m_pos.group(1).lower()
            if cle not in [p["cle"] for p in parametres]:
                parametres.append({
                    "cle": cle,
                    "question": "Valeur pour %s ?" % cle,
                    "type": "texte", "obligatoire": True,
                })
            modeles.append("{" + cle + "}")
    return " ".join(modeles), parametres


# ---------------------------------------------------------------------------
# Scan des outils reels
# ---------------------------------------------------------------------------

def scan_outils():
    """Trouve les outils reels : agents/tools/<cat>/<outil>/<outil>.py"""
    outils = []
    for racine, dossiers, fichiers in os.walk(RACINE_TOOLS):
        if "__pycache__" in racine or "/tester/" in racine or "/spec/" in racine:
            continue
        rel = os.path.relpath(racine, RACINE_TOOLS)
        parts = rel.split(os.sep)
        if len(parts) != 2:
            continue
        cat, outil_dir = parts
        if cat in ("tester", "combos", "templates") or outil_dir in ("spec",):
            continue
        if outil_dir in ("outil-template", "generateurs-regenerer-catalogue"):
            continue
        py = os.path.join(racine, outil_dir + ".py")
        if os.path.exists(py):
            outils.append({
                "chemin": os.path.join(RACINE_TOOLS, rel, outil_dir + ".py"),
                "chemin_abs": py,
                "nom": outil_dir,
            })
    return outils


# ---------------------------------------------------------------------------
# Garde-fou : cles dupliquees
# ---------------------------------------------------------------------------

def verifier_cles_dupliquees(commandes):
    """GARDE-FOU : detecte les cles dupliquees dans parametres (collision de
    placeholder : deux parametres meme cle = meme valeur generee 2 fois).
    Retourne [(nom, [cles_dupliquees]), ...]."""
    defauts = []
    for e in commandes:
        cles = [p.get("cle") for p in e.get("parametres", []) if p.get("cle")]
        doublons = sorted({c for c in cles if cles.count(c) > 1})
        if doublons:
            defauts.append((e["nom"], doublons))
    return defauts


def chemin_catalogue():
    """Chemin du catalogue : option --catalogue <chemin> (tests) ou defaut."""
    for i, a in enumerate(sys.argv):
        if a == "--catalogue" and i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return CATALOGUE


def charger_catalogue(catalogue):
    """Charge et parse le catalogue JSON. Message d erreur clair si le fichier
    est introuvable ou le JSON invalide (jamais de traceback brut).
    Retourne le dict, ou None si erreur (message deja affiche sur stderr)."""
    try:
        with io.open(catalogue, encoding="utf-8", newline="") as fh:
            txt = fh.read()
    except OSError as e:
        print("ERREUR: catalogue illisible : %s (%s)" % (catalogue, e), file=sys.stderr)
        return None
    # Normaliser LF en memoire (piege CRLF parasite) puis ecrire en LF pur (standard projet)
    txt_normalise = txt.replace("\r\n", "\n")
    try:
        return json.loads(txt_normalise)
    except ValueError as e:
        print("ERREUR: catalogue invalide (JSON) : %s (%s)" % (catalogue, e), file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    dry = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    if "--version" in sys.argv:
        print("regenerer-catalogue v%s (%s)" % (VERSION, STATUT))
        return
    catalogue = chemin_catalogue()

    d = charger_catalogue(catalogue)
    if d is None:
        sys.exit(1)
    commandes_existantes = {e["nom"]: e for e in d["commandes"]}
    outils = scan_outils()

    a_ajouter = []
    a_preserver = []
    for outil in outils:
        nom = outil["nom"]
        if nom in COMMANDES_ORIGINALES or nom in ENTREES_SPECIALES:
            continue
        if nom in commandes_existantes:
            a_preserver.append(nom)
            continue
        # Nouvel outil : construire l'entree
        desc = extraire_description(outil["chemin_abs"], nom)
        modele, parametres = parser_aide(outil["chemin_abs"])
        if not desc:
            desc = "Outil %s du cerveau-projet" % nom
        if not modele:
            modele = "{chemin}"
            parametres = [{"cle": "chemin", "question": "Valeur pour chemin ?",
                           "type": "texte", "obligatoire": True}]
        a_ajouter.append({
            "nom": nom,
            "description": desc,
            "interpreteur": "python3",
            "script": outil["chemin"],
            "modele": modele,
            "parametres": parametres,
        })

    if dry:
        print("=== DRY-RUN : %d outils scannes | %d existants preserves | %d a ajouter ==="
              % (len(outils), len(a_preserver), len(a_ajouter)))
        for e in a_ajouter[:10]:
            print("  + %-32s | %s" % (e["nom"], e["description"][:60]))
        defauts = verifier_cles_dupliquees(d["commandes"])
        if defauts:
            print("=== GARDE-FOU : cles dupliquees dans parametres (%d entree(s)) ==="
                  % len(defauts))
            for nom, cles in defauts:
                print("  ERREUR %-32s cles dupliquees: %s" % (nom, ", ".join(cles)))
        else:
            print("GARDE-FOU : 0 cle dupliquee (OK)")
        if force:
            print("(--force : reconstruirait depuis zero)")
        return

    # Application
    if not force:
        # Synchronisation : preserver l'existant, ajouter les manquants
        d["commandes"].extend(a_ajouter)
        d["commandes"].sort(key=lambda e: e["nom"])
        n_ajoutes = len(a_ajouter)
    else:
        # Force : reconstruire (originales + speciales + tous les outils)
        commandes = []
        for nom_orig in COMMANDES_ORIGINALES:
            if nom_orig in commandes_existantes:
                commandes.append(commandes_existantes[nom_orig])
        for nom_spec, entree in ENTREES_SPECIALES.items():
            commandes.append(entree)
        commandes.extend(a_ajouter)
        d["commandes"] = commandes
        d["commandes"].sort(key=lambda e: e["nom"])
        n_ajoutes = len(a_ajouter)

    # GARDE-FOU : refuser d ecrire si des cles sont dupliquees
    defauts = verifier_cles_dupliquees(d["commandes"])
    if defauts:
        print("=== GARDE-FOU : cles dupliquees dans parametres (%d entree(s)) ==="
              % len(defauts))
        for nom, cles in defauts:
            print("  ERREUR %-32s cles dupliquees: %s" % (nom, ", ".join(cles)))
        print("Refus d ecrire le catalogue : corriger les entrees fautives avant regeneration.")
        sys.exit(1)

    resultat = json.dumps(d, ensure_ascii=True, indent=2) + "\n"
    with io.open(catalogue, "w", encoding="utf-8", newline="") as fh:
        fh.write(resultat)
    print("=== APPLIQUE : %d outils ajoutes (total %d commandes) ==="
          % (n_ajoutes, len(d["commandes"])))
    for e in a_ajouter[:8]:
        print("  + %-32s | %s" % (e["nom"], e["description"][:55]))


if __name__ == "__main__":
    main()
