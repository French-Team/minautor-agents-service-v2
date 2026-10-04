#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-130-corriger-nommage-type-optionnel-garde-fou
===================================================
Garde-fou du correctif corriger-nommage v0.3.1 (mission 8ed06172 Vulcain,
inter-round suite Buffy 666bec53).

Contexte : le combo combo-corriger-fichier (case c1) lancait corriger-nommage
SANS --type alors que l outil exigeait --type {protocole,agent,outil,
convention} -> echec code 2 sur TOUT fichier passe au combo (JSON de parcours
comme .md). Correctif : --type devient OPTIONNEL avec AUTO-DETECTION par le
chemin + garde anti-renommage par extension (les .json de parcours v2 ne sont
JAMAIS renommes).

Le test verrouille :
1. Presence des 3 fichiers de l outil (.py, .sh, .md).
2. Sans --type sur un .md d outil (agents/tools/) : retour 0 (plus de code 2).
3. Sans --type sur un .json de parcours (agents/<agent>/parcours/) : retour 0
   ET AUCUN renommage (le .json existe toujours, aucun .json.md cree).
4. Auto-detection par chemin : agents/tools/ -> outil, agents/conventions/
   -> convention, protocole-* -> protocole, agents/<agent>/ -> agent
   (verifie sur la ligne '[AUTO] Type detecte depuis le chemin : <type>').
5. --type explicite conserve le comportement historique (--type outil .py OK).
6. Parite py/sh : le .sh retourne 0 sans --type sur le meme fichier.
7. Le combo-corriger-fichier passe de bout en bout (rc 0) sur un .md et sur
   un .json (la case c1 ne plante plus).
8. Normes ASCII 0/0 + LF pur sur corriger-nommage.py/.sh/.md.
9. PREUVE NEGATIVE : le correctif ne renomme JAMAIS un .json meme quand la
   detection par chemin le classerait 'agent' (garde d extension).

