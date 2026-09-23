#!/usr/bin/env python3
"""verifier-placeholders.py -- un champ DECLARE ne doit pas CONTREDIRE la mesure (EO-268).

Pourquoi : le pilote declarait duree_s = 0 a chaque cloture -- un PLACEHOLDER pris
pour une mesure. La vue a affiche zero pendant des mois alors que les bornes du
MEME journal donnaient 149 s (L-055 : une valeur qui ment se lit comme un fait),
et AUCUN instrument ne s en plaignait.

CE QU IL ACCUSE, ET RIEN D AUTRE : un champ declare qui CONTREDIT une mesure
calculable depuis le meme document. Un SILENCE n est pas un mensonge : une duree
inconnue (vide) n est jamais accusee.

REVERSEMENT DU 2026-09-21 (demande createur) : ce garde tenait un cas nomme
"zero LEGITIME NON accuse (les bornes donnent bien 0 s)". C ETAIT FAUX, et la
mesure le prouve : 59 missions portent un `debut` a la SECONDE EXACTE de leur
`fin`, parce que le garde anti-fin-orphelin de la porte `noter` cree la borne
manquante au moment ou la fin arrive -- ce n est pas une mission de zero seconde,
c est un debut POSE APRES COUP. La duree de ces missions est INCONNUE (la vue
affiche `inconnue`, plus jamais 0), et un declare POSITIF sur de telles bornes est
un MENSONGE CERTAIN : il affirme une mesure que rien ne peut produire (L-055).
La POPULATION des bornes identiques est DESORMAIS DITE par ce garde (comptee,
nommee) : une duree inconnue qui n est jamais nommee se lit comme une duree.

LA REGLE N EST PAS RECOPIEE : l agregat et le calcul de duree viennent du DOMICILE
(suivi-optimus/vue/fonctions.py). Un garde qui rejoue la regle ne prouve rien (L-032).

Usage: python verifier-placeholders.py [--racine <matrix>] [--auto-test]
  code 0 = sain, 1 = ecart nomme, 2 = racine ou domicile illisible.
"""

import argparse
import importlib.util
import json
import sys
from pathlib import Path

CHAMP = "duree_s"
PLACEHOLDERS = ("", "-", "?", "na", "inconnu", "inconnue", "none", "null")


def charger_domicile(racine):
    """Charge le DOMICILE de la regle (la vue du suivi) -- jamais une copie."""
    # Le domicile vit sous matrice/ (erreur deja faite en MO-202 : resolue sous
    # <racine>/data/outils, la mesure ne trouvait AUCUNE cible). On essaie la
    # forme reelle, puis la forme courte, et le refus NOMME le chemin cherche.
    base = racine / "matrice" / "data"
    if not base.is_dir():
        base = racine / "data"
    outil = base / "outils" / "suivi-optimus"
    chemin = outil / "vue" / "fonctions.py"
    if not chemin.is_file():
        return None, "domicile absent : " + str(chemin)
    if str(outil) not in sys.path:
        sys.path.insert(0, str(outil))
    try:
        spec = importlib.util.spec_from_file_location("vue_suivi_placeholders", str(chemin))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except (ImportError, OSError, SyntaxError, AttributeError) as erreur:
        return None, "domicile ILLISIBLE : " + type(erreur).__name__ + " : " + str(erreur)
    return module, ""


def lire_evenements(racine):
    base = racine / "matrice" / "data"
    if not base.is_dir():
        base = racine / "data"
    chemin = base / "suivi-optimus.jsonl"
    if not chemin.is_file():
        return []
    evenements = []
    with open(chemin, "r", encoding="utf-8") as flux:
        for ligne in flux:
            if ligne.strip():
                try:
                    evenements.append(json.loads(ligne))
                except json.JSONDecodeError:
                    continue
    return evenements


def declarees(evenements, mission):
    """Les valeurs DECLAREES du champ mesure : un silence n est pas une valeur."""
    valeurs = []
    for evenement in evenements:
        if evenement.get("mission") != mission:
            continue
        valeur = str(evenement.get(CHAMP, "") or "").strip()
        if valeur.lower() not in PLACEHOLDERS:
            valeurs.append(valeur)
    return valeurs


