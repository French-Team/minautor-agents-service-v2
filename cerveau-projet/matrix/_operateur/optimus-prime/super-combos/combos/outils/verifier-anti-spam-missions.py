#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-anti-spam-missions.py -- Garde : le depot d'une vigie est borne par MISSION

Pourquoi (2026-09-13, MO-070 puis MO-073) : les DEUX vigies ont eu le MEME
defaut, decouvert deux fois -- un anti-bruit qui comptait les ETATS CHANGEANTS
au lieu des MISSIONS. La fiche du createur se remplit UN CHAMP A LA FOIS (chaque
champ = une signature nouvelle -> 4 depots en 3 minutes, MO-070) ; et vigie-portes
signait TOUTES ses observations, y compris les "basses" qui ne partent jamais
dans l'inbox (-> un depot identique par mouvement d'usage, et un plancher repousse
a chaque passe, donc une vigie MUETTE, MO-073).

Ce garde rejoue les incidents REELS sur les fonctions PURES des routines et exige
le resultat ATTENDU. Il est BLOQUANT : sans lui, la meme panne peut revenir par
une refonte de l'anti-spam sans qu'aucune suite ne se plaigne (c'est exactement
ce qui s'est passe entre les deux vigies).

CE QU'IL NE FAIT PAS : il n'execute AUCUN depot (aucune porte `signaler`), ne
touche NI l'inbox NI l'etat NI le journal d'une routine en service. Les routines
sont chargees DANS UN SOUS-PROCESSUS CHACUNE (leurs modules s'appellent tous
`constants`/`commun`/`tour` : les charger ensemble masquerait l'un par l'autre,
lecon L-029).

Usage: python verifier-anti-spam-missions.py [--racine <path>]
       python verifier-anti-spam-missions.py --routine <nom> --racine <path>  (une seule, dans SON processus)
  code 0 = sain, 1 = ecart (liste et nomme), 2 = racine ou routine introuvable.
"""

import argparse
import hashlib
import importlib
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# --- SEUILS ET REFERENCES (aucune valeur en dur dans la logique) -------------
# MO-102 (P5 de la revue MO-098) : le plafond d'un sous-processus n'est plus
# declare ici -- il est LU chez son proprietaire (data/commun/lancement.py).
FORMAT_DATE = "%Y-%m-%d %H:%M:%S"
T0 = datetime.strptime("2026-09-13 13:49:43", FORMAT_DATE)
PAS_SECONDES = 60

# Les routines surveillees (nom = dossier sous matrice/routines/).
ROUTINES = ("vigie-profil", "vigie-portes")

# Incident MO-070 : la fiche USER-PROFIL remplie CHAMP PAR CHAMP (etats successifs
# des champs ATTENDUS encore vides -- mesure reelle : 4 depots en 3 minutes).
CHAMPS_PROFIL = (
    "Pseudo", "Age", "Langue", "Fuseau horaire",
    "Style de conversation", "Sujets d'interet",
    "Mode d'apprentissage", "Niveau technique",
)
ETATS_INCIDENT_PROFIL = (
    ["Pseudo", "Age", "Fuseau horaire", "Style de conversation", "Sujets d'interet",
     "Mode d'apprentissage", "Niveau technique"],
    ["Fuseau horaire", "Sujets d'interet", "Mode d'apprentissage", "Niveau technique"],
    ["Fuseau horaire", "Mode d'apprentissage", "Niveau technique"],
    ["Fuseau horaire", "Niveau technique"],
    [],
)

# Incident MO-073 : trois mouvements d'observations BASSES (rien de notable a
# dire dans l'inbox) et trois VRAIS changements du jeu notable.
ALERTE_BASSE = "basse"
MOUVEMENTS_BASSES_PORTES = (
    [("muette-observation:signaler", ALERTE_BASSE)],
    [("muette-observation:signaler", ALERTE_BASSE), ("nom-inconnu:c-001-lecons", ALERTE_BASSE)],
    [("muette-vivante:signaler", ALERTE_BASSE)],
)
CHANGEMENTS_NOTABLES_PORTES = (
    [("recette:benchmark", "moyenne")],
    [("recette:benchmark", "moyenne"), ("recette:maintenir", "critique")],
    [("recette:pause-session", "moyenne")],
)

DEPOTS_ATTENDUS = {
    "vigie-profil": 1,
    "vigie-portes": 1,
}


def trouver_matrix(racine):
    """Retourne le dossier matrix/, ou None."""
    candidats = [racine / "cerveau-projet" / "matrix", racine / "matrix"]
    if racine.name == "matrix":
        candidats.insert(0, racine)
    for candidat in candidats:
        if (candidat / "matrice").is_dir():
            return candidat
    return None


def empreinte_locale(vides):
    """Cle stable d'un etat de fiche (meme role que la cle de l'etat reel)."""
    return hashlib.sha256("|".join(sorted(vides)).encode("utf-8")).hexdigest()


def ancienne_regle_deux_args(etat, memoire, maintenant):
    """L'ANCIENNE regle de vigie-profil : re-alerte des que la signature change."""
    return (bool(etat["attendus_vides"]) and etat["cle"] != memoire.get("signature", ""),
            "ancienne-regle")


