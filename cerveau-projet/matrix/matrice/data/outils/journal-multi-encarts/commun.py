"""Fonctions communes de l'outil journal-multi-encarts : une seule tache chacune.

Format createur (M-080) : chaque encart est un TABLEAU a 3 colonnes
(Entree | Heure | Date), heure et date SEPAREES, format 'HH:MM:SS' et
'JJ/MM/AAAA'. Chaque encart porte SA ligne de FLUX : d'ou viennent les
informations, vers ou elles vont (tracabilite, demande createur).
"""
import json
import re

from constants import (
    CHEMIN_ALERTES,
    CHEMIN_BDD_LECONS,
    CHEMIN_BDD_MODIFICATIONS,
    CHEMIN_BDD_USAGES,
    CHEMIN_BOITE_CAMELEON,
    CHEMIN_CLASSEUR_VARIABLES,
    CHEMIN_ENTONNOIR_FILES,
    CHEMIN_FILE_MISSIONS,
    CHEMIN_INBOX_MATRICE,
    ENCODAGE,
)

# data/commun (motif unique M-076) : la LECTURE BORNEE d'un journal est partagee,
# jamais recopiee -- elle vient avec le moteur de rotation (MO-078). L'import est
# VOLONTAIREMENT apres celui de constants : c'est constants qui installe
# data/commun dans sys.path (ne pas trier alphabetiquement).
from rotation_journal import lire_queue_journal, octets_queue_du_journal  # noqa: E402

# Horodatage Matrice (YYYY-MM-DD HH:MM:SS) extrait des lignes brutes.
MOTIF_DATE = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")


def separer(source):
    """Retourne (heure 'HH:MM:SS', date 'JJ/MM/AAAA') extraites d'une source.

    Sans date trouvable : couple vide (jamais de '?').
    """
    trouve = MOTIF_DATE.search(str(source)) if source else None
    if not trouve:
        return "", ""
    date, heure = trouve.group(1).split(" ", 1)
    annee, mois, jour = date.split("-")
    return heure, jour + "/" + mois + "/" + annee


def paire(corps, source):
    """Retourne le triple (corps, heure, date) d'une entree d'encart."""
    heure, date = separer(source)
    return str(corps), heure, date


def composer_encart(titre, flux, entrees):
    """Compose UN encart markdown : ligne de flux + TABLEAU a 3 colonnes.

    Encart vide = tableau present avec '(aucune entree)' -- jamais en vrac.
    Les barres verticales du corps sont echappees (tableau intact).
    """
    blocs = [
        "## Encart : " + titre,
        "",
        "Flux : " + flux,
        "",
        "| Entree | Heure | Date |",
        "|---|---|---|",
    ]
    if not entrees:
        return blocs + ["(aucune entree)", ""]
    for corps, heure, date in entrees:
        corps_propre = str(corps).replace("|", "\\|")
        blocs.append("| " + corps_propre + " | " + str(heure) + " | " + str(date) + " |")
    return blocs + [""]


def charger_json(chemin, defaut):
    """Charge UN fichier JSON ; retourne defaut si absent ou casse (jamais bloquant)."""
    try:
        return json.loads(chemin.read_text(encoding=ENCODAGE))
    except (OSError, ValueError):
        return defaut


def lire_lignes_jsonl(chemin, maximum):
    """Retourne les `maximum` dernieres lignes d'un JSONL (jamais bloquant)."""
    try:
        lignes = chemin.read_text(encoding=ENCODAGE).splitlines()
    except OSError:
        return []
    entrees = []
    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            entrees.append(json.loads(ligne))
        except ValueError:
            continue
    return entrees[-maximum:]


