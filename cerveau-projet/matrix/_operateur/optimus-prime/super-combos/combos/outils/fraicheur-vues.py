#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fraicheur-vues.py -- ACCUSER UNE VUE DE SUIVI QUI N EST PLUS A JOUR (MO-568).

LE FAUT, MESURE AVANT. Les vues de suivi (les `.md` REGENERABLES) disent l etat
du pilote, de la Matrice, d une routine. Elles se regenerent par une porte, donc
A LA DEMANDE -- et une porte qu on ne joue pas ne se signale pas. Une vue
perimee continue d avoir l air fraiche : elle porte une date, des chiffres, un
tableau bien mis en page. Rien ne distinguait "mesure a 04:10" de "mesure a
hier", et le lecteur qui la consultait recevait des FAITS MORTS.

CE QUE CETTE PORTE FAIT. Elle lit une DECLARATION
(`suivi-parties/frais-declarees.json`) qui nomme, pour chaque vue : la porte
qui la regenere, ses SOURCES, le DELAI au-dela duquel elle est perimee, et le
COUT de la rafraichir. Elle mesure ensuite le RETARD entre le sceau de la vue
et la source la plus recente, et ACCUSE en nommant la porte a jouer.

CE QU ELLE NE FAIT PAS, ET C EST CHOISI.
- Elle ne REGENERE rien. Rafraichir une vue est une DECISION : la vue affiche ce
  qu elle a juge, et un outil qui la rejoue en douce effacerait la preuve meme
  qu elle etait perimee.
- Elle ne DEVINE ni la porte, ni les sources, ni le seuil : les trois sont
  declares. Un outil qui invente son seuil ne rend plus de justice.
- Elle ne juge pas l URGENCE. Elle donne le fait (le retard) et le prix (les
  frais declares) ; relire ou regenerer maintenant reste au lecteur, parce que
  le cout d une vue depend de ce qu on va en faire.

LES CINQ VERDICTS.
  a_jour    : le retard est sous la tolerance declaree.
  perime    : il la depasse -- ACCUSE, avec la porte a jouer.
  en_avance : le sceau est POSTERIEUR a la source la plus recente (retard
              negatif). Ce n est pas une faute : le sceau peut dater d avant
              qu une source ne bouge. DIT, jamais traite comme un defaut.
  absente   : la vue est declaree et le fichier n existe pas -- accuse.
  illisible : le fichier existe mais ne porte AUCUN sceau. Une vue qu on ne
              peut pas dater, on ne peut pas la declarer fraiche -- accuse.
  non_declaree : LE SIXIEME, et celui qui ferme l angle mort. Les cinq autres
              mesurent des vues qu on a NOMMEES ; rien n accusait une vue
              qu on n a jamais nommee, donc une vue neuve -- celle que
              personne n a encore enregistree -- etait invisible par
              construction. Le PERIMETRE declare (racines + motif + exclusions
              motives) donne le moyen de DECOUVRIR les vues : tout fichier du
              perimetre sans entree dans la declaration est ACCUSE, nomme, et
              son remede est de le declarer ou de l exclure -- jamais de
              l ignorer en silence.

LES EXCLUSIONS SONT DITES, MEME S I LEUR FICHIER N EXISTE PAS. Une exclusion
que personne ne lit disparait au premier renommage, et le perimetre se ferme
sans bruit. Le rapport les nomme donc toujours, avec leur motif.

LE NOM `retard_secondes`, ET PAS `age_secondes`. Une collision de homonyme avec
un autre `age_secondes` du parc faisait tressaillir la mesure du 2026-10-03 :
le resultat affichait le nombre d une AUTRE vue, sans qu on le voie. Ici le nom
dit ce qu il mesure -- l ECART entre la source et la vue, pas l age de la vue.
Une mesure qui ne dit pas ce qu elle mesure ne peut pas etre relue.

L AUTO-TEST joue sur des FAITS FABRIQUES, dans un repertoire temporaire cree
puis detruit PAR LE TEST LUI MEME : il ne touche jamais une vue reelle et il ne
laisse rien derriere lui. Le cobaye MORD (vue perimee, vue absente, vue sans
sceau, source declaree absente, source la plus recente reperee) et le
contre-temoin EPARGNE (vue a jour, vue en avance).

