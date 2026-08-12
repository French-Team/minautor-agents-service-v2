#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-009-valider-case.py
Test formel de l'outil valider-case v1.1.1 (categorie valider/).

Outil teste (cerveau-projet/agents/tools/valider/valider-case/):
  .py + .sh (wrapper pur exec python3) + .md + spec/
  Valide et ALLEGE une carte de decision (parcours JSON) : structure, modele
  compose, surcharge des indices (BUDGET PONDERE : court <= 100 car. = 0,5 /
  long > 100 = 1, budget 3,0 par case - 2 courts = 1 long ; texte > 160 car.
  reste le plafond absolu d'un indice), references, normes.
  Verdict : CONFORME / A ALLEGER / NON CONFORME + rapport markdown.
  (Etape 2 de la spec-refonte-cartes-decision v0.1.1)

Cas couverts:
  1. --version py/sh identiques v1.1.1 (parite)
  2. --aide : usage complet (requis par detecter-decalages-catalogue)
  3. Execution sur parcours-cerberus (migre, etape 6) : verdict CONFORME
     (0 erreur, 0 surcharge, avertissement pattern de re-essai c5) +
     temoin ARTIFICIEL a alleger (genere dans tmp : cerberus + 3 indices
     de 200 car.) : verdict A ALLEGER avec >= 3 surcharges
  3f. BUDGET PONDERE v1.1.1 : temoin 6 indices COURTS (<= 100 car.) =
     poids 3,0 -> CONFORME (6 courts acceptes) ; temoin 4 indices LONGS
     (> 100 car.) = poids 4,0 -> A ALLEGER (2 courts = 1 long)
  4. --case c12b (existante) : CONFORME ; --case c13b (inexistante) : NON CONFORME
  5. --modele : pattern de re-essai (NON -> soi-meme) en AVERTISSEMENT, pas erreur
  6. --surcharge : items signales sur le temoin artificiel a alleger (>= 3)
  7. --references : CONFORME (aucune ref dans les parcours actuels)
  8. Rapport wet : fichier markdown cree avec en-tete + verdict + comptages
  9. Parcours inexistant : ERREUR claire + code non nul
 10. JSON invalide : ERREUR claire + code non nul
 11. Protection : aucun fichier cree dans le dossier outil
 11c. Garde-fou positif v1.0.2 : ACCEPTATION d'un id cT* (convention etendue,
      prefixe thematique majuscule - ligne Trio de Janus)
 12. ASCII strict : 0 non-ASCII sur les 4 fichiers de l outil

Usage:
  python3 test-009-valider-case.py
"""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

TOOLS_DIR = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents", "tools")
PYTHON = sys.executable

OUTIL_DIR = os.path.join(TOOLS_DIR, "valider", "valider-case")
OUTIL_PY = os.path.join(OUTIL_DIR, "valider-case.py")
OUTIL_SH = os.path.join(OUTIL_DIR, "valider-case.sh")
OUTIL_MD = os.path.join(OUTIL_DIR, "valider-case.md")
OUTIL_SPEC = os.path.join(OUTIL_DIR, "spec", "spec-valider-case.001.01.ebauche.md")
PARCOURS_CERBERUS = os.path.join(PROJECT_ROOT, "cerveau-projet", "agents",
                                 "cerberus", "parcours", "parcours-cerberus.json")
# Parcours temoin A ALLEGER : ARTIFICIEL (tous les parcours reels sont
# CONFORME depuis l'allegement de janus - Pattern 16). On genere dans tmp
# une copie de parcours-cerberus avec 3 indices regle > 160 car. pour forcer
# le verdict A ALLEGER (>= 3 surcharges) sans dependre de l'etat des parcours.
def fabriquer_temoin_surcharge(tmp, cerberus_chemin):
    with io.open(cerberus_chemin, encoding="utf-8") as fh:
        d = json.load(fh)
    # 3 cases action existantes : on ajoute un indice regle de 200 caracteres
    cibles = [k for k, c in d["cases"].items()
              if c.get("type") in ("action", "controle")][:3]
    gros_texte = ("REGLE SURCHARGE TEST (temoin artificiel) : "
                  "ceci est un indice de regle volontairement tres long pour "
                  "depasser le seuil de 160 caracteres et forcer le verdict "
                  "A ALLEGER sur cette case du parcours temoin du test-009. ")
    for k in cibles:
        d["cases"][k].setdefault("indices", []).append(
            {"type": "regle", "texte": gros_texte})
    temoin = os.path.join(tmp, "parcours-temoin-surcharge.json")
    with io.open(temoin, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=True, indent=2)
    return temoin

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


def run(cmd, timeout=60):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def ascii_count(chemin):
    """Compte les caracteres non-ASCII d'un fichier (0 = conforme)."""
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        txt = fh.read()
    return sum(1 for c in txt if ord(c) > 127)


