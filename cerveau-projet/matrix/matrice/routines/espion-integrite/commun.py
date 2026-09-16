"""Fonctions communes de l'espion : empreinte, journal, PID, etat.

Chaque fonction fait UNE chose (convention-architecture-outils).
"""
import hashlib
import json
import os
from datetime import datetime

from constants import (
    BDDS,
    CHEMIN_ETAT,
    CHEMIN_ETAT_BDDS,
    CHEMIN_JOURNAL,
    CHEMIN_PID,
    ENCODAGE,
    REPERTOIRE_DATA,
)


def calculer_empreinte(chemin):
    """Calcule l'empreinte SHA-256 d'un fichier."""
    hacheur = hashlib.sha256()
    with open(chemin, "rb") as flux:
        for bloc in iter(lambda: flux.read(65536), b""):
            hacheur.update(bloc)
    return hacheur.hexdigest()


def calculer_empreinte_si_existe(chemin):
    """Retourne l'empreinte du fichier, ou None s'il est absent (jamais de crash)."""
    if not chemin.exists():
        return None
    return calculer_empreinte(chemin)


def lire_empreinte_enregistree(nom_bdd):
    """Retourne l'empreinte etalon d'une BDD, ou None si absente."""
    chemin = REPERTOIRE_DATA / (nom_bdd + ".sha256")
    if not chemin.exists():
        return None
    return chemin.read_text(encoding=ENCODAGE).strip()


def chemin_bdd(nom_bdd):
    """Retourne le chemin complet d'une BDD du registre."""
    return REPERTOIRE_DATA / nom_bdd


def nombre_bdds():
    """Retourne la taille du registre (pour la normalisation du taux)."""
    return len(BDDS)


def horodater():
    """Retourne la date-heure locale au format du journal."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def journaliser(entree, chemin=None):
    """Ajoute UNE ligne au journal (en ajout seul, jamais modifie a posteriori).

    `chemin` est facultatif : le journal de service par defaut, ou celui d'une
    AUTRE racine (cobaye). Un cobaye ecrit dans SON journal, jamais dans celui du
    service (lecon L-015 : un test ne laisse aucune trace dans un append-only).
    """
    chemin = chemin or CHEMIN_JOURNAL
    entree = dict(entree)
    entree["date"] = horodater()
    # Fins de ligne LF FORCEES (convention-integrite-sha256 / lecon L-001) : sans
    # cela, Windows ecrit du CRLF et le journal melange les deux fins de ligne
    # des qu'une rotation l'a reecrit -- une empreinte derivante sans difference
    # logique, et un journal qui ne se compare plus a lui-meme.
    with open(str(chemin), "a", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(json.dumps(entree, ensure_ascii=True) + "\n")


def lire_lignes_journal(chemin=None):
    """Retourne les lignes BRUTES du journal (sans fin de ligne, vides ecartees).

    Lecture complete : reservee a la ROTATION, qui doit tout voir pour ne rien
    perdre. Les suites, elles, lisent la QUEUE (lire_queue_journal).
    """
    chemin = chemin or CHEMIN_JOURNAL
    if not chemin.exists():
        return []
    with open(str(chemin), "r", encoding=ENCODAGE, errors="replace") as flux:
        return [ligne.rstrip("\r\n") for ligne in flux if ligne.strip()]


def lire_queue_journal(chemin, octets):
    """Retourne les DERNIERES lignes d'un journal, sans balayer l'historique.

    On lit les `octets` de la fin du fichier ; la premiere ligne lue peut etre
    TRONQUEE (on a coupe au milieu) et n'est donc gardee que si la lecture a
    commence au debut du fichier. C'est ce qui rend le cout constant : que le
    journal pese 1 Mo ou 1 Go, on ne lit que la queue.
    """
    if not chemin.is_file():
        return []
    try:
        taille = chemin.stat().st_size
    except OSError:
        return []
    debut = max(0, taille - octets)
    try:
        with open(str(chemin), "rb") as flux:
            flux.seek(debut)
            bloc = flux.read()
    except OSError:
        return []
    lignes = bloc.decode(ENCODAGE, errors="replace").splitlines()
    if debut > 0 and lignes:
        lignes = lignes[1:]
    return [ligne for ligne in lignes if ligne.strip()]


def empreinte_fichier(chemin):
    """Retourne (taille en octets, mtime en nanosecondes) ; (None, None) si absent.

    Sert a la rotation : la taille est un VERSIONNAGE bon marche du journal (un
    ajout la fait bouger) et c'est ce qui permet de refuser d'ecraser ce qui a
    ete ecrit pendant la rotation.
    """
    try:
        etat = os.stat(str(chemin))
    except OSError:
        return None, None
    return etat.st_size, etat.st_mtime_ns


def ecrire_etat(donnees, chemin=None):
    """Ecrit un ETAT COURT (une ligne JSON), de facon ATOMIQUE.

    `chemin` est facultatif : l'etat de CADENCE par defaut (ecrit au demarrage),
    ou l'etat DU CONTROLE -- le tableau des BDD (MO-081). Ecrase a chaque appel :
    ce n'est pas une histoire, c'est un etat. UNE SEULE LIGNE et une ecriture
    atomique, pour qu'un lecteur de journal puisse le lire ligne par ligne sans
    jamais tomber sur un fichier tronque.
    """
    chemin = chemin or CHEMIN_ETAT
    contenu = json.dumps(donnees, ensure_ascii=True, sort_keys=True) + "\n"
    temporaire = chemin.with_name(chemin.name + ".tmp")
    with open(str(temporaire), "w", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(contenu)
    os.replace(str(temporaire), str(chemin))
    return chemin


def ecrire_etat_bdds(donnees, chemin=None):
    """Ecrit l'ETAT COURT du CONTROLE : le tableau des BDD vues par la passe.

    C'est un etat, pas une histoire : il est ECRASE a chaque passe et porte le
    tableau COMPLET, la signature du dernier tableau ECRIT au journal et le
    nombre de passes absorbees depuis -- de quoi distinguer "rien a ecrire" de
    "la routine est morte" (le compteur AVANCE a chaque tour).
    """
    return ecrire_etat(donnees, chemin or CHEMIN_ETAT_BDDS)


def lire_etat_bdds(chemin=None):
    """Lit l'etat du controle ; {} si absent ou illisible (jamais de crash)."""
    chemin = chemin or CHEMIN_ETAT_BDDS
    try:
        return json.loads(chemin.read_text(encoding=ENCODAGE))
    except (OSError, ValueError):
        return {}


def ecrire_pid(pid):
    """Note le PID de la boucle dans espion.pid."""
    CHEMIN_PID.write_text(str(pid) + "\n", encoding=ENCODAGE)


def lire_pid():
    """Retourne le PID de la boucle, ou None si absent."""
    if not CHEMIN_PID.exists():
        return None
    contenu = CHEMIN_PID.read_text(encoding=ENCODAGE).strip()
    return int(contenu) if contenu else None


def supprimer_pid():
    """Retire espion.pid (arret propre)."""
    if CHEMIN_PID.exists():
        os.remove(CHEMIN_PID)