Usage :
  python3 fraicheur-vues.py              le rapport, en clair
  python3 fraicheur-vues.py --json       la vue en JSON (pour un appelant)
  python3 fraicheur-vues.py --auto-test  les epreuves sur faits fabriques

code 0 = aucune vue perimee ; code 1 = au moins une vue a rafraichir.
"""
import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

# --- L ANCRAGE : la racine de la MATRICE, montee par MARQUEUR (M-088) ---------
_OUTIL = Path(__file__).resolve().parent
_MATRICE = _OUTIL
while _MATRICE.name != "matrix" and _MATRICE.parent != _MATRICE:
    _MATRICE = _MATRICE.parent

# L ANCRAGE, ET POURQUOI PAS `detecter_racine`. Les chemins de la declaration
# sont relatifs a la racine de la MATRICE (`cerveau-projet/matrix`), comme ceux
# que lit `fraicheur` dans ses sources. Or `detecter_racine` rend la racine du
# WORKSPACE (`.../analyste-in-console`) : ancree la, la declaration se
# cherchait un dossier `_operateur/` a la racine du workspace, et la porte
# disait INTROUVABLE sur une declaration qui existe. `_MATRICE` -- le dossier
# nomme `matrix`, remonte par MARQUEUR, jamais par un nombre de parents (M-088)
# -- est donc l ancrage, et il est refuse explicitement s il n existe pas.
if not (_MATRICE / "matrice" / "data").is_dir():
    raise RuntimeError("Racine matrix introuvable par marqueur depuis " + str(_OUTIL))
RACINE = _MATRICE
CHEMIN_DECLARATION = RACINE / "_operateur" / "optimus-prime" / "suivi-parties" / "frais-declarees.json"

FORMAT_SCEAU = "%Y-%m-%d %H:%M:%S"
MOTIF_DEFAUT = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"


def lire_declaration(chemin=None):
    """(declaration, message). Jamais d exception : une porte qui leve n accuse rien."""
    chemin = Path(chemin) if chemin else CHEMIN_DECLARATION
    try:
        donnees = json.loads(chemin.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, "DECLARATION INTROUVABLE : " + str(chemin)
    except (OSError, ValueError) as erreur:
        return None, ("DECLARATION ILLISIBLE (" + type(erreur).__name__ + " : "
                      + str(erreur)[:80] + ") : " + str(chemin))
    if not isinstance(donnees, dict) or not isinstance(donnees.get("vues"), list):
        return None, "DECLARATION MAL FORMEE (aucune liste `vues`) : " + str(chemin)
    return donnees, ""


def sceau_de(texte, motif=None):
    """La PREMIERE date-heure du texte, ou None si la vue ne porte AUCUN sceau.

    La PREMIERE, et pas la derniere : une vue porte souvent la date de sa
    generation en tete, et celle d un evenement rappele plus bas. Prendre la
    derniere ferait paraitre fraiche une vue qui ne l est pas.
    """
    trouve = re.search(motif or MOTIF_DEFAUT, texte)
    if not trouve:
        return None
    try:
        return datetime.strptime(trouve.group(0), FORMAT_SCEAU)
    except ValueError:
        return None


def source_la_plus_recente(sources, racine):
    """(chemin, date) de la source la PLUS RECENTE, et la liste des absentes.

    Les absentes sont RENDUES : une source declaree et introuvable est un
    defaut de la declaration, pas un detail. Le silence la cacherait, et le
    retard serait alors calcule sur un sous-ensemble -- un chiffre qui a l
    air juste et ne l est pas.
    """
    plus_recent, chemin_plus_recent = None, None
    absentes = []
    for source in sources:
        chemin = Path(racine) / str(source)
        try:
            date = datetime.fromtimestamp(chemin.stat().st_mtime)
        except (OSError, ValueError):
            absentes.append(str(source))
            continue
        if plus_recent is None or date > plus_recent:
            plus_recent, chemin_plus_recent = date, source
    return chemin_plus_recent, plus_recent, absentes


def mesurer_vue(vue, racine, motif_defaut=MOTIF_DEFAUT):
    """Mesure UNE vue declaree. Rend sa ligne de rapport (jamais d exception)."""
    ligne = {
        "id": str(vue.get("id", "?")),
        "fichier": str(vue.get("fichier", "")),
        "porte": str(vue.get("porte", "")),
        "tolerance_secondes": vue.get("tolerance_secondes"),
        "frais_secondes": (vue.get("frais") or {}).get("valeur"),
        "sources": [str(s) for s in (vue.get("sources") or [])],
        "sources_absentes": [],
        "source_la_plus_recente": None,
        "sceau": None,
        "retard_secondes": None,
        "verdict": None,
        "accusation": "",
    }
    chemin = Path(racine) / ligne["fichier"]
    if not ligne["fichier"]:
        ligne["verdict"] = "illisible"
        ligne["accusation"] = "vue declaree SANS fichier : rien a mesurer"
        return ligne
    try:
        texte = chemin.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError) as erreur:
        ligne["verdict"] = "absente"
        ligne["accusation"] = ("vue declaree et fichier INTROUVABLE : " + str(chemin)
                               + " (" + type(erreur).__name__ + ")")
        return ligne

    motif = str(vue.get("motif_sceau") or motif_defaut)
    sceau = sceau_de(texte, motif)
    if sceau is None:
        ligne["verdict"] = "illisible"
        ligne["accusation"] = ("la vue ne porte AUCUN sceau (motif " + motif
                               + ") : on ne peut pas dire qu elle est a jour")
        return ligne
    ligne["sceau"] = sceau.strftime(FORMAT_SCEAU)

    source, date_source, absentes = source_la_plus_recente(ligne["sources"], racine)
    ligne["sources_absentes"] = absentes
    ligne["source_la_plus_recente"] = source
    if absentes:
        ligne["verdict"] = "illisible"
        ligne["accusation"] = ("source(s) DECLAREE(S) introuvable(s), le retard "
                               "serait calcule sur un sous-ensemble : "
                               + ", ".join(absentes))
        return ligne
    if date_source is None:
        ligne["verdict"] = "illisible"
        ligne["accusation"] = "aucune source declaree : le retard n a pas de sens"
        return ligne

    retard = (date_source - sceau).total_seconds()
    ligne["retard_secondes"] = int(round(retard))
    try:
        tolerance = float(vue.get("tolerance_secondes", 0))
    except (TypeError, ValueError):
        tolerance = 0.0
    if retard < 0:
        ligne["verdict"] = "en_avance"
    elif retard <= tolerance:
        ligne["verdict"] = "a_jour"
    else:
        ligne["verdict"] = "perime"
        ligne["accusation"] = (
            "vue PERIMEE : son sceau est de " + str(int(round(retard))) + " s en retard"
            " sur " + str(source) + ", au-dela de la tolerance declaree ("
            + str(int(tolerance)) + " s) -- porte a jouer : " + ligne["porte"])
    return ligne


def mesurer_toutes(declaration, racine, motif_defaut=MOTIF_DEFAUT):
    """Toutes les vues declarees, dans l ORDRE de la declaration."""
    return [mesurer_vue(vue, racine, motif_defaut) for vue in declaration.get("vues", [])]


def decouvrir_vues(declaration, racine):
    """(vues presentees, exclusions) du PERIMETRE declare.

    Les vues sont DECOUVERTES, pas supposees : le perimetre dit ou chercher et
    sur quel nom. Une exclusion porte un MOTIF, et le rapport le dit toujours --
    une exclusion muette disparait au premier renommage, et le perimetre se
    ferme sans bruit (le meme piege que les exemptions visibles).
    """
    perimetre = declaration.get("perimetre") or {}
    motif = re.compile(str(perimetre.get("motif") or MOTIF_DEFAUT))
    exclus = []
    for entree in perimetre.get("exclus") or []:
        if isinstance(entree, dict):
            exclus.append({"fichier": str(entree.get("fichier", "")),
                           "motif": str(entree.get("motif", ""))})
        else:
            exclus.append({"fichier": str(entree), "motif": "(aucun motif donne)"})
    exclus_fichiers = {e["fichier"] for e in exclus}
    trouvees = []
    for base in perimetre.get("racines") or []:
        dossier = Path(racine) / str(base)
        if not dossier.is_dir():
            continue
        for chemin in sorted(dossier.rglob("*.md")):
            if ".bak" in chemin.name or not motif.match(chemin.name):
                continue
            relatif = str(chemin.relative_to(racine)).replace("\\", "/")
            if relatif not in exclus_fichiers:
                trouvees.append(relatif)
    return trouvees, exclus


def accuser_non_declarees(declaration, racine, chemin_declaration):
    """Les vues du perimetre qui ne sont pas declarees. Chacune est une LIGNE."""
    trouvees, exclus = decouvrir_vues(declaration, racine)
    declarees = {str(v.get("fichier", "")) for v in declaration.get("vues", [])}
    lignes = []
    for fichier in trouvees:
        if fichier in declarees:
            continue
        lignes.append({
            "id": "non-declaree/" + Path(fichier).stem,
            "fichier": fichier,
            "porte": "",
            "tolerance_secondes": None,
            "frais_secondes": None,
            "sources": [],
            "sources_absentes": [],
            "source_la_plus_recente": None,
            "sceau": None,
            "retard_secondes": None,
            "verdict": "non_declaree",
            "accusation": (
                "vue PRESENTE dans le perimetre et NON DECLAREE : personne ne surveille "
                "sa fraicheur, donc elle ne sera jamais accusee. Declare-la (porte, "
                "sources, tolerance_secondes, frais) dans " + str(chemin_declaration)
                + ", ou exclue-la du perimetre AVEC son motif."),
        })
    return lignes, exclus


def rapport(lignes, exclus=None):
    """Le verdict, la liste de ce qui doit etre joue, et les exclusions DITES."""
    perimes = [l for l in lignes if l["verdict"] == "perime"]
    defauts = [l for l in lignes
               if l["verdict"] in ("absente", "illisible", "non_declaree")]
    return {
        "nb_vues": len(lignes),
        "verdict": "KO" if (perimes or defauts) else "OK",
        "code": 1 if (perimes or defauts) else 0,
        "vues": lignes,
        "non_declarees": [l["fichier"] for l in lignes if l["verdict"] == "non_declaree"],
        "perimetre_exclus": exclus or [],
        # La porte d une vue NON DECLAREE est vide -- et c est justement ce qu il
        # faut reparer. Afficher une ligne `id :  (retard None s)` se lirait
        # comme une donnee manquante ; elle dit donc que la porte MANQUE.
        "a_jouer": [{"id": l["id"],
                     "porte": l["porte"] or "(aucune : la vue n est pas declaree)",
                     "retard_secondes": l["retard_secondes"],
                     "frais_secondes": l["frais_secondes"]}
                    for l in (perimes + defauts)],
    }


# --- L AUTO-TEST : des faits FABRIQUES, un repertoire que le test detruit ----
def auto_test():
    import shutil
    echecs = []

    def verifie(nom, condition, observe):
        if condition:
            print("  OK   " + nom)
            return
        print("  KO   " + nom + " -- observe : " + str(observe))
        echecs.append(nom)

    base = Path(tempfile.mkdtemp(prefix="fraicheur-vues-"))
    try:
        moment = datetime(2026, 10, 4, 4, 10, 0)

        def poser(nom, contenu):
            chemin = base / nom
            chemin.write_text(contenu, encoding="utf-8", newline="\n")
            return chemin

        # Une source datee de `secondes` APRES le sceau de la vue : positif = la
        # source a bouge apres la mesure, donc la vue est en RETARD de `secondes`.
        # NEGATIF = la source est anterieure, la vue est en avance (pas une faute).
        def poser_source(nom, secondes):
            chemin = base / ("src-" + nom)
            chemin.write_text("x", encoding="utf-8")
            stamp = (moment + timedelta(seconds=secondes)).timestamp()
            os.utime(chemin, (stamp, stamp))
            return "src-" + nom

        # 1. LE COBAYE : la vue perimee se fait ACCUSER, porte nommee.
        poser_source("a.txt", 3600)
        poser("v-perimee.md", "Mesure du 2026-10-04 04:10:00 | fines : 3\n")
        # 2. LE CONTRE-TEMOIN : la vue a jour passe.
        poser_source("b.txt", 10)
        poser("v-a-jour.md", "Mesure du 2026-10-04 04:10:00 | fines : 3\n")
        # 3. EN AVANCE : un sceau posterieur n est PAS une faute.
        poser_source("c.txt", -10)
        poser("v-avance.md", "Mesure du 2026-10-04 04:10:00 | fines : 3\n")
        # 4. SANS SCEAU : une vue qu on ne peut pas dater, on ne peut pas l absoudre.
        poser("v-sans-sceau.md", "Aucune date ici.\n")
        # 5. DECLAREE ET ABSENTE.
        # 6. SOURCES : celle qui manque est nommee, jamais ignoree.
        # 7. LA PLUS RECENTE : parmi trois, la bonne.
        poser_source("d1.txt", 100)
        poser_source("d2.txt", 5000)
        poser_source("d3.txt", 800)
        poser("v-plusrecente.md", "Mesure du 2026-10-04 04:10:00 | fines : 3\n")

        def vue(fichier, sources, tolerance=300, identifiant="v"):
            return {"id": identifiant, "fichier": fichier, "porte": "porte-test",
                    "tolerance_secondes": tolerance, "frais": {"valeur": 1.0},
                    "sources": sources}

        l = mesurer_vue(vue("v-perimee.md", ["src-a.txt"]), base)
        verifie("1. une vue perimee est ACCUSEE, porte nommee",
                l["verdict"] == "perime" and "porte-test" in l["accusation"]
                and l["retard_secondes"] >= 3599, l)

        l = mesurer_vue(vue("v-a-jour.md", ["src-b.txt"]), base)
        verifie("2. contre-temoin : une vue a jour passe",
                l["verdict"] == "a_jour" and not l["accusation"], l)

        l = mesurer_vue(vue("v-avance.md", ["src-c.txt"]), base)
        verifie("3. un sceau en avance n est pas une faute",
                l["verdict"] == "en_avance", l)

        l = mesurer_vue(vue("v-sans-sceau.md", ["src-c.txt"]), base)
        verifie("4. une vue sans sceau est illisible, pas absous",
                l["verdict"] == "illisible" and "sceau" in l["accusation"], l)

        l = mesurer_vue(vue("v-absente.md", ["src-c.txt"]), base)
        verifie("5. une vue declaree et absente est nommee",
                l["verdict"] == "absente", l)

        l = mesurer_vue(vue("v-perimee.md", ["src-a.txt", "src-absent.txt"]), base)
        verifie("6. une source declaree introuvable est NOMMEE, jamais ignoree",
                l["verdict"] == "illisible" and "src-absent.txt" in l["accusation"], l)

        l = mesurer_vue(vue("v-plusrecente.md", ["src-d1.txt", "src-d2.txt", "src-d3.txt"]),
                        base)
        verifie("7. c est la source la PLUS RECENTE qui est retenue",
                l["source_la_plus_recente"] == "src-d2.txt" and l["verdict"] == "perime", l)

        l = mesurer_vue(vue("v-perimee.md", []), base)
        verifie("8. une vue sans source declaree est illisible, pas muette",
                l["verdict"] == "illisible", l)

        vide = rapport(mesurer_toutes({"vues": []}, base))
        verifie("9. une declaration vide donne zero vue, pas une erreur muette",
                vide["nb_vues"] == 0 and vide["verdict"] == "OK", vide)

        # --- L ANGLE MORT (MO-571) : une vue qu on n a pas NOMMEE -----------
        # Le perimetre DECOUVRE ; ce qui n est pas declare est accuse.
        perimetre = {"critere": "vue", "racines": ["vues"],
                     "motif": "^suivi-[a-z0-9-]*\\.md$",
                     "exclus": [{"fichier": "vues/regles/suivi-marbre.md",
                                 "motif": "MARBRE : decide par le createur"}]}
        (base / "vues" / "regles").mkdir(parents=True)
        poser("vues/suivi-neuve.md", "Mesure du 2026-10-04 04:10:00 | fines : 3\n")
        poser("vues/regles/suivi-marbre.md", "suivi- mais pas un visuel\n")
        poser("vues/pas-une-vue.md", "ce nom ne tombe pas dans le perimetre\n")

        declaration = {"vues": [], "perimetre": perimetre}
        non_declarees, exclus = accuser_non_declarees(
            declaration, base, "declaration.json")
        verifie("10. une vue du perimetre NON DECLAREE est accusee et nommee",
                [l["fichier"] for l in non_declarees] == ["vues/suivi-neuve.md"]
                and non_declarees[0]["verdict"] == "non_declaree",
                non_declarees)
        verifie("11. un fichier EXCLU n est pas accuse, et son motif est DIT",
                not any("suivi-marbre" in l["fichier"] for l in non_declarees)
                and exclus and "MARBRE" in exclus[0]["motif"],
                (non_declarees, exclus))
        # L exclusion est dite MEME si son fichier a disparu : une exclusion
        # muette disparait au premier renommage.
        declaration["perimetre"]["exclus"].append(
            {"fichier": "vues/absent-depuis-longtemps.md", "motif": "fichier deja gone"})
        _lignes, exclus = accuser_non_declarees(declaration, base, "declaration.json")
        verifie("12. une exclusion dont le fichier est ABSENT reste dite",
                any("absent-depuis-longtemps" in e["fichier"] for e in exclus), exclus)
    finally:
        shutil.rmtree(base, ignore_errors=True)

    print("")
    if echecs:
        print("AUTO-TEST : " + str(len(echecs)) + " en echec -> " + ", ".join(echecs))
        return 1
    print("AUTO-TEST : 12/12.")
    return 0


def main(argv=None):
    analyseur = argparse.ArgumentParser(add_help=True)
    analyseur.add_argument("--json", action="store_true")
    analyseur.add_argument("--auto-test", action="store_true")
    arguments = analyseur.parse_args(argv)

    if arguments.auto_test:
        return auto_test()

    declaration, message = lire_declaration()
    if declaration is None:
        print(message)
        return 2
    lignes = mesurer_toutes(declaration, RACINE,
                            str(declaration.get("motif_sceau_defaut") or MOTIF_DEFAUT))
    non_declarees, exclus = accuser_non_declarees(declaration, RACINE,
                                                  CHEMIN_DECLARATION)
    lignes = lignes + non_declarees
    verdict = rapport(lignes, exclus)

    if arguments.json:
        print(json.dumps(verdict, ensure_ascii=True, sort_keys=True))
        return verdict["code"]

    print("VUES DE SUIVI : " + str(verdict["nb_vues"]) + " declaree(s) -- verdict "
          + verdict["verdict"])
    for ligne in lignes:
        retard = ("retard " + str(ligne["retard_secondes"]) + " s"
                  if ligne["retard_secondes"] is not None else "retard non mesure")
        print("  [" + str(ligne["verdict"]).upper().rjust(10) + "] " + ligne["id"]
              + " -- " + retard + " (tolerance " + str(ligne["tolerance_secondes"])
              + " s, frais " + str(ligne["frais_secondes"]) + " s) : " + ligne["fichier"])
        if ligne["accusation"]:
            print("      -> " + ligne["accusation"])
    if verdict["non_declarees"]:
        print("")
        print("NON DECLAREES (le perimetre les trouve, la declaration ne les nomme pas) :")
        for fichier in verdict["non_declarees"]:
            print("  " + fichier)
    if verdict["perimetre_exclus"]:
        # DITES MEME SI LE FICHIER N EXISTE PLUS : une exclusion muette disparait
        # au premier renommage, et le perimetre se ferme sans bruit.
        print("")
        print("EXCLUES DU PERIMETRE (dites meme si le fichier est absent) :")
        for entree in verdict["perimetre_exclus"]:
            print("  " + entree["fichier"] + " -- " + entree["motif"])
    if verdict["a_jouer"]:
        print("")
        print("A JOUER :")
        for entree in verdict["a_jouer"]:
            print("  " + str(entree["id"]) + " : " + str(entree["porte"])
                  + " (retard " + str(entree["retard_secondes"]) + " s, cout declare "
                  + str(entree["frais_secondes"]) + " s)")
    return verdict["code"]


if __name__ == "__main__":
    sys.exit(main())
