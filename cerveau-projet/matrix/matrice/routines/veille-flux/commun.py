"""Fonctions communes de la routine veille-flux : une seule tache chacune."""
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

from constants import (
    BUDGET_PASSE_MS,
    CHEMIN_BOITE_MATRICE_IN,
    CHEMIN_CADENCE,
    CHEMIN_ENTONNOIR,
    CHEMIN_ETAT_ALERTES,
    CHEMIN_JOURNAL,
    CHEMIN_PID,
    CHEMIN_SIGNALER,
    ENCODAGE,
    ETATS_TESTES,
    EXPEDITEUR_SIGNAL,
    LONGUEUR_MAX_COMMANDE,
    LOT_PY_COMPILE_MAX,
    MISSION_SIGNAL,
    NIVEAU_DEFAUT,
    NIVEAU_PAR_ETAT,
    NOM_ARCHIVE_BOITE_PREFIXE,
    OUTIL_SIGNAL,
    PREFIXE_ZONE,
    REPERTOIRE_MATRIX,
    TIMEOUT_COMBO_SECONDES,
    THEME_REPARATION,
    URGENCE_VEILLE,
    env_console_sure,
)

# L'interpreteur vient de son DOMICILE PARTAGE (data/commun/interpreteur.py), non
# de constants.py : une valeur, une maison (M-076). data/commun est deja installe
# dans sys.path par l'import de constants juste au-dessus.
from interpreteur import chemin_python  # noqa: E402


def horodater():
    """Retourne la date-heure locale au format du journal."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def journaliser(entree):
    """Ajoute UNE ligne au journal (en ajout seul, jamais modifie a posteriori).

    Fins de ligne LF FORCEES (lecon L-001, convention-integrite-sha256) : sans
    cela Windows ecrit du CRLF et le journal melange les deux fins de ligne des
    qu'une rotation le reecrit -- une empreinte qui derive sans difference
    logique, et un journal qui ne se compare plus a lui-meme.
    """
    entree = dict(entree)
    entree["date"] = horodater()
    with open(CHEMIN_JOURNAL, "a", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(json.dumps(entree, ensure_ascii=True) + "\n")


def publier_cadence(intervalle, mode=None):
    """Publie la cadence EFFECTIVE dans un etat COURT (veille-cadence.json).

    Pourquoi un fichier a part (lecon L-040, mesuree en MO-077/MO-078) : le
    journal est ROTATIONNE -- un jour, l'evenement de demarrage quitte le journal
    actif pour l'archive, et un controle qui cherche la cadence DANS LE JOURNAL
    devient AVEUGLE, c'est-a-dire neutralise par le nettoyage qu'il surveille.
    Un etat se lit dans un fichier d'etat, une histoire se lit dans un journal.
    """
    donnees = {"type": "demarrage", "intervalle": intervalle, "pid": os.getpid(), "date": horodater()}
    if mode:
        donnees["mode"] = mode
    # Budget declare (MO-097) : publie ICI pour que le cockpit LISE le budget de
    # la routine au lieu de comparer a un seuil en dur. Etat court PUBLIE, comme
    # la cadence (doctrine : une valeur declaree se lit, elle ne se devine pas).
    donnees["budget_passe_ms"] = BUDGET_PASSE_MS
    temporaire = CHEMIN_CADENCE.with_name(CHEMIN_CADENCE.name + ".tmp")
    with open(str(temporaire), "w", encoding=ENCODAGE, newline="\n") as flux:
        flux.write(json.dumps(donnees, ensure_ascii=True, sort_keys=True) + "\n")
    os.replace(str(temporaire), str(CHEMIN_CADENCE))
    return CHEMIN_CADENCE


def ecrire_pid(pid):
    """Note le PID de la boucle dans veille-flux.pid."""
    CHEMIN_PID.write_text(str(pid) + "\n", encoding=ENCODAGE)


def lire_pid():
    """Retourne le PID de la boucle, ou None si absent."""
    if not CHEMIN_PID.exists():
        return None
    contenu = CHEMIN_PID.read_text(encoding=ENCODAGE).strip()
    return int(contenu) if contenu else None


def supprimer_pid():
    """Retire veille-flux.pid (arret propre)."""
    if CHEMIN_PID.exists():
        os.remove(CHEMIN_PID)


def relativiser(chemin):
    """Retourne le chemin RELATIF a matrix/ (portabilite) ; inchange si dehors.

    py_compile cite des chemins ABSOLUS. Les PERSISTER (signature anti-spam,
    theme de mission) les rendrait faux des que le projet change de racine -- et
    `cible_fichier_morte` les declarerait MORTS a tort sur une autre machine.
    On stocke donc du relatif et on resout a l'usage (doctrine : chemin
    DETECTE, jamais suppose). `as_posix()` garde des `/` valables partout.
    """
    try:
        return Path(chemin).resolve().relative_to(REPERTOIRE_MATRIX.resolve()).as_posix()
    except (ValueError, OSError):
        return chemin


def resoudre(chemin):
    """Resout un chemin de signature : relatif a matrix/ s'il est relatif."""
    chemin = Path(chemin)
    if chemin.is_absolute():
        return chemin
    return REPERTOIRE_MATRIX / chemin


