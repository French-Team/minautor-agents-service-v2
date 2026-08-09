#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-005-generateurs-commande.py
Test formel du generateur de commande v0.2.1 (fiabilisation des flags optionnels)
et du parcours Atlas v0.1.2 (pilote strict : commandes en dur retirees).

Objet (correction Buffy 2026-08-09) :
  - composer_commande avait une condition INVERSEE : les flags optionnels non
    renseignes etaient composes en VIDE (--debut --fin --lignes sans valeur)
    -> argparse code 2 (usage). Corrige py v0.2.1 + sh v0.2.1.
  - 9 flags booleens en dur dans les modeles du catalogue (--inverse, --forcer,
    --backup, --unique, --liste, --lister, --resume, --compter, --json) ont ete
    remplaces par des placeholders {cle} : reponse oui = flag present, non = absent.
  - parcours-atlas v0.1.1 -> v0.1.2 : 24 commandes en dur retirees des indices
    outil avec catalogue (ne restent que type/nom/catalogue/chemin).

Cas couverts (22 points) :
  GENERATEUR v0.2.1
  1. --version py = v0.2.1
  2. --version sh = v0.2.1
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
 14. catalogue version = 0.2.2
 15. flag optionnel renseigne conserve : lister-fichiers --extension md PRESENT
 16. non-regression : creer-fichier (fichier;contenu) compose correctement
  PARCOURS ATLAS v0.1.2
 17. parcours-atlas.json : json.load valide + version 0.1.2
 18. 0 champ commande restant dans les indices outil avec catalogue
 19. navigation chemin explorer : PARCOURS TERMINE
 20. navigation chemin autre+OUI (delegation) : PARCOURS TERMINE
 21. valider-cartes-decision --agent atlas : CONFORME
 22. affichage case c3 : PASSE PAR LE GENERATEUR sans commande en dur

Usage:
  python3 test-005-generateurs-commande.py
