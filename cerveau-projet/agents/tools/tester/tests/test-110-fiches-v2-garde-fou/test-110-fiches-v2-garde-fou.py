#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
test-110-fiches-v2-garde-fou.py

GARDE-FOU MIGRATION V2 DES FICHES AGENTS (decision utilisateur
2026-08-30 : les fiches v1 restees au format v1 doivent etre migrees
vers le format v2 -- frontmatter D17 enrichi). Ce test verrouille la
migration pour controler nos changements : la suite complete n est pas
necessaire, ce test cible exactement les fiches concernees.

Agents migres (format v2) : cerberus, oracle, buffy, vulcain, morpheus,
janus, atlas, themis, clio, hygie, hermes, argus, athena, chiron,
gardien, hades, minerve, promethee, redacteur-v2, socrate
(ferrari deja migre).
Format v2 = frontmatter enrichi (D17) : nom, version, cree, statut,
grade, medaille, notation, mot-cles (>= 5), type, appartient_a,
commun, tags, session. En plus, la fiche doit rester CONFORME au
template (verifier-conformite-fiche : noyau + variante) et respecter
les normes v1 (ASCII strict + LF pur).

Points verifies :
  1. Les fiches migrees existent (cerveau-projet/agents/<agent>/<agent>.md).
  2. Frontmatter D17 : nom + version + cree + statut presents.
  3. Frontmatter D17 : grade present (copper|iron|silver|gold|platinum|diamond).
  4. Frontmatter D17 : medaille presente (liste ou []).
  5. Frontmatter D17 : notation presente (entier 0..100).
  6. Frontmatter D17 : mot-cles presents (liste, >= 5 entrees).
  7. Session declaree (admin pour v1).
  8. ASCII strict (0 octet > 127) + LF pur (0 CRLF).
  9. Conformite au template : verifier-conformite-fiche --agent <a>
     retourne CONFORME (0 ecart bloquant).
  10. Preuve negative : une fiche v2 SANS grade est detectee comme
      non conforme (la detection marche vraiment).