def cible_fichier_morte(signature):
    """True si la signature porte une cible fichier qui n'existe plus (M-051/M-052).

    Seules les signatures python-compile portent une cible fichier ; toute
autre signature (ou cible non-fichier comme 'py_compile') n'est jamais
declaree morte. La cible peut etre RELATIVE (matrix/...) : on la resout sur la
racine detectee, sinon un projet deplace ferait declarer mortes des cibles
vivantes (et l'alerte serait purgee a tort).
    """
    if not signature.startswith("python-compile:"):
        return False
    cible = signature.split(":", 1)[1]
    if not ("\\" in cible or "/" in cible):
        return False
    return not resoudre(cible).exists()


def purger_signatures_mortes():
    """Retire les signatures dont la cible n'existe plus (M-051).

    Une signature morte bloquerait la future alerte si la cible etait recreee.
    Seules les signatures python-compile portent une cible fichier ; les autres
    sont conservees telles quelles. Jamais bloquant : tout incident est
    journalise et la passe continue.
    """
    try:
        etat = charger_alertes_emises()
    except Exception as erreur:
        journaliser({"type": "incident-purge", "detail": str(erreur)})
        return
    vivantes = {}
    for signature, date in etat.items():
        if cible_fichier_morte(signature):
            continue
        vivantes[signature] = date
    if len(vivantes) == len(etat):
        return
    purges = len(etat) - len(vivantes)
    try:
        CHEMIN_ETAT_ALERTES.write_text(
            json.dumps(vivantes, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
            encoding=ENCODAGE,
        )
    except Exception as erreur:
        journaliser({"type": "incident-purge", "detail": str(erreur)})
        return
    journaliser({"type": "purge-signatures", "purgees": purges})


def purger_signatures_resolues(mode, detections):
    """Retire les signatures dont l'etat est re-teste et n'est plus detecte.

    Le garde-fou d'anti-spam (une alerte par signature) devient un piege quand
    plus rien ne purge : une signature `ascii-non-convertible:U+XXXX` dont le
    caractere a disparu du disque restait "vivante" POUR TOUJOURS -- 5 des 9
    signatures de l'etat -- et bloquait silencieusement toute alerte future du
    meme caractere. On ne purge QUE les etats que ce mode RE-TESTE vraiment
    (voir ETATS_TESTES) : `marbre` n'est teste qu'en VIGILE, le purger en RELAX
    relancerait l'alerte a chaque passe VIGILE (fausse boucle).
    Jamais bloquant : tout incident est journalise et la passe continue.
    """
    etats_testes = ETATS_TESTES.get(mode, ())
    if not etats_testes:
        return
    try:
        etat = charger_alertes_emises()
    except Exception as erreur:
        journaliser({"type": "incident-purge", "detail": str(erreur)})
        return
    vivantes = set(str(detection["etat"]) + ":" + str(detection["cible"]) for detection in detections)
    resolues = [
        signature for signature in etat
        if signature.split(":", 1)[0] in etats_testes and signature not in vivantes
    ]
    if not resolues:
        return
    for signature in resolues:
        del etat[signature]
    try:
        CHEMIN_ETAT_ALERTES.write_text(
            json.dumps(etat, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
            encoding=ENCODAGE,
        )
    except Exception as erreur:
        journaliser({"type": "incident-purge", "detail": str(erreur)})
        return
    journaliser({
        "type": "purge-signatures-resolues", "mode": mode,
        "purgees": len(resolues), "signatures": resolues,
    })


def purger_alertes_fantomes():
    """Retire les alertes-grave fantomes de la boite Matrice (M-052).

    Une alerte-grave python-compile dont le fichier cible n'existe plus est
    un fantome : son incident est deja resolu ou sans objet. Les AUTRES
    messages de la boite (fin-mission, retour-lot, incident, alertes vivantes)
    sont INTOUCHABLES. Jamais bloquant : tout incident est journalise.
    """
    if not CHEMIN_BOITE_MATRICE_IN.exists():
        return
    try:
        lignes = CHEMIN_BOITE_MATRICE_IN.read_text(encoding=ENCODAGE).splitlines()
        messages = [json.loads(ligne) for ligne in lignes if ligne.strip()]
    except Exception as erreur:
        journaliser({"type": "incident-purge-boite", "detail": str(erreur)})
        return
    vivantes = []
    purges = 0
    for message in messages:
        if message.get("type") == "alerte-grave" and cible_fichier_morte(
            message.get("etat", "") + ":" + str(message.get("cible", ""))
        ):
            purges += 1
            continue
        vivantes.append(message)
    if purges == 0:
        return
    try:
        CHEMIN_BOITE_MATRICE_IN.write_text(
            "".join(json.dumps(m, ensure_ascii=True) + "\n" for m in vivantes),
            encoding=ENCODAGE,
        )
    except Exception as erreur:
        journaliser({"type": "incident-purge-boite", "detail": str(erreur)})
        return
    journaliser({"type": "purge-boite", "purgees": purges})


def chemin_archive_boite(maintenant=None):
    """Le chemin de l'archive NOMINATIVE du jour, posee a cote de la boite."""
    jour = (maintenant or datetime.now()).strftime("%Y%m%d")
    return CHEMIN_BOITE_MATRICE_IN.parent / (NOM_ARCHIVE_BOITE_PREFIXE + "-" + jour + ".jsonl")


def archiver_messages(messages, motif, mode):
    """Ecrit les messages retires dans l'archive du jour, AVEC leur motif.

    Le message COMPLET est conserve, augmente de purge_le, motif et mode : une
    purge sans archive est indiscernable d'une disparition. Ajout seul ; rend le
    chemin de l'archive, ou None si l'ecriture a echoue (l'incident est journalise,
    la passe continue).
    """
    chemin = chemin_archive_boite()
    try:
        with open(chemin, "a", encoding=ENCODAGE) as fichier:
            for message in messages:
                enregistre = dict(message)
                enregistre["purge_le"] = horodater()
                enregistre["motif"] = motif
                enregistre["mode"] = mode
                fichier.write(json.dumps(enregistre, ensure_ascii=True) + chr(10))
    except Exception as erreur:
        journaliser({"type": "incident-archive-boite", "detail": str(erreur)})
        return None
    return chemin


def purger_alertes_resolues(mode, detections):
    """Retire de la BOITE les alerte-grave dont l'etat est RE-TESTE et plus detecte.

    M-052 (purger_alertes_fantomes) ne connait QU'UN motif de retrait : la cible
    fichier DISPARUE. Une alerte dont le defaut est REPARE -- le fichier existe et
    compile, le caractere a ete converti -- restait donc dans la boite POUR
    TOUJOURS, comptee comme anormale par le routeur a chaque passe. Mesure MO-187 :
    les 11 alerte-grave de la boite etaient dans ce cas, AUCUNE n'etait un fantome.

    Ici la BOITE recoit la MEME regle que l'etat anti-spam
    (purger_signatures_resolues) : une alerte dont l'etat est RE-TESTE par ce mode
    (ETATS_TESTES) et dont la signature n'est PLUS dans les detections est
    RESOLUE. Les autres messages (fin-mission, retour-lot, signaler) sont
    INTOUCHABLES (M-052). Le retrait est TRACE : archive nominative + journal.
    Jamais bloquant : tout incident est journalise et la passe continue.
    """
    etats_testes = ETATS_TESTES.get(mode, ())
    if not etats_testes or not CHEMIN_BOITE_MATRICE_IN.exists():
        return
    try:
        lignes = CHEMIN_BOITE_MATRICE_IN.read_text(encoding=ENCODAGE).splitlines()
        messages = [json.loads(ligne) for ligne in lignes if ligne.strip()]
    except Exception as erreur:
        journaliser({"type": "incident-purge-boite", "detail": str(erreur)})
        return
    vivantes = set(
        str(detection["etat"]) + ":" + str(detection["cible"])
        for detection in detections
    )
    resolues = []
    gardees = []
    for message in messages:
        etat = str(message.get("etat", ""))
        signature = etat + ":" + str(message.get("cible", ""))
        if (
            message.get("type") == "alerte-grave"
            and not message.get("traite_par_routeur")
            and etat in etats_testes
            and signature not in vivantes
        ):
            resolues.append(message)
            continue
        gardees.append(message)
    if not resolues:
        return
    chemin_archive = archiver_messages(
        resolues,
        "etat re-teste par la passe " + mode + " : plus detecte",
        mode,
    )
    try:
        CHEMIN_BOITE_MATRICE_IN.write_text(
            "".join(json.dumps(m, ensure_ascii=True) + chr(10) for m in gardees),
            encoding=ENCODAGE,
        )
    except Exception as erreur:
        journaliser({"type": "incident-purge-boite", "detail": str(erreur)})
        return
    journaliser({
        "type": "purge-boite-resolues", "mode": mode, "purgees": len(resolues),
        "archive": str(chemin_archive) if chemin_archive else "",
        "signatures": [str(m.get("etat", "")) + ":" + str(m.get("cible", "")) for m in resolues],
    })


def charger_alertes_emises():
    """Retourne l'etat des alertes deja emises {signature: date} (ou {})."""
    if not CHEMIN_ETAT_ALERTES.exists():
        return {}
    return json.loads(CHEMIN_ETAT_ALERTES.read_text(encoding=ENCODAGE))


def enregistrer_alerte_emise(signature):
    """Note UNE alerte comme emise (anti-spam : une seule alerte par signature)."""
    etat = charger_alertes_emises()
    etat[signature] = horodater()
    CHEMIN_ETAT_ALERTES.write_text(
        json.dumps(etat, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding=ENCODAGE,
    )


def niveau_pour_etat(etat):
    """Retourne le niveau d'alerte d'un etat (NIVEAU_DEFAUT si l'etat est inconnu)."""
    return NIVEAU_PAR_ETAT.get(etat, NIVEAU_DEFAUT)


def deposer_signal(etat, cible, detail):
    """Depose UNE alerte par la PORTE OFFICIELLE `signaler` (jamais en direct).

    La boite de la Matrice a DEUX consommateurs (routeur-maintenance puis
    maintenir) et tous deux ne routent que `type == "signaler"`. La porte tient
    ce format ; une ecriture directe en `alerte-grave` etait une porte PIRATE :
    comptee en `ignores` anonymes, jamais vue par personne. Retourne (code, sortie).
    """
    description = OUTIL_SIGNAL + " : " + etat + " | " + cible + " | " + detail
    arguments = [
        "signaler",
        "--outil", OUTIL_SIGNAL,
        "--niveau", niveau_pour_etat(etat),
        "--description", description,
        "--mission", MISSION_SIGNAL,
        "--expediteur", EXPEDITEUR_SIGNAL,
    ]
    return lancer_combo(CHEMIN_SIGNALER, arguments)


def alerte_grave(etat, cible, detail):
    """Depose UNE alerte grave par la porte `signaler` (une seule fois par signature).

    Retourne True si l'alerte est NOUVELLE (emise), False sinon.
    Si la porte est injoignable, la signature n'est PAS marquee : la passe
    suivante reessaiera (jamais d'alerte perdue en silence).
    """
    signature = etat + ":" + cible
    if signature in charger_alertes_emises():
        return False
    try:
        code, sortie = deposer_signal(etat, cible, detail)
    except OSError as erreur:
        journaliser({"type": "incident-signal", "etat": etat, "cible": cible, "detail": str(erreur)})
        return False
    if code != 0:
        journaliser({
            "type": "incident-signal", "etat": etat, "cible": cible,
            "code": code, "detail": sortie[:200],
        })
        return False
    enregistrer_alerte_emise(signature)
    journaliser({"type": "alerte", "etat": etat, "cible": cible})
    deposer_mission_vrac(etat, cible, detail)
    return True


def deposer_mission_vrac(etat, cible, detail):
    """Verse UNE mission-reparation au vrac de l'entonnoir (M-020, echec jamais bloquant).

    L'anti-spam des alertes garantit UN depot par signature (une alerte nouvelle,
    une mission nouvelle). Theme commence par 'reparer' : le classement propose
    de l'entonnoir le rangera en reparation.
    """
    arguments = (
        ["deposer", "--theme", THEME_REPARATION + " " + cible,
         "--objectif", etat + " : " + detail,
         "--urgence", URGENCE_VEILLE, "--source", "veille"]
    )
    try:
        code_depot, sortie = lancer_combo(CHEMIN_ENTONNOIR, arguments)
    except OSError as erreur:
        journaliser({"type": "incident-depot-vrac", "detail": str(erreur)})
        return
    if code_depot != 0:
        journaliser({"type": "incident-depot-vrac", "code": code_depot, "detail": sortie[:200]})
        return
    journaliser({"type": "mission-vrac", "cible": cible})


def charger_base_acceptee():
    """Retourne l'ensemble des codes Unicode acceptes (base-acceptee.json), ou set() vide.

    Garde (classe MO-035) : une base ILLISIBLE (JSON corrompu, disque) ne doit
    JAMAIS tuer la passe -- ce serait une mort silencieuse entre `passe-debut`
    et `passe-fin`, exactement le mode de panne qui a rendu la veille muette
    pendant 11 heures. Une base illisible est traitee comme une base ABSENTE
    (comportement deja en place) et l'incident est JOURNALISE.
    """
    from constants import CHEMIN_BASE

    if not CHEMIN_BASE.exists():
        return set()
    try:
        donnees = json.loads(CHEMIN_BASE.read_text(encoding=ENCODAGE))
        return set(donnees.get("acceptes", ()))
    except (OSError, ValueError) as erreur:
        journaliser({"type": "incident-base-acceptee", "detail": str(erreur)})
        return set()


def lancer_combo(chemin_outil, arguments):
    """Lance UN combo (outil Python de la Matrice). Retourne (code, sortie).

    Garde E-045 : timeout=TIMEOUT_COMBO_SECONDES. Un combo qui depasse le delai
    est tue (TimeoutExpired) et l'incident est journalise : la boucle ne pend
    jamais. Code retourne : 124 (convention unix de kill par timeout).
    """
    commande = [chemin_python(), "main.py"] + list(arguments)
    try:
        termine = subprocess.run(
            commande,
            cwd=str(chemin_outil),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env_console_sure(),
            timeout=TIMEOUT_COMBO_SECONDES,
        )
    except subprocess.TimeoutExpired:
        journaliser({"type": "incident-combo-bloquant", "combo": str(chemin_outil),
                     "arguments": " ".join(arguments), "timeout": TIMEOUT_COMBO_SECONDES})
        return 124, "combo tue par timeout " + str(TIMEOUT_COMBO_SECONDES) + "s"
    return termine.returncode, (termine.stdout or "") + (termine.stderr or "")


def lister_fichiers_python():
    """Retourne la liste triee des .py de matrix/ (hors __pycache__ et jetables).

    EO-175 : les ZONES JETABLES (`tmp-*`, motif PREFIXE_ZONE lu chez son
    moteur data/commun/zone_tmp.py) sont HORS PERIMETRE de la veille. Leur
    contenu est vide en fin de mission (regle immuable `perimetre-tmp.md`,
    point 4) : un .py qui ne compile pas y est un etat PASSAGER, jamais un
    defaut durable. Les compiler a fabrique EO-140 -- une mission de
    reparation BLOQUANTE et SANS ROLE dont la cible
    (`tmp-optimus/mo160-cobaye/p11/cible.py`) avait deja disparu : un item ne
    dans le vide, que personne ne pouvait reparer.

    Une zone `tmp-*` trouvee ailleurs qu a la racine reste un ECART -- mais
    c est le DOMICILE que juge le garde des zones (garde-tmp), pas la veille :
    une seule maison par idee. La veille regarde le CODE du projet, pas le
    jetable.
    """
    fichiers = []
    for racine, dossiers, noms in os.walk(str(REPERTOIRE_MATRIX)):
        dossiers[:] = [
            dossier for dossier in dossiers
            if dossier != "__pycache__" and not dossier.startswith(PREFIXE_ZONE)
        ]
        for nom in noms:
            if nom.endswith(".py"):
                fichiers.append(os.path.join(racine, nom))
    return sorted(fichiers)


def compiler_lot(fichiers):
    """Compile UN seul lot de .py (une ligne de commande). Retourne (code, sortie).

    Garde E-045 : meme timeout que les combos (l'incident est journalise).
    Garde Windows MO-035 : tout OSError de lancement (dont WinError 206 --
    ligne de commande trop longue) devient une detection journalisee, jamais
    une exception qui remonte et tue la passe.
    """
    commande = [chemin_python(), "-m", "py_compile"] + list(fichiers)
    try:
        termine = subprocess.run(
            commande,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env_console_sure(),
            timeout=TIMEOUT_COMBO_SECONDES,
        )
    except subprocess.TimeoutExpired:
        journaliser({"type": "incident-py-compile-bloquant",
                     "timeout": TIMEOUT_COMBO_SECONDES})
        return 124, "py_compile tue par timeout " + str(TIMEOUT_COMBO_SECONDES) + "s"
    except OSError as erreur:
        journaliser({"type": "incident-py-compile-lancement", "detail": str(erreur)})
        return 1, "py_compile impossible a lancer : " + str(erreur)
    return termine.returncode, (termine.stdout or "") + (termine.stderr or "")


def decouper_lots(fichiers, longueur_max=LONGUEUR_MAX_COMMANDE, max_fichiers=LOT_PY_COMPILE_MAX):
    """Decoupe les fichiers en lots tenant sous la LONGUEUR de commande declaree.

    MO-097 : le lot etait un NOMBRE fixe (40) -- un plancher tres prudent qui
    multipliait les demarrages d'interpreteur : 435 .py = 11 lots = 11 processus,
    ~460 ms de pure tare par passe (mesure du 2026-09-15). La contrainte REELLE
    est la longueur de la ligne de commande (plafond Windows ~32767, garde
    MO-035) : on accumule donc les chemins jusqu'au budget DECLARE, avec un
    plafond de securite en nombre. Couverture INCHANGEE : tous les fichiers
    passent, dans l'ordre, et un chemin plus long que le budget part seul (il ne
    peut pas etre reparti).
    """
    lots = []
    courant = []
    longueur = 0
    for fichier in fichiers:
        taille = len(str(fichier)) + 1
        if courant and (longueur + taille > longueur_max or len(courant) >= max_fichiers):
            lots.append(courant)
            courant = []
            longueur = 0
        courant.append(fichier)
        longueur += taille
    if courant:
        lots.append(courant)
    return lots


def lancer_py_compile(fichiers=None):
    """Compile les .py de matrix/ PAR LOTS. Retourne (code, sortie).

    MO-035 : compiler les 352 .py en UNE commande depassait la limite de la
    ligne de commande Windows (WinError 206) et tuait la passe. Les sorties de
    lots sont concatenees : le contrat d'extraction des fichiers en erreur est
    inchange. Code retourne : 0 si tous les lots passent, sinon le PREMIER code
    d'echec (1 = ecart confirme, 124 = lot tue par timeout).
    MO-097 : les lots se decoupent sur la LONGUEUR de commande (decouper_lots),
    pas sur un nombre fixe de fichiers -- moins de processus, donc moins de tare.
    MO-182 : la passe est EXHAUSTIVE. Mesure du cobaye de MO-181 : avec DEUX .py
    casses dans un meme lot, py_compile ne cite QUE le premier (le processus
    s arrete la) ; or la passe ne remonte que les fichiers CITES, donc un seul
    item par passe -- les autres fichiers casses restaient INVISIBLES tant que
    le premier n etait pas repare. Le lot est donc REJOUE en RETIRANT les
    fichiers deja accuses, tant qu il en reste : cout nul quand tout compile
    (un seul appel par lot, la cadence de MO-097 est preservee).
    """
    if fichiers is None:
        fichiers = lister_fichiers_python()
    fichiers = list(fichiers)
    code_global = 0
    sorties = []
    for lot in decouper_lots(fichiers):
        restants = lot
        while True:
            code, sortie = compiler_lot(restants)
            sorties.append(sortie)
            if code != 0 and code_global == 0:
                code_global = code
            if code == 0:
                break
            accuses = [
                os.path.normcase(os.path.normpath(str(chemin)))
                for chemin in extraire_fichiers_python_en_erreur(sortie)
            ]
            suivants = [
                fichier for fichier in restants
                if os.path.normcase(os.path.normpath(str(fichier))) not in accuses
            ]
            if not suivants or len(suivants) == len(restants):
                break
            restants = suivants
    return code_global, "".join(sorties)


def sortie_en_crash(sortie):
    """Retourne True si la sortie d'un sous-processus porte la signature d'un crash.

    Un code de sortie 1 peut etre LEGITIME (ecarts detectes) : seule la signature
    de crash fait foi pour distinguer un echec du processus d'un verdict d'outil.
    """
    return "Fatal Python error" in sortie or "Traceback (most recent call last)" in sortie


def extraire_codes_unicode(sortie):
    """Retourne les codes U+XXXX cites dans la sortie d'un combo (contrat de nos outils)."""
    return sorted(set(re.findall(r"U\+[0-9A-Fa-f]{4,6}", sortie)))


def extraire_fichiers_python_en_erreur(sortie):
    """Retourne les chemins des fichiers qui ne compilent pas (sortie py_compile)."""
    return sorted(set(re.findall(r'File "([^"]+\.py)"', sortie)))