def entrees_missions():
    """Encart missions : mission en cours + file pilote + entonnoir."""
    entrees = []
    file_data = charger_json(CHEMIN_FILE_MISSIONS, {"missions": []})
    for mission in file_data.get("missions", ()):
        if mission.get("statut") == "en-cours":
            entrees.append(paire(
                "EN COURS " + mission.get("id", "?") + " -- " + mission.get("theme", "?"),
                mission.get("injectee_le") or mission.get("chargee_le", ""),
            ))
    en_attente = [
        m for m in file_data.get("missions", ()) if m.get("statut") == "en-attente"
    ]
    if en_attente:
        dernier = en_attente[-1]
        entrees.append(paire(
            "file pilote : " + str(len(en_attente)) + " en attente ("
            + ", ".join(m.get("id", "?") for m in en_attente[-5:]) + ")",
            dernier.get("chargee_le", ""),
        ))
    entonnoir = charger_json(CHEMIN_ENTONNOIR_FILES, {})
    vrac = entonnoir.get("vrac", ())
    if vrac:
        entrees.append(paire(
            "vrac : " + str(len(vrac)) + " mission(s) ("
            + ", ".join(m.get("id", "?") for m in vrac) + ")",
            vrac[-1].get("deposee_le", ""),
        ))
    for type_file, compte in sorted(entonnoir.get("files", {}).items()):
        if compte:
            entrees.append(("file " + type_file + " : " + str(compte) + " mission(s)", "", ""))
    brin = entonnoir.get("brin", ())
    if brin:
        entrees.append((
            "brin (tresse) : " + str(len(brin)) + " mission(s) ("
            + ", ".join(m.get("id", "?") for m in brin) + ")", "", "",
        ))
    return entrees


def heure_fichier(chemin):
    """Retourne (heure, date) de la modification d'un fichier (mtime), ou vide."""
    import os
    from datetime import datetime
    try:
        stamp = datetime.fromtimestamp(os.path.getmtime(chemin))
    except OSError:
        return "", ""
    return stamp.strftime("%H:%M:%S"), stamp.strftime("%d/%m/%Y")


def entrees_matrice():
    """Encart matrice : defcon courant + etat des boucles de fond (horodate)."""
    entrees = []
    classeur = charger_json(CHEMIN_CLASSEUR_VARIABLES, {"variables": []})
    for variable in classeur.get("variables", ()):
        if variable.get("cle") == "defcon":
            entrees.append(paire(
                "defcon : " + str(variable.get("valeur")), variable.get("date", "")
            ))
    repertoire = REPERTOIRE_MATRICE_PID() / "routines"
    chemin_veille = repertoire / "veille-flux" / "veille-flux.pid"
    pid_veille = lire_pid(chemin_veille)
    etat_veille = "veille-flux : ACTIVE (PID " + pid_veille + ")" if pid_veille else "veille-flux : ARRET"
    entrees.append((etat_veille,) + heure_fichier(chemin_veille))
    chemin_espion = repertoire / "espion-integrite" / "espion.pid"
    pid_espion = lire_pid(chemin_espion)
    etat_espion = "espion-integrite : ACTIVE (PID " + pid_espion + ")" if pid_espion else "espion-integrite : ARRET"
    entrees.append((etat_espion,) + heure_fichier(chemin_espion))
    return entrees


def REPERTOIRE_MATRICE_PID():
    """Retourne le dossier matrice (chemin des PID des boucles)."""
    from constants import REPERTOIRE_MATRICE
    return REPERTOIRE_MATRICE


def lire_pid(chemin):
    """Lit UN fichier PID (contenu trimmed, ou None si absent)."""
    try:
        return chemin.read_text(encoding=ENCODAGE).strip()
    except OSError:
        return None


def entrees_routines():
    """Encart routines : dernieres passes de la veille, horodatees.

    LECTURE BORNEE (MO-078) : ce lecteur balayait le journal EN ENTIER (3,85 Mo /
    44 050 lignes mesures le 2026-09-13) pour n'en garder que 5 evenements. On
    lit la QUEUE, ce qui rend le cout constant quelle que soit la taille.
    """
    from constants import REPERTOIRE_MATRICE
    chemin = REPERTOIRE_MATRICE / "routines" / "veille-flux" / "journal-veille.txt"
    # MO-099 : la fenetre est demandee AU JOURNAL LU (sa borne declaree), jamais
    # recopiee -- la veille declare 2 Mo de rotation, donc on lit au moins 2 Mo.
    lignes = lire_queue_journal(chemin, octets_queue_du_journal(chemin))
    dernieres = [l for l in lignes if '"passe' in l][-5:]
    entrees = []
    for l in dernieres:
        corps = l.strip()[:120]
        try:
            evenement = json.loads(l)
            if evenement.get("type") == "passe-fin":
                corps = (
                    "passe " + str(evenement.get("mode", "?")) + " terminee : "
                    + str(evenement.get("detections", 0)) + " detection(s), "
                    + str(evenement.get("alertes", 0)) + " alerte(s)"
                )
            elif evenement.get("type") == "passe-debut":
                corps = "passe " + str(evenement.get("mode", "?")) + " demarree"
        except ValueError:
            pass
        entrees.append(paire(corps, l))
    return entrees