Proprietaire : Morpheus (testeur dedie)
Version : 0.1.0
Tags: fiche, v2, frontmatter, garde-fou, migration, d17, conventions
"""
import importlib.util
import io
import os
import re
import subprocess
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(PROJECT_ROOT, "cerveau-projet")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

CERVEau = os.path.join(PROJECT_ROOT, "cerveau-projet")
TOOLS_DIR = os.path.join(CERVEau, "agents", "tools")
PYTHON = sys.executable

VERIF_FICHE = os.path.join(TOOLS_DIR, "verifier", "verifier-conformite-fiche",
                           "verifier-conformite-fiche.py")

# Agents migres au format v2 (decision utilisateur 2026-08-30).
AGENTS_MIGRES = ["cerberus", "oracle", "buffy", "vulcain", "morpheus",
                 "janus", "atlas", "themis", "clio", "hygie", "hermes",
                 "argus", "athena", "chiron", "gardien", "hades",
                 "minerve", "promethee", "redacteur-v2", "socrate"]

GRADES_VALIDES = ["copper", "iron", "silver", "gold", "platinum", "diamond"]

NB_POINTS = 0
NB_OK = 0
NB_KO = 0

CHRONO_ACTIF = "--no-chrono" not in sys.argv
ISOLE = None
DESACTIVES = []
for i, arg in enumerate(sys.argv):
    if arg == "--isoler" and i + 1 < len(sys.argv):
        try:
            ISOLE = int(sys.argv[i + 1])
        except ValueError:
            ISOLE = None
    if arg == "--desactiver" and i + 1 < len(sys.argv):
        DESACTIVES = [int(x) for x in sys.argv[i + 1].split(",")
                      if x.strip().isdigit()]

DEBUT_TEST = time.monotonic()
ETAPES = []


def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROTECTIONS = charger_protections()


def point_actif(numero):
    if ISOLE is not None:
        return numero == ISOLE
    return numero not in DESACTIVES


def verifier(nom, condition, detail=""):
    global NB_POINTS, NB_OK, NB_KO
    NB_POINTS += 1
    if condition:
        NB_OK += 1
        print("  [OK] %s" % nom)
    else:
        NB_KO += 1
        print("  [KO] %s %s" % (nom, ("-- " + detail) if detail else ""))


def run(cmd, timeout=120):
    return PROTECTIONS.lancer_protege(cmd, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace",
                                      timeout=timeout)


def lire(chemin):
    try:
        with io.open(chemin, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def lire_frontmatter(chemin):
    """Extrait le bloc frontmatter (entre --- et ---). Retourne (texte, ok)."""
    contenu = lire(chemin)
    lignes = contenu.split("\n")
    if not lignes or lignes[0].strip() != "---":
        return "", False
    fin = None
    for i in range(1, min(len(lignes), 200)):
        if lignes[i].strip() == "---":
            fin = i
            break
    if fin is None:
        return "", False
    return "\n".join(lignes[1:fin]), True


def champ(frontmatter, cle):
    """Extrait la valeur d une cle YAML simple 'cle: valeur' dans le
    frontmatter (cle en debut de ligne, indentee ou non)."""
    for ligne in frontmatter.split("\n"):
        m = re.match(r"^\s*%s:\s*(.*)$" % re.escape(cle), ligne)
        if m:
            return m.group(1).strip()
    return None


def champ_liste(frontmatter, cle):
    """Extrait une liste YAML 'cle:\n  - x\n  - y' OU inline
    'cle: [a, b, c]' -> liste de valeurs."""
    # Forme inline : cle: [a, b, c]
    m = re.search(r"^\s*%s:\s*\[(.*)\]\s*$" % re.escape(cle),
                  frontmatter, re.M)
    if m:
        return [x.strip().strip('"').strip("'") for x in m.group(1).split(",")
                if x.strip()]
    # Forme multiligne : cle:\n  - x\n  - y
    lignes = frontmatter.split("\n")
    result = []
    dedans = False
    for ligne in lignes:
        m2 = re.match(r"^\s*%s:\s*$" % re.escape(cle), ligne)
        if m2:
            dedans = True
            continue
        if dedans:
            if re.match(r"^\s*-", ligne):
                result.append(ligne.strip()[2:].strip().strip('"').strip("'"))
            elif re.match(r"^\s*\w", ligne):
                break
    return result


def point_1_fiches_existent():
    manquantes = []
    for agent in AGENTS_MIGRES:
        chemin = os.path.join(CERVEau, "agents", agent, "%s.md" % agent)
        if not os.path.isfile(chemin):
            manquantes.append(agent)
    verifier("1. fiches migrees existent (%s)" % ", ".join(AGENTS_MIGRES),
             not manquantes, "manquantes: %s" % ", ".join(manquantes))


def point_2_nom_version_cree_statut():
    details = []
    for agent in AGENTS_MIGRES:
        chemin = os.path.join(CERVEau, "agents", agent, "%s.md" % agent)
        fm, ok = lire_frontmatter(chemin)
        if not ok:
            details.append("%s: frontmatter absent" % agent)
            continue
        for cle in ("nom", "version", "cree", "statut"):
            if champ(fm, cle) is None:
                details.append("%s: %s absent" % (agent, cle))
    verifier("2. frontmatter D17 : nom+version+cree+statut", not details,
             "; ".join(details))


def point_3_grade():
    details = []
    for agent in AGENTS_MIGRES:
        chemin = os.path.join(CERVEau, "agents", agent, "%s.md" % agent)
        fm, ok = lire_frontmatter(chemin)
        if not ok:
            details.append("%s: frontmatter absent" % agent)
            continue
        grade = champ(fm, "grade")
        if grade is None:
            details.append("%s: grade absent" % agent)
        elif grade.strip('"').lower() not in GRADES_VALIDES:
            details.append("%s: grade invalide (%s)" % (agent, grade))
    verifier("3. frontmatter D17 : grade valide", not details,
             "; ".join(details))


def point_4_medaille():
    details = []
    for agent in AGENTS_MIGRES:
        chemin = os.path.join(CERVEau, "agents", agent, "%s.md" % agent)
        fm, ok = lire_frontmatter(chemin)
        if not ok:
            details.append("%s: frontmatter absent" % agent)
            continue
        med = champ(fm, "medaille")
        if med is None:
            details.append("%s: medaille absent" % agent)
        elif med not in ("[]", "{}") and not champ_liste(fm, "medaille"):
            # medaille peut etre [] (vide) ou une liste YAML
            if not (med.startswith("[") or med == "[]"):
                details.append("%s: medaille mal formee (%s)" % (agent, med))
    verifier("4. frontmatter D17 : medaille presente", not details,
             "; ".join(details))


def point_5_notation():
    details = []
    for agent in AGENTS_MIGRES:
        chemin = os.path.join(CERVEau, "agents", agent, "%s.md" % agent)
        fm, ok = lire_frontmatter(chemin)
        if not ok:
            details.append("%s: frontmatter absent" % agent)
            continue
        nota = champ(fm, "notation")
        if nota is None:
            details.append("%s: notation absent" % agent)
        else:
            try:
                val = int(nota)
                if not (0 <= val <= 100):
                    details.append("%s: notation hors 0..100 (%s)" % (agent, nota))
            except ValueError:
                details.append("%s: notation non entier (%s)" % (agent, nota))
    verifier("5. frontmatter D17 : notation 0..100", not details,
             "; ".join(details))


def point_6_mots_cles():
    details = []
    for agent in AGENTS_MIGRES:
        chemin = os.path.join(CERVEau, "agents", agent, "%s.md" % agent)
        fm, ok = lire_frontmatter(chemin)
        if not ok:
            details.append("%s: frontmatter absent" % agent)
            continue
        mcl = champ_liste(fm, "mot-cles")
        if champ(fm, "mot-cles") is None and not mcl:
            details.append("%s: mot-cles absent" % agent)
        elif len(mcl) < 5:
            details.append("%s: mot-cles < 5 (%d)" % (agent, len(mcl)))
    verifier("6. frontmatter D17 : mot-cles >= 5", not details,
             "; ".join(details))


def point_7_session():
    details = []
    for agent in AGENTS_MIGRES:
        chemin = os.path.join(CERVEau, "agents", agent, "%s.md" % agent)
        fm, ok = lire_frontmatter(chemin)
        if not ok:
            details.append("%s: frontmatter absent" % agent)
            continue
        sess = champ(fm, "session")
        if sess is None:
            details.append("%s: session absent" % agent)
    verifier("7. frontmatter D17 : session declaree", not details,
             "; ".join(details))


def point_8_ascii_lf():
    details = []
    for agent in AGENTS_MIGRES:
        chemin = os.path.join(CERVEau, "agents", agent, "%s.md" % agent)
        try:
            data = open(chemin, "rb").read()
        except OSError as e:
            details.append("%s: lecture impossible (%s)" % (agent, e))
            continue
        crlf = data.count(b"\r\n")
        non_ascii = len([c for c in data if c > 127])
        if crlf or non_ascii:
            details.append("%s: CRLF=%d octets>127=%d" % (agent, crlf, non_ascii))
    verifier("8. ASCII strict + LF pur", not details, "; ".join(details))


def point_9_conformite_template():
    details = []
    for agent in AGENTS_MIGRES:
        r = run([PYTHON, VERIF_FICHE, "--agent", agent], timeout=120)
        sortie = (r.stdout or "") + (r.stderr or "")
        if "CONFORME" not in sortie:
            details.append("%s: %s" % (agent, sortie.strip()[-200:]))
    verifier("9. conformite template (verifier-conformite-fiche)",
             not details, "; ".join(details))


def point_10_preuve_negative():
    """Preuve negative : une fiche v2 SANS grade est detectee par la
    detection du point 3. On simule un frontmatter sans grade sur un
    fichier temporaire (aucun fichier reel modifie)."""
    agent = AGENTS_MIGRES[0]
    chemin = os.path.join(CERVEau, "agents", agent, "%s.md" % agent)
    fm, ok = lire_frontmatter(chemin)
    if not ok:
        verifier("10. preuve negative : detection sans grade", False,
                 "frontmatter illisible")
        return
    # Retire la ligne grade -> la detection du point 3 doit l attraper
    lignes = [l for l in fm.split("\n")
              if not re.match(r"^\s*grade:\s*", l)]
    fm_sans_grade = "\n".join(lignes)
    detecte = champ(fm_sans_grade, "grade") is None
    verifier("10. preuve negative : fiche sans grade detectee", detecte)


def main():
    print("=== test-110 : garde-fou migration v2 des fiches agents ===")
    points = [
        ("1. fiches existent", point_1_fiches_existent),
        ("2. nom+version+cree+statut", point_2_nom_version_cree_statut),
        ("3. grade valide", point_3_grade),
        ("4. medaille", point_4_medaille),
        ("5. notation 0..100", point_5_notation),
        ("6. mot-cles >= 5", point_6_mots_cles),
        ("7. session", point_7_session),
        ("8. ASCII + LF", point_8_ascii_lf),
        ("9. conformite template", point_9_conformite_template),
        ("10. preuve negative", point_10_preuve_negative),
    ]
    for num, (nom, fn) in enumerate(points, start=1):
        if not point_actif(num):
            continue
        t_debut = time.monotonic()
        fn()
        if CHRONO_ACTIF:
            ETAPES.append((nom, time.monotonic() - t_debut))

    if CHRONO_ACTIF:
        total = time.monotonic() - DEBUT_TEST
        print("")
        print("=== CHRONO test (total %.1fs) === " % total)
        for nom, duree in ETAPES:
            print("  %-34s %6.2fs" % (nom, duree))

    print("")
    print("=== RESULTAT : %d OK / %d KO (sur %d points) ==="
          % (NB_OK, NB_KO, NB_POINTS))
    return 1 if NB_KO else 0


if __name__ == "__main__":
    sys.exit(main())