def ancienne_regle_trois_args(signature_actuelle, signature_alertee, ecoule):
    """L'ANCIENNE regle de vigie-portes : aucun plancher de temps."""
    return (signature_actuelle != signature_alertee, "ancienne-regle")


def rejouer_profil(decider, sequence):
    """Rejoue la fiche remplie champ par champ. Rend le nombre de DEPOTS."""
    memoire = {"signature": "", "alerte_le": ""}
    depots = 0
    for index, vides in enumerate(sequence):
        moment = T0 + timedelta(seconds=PAS_SECONDES * index)
        etat = {"attendus_vides": list(vides), "present": True, "cle": empreinte_locale(vides)}
        deposer, _ = decider(etat, memoire, moment)
        if deposer:
            depots += 1
            memoire = {"signature": etat["cle"], "alerte_le": moment.strftime(FORMAT_DATE)}
        if not vides and memoire.get("signature"):
            # Fiche COMPLETE : l'episode se ferme (le tour remet la memoire a zero).
            memoire = {"signature": "", "alerte_le": memoire.get("alerte_le", "")}
    return depots


def rejouer_portes(decider, sequence, selection, signature, secondes_depuis):
    """Rejoue une suite de jeux d'alertes. Rend le nombre de DEPOTS.

    `selection` modelise la BASE de la signature : les alertes NOTABLES (regle
    corrigee) ou TOUTES les alertes (ancienne regle).
    """
    memoire = {"signature": "", "alerte_le": ""}
    depots = 0
    for index, jeu in enumerate(sequence):
        moment = T0 + timedelta(seconds=PAS_SECONDES * index)
        alertes = [{"cle": cle, "niveau": niveau, "porte": cle.split(":")[-1], "detail": cle}
                   for cle, niveau in jeu]
        retenues = selection(alertes)
        if not retenues:
            continue  # le chemin reel s'arrete la : rien de notable, rien a deposer
        signature_actuelle = signature(retenues)
        ecoule = (secondes_depuis(memoire.get("alerte_le", ""), moment)
                  if memoire.get("alerte_le") else None)
        deposer, _ = decider(signature_actuelle, memoire.get("signature", ""), ecoule)
        if deposer:
            depots += 1
            memoire = {"signature": signature_actuelle, "alerte_le": moment.strftime(FORMAT_DATE)}
    return depots


