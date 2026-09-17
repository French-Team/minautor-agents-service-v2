#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto-suivi -- Super-combo auto-suivi (Optimus Prime)

Orchestre l'ENTRETIEN de la trace d'Optimus, PHASE PAR PHASE, par les portes
officielles de l'outil suivi-optimus (jamais une reecriture a la main).

POURQUOI (decision createur, 2026-09-16) : "il faut lancer un
super-combos-auto-xxx pour le travail du pilote et les mises a jours du fichier
de suivi". Mesure a l'appui -- la vue suivi-optimus.md ne representait pas le
travail :
  - le DETAIL des evenements etait AMPUTE a 200 caracteres ; un bilan de mission
    en fait 2 000 a 3 000 : la vue livrait des phrases coupees au milieu ;
  - seuls 10 evenements par action etaient affiches, sur 246 : aucun recap ;
  - le compteur "Missions finies" comptait les missions PRESENTES, pas celles qui
    portent une FIN ;
  - ses colonnes Fichiers et Portes etaient vides parce que le pilote ne les
    transmettait JAMAIS a la porte `noter`, qui les accepte depuis sa naissance.
Et l'entretien lui-meme reposait sur la MEMOIRE : un `vue` par-ci, un
`coherence` par-la, quand on y pensait. Ce super-combo REMPLACE cette memoire :
le pilote le lance a la cloture de chaque mission.

Phases (chacune est UNE porte officielle -- aucune logique recopiee ici) :
  coherence -- croise la file du pilote et le journal (rien ne les comparait)
  verifier  -- integrite de la BDD (SHA-256) + coherence debut/fin (le marbre juge)
  vue       -- regenere le markdown (recap par mission + bilan par journee)
  rapport   -- MONTRE le travail tel que la vue vient de l'ecrire (lecture seule)

Verbes :
  executer  -- la chaine complete (coherence -> verifier -> vue -> rapport)
  rapide    -- la passe de fin de mission (coherence -> vue), bornee
  status    -- l'etat de la trace, en LECTURE SEULE (aucune ecriture)
  auto-test -- PROUVE que la chaine sait ACCUSER (cobayes en racine jetable)

Codes retour : 0 = les phases ont rendu 0 ; 1 = au moins une phase a ACCUSE
(le verdict est rendu, le texte le dit) ; 2 = refus (porte injoignable, verbe
hors contrat) -- un refus n'est JAMAIS un succes muet.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

# --- Domiciles, declares UNE fois ---------------------------------------------
# La RACINE matrix/ se DETECTE par le MARQUEUR PARTAGE (matrice/data/commun/
# racine.py, M-076) : ici aucun `parents[N]` nu (contrat fondamental, controle
# CHEMINS) -- un nombre de niveaux compte a la main devient faux le jour ou
# l'objet change de place, et il se TAIT en devenant faux. Un fichier vivant sous
# _operateur/ ne peut PAS atteindre data/commun en remontant : c'est le couple
# `matrice/data` qui marque la racine, pas le dossier `commun` seul.
REPERTOIRE_FICHIER = Path(__file__).resolve().parent
BORNES_REMONTEE = 30
_courant = REPERTOIRE_FICHIER
for _ in range(BORNES_REMONTEE):
    if (_courant / "matrice" / "data" / "commun" / "racine.py").is_file():
        break
    _courant = _courant.parent
else:
    raise RuntimeError("Racine matrix/ introuvable en remontant depuis "
                       + str(REPERTOIRE_FICHIER))
REPERTOIRE_MATRIX = _courant
if REPERTOIRE_MATRIX.name != "matrix":
    raise RuntimeError("Structure inattendue : " + str(REPERTOIRE_MATRIX)
                       + " n'est pas le dossier matrix/")
PORTE_SUIVI = REPERTOIRE_MATRIX / "matrice" / "data" / "outils" / "suivi-optimus" / "main.py"
VUE_SUIVI = REPERTOIRE_MATRIX / "matrice" / "suivi-optimus.md"
# Le registre de la famille : le contrat de lancement y vit (verbes acceptes).
# `.parent` (le dossier immediat) et non `parents[N]` : aucune profondeur comptee.
REGISTRE = REPERTOIRE_FICHIER.parent / "registry.json"
NUMERO = "sc-003"

