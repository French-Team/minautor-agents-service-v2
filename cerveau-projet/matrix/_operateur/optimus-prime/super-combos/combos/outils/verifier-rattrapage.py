#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-rattrapage.py -- Garde : le pilote COMBLE les fichiers non traces (EO-133).

POURQUOI (audit de fin de round du 2026-09-16, arbitrage createur) : la vue
`suivi-optimus.md` ne lit QUE le journal. Une modification notee au DOMICILE
(`modifications-par-fichier.json`) apres la cloture d'une mission n'y apparait donc
JAMAIS -- mesure : la colonne `Fichiers` affichait un tiret pour MO-136 alors que
10 fichiers etaient REELLEMENT modifies, 2 de plus pour MO-132, et 576 fichiers sur
80 missions invisibles depuis la naissance de la derivation (MO-139). Il a fallu
les recrire A LA MAIN dans le journal. Le createur a tranche entre deux voies :
(a) la vue lit le domicile (deux deriveurs sur la meme verite, M-076), ou (b) le
PILOTE rattrape a chaque cloture. C'est (b) : la vue reste un rendereur, et celui
qui ECRIT la trace comble le trou.

CE QU'IL EXIGE :
  1. MOTEUR SAIN : sur fixtures JETABLES, une mission dont le domicile porte un
     fichier absent du journal est DETECTEE, avec les BONS fichiers -- un fichier
     deja dit n'est jamais renote, et une mission absente du domicile est epargnee.
  2. IDEMPOTENT : une seconde passe, quand la ligne est ecrite, ne note RIEN. Un
     rattrapage qui doublerait fabriquerait le desordre qu'il repare.
  3. JAMAIS MUET : journal illisible ou domicile illisible -> AUCUNE ecriture (un
     rattrapage qui devine serait pire qu'un rattrapage qui se tait) ET le fait est
     DIT (L-037).
  4. CABLE A LA CLOTURE, ET AVANT LA VUE : `rattraper_fichiers_non_traces()` est
     appele dans `fin/fonctions.py` AVANT `entretenir_suivi()`. L'ordre n'est pas
     un detail : la vue est regeneree par l'entretien, donc un rattrapage place
     apres elle ne serait visible qu'au tour suivant -- la cecite d'une mission
     exactement corrigee par MO-139.
  5. ACTION DECLAREE : le rattrapage note par la PORTE, avec une action de la liste
     FERMEE du marbre (`decouverte`). Une action inventee serait REFUSEE par la
     porte et le rattrapage se tairait (c'est le defaut de MO-136/EO-123, deja
     paye une fois).
  6. UN SEUL DERIVEUR : la REGLE de derivation (le tag, ou la mention en TETE du
     detail, fenetre declaree) vit dans UN module -- celui qui la DECLARE (`constants.py`)
     et celui qui l'EMPLOIE (`commun.py`). Une seconde copie deriverait en silence.

L'AUTOTEST le PIEGE (lecon L-032) : le controle de cablage est rejoue sur une
source AMPUTEE de l'appel -- il doit l'ACCUSER. Un garde qui ne peut pas crier ne
prouve rien.

CE QU'IL NE FAIT PAS : le moteur est eprouve sur des fixtures JETABLES ; le journal
reel et le domicile reel ne sont JAMAIS ecrits (lecture seule du code et des
fixtures).

Usage: python verifier-rattrapage.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = zone introuvable.
"""

import argparse
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
from pathlib import Path

# Les domiciles : declares UNE fois, jamais recopies dans la logique.
FICHIER_COMMUN = Path("_operateur") / "optimus-prime" / "pilote" / "commun.py"
FICHIER_CLOTURE = (Path("_operateur") / "optimus-prime" / "pilote" / "fin"
                   / "fonctions.py")
FICHIER_ACTIONS = (Path("matrice") / "data" / "outils" / "suivi-optimus"
                   / "constants.py")
DOSSIER_ZONE = Path("_operateur") / "optimus-prime"

APPEL_RATTRAPAGE = "rattraper_fichiers_non_traces()"
APPEL_ENTRETIEN = "entretenir_suivi()"
ACTION_ATTENDUE = "decouverte"
REGLE_DERIVATION = "FENETRE_MENTION_DETAIL"

RESULTATS = []


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def trouver_racine(racine):
    """Retourne le dossier matrix/ (celui qui porte le pilote), ou None."""
    for candidat in (racine, racine / "cerveau-projet" / "matrix", racine / "matrix"):
        if (candidat / FICHIER_COMMUN).is_file():
            return candidat
    return None


def charger_commun(racine):
    """Charge le commun du pilote SANS passer par la porte (lecture du moteur)."""
    chemin = racine / FICHIER_COMMUN
    dossier = chemin.parent
    if str(dossier) not in sys.path:
        sys.path.insert(0, str(dossier))
    specification = importlib.util.spec_from_file_location("commun_verifie_mo148", chemin)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def fixture(dossier):
    """Domicile + journal JETABLES : un trou attendu par mission, une epargnee."""
    domicile = dossier / "modifications.json"
    journal = dossier / "journal.jsonl"
    domicile.write_text(json.dumps({
        "fichiers": {
            "a.py": {"modifications": [{"tags": ["MO-001"], "detail": "MO-001 : fait"}]},
            "b.py": {"modifications": [{"tags": [], "detail": "MO-001 : fait aussi"}]},
            "c.py": {"modifications": [{"tags": ["MO-002"], "detail": "autre"}]},
        }
    }, ensure_ascii=False), encoding="utf-8")
    lignes = [
        json.dumps({"mission": "MO-001", "theme": "PILOTE", "action": "fin",
                    "fichiers": ["a.py"]}),
        json.dumps({"mission": "MO-002", "theme": "OUTIL", "action": "fin", "fichiers": []}),
        json.dumps({"mission": "MO-003", "theme": "AUDIT", "action": "fin",
                    "fichiers": ["z.py"]}),
    ]
    journal.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    return domicile, journal


def cablage(texte):
    """(cable, avant_la_vue) : l'appel existe, et il precede l'entretien de la vue."""
    if APPEL_RATTRAPAGE not in texte:
        return False, False
    if APPEL_ENTRETIEN not in texte:
        return True, False
    return True, texte.index(APPEL_RATTRAPAGE) < texte.index(APPEL_ENTRETIEN)


def utilisateurs_de_la_regle(zone, garde):
    """Les modules de la zone qui EMPLOIENT la regle de derivation (hors garde)."""
    trouves = []
    for chemin in sorted(zone.rglob("*.py")):
        if "__pycache__" in chemin.parts or ".bak" in chemin.name:
            continue
        if chemin.resolve() == garde.resolve():
            continue  # un garde ne s'audite pas lui-meme (il cite le marqueur)
        try:
            texte = chemin.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if REGLE_DERIVATION in texte:
            trouves.append(chemin.relative_to(zone).as_posix())
    return trouves


def main():
    analyseur = argparse.ArgumentParser(description="Garde du rattrapage des fichiers non traces")
    analyseur.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = analyseur.parse_args()

    racine = trouver_racine(Path(arguments.racine).resolve())
    if racine is None:
        print("Zone introuvable depuis " + arguments.racine)
        return 2
    zone = racine / DOSSIER_ZONE

    ecarts = []
    commun = charger_commun(racine)
    dossier = Path(tempfile.mkdtemp(prefix="verifier-rattrapage-"))
    domicile, journal = fixture(dossier)
    commun.CHEMIN_MODIFICATIONS = domicile
    commun.CHEMIN_MARBRE = journal

    # 1. LE MOTEUR : le trou est vu, avec les bons fichiers, et les epargnes le sont.
    trous = commun.missions_au_domicile_sans_trace()
    obtenu = [(mission, fichiers) for mission, _theme, fichiers in trous]
    attendu = [("MO-001", ["b.py"]), ("MO-002", ["c.py"])]
    controler("moteur-sain", obtenu == attendu,
              "MO-001 -> b.py (a.py est DEJA dit), MO-002 -> c.py, MO-003 epargnee"
              if obtenu == attendu
              else "trouve " + str(obtenu) + " au lieu de " + str(attendu))
    if obtenu != attendu:
        ecarts.append("moteur du rattrapage : detection fausse (" + str(obtenu) + ")")

    # 2. IDEMPOTENCE : la ligne ecrite, la seconde passe ne note plus rien.
    journal.write_text("\n".join([
        json.dumps({"mission": "MO-001", "theme": "PILOTE", "action": "fin",
                    "fichiers": ["a.py"]}),
        json.dumps({"mission": "MO-001", "theme": "PILOTE", "action": "decouverte",
                    "fichiers": ["b.py"]}),
        json.dumps({"mission": "MO-002", "theme": "OUTIL", "action": "decouverte",
                    "fichiers": ["c.py"]}),
    ]) + "\n", encoding="utf-8")
    appels = []
    vrai_noter = commun.noter_journal

    def porte_factice(mission, theme, action, detail, duree_s="0", si_absent=False,
                      fichiers=None, portes=None):
        appels.append((mission, list(fichiers or [])))
        return 0, "simule"

    commun.noter_journal = porte_factice
    missions, fichiers_n, message = commun.rattraper_fichiers_non_traces()
    controler("idempotent", (missions, fichiers_n, message, appels) == (0, 0, "", []),
              "seconde passe : 0 mission, 0 fichier, la porte n'est PAS appelee"
              if (missions, fichiers_n, appels) == (0, 0, [])
              else "la seconde passe a encore ecrit : " + str(appels))
    if (missions, fichiers_n, appels) != (0, 0, []):
        ecarts.append("rattrapage non idempotent (il double ce qu'il a deja ecrit)")

    # 3. JAMAIS MUET : lecture impossible -> aucune ecriture, et le fait est DIT.
    muets = []
    for nom, chemin_casse in (("journal-illisible", dossier / "absent" / "journal.jsonl"),
                              ("domicile-illisible", dossier / "absent.json")):
        appels.clear()
        ancien_marbre, ancien_domicile = commun.CHEMIN_MARBRE, commun.CHEMIN_MODIFICATIONS
        if nom == "journal-illisible":
            commun.CHEMIN_MARBRE = chemin_casse
        else:
            commun.CHEMIN_MARBRE = journal
            commun.CHEMIN_MODIFICATIONS = chemin_casse
        tampon = io.StringIO()
        with contextlib.redirect_stdout(tampon):
            resultat = commun.rattraper_fichiers_non_traces()
        dit = "illisible" in tampon.getvalue()
        commun.CHEMIN_MARBRE, commun.CHEMIN_MODIFICATIONS = ancien_marbre, ancien_domicile
        if not (resultat[:2] == (0, 0) and appels == [] and dit):
            muets.append(nom)
    controler("jamais-muet", not muets,
              "journal ou domicile illisible : 0 ecriture, et le fait est DIT"
              if not muets else "MUET sur : " + ", ".join(muets))
    if muets:
        ecarts.append("lecture impossible mais silence total : " + ", ".join(muets))
    commun.noter_journal = vrai_noter

    # 4 + 5. LE CABLAGE, ET SON ORDRE (l'appel doit preceder l'entretien de la vue).
    texte_cloture = (racine / FICHIER_CLOTURE).read_text(encoding="utf-8", errors="replace")
    cable, avant = cablage(texte_cloture)
    controler("cable-a-la-cloture", cable,
              APPEL_RATTRAPAGE + " est appele dans fin/fonctions.py"
              if cable else "l'appel a DISPARU de la cloture -- plus rien ne comble les trous")
    controler("avant-la-vue", avant,
              "l'appel precede " + APPEL_ENTRETIEN + " (la vue montre le rattrapage du meme tour)"
              if avant else "l'appel est ABSENT ou place APRES l'entretien : la vue aurait un"
              " tour de retard")
    if not cable:
        ecarts.append("rattrapage non cable a la cloture")
    if not avant:
        ecarts.append("rattrapage place apres l'entretien de la vue (cecite d'un tour)")

    # 6. L'ACTION EST DECLAREE (liste fermee du marbre) : sinon la porte REFUSE.
    texte_actions = (racine / FICHIER_ACTIONS).read_text(encoding="utf-8", errors="replace")
    action_declaree = '"' + ACTION_ATTENDUE + '"' in texte_actions
    controler("action-declaree", action_declaree,
              "l'action " + ACTION_ATTENDUE + " est declaree dans la liste fermee du marbre"
              if action_declaree
              else "l'action " + ACTION_ATTENDUE + " n'est PAS declaree : la porte la"
              " refuserait en silence (defaut de MO-136)")
    if not action_declaree:
        ecarts.append("action " + ACTION_ATTENDUE + " absente de la liste fermee du marbre")

    # 7. UN SEUL DERIVEUR : la regle de derivation n'a pas de seconde copie.
    utilisateurs = utilisateurs_de_la_regle(zone, Path(__file__))
    attendus = {FICHIER_COMMUN.relative_to(DOSSIER_ZONE).as_posix()}
    surplus = [chemin for chemin in utilisateurs
               if chemin not in attendus and not chemin.endswith("constants.py")]
    controler("un-seul-deriveur", not surplus,
              "la regle vit dans " + FICHIER_COMMUN.name + " (declaree dans constants.py)"
              if not surplus
              else "SECONDE COPIE de la regle dans : " + ", ".join(surplus))
    if surplus:
        ecarts.append("regle de derivation recopiee : " + ", ".join(surplus))

    # 8. AUTOTEST (L-032) : le controle de cablage doit ACCUSER une source ampute.
    ampute = texte_cloture.replace("rattraper_fichiers_non_traces()", "SANS_APPEL()")
    cable_ampute, _avant_ampute = cablage(ampute)
    epreuves = [
        ("complete acceptee", cable and avant),
        ("appel absent ACCUSE", not cable_ampute),
        ("ordre stable (deux lectures, meme verdict)",
         cablage(texte_cloture) == (cable, avant)),
        ("detecteur sensible a la fixture",
         commun.missions_au_domicile_sans_trace() == []),
    ]
    reussies = sum(1 for _nom, ok in epreuves if ok)
    controler("autotest", reussies == len(epreuves),
              "piege (" + str(reussies) + "/" + str(len(epreuves)) + ")"
              if reussies == len(epreuves)
              else "rate : " + ", ".join(nom for nom, ok in epreuves if not ok))
    if reussies != len(epreuves):
        ecarts.append("autotest du rattrapage rate")

    print("\nVERIFIER RATTRAPAGE -- la vue ne lit que le journal : c'est le pilote qui comble")
    if ecarts or any(not ok for _n, ok, _d in RESULTATS):
        print("\nVERDICT KO : les fichiers non traces ne sont plus combles, ou ils le sont mal"
              " (voir les ecarts nommes).")
        return 1
    print("\nVERDICT OK : le rattrapage detecte les trous du domicile, ne double jamais, se"
          " tait proprement, et il tourne AVANT la vue.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
