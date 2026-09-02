#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-005-generateurs-commande.py
Test formel du generateur de commande v0.2.6 (fiabilisation des flags optionnels),
du catalogue (chaque commande doit avoir sa documentation .md : REGLE ABSOLUE
LECTURE DOC) et du parcours Atlas v0.4.1 (migre au format action : references +
cases action, 2 commandes templates residuelles c30 + c11a conservees et documentees).

Objet (correction Buffy 2026-08-09) :
  - composer_commande avait une condition INVERSEE : les flags optionnels non
    renseignes etaient composes en VIDE (--debut --fin --lignes sans valeur)
    -> argparse code 2 (usage). Corrige py v0.2.1 + sh v0.2.1.
  - 9 flags booleens en dur dans les modeles du catalogue (--inverse, --forcer,
    --backup, --unique, --liste, --lister, --resume, --compter, --json) ont ete
    remplaces par des placeholders {cle} : reponse oui = flag present, non = absent.
  - parcours-atlas v0.1.1 -> v0.1.2 : 24 commandes en dur retirees des indices
    outil avec catalogue (ne restent que type/nom/catalogue/chemin).
  - parcours-atlas v0.1.2 -> v0.1.10 : pilote strict - 1 commande template
    residuelles cases c30 (cartographier-parcours.py {parcours}) + c11a (activer themis), connues et documentees.
  - parcours-atlas v0.1.10 -> v0.2.0 : migration format action (references + cases
    action). Les commandes templates c30 et c11a sont conservees comme residus connus (2).
  - parcours-atlas v0.3.3 -> v0.4.1 (2026-08-11) : ajout case c0d LIRE LA
  - parcours-atlas v0.4.2 -> v0.4.3 (2026-08-16) : branchage corriger-symboles
  - parcours-atlas v0.4.3 -> v0.4.4 (2026-08-16) : c0b relecture avec commandes lire-fichier (corrections puis fiche) - 3e cas commande en dur documente
  - parcours-atlas v0.4.6 (2026-08-16) : migration relecture obligatoire - c0 porte les 2 commandes lire-fichier (c0b devient question) - 7 commandes en dur documentees
  - parcours-atlas v0.4.1 -> v0.4.2 (2026-08-13) : Themis maillon (c11a/c11b)
    DOCUMENTATION DE L OUTIL avant utilisation (garde-fou lecture .md).

Cas couverts (26 points) :
  GENERATEUR v0.3.2 (py) / v0.3.1 (.sh exempte - pas de journalisation)
  1. --version py = v0.3.2
  2. --version sh = v0.3.1
  3. py_compile OK (generateurs-commande.py)
  4. bash -n OK (generateurs-commande.sh)
  5. composition lire-fichier (fichier=AGENTS.md;lignes=3) : SANS --debut/--fin vides
  6. commande composee lire-fichier : EXECUTABLE code 0
  7. composition lire-activite-recente (fichier;nombre=2) : SANS --longueur vide
  8. commande composee lire-activite-recente : EXECUTABLE code 0
  9. flag booleen analyser-dependances inverse=oui : --inverse PRESENT
 10. flag booleen analyser-dependances inverse=non : --inverse ABSENT
 11. flag booleen ecrire-fichier backup=non : --backup ABSENT (py)
 12. parite py/sh : commande composee identique (CRLF normalise)
 13. catalogue JSON valide (json.load)
 14. catalogue version = 0.2.16
 15. flag optionnel renseigne conserve : lister-fichiers --extension md PRESENT
 16. non-regression : creer-fichier (fichier;contenu) compose correctement
  PARCOURS ATLAS v0.4.1
17. parcours-atlas.json : json.load valide + version 0.5.4
18. 7 commandes en dur connues (c0 x2 + c10/c18/c19 corriger-symboles + c11a + c30) dans les indices outil avec catalogue
 19. navigation chemin explorer : PARCOURS TERMINE
 20. navigation chemin autre+OUI (delegation) : PARCOURS TERMINE
 21. valider-cartes-decision --agent atlas : CONFORME
 22. affichage case c3 : PASSE PAR LE GENERATEUR sans commande en dur
  CATALOGUE - CONTRAT DOCUMENTATION (REGLE ABSOLUE LECTURE DOC)
 23. chaque commande du catalogue (138) a son .md a cote du script
 24. les commandes de test (test-004 a test-021) sont composables
     via generateurs-commande (generation reelle en dry-run)

Usage:
  python3 test-005-generateurs-commande.py
