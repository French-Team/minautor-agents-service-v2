#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-029-conformite-template.py
GARDE-FOU : chaque test-0XX doit respecter la structure du TEMPLATE de test
(tester/template-test.md v0.3.0, format Python canonique,
regle immuable protections + options on/off + chrono).

Contexte (audit Morpheus 2026-08-12, demande utilisateur) :
  - Le template-test.md (v0.1.0) etait obsolete (format bash avec protections)
    alors que les tests reels sont des .py Python purs avec [OK]/[KO].
  - Aucune case de la carte de Morpheus ne referencait le template : chaque
    nouveau test etait cale sur les tests precedents (derive : test-001/002/003
    en coding utf-8 + marqueur [ECHEC] invisible pour le lanceur de
    non-regression qui compte les [KO]).
  - Anti-recurrence : ce test verifie pour CHAQUE test-0XX les invariants
    vitaux du template. Le TEMPLATE est LA reference, pas les tests precedents.

Invariants verifies (pour chaque test-0XX) :
  1. Shebang python3
  2. coding ascii (JAMAIS utf-8)
  3. Fonction d assertion : def verifier( ou def check(
  4. Marqueurs [OK] et [KO] presents (le lanceur compte les [KO])
  5. Bilan final : RESULTAT / VERDICT / BILAN affiche
  6. Code retour fiable : sys.exit(main()) ou sys.exit(0/1)
  7. AUCUN marqueur [ECHEC] (ancien format, invisible pour le lanceur)
  8. Normes : ASCII strict (0 non-ASCII) + LF pur (0 CRLF) sur chaque test
"""
import importlib.util
import io
import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TESTS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                         "tester", "tests")
TEMPLATE = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                        "tester", "template-test.md")

NB_POINTS = 0
NB_OK = 0
NB_KO = 0


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def ascii_count(chemin):
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return sum(1 for c in fh.read() if ord(c) > 127)


def crlf_count(chemin):
    with open(chemin, "rb") as fh:
        return fh.read().count(b"\r\n")


def _texte_executable(texte):
    """Retire la docstring (premier bloc \"\"\"...\"\"\") et les lignes de
    commentaire pour ne garder que le code executable."""
    lignes = []
    dans_docstring = False
    for ligne in texte.splitlines():
        if '"""' in ligne:
            dans_docstring = not dans_docstring
            continue
        if dans_docstring:
            continue
        if ligne.strip().startswith("#"):
            continue
        lignes.append(ligne)
    return "\n".join(lignes)


def lister_tests():
    """Retourne la liste des fichiers test-0XX*.py (triee)."""
    resultats = []
    if not os.path.isdir(TESTS_DIR):
        return resultats
    for nom in sorted(os.listdir(TESTS_DIR)):
        dossier = os.path.join(TESTS_DIR, nom)
        if not os.path.isdir(dossier):
            continue
        for fichier in sorted(os.listdir(dossier)):
            if fichier.startswith("test-0") and fichier.endswith(".py"):
                resultats.append(os.path.join(dossier, fichier))
    return resultats


def main():
    print("=== test-029 : conformite au template-test.md v0.3.0 ===")

    tests = lister_tests()
    verifier("1. Le dossier tests/ contient des tests (test-0XX)",
             len(tests) > 0, "nb=%d" % len(tests))

    # 2. Le template de reference existe et est en v0.3.0 (format Python
    #    + bloc d import OBLIGATOIRE des protections
    #    + regle immuable options on/off + chrono : point_actif / bilan_chrono)
    template_ok = os.path.isfile(TEMPLATE)
    if template_ok:
        with io.open(TEMPLATE, encoding="utf-8", errors="replace") as fh:
            contenu_template = fh.read()
        template_ok = ("Version : 0.3.0" in contenu_template
                       and "python" in contenu_template
                       and "PROTECTIONS = charger_protections()" in contenu_template
                       and "point_actif" in contenu_template
                       and "bilan_chrono" in contenu_template)
    verifier("2. template-test.md existe en v0.3.0 (Python + protections + chrono)",
             template_ok, "chemin=%s" % TEMPLATE)

    # 3. Le template est reference dans la carte de Morpheus
    carte = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "morpheus",
                         "parcours", "parcours-morpheus.json")
    carte_template = False
    if os.path.isfile(carte):
        with io.open(carte, encoding="utf-8", errors="replace") as fh:
            carte_texte = fh.read()
        carte_template = "template-test" in carte_texte
    verifier("3. La carte de Morpheus reference template-test.md",
             carte_template, "chemin=%s" % carte)

    # 4. Invariants vitaux sur CHAQUE test
    ko_marqueur = []
    ko_ascii_coding = []
    ko_sans_assert = []
    ko_sans_ok_ko = []
    ko_sans_bilan = []
    ko_sans_exit = []
    ko_echec = []
    ko_normes = []

    for t in tests:
        nom = os.path.basename(t)
        with io.open(t, encoding="utf-8", errors="replace") as fh:
            texte = fh.read()

        # 4a. Shebang python3
        if not texte.startswith("#!/usr/bin/env python3"):
            ko_marqueur.append(nom)

        # 4b. coding ascii, JAMAIS utf-8 : on ne verifie QUE les 2 premieres
        # lignes (un test peut mentionner le motif dans son propre code de
        # verif sans s auto-incriminer)
        tete = "\n".join(texte.splitlines()[:2])
        if "# -*- coding: utf-8 -*-" in tete:
            ko_ascii_coding.append(nom)
        elif "# -*- coding: ascii -*-" not in tete:
            ko_ascii_coding.append(nom)

        # 4c. Fonction d assertion (verifier ou check)
        if not re.search(r"def (verifier|check)\(", texte):
            ko_sans_assert.append(nom)

        # 4d. Marqueurs [OK] et [KO]
        if "[OK]" not in texte or "[KO]" not in texte:
            ko_sans_ok_ko.append(nom)

        # 4e. Bilan final (RESULTAT / VERDICT / BILAN)
        if not re.search(r"(RESULTAT|VERDICT|BILAN)\s*:", texte):
            ko_sans_bilan.append(nom)

        # 4f. Code retour fiable
        if not re.search(r"sys\.exit\((main\(\)|0 if|1 if)", texte):
            ko_sans_exit.append(nom)

        # 4g. Aucun marqueur [ECHEC] : on retire la docstring et les lignes
        # de commentaire pour ne garder que le code executable (une mention
        # documentaire du motif ne doit pas compter comme une violation).
        # Le motif est construit par concatenation pour que ce garde-fou ne
        # contienne jamais le litteral lui-meme (auto-incrimination evitee).
        motif_echec = "[" + "ECHEC" + "]"
        code_exec = _texte_executable(texte)
        if motif_echec in code_exec:
            ko_echec.append(nom)

        # 4h. Normes ASCII strict + LF pur
        if ascii_count(t) != 0 or crlf_count(t) != 0:
            ko_normes.append(nom)

    nb_tests = len(tests)
    verifier("4a. Shebang python3 sur les %d tests" % nb_tests,
             len(ko_marqueur) == 0, "KO=%s" % ko_marqueur)
    verifier("4b. coding ascii sur les %d tests (aucun utf-8)" % nb_tests,
             len(ko_ascii_coding) == 0, "KO=%s" % ko_ascii_coding)
    verifier("4c. def verifier()/check() sur les %d tests" % nb_tests,
             len(ko_sans_assert) == 0, "KO=%s" % ko_sans_assert)
    verifier("4d. Marqueurs OK et KO presents sur les %d tests" % nb_tests,
             len(ko_sans_ok_ko) == 0, "KO=%s" % ko_sans_ok_ko)
    verifier("4e. Bilan final (RESULTAT/VERDICT/BILAN) sur les %d tests" % nb_tests,
             len(ko_sans_bilan) == 0, "KO=%s" % ko_sans_bilan)
    verifier("4f. Code retour fiable (sys.exit) sur les %d tests" % nb_tests,
             len(ko_sans_exit) == 0, "KO=%s" % ko_sans_exit)
    verifier("4g. Aucun marqueur " + motif_echec + " sur les %d tests" % nb_tests,
             len(ko_echec) == 0, "KO=%s" % ko_echec)
    verifier("4h. ASCII strict + LF pur sur les %d tests" % nb_tests,
             len(ko_normes) == 0, "KO=%s" % ko_normes)

    # 5. Le lanceur de non-regression compte les [KO] (les marqueurs servent)
    lanceur = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools",
                           "tester", "tester-lancer-non-regression",
                           "tester-lancer-non-regression.py")
    lanceur_ok = False
    if os.path.isfile(lanceur):
        with io.open(lanceur, encoding="utf-8", errors="replace") as fh:
            lanceur_texte = fh.read()
        lanceur_ok = "[KO]" in lanceur_texte
    verifier("5. Le lanceur compte les KO (marqueurs fiables)",
             lanceur_ok, "chemin=%s" % lanceur)

    # 6. Normes ASCII strict + LF pur sur le template
    na_template = ascii_count(TEMPLATE)
    crlf_template = crlf_count(TEMPLATE)
    verifier("6a. ASCII strict : 0 non-ASCII (template-test.md)",
             na_template == 0, "total=%d" % na_template)
    verifier("6b. LF pur : 0 CRLF (template-test.md)",
             crlf_template == 0, "total=%d" % crlf_template)

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