def raison_sans_mesure(agregat, vue):
    """POURQUOI aucune duree n est mesurable -- le texte vient du DOMICILE (M-076).

    Deux causes, deux textes : les deux bornes sont le MEME instant (le debut a ete
    pose apres coup), ou elles sont illisibles / inversees. Les recopier ici ferait
    naitre la divergence que ce garde surveille.
    """
    if agregat.get("debut") and agregat["debut"] == agregat.get("fin"):
        return getattr(vue, "DUREE_INCONNUE_BORNES_IDENTIQUES", "bornes identiques")
    return getattr(vue, "DUREE_INCONNUE_BORNES_ILLISIBLES", "bornes illisibles")


def durees_inconnues(agregats, vue):
    """Les missions dont la DUREE n est pas mesurable : la population, NOMMEE.

    Elle n est pas accusee (une duree inconnue n est pas un mensonge) mais elle est
    DITE : sans ce compte, une colonne pleine d `inconnue` resterait inexpliquee,
    et le phenomene (des debuts poses apres coup) redeviendrait invisible.
    """
    missions = []
    for mission, agregat in sorted(agregats.items()):
        if not agregat.get("debut") or not agregat.get("fin"):
            continue
        if vue.calculer_duree(agregat["debut"], agregat["fin"]) is None:
            missions.append(mission)
    return missions


def ecarts_pour(agregats, evenements, vue):
    """Les declares qui CONTREDISENT la mesure des bornes, et rien d autre."""
    ecarts = []
    for mission, agregat in sorted(agregats.items()):
        if not agregat.get("debut") or not agregat.get("fin"):
            continue
        mesure = vue.calculer_duree(agregat["debut"], agregat["fin"])
        if mesure is None:
            # AUCUNE MESURE POSSIBLE : un declare POSITIF affirme alors une duree
            # que les bornes ne peuvent pas produire -- c est un mensonge certain
            # (mesure du 2026-09-21 : 0 mission dans ce cas aujourd hui, l accusation
            # est donc un PIEGE pour l avenir, pas une dette). Un "0" (placeholder)
            # ou un silence ne pretendent rien : ils passent.
            for declaree in sorted(set(declarees(evenements, mission))):
                try:
                    nombre = int(float(declaree))
                except ValueError:
                    ecarts.append(mission + " : " + CHAMP + " declare " + repr(declaree)
                                  + " n est pas un nombre (aucune mesure possible : "
                                  + raison_sans_mesure(agregat, vue) + ")")
                    continue
                if nombre > 0:
                    ecarts.append(mission + " : " + CHAMP + " declare " + str(nombre)
                                  + " alors qu AUCUNE duree n est mesurable ("
                                  + raison_sans_mesure(agregat, vue) + ") -- un declare"
                                  + " positif sur ces bornes se lit comme une mesure (L-055)")
            continue
        # UNE accusation par mission et par VALEUR distincte : le journal porte la
        # meme declaration sur plusieurs evenements (debut ET fin), et 3 lignes
        # identiques se lisent comme du bruit -- mon premier jet les produisait, et
        # c est l AUTOTEST du garde qui l a crie (2 ecarts au lieu de 1 attendu).
        for declaree in sorted(set(declarees(evenements, mission))):
            try:
                nombre = int(float(declaree))
            except ValueError:
                ecarts.append(mission + " : " + CHAMP + " declare " + repr(declaree)
                              + " n est pas un nombre (mesure " + str(mesure) + " s)")
                continue
            if nombre != mesure:
                ecarts.append(mission + " : " + CHAMP + " declare " + str(nombre)
                              + " contre " + str(mesure) + " s mesurees par les bornes"
                              + " -- un declare qui contredit la mesure se lit comme"
                              + " un fait (L-055)")
    return ecarts


