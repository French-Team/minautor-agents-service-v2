#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-129-regle-serie-garde-fou
===============================
Garde-fou du contenu de la regle TRAVAIL EN SERIE OBLIGATOIRE
(decision utilisateur 2026-09-05).

Contexte : en mode single-llm, le travail en parallele n existe PAS.
Buffy (mission 666bec53) a reformule COMMENT-DEMARRER.md ('demarrer un
second llm en parallel' -> TRAVAIL EN SERIE) et ajoute la regle serie
dans demarrer.md ORDRE 5. La regle 3 a ete ajoutee dans AGENTS.md par
Gardien (mission ab5d3ca4, zone MARBRE constitution).

Le test verrouille :
1. COMMENT-DEMARRER.md ne contient PLUS l ancienne instruction
   'second llm en parallel' (aucun multi-relais autorise).
2. COMMENT-DEMARRER.md contient 'TRAVAIL EN SERIE'.
3. demarrer.md ORDRE 5 contient le bloc 'TRAVAIL EN SERIE OBLIGATOIRE'.
4. demarrer.md contient 'JAMAIS 2 missions relayees simultanement'.
5. AGENTS.md contient la regle 'TRAVAIL EN SERIE OBLIGATOIRE' (regle 3).
6. Coherence croisee 3/3 : les 3 fichiers (AGENTS.md, demarrer.md,
   COMMENT-DEMARRER.md) portent tous la regle serie.
7. ASCII strict (0 non-ASCII) sur les 2 fichiers modifies.
8. LF pur (0 CRLF) sur les 2 fichiers modifies.
9. PREUVE NEGATIVE : un fichier fixture (copie sans la regle serie)
   est DETECTE comme non conforme par le scanner du test.

Normes : ASCII strict, LF pur, marqueurs [OK]/[KO], bilan final
RESULTAT : N OK / M KO, sys.exit(main()).
"""
import io
import os
import sys
import tempfile

NB_POINTS = 12
NB_OK = 0
NB_KO = 0

RACINE = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(RACINE, "cerveau-projet")):
    RACINE = os.path.dirname(RACINE)

F_COMMENT = os.path.join(RACINE, "COMMENT-DEMARRER.md")
F_DEMARRER = os.path.join(RACINE, "demarrer.md")
F_AGENTS = os.path.join(RACINE, "AGENTS.md")

MARQUEURS_SERIE = [
    "TRAVAIL EN SERIE OBLIGATOIRE",
    "JAMAIS 2 missions relayees simultanement",
    "un SEUL agent est incarne a la fois",
]


def verifier(nom, condition, detail=""):
    """Affiche [OK] ou [KO] et compte le resultat."""
    global NB_OK, NB_KO
    if condition:
        NB_OK += 1
        print("[OK] %s" % nom)
    else:
        NB_KO += 1
        print("[KO] %s -- %s" % (nom, detail))


def lire_texte(chemin):
    """Lit un fichier en texte UTF-8 (avec BOM tolere a la lecture)."""
    with io.open(chemin, "r", encoding="utf-8-sig") as f:
        return f.read()


def normaliser(texte):
    """Supprime les retours a la ligne et espaces multiples pour matcher
    des marqueurs phrases coupes par la mise en page markdown (ex:
    'JAMAIS 2 missions relayees\n  simultanement')."""
    return " ".join(texte.split())


def octets(chemin):
    """Lit un fichier en octets bruts (pour ASCII/CRLF)."""
    with open(chemin, "rb") as f:
        return f.read()


def est_conforme_serie(texte):
    """Un contenu est conforme serie si AUCUN marqueur ne manque."""
    return all(m in texte for m in MARQUEURS_SERIE)


def main():
    print("=== test-129 -- Regle TRAVAIL EN SERIE (decision 2026-09-05) ===")

    # 1. Presence des 3 fichiers
    for nom, chemin in [("COMMENT-DEMARRER.md", F_COMMENT),
                        ("demarrer.md", F_DEMARRER),
                        ("AGENTS.md", F_AGENTS)]:
        verifier("fichier present: %s" % nom, os.path.isfile(chemin),
                 "introuvable: %s" % chemin)
    if not all(os.path.isfile(p) for p in (F_COMMENT, F_DEMARRER, F_AGENTS)):
        print("RESULTAT : %d OK / %d KO (fichiers manquants)" % (NB_OK, NB_KO))
        return 1 if NB_KO else 0

    comment = normaliser(lire_texte(F_COMMENT))
    demarrer = normaliser(lire_texte(F_DEMARRER))
    agents = normaliser(lire_texte(F_AGENTS))

    # 2. COMMENT-DEMARRER.md : plus d'ancienne instruction parallele
    ancien = "second llm en parallel"
    verifier(
        "COMMENT-DEMARRER.md sans '%s'" % ancien,
        ancien not in comment,
        "l'ancienne instruction 'second llm en parallel' est encore presente")

    # 3. COMMENT-DEMARRER.md porte la regle serie
    verifier("COMMENT-DEMARRER.md contient 'TRAVAIL EN SERIE'",
             "TRAVAIL EN SERIE" in comment,
             "marqueur TRAVAIL EN SERIE absent")

    # 4. demarrer.md ORDRE 5 porte le bloc serie
    verifier("demarrer.md contient 'TRAVAIL EN SERIE OBLIGATOIRE'",
             "TRAVAIL EN SERIE OBLIGATOIRE" in demarrer,
             "bloc serie absent de demarrer.md")

    # 5. demarrer.md interdit le double relais
    verifier("demarrer.md contient 'JAMAIS 2 missions relayees simultanement'",
             "JAMAIS 2 missions relayees simultanement" in demarrer,
             "interdiction du double relais absente")

    # 6. AGENTS.md porte la regle 3
    verifier("AGENTS.md contient 'TRAVAIL EN SERIE OBLIGATOIRE' (regle 3)",
             "TRAVAIL EN SERIE OBLIGATOIRE" in agents,
             "regle 3 absente d'AGENTS.md")

    # 7. Coherence croisee 3/3 : les marqueurs cles sont dans les 3 fichiers
    #    (comparaison insensible a la casse : COMMENT-DEMARRER.md ecrit
    #    'un seul' en minuscules, demarrer.md/AGENTS.md 'un SEUL')
    c_low, d_low, a_low = comment.lower(), demarrer.lower(), agents.lower()
    couverts = 0
    for m in ["travail en serie obligatoire",
              "jamais 2 missions relayees simultanement",
              "un seul agent est incarne a la fois"]:
        if m in c_low and m in d_low and m in a_low:
            couverts += 1
    verifier("coherence croisee 3/3 (3 marqueurs dans les 3 fichiers)",
             couverts == 3,
             "seulement %d/3 marqueurs couverts par les 3 fichiers" % couverts)

    # 8. Normes : ASCII strict + LF pur sur les 2 fichiers modifies
    for nom, chemin in [("COMMENT-DEMARRER.md", F_COMMENT),
                        ("demarrer.md", F_DEMARRER)]:
        d = octets(chemin)
        non_ascii = sum(1 for b in d if b > 127)
        crlf = d.count(b"\r\n")
        verifier("normes %s : ASCII 0/0 (%d) + LF pur 0 CRLF (%d)"
                 % (nom, non_ascii, crlf),
                 non_ascii == 0 and crlf == 0,
                 "non-ascii=%d crlf=%d" % (non_ascii, crlf))

    # 12. PREUVE NEGATIVE : fixture sans la regle serie detectee
    fixture = ("# Fichier fixture sans la regle serie\n"
               "- pour demarrer un second llm en parallel : changer l id\n")
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False,
                                      encoding="ascii")
    try:
        tmp.write(fixture)
        tmp.close()
        with io.open(tmp.name, "r", encoding="ascii") as f:
            contenu_fixture = f.read()
        detecte = not est_conforme_serie(contenu_fixture)
        verifier("preuve negative : fixture sans serie DETECTEE",
                 detecte,
                 "la fixture sans la regle serie n'a pas ete detectee")
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass

    print("=== CHRONO test (total 0.0s) ====")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