# Phases = les portes officielles consommees, dans l'ordre de la chaine.
PHASES_PORTE = ("coherence", "verifier", "vue")
PHASES_TOUTES = PHASES_PORTE + ("rapport",)
# Bornes DECLAREES : une porte qui ne repond pas ne doit jamais figer le pilote
# (il lance `rapide` a chaque cloture).
LIMITE_PORTE_S = 60
# Sections de la vue que le rapport MONTRE (lecture seule, jamais recalculees).
SECTIONS_RAPPORT = ("Bilan par journee", "Recap par mission")
LIMITE_LIGNES_SECTION = 25


def lancer_porte(verbe, options=()):
    """Lance UNE porte officielle de suivi-optimus. Retourne (code, sortie).

    Le refus est NOMME : une porte absente rend 2 avec son chemin, jamais un
    succes muet (un controle qui ne peut pas echouer ne dit rien -- doctrine
    sc-001). La sortie est ramenee en ASCII : la console Windows tue un enfant
    sur un caractere hors de sa table, et l'entretien de la trace ne doit pas
    dependre du codec de la console.
    """
    if not PORTE_SUIVI.is_file():
        return 2, ("REFUS : la porte suivi-optimus est introuvable (" + str(PORTE_SUIVI)
                   + ") -- aucune phase ne peut etre invoquee.")
    commande = [sys.executable, str(PORTE_SUIVI), verbe] + [str(o) for o in options]
    try:
        resultat = subprocess.run(
            commande, capture_output=True, timeout=LIMITE_PORTE_S, cwd=str(REPERTOIRE_MATRIX),
        )
    except (subprocess.TimeoutExpired, OSError) as erreur:
        return 2, "REFUS : porte " + verbe + " injoignable (" + str(erreur) + ")."
    brut = (resultat.stdout or b"") + (resultat.stderr or b"")
    sortie = brut.decode("utf-8", errors="replace").encode("ascii", "ignore").decode("ascii")
    return resultat.returncode, sortie


def extraire_section(chemin, titre, limite_lignes=LIMITE_LIGNES_SECTION):
    """Retourne les lignes d'une section `## <titre>` d'un markdown, ou None.

    Le RAPPORT ne recalcule rien : il MONTRE ce que la porte `vue` vient
    d'ecrire. Recalculer un bilan ici en ferait une SECONDE verite, qui
    divergerait de la premiere au premier changement d'affichage (L-029).
    """
    try:
        lignes = Path(chemin).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    entete = "## " + titre
    if entete not in lignes:
        return None
    debut = lignes.index(entete)
    fin = len(lignes)
    for rang in range(debut + 1, len(lignes)):
        if lignes[rang].startswith("## "):
            fin = rang
            break
    return lignes[debut:min(fin, debut + limite_lignes)]


def composer_rapport(chemin_vue=None):
    """Retourne les lignes du rapport : ce que la vue dit du travail, borne.

    Si une section manque, on le DIT (jamais un silence qui se lit comme "rien a
    signaler") : une vue plus ancienne que ce super-combo n'a pas les deux
    tableaux de lecture du travail.
    """
    chemin_vue = Path(chemin_vue) if chemin_vue else VUE_SUIVI
    lignes = ["Vue : " + str(chemin_vue)]
    for titre in SECTIONS_RAPPORT:
        section = extraire_section(chemin_vue, titre)
        if section is None:
            lignes.append("SECTION ABSENTE de la vue : " + titre
                          + " (vue anterieure a MO-139 ? regenerer par la phase vue).")
            continue
        lignes.extend(section)
    return lignes


