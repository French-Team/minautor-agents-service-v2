#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routeur-maintenance : Route les signalements cameleon -> maintenance Optimus.

Lit matrice/intercom/matrice/inbox.jsonl, detecte les type=signaler,
les ecrit dans _operateur/maintenance/matrice/inbox.jsonl.

REGLE : jamais en silence. Les messages non routes sont COMPTES et NOMMES
(par type). Un type inattendu (par ex. `alerte-grave`, ecrit autrefois en
direct par veille-flux) laisse une trace dans l'historique -- c'est faute de
cette trace que 10 alertes graves ont disparu sans que personne ne le voie.

Usage:
  python routeur.py tour        (une passe)
  python routeur.py boucle      (veille)
  python routeur.py boucle arret
  python routeur.py rotation [--racine <matrix>] [--seuil <octets>] [--gardes <n>] [--force]
"""

import json
import os
import sys
import time
from pathlib import Path

# LES VALEURS VIVENT DANS constants.py (moule routine, friction du 2026-09-23) :
# le controle d'attribution lit les declarations d'une routine dans SES constantes
# (`PRODUCTIONS`) -- les porter dans le script les rendait INLISIBLES, donc tues.
# Ici le script les CONSOMME : il n'en recopie aucune (M-076).
from constants import (  # noqa: E402
    BASE, RACINE_MATRIX, REPERTOIRE_MATRICE, REPERTOIRE_OPERATEUR,
    BOITE_MATRICE_IN, BOITE_MAINTENANCE_IN, HISTORIQUE,
    PID_FILE, DRAPEAU_ARRET, INTERVALLE_SECONDS, INTERVALLE_DECLARE_SECONDES,
    NOM_ARCHIVE_PREFIXE, SEUIL_OCTETS_JOURNAL, EVENEMENTS_GARDES_JOURNAL,
    ESSAIS_ROTATION, NOM_HISTORIQUE, NOM_REPERTOIRE, CHEMIN_RELATIF_JOURNAL,
    NOM_CADENCE, CHEMIN_CADENCE, NOM_ETAT, CHEMIN_ETAT,
    PASSES_GARDEES_ETAT, CLE_ANNEAU_PASSES, REPERTOIRE_COMMUN, TYPES_NORMAUX,
)

# data/commun (motif unique M-076) : l'attente cooperative est PARTAGEE, jamais
# recopiee. L'INSERTION dans sys.path vit dans `constants.py` (invariant 1 du
# moule) : ces imports la SUIVENT, ils ne la refont pas.
from attente import attendre  # noqa: E402
from vivacite import processus_vivant  # noqa: E402
from battement import ajouter_passe  # noqa: E402
from etat_histoire import decision_fait as _decision_fait  # noqa: E402
from etat_histoire import signature_fait as _signature_fait_partage  # noqa: E402
from etat_histoire import CHAMP_IDENTITE as _CHAMP_IDENTITE  # noqa: E402
from rotation_journal import cli  # noqa: E402
from rotation_journal import tourner_et_journaliser as _tourner_et_journaliser  # noqa: E402


# --- Rotation et cadence (MO-079) ------------------------------------------
def journaliser_historique(evenement):
    """Trace un evenement (rotation incluse) dans le journal du routeur."""
    ecrire_message(HISTORIQUE, evenement)


def chemin_journal(racine=None):
    """Retourne le journal a traiter pour une racine donnee (defaut : le depot).

    Le parametre sert aux COBAYES : un controle qu'on ne peut pas pieger ne
    prouve rien (lecon L-032).
    """
    return (Path(racine) if racine else RACINE_MATRIX) / CHEMIN_RELATIF_JOURNAL


def publier_cadence(intervalle):
    """Publie la cadence EFFECTIVE dans un etat COURT (routeur-cadence.json).

    UNE SEULE LIGNE : un etat lu par un lecteur de journal se lit ligne par ligne
    -- un JSON indente serait illisible pour lui, et le controle retomberait en
    silence sur "sans trace". Ecriture atomique (tmp + remplacement, LF forces).
    """
    donnees = {
        "type": "demarrage",
        "intervalle": intervalle,
        "pid": os.getpid(),
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    temporaire = CHEMIN_CADENCE.with_name(CHEMIN_CADENCE.name + ".tmp")
    with open(str(temporaire), "w", encoding="utf-8", newline="\n") as flux:
        flux.write(json.dumps(donnees, ensure_ascii=True, sort_keys=True) + "\n")
    os.replace(str(temporaire), str(CHEMIN_CADENCE))
    return CHEMIN_CADENCE


# --- Etat / histoire (MO-080) ----------------------------------------------
def resume_passe(routes, ignores_par_type, anormaux):
    """Le resume COMPLET d'une passe : ce qui part dans l'ETAT (et pas ailleurs)."""
    return {
        "routes": routes,
        "ignores": sum(ignores_par_type.values()),
        "ignores_par_type": ignores_par_type,
        "anormaux": anormaux,
    }


def anomalies_par_type(ignores_par_type):
    """Le tableau des types ANORMAUX ignores (le trafic normal n'y est pas)."""
    return {t: n for t, n in ignores_par_type.items() if t not in TYPES_NORMAUX}


def signature_fait(ignores_par_type):
    """Signature COMPARABLE d'un fait : le tableau des ANOMALIES.

    Le trafic NORMAL ignore (fin-mission, retour-lot) n'y entre PAS : il ne fait
    que remplir l'inbox, c'est un etat, pas un fait.
    Le COURRIER ROUTE n'y entre pas non plus, et pour une autre raison : il est
    un fait PAR LUI-MEME (chaque message route compte, meme si le compte se
    repete). L'y mettre faisait changer la signature au seul RETOUR du compteur a
    zero -- deux passes consecutives egales a 1 route puis 0 route passaient pour
    deux faits, donc une ligne de trop a chaque rafale (attrapee par le cobaye).
    """
    # La signature elle-meme vient du moteur PARTAGE (data/commun/etat_histoire.py,
    # MO-082) : quatre implementations de la meme idee divergent (lecon L-029).
    return _signature_fait_partage({"anomalies_par_type": anomalies_par_type(ignores_par_type)})


def fait_notable(routes, ignores_par_type, signature_ecrite):
    """DECISION PURE : cette passe laisse-t-elle un FAIT a l'historique ?

    Vrai si du courrier a ete ROUTE -- chaque message route est un fait, meme si
    le COMPTE se repete d'une passe a l'autre (deux passes qui routent 1 message
    chacune sont deux faits) -- ou si le tableau des ANOMALIES a change (une
    anomalie apparait, evolue ou disparait).
    Faux = la passe n'apporte rien de neuf : elle va dans l'ETAT, pas dans
    l'histoire. Rien n'est perdu : l'etat complet est ecrit a chaque passe.
    """
    # Deux sources de fait : du courrier ROUTE (le compteur compte, meme s'il se
    # repete : chaque message route est un fait) ou un tableau d'anomalies
    # DIFFERENT. La comparaison elle-meme est la decision PURE du moteur partage.
    if routes > 0:
        return True
    return _decision_fait(signature_fait(ignores_par_type), signature_ecrite)[0]


def lire_etat(chemin=None):
    """Lit l'ETAT de passe (dict) ; {} si absent ou illisible (jamais de crash)."""
    chemin = chemin or CHEMIN_ETAT
    try:
        return json.loads(chemin.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def publier_etat(resume, signature_ecrite, passes_absorbes, derniere_ecriture, anneau_avant=None):
    """Ecrit l'ETAT de passe : une ligne, ATOMIQUE, ecrase a chaque passe.

    Ce n'est pas une histoire : c'est la photographie courante des boites. Il
    porte la date de la passe, la date de la DERNIERE ligne d'histoire ecrite et
    le nombre de passes absorbees depuis -- de quoi distinguer "rien a ecrire"
    de "la routine ne tourne plus" sans gonfler aucun journal.

    Il porte AUSSI l'ANNEAU DES PASSES (`CLE_ANNEAU_PASSES`) : c'est lui, et lui
    seul, qui rend le battement REEL mesurable en MEDIANE par `verifier-cadence`.
    """
    passe = time.strftime("%Y-%m-%d %H:%M:%S")
    donnees = dict(resume)
    donnees.update(
        {
            "type": "passe",
            "date": passe,
            "signature_ecrite": signature_ecrite,
            "passes_absorbes": passes_absorbes,
            "derniere_ecriture": derniere_ecriture,
            CLE_ANNEAU_PASSES: ajouter_passe(anneau_avant, passe, PASSES_GARDEES_ETAT),
        }
    )
    temporaire = CHEMIN_ETAT.with_name(CHEMIN_ETAT.name + ".tmp")
    with open(str(temporaire), "w", encoding="utf-8", newline="\n") as flux:
        flux.write(json.dumps(donnees, ensure_ascii=True, sort_keys=True) + "\n")
    os.replace(str(temporaire), str(CHEMIN_ETAT))
    return CHEMIN_ETAT


def rotation(arguments):
    """Verbe `rotation` : borne le journal en ARCHIVANT ses evenements anciens."""
    return cli(
        arguments,
        chemin_journal,
        SEUIL_OCTETS_JOURNAL,
        EVENEMENTS_GARDES_JOURNAL,
        ESSAIS_ROTATION,
        NOM_ARCHIVE_PREFIXE,
        journaliser_historique,
    )


def tourner_et_journaliser(racine=None, verbeux=False, forcer=False):
    """Rotation silencieuse, verifiee AVANT chaque passe de la boucle.

    Rend (code, rapport) et ne leve jamais : une rotation refusee est un fait
    journalise, pas une passe morte (lecon L-026).
    """
    return _tourner_et_journaliser(
        chemin_journal(racine),
        SEUIL_OCTETS_JOURNAL,
        EVENEMENTS_GARDES_JOURNAL,
        ESSAIS_ROTATION,
        NOM_ARCHIVE_PREFIXE,
        journaliser_historique,
        verbeux=verbeux,
        forcer=forcer,
    )


def lire_messages(chemin):
    """Lit tous les messages d'une boite JSONL."""
    if not chemin.is_file():
        return []
    messages = []
    for ligne in chemin.read_text(encoding="utf-8", errors="replace").splitlines():
        ligne = ligne.strip()
        if ligne:
            try:
                messages.append(json.loads(ligne))
            except json.JSONDecodeError:
                continue
    return messages


def ecrire_message(chemin, message):
    """Append un message dans une boite."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(message, ensure_ascii=False) + "\n")


def marquer_traiter(chemin, index):
    """Marque un message comme traite (ajoute un champ traite=true)."""
    if not chemin.is_file():
        return
    lignes = chemin.read_text(encoding="utf-8", errors="replace").splitlines()
    if index < len(lignes):
        try:
            msg = json.loads(lignes[index])
            msg["traite_par_routeur"] = True
            msg["traite_le"] = time.strftime("%Y-%m-%d %H:%M:%S")
            lignes[index] = json.dumps(msg, ensure_ascii=False)
            with open(chemin, "w", encoding="utf-8", newline="\n") as f:
                for l in lignes:
                    f.write(l + "\n")
        except json.JSONDecodeError:
            pass


def tour():
    """Une passe de routage : inbox matrice -> maintenance."""
    if not BOITE_MATRICE_IN.is_file():
        print("Aucune boite inbox matrice.")
        return 0

    messages = lire_messages(BOITE_MATRICE_IN)
    routes = 0
    ignores_par_type = {}
    anormaux = 0
    # EO-163 : l IDENTITE des messages routes par CETTE passe (le fait dit CE QUI
    # s est passe, pas seulement COMBIEN).
    identites = []

    for i, msg in enumerate(messages):
        # Deja traite ?
        if msg.get("traite_par_routeur"):
            continue

        # Route seulement les signalements : les consommateurs en aval
        # (maintenir) ne savent lire que `signaler`.
        if msg.get("type") == "signaler":
            # Ajoute le metadata de routage
            msg["route_le"] = time.strftime("%Y-%m-%d %H:%M:%S")
            # La provenance est celle que le signal DECLARE : un signal de
            # routine n'est pas un signal du cameleon (l'etiquette en dur
            # `cameleon` mentait sur tous les signaux des routines).
            msg["source"] = msg.get("expediteur", "cameleon")
            msg["destination"] = "optimus"

            # Ecrit dans maintenance
            ecrire_message(BOITE_MAINTENANCE_IN, msg)
            marquer_traiter(BOITE_MATRICE_IN, i)
            routes += 1
            identites.append({
                "index": i,
                "type": msg.get("type", "?"),
                "outil": msg.get("outil") or msg.get("cible", "?"),
                "niveau": msg.get("niveau", "?"),
                "expediteur": msg.get("source", "?"),
            })
            print(f"  ROUTE : {msg.get('niveau', '?').upper()} {msg.get('outil', '?')} -> maintenance")
        else:
            type_msg = msg.get("type", "?")
            ignores_par_type[type_msg] = ignores_par_type.get(type_msg, 0) + 1
            if type_msg not in TYPES_NORMAUX:
                anormaux += 1
                print(f"  NON ROUTE : {type_msg} (outil {msg.get('outil') or msg.get('cible', '?')})")

    # --- ETAT et HISTOIRE : deux objets, deux durees de vie (MO-080) ---------
    # L'ETAT est le tableau COURANT : ecrit a CHAQUE passe, ecrase. L'HISTOIRE
    # est une suite de FAITS : on n'y ecrit que si du courrier a ete ROUTE ou si
    # le tableau des ANOMALIES a change. Avant, la passe recopiait le meme tableau
    # a chaque tour (510 lignes identiques a la date pres sur 512 : 99,4 %) --
    # un journal qui repete un etat n'est plus une histoire, c'est un battement de
    # coeur qui noie les faits sans rien apprendre.
    # La redondance supprimee est TRACEE (`passes_absorbes`), jamais silencieuse.
    resume = resume_passe(routes, ignores_par_type, anormaux)
    etat_avant = lire_etat()
    signature_ecrite = etat_avant.get("signature_ecrite")
    absorbes = int(etat_avant.get("passes_absorbes") or 0)
    derniere_ecriture = etat_avant.get("derniere_ecriture") or ""

    if fait_notable(routes, ignores_par_type, signature_ecrite):
        derniere_ecriture = time.strftime("%Y-%m-%d %H:%M:%S")
        ecrire_message(HISTORIQUE, {
            "date": derniere_ecriture,
            "routes": routes,
            "ignores": resume["ignores"],
            "ignores_par_type": ignores_par_type,
            "anormaux": anormaux,
            "passes_absorbes": absorbes,
            # LE FAIT PORTE SON IDENTITE (EO-163) : les messages routes, ou -- si
            # le fait vient d un CHANGEMENT du tableau -- la transition elle-meme.
            _CHAMP_IDENTITE: identites or [{"transition": {
                "avant": signature_ecrite,
                "apres": signature_fait(ignores_par_type)}}],
        })
        signature_ecrite = signature_fait(ignores_par_type)
        absorbes = 0
    else:
        absorbes += 1

    publier_etat(resume, signature_ecrite, absorbes, derniere_ecriture,
                 etat_avant.get(CLE_ANNEAU_PASSES))
    return routes


def main():
    """Point d'entree."""
    args = sys.argv[1:]
    mode = args[0] if args else "tour"

    if mode in ("--help", "-h", "help"):
        print(__doc__)
        return 0

    if mode == "tour":
        print(f"=== ROUTEUR MAINTENANCE -- {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
        routes = tour()
        print(f"Routes : {routes}")
        return 0

    if mode == "rotation":
        return rotation(args[1:])

    if mode == "boucle":
        # Arret cooperatif
        if len(args) > 1 and args[1] == "arret":
            DRAPEAU_ARRET.touch()
            print("Drapeau d'arret pose. La boucle s'arretera apres la passe en cours.")
            return 0

        # Garde double lancement (EO-404) : un PID ECRIT ne prouve RIEN, il faut un
        # processus VIVANT. Avant, la seule PRESENCE du fichier refusait le
        # lancement : un routeur tue en plein vol -- ou plante AVANT son `finally`
        # -- laissait un PID fantome qui BLOQUAIT toute relance, et la Matrice
        # restait a 6/7 sans que rien ne le lise. La sonde est le motif PARTAGE
        # (data/commun/vivacite.py, M-076) : la MEME que `vie etat`.
        ancien_pid = None
        if PID_FILE.is_file():
            try:
                ancien_pid = int(PID_FILE.read_text(encoding="utf-8").strip())
            except (OSError, ValueError):
                ancien_pid = None
            if ancien_pid is not None and processus_vivant(ancien_pid):
                print(f"Un routeur tourne deja (PID {ancien_pid}).")
                return 1
            print(
                "PID fantome "
                + (str(ancien_pid) if ancien_pid is not None else "illisible")
                + " : aucun processus vivant, la place est libre."
            )

        # Le PID s'ecrit DANS le `try` : le prelude ET la boucle sont donc sous le
        # `finally` qui le retire. Un plantage a l'allumage (mesure du 2026-09-23 :
        # `NameError` sur la cadence declaree) ne laisse plus de PID fantome -- ce
        # residu est exactement ce qui rendait la relance muette.
        try:
            PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
            print(f"Routeur demarre (PID {os.getpid()})")
            # Cadence EFFECTIVE publiee a l'allumage : on la LIT, on ne l'attend pas.
            # Deux traces, deux roles : le journal garde l'HISTOIRE (une rotation peut
            # en deplacer les evenements anciens), l'etat COURT garde la cadence du
            # demarrage en cours -- le controle de cadence n'est donc jamais aveugle.
            ecrire_message(HISTORIQUE, {
                "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "demarrage": INTERVALLE_SECONDS,
            })
            publier_cadence(INTERVALLE_SECONDS)

            while True:
                if DRAPEAU_ARRET.is_file():
                    DRAPEAU_ARRET.unlink()
                    print("Arret cooperatif.")
                    break
                # Borne du journal AVANT la passe : le declenchement se LIT
                # (taille vs seuil des constantes), et un refus de rotation ne
                # tue jamais la passe (lecon L-026).
                tourner_et_journaliser()
                tour()
                # Attente DECOUPEE : un arret demande est vu en 2 s.
                if attendre(INTERVALLE_SECONDS, DRAPEAU_ARRET):
                    DRAPEAU_ARRET.unlink()
                    print("Arret cooperatif.")
                    break
        finally:
            if PID_FILE.is_file():
                PID_FILE.unlink()

        # `boucle` SE TERMINE ICI : sans ce retour, la fin NORMALE (arret
        # cooperatif) tombait dans le message d erreur plus bas, et le routeur
        # sortait en criant "Mode inconnu : boucle" -- un MENSONGE que personne ne
        # lisait (sortie vers DEVNULL) et que la TRACE DE LANCEMENT (EO-409) a fait
        # remonter le jour meme : elle en donnait la derniere ligne pour une cause.
        return 0

    print(f"Mode inconnu : {mode}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
