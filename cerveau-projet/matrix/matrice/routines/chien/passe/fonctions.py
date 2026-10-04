"""Passe de la routine chien -- LE TRAVAIL DE LA ROUTINE SE POSE ICI.

Contrat d'une passe (le meme que suivi-sync et veille-flux) :
  - `passer()` fait UNE passe et retourne (nombre, messages) :
      nombre   : ce que la passe a traite (entier >= 0) ;
      messages : ce qui doit s'afficher (liste de textes, souvent vide).
  - une passe qui ne peut pas travailler ne LEVE pas : elle rend 0 et un
    message clair. Un echec se DIT, il ne plante pas la boucle.
  - `publier_passe(nombre, messages)` ecrit l'ETAT COURT (le temoin de cadence
    lu par `verifier-cadence`) : ne pas le retirer, ne pas le deplacer.

CE QUE LE CHIEN FAIT, et RIEN DE PLUS : il observe, il compare, et il lance un
COMBO quand quelque chose a bouge. Il ne corrige pas lui-meme. Et le cas le plus
important est celui ou il ne se passe RIEN -- alors il se TAIT.
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime

from battement import ajouter_passe, lire_anneau
from constants import (
    CHEMIN_ETAT,
    CHEMIN_JOURNAL,
    CHEMIN_LANCEUR,
    CLE_ANNEAU_PASSES,
    COMBO_CORRECTION,
    DOSSIERS_EXCLUS,
    DOSSIERS_SURVEILLES,
    ENCODAGE,
    EXTENSIONS,
    FORMAT_HORODATAGE,
    OPTION_APPLIQUER,
    PASSES_GARDEES_ETAT,
    PRODUCTIONS,
    REPERTOIRE_ROUTINE,
    VERBE_CORRECTION,
)
from lancement import drapeaux_popen  # noqa: E402  (le seul lancement, EO-428)


def observer():
    """L EMPREINTE du disque : {chemin: (date_ns, taille)}.

    On lit la DATE et la TAILLE, pas le contenu : 990 fichiers annonces sont lus en
    68 ms (mesure du 2026-10-03). Hasher 990 fichiers a chaque passage serait un
    travail sans fin pour une question qui porte sur l EXISTENCE d un changement,
    pas sur sa nature -- et le contenu ne change jamais d une passe a l autre sans
    que la date bouge avec lui.

    Un fichier qui disparait disparait aussi de l empreinte : le chien voit une
    suppression comme il voit une creation, parce que c est la meme information --
    le repertoire a change.

    LE CHIEN NE S OBSERVE PAS LUI-MEME (mesure du 2026-10-03, premier banc). Il
    ecrivait `chien-etat.json` a chaque passe, son propre fichier entrait donc dans
    son observation, la passe suivante le voyait MODIFIE, et il relancait une
    correction sur son propre souffle. Un chien qui se chasse ne veille sur rien :
    il tourne en boucle sur lui-meme, et le journal le prouve (deux corrections
    consecutives, chacune sur le fichier de l autre).

    On s EXCLUT donc -- pas son dossier entier, mais sa propre production : l etat,
    le journal, le PID et le drapeau. Ses SOURCES, lui, restent surveillees comme
    les autres.
    """
    empreinte = {}
    exclus = set(DOSSIERS_EXCLUS)
    mes_productions = tuple(str(chemin) for chemin in PRODUCTIONS)
    for base in DOSSIERS_SURVEILLES:
        if not base.is_dir():
            continue
        for racine, dossiers, fichiers in os.walk(base):
            dossiers[:] = [d for d in dossiers if d not in exclus]
            if os.path.abspath(racine) == os.path.abspath(str(REPERTOIRE_ROUTINE)):
                # Le dossier du chien : rien de ce qui s y trouve n est du travail
                # du createur, donc rien n a etre corrige par reaction a lui.
                dossiers[:] = []
                continue
            for nom in fichiers:
                if not nom.endswith(EXTENSIONS):
                    continue
                chemin = os.path.join(racine, nom)
                try:
                    infos = os.stat(chemin)
                except OSError:
                    continue
                # UNE LISTE, PAS UN TUPLE (mesure du 2026-10-03, premiere
                # correction du chien). L empreinte passe par du JSON : un tuple y
                # ressort en liste au relecture, et `[12, 3] != (12, 3)` est VRAI
                # dans le meme Python. Le chien voyait donc 1 001 fichiers
                # "modifies" a chaque passe, et relancait une correction sur un
                # disque immobile -- exactement le bruit que le contrat interdit.
                empreinte[chemin] = [infos.st_mtime_ns, infos.st_size]
    return {cle: valeur for cle, valeur in empreinte.items()
            if not cle.endswith((".tmp",)) }


def lire_empreinte():
    """L empreinte precedente, ou VIDE si le chien demarre pour la premiere fois."""
    try:
        donnees = json.loads(CHEMIN_ETAT.read_text(encoding=ENCODAGE))
    except (OSError, ValueError):
        return {}
    if not isinstance(donnees, dict):
        return {}
    empreinte = donnees.get("empreinte")
    return empreinte if isinstance(empreinte, dict) else {}


def ecarts_depuis(avant, maintenant):
    """Ce qui a BOUGE : (crees, modifies, supprimes).

    On rend les trois noms parce qu ils ne veulent pas dire la meme chose : une
    creation est une entree, une modification est le cas ordinaire, une suppression
    veut dire qu une porte a agi. Le chien ne les traite pas de la meme facon -- il
    les DIT tous les trois.
    """
    cles_avant, cles_maintenant = set(avant), set(maintenant)
    crees = sorted(cles_maintenant - cles_avant)
    supprimes = sorted(cles_avant - cles_maintenant)
    modifies = sorted(cle for cle in cles_avant & cles_maintenant
                      if avant[cle] != maintenant[cle])
    return crees, modifies, supprimes


def journaliser(evenement):
    """Trace une intervention. Un journal qu on ne peut pas ecrire ne tue pas le chien."""
    evenement["date"] = datetime.now().strftime(FORMAT_HORODATAGE)
    ligne = json.dumps(evenement, ensure_ascii=True, sort_keys=True)
    try:
        with open(str(CHEMIN_JOURNAL), "a", encoding=ENCODAGE, newline="\n") as flux:
            flux.write(ligne + "\n")
    except OSError:
        pass


def lancer_correction():
    """Lance le combo de correction. Rend (code, duree_ms, sortie).

    SANS FENETRE : c est un travail de fond, il ne doit pas ouvrir une console sur
    le poste de travail. Les drapeaux viennent du moteur partage (contrat EO-428).
    """
    commande = [sys.executable, str(CHEMIN_LANCEUR), "--appelant", "operateur",
                COMBO_CORRECTION, VERBE_CORRECTION, OPTION_APPLIQUER]
    debut = time.time()
    try:
        resultat = subprocess.run(commande, capture_output=True, text=True,
                                  timeout=300, **drapeaux_popen())
    except (OSError, subprocess.SubprocessError) as erreur:
        return 2, int((time.time() - debut) * 1000), str(erreur)[:200]
    sortie = ((resultat.stdout or "") + (resultat.stderr or "")).strip()
    return resultat.returncode, int((time.time() - debut) * 1000), sortie


def passer():
    """UNE passe du chien. Trois cas, et UN SEUL agit.

    1. PREMIER PASSAGE -> prise de temperature : on enregistre ce qu on voit et on ne
       fait RIEN. Sans cette neutralite, le chien viderait le disque de corrections a
       son allumage, et le dirait comme si c etait un changement. Une prise de
       temperature n est pas un evenement.
    2. RIEN A BOUGE -> SILENCE : pas de combo, pas de journal, pas de message. C est
       le contrat du createur ("s eteint jusqu a la prochaine demande") : un chien
       qui relance sur un dossier immobile ne veille pas, il consomme -- et il le
       ferait 4 320 fois par jour.
    3. QUELQUE CHOSE A BOUGE -> le combo part, le geste est trace, l empreinte est
       mise a jour. Un refus du combo est un message DIT, jamais un silence.
    """
    avant = lire_empreinte()
    # LE TEMOIN DE CADENCE : chaque passe laisse son heure, meme la premiere et
    # meme celles qui ne font RIEN. Une passe qui n ecrit rien n en est pas moins
    # une passe -- et une routine qui se tait doit pouvoir prouver qu elle veillait
    # plutot que dormir. C est la difference entre un chien endormi et un chien
    # discret, et on ne la distingue que par cette ligne.
    journaliser({"type": "passe-debut", "mode": "boucle"})
    maintenant = observer()

    if not avant:
        # CAS 1 : premier passage.
        nombre = len(maintenant)
        _ecrire_empreinte(maintenant)
        return 0, ["chien : prise de temperature, " + str(nombre)
                   + " fichier(s) observes (rien ne bouge encore)"]

    crees, modifies, supprimes = ecarts_depuis(avant, maintenant)
    if not (crees or modifies or supprimes):
        # CAS 2 : le silence. C'est le cas le plus frequent, et il doit etre muet.
        _ecrire_empreinte(maintenant)
        return 0, []

    # CAS 3 : quelque chose a bouge.
    code, duree_ms, sortie = lancer_correction()
    resume = (str(len(crees)) + " cree(s), " + str(len(modifies)) + " modifie(s), "
              + str(len(supprimes)) + " supprime(s)")
    journaliser({"type": "correction", "code": code, "duree_ms": duree_ms,
                 "resume": resume, "crees": len(crees), "modifies": len(modifies),
                 "supprimes": len(supprimes),
                 "echantillon": (modifies + crees + supprimes)[:5]})
    _ecrire_empreinte(maintenant)
    if code != 0:
        return 1, ["chien : correction REFUSEE (code " + str(code) + ") apres "
                   + resume + " -- " + sortie[:140]]
    return len(crees) + len(modifies) + len(supprimes), [
        "chien : correction lancee (" + str(duree_ms) + " ms) -- " + resume]


def _ecrire_empreinte(maintenant):
    """L empreinte du chien, ecrit en ATOMIQUE, sans ecraser l'etat de passe.

    `publier_passe` ecrase `chien-etat.json` a chaque passe -- c'est le temoin de
    cadence, et son ANNEAU vit la dessous. On y joint donc l'empreinte, sinon elle
    disparaitrait au passage suivant et le chien repartirait de zero, donc
    rejouerait une correction deja faite.
    """
    donnees = {}
    try:
        lu = json.loads(CHEMIN_ETAT.read_text(encoding=ENCODAGE))
        if isinstance(lu, dict):
            donnees = lu
    except (OSError, ValueError):
        donnees = {}
    donnees["empreinte"] = dict(maintenant)
    donnees["empreinte_le"] = datetime.now().strftime(FORMAT_HORODATAGE)
    donnees["fichiers"] = len(maintenant)
    temporaire = CHEMIN_ETAT.with_name(CHEMIN_ETAT.name + ".tmp")
    with open(str(temporaire), "w", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(json.dumps(donnees, ensure_ascii=True, sort_keys=True) + "\n")
    os.replace(str(temporaire), str(CHEMIN_ETAT))


def publier_passe(nombre, messages):
    """Ecrit l'ETAT COURT de la passe : ce que la routine a fait, et QUAND.

    Le battement REEL d'une routine est un ETAT, pas une histoire (friction 28,
    2026-09-14) : il s'ecrit ici, a CHAQUE passe et ECRASE. C'est ce que lit
    `verifier-cadence`, qui le compare a la cadence DECLAREE.

    Meme contrat que suivi-sync : l'anneau borne vient du moteur PARTAGE
    `data/commun/battement.py` (L-029 : un moteur recopie diverge).
    """
    passe = datetime.now().strftime(FORMAT_HORODATAGE)
    # L EMPREINTE SURVIT A LA PASSE. `publier_passe` ecrase son etat, donc si elle
    # ecrivait un dictionnaire neuf elle effacerait l empreinte -- et le chien, au
    # passage suivant, verrait "aucune empreinte", ferait sa prise de temperature,
    # et ne corrigerait plus JAMAIS rien. Le defaut est mesure : c est exactement ce
    # qu ont fait les deux premieres passes de ce chien. On relit donc l etat et on
    # ne remplace que les cles de la passe.
    donnees = {}
    try:
        lu = json.loads(CHEMIN_ETAT.read_text(encoding=ENCODAGE))
        if isinstance(lu, dict):
            donnees = lu
    except (OSError, ValueError):
        donnees = {}
    donnees["type"] = "passe"
    donnees["date"] = passe
    donnees["traitees"] = nombre
    donnees["messages"] = len(messages or [])
    donnees[CLE_ANNEAU_PASSES] = ajouter_passe(
        lire_anneau(CHEMIN_ETAT, CLE_ANNEAU_PASSES), passe, PASSES_GARDEES_ETAT)
    temporaire = CHEMIN_ETAT.with_name(CHEMIN_ETAT.name + ".tmp")
    with open(str(temporaire), "w", encoding="utf-8", newline="\n") as flux:
        flux.write(json.dumps(donnees, ensure_ascii=True, sort_keys=True) + "\n")
    os.replace(str(temporaire), str(CHEMIN_ETAT))
    return CHEMIN_ETAT