Tags: outils, catalogue, generateurs
"""

import contextlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", ".."))
TOOLS_DIR = os.path.join(RACINE, "cerveau-projet", "agents", "tools")


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

PROTECTIONS = charger_protections()
# ------------------------------------------------------------------
# OPTIONS ON/OFF + CHRONO (regle immuable v0.3.0, deploiement dynamique) :
#   --no-chrono            desactive le chrono (defaut : actif)
#   --isoler N             n execute que le point N (diagnostic cible)
#   --desactiver 1,3,5     saute les points listes (sans toucher au code)
# ------------------------------------------------------------------
CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for _i, _arg in enumerate(sys.argv):
    if _arg == "--isoler" and _i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[_i + 1])
        except ValueError:
            pass
    if _arg == "--desactiver" and _i + 1 < len(sys.argv):
        for _p in sys.argv[_i + 1].split(','):
            try:
                DESACTIVES.append(int(_p))
            except ValueError:
                pass
ETAPES = []
T_START = __import__("time").monotonic()


def point_actif(numero):
    # True si le point N doit s executer (options on/off du test)
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def chrono_etape(nom, t_debut):
    # Enregistre la duree d une etape (no-op si --no-chrono)
    if CHRONO_ACTIF:
        ETAPES.append((nom, __import__("time").monotonic() - t_debut))


def bilan_chrono():
    # Affiche le bilan des durees : total + detail par etape
    if not CHRONO_ACTIF:
        return
    _total = __import__("time").monotonic() - T_START
    print("")
    print("=== CHRONO test (total %.1fs) ===" % _total)
    for _nom, _duree in ETAPES:
        print("  %-34s %6.2fs" % (_nom, _duree))

GC_PY = os.path.join(RACINE, "cerveau-projet/agents/tools/generateurs/generateurs-commande/generateurs-commande.py")
GC_SH = os.path.join(RACINE, "cerveau-projet/agents/tools/generateurs/generateurs-commande/generateurs-commande.sh")
CATALOGUE = os.path.join(RACINE, "cerveau-projet/agents/tools/generateurs/generateurs-commande/catalogue-commandes.json")
PARCOURS_ATLAS = os.path.join(RACINE, "cerveau-projet/agents/atlas/parcours/parcours-atlas.json")
GUIDER = os.path.join(RACINE, "cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py")
VALIDER_CARTES = os.path.join(RACINE, "cerveau-projet/agents/tools/valider/valider-cartes-decision/valider-cartes-decision.py")
ASCII = os.path.join(RACINE, "cerveau-projet/agents/tools/valider/valider-conformite-ascii/valider-conformite-ascii.py")


def charger_generateur():
    spec = importlib.util.spec_from_file_location("gen_commande_mod", GC_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


GEN = charger_generateur()
CAT_GEN = GEN.charger_catalogue(CATALOGUE)

REUSSIS = 0
ECHECS = 0


def verifier(numero, description, condition, detail=""):
    global REUSSIS, ECHECS
    if condition:
        REUSSIS += 1
        print("[OK] %2d. %s" % (numero, description))
    else:
        ECHECS += 1
        print("[KO] %2d. %s | %s" % (numero, description, detail))


def exec_cmd(ligne):
    r = PROTECTIONS.lancer_protege(ligne, shell=True, capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def exec_list(args):
    """Execute sans shell (fiable sous Windows pour les pipes dans les arguments)."""
    r = PROTECTIONS.lancer_protege(args, capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def composer(nom, reponses, sh=False):
    """Compose via le generateur. py = EN PROCESS (rapide), sh = via bash.

    Optimisation 2026-08-17 (goulot de la suite) : composer chaque commande
    relancait un sous-processus python3 (~0.2s x 28 = ~6s). On importe le
    generateur EN PROCESS et on appelle les MEMES fonctions que le CLI
    (trouver_commande / parser_reponses_forcees / interroger_interactif /
    composer_commande). L integrite du wrapper CLI reste couverte par les
    points 1-4 (--version, py_compile, bash -n).
    """
    if sh:
        r = PROTECTIONS.lancer_protege(["bash", GC_SH, "--commande", nom, "--reponses", reponses],
                           capture_output=True, text=True)
        lignes = ((r.stdout or "") + (r.stderr or "")).splitlines()
        for i, ligne in enumerate(lignes):
            if "COMMANDE A LANCER" in ligne and i + 1 < len(lignes):
                return lignes[i + 1].strip()
        return None
    commandes = GEN.trouver_commande(CAT_GEN, nom)
    if commandes is None:
        return None
    rep = GEN.parser_reponses_forcees(reponses)
    with contextlib.redirect_stdout(io.StringIO()):
        valides = GEN.interroger_interactif(commandes, rep)
    if valides is None:
        return None
    return GEN.composer_commande(commandes, valides)


def normale(s):
    return s.replace("\r\n", "\n").replace("\r", "\n")


def main():
    print("=== Test 005 -- generateurs-commande v0.3.2 + catalogue 0.2.16 + parcours-atlas v0.5.4 ===")
    print("")

    # ---------- GENERATEUR v0.3.2 ----------
    code, out = exec_cmd("python3 %s --version" % GC_PY)
    verifier(1, "generateurs-commande.py --version = v0.3.2", "v0.3.2" in out, out.strip())

    code, out = exec_cmd("bash %s --version" % GC_SH)
    verifier(2, "generateurs-commande.sh --version = v0.3.1", "v0.3.1" in out, out.strip())

    code, out = exec_cmd("python3 -m py_compile %s" % GC_PY)
    verifier(3, "py_compile generateurs-commande.py", code == 0, out.strip())

    code, out = exec_cmd("bash -n %s" % GC_SH)
    verifier(4, "bash -n generateurs-commande.sh", code == 0, out.strip())

    cmd = composer("lire-fichier", "fichier=AGENTS.md;lignes=3")
    ok = cmd is not None and "--debut" not in cmd and "--fin" not in cmd and "--lignes 3" in cmd
    verifier(5, "lire-fichier compose SANS flags vides (--debut/--fin)", ok, str(cmd))

    if cmd:
        c2, out2 = exec_cmd(cmd)
        verifier(6, "lire-fichier composee EXECUTABLE (code 0)", c2 == 0, out2[:80])

    cmd = composer("lire-activite-recente", "fichier=AGENTS-historique.md;nombre=2")
    ok = cmd is not None and "--longueur" not in cmd and "--nombre 2" in cmd
    verifier(7, "lire-activite-recente composee SANS --longueur vide", ok, str(cmd))

    if cmd:
        c2, out2 = exec_cmd(cmd)
        verifier(8, "lire-activite-recente composee EXECUTABLE (code 0)", c2 == 0, out2[:80])

    cmd = composer("analyser-dependances", "fichier=x.py;inverse=oui")
    verifier(9, "flag booleen inverse=oui -> --inverse PRESENT", cmd is not None and "--inverse" in cmd, str(cmd))

    cmd = composer("analyser-dependances", "fichier=x.py;inverse=non")
    verifier(10, "flag booleen inverse=non -> --inverse ABSENT", cmd is not None and "--inverse" not in cmd, str(cmd))

    cmd = composer("ecrire-fichier", "fichier=x.md;contenu=hi;backup=non")
    verifier(11, "flag booleen backup=non -> --backup ABSENT (py)", cmd is not None and "--backup" not in cmd, str(cmd))

    cmd_py = composer("lire-fichier", "fichier=AGENTS.md;lignes=3")
    cmd_sh = composer("lire-fichier", "fichier=AGENTS.md;lignes=3", sh=True)
    verifier(12, "parite py/sh commande composee identique", cmd_py == cmd_sh, "py=%s sh=%s" % (cmd_py, cmd_sh))

    try:
        with io.open(CATALOGUE, encoding="utf-8") as fh:
            cat = json.load(fh)
        verifier(13, "catalogue-commandes.json JSON valide", True)
        verifier(14, "catalogue version = 0.2.16", cat.get("version") == "0.2.16", str(cat.get("version")))
    except Exception as e:
        verifier(13, "catalogue-commandes.json JSON valide", False, str(e))
        verifier(14, "catalogue version = 0.2.0", False, "")

    cmd = composer("lister-fichiers", "chemin=agents;extension=md")
    verifier(15, "flag optionnel renseigne conserve (--extension md)", cmd is not None and "--extension md" in cmd, str(cmd))

    cmd = composer("creer-fichier", "fichier=x.md;contenu=hello")
    ok = cmd is not None and "creer-fichier.py x.md" in cmd and "hello" in cmd
    verifier(16, "non-regression creer-fichier composee correctement", ok, str(cmd))

    # ---------- PARCOURS ATLAS v0.5.4 ----------
    try:
        with io.open(PARCOURS_ATLAS, encoding="utf-8") as fh:
            p = json.load(fh)
        verifier(17, "parcours-atlas.json JSON valide + version 0.5.7",
                 p.get("parcours", {}).get("version") == "0.5.7", str(p.get("parcours", {}).get("version")))
    except Exception as e:
        verifier(17, "parcours-atlas.json JSON valide + version 0.5.4", False, str(e))
        p = {}

    # Commandes en dur connues et documentees : c30 (template
    # cartographier-parcours.py {parcours}), c11a (activer themis), c0 x2
    # (relecture lire-fichier, portees par c0 depuis la migration relecture
    # obligatoire 2026-08-16), c10/c18/c19 (corriger-symboles --all ajoutees
    # par Buffy 2026-08-16), c12/c13 (detecter-recherches-obsoletes /
    # rechercher-web ajoutees par Buffy 2026-08-16), c10 x2 suppl.
    # (enregistrer-lecon + consulter-lecons, round BDD lecons 2026-08-17),
    # c0e (consulter-lecons consultation pre-mission, round 2026-08-18),
    # cU2 (comprendre l outil : consulter-combos, ajoutee par Buffy
    # 2026-08-21), c0g (GATE BON AGENT : verifier-agent-perimetre --gate,
    # decision utilisateur marbre-log 2026-08-29). Toute commande
    # SUPPLEMENTAIRE = regression.
    n_commande = 0
    cases_commande = []
    for k, c in p.get("cases", {}).items():
        for i in c.get("indices", []):
            if i.get("type") == "outil" and i.get("catalogue") and i.get("commande"):
                n_commande += 1
                cases_commande.append(k)
    verifier(18, "15 commandes en dur connues (c0 x2 + c0e + c0g + c10 x3 + c11a + c12/c13 + c18/c19 + c30 + c35 + cU2) dans les indices avec catalogue",
             n_commande == 15 and sorted(cases_commande) == ["c0", "c0", "c0e", "c0g", "c10", "c10", "c10", "c11a", "c12", "c13", "c18", "c19", "c30", "c35", "cU2"],
             "restants=%d cases=%s" % (n_commande, sorted(cases_commande)))

    # Depuis Buffy 2026-08-21 (case COMPRENDRE L OUTIL cU1), le flux passe
    # par cU1 (NON) avant la question Mission : les sequences de navigation
    # portent un NON supplementaire apres le OUI de c0b.
    for num, nom_chemin, chemin in [(19, "explorer", "OUI|NON|explorer|NON|OUI|NON|OUI"), (20, "autre+OUI", "OUI|NON|autre|OUI|NON|OUI|NON|OUI")]:
        c, out = exec_list(["python3", GUIDER, PARCOURS_ATLAS, "--reponses", chemin])
        verifier(num, "navigation %s : PARCOURS TERMINE" % nom_chemin, "PARCOURS TERMINE" in out, out[-80:])

    c, out = exec_cmd("python3 %s --agent atlas" % VALIDER_CARTES)
    verifier(21, "valider-cartes-decision --agent atlas : CONFORME", "CONFORME" in out, out[-80:])

    c, out = exec_list(["python3", GUIDER, PARCOURS_ATLAS, "--case", "c16"])
    segment = out[out.find("Lister les fichiers"):out.find("Lister les fichiers") + 400] if "Lister les fichiers" in out else ""
    ok = ("PASSE PAR LE GENERATEUR" in segment) and ("catalogue: lister-fichiers" in segment)
    verifier(22, "case c16 : PASSE PAR LE GENERATEUR sans commande en dur", ok, segment[:200])

    # ---------- CONTRAT DOCUMENTATION (REGLE ABSOLUE LECTURE DOC) ----------
    # Chaque commande du catalogue doit pointer vers un outil dont la documentation
    # .md existe a cote du script : le .md est le contrat d utilisation (l agent
    # DOIT le lire avant d utiliser l outil - REGLE ABSOLUE LECTURE DOC).
    try:
        with io.open(CATALOGUE, encoding="utf-8") as fh:
            cat2 = json.load(fh)
        sans_md = []
        for e in cat2.get("commandes", []):
            script = e.get("script", "")
            if not script:
                sans_md.append((e.get("nom"), "sans script"))
                continue
            md = script.rsplit(".", 1)[0] + ".md"
            if not os.path.exists(md):
                sans_md.append((e.get("nom"), script))
        verifier(23, "chaque commande du catalogue (138) a son .md a cote du script",
                 len(sans_md) == 0, "sans .md: %s" % sans_md[:5])
    except Exception as e:
        verifier(23, "chaque commande du catalogue (138) a son .md a cote du script", False, str(e))

    # Les commandes de test (test-004 a test-021) doivent etre composables
    # via generateurs-commande (generation reelle en dry-run).
    tests_ko = []
    for e in cat2.get("commandes", []):
        nom = e.get("nom", "")
        if not (nom.startswith("test-") and nom != "test-001" and nom != "test-002" and nom != "test-003"):
            continue
        cmd = composer(nom, "chemin=.")
        if cmd is None:
            tests_ko.append(nom)
    verifier(24, "les commandes de test (test-004 a test-021) sont composables",
             len(tests_ko) == 0, "non composables: %s" % tests_ko[:5])

    # ---------- ASCII ----------
    for f, num in [(GC_PY, 25), (GC_SH, 26), (CATALOGUE, 27), (PARCOURS_ATLAS, 28)]:
        c, out = exec_cmd("python3 %s %s" % (ASCII, f))
        verifier(num, "ASCII 0 : %s" % os.path.basename(f), "validee" in out, out.strip())

    print("")
    print("=== RESULTAT : %d OK / %d KO ===" % (REUSSIS, ECHECS))
    return 1 if ECHECS else 0


bilan_chrono()

if __name__ == "__main__":
    sys.exit(main())