def controler_routine(nom, racine):
    """Controle UNE routine. Retourne (resultats, ecarts)."""
    resultats = []
    ecarts = []
    dossier = racine / "matrice" / "routines" / nom
    if not dossier.is_dir():
        return resultats, ["routine introuvable : " + str(dossier)]

    sys.path.insert(0, str(dossier))
    try:
        # `constants` D'ABORD : c'est lui qui pose les chemins partages dans
        # sys.path (data/commun pour le motif `fiche_profil`). Importer
        # `tour.fonctions` en premier echouait sur `No module named
        # 'fiche_profil'` -- l'ordre reel du chargement (main.py -> boucle ->
        # tour) doit etre reproduit, sinon le garde accuse la routine a tort.
        import constants as constantes
        module = importlib.import_module("tour.fonctions")
    except Exception as erreur:  # noqa: BLE001 -- on AVOUe l'echec, on ne plante pas
        return resultats, ["routine illisible (" + nom + ") : " + str(erreur)]

    # 0. Le plancher EXISTE et c'est un nombre de secondes positif.
    plancher = getattr(constantes, "ANTI_SPAM_SECONDES", None)
    ok_plancher = isinstance(plancher, int) and plancher > 0
    resultats.append(("plancher", ok_plancher,
                      "ANTI_SPAM_SECONDES = " + str(plancher) + " s (secondes murales)"))
    if not ok_plancher:
        ecarts.append(nom + " : ANTI_SPAM_SECONDES absent ou invalide dans constants.py")

    # 1. La decision est une FONCTION, et elle est PURE (rejouable a heure fixe).
    decideur = getattr(module, "decision_depot", None)
    ok_decision = callable(decideur)
    resultats.append(("decision", ok_decision,
                      "decision_depot presente" if ok_decision else "decision_depot ABSENTE"))
    if not ok_decision:
        ecarts.append(nom + " : decision_depot absente de tour/fonctions.py")
        return resultats, ecarts

    # 2. La decision est JOURNALISEE par la passe (aucune suppression silencieuse).
    #    Le journal peut vivre dans tour/entry.py (vigie-profil) ou dans
    #    tour/fonctions.py (vigie-portes) : on lit TOUT le paquet tour/, pas un
    #    seul fichier -- sinon on accuse une routine qui journalise tres bien.
    source = "".join((dossier / "tour" / fichier).read_text(encoding="utf-8", errors="replace")
                     for fichier in ("entry.py", "fonctions.py")
                     if (dossier / "tour" / fichier).is_file())
    ok_trace = "motif" in source
    resultats.append(("trace", ok_trace,
                      "la passe journalise son motif" if ok_trace
                      else "le motif de decision n'est pas journalise"))
    if not ok_trace:
        ecarts.append(nom + " : la passe ne journalise pas le motif de sa decision")

    if nom == "vigie-profil":
        # 3. La borne : la fiche remplie CHAMP PAR CHAMP ne produit QU'UN depot.
        depots = rejouer_profil(decideur, ETATS_INCIDENT_PROFIL)
        attendu = DEPOTS_ATTENDUS[nom]
        ok_borne = depots == attendu
        resultats.append(("borne", ok_borne,
                          "fiche remplie champ par champ : " + str(depots) + " depot(s)"
                          + " (attendu " + str(attendu) + ")"))
        if not ok_borne:
            ecarts.append(nom + " : " + str(depots) + " depot(s) au lieu de " + str(attendu)
                          + " -- le depot n'est plus borne par mission")

        # 4. AUTOTEST : l'ANCIENNE regle doit ETRE ACCUSEE par ce meme rejeu.
        depots_anciens = rejouer_profil(ancienne_regle_deux_args, ETATS_INCIDENT_PROFIL)
        ok_autotest = depots_anciens > attendu
        resultats.append(("autotest", ok_autotest,
                          "l'ancienne regle rejouee produit " + str(depots_anciens)
                          + " depot(s) : le rejeu DETECTE la panne"))
        if not ok_autotest:
            ecarts.append(nom + " : le rejeu ne detecte PAS l'ancienne panne (cobaye suspect, L-032)")

        # 5. Le plancher : un nouveau signal COLLE au dernier est retenu.
        etat_court = {"attendus_vides": ["Pseudo"], "present": True, "cle": empreinte_locale(["Pseudo"])}
        deposer_recent, _ = decideur(etat_court,
                                     {"signature": "", "alerte_le": (T0 - timedelta(seconds=60)).strftime(FORMAT_DATE)},
                                     T0)
        deposer_vieux, _ = decideur(etat_court,
                                    {"signature": "", "alerte_le": (T0 - timedelta(seconds=plancher + 1)).strftime(FORMAT_DATE)},
                                    T0)
        ok_plancher_jeu = (not deposer_recent) and deposer_vieux
        resultats.append(("plancher-joue", ok_plancher_jeu,
                          "retenu sous le plancher, rouvert apres (rien n'est perdu)"))
        if not ok_plancher_jeu:
            ecarts.append(nom + " : le plancher ne retarde pas le depot (ou le supprime)")
    else:
        # 3. La borne : les mouvements d'observations BASSES ne deposent RIEN.
        depots_basses = rejouer_portes(decideur, MOUVEMENTS_BASSES_PORTES,
                                       module.alertes_notables, module.signature,
                                       module.secondes_depuis)
        ok_basses = depots_basses == 0
        resultats.append(("borne", ok_basses,
                          "mouvements d'observations basses : " + str(depots_basses)
                          + " depot(s) (attendu 0)"))
        if not ok_basses:
            ecarts.append(nom + " : une observation basse declenche encore un depot")

        # 4. Les VRAIS changements notables : borne par le temps (1 seul depot).
        depots_notables = rejouer_portes(decideur, CHANGEMENTS_NOTABLES_PORTES,
                                         module.alertes_notables, module.signature,
                                         module.secondes_depuis)
        attendu = DEPOTS_ATTENDUS[nom]
        ok_notables = depots_notables == attendu
        resultats.append(("borne-temps", ok_notables,
                          "3 changements notables en 3 minutes : " + str(depots_notables)
                          + " depot(s) (attendu " + str(attendu) + ")"))
        if not ok_notables:
            ecarts.append(nom + " : " + str(depots_notables) + " depot(s) au lieu de "
                          + str(attendu) + " pour un vrai changement notable")

        # 5. AUTOTEST : l'ancienne regle (signature sur TOUTES les alertes, aucun
        #    plancher) doit etre ACCUSEE par le meme rejeu.
        depots_anciens = rejouer_portes(ancienne_regle_trois_args, MOUVEMENTS_BASSES_PORTES,
                                        lambda alertes: alertes, module.signature,
                                        module.secondes_depuis)
        ok_autotest = depots_anciens > 0
        resultats.append(("autotest", ok_autotest,
                          "l'ancienne regle rejouee produit " + str(depots_anciens)
                          + " depot(s) sur les observations basses : le rejeu DETECTE la panne"))
        if not ok_autotest:
            ecarts.append(nom + " : le rejeu ne detecte PAS l'ancienne panne (cobaye suspect, L-032)")

    return resultats, ecarts