def autotest(vue):
    """5 cas : un detecteur jamais vu crier ne prouve rien (L-032).

    Le quatrieme cas REMPLACE "zero LEGITIME NON accuse" (ancienne doctrine,
    renversee le 2026-09-21) : des bornes IDENTIQUES ne mesurent rien, donc un
    declare 0 y est un PLACEHOLDER (non accuse) et un declare 42 y est un MENSONGE
    (accuse). Le cinquieme cas est l accusation POSITIVE : le meme cobaye, un
    declare qui doit mordre.
    """
    base = [{"mission": "MO-901", "action": "debut", "date": "2026-01-01 10:00:00"},
            {"mission": "MO-901", "action": "fin", "date": "2026-01-01 10:02:29"}]
    identiques = [{"mission": "MO-902", "action": "debut",
                   "date": "2026-01-01 10:00:00"},
                  {"mission": "MO-902", "action": "fin",
                   "date": "2026-01-01 10:00:00"}]
    cas = (
        ("contradiction ACCUSEE (0 declare contre 149 s mesurees)",
         [dict(e, duree_s="0") for e in base], 1),
        ("silence NON accuse (duree inconnue, honnete)",
         [dict(e, duree_s="") for e in base], 0),
        ("declare JUSTE NON accuse (149 declare, 149 mesure)",
         [dict(e, duree_s="149") for e in base], 0),
        ("bornes IDENTIQUES + declare 0 NON accuse (placeholder, aucune mesure)",
         [dict(e, duree_s="0") for e in identiques], 0),
        ("bornes IDENTIQUES + declare 42 ACCUSE (mensonge certain)",
         [dict(e, duree_s="42") for e in identiques], 1),
    )
    epreuves = []
    for nom, evenements, attendu in cas:
        obtenu = ecarts_pour(vue.agreger_par_mission(evenements), evenements, vue)
        epreuves.append((nom + " -> " + str(len(obtenu)) + " ecart(s)",
                         len(obtenu) == attendu))
    # LE CAS REEL QUI A DECIDE : des bornes identiques SONT une duree inconnue --
    # le cobaye prouve que la population est VUE (sinon le compte serait muet).
    vues = durees_inconnues(vue.agreger_par_mission(identiques), vue)
    epreuves.append(("bornes identiques COMPTEES comme duree inconnue -> "
                     + str(len(vues)) + " mission(s)", vues == ["MO-902"]))
    return epreuves


def main():
    analyseur = argparse.ArgumentParser()
    analyseur.add_argument("--racine", default="")
    analyseur.add_argument("--auto-test", action="store_true")
    arguments = analyseur.parse_args()
    racine = Path(arguments.racine).resolve() if arguments.racine else next(
        (p for p in [Path(__file__).resolve(), *Path(__file__).resolve().parents]
         if p.name == "matrix"), None)
    if racine is None or not racine.is_dir():
        print("REFUS : racine de la Matrice introuvable (--racine <chemin>).")
        return 2
    vue, erreur = charger_domicile(racine)
    if vue is None:
        print("REFUS : " + erreur)
        return 2
    print("VERIFIER PLACEHOLDERS -- un champ declare ne doit pas contredire la mesure")
    epreuves = autotest(vue)
    for nom, tenu in epreuves:
        print(("  [OK] " if tenu else "  [KO] ") + nom)
    if arguments.auto_test:
        ratees = [nom for nom, tenu in epreuves if not tenu]
        print("  AUTOTEST : " + str(len(epreuves) - len(ratees)) + "/"
              + str(len(epreuves)) + " epreuve(s) tenue(s)")
        return 1 if ratees else 0
    evenements = lire_evenements(racine)
    agregats = vue.agreger_par_mission(evenements)
    # LA POPULATION EST DITE (2026-09-21) : les missions dont la duree n est pas
    # mesurable sont comptees et nommees. Les taire laisserait la vue afficher une
    # colonne d `inconnue` sans cause lisible.
    inconnues = durees_inconnues(agregats, vue)
    if inconnues:
        print("  [--] duree NON MESURABLE : " + str(len(inconnues)) + " mission(s) -- "
              + raison_sans_mesure(agregats[inconnues[0]], vue) + " : "
              + ", ".join(inconnues[:8])
              + (" ..." if len(inconnues) > 8 else ""))
    ecarts = ecarts_pour(agregats, evenements, vue)
    for ecart in ecarts:
        print("  [KO] " + ecart)
    if ecarts:
        print("VERDICT KO : " + str(len(ecarts)) + " champ(s) declare(s) contredisant la mesure.")
        return 1
    print("VERDICT OK : aucun champ declare ne contredit la mesure.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
