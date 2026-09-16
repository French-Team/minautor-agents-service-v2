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

BASE = Path(__file__).resolve().parent
# Remonter jusqu'a cerveau-projet/matrix
RACINE_MATRIX = None
for p in [BASE, *BASE.parents]:
    if p.name == "matrix" and (p / "matrice").is_dir():
        RACINE_MATRIX = p
        break
if RACINE_MATRIX is None:
    # Jamais un compte de parents (L-013) : la remontee ci-dessus EST l'ancre et son
    # echec doit se DIRE -- un repli compte serait un chemin FAUX et SILENCIEUX.
    raise RuntimeError("Racine matrix/ introuvable en remontant depuis " + str(BASE))
REPERTOIRE_MATRICE = RACINE_MATRIX / "matrice"
REPERTOIRE_OPERATEUR = RACINE_MATRIX / "_operateur"

# Boites
BOITE_MATRICE_IN = REPERTOIRE_MATRICE / "intercom" / "matrice" / "inbox.jsonl"
BOITE_MAINTENANCE_IN = REPERTOIRE_OPERATEUR / "maintenance" / "matrice" / "inbox.jsonl"
HISTORIQUE = BASE / "routeur-historique.jsonl"

PID_FILE = BASE / "routeur.pid"
DRAPEAU_ARRET = BASE / "routeur-arret.flag"
INTERVALLE_SECONDES = 30
# Nom CANONIQUE de la cadence declaree, lu par `vie etat` : on LIT la cadence
# au lieu de l'attendre (attendre n'est pas verifier). Meme valeur, meme objet.
INTERVALLE_DECLARE_SECONDES = INTERVALLE_SECONDES

# --- Rotation du journal (MO-079) -------------------------------------------
# Le routeur est le DERNIER journal de routine sans borne. Mesure du 2026-09-14 :
# 1919 lignes / 296 Ko en 2 jours (~30 s par passe). Rien ne s'y supprime jamais :
# le borner, c'est DEPLACER ses evenements anciens dans une archive DATEE.
# Le moteur est PARTAGE (`matrice/data/commun/rotation_journal.py`, motif unique
# M-076) : cette routine ne declare que SES valeurs.
NOM_ARCHIVE_PREFIXE = "routeur-archive"
SEUIL_OCTETS_JOURNAL = 512 * 1024
EVENEMENTS_GARDES_JOURNAL = 500
ESSAIS_ROTATION = 3
NOM_HISTORIQUE = "routeur-historique.jsonl"
NOM_REPERTOIRE = BASE.name
CHEMIN_RELATIF_JOURNAL = Path("matrice") / "routines" / NOM_REPERTOIRE / NOM_HISTORIQUE

# Etat COURT de la cadence EFFECTIVE (une ligne, ecrasee a chaque demarrage).
# Sans lui, la rotation rendrait AVEUGLE le controle de cadence :
# `verifier-sans-attendre` cherchait le `demarrage` DANS LE JOURNAL, et la
# premiere rotation l'aurait emporte dans l'archive -- le controle aurait ete
# neutralise par le nettoyage qu'il surveille (lecon L-040). Un etat se lit dans
# un fichier d'etat, une histoire dans un journal.
NOM_CADENCE = "routeur-cadence.json"
CHEMIN_CADENCE = BASE / NOM_CADENCE

# --- Etat de passe (MO-080) -------------------------------------------------
# L'HISTORIQUE ne portait que des REPETITIONS : mesure du 2026-09-14, 510 lignes
# identiques a la date pres sur 512 (99,4 %), parce que la passe recopiait le
# meme tableau a chaque tour (~150 Ko par jour pour rien).
#
# Un journal est une suite de FAITS ; le tableau courant des boites est un ETAT.
# Le FAIT, ici, c'est : du courrier a ete ROUTE, ou le tableau des ANOMALIES a
# change. Le reste (l'inbox qui se remplit de trafic normal fin-mission /
# retour-lot) s'ecrit comme ETAT -- ecrase a chaque passe.
#
# L'etat porte AUSSI le nombre de passes absorbees depuis la derniere ligne : la
# redondance supprimee est TRACEE, jamais silencieuse -- et il distingue "rien a
# ecrire" de "le routeur est mort".
NOM_ETAT = "routeur-etat.json"
CHEMIN_ETAT = BASE / NOM_ETAT
# L'ANNEAU DES PASSES (friction 28) : les derniers horodatages de passe, pour que
# le battement REEL soit mesurable en MEDIANE. `passes_absorbes` /
# `derniere_ecriture` disent COMBIEN de passes ont ete absorbees, ils ne disent
# pas QUAND -- en tirer une moyenne est faux des qu'une passe n'est pas a
# l'heure (mesure du 2026-09-14 : la meme cadence de 900 s lue 450,5 s puis
# 600,3 s sur les vigies). La fabrique de l'anneau et sa lecture sont le moteur
# PARTAGE `data/commun/battement.py` (L-029), le routeur ne declare QUE la
# longueur.
PASSES_GARDEES_ETAT = 5
CLE_ANNEAU_PASSES = "dernieres_passes"

# data/commun (motif unique M-076) : l'attente cooperative est PARTAGEE, jamais
# recopiee. Sans elle, un arret demande attendait la cadence entiere en un seul
# `time.sleep`.
REPERTOIRE_COMMUN = REPERTOIRE_MATRICE / "data" / "commun"
if not (REPERTOIRE_COMMUN / "attente.py").is_file():
    raise RuntimeError(
        "Motif attente introuvable : " + str(REPERTOIRE_COMMUN / "attente.py")
    )
sys.path.insert(0, str(REPERTOIRE_COMMUN))
from attente import attendre  # noqa: E402
from battement import ajouter_passe  # noqa: E402
from etat_histoire import decision_fait as _decision_fait  # noqa: E402
from etat_histoire import signature_fait as _signature_fait_partage  # noqa: E402
from rotation_journal import cli  # noqa: E402
from rotation_journal import tourner_et_journaliser as _tourner_et_journaliser  # noqa: E402

# Types de messages qui ne regardent PAS le routeur (trafic normal des autres
# maillons : le pilote, les fins de mission). Tout AUTRE type non route est
# anormal et doit laisser une trace (voir tour()).
TYPES_NORMAUX = ("fin-mission", "retour-lot")


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

        # Garde double lancement
        if PID_FILE.is_file():
            ancien_pid = PID_FILE.read_text(encoding="utf-8").strip()
            print(f"Un routeur tourne deja (PID {ancien_pid}).")
            return 1

        PID_FILE.write_text(str(os.getpid()), encoding="utf-8")
        print(f"Routeur demarre (PID {os.getpid()})")
        # Cadence EFFECTIVE publiee a l'allumage : on la LIT, on ne l'attend pas.
        # Deux traces, deux roles : le journal garde l'HISTOIRE (une rotation peut
        # en deplacer les evenements anciens), l'etat COURT garde la cadence du
        # demarrage en cours -- le controle de cadence n'est donc jamais aveugle.
        ecrire_message(HISTORIQUE, {
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "demarrage": INTERVALLE_SECONDES,
        })
        publier_cadence(INTERVALLE_SECONDES)

        try:
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
                if attendre(INTERVALLE_SECONDES, DRAPEAU_ARRET):
                    DRAPEAU_ARRET.unlink()
                    print("Arret cooperatif.")
                    break
        finally:
            if PID_FILE.is_file():
                PID_FILE.unlink()

    print(f"Mode inconnu : {mode}")
    return 2


if __name__ == "__main__":
    sys.exit(main())
