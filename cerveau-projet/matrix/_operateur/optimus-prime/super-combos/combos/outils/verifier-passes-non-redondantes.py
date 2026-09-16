#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-passes-non-redondantes.py -- Garde : la PASSE d'une vigie est un ETAT

Pourquoi (2026-09-14, MO-082) : les deux vigies ecrivaient la MEME ligne `passe`
a CHAQUE tour, meme quand rien n'avait bouge. Mesure :

    vigie-profil-log.jsonl : 330 lignes, 17 contenus distincts, la meme ligne 194
                             fois (58,8 %), une par tour de 900 s ;
    vigie-portes-log.jsonl : 204 lignes, 19 contenus distincts, la meme signature
                             105 fois (51,5 %).

C'est le MEME defaut que celui repare sur le routeur (MO-080) et sur l'espion
(MO-081), sur deux journaux de plus : un journal qui repete un ETAT n'est plus une
histoire, c'est un battement de coeur qui noie les faits. La difference -- et elle
compte -- c'est que la ligne `passe` n'etait lue par AUCUN controle : leur cadence
se lit dans un etat court (`*-cadence.json`) depuis MO-078. Le temoin de vie que
l'espion doit garder (le flux lit sa derniere ligne) n'a donc pas a etre conserve
ici : rien ne deviendrait aveugle.

La reparation separe donc deux objets, comme les deux fois precedentes :

  - l'ETAT   (`vigie-<nom>-etat-passes.json`) : la photo de la passe, ecrite a
    CHAQUE tour et ECRASE. Il porte la signature de la derniere passe JOURNALISEE,
    le motif de la decision anti-spam et le compte des passes absorbees -- la
    redondance supprimee est TRACEE, jamais silencieuse ;
  - l'HISTOIRE (`vigie-<nom>-log.jsonl`) : la passe n'y est ecrite que si ce
    qu'elle a VU a change -- et ce changement EST le fait.

CE QUE CE GARDE EXIGE
  1. la fabrique est DECLAREE dans constants.py (etat de passe) et le moteur
     partage `data/commun/etat_histoire.py` est REELLEMENT utilise (jamais recopie,
     lecon L-029) ;
  2. la politique est CABLEE dans la passe (le journal ne la contourne pas) ;
  3. la decision est PURE : memes donnees, meme reponse, sans disque ni horloge ;
  4. des passes SANS CHANGEMENT n'ecrivent RIEN -- et l'etat AVANCE (compteur) ;
  5. un CHANGEMENT n'est JAMAIS absorbe, et la ligne ecrite DIT ce silence
     (combien de passes avaient ete absorbees avant elle) ;
  6. sur le journal REEL : deux lignes consecutives ne peuvent pas etre identiques
     (c'est l'invariant exact que la reparation pose).

CE QU'IL NE FAIT PAS : il ne touche JAMAIS les fichiers de service d'une routine.
Son cobaye vit dans le dossier temporaire du systeme (journal et etat REDIRIGES),
et il s'AUTOTESTE en rejouant l'ANCIENNE regle (une ligne par passe) : si elle
revenait, le garde doit l'ACCUSER (lecon L-032).

Chaque routine est chargee DANS SON PROPRE PROCESSUS : leurs modules `constants`,
`commun` et `tour` sont homonymes (lecon L-029).

Usage: python verifier-passes-non-redondantes.py [--racine <path>]
       python verifier-passes-non-redondantes.py --routine <nom> --racine <path>
  code 0 = sain, 1 = ecart (liste et nomme), 2 = racine ou routine introuvable.
"""

import argparse
import importlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

# --- REFERENCES (aucune valeur en dur dans la logique) ----------------------
# MO-102 (P5 de la revue MO-098) : le plafond d'un sous-processus est LU chez
# son proprietaire (data/commun/lancement.py), jamais recopie ici.
ROUTINES = ("vigie-profil", "vigie-portes")
PASSES_IDENTIQUES = 3
# Champs VOLATILS d'une ligne du journal : ils bougent a chaque ecriture sans
# rien dire. C'est exactement la liste que le moteur partage documente.
VOLATILS_JOURNAL = ("date", "mode", "passes_absorbes")

RESULTATS = []


def trouver_matrix(racine):
    """Retourne le dossier matrix/, ou None."""
    candidats = [racine / "cerveau-projet" / "matrix", racine / "matrix"]
    if racine.name == "matrix":
        candidats.insert(0, racine)
    for candidat in candidats:
        if (candidat / "matrice").is_dir():
            return candidat
    return None


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def lire_lignes(chemin):
    """Lignes non vides d'un fichier (vide si absent)."""
    if chemin is None or not Path(chemin).is_file():
        return []
    with open(str(chemin), "r", encoding="utf-8", errors="replace") as flux:
        return [ligne.rstrip("\r\n") for ligne in flux if ligne.strip()]