"""

import io
import json
import os
import re
import subprocess
import sys
import tempfile

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", ".."))
GC_PY = os.path.join(RACINE, "cerveau-projet/agents/tools/generateurs/generateurs-commande/generateurs-commande.py")
GC_SH = os.path.join(RACINE, "cerveau-projet/agents/tools/generateurs/generateurs-commande/generateurs-commande.sh")
CATALOGUE = os.path.join(RACINE, "cerveau-projet/agents/tools/generateurs/generateurs-commande/catalogue-commandes.json")
PARCOURS_ATLAS = os.path.join(RACINE, "cerveau-projet/agents/atlas/parcours/parcours-atlas.json")
GUIDER = os.path.join(RACINE, "cerveau-projet/agents/tools/guider/guider-parcours/guider-parcours.py")
VALIDER_CARTES = os.path.join(RACINE, "cerveau-projet/agents/tools/valider/valider-cartes-decision/valider-cartes-decision.py")
ASCII = os.path.join(RACINE, "cerveau-projet/agents/tools/valider/valider-conformite-ascii/valider-conformite-ascii.py")

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
    r = subprocess.run(ligne, shell=True, capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def exec_list(args):
    """Execute sans shell (fiable sous Windows pour les pipes dans les arguments)."""
    r = subprocess.run(args, capture_output=True, text=True)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def composer(nom, reponses, sh=False):
    """Compose via le generateur (py ou sh) et retourne la commande generee."""
    if sh:
        r = subprocess.run(["bash", GC_SH, "--commande", nom, "--reponses", reponses],
                           capture_output=True, text=True)
    else:
        r = subprocess.run(["python3", GC_PY, "--commande", nom, "--reponses", reponses],
                           capture_output=True, text=True)
    lignes = ((r.stdout or "") + (r.stderr or "")).splitlines()
    for i, ligne in enumerate(lignes):
        if "COMMANDE A LANCER" in ligne and i + 1 < len(lignes):
            return lignes[i + 1].strip()
    return None


def normale(s):
    return s.replace("\r\n", "\n").replace("\r", "\n")


def main():
    print("=== Test 005 -- generateurs-commande v0.2.1 + parcours-atlas v0.1.2 ===")
    print("")

    # ---------- GENERATEUR v0.2.1 ----------
    code, out = exec_cmd("python3 %s --version" % GC_PY)
    verifier(1, "generateurs-commande.py --version = v0.2.1", "v0.2.1" in out, out.strip())

    code, out = exec_cmd("bash %s --version" % GC_SH)
    verifier(2, "generateurs-commande.sh --version = v0.2.1", "v0.2.1" in out, out.strip())

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
        verifier(14, "catalogue version = 0.2.2", cat.get("version") == "0.2.2", str(cat.get("version")))
    except Exception as e:
        verifier(13, "catalogue-commandes.json JSON valide", False, str(e))
        verifier(14, "catalogue version = 0.2.0", False, "")

    cmd = composer("lister-fichiers", "chemin=agents;extension=md")
    verifier(15, "flag optionnel renseigne conserve (--extension md)", cmd is not None and "--extension md" in cmd, str(cmd))

    cmd = composer("creer-fichier", "fichier=x.md;contenu=hello")
    ok = cmd is not None and "creer-fichier.py x.md" in cmd and "hello" in cmd
    verifier(16, "non-regression creer-fichier composee correctement", ok, str(cmd))

    # ---------- PARCOURS ATLAS v0.1.2 ----------
    try:
        with io.open(PARCOURS_ATLAS, encoding="utf-8") as fh:
            p = json.load(fh)
        verifier(17, "parcours-atlas.json JSON valide + version 0.1.2",
                 p.get("parcours", {}).get("version") == "0.1.2", str(p.get("parcours", {}).get("version")))
    except Exception as e:
        verifier(17, "parcours-atlas.json JSON valide + version 0.1.2", False, str(e))
        p = {}

    n_commande = 0
    for c in p.get("cases", {}).values():
        for i in c.get("indices", []):
            if i.get("type") == "outil" and i.get("catalogue") and i.get("commande"):
                n_commande += 1
    verifier(18, "0 champ commande restant dans les indices avec catalogue", n_commande == 0, "restants=%d" % n_commande)

    for num, nom_chemin, chemin in [(19, "explorer", "OUI|explorer"), (20, "autre+OUI", "OUI|autre|OUI")]:
        c, out = exec_list(["python3", GUIDER, PARCOURS_ATLAS, "--reponses", chemin])
        verifier(num, "navigation %s : PARCOURS TERMINE" % nom_chemin, "PARCOURS TERMINE" in out, out[-80:])

    c, out = exec_cmd("python3 %s --agent atlas" % VALIDER_CARTES)
    verifier(21, "valider-cartes-decision --agent atlas : CONFORME", "CONFORME" in out, out[-80:])

    c, out = exec_list(["python3", GUIDER, PARCOURS_ATLAS, "--reponses", "OUI|explorer"])
    segment = out[out.find("Lister les fichiers"):out.find("Lister les fichiers") + 400] if "Lister les fichiers" in out else ""
    ok = ("PASSE PAR LE GENERATEUR" in segment) and ("catalogue: lister-fichiers" in segment)
    verifier(22, "case c3 : PASSE PAR LE GENERATEUR sans commande en dur", ok, segment[:200])

    # ---------- ASCII ----------
    for f, num in [(GC_PY, 23), (GC_SH, 24), (CATALOGUE, 25), (PARCOURS_ATLAS, 26)]:
        c, out = exec_cmd("python3 %s %s" % (ASCII, f))
        verifier(num, "ASCII 0 : %s" % os.path.basename(f), "validee" in out, out.strip())

    print("")
    print("=== RESULTAT : %d OK / %d KO ===" % (REUSSIS, ECHECS))
    return 1 if ECHECS else 0


if __name__ == "__main__":
    sys.exit(main())