def entrees_alertes():
    """Encart alertes : alertes de la veille + intercom matrice, horodatees."""
    entrees = []
    alertes = charger_json(CHEMIN_ALERTES, {})
    signatures = alertes.get("signatures", alertes if isinstance(alertes, list) else {})
    if isinstance(signatures, dict):
        for signature in sorted(signatures)[-5:]:
            entrees.append(paire("veille : " + signature[:100], signature))
    for entree in lire_lignes_jsonl(CHEMIN_INBOX_MATRICE, 5):
        entrees.append(paire(
            "intercom : " + str(entree.get("type", "?"))[:90], entree.get("date", "")
        ))
    return entrees


def entrees_cameleon():
    """Encart cameleon : messages RECUS par le cameleon (sa boite intercom).

    Etancheite conservee : raison "maintenance" seulement, jamais la
    raison reelle de la pause (protocole M-080).
    """
    return [
        paire(
            str(e.get("type", "?")) + " -- mission " + str(e.get("mission", "?")),
            e.get("date", ""),
        )
        for e in lire_lignes_jsonl(CHEMIN_BOITE_CAMELEON, 8)
    ]


def entrees_usages():
    """Encart usages : 8 derniers appels d'outils (BDD usages, sac-a-dos)."""
    return [
        paire(
            str(e.get("outil", "?")) + "/" + str(e.get("commande", "?")) + " code "
            + str(e.get("code", "?")) + " " + str(e.get("duree_ms", "?")) + "ms",
            e.get("date", ""),
        )
        for e in lire_lignes_jsonl(CHEMIN_BDD_USAGES, 8)
    ]


def entrees_modifications():
    """Encart modifications : 5 derniers fichiers notes (BDD modifications)."""
    donnees = charger_json(CHEMIN_BDD_MODIFICATIONS, {"fichiers": {}})
    fichiers = donnees.get("fichiers", donnees)
    if not isinstance(fichiers, dict):
        return []
    couples = []
    for chemin_fichier, detail in fichiers.items():
        notes = detail.get("modifications", ()) if isinstance(detail, dict) else ()
        dernier = notes[-1] if notes else None
        date = dernier.get("date", "?") if isinstance(dernier, dict) else "?"
        couples.append((str(date), str(chemin_fichier)))
    return [paire(c[1], c[0]) for c in sorted(couples)[-5:]]


def entrees_lecons():
    """Encart lecons : les 5 dernieres lecons gravees (BDD lecons)."""
    donnees = charger_json(CHEMIN_BDD_LECONS, {"lecons": []})
    lecons = donnees.get("lecons", donnees.get("entrees", ()))
    if not isinstance(lecons, list):
        return []
    return [
        paire(
            str(l.get("id", "?")) + " " + str(l.get("lecon", ""))[:100],
            l.get("date", ""),
        )
        for l in lecons[-5:]
    ]


def entrees_variables():
    """Encart variables : les cles du classeur-variables (valeurs courantes).

    Valeur vide significative explicite : 'perimetre-cameleon = (perimetre
    complet)' -- le vide est un ETAT (aucune zone exclue), pas une absence.
    """
    classeur = charger_json(CHEMIN_CLASSEUR_VARIABLES, {"variables": []})
    entrees = []
    for v in classeur.get("variables", ()):
        cle = str(v.get("cle", "?"))
        valeur = str(v.get("valeur", ""))
        if cle == "perimetre-cameleon" and not valeur:
            valeur = "(perimetre complet : aucune zone exclue)"
        elif not valeur:
            valeur = "(vide)"
        entrees.append(paire(cle + " = " + valeur, v.get("date", "")))
    return entrees
