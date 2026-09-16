#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verifier-observations-non-redondantes.py -- Garde : les observations d'une passe sont un ETAT

Pourquoi (2026-09-14, MO-081) : la passe de `espion-integrite` journalisait
QUATORZE observations -- une par BDD du registre -- a CHAQUE tour, meme quand rien
n'avait bouge. Mesure : 504 134 observations pour 36 000 passes, soit 93 % du
journal du plus ancien espion de la Matrice. Or l'integrite d'une BDD est un
ETAT : elle ne change pas entre deux passes. Repeter le tableau, c'est noyer les
faits : il fallait lire 14 lignes pour trouver la seule qui dise quelque chose.

La reparation (meme doctrine que MO-080, sur le routeur) separe deux objets :

  - l'ETAT   (`espion-etat-bdds.json`) : le TABLEAU DES BDD vu par la passe,
    ecrit a CHAQUE tour et ECRASE. Il porte aussi la signature du dernier tableau
    JOURNALISE et le nombre de passes absorbees -- la redondance supprimee est
    TRACEE, jamais silencieuse ;
  - l'HISTOIRE (`espion-log.jsonl`) : les observations ne sont ecrites que si le
    tableau CHANGE -- et ce changement est le fait.

CE QUE CE GARDE EXIGE
  1. la DECISION est PURE (`fait_notable` / `signature_controle`) : elle se teste
     sans disque ;
  2. une passe SANS CHANGEMENT n'ecrit AUCUNE observation -- mais l'ETAT est
     ecrit quand meme, et son compteur de passes absorbees AVANCE ;
  3. la ligne `passe` reste ecrite a CHAQUE tour, et porte COMBIEN de passes
     avaient ete absorbees avant ce qu'elle rapporte : c'est le TEMOIN DE VIE que
     lit la non-regression du flux (lecon L-026), et un temoin n'a pas le droit de
     devenir aveugle ;
  4. un CHANGEMENT n'est JAMAIS absorbe : le tableau complet repart au journal.

CE QU'IL NE FAIT PAS : il ne touche JAMAIS les fichiers de service (journal, etat,
registre). Son cobaye vit dans le dossier temporaire du systeme, et il
s'AUTOTESTE en rejouant l'ANCIENNE regle (journaliser les 14 observations a chaque
passe) : si elle revenait, le garde doit l'ACCUSER (lecon L-032).

Il tourne dans SON PROPRE processus : les routines de la Matrice portent des
modules `constants` et `commun` homonymes (lecon L-029), un import partage les
ferait se marcher dessus.

Usage: python verifier-observations-non-redondantes.py [--racine <path>]
  code 0 = sain, 1 = ecart (liste et nomme), 2 = racine introuvable.
"""

import argparse
import contextlib
import io
import json
import shutil
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# --- REFERENCES (aucune valeur en dur dans la logique) ----------------------
ROUTINE = "espion-integrite"
NOM_JOURNAL = "espion-log.jsonl"
NOM_ETAT = "espion-etat-bdds.json"
# Le registre du COBAYE : deux BDD REELLES (elles existent, donc "faite" rend un
# constat sain -- un cobaye qui crie ECART sur une BDD absente mesurerait des
# alertes, pas la journalisation) et une fictive a-construire (le chapitre 2 n'est
# produit que par celles-la -- MO-072).
REGISTRE_COBAYE = {
    "lecons.json": True,
    "conventions-matrice.json": True,
    "bdd-cobaye-a-construire.json": False,
}
# Le CHANGEMENT : une BDD faite devient a-construire (le tableau bascule, le
# chapitre 2 se rallume). C'est un fait, il doit repartir au journal.
REGISTRE_CHANGE = {
    "lecons.json": True,
    "conventions-matrice.json": False,
    "bdd-cobaye-a-construire.json": False,
}
# Passes SANS CHANGEMENT eprouvees : assez pour que l'absorption soit visible.
PASSES_ABSORBEES = 3

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


def age_secondes(horodatage):
    """Age en secondes d'un horodatage 'YYYY-MM-DD HH:MM:SS', ou None si illisible."""
    try:
        return int((datetime.now() - datetime.strptime(str(horodatage), "%Y-%m-%d %H:%M:%S")).total_seconds())
    except (TypeError, ValueError):
        return None


def controler(nom, condition, detail=""):
    RESULTATS.append((nom, bool(condition), detail))
    print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)
    return bool(condition)