def main():
    global NB_POINTS, NB_OK, NB_KO

    tmp = tempfile.mkdtemp(prefix="test-009-")
    try:
        print("=== Test formel valider-case v1.0.2 ===")

        # 1. --version py/sh identiques (parite)
        r_py = run([PYTHON, OUTIL_PY, "--version"])
        r_sh = run(["bash", OUTIL_SH, "--version"])
        verifier("1. --version py/sh identiques v1.1.1",
                 r_py.returncode == 0 and r_sh.returncode == 0
                 and "v1.1.1" in r_py.stdout
                 and r_py.stdout.strip() == r_sh.stdout.strip(),
                 "py=%r sh=%r" % (r_py.stdout.strip(), r_sh.stdout.strip()))

        # 2. --aide : usage complet
        r_aide = run([PYTHON, OUTIL_PY, "--aide"])
        verifier("2a. --aide retourne 0",
                 r_aide.returncode == 0, r_aide.stderr.strip()[-80:])
        verifier("2b. --aide affiche les options cles",
                 all(opt in r_aide.stdout for opt in
                     ("--case", "--surcharge", "--modele", "--references",
                      "--dry-run", "--rapport")),
                 r_aide.stdout.strip()[-150:])

        # 3. Execution sur parcours-cerberus (MIGRE, etape 6) : verdict CONFORME
        r = run([PYTHON, OUTIL_PY, PARCOURS_CERBERUS, "--dry-run"])
        verifier("3a. Execution parcours-cerberus retourne 0",
                 r.returncode == 0, r.stdout.strip()[-100:])
        verifier("3b. Verdict CONFORME (0 erreur, 0 surcharge apres migration)",
                 "CONFORME" in r.stdout and "erreurs: 0" in r.stdout
                 and "a alleger: 0" in r.stdout,
                 r.stdout.strip()[:120])
        verifier("3c. Aucune surcharge restante (migration etape 6)",
                 "a alleger:" in r.stdout
                 and int(r.stdout.split("a alleger:")[1].split("|")[0].strip()) == 0,
                 r.stdout.strip()[:120])
        verifier("3d. Pattern de re-essai c5 en AVERTISSEMENT",
                 "pattern de re-essai" in r.stdout and "c5" in r.stdout,
                 r.stdout.strip()[:150])
        # 3e. Parcours temoin ARTIFICIEL : verdict A ALLEGER toujours detecte
        #     (tous les parcours reels sont CONFORME depuis l'allegement de janus)
        temoin_surcharge = fabriquer_temoin_surcharge(tmp, PARCOURS_CERBERUS)
        r_sur = run([PYTHON, OUTIL_PY, temoin_surcharge, "--dry-run"])
        verifier("3e. Temoin artificiel : A ALLEGER avec >= 3 surcharges",
                 "A ALLEGER" in r_sur.stdout and "erreurs: 0" in r_sur.stdout
                 and "a alleger:" in r_sur.stdout
                 and int(r_sur.stdout.split("a alleger:")[1].split("|")[0].strip()) >= 3,
                 r_sur.stdout.strip()[:120])

        # 3f. BUDGET PONDERE v1.1.1 : 6 courts = 3,0 CONFORME ; 4 longs = 4,0 A ALLEGER
        # Parcours minimal : case action c1 (SANS indices) enchaine vers la fin c9.
        def fabriquer_temoin_budget(tmp, nb, taille):
            indices = [{"type": "regle", "texte": "R" * taille} for _ in range(nb)]
            dd = {
                "parcours": {"agent": "test-budget", "version": "0.1.0",
                             "case_depart": "c0"},
                "cases": {
                    "c0": {"type": "question", "titre": "Depart",
                            "question": "Tester le budget ?",
                            "branches": [
                                {"reponse": "OUI", "vers": "c1"},
                                {"reponse": "NON", "vers": "c1"}]},
                    "c1": {"type": "action", "titre": "Case avec indices",
                            "indices": indices, "suivant": "c9"},
                    "c9": {"type": "fin", "titre": "Fin"},
                },
            }
            t = os.path.join(tmp, "parcours-temoin-budget-%d-%d.json" % (nb, taille))
            with io.open(t, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(dd, fh, ensure_ascii=True, indent=2)
            return t
        # 6 courts (50 car.) : poids = 0,5*6 = 3,0 -> CONFORME (nouvelle flexibilite)
        t_courts = fabriquer_temoin_budget(tmp, 6, 50)
        r_courts = run([PYTHON, OUTIL_PY, t_courts, "--dry-run"])
        verifier("3f. 6 indices courts (<= 100 car.) = poids 3,0 : CONFORME",
                 r_courts.returncode == 0 and "CONFORME" in r_courts.stdout
                 and "a alleger: 0" in r_courts.stdout,
                 r_courts.stdout.strip()[:120])
        # 4 longs (120 car.) : poids = 1*4 = 4,0 -> A ALLEGER
        t_longs = fabriquer_temoin_budget(tmp, 4, 120)
        r_longs = run([PYTHON, OUTIL_PY, t_longs, "--dry-run"])
        verifier("3g. 4 indices longs (> 100 car.) = poids 4,0 : A ALLEGER",
                 "A ALLEGER" in r_longs.stdout and "erreurs: 0" in r_longs.stdout
                 and "a alleger:" in r_longs.stdout
                 and int(r_longs.stdout.split("a alleger:")[1].split("|")[0].strip()) >= 1,
                 r_longs.stdout.strip()[:120])

        # 4. --case : existante CONFORME, inexistante NON CONFORME
        r_ok = run([PYTHON, OUTIL_PY, PARCOURS_CERBERUS, "--case", "c12b", "--dry-run"])
        verifier("4a. --case c12b (existante) : CONFORME",
                 r_ok.returncode == 0 and "CONFORME" in r_ok.stdout
                 and "erreurs: 0" in r_ok.stdout,
                 r_ok.stdout.strip()[:120])
        r_ko = run([PYTHON, OUTIL_PY, PARCOURS_CERBERUS, "--case", "c13b", "--dry-run"])
        verifier("4b. --case c13b (inexistante) : NON CONFORME",
                 r_ko.returncode != 0 and "NON CONFORME" in r_ko.stdout
                 and "c13b" in r_ko.stdout,
                 r_ko.stdout.strip()[:120])

        # 5. --modele : re-essai en avertissement (pas erreur)
        r_mod = run([PYTHON, OUTIL_PY, PARCOURS_CERBERUS, "--modele", "--dry-run"])
        verifier("5. --modele : re-essai en AVERTISSEMENT, 0 erreur",
                 "AVERTISSEMENT" in r_mod.stdout and "erreurs: 0" in r_mod.stdout,
                 r_mod.stdout.strip()[:150])

        # 6. --surcharge : items signales sur le temoin artificiel (>= 3)
        r_sur = run([PYTHON, OUTIL_PY, temoin_surcharge, "--surcharge", "--dry-run"])
        verifier("6. --surcharge : items signales sur temoin artificiel (>= 3)",
                 r_sur.returncode == 0
                 and int(r_sur.stdout.split("a alleger:")[1].split("|")[0].strip()) >= 3,
                 r_sur.stdout.strip()[:120])

        # 7. --references : refs resolvables (cerberus migre a des refs pattern/protocole)
        r_ref = run([PYTHON, OUTIL_PY, PARCOURS_CERBERUS, "--references", "--dry-run"])
        verifier("7. --references : CONFORME (refs resolvables apres migration)",
                 r_ref.returncode == 0 and "CONFORME" in r_ref.stdout,
                 r_ref.stdout.strip()[:120])

        # 8. Rapport wet : fichier markdown cree (sur le temoin artificiel : A ALLEGER)
        rapport = os.path.join(tmp, "rapport-vc.md")
        r_wet = run([PYTHON, OUTIL_PY, temoin_surcharge, "--rapport", rapport])
        ok_rapport = os.path.isfile(rapport)
        contenu = ""
        if ok_rapport:
            with io.open(rapport, encoding="utf-8") as fh:
                contenu = fh.read()
        verifier("8a. Rapport wet : fichier cree", ok_rapport and r_wet.returncode == 0)
        verifier("8b. Rapport : en-tete + verdict + comptages",
                 ok_rapport and "# Rapport" in contenu and "## Verdict" in contenu
                 and "**A ALLEGER**" in contenu and "| ERREURS" in contenu,
                 "contenu partiel")

        # 9. Parcours inexistant : ERREUR
        r_abs = run([PYTHON, OUTIL_PY, os.path.join(tmp, "absent.json")])
        verifier("9. Parcours inexistant : ERREUR + code non nul",
                 r_abs.returncode != 0 and "ERREUR" in (r_abs.stdout + r_abs.stderr),
                 "code=%d" % r_abs.returncode)

        # 10. JSON invalide : ERREUR
        invalide = os.path.join(tmp, "invalide.json")
        with io.open(invalide, "w", encoding="utf-8") as fh:
            fh.write("{ ceci n est pas du json ")
        r_inv = run([PYTHON, OUTIL_PY, invalide])
        verifier("10. JSON invalide : ERREUR + code non nul",
                 r_inv.returncode != 0 and "ERREUR" in (r_inv.stdout + r_inv.stderr),
                 "code=%d" % r_inv.returncode)

        # 11. Protection : aucun fichier cree dans le dossier outil
        avant = set(os.listdir(OUTIL_DIR))
        run([PYTHON, OUTIL_PY, PARCOURS_CERBERUS, "--dry-run"])
        apres = set(os.listdir(OUTIL_DIR))
        verifier("11. Protection : aucun fichier cree dans le dossier outil",
                 avant == apres, "cree: %s" % (apres - avant))

        # 11b. GARDE-FOU v1.0.1 : sans --rapport ni --dry-run, AUCUN rapport cree
        #      dans le repertoire courant (lecon : rapport a la racine)
        avant_cwd = set(os.listdir(tmp))
        r_gf = run([PYTHON, OUTIL_PY, PARCOURS_CERBERUS])
        apres_cwd = set(os.listdir(tmp))
        verifier("11b. Garde-fou v1.0.2 : sans --rapport, aucun fichier cree",
                 r_gf.returncode == 0 and avant_cwd == apres_cwd
                 and "AUCUN RAPPORT ECRIT" in r_gf.stdout,
                 "cree: %s | sortie: %s" % (apres_cwd - avant_cwd,
                                            r_gf.stdout.strip()[-80:]))

        # 11c. GARDE-FOU POSITIF v1.0.2 (lecon Morpheus 2026-08-11) : la
        #      convention etendue doit ACCEPTER les ids cT* (prefixe
        #      thematique majuscule, ligne Trio de Janus). Parcours
        #      artificiel minimal : depart c0 -> fin cT6.
        ct = os.path.join(tmp, "parcours-ct.json")
        with io.open(ct, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({
                "parcours": {"agent": "test-ct", "version": "0.1.0",
                             "case_depart": "c0"},
                "cases": {
                    "c0": {"type": "question", "titre": "Depart",
                            "question": "Tester la fin cT ?",
                            "branches": [
                                {"reponse": "OUI", "vers": "cT6"},
                                {"reponse": "NON", "vers": "cT6"}]},
                    "cT6": {"type": "fin", "titre": "Fin ligne Trio"},
                },
            }, fh, ensure_ascii=True, indent=2)
        r_ct = run([PYTHON, OUTIL_PY, ct, "--dry-run"])
        verifier("11c. Garde-fou positif : id cT6 ACCEPTE (0 erreur NOMMAGE)",
                 r_ct.returncode == 0 and "CONFORME" in r_ct.stdout
                 and "erreurs: 0" in r_ct.stdout
                 and "NOMMAGE" not in r_ct.stdout,
                 r_ct.stdout.strip()[:120])

        # 12. ASCII strict : 0 non-ASCII sur les 4 fichiers de l outil
        total_non_ascii = sum(ascii_count(f) for f in
                              (OUTIL_PY, OUTIL_SH, OUTIL_MD, OUTIL_SPEC))
        verifier("12. ASCII strict : 0 non-ASCII (4 fichiers)",
                 total_non_ascii == 0, "total non-ASCII = %d" % total_non_ascii)

        print("")
        print("=== RESULTAT : %d OK / %d KO (sur %d points) ===" % (NB_OK, NB_KO, NB_POINTS))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