def controler_par_sous_processus(racine):
    """Lance le controle de CHAQUE routine dans SON processus (modules homonymes)."""
    from lancement import delai_sous_processus  # data/commun installe par main()
    resultats = []
    ecarts = []
    for nom in ROUTINES:
        commande = [sys.executable, str(Path(__file__).resolve()),
                    "--routine", nom, "--racine", str(racine)]
        try:
            passe = subprocess.run(commande, capture_output=True, text=True,
                                   encoding="utf-8", errors="replace", timeout=delai_sous_processus())
        except (OSError, subprocess.SubprocessError) as erreur:
            ecarts.append(nom + " : controle injoignable (" + str(erreur) + ")")
            continue
        if passe.stdout and passe.stdout.strip():
            for ligne in passe.stdout.strip().splitlines():
                ligne = ligne.strip()
                if not ligne.startswith("["):
                    continue  # en-tete de la routine : ni OK ni KO
                resultats.append((nom, ligne.startswith("[OK"), ligne))
        if passe.returncode != 0:
            for ligne in (passe.stdout or "").splitlines():
                if ligne.strip().startswith("ECART"):
                    ecarts.append(nom + " : " + ligne.strip()[len("ECART"):].strip(" :"))
            if not (passe.stdout or "").strip():
                ecarts.append(nom + " : code " + str(passe.returncode) + " sans message")
    return resultats, ecarts


def main():
    parser = argparse.ArgumentParser(description="Garde : le depot d'une vigie est borne par mission")
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
        print("ANTI-SPAM -- " + arguments.routine + " (depot borne par mission)")
        for _, ok, detail in resultats:
            print("[" + ("OK" if ok else "KO") + "] " + detail)
        for ecart in ecarts:
            print("ECART : " + ecart)
        return 1 if ecarts else 0

    resultats, ecarts = controler_par_sous_processus(matrix)

    print("VERIFIER ANTI-SPAM MISSIONS -- le depot est borne par mission")
    for routine, ok, detail in resultats:
        print("[" + ("OK" if ok else "KO") + "] " + routine + " : " + detail)
    for ecart in ecarts:
        print("       -> " + ecart)

    if ecarts:
        print("\nVERDICT KO : l'anti-spam d'une vigie n'est plus borne par mission"
              " (voir les ecarts nommes).")
        return 1
    print("\nVERDICT OK : les deux vigies bornent leur depot par mission.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