def charger_routine(matrix):
    """Rend (constantes, commun, tour_entry) de la routine, ou None.

    Chargement PAR SON DOSSIER : les modules s'appellent `constants` et `commun`
    et ne se resolvent que depuis le dossier de la routine. Un seul jeu de modules
    par processus, donc aucun melange avec une autre routine.
    """
    dossier = matrix / "matrice" / "routines" / ROUTINE
    if not (dossier / "tour" / "entry.py").is_file():
        return None
    sys.path.insert(0, str(dossier))
    try:
        import constants as constantes  # noqa: PLC0415 -- chemin installe juste avant
        import commun  # noqa: PLC0415
        from tour import entry as tour_entry  # noqa: PLC0415
    except Exception as erreur:  # noqa: BLE001 -- on AVOUE l'echec, on ne plante pas
        print("ECHEC de chargement (" + ROUTINE + ") : " + str(erreur))
        return None
    return constantes, commun, tour_entry


def lire_lignes(chemin):
    """Lignes non vides d'un fichier (vide si absent)."""
    if chemin is None or not Path(chemin).is_file():
        return []
    with open(str(chemin), "r", encoding="utf-8", errors="replace") as flux:
        return [ligne.rstrip("\r\n") for ligne in flux if ligne.strip()]


def lire_etat(chemin):
    """L'etat du controle, ou {} (jamais d'exception dans un garde)."""
    try:
        return json.loads(Path(chemin).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def ancienne_regle_observations(nb_passes, nb_bdds):
    """L'ANCIENNE regle, telle quelle : une observation par BDD a CHAQUE passe.

    Rejouee par l'autotest : c'est ELLE qui a produit 93 % du journal, et le garde
    doit savoir l'accuser si elle revenait.
    """
    return nb_passes * nb_bdds


def _passer(constantes, commun, tour_entry, registre, journal, etat):
    """Joue UNE passe sur les fichiers du cobaye. Rend le code du verdict."""
    commun.CHEMIN_JOURNAL = journal
    commun.CHEMIN_ETAT_BDDS = etat
    tour_entry.BDDS = dict(registre)
    # La passe REELLE raconte son verdict : le cobaye se TAIT, sinon sa sortie
    # noierait celle du garde (un garde illisible finit ignore, lecon L-054).
    with contextlib.redirect_stdout(io.StringIO()):
        return tour_entry.executer([])


# --------------------------------------------------------------------------- 1
def controler_decision_pure(tour_entry, erreurs):
    """La decision est PURE : memes constats, meme reponse, sans disque."""
    manquants = [
        nom for nom in ("signature_controle", "fait_notable")
        if not callable(getattr(tour_entry, nom, None))
    ]
    if manquants:
        erreurs.append("decision non separable : " + ", ".join(manquants))
        controler("decision-pure", False, "ABSENTE : " + ", ".join(manquants))
        return
    constats = [
        {"bdd": "a.json", "chapitre": 1, "etat": "ok", "detail": "integrite verifiee"},
        {"bdd": "b.json", "chapitre": 2, "etat": "INFO", "detail": "BDD a construire (absente : True)"},
    ]
    signature = tour_entry.signature_controle(constats)
    change = [dict(constat) for constat in constats]
    change[0]["etat"] = "ECART"
    change[0]["detail"] = "empreinte reelle != etalon"
    presence = [dict(constat) for constat in constats]
    presence[1]["detail"] = "BDD a construire (absente : False)"
    cas = [
        ("tableau identique = absorbe", tour_entry.fait_notable(constats, signature), False),
        ("etat qui bascule = fait", tour_entry.fait_notable(change, signature), True),
        ("presence qui change = fait", tour_entry.fait_notable(presence, signature), True),
        ("premiere passe = fait", tour_entry.fait_notable(constats, None), True),
        ("ordre des BDD indifferent", tour_entry.fait_notable(list(reversed(constats)), signature), False),
    ]
    echecs = [nom for nom, obtenu, attendu in cas if obtenu != attendu]
    controler(
        "decision-pure",
        not echecs,
        str(len(cas)) + " cas" + ("" if not echecs else " : ECHECS " + str(echecs)),
    )
    if echecs:
        erreurs.append("decision de journalisation fausse : " + str(echecs))


# --------------------------------------------------------------------------- 2
def controler_cobaye(constantes, commun, tour_entry, dossier, erreurs):
    """Passe reelle sur un cobaye : rien de neuf = aucune observation, mais tout est TRACE."""
    journal = dossier / "espion-log.jsonl"
    etat = dossier / NOM_ETAT
    nb_bdds = len(REGISTRE_COBAYE)

    # 1. Premiere passe : le tableau part au journal (un fait).
    code = _passer(constantes, commun, tour_entry, REGISTRE_COBAYE, journal, etat)
    apres_1 = lire_lignes(journal)
    observations_1 = [l for l in apres_1 if "\"observation\"" in l]
    controler(
        "premiere-passe-complete",
        code == 0 and len(observations_1) == nb_bdds and len(apres_1) == nb_bdds + 1,
        "code " + str(code) + ", " + str(len(observations_1)) + " observation(s) + 1 ligne passe"
        " (attendu " + str(nb_bdds) + " observations)",
    )
    if len(observations_1) != nb_bdds:
        erreurs.append("la premiere passe n'a pas journalise le tableau complet")

    # 2. Passes SANS CHANGEMENT : aucune observation nouvelle, l'etat AVANCE.
    for _ in range(PASSES_ABSORBEES):
        _passer(constantes, commun, tour_entry, REGISTRE_COBAYE, journal, etat)
    apres_2 = lire_lignes(journal)
    observations_2 = [l for l in apres_2 if "\"observation\"" in l]
    passes_2 = [l for l in apres_2 if "\"passe\"" in l]
    controler(
        "observations-absorbees",
        len(observations_2) == len(observations_1),
        str(PASSES_ABSORBEES) + " passes identiques -> " + str(len(observations_2))
        + " observation(s) (inchange)",
    )
    if len(observations_2) != len(observations_1):
        erreurs.append("une passe sans changement a journalise des observations : la redondance est revenue")

    # 3. Le TEMOIN DE VIE reste ecrit a CHAQUE passe, et dit ce qui a ete absorbe.
    controler(
        "temoin-de-vie-a-chaque-passe",
        len(passes_2) == PASSES_ABSORBEES + 1,
        str(len(passes_2)) + " ligne(s) `passe` pour " + str(PASSES_ABSORBEES + 1)
        + " passes (le flux lit la derniere : elle ne doit jamais devenir aveugle)",
    )
    if len(passes_2) != PASSES_ABSORBEES + 1:
        erreurs.append("la ligne `passe` n'est plus ecrite a chaque tour : le temoin de vie est rompu")

    etat_courant = lire_etat(etat)
    controler(
        "etat-ecrit-et-avance",
        etat_courant.get("type") == "controle"
        and int(etat_courant.get("passes_absorbes") or 0) == PASSES_ABSORBEES
        and len(etat_courant.get("observations") or {}) == nb_bdds,
        "etat : " + str(PASSES_ABSORBEES) + " passe(s) absorbe(s), "
        + str(len(etat_courant.get("observations") or {})) + " BDD(s) au tableau",
    )
    if int(etat_courant.get("passes_absorbes") or 0) != PASSES_ABSORBEES:
        erreurs.append("l'etat n'avance pas : la redondance supprimee serait invisible")
    if len(etat_courant.get("observations") or {}) != nb_bdds:
        erreurs.append("l'etat ne porte pas le tableau complet des BDD")

    # 4. Un CHANGEMENT n'est jamais absorbe, et la ligne `passe` DIT la silence
    #    qu'elle a rompu (le nombre de passes absorbees avant elle).
    _passer(constantes, commun, tour_entry, REGISTRE_CHANGE, journal, etat)
    apres_3 = lire_lignes(journal)
    observations_3 = [l for l in apres_3 if "\"observation\"" in l]
    nouvelle = json.loads(apres_3[-1])
    controler(
        "changement-jamais-absorbe",
        len(observations_3) == len(observations_2) + nb_bdds
        and nouvelle.get("motif") == "changement"
        and int(nouvelle.get("passes_absorbes") or 0) == PASSES_ABSORBEES,
        "tableau change -> " + str(len(observations_3) - len(observations_2))
        + " observation(s), motif=" + str(nouvelle.get("motif"))
        + ", passes_absorbes=" + str(nouvelle.get("passes_absorbes")),
    )
    if len(observations_3) != len(observations_2) + nb_bdds:
        erreurs.append("un changement de tableau n'a pas reparti au journal")
    if int(nouvelle.get("passes_absorbes") or 0) != PASSES_ABSORBEES:
        erreurs.append("la ligne ecrite ne dit pas combien de passes avaient ete absorbees")

    # 5. Un FAIT ne se repete pas : deux tableaux journalises differents.
    signatures = []
    for ligne in apres_3:
        try:
            evenement = json.loads(ligne)
        except ValueError:
            continue
        if evenement.get("type") == "observation":
            signatures.append(ligne)
    controler(
        "tableaux-journalises-differents",
        len(signatures) == 2 * nb_bdds,
        str(len(signatures)) + " observation(s) ecrite(s) pour 2 tableaux distincts",
    )
    if len(signatures) != 2 * nb_bdds:
        erreurs.append("le nombre d'observations journalisees ne correspond pas a deux tableaux")

    # 6. L'ETAT a ete REINITIALISE par le changement (le silence rompu se compte a
    #    partir du nouveau fait).
    etat_final = lire_etat(etat)
    controler(
        "etat-repart-au-changement",
        int(etat_final.get("passes_absorbes") or 0) == 0
        and bool(etat_final.get("derniere_observation")),
        "apres un changement : " + str(etat_final.get("passes_absorbes"))
        + " passe(s) absorbe(s), derniere observation " + str(etat_final.get("derniere_observation")),
    )
    if int(etat_final.get("passes_absorbes") or 0) != 0:
        erreurs.append("le compteur d'absorption ne repart pas au changement")
    return len(observations_2), len(observations_3)


# --------------------------------------------------------------------------- 3
def controler_autotest(observations_nouvelles, nb_bdds, erreurs):
    """Le garde doit ACCUSER l'ancienne regle (lecon L-032).

    Sequence du cobaye : 1 passe (le tableau), 3 passes identiques, un changement.
    L'ancienne regle journalise les 4 observations a CHAQUE passe. Si elle ne
    produisait pas plus de lignes que la nouvelle, c'est que ce garde ne saurait
    pas voir une redondance.
    """
    nb_passes = PASSES_ABSORBEES + 2
    anciennes = ancienne_regle_observations(nb_passes, nb_bdds)
    ok = anciennes > observations_nouvelles
    controler(
        "autotest-ancienne-regle-accusee",
        ok,
        "ancienne regle : " + str(anciennes) + " observation(s) ; nouvelle : "
        + str(observations_nouvelles) + " sur " + str(nb_passes) + " passes"
        + ("" if ok else " -- NON ACCUSEE"),
    )
    if not ok:
        erreurs.append("l'ancienne regle n'est pas accusee : le garde ne verrait pas la redondance")


# --------------------------------------------------------------------------- 4
def controler_fabrique(constantes, tour_entry, matrix, erreurs):
    """La routine DECLARE son etat et sa decision ; le SERVICE est mesure."""
    manquants = [
        nom for nom in ("NOM_ETAT_BDDS", "CHEMIN_ETAT_BDDS")
        if not hasattr(constantes, nom)
    ]
    controler(
        "fabrique-declaree",
        not manquants,
        "etat du controle declare dans constants.py"
        if not manquants else "MANQUANT : " + ", ".join(manquants),
    )
    if manquants:
        erreurs.append("la routine ne declare pas : " + ", ".join(manquants))

    dossier = matrix / "matrice" / "routines" / ROUTINE
    journal = dossier / NOM_JOURNAL
    etat_service = lire_etat(dossier / NOM_ETAT)

    # 1. L'ETAT du service porte le tableau et a deja absorbe : c'est la PREUVE sur
    #    le service, sans jamais le toucher.
    absorbees = int(etat_service.get("passes_absorbes") or 0)
    bdds = len(etat_service.get("observations") or {})
    controler(
        "etat-de-service-present",
        etat_service.get("type") == "controle" and bdds > 0,
        NOM_ETAT + " : " + str(etat_service.get("date")) + ", " + str(bdds)
        + " BDD(s) au tableau, " + str(absorbees) + " passe(s) absorbe(s)",
    )
    if not etat_service:
        erreurs.append("l'etat du controle est absent ou illisible")
    # RECUL (MO-097) : un service qui vient de DEMARRER n'a pas encore eu le TEMPS
    # d'absorber une passe. La regle immuable (attente-ne-prouve-rien) est
    # explicite : un temoin qui manque de recul l'ANNONCE ("recul insuffisant") et
    # s'appuie sur la valeur DECLAREE -- il n'accuse pas, et il ne demande jamais a
    # l'agent D'ATTENDRE une cadence. Sans cette branche, un redemarrage
    # COOPERATIF legitime (L-012 : un processus vivant garde le code de son
    # lancement) faisait crier la suite sur un service parfaitement sain ;
    # l'absorption vient SEULE, a la passe suivante.
    cadence = getattr(constantes, "INTERVALLE_DECLARE_SECONDES", None)
    age_etat = age_secondes(etat_service.get("date"))
    recul_insuffisant = bool(
        absorbees < 1 and cadence and age_etat is not None and age_etat < cadence
    )
    controler(
        "passe-absorbee-sur-le-service",
        absorbees >= 1 or recul_insuffisant,
        str(absorbees) + " passe(s) sans changement absorbe(s) depuis la derniere observation"
        + (
            " -- RECUL INSUFFISANT : etat vieux de " + str(age_etat) + " s pour une cadence"
            + " declaree de " + str(cadence) + " s (l'absorption vient SEULE, aucune attente requise)"
            if recul_insuffisant else ""
        ),
    )
    if absorbees < 1 and not recul_insuffisant:
        erreurs.append(
            "aucune passe absorbee sur le service : la routine tourne-t-elle le code repare ?"
        )

    # 2. La QUEUE du journal : chaque ligne `passe` NOUVELLE est suivie des
    #    observations de la passe SUIVANTE si -- et seulement si -- elle annonce un
    #    changement. C'est la propriete mesuree sur le journal REEL, et elle est
    #    non vide des la premiere ligne nouvelle.
    lignes = []
    for ligne in lire_lignes(journal):
        try:
            lignes.append(json.loads(ligne))
        except ValueError:
            continue
    sequences = []
    precedente = None
    for index, evenement in enumerate(lignes):
        if evenement.get("type") != "passe":
            continue
        # Les observations d'une passe sont ecrites AVANT sa propre ligne `passe`
        # (le tableau part au journal, puis le temoin le constate). On compte donc
        # les observations depuis la ligne `passe` PRECEDENTE : c'est le segment
        # exact de CETTE passe.
        if precedente is not None and "motif" in evenement:
            segment = [ligne for ligne in lignes[precedente + 1:index]
                       if ligne.get("type") == "observation"]
            sequences.append((evenement.get("motif"), len(segment),
                              int(evenement.get("bdds_surveillees") or 0)))
        precedente = index
    # La ligne `passe` DECLARE son propre compte de BDDs surveillees au moment
    # de la passe (mesure du 2026-09-14 : `bdds_surveillees: 15` sur une passe
    # historique, compte du present = 14). L'attente s'ancre sur SA declaration,
    # jamais sur le compte du present mutable : c'est le refus d'arbitrer
    # l'histoire avec l'etat courant.
    fautives = [
        motif for motif, suivantes, attendues in sequences
        if suivantes != (attendues if motif == "changement" else 0)
    ]
    controler(
        "journal-reel-conforme-au-motif",
        bool(sequences) and not fautives,
        str(len(sequences)) + " ligne(s) `passe` mesuree(s) : "
        + str(sum(1 for motif, _s, _a in sequences if motif == "changement")) + " changement(s), "
        + str(sum(1 for motif, _s, _a in sequences if motif != "changement")) + " absorbe(s)"
        + ("" if not fautives else " ; FAUTIVES : " + str(sorted(set(fautives)))),
    )
    if fautives:
        erreurs.append(
            "des observations ne correspondent pas au motif annonce : " + str(sorted(set(fautives)))
        )
    if not sequences:
        print(
            "[--] journal-reel-conforme-au-motif : aucune ligne `passe` du code repare"
            " (rien a verifier sur le service -- voir le cobaye)"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Garde : les observations d'une passe sont un etat, l'histoire ne recoit que les faits"
    )
    parser.add_argument("--racine", default=".", help="Racine projet (defaut: cwd)")
    arguments = parser.parse_args()

    matrix = trouver_matrix(Path(arguments.racine).resolve())
    if matrix is None:
        print("Dossier matrix/ introuvable sous " + str(arguments.racine))
        return 2
    charges = charger_routine(matrix)
    if charges is None:
        print("Routine introuvable ou illisible : " + str(matrix / "matrice" / "routines" / ROUTINE))
        return 2
    constantes, commun, tour_entry = charges

    print("VERIFIER OBSERVATIONS NON REDONDANTES -- un etat dans l'etat, des faits dans l'histoire")

    dossier = Path(tempfile.mkdtemp(prefix="garde-observations-"))
    erreurs = []
    try:
        controler_decision_pure(tour_entry, erreurs)
        observations_absorbees, observations_nouvelles = controler_cobaye(
            constantes, commun, tour_entry, dossier, erreurs
        )
        controler_autotest(observations_nouvelles, len(REGISTRE_COBAYE), erreurs)
        controler_fabrique(constantes, tour_entry, matrix, erreurs)
        _ = observations_absorbees
    finally:
        shutil.rmtree(dossier, ignore_errors=True)

    echecs = [nom for nom, ok, _ in RESULTATS if not ok]
    if erreurs or echecs:
        for ecart in erreurs:
            print("ECART : " + ecart)
        print("")
        print("VERDICT KO : les observations d'une passe repartent au journal comme un etat.")
        return 1
    print("")
    print("VERDICT OK : le tableau des BDD est un etat, l'histoire ne recoit que ses changements.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