def _chaine(phases, avec_rapport):
    """Execute des phases en SERIE et retourne le pire code (jamais un arret sec).

    Une phase qui accuse n'empeche PAS les suivantes : la trace doit etre
    rafraichie meme quand la coherence crie un ecart (sinon l'ecart reste
    invisible dans la vue, ce qui est exactement le defaut d'origine).
    """
    pire = 0
    for phase in phases:
        code, sortie = lancer_porte(phase)
        print("[PHASE " + phase + "] code " + str(code))
        for ligne in (sortie.strip().splitlines() if sortie.strip() else []):
            print("  " + ligne)
        if code != 0 and pire == 0:
            pire = code
    if avec_rapport:
        print("[PHASE rapport]")
        for ligne in composer_rapport():
            print("  " + ligne)
    return pire


def cmd_executer():
    """Chaine complete : coherence -> verifier -> vue -> rapport."""
    return _chaine(PHASES_PORTE, True)


def cmd_rapide():
    """Passe de fin de mission : coherence -> vue (le pilote l'appelle a chaque cloture).

    Pas de phase `verifier` ici : elle relit la BDD et son empreinte -- c'est la
    passe d'entretien, pas celle de cloture. La vue, elle, DOIT etre a jour a
    chaque fin de mission : c'est ce que le createur ouvre.
    """
    return _chaine(("coherence", "vue"), False)


def cmd_status():
    """Etat de la trace en LECTURE SEULE : aucun fichier n'est ecrit."""
    print("Super-combo auto-suivi -- phases : " + ", ".join(PHASES_TOUTES))
    pire = 0
    for phase in ("coherence", "verifier"):
        code, sortie = lancer_porte(phase)
        print("[PHASE " + phase + "] code " + str(code))
        for ligne in (sortie.strip().splitlines() if sortie.strip() else []):
            print("  " + ligne)
        if code != 0 and pire == 0:
            pire = code
    if VUE_SUIVI.is_file():
        for titre in SECTIONS_RAPPORT:
            present = extraire_section(VUE_SUIVI, titre) is not None
            print("VUE : section '" + titre + "' " + ("presente" if present else "ABSENTE"))
    else:
        print("VUE ABSENTE : " + str(VUE_SUIVI) + " (lancer la phase vue).")
    return pire


# --- AUTO-TEST : prouver que la chaine sait ACCUSER ---------------------------

FILE_COBAYE = {
    "missions": [{"id": "MO-500", "theme": "OUTIL", "statut": "terminee"}],
    "compteur": 500,
    "lot": None,
}


def _evenement(action):
    """Une ligne du journal cobaye : la forme REELLE d'un evenement de la trace."""
    return {
        "date": "2026-01-01 00:00:00",
        "mission": "MO-500",
        "theme": "OUTIL",
        "action": action,
        "detail": "cobaye sc-003",
        "fichiers": [],
        "portes": [],
        "duree_s": "0",
    }


def _poser_racine_cobaye(racine, avec_fin):
    """Pose une racine jetable : file du pilote + journal, avec ou sans fin.

    SANS la fin : la file dit MO-500 `terminee` et le journal ne le sait pas --
    c'est l'ECART que le controle doit crier. AVEC la fin : la paire est saine et
    le controle doit se TAIRE. Les deux cas sont joues : un controle qui accuse
    sans temoin positif ne prouve pas qu'il regarde la bonne chose.
    """
    pilote = racine / "_operateur" / "optimus-prime" / "pilote"
    pilote.mkdir(parents=True, exist_ok=True)
    (pilote / "file-missions-optimus.json").write_text(
        json.dumps(FILE_COBAYE, indent=2) + "\n", encoding="utf-8", newline="\n")
    donnees = racine / "matrice" / "data"
    donnees.mkdir(parents=True, exist_ok=True)
    evenements = [_evenement("debut")] + ([_evenement("fin")] if avec_fin else [])
    (donnees / "suivi-optimus.jsonl").write_text(
        "\n".join(json.dumps(e) for e in evenements) + "\n", encoding="utf-8", newline="\n")


def _verbes_du_registre():
    """Les verbes declares pour CE super-combo dans le registre de la famille, ou None.

    Le contrat de lancement vit dans le registre (le lanceur LIT ce contrat) ;
    le code porte sa propre garde. Deux listes = deux verites : l'auto-test les
    COMPARE (une liste qui a oublie le code fabrique un objet inlancable, une
    liste qui a oublie le registre passe sous le radar du lanceur).
    """
    try:
        with open(REGISTRE, "r", encoding="utf-8") as flux:
            registre = json.load(flux)
    except (OSError, ValueError):
        return None
    for entree in registre.get("super-combos", []):
        if entree.get("id") == NUMERO:
            return list(entree.get("verbes", []))
    return None