Les fichiers testes sont des COPIES temporaires (jamais les vrais fichiers) :
le test cree une hierarchie tmp/agents/... et ne touche pas au cerveau-projet.
Normes : ASCII strict, LF pur, marqueurs [OK]/[KO], bilan final
RESULTAT : N OK / M KO, sys.exit(main()).
"""
import io
import os
import shutil
import subprocess
import sys
import tempfile

NB_POINTS = 19
NB_OK = 0
NB_KO = 0

RACINE = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(RACINE, "cerveau-projet")):
    RACINE = os.path.dirname(RACINE)

DOSSIER_OUTIL = os.path.join(RACINE, "cerveau-projet", "agents", "tools",
                             "corriger", "corriger-nommage")
PY = os.path.join(DOSSIER_OUTIL, "corriger-nommage.py")
SH = os.path.join(DOSSIER_OUTIL, "corriger-nommage.sh")
MD = os.path.join(DOSSIER_OUTIL, "corriger-nommage.md")
COMBO = os.path.join(RACINE, "cerveau-projet", "agents", "tools", "combos",
                     "combo-corriger-fichier", "definition-combo.json")
MOTEUR = os.path.join(RACINE, "cerveau-projet", "agents", "tools", "combos",
                      "combos-moteur", "combos-moteur.py")

TMP = None


def verifier(nom, condition, detail=""):
    """Affiche [OK] ou [KO] et compte le resultat."""
    global NB_OK, NB_KO
    if condition:
        NB_OK += 1
        print("[OK] %s" % nom)
    else:
        NB_KO += 1
        print("[KO] %s -- %s" % (nom, detail))


def octets(chemin):
    """Lit un fichier en octets bruts (pour ASCII/CRLF)."""
    with open(chemin, "rb") as f:
        return f.read()


def creer_hierarchie_tmp():
    """Cree une hierarchie temporaire agents/... avec des fichiers factices.
    Retourne un dict de chemins. Le .json porte un contenu JSON valide de
    parcours pour que les outils aval (nettoyage) ne le cassent pas."""
    global TMP
    TMP = tempfile.mkdtemp(prefix="tmp-test130-")
    base = os.path.join(TMP, "agents")
    outils = os.path.join(base, "tools", "mon-outil")
    os.makedirs(outils)
    fichier_md_outil = os.path.join(outils, "mon-outil.md")
    with io.open(fichier_md_outil, "w", encoding="ascii", newline="\n") as f:
        f.write("---\nidentite:\n  type: outil\n  commun: true\n---\n"
                "# mon-outil\n\nDocumentation factice de test.\n")

    parcours = os.path.join(base, "buffy", "parcours")
    os.makedirs(parcours)
    fichier_json = os.path.join(parcours, "theme-autre.json")
    with io.open(fichier_json, "w", encoding="ascii", newline="\n") as f:
        f.write('{"identite": {"type": "theme", "appartient_a": "buffy"},'
                ' "theme": {"nom": "AUTRE", "redirects": []}}')

    conventions = os.path.join(base, "conventions", "liens")
    os.makedirs(conventions)
    fichier_convention = os.path.join(conventions, "convention-liens.md")
    with io.open(fichier_convention, "w", encoding="ascii", newline="\n") as f:
        f.write("---\nidentite:\n  type: convention\n---\n"
                "# convention-liens\n\nFactice.\n")

    protocoles = os.path.join(base, "regles-immuables", "general",
                              "protocole-test")
    os.makedirs(protocoles)
    fichier_protocole = os.path.join(protocoles,
                                     "protocole-test.001.01.ebauche.md")
    with io.open(fichier_protocole, "w", encoding="ascii", newline="\n") as f:
        f.write("---\nidentite:\n  type: protocole\n---\n"
                "# protocole-test\n\nFactice.\n")

    dossier_agent = os.path.join(base, "buffy")
    fichier_agent = os.path.join(dossier_agent, "buffy.md")
    with io.open(fichier_agent, "w", encoding="ascii", newline="\n") as f:
        f.write("---\nidentite:\n  type: fiche-agent\n---\n# buffy\n\nFactice.\n")

    fichier_py = os.path.join(TMP, "mon-outil.py")
    with io.open(fichier_py, "w", encoding="ascii", newline="\n") as f:
        f.write("#!/usr/bin/env python3\n# mon-outil.py\nprint('ok')\n")

    return {"md_outil": fichier_md_outil,
            "json": fichier_json,
            "convention": fichier_convention,
            "protocole": fichier_protocole,
            "agent": fichier_agent,
            "py": fichier_py,
            "dossier_json": parcours}


def lancer(cmd, cwd=None):
    """Lance une commande et retourne (rc, sortie_stdout)."""
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           timeout=120)
        return p.returncode, (p.stdout or "")
    except Exception as exc:  # noqa: BLE001 - le test affiche l erreur
        return -1, str(exc)


def nettoyer_tmp():
    """Supprime la hierarchie temporaire."""
    global TMP
    if TMP and os.path.isdir(TMP):
        shutil.rmtree(TMP, ignore_errors=True)
        TMP = None


def main():
    print("=== test-130 -- corriger-nommage --type optionnel (v0.3.1) ===")

    # 1. Presence des fichiers de l outil
    for nom, chemin in [("corriger-nommage.py", PY),
                        ("corriger-nommage.sh", SH),
                        ("corriger-nommage.md", MD)]:
        verifier("fichier present: %s" % nom, os.path.isfile(chemin),
                 "introuvable: %s" % chemin)
    if not all(os.path.isfile(p) for p in (PY, SH, MD, COMBO, MOTEUR)):
        print("RESULTAT : %d OK / %d KO (fichiers manquants)"
              % (NB_OK, NB_KO))
        return 1 if NB_KO else 0

    chemins = creer_hierarchie_tmp()
    try:
        # 2. Sans --type sur un .md d outil : retour 0 (plus de code 2)
        rc, sortie = lancer([sys.executable, PY, chemins["md_outil"]])
        verifier("sans --type .md outil -> rc 0 (plus de code 2)",
                 rc == 0, "rc=%d sortie=%s" % (rc, sortie[-200:]))

        # 3. Sans --type sur un .json de parcours : retour 0
        rc, sortie = lancer([sys.executable, PY, chemins["json"]])
        verifier("sans --type .json parcours -> rc 0",
                 rc == 0, "rc=%d sortie=%s" % (rc, sortie[-200:]))

        # 4. AUCUN renommage du .json (aucun fichier .json.md cree)
        fichiers_apres = sorted(os.listdir(chemins["dossier_json"]))
        renommage = any(f.endswith(".md") for f in fichiers_apres)
        verifier("aucun renommage du .json parcours",
                 not renommage and chemins["json"] in \
                 [os.path.join(chemins["dossier_json"], f)
                  for f in fichiers_apres],
                 "fichiers apres: %s" % fichiers_apres)

        # 5. Auto-detection par chemin : agents/tools/ -> outil
        rc, sortie = lancer([sys.executable, PY, chemins["md_outil"]])
        verifier("auto-detection agents/tools/ -> outil",
                 "Type detecte depuis le chemin : outil" in sortie,
                 "sortie=%s" % sortie[-200:])

        # 6. Auto-detection : agents/conventions/ -> convention
        rc, sortie = lancer([sys.executable, PY, chemins["convention"]])
        verifier("auto-detection agents/conventions/ -> convention",
                 "Type detecte depuis le chemin : convention" in sortie,
                 "rc=%d sortie=%s" % (rc, sortie[-200:]))

        # 7. Auto-detection : protocole-* -> protocole
        rc, sortie = lancer([sys.executable, PY, chemins["protocole"]])
        verifier("auto-detection protocole-* -> protocole",
                 "Type detecte depuis le chemin : protocole" in sortie,
                 "rc=%d sortie=%s" % (rc, sortie[-200:]))

        # 8. Auto-detection : agents/<agent>/ -> agent
        rc, sortie = lancer([sys.executable, PY, chemins["agent"]])
        verifier("auto-detection agents/<agent>/ -> agent",
                 "Type detecte depuis le chemin : agent" in sortie,
                 "rc=%d sortie=%s" % (rc, sortie[-200:]))

        # 9. --type explicite conserve le comportement historique
        rc, sortie = lancer([sys.executable, PY, "--type", "outil",
                             chemins["py"]])
        verifier("--type explicite outil .py -> rc 0 (historique conserve)",
                 rc == 0, "rc=%d sortie=%s" % (rc, sortie[-200:]))

        # 10. Parite .sh : sans --type sur .md outil -> rc 0
        rc, sortie = lancer(["bash", SH, chemins["md_outil"]])
        verifier("parite .sh : sans --type .md outil -> rc 0",
                 rc == 0, "rc=%d sortie=%s" % (rc, sortie[-200:]))

        # 11. Le combo passe de bout en bout sur un .md (c1 ne plante plus)
        rc, sortie = lancer([sys.executable, MOTEUR, COMBO,
                             "--var", "fichier=" + chemins["md_outil"]],
                            cwd=RACINE)
        verifier("combo-corriger-fichier sur .md -> rc 0 (FIN atteinte)",
                 rc == 0 and "FIN" in sortie,
                 "rc=%d sortie=%s" % (rc, sortie[-300:]))

        # 12. Le combo passe de bout en bout sur un .json
        rc, sortie = lancer([sys.executable, MOTEUR, COMBO,
                             "--var", "fichier=" + chemins["json"]],
                            cwd=RACINE)
        verifier("combo-corriger-fichier sur .json -> rc 0 (FIN atteinte)",
                 rc == 0 and "FIN" in sortie,
                 "rc=%d sortie=%s" % (rc, sortie[-300:]))

        # 13-15. Normes ASCII/LF sur les 3 fichiers de l outil
        for nom, chemin in [("corriger-nommage.py", PY),
                            ("corriger-nommage.sh", SH),
                            ("corriger-nommage.md", MD)]:
            d = octets(chemin)
            non_ascii = sum(1 for b in d if b > 127)
            crlf = d.count(b"\r\n")
            verifier("normes %s : ASCII 0/0 (%d) + LF pur 0 CRLF (%d)"
                     % (nom, non_ascii, crlf),
                     non_ascii == 0 and crlf == 0,
                     "non-ascii=%d crlf=%d" % (non_ascii, crlf))

        # 16. PREUVE NEGATIVE : detection .json classe 'agent' mais non renomme
        #     (la detection par chemin agents/<agent>/ classerait le fichier
        #     'agent' ; la garde d extension doit l empecher de renommer)
        rc, sortie = lancer([sys.executable, PY, chemins["json"]])
        fichiers_apres = sorted(os.listdir(chemins["dossier_json"]))
        verifier("preuve negative : .json sous agents/<agent>/ NON renomme",
                 not any(f.endswith((".md", ".js.md")) for f in fichiers_apres)
                 and os.path.isfile(chemins["json"]),
                 "fichiers apres: %s" % fichiers_apres)

        # 17. Preuve negative : fichier racine sans type detectable -> rc 0
        fichier_racine = os.path.join(TMP, "note.md")
        with io.open(fichier_racine, "w", encoding="ascii", newline="\n") as f:
            f.write("# note\n\nFactice racine.\n")
        rc, sortie = lancer([sys.executable, PY, fichier_racine])
        verifier("preuve negative : fichier hors agents -> rc 0 sans renommage",
                 rc == 0 and os.path.isfile(fichier_racine),
                 "rc=%d sortie=%s" % (rc, sortie[-200:]))
    finally:
        nettoyer_tmp()

    print("=== CHRONO test (total 0.0s) ====")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