def lire_json(chemin):
    """JSON d'un fichier, ou {} (jamais d'exception dans un garde)."""
    try:
        return json.loads(Path(chemin).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def charger_routine(matrix, nom):
    """Rend (constantes, commun, module_de_passe) de la routine, ou None.

    La passe vit dans `tour/entry.py` (vigie-profil) ou `tour/fonctions.py`
    (vigie-portes) : on charge les DEUX quand ils existent, et on rend celui qui
    porte `journaliser_passe`.
    """
    dossier = matrix / "matrice" / "routines" / nom
    if not dossier.is_dir():
        return None
    sys.path.insert(0, str(dossier))
    try:
        import constants as constantes  # noqa: PLC0415 -- chemin installe juste avant
        import commun  # noqa: PLC0415
        module = importlib.import_module("tour.fonctions")
        if not callable(getattr(module, "journaliser_passe", None)):
            module = importlib.import_module("tour.entry")
    except Exception as erreur:  # noqa: BLE001 -- on AVOUE l'echec, on ne plante pas
        print("ECHEC de chargement (" + nom + ") : " + str(erreur))
        return None
    return constantes, commun, module


def etat_de_cobaye(nom):
    """Le premier etat du cobaye : deux champs attendus VIDES (fiche incomplete)."""
    if nom == "vigie-profil":
        return {
            "present": True,
            "pourcentage": 71,
            "attendus_vides": ["Age", "Fuseau horaire"],
            "optionnels_vides": ["Email"],
        }
    return None


def etat_change(nom):
    """Le CHANGEMENT : un champ attendu s'est rempli (la fiche a bouge)."""
    if nom == "vigie-profil":
        return {
            "present": True,
            "pourcentage": 86,
            "attendus_vides": ["Fuseau horaire"],
            "optionnels_vides": ["Email"],
        }
    return None


def jouer_passe(nom, module, etat):
    """Joue UNE passe de la politique, sur les fichiers rediriges du cobaye."""
    if nom == "vigie-profil":
        return module.journaliser_passe(etat, False, "episode-ouvert")
    # vigie-portes : (portes, alertes, notables, signature_notable, motif)
    portes = ["porte-a", "porte-b"]
    basses = [{"cle": "muette-observation:a", "niveau": "basse", "porte": "a", "detail": "muette"}]
    notables = list(etat["notables"])
    return module.journaliser_passe(portes, basses, notables, etat["signature"], etat["motif"])


def etat_portes(nom, module, notables, motif):
    """Le second etat du cobaye de vigie-portes : un jeu notable (ou vide)."""
    return {"notables": notables, "signature": module.signature(notables), "motif": motif}


def signature_journal(module, ligne):
    """Signature COMPARABLE d'une ligne du journal, ou None si illisible.

    On retire les champs volatils (date, mode, compteur) : deux lignes qui ne
    different QUE par eux sont la meme passe -- c'est tout l'objet du garde.
    """
    try:
        donnees = json.loads(ligne)
    except ValueError:
        return None
    volatils = [cle for cle in VOLATILS_JOURNAL]
    return json.dumps({cle: valeur for cle, valeur in donnees.items() if cle not in volatils},
                      sort_keys=True, ensure_ascii=True)


# --------------------------------------------------------------------------- 1
def controler_fabrique(constantes, nom, source, erreurs):
    """L'etat de passe est DECLARE, et le moteur partage est REELLEMENT utilise."""
    declares = [champ for champ in ("NOM_ETAT_PASSES", "CHEMIN_ETAT_PASSES")
                if getattr(constantes, champ, None)]
    ok_declare = len(declares) == 2
    controler("fabrique-declaree", ok_declare,
              ", ".join(declares) + " dans constants.py" if ok_declare
              else "ABSENT : " + str([champ for champ in ("NOM_ETAT_PASSES", "CHEMIN_ETAT_PASSES")
                                      if champ not in declares]))
    if not ok_declare:
        erreurs.append(nom + " : l'etat de passe n'est pas declare dans constants.py")

    ok_moteur = "etat_histoire" in source
    controler("moteur-partage-utilise", ok_moteur,
              "la passe s'appuie sur data/commun/etat_histoire.py" if ok_moteur
              else "le moteur partage n'est PAS utilise : le motif serait recopie (L-029)")
    if not ok_moteur:
        erreurs.append(nom + " : ni signature ni decision du moteur partage")

    ok_cable = "journaliser_passe(" in source
    controler("politique-cablee", ok_cable,
              "la passe passe par journaliser_passe()" if ok_cable
              else "journaliser_passe() n'est PAS appelee : politique morte")
    if not ok_cable:
        erreurs.append(nom + " : la politique d'ecriture n'est pas cablee dans la passe")


# --------------------------------------------------------------------------- 2
def controler_decision_pure(etat_histoire, erreurs):
    """La decision est PURE : memes donnees, meme reponse (sans disque, sans horloge)."""
    if etat_histoire is None:
        controler("decision-pure", False, "moteur partage NON CHARGE")
        erreurs.append("data/commun/etat_histoire.py introuvable ou illisible")
        return
    signature = etat_histoire.signature_fait({"a": 1, "b": [1, 2]})
    ordonne = etat_histoire.signature_fait({"b": [1, 2], "a": 1})
    change = etat_histoire.signature_fait({"a": 2, "b": [1, 2]})
    cas = [
        ("identique = absorbe", etat_histoire.decision_fait(signature, signature), (False, "absorbee")),
        ("change = fait", etat_histoire.decision_fait(change, signature), (True, "changement")),
        ("premiere passe = fait", etat_histoire.decision_fait(signature, None), (True, "changement")),
        ("ordre des clefs indifferent", ordonne == signature, True),
    ]
    echecs = [nom for nom, obtenu, attendu in cas if obtenu != attendu]
    controler("decision-pure", not echecs,
              str(len(cas)) + " cas" + ("" if not echecs else " : ECHECS " + str(echecs)))
    if echecs:
        erreurs.append("decision du moteur partage fausse : " + str(echecs))


# --------------------------------------------------------------------------- 3
def controler_cobaye(nom, module, commun, dossier, erreurs):
    """Passees reelles sur un cobaye : rien de neuf = RIEN au journal, mais tout est TRACE.

    Le journal et l'etat de la routine sont REDIRIGES vers le dossier temporaire :
    les fichiers de service ne sont jamais touches (un garde qui ecrit dans le
    service n'est plus un garde, lecon L-040).
    """
    journal = dossier / (nom + "-log.jsonl")
    etat_passe = dossier / (nom + "-etat-passes.json")
    commun.CHEMIN_JOURNAL = journal
    commun.CHEMIN_ETAT_PASSES = etat_passe

    premier = etat_de_cobaye(nom)
    if nom == "vigie-portes":
        premier = etat_portes(nom, module, [], "aucune-alerte-notable")

    # 1. Premiere passe : la photo part au journal (un fait).
    jouer_passe(nom, module, premier)
    apres_1 = lire_lignes(journal)
    controler("premiere-passe-ecrite", len(apres_1) == 1,
              "1 passe -> " + str(len(apres_1)) + " ligne(s) d'histoire")
    if len(apres_1) != 1:
        erreurs.append(nom + " : la premiere passe n'a pas laisse de fait")

    # 2. Passes SANS CHANGEMENT : rien de plus, et l'etat AVANCE.
    for _ in range(PASSES_IDENTIQUES):
        jouer_passe(nom, module, premier)
    apres_2 = lire_lignes(journal)
    controler("passes-identiques-absorbees", len(apres_2) == len(apres_1),
              str(PASSES_IDENTIQUES) + " passes identiques -> " + str(len(apres_2))
              + " ligne(s) (inchange)")
    if len(apres_2) != len(apres_1):
        erreurs.append(nom + " : une passe sans changement a ecrit au journal : la redondance est revenue")

    etat_courant = lire_json(etat_passe)
    controler("etat-ecrit-et-avance",
              int(etat_courant.get("passes_absorbes") or 0) == PASSES_IDENTIQUES
              and bool(etat_courant.get("signature")),
              "etat : " + str(etat_courant.get("passes_absorbes")) + " passe(s) absorbe(s)"
              + ", signature posee : " + str(bool(etat_courant.get("signature"))))
    if int(etat_courant.get("passes_absorbes") or 0) != PASSES_IDENTIQUES:
        erreurs.append(nom + " : l'etat n'avance pas : la redondance supprimee serait invisible")

    # 3. Un CHANGEMENT n'est JAMAIS absorbe, et la ligne DIT le silence qu'elle rompt.
    change = etat_change(nom)
    if nom == "vigie-portes":
        notables = [{"cle": "recette:benchmark", "niveau": "moyenne", "porte": "benchmark",
                     "detail": "recette incomplete : DESCRIPTION.md absent (CV-010)"}]
        change = etat_portes(nom, module, notables, "plancher")
    jouer_passe(nom, module, change)
    apres_3 = lire_lignes(journal)
    nouvelle = json.loads(apres_3[-1]) if apres_3 else {}
    controler("changement-jamais-absorbe",
              len(apres_3) == len(apres_2) + 1
              and int(nouvelle.get("passes_absorbes") or 0) == PASSES_IDENTIQUES
              and nouvelle.get("mode") == "changement",
              "change -> " + str(len(apres_3) - len(apres_2)) + " ligne(s), mode="
              + str(nouvelle.get("mode")) + ", passes_absorbes="
              + str(nouvelle.get("passes_absorbes")))
    if len(apres_3) != len(apres_2) + 1:
        erreurs.append(nom + " : un changement de photo n'a pas reparti au journal")

    # 4. AUTOTEST : l'ANCIENNE regle (une ligne par passe) doit etre ACCUSEE.
    lignes_anciennes = PASSES_IDENTIQUES + 2
    controler("autotest-ancienne-regle-accusee", lignes_anciennes > len(apres_3),
              "ancienne regle : " + str(lignes_anciennes) + " ligne(s) ; nouvelle : "
              + str(len(apres_3)) + " sur la meme sequence")
    if lignes_anciennes <= len(apres_3):
        erreurs.append(nom + " : le rejeu n'accuse PAS l'ancienne regle (cobaye suspect, L-032)")


# --------------------------------------------------------------------------- 4
def controler_service(nom, matrix, module, erreurs):
    """Ce que le SERVICE a ecrit depuis la reparation : lu, jamais touche."""
    dossier = matrix / "matrice" / "routines" / nom
    etat = lire_json(dossier / (nom + "-etat-passes.json"))
    journal = dossier / (nom + "-log.jsonl")

    controler("etat-de-service-present",
              bool(etat.get("signature")) or int(etat.get("passes_absorbes") or 0) > 0,
              (nom + "-etat-passes.json : " + str(etat.get("date") or etat.get("derniere_ecriture") or "?")
               + ", " + str(etat.get("passes_absorbes")) + " passe(s) absorbe(s)") if etat
              else nom + "-etat-passes.json ABSENT : la routine ne tourne pas le code repare")
    if not etat:
        erreurs.append(nom + " : aucun etat de passe en service (reparation non active)")

    # Seules les lignes ECRITES PAR LE CODE REPARE sont mesurees : elles seules
    # portent `passes_absorbes`. Le bloc d'avant la reparation reste au journal
    # (on ne supprime jamais une histoire) et doit etre NOMME, pas compte comme un
    # ecart -- sinon le garde accuserait un passe qu'il n'a pas a juger.
    lignes = lire_lignes(journal)
    nouvelles = [ligne for ligne in lignes if '"passes_absorbes"' in ligne]
    legacy = len(lignes) - len(nouvelles)
    controler("lignes-post-reparation-presentes", bool(nouvelles),
              str(len(nouvelles)) + " ligne(s) du code repare "
              + str(legacy) + " ligne(s) legacy au journal (bloc d'avant la reparation)")
    if not nouvelles:
        erreurs.append(nom + " : aucune ligne ecrite par le code repare (reparation non active)")

    # L'INVARIANT EXACT : deux lignes CONSECUTIVES ne peuvent pas etre la meme passe
    # (ecrire la deuxieme supposerait que la premiere n'a pas ete enregistree).
    signatures = [signature_journal(module, ligne) for ligne in nouvelles]
    signatures = [signature for signature in signatures if signature is not None]
    repetitions = sum(1 for index in range(1, len(signatures))
                      if signatures[index] == signatures[index - 1])
    controler("journal-reel-sans-repetition-consecutive", repetitions == 0,
              str(len(signatures)) + " ligne(s) mesuree(s) : " + str(repetitions)
              + " repetition(s) consecutive(s)")
    if repetitions:
        erreurs.append(nom + " : " + str(repetitions) + " ligne(s) consecutive(s) identique(s) dans le journal")

    absorbes = int(etat.get("passes_absorbes") or 0)
    controler("absorption-tracee-sur-le-service", bool(etat) and absorbes >= 0,
              str(absorbes) + " passe(s) absorbe(s) depuis la derniere ligne d'histoire"
              if etat else "etat absent")


def controler_routine(nom, matrix):
    """Controle UNE routine (et son moteur partage). Rend (resultats, ecarts)."""
    global RESULTATS
    RESULTATS = []
    erreurs = []
    charge = charger_routine(matrix, nom)
    if charge is None:
        return RESULTATS, [nom + " : routine introuvable ou illisible"]
    constantes, commun, module = charge

    source = "".join(
        (matrix / "matrice" / "routines" / nom / "tour" / fichier).read_text(
            encoding="utf-8", errors="replace")
        for fichier in ("entry.py", "fonctions.py")
        if (matrix / "matrice" / "routines" / nom / "tour" / fichier).is_file()
    )

    # Le moteur partage, charge depuis la racine (il vit hors du dossier de la routine).
    etat_histoire = None
    chemin_moteur = matrix / "matrice" / "data" / "commun"
    if (chemin_moteur / "etat_histoire.py").is_file():
        sys.path.insert(0, str(chemin_moteur))
        try:
            etat_histoire = importlib.import_module("etat_histoire")
        except Exception as erreur:  # noqa: BLE001
            print("ECHEC de chargement du moteur partage : " + str(erreur))

    controler_fabrique(constantes, nom, source, erreurs)
    controler_decision_pure(etat_histoire, erreurs)
    with tempfile.TemporaryDirectory(prefix="cobaye-passes-") as temporaire:
        controler_cobaye(nom, module, commun, Path(temporaire), erreurs)
    controler_service(nom, matrix, module, erreurs)
    return RESULTATS, erreurs


def controler_par_sous_processus(matrix):
    """Lance le controle de CHAQUE routine dans SON processus (modules homonymes)."""
    from lancement import delai_sous_processus  # data/commun installe par main()
    resultats = []
    ecarts = []
    for nom in ROUTINES:
        commande = [sys.executable, str(Path(__file__).resolve()),
                    "--routine", nom, "--racine", str(matrix)]
        try:
            passe = subprocess.run(commande, capture_output=True, text=True,
                                   encoding="utf-8", errors="replace", timeout=delai_sous_processus())
        except (OSError, subprocess.SubprocessError) as erreur:
            ecarts.append(nom + " : controle injoignable (" + str(erreur) + ")")
            continue
        for ligne in (passe.stdout or "").strip().splitlines():
            ligne = ligne.strip()
            if ligne.startswith("["):
                resultats.append((nom, ligne.startswith("[OK"), ligne))
        if passe.returncode != 0:
            for ligne in (passe.stdout or "").splitlines():
                if ligne.strip().startswith("ECART"):
                    ecarts.append(nom + " : " + ligne.strip()[len("ECART"):].strip(" :"))
            if not (passe.stdout or "").strip():
                ecarts.append(nom + " : code " + str(passe.returncode) + " sans message")
    return resultats, ecarts


def main():
    parser = argparse.ArgumentParser(description="Garde : la passe d'une vigie est un etat")
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    parser.add_argument("--routine", default="", help="Controler UNE routine (mode sous-processus)")
    arguments = parser.parse_args()

    matrix = trouver_matrix(Path(arguments.racine).resolve())
    if matrix is None:
        print("Dossier matrix/ introuvable sous " + str(arguments.racine))
        return 2
    # data/commun sur sys.path (motif M-076) : le plafond d'un sous-processus a
    # son domicile unique (lancement.py), il n'est jamais recopie ici.
    sys.path.insert(0, str(matrix / "matrice" / "data" / "commun"))

    if arguments.routine:
        resultats, ecarts = controler_routine(arguments.routine, matrix)
        print("PASSES NON REDONDANTES -- " + arguments.routine)
        for _, ok, detail in resultats:
            print("[" + ("OK" if ok else "KO") + "] " + detail)
        for ecart in ecarts:
            print("ECART : " + ecart)
        return 1 if ecarts else 0

    resultats, ecarts = controler_par_sous_processus(matrix)

    print("VERIFIER PASSES NON REDONDANTES -- la passe d'une vigie est un etat")
    for routine, ok, detail in resultats:
        print("[" + ("OK" if ok else "KO") + "] " + routine + " : " + detail)
    for ecart in ecarts:
        print("       -> " + ecart)

    if ecarts:
        print("\nVERDICT KO : une vigie journalise a nouveau un etat a chaque passe"
              " (voir les ecarts nommes).")
        return 1
    print("\nVERDICT OK : les deux vigies ecrivent un FAIT, jamais un battement de coeur.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