def cmd_auto_test():
    """Prouve que la chaine ACCUSE -- sinon la preuve ne prouve rien."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append((nom, bool(condition), detail))

    # 1. Verbe hors contrat : refuse NOMME (jamais un succes muet, jamais auto-test).
    refus = refus_verbe("verbe-inexistant")
    controler("verbe hors contrat refuse",
              "REFUS" in refus and "verbe-inexistant" in refus, refus[:70])

    # 2. Le registre et le code disent la MEME liste de verbes.
    verbes_registre = _verbes_du_registre()
    controler("registre et code d'accord sur les verbes",
              verbes_registre is not None and set(verbes_registre) == set(ROUTES),
              "registre : " + str(verbes_registre))

    with tempfile.TemporaryDirectory() as dossier:
        racine = Path(dossier)

        # 3. TEMOIN NEGATIF : file `terminee` + journal SANS fin -> ECART nomme.
        _poser_racine_cobaye(racine, avec_fin=False)
        code, sortie = lancer_porte("coherence", ("--racine", str(racine)))
        ligne_ecart = [l for l in sortie.splitlines() if l.startswith("ECART")]
        controler("ecart file<->journal ACCUSE",
                  code == 1 and ligne_ecart and "MO-500" in ligne_ecart[0],
                  "code " + str(code) + " | " + (ligne_ecart[0][:70] if ligne_ecart else "aucun ECART"))

        # 4. TEMOIN POSITIF : la meme racine AVEC la fin -> le controle se TAIT.
        _poser_racine_cobaye(racine, avec_fin=True)
        code, sortie = lancer_porte("coherence", ("--racine", str(racine)))
        controler("paire saine -> silence", code == 0 and "ECART" not in sortie,
                  "code " + str(code))

        # 5. Le rapport DIT une section absente au lieu de se taire.
        vide = racine / "vue-vide.md"
        vide.write_text("# rien\n", encoding="utf-8", newline="\n")
        rapport_vide = composer_rapport(vide)
        controler("section absente DITE",
                  extraire_section(vide, "Bilan par journee") is None
                  and any("SECTION ABSENTE" in ligne for ligne in rapport_vide),
                  "vue sans section")

    # 6. Porte absente : le refus est NOMME avec son chemin (jamais un traceback).
    global PORTE_SUIVI
    garde = PORTE_SUIVI
    PORTE_SUIVI = REPERTOIRE_MATRIX / "porte-absente-pour-le-cobaye.py"
    try:
        code, sortie = lancer_porte("vue")
        controler("porte absente -> refus nomme",
                  code == 2 and "REFUS" in sortie and "porte-absente" in sortie,
                  "code " + str(code))
    finally:
        PORTE_SUIVI = garde

    reussis = sum(1 for _, ok, _ in resultats if ok)
    print("[AUTO-TEST] " + str(reussis) + "/" + str(len(resultats)) + " controles")
    for nom, ok, detail in resultats:
        print("  " + ("OK   " if ok else "ECHEC") + " : " + nom
              + (" (" + detail + ")" if detail else ""))
    return 0 if reussis == len(resultats) else 1


# --- Routage ------------------------------------------------------------------

ROUTES = {
    "executer": cmd_executer,
    "rapide": cmd_rapide,
    "status": cmd_status,
    "auto-test": cmd_auto_test,
}


def refus_verbe(verbe):
    """Le message de refus d'un verbe hors contrat (UNE seule formulation)."""
    return ("REFUS : verbe " + repr(verbe) + " hors contrat (verbes acceptes : "
            + ", ".join(ROUTES) + ")")


def main(arguments):
    if not arguments:
        print(__doc__)
        return 2
    verbe = arguments[0]
    if verbe not in ROUTES:
        print(refus_verbe(verbe))
        return 2
    return ROUTES[verbe]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
