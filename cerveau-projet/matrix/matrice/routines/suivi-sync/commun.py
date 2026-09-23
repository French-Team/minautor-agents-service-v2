"""Fonctions communes de la routine suivi-sync.

Lecture de l'inbox, synchronisation vers suivi-optimus (append-only,
pas de duplication si l'entree existe deja dans le suivi).
"""
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

from battement import ajouter_passe, lire_anneau
from constants import (
    CHEMIN_ETAT,
    CHEMIN_INBOX,
    CLE_ANNEAU_PASSES,
    ENCODAGE,
    ENCODAGE_ETAT,
    FORMAT_HORODATAGE,
    PASSES_GARDEES_ETAT,
    REPERTOIRE_OUTIL_SUIVI,
    TYPES_INTERESSANTS,
)


def publier_passe(nombre, messages):
    """Ecrit l'ETAT COURT de la passe : ce que la routine a fait, et QUAND.

    Le battement REEL d'une routine est un ETAT (friction 28, 2026-09-14 : un
    override de cadence a 5 s a vecu 3 jours sans que rien ne le voie) : il
    s'ecrit ici, a CHAQUE passe et ECRASE, jamais dans un journal.

    L'etat garde les PASSES_GARDEES_ETAT derniers horodatages -- assez pour un
    ecart MEDIAN (un redemarrage ou une passe en retard ne doivent pas faire
    croire a une derive), et BORNE pour rester un etat. C'est ce que lit
    `verifier-cadence`, qui le compare a la cadence DECLAREE.

    La fabrique de l'anneau et sa lecture vivent dans le moteur PARTAGE
    `data/commun/battement.py` : la routine ne recopie pas le decoupage qui
    borne la suite (L-029).
    """
    passe = datetime.now().strftime(FORMAT_HORODATAGE)
    donnees = {
        "type": "passe",
        "date": passe,
        "synchronisees": nombre,
        "messages": len(messages or []),
        CLE_ANNEAU_PASSES: ajouter_passe(lire_anneau(CHEMIN_ETAT, CLE_ANNEAU_PASSES),
                                        passe, PASSES_GARDEES_ETAT),
    }
    temporaire = CHEMIN_ETAT.with_name(CHEMIN_ETAT.name + ".tmp")
    with open(str(temporaire), "w", encoding=ENCODAGE_ETAT, newline="\n") as flux:
        flux.write(json.dumps(donnees, ensure_ascii=True, sort_keys=True) + "\n")
    os.replace(str(temporaire), str(CHEMIN_ETAT))
    return CHEMIN_ETAT


def lire_inbox():
    """Retourne la liste des evenements de l'inbox (liste de dicts)."""
    if not CHEMIN_INBOX.exists():
        return []
    try:
        lignes = CHEMIN_INBOX.read_text(encoding=ENCODAGE).splitlines()
    except OSError:
        return []
    evenements = []
    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            evenements.append(json.loads(ligne))
        except json.JSONDecodeError:
            continue
    return evenements


def lire_missions(chemin):
    """Missions citees par un journal jsonl (ensemble), ou vide si absent/illisible."""
    connues = set()
    if not chemin.exists():
        return connues
    try:
        lignes = chemin.read_text(encoding=ENCODAGE).splitlines()
    except OSError:
        return connues
    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            mission = json.loads(ligne).get("mission", "")
        except json.JSONDecodeError:
            continue
        if mission:
            connues.add(mission)
    return connues


def missions_connues(chemin_journal):
    """Missions deja connues : le journal ACTIF **et ses archives**.

    MO-052 -- lecon apprise en reel : ce garde anti-doublon ne regardait que le
    journal actif, or la porte `archiver` sort justement des evenements DU
    journal actif. Resultat : chaque archivage etait ANNULE a la passe suivante,
    la routine reimportant tout ce qu'on venait de deplacer (178 evenements
    reimportes d'un coup, 144 `noter` en 8 secondes). "Deja connu" doit inclure
    ce qu'on a archive, sinon la porte et cette routine se neutralisent.

    Les archives sont trouvees par MOTIF (`suivi-optimus-*.jsonl`) pour ne pas
    recopier ici le nom declare par l'outil suivi-optimus (une seule verite).
    """
    connues = lire_missions(chemin_journal)
    for archive in sorted(chemin_journal.parent.glob(chemin_journal.stem + "-*.jsonl")):
        connues |= lire_missions(archive)
    return connues


def synchroniser():
    """Synchronise les missions terminees de l'inbox vers le suivi-optimus.

    Retourne (nombre_evenements_synchro, messages).
    """
    import sys
    # Insertion MORTE retiree (elle visait `matrice/data/data/commun`, inexistant,
    # et rien ici n'importe le module partage : la suite passe par subprocess).

    evenements_inbox = lire_inbox()
    if not evenements_inbox:
        return 0, ["inbox vide"]

    chemin_suivi = REPERTOIRE_OUTIL_SUIVI.parent.parent / "suivi-optimus.jsonl"
    synchronisees = missions_connues(chemin_suivi)

    nouveaux = []
    for ev in evenements_inbox:
        typ = ev.get("type", "")
        if typ not in TYPES_INTERESSANTS:
            continue
        date_ev = ev.get("date", "")
        if not date_ev:
            continue  # Date manquante : on ne peut pas comparer.
        # Determiner la mission et le theme.
        mission = ""
        theme = ""
        if typ == "fin-mission":
            mission = ev.get("mission", "")
            theme = (ev.get("theme", "") or "").strip()
            # Protection contre la duplication : si la mission est deja synchronisee, on skip.
            if mission in synchronisees:
                continue
            synchronisees.add(mission)
            bilan = ev.get("bilan", "")
            # Theme : on prefere l'inbox, sinon historique pilote (sinon SUIVI-OPTIMUS par defaut).
            if not theme:
                try:
                    from constants import REPERTOIRE_OUTIL_SUIVI as _RO
                    _chemin_hist = _RO.parent.parent / "historiques-missions.jsonl"
                    _derniere = ""
                    if _chemin_hist.exists():
                        for _ligne in _chemin_hist.read_text(encoding=ENCODAGE).splitlines():
                            _j = json.loads(_ligne) if _ligne.strip() else None
                            if _j and _j.get("id") == mission and _j.get("type") == "mission-terminee":
                                _derniere = _j.get("theme", "")
                        if _derniere:
                            theme = _derniere
                except Exception:
                    pass
            nouveaux.append(
                (
                    mission,
                    theme,
                    typ,
                    bilan or ev.get("detail", ""),
                    ev.get("date", ""),
                )
            )
        elif typ == "retour-lot":
            lot = ev.get("lot", [])
            bilan_consolide = ev.get("bilan_consolide", "")
            theme_lot = (ev.get("theme", "") or "").strip()
            # Pour un retour-lot, on cree une entree par mission du lot.
            for m in lot:
                if m in synchronisees:
                    continue
                synchronisees.add(m)
                nouveaux.append(
                    (
                        m,
                        theme_lot or theme or "SUIVI-OPTIMUS",
                        typ,
                        bilan_consolide,
                        ev.get("date", ""),
                    )
                )

    if not nouveaux:
        return 0, ["aucune mission a synchroniser"]

    messages = []
    for mission, theme, typ, detail, date_ev in nouveaux:
        # Ecrire dans suivi-optimus via subprocess (porte unique).
        try:
            termine = subprocess.run(
                [
                    sys.executable,
                    "main.py",
                    "noter",
                    "--mission", mission,
                    "--theme", theme or "SUIVI-OPTIMUS",
                    "--action", "fin",
                    "--detail", detail,
                    # EO-267 / decision du 2026-09-21 : AUCUNE duree declaree -- la
                    # routine ne MESURE pas le temps, et un "0" est le placeholder
                    # qui a fige la colonne Duree de la vue a zero pendant des mois
                    # (une valeur qui ment se lit comme un fait, L-055). La vue
                    # CALCULE la duree des bornes quand elles existent, et affiche
                    # `inconnue` quand elles ne mesurent rien.
                ],
                cwd=str(REPERTOIRE_OUTIL_SUIVI),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )
            if termine.returncode == 0:
                messages.append("synchro : " + mission + " (" + typ + ")")
            else:
                messages.append(
                    "echec synchro : " + mission + " (code " + str(termine.returncode) + ")"
                )
                if termine.stderr:
                    messages.append("  " + termine.stderr.strip())
        except Exception as e:
            messages.append("echec synchro : " + mission + " (" + str(e) + ")")

    return len(nouveaux), messages


def noter_boot_check(messages_boot):
    """Note une entree 'decision' dans le suivi-optimus pour un demarrage du serveur."""
    import sys
    # Meme insertion morte que dans synchroniser() : retiree.

    detail = (
        "Demarrage du serveur matrice (boot-check) : "
        + ("; ".join(messages_boot) if messages_boot else "aucune alerte")
    )
    try:
        termine = subprocess.run(
            [
                sys.executable,
                "main.py",
                "noter",
                "--mission", "",
                "--theme", "SUIVI-OPTIMUS",
                "--action", "decision",
                "--detail", detail,
                # Meme regle : un boot-check n a AUCUNE duree. Le champ est OMIS
                # (une absence honnete vaut mieux qu un zero qui se lit mesure).
            ],
            cwd=str(REPERTOIRE_OUTIL_SUIVI),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        if termine.returncode == 0:
            return 0, ["boot-check note dans suivi-optimus"]
        else:
            return 1, ["echec boot-check note (code " + str(termine.returncode) + ")"]
    except Exception as e:
        return 1, ["echec boot-check note (" + str(e) + ")"]
