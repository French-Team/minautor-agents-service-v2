# -*- coding: ascii -*-
"""fonctions/files.py - UNE tache : les files d'attente (protocole 13 v2)."""

import json
from datetime import datetime, timezone
from pathlib import Path

from historique import historiser

FILES_DIR = Path(__file__).parent.parent / "files"


def _chemin_file(nom):
    return FILES_DIR / f"{nom}.jsonl"


def cmd_mettre_en_attente(args):
    """Protocole 13 v2 : placer une mission en file selon le declencheur.
    --niveau attente/attention/urgent determine file et statut."""
    niveaux = {
        "attente":  ("file-attente", "EN_ATTENTE", "ATTENTE"),
        "attention": ("file-asap",   "SUIVANTE",   "AT-1"),
        "urgent":   ("file-attente", "PRIORITAIRE", "UR-1"),
    }
    niveau = getattr(args, "niveau", None) or (
        "attente" if args.file == "file-attente" else "attention")
    file, statut, type_declencheur = niveaux[niveau]
    entree = {
        "type": type_declencheur,
        "mission": args.mission,
        "agent": args.agent,
        "contexte_avant": args.contexte,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "statut": statut,
    }
    with open(_chemin_file(file), "a", encoding="utf-8") as f:
        f.write(json.dumps(entree, ensure_ascii=False) + "\n")
    # v0.6.2 (URGENT) : l'intervention de JARVIS doit etre TRACEE
    historiser("jarvis", f"Mise en attente [{niveau}] ({file}): "
               f"{args.mission[:60]}",
               "R", session=getattr(args, "session", ""))
    print(f"[JARVIS] Mission placee en {file} (statut: {statut}, "
          f"declencheur: [{niveau}]).")
    print(f"  Mission: {args.mission}")
    if args.contexte:
        print(f"  Contexte de reprise: {args.contexte}")


def cmd_stop_dev(args):
    """[stop] DEFCON 5 : arret complet du dev. Gele TOUTES les missions
    en files et enregistre la raison dans files/defcon.jsonl."""
    raison = args.raison
    gelees = 0
    for nom in ("file-attente", "file-asap"):
        chemin = _chemin_file(nom)
        if not chemin.exists():
            continue
        lignes = [l for l in chemin.read_text(encoding="utf-8").splitlines()
                  if l.strip()]
        modifie = False
        for i, l in enumerate(lignes):
            try:
                e = json.loads(l)
            except ValueError:
                continue
            if e.get("statut") in ("EN_ATTENTE", "PREPAREE", "SUIVANTE",
                                   "PRIORITAIRE"):
                e["statut"] = "DEFCON5"
                lignes[i] = json.dumps(e, ensure_ascii=False)
                modifie = True
                gelees += 1
        if modifie:
            chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    defcon = {
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S"),
        "niveau": 5,
        "raison": raison,
        "missions_gelees": gelees,
        "declare_par": "utilisateur via stark",
    }
    (FILES_DIR / "defcon.jsonl").parent.mkdir(exist_ok=True)
    with open(FILES_DIR / "defcon.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(defcon, ensure_ascii=False) + "\n")
    historiser("jarvis", f"[STOP] DEFCON 5 - arret du dev: {raison[:60]}",
               "R", session=getattr(args, "session", ""))
    print(f"[JARVIS] *** [STOP] DEFCON 5 - ARRET COMPLET DU DEV ***")
    print(f"  Raison: {raison}")
    print(f"  Missions gelees: {gelees}")
    print(f"  Toute reprise exige une decision explicite de l'utilisateur.")


def cmd_file(args):
    """Lister les deux files d'attente."""
    for nom in ("file-attente", "file-asap"):
        chemin = _chemin_file(nom)
        entrees = []
        if chemin.exists():
            for l in chemin.read_text(encoding="utf-8").splitlines():
                if not l.strip():
                    continue
                try:
                    e = json.loads(l)
                except ValueError:
                    continue
                if e.get("statut") not in (None, "VIDE"):
                    entrees.append(e)
        print(f"[{nom}] {len(entrees)} entree(s)")
        for e in entrees:
            print(f"  [{e.get('statut')}] {e.get('mission', '')[:70]}"
                  f" ({e.get('date', '')})")


def cmd_reprendre(args):
    """Protocole 13 v2 : reprendre la mission prioritaire.
    Ordre : PRIORITAIRE > SUIVANTE > EN_ATTENTE/PREPAREE."""
    ordre = ["PRIORITAIRE", "SUIVANTE", "EN_ATTENTE", "PREPAREE"]
    fichiers = [("file-attente", _chemin_file("file-attente")),
                ("file-asap", _chemin_file("file-asap"))]
    if getattr(args, "file", None) and args.file != "file-attente":
        fichiers = [f for f in fichiers if f[0] == args.file]
    candidates = []
    for nom, chemin in fichiers:
        if not chemin.exists():
            continue
        lignes = [l for l in chemin.read_text(encoding="utf-8").splitlines()
                  if l.strip()]
        for i in range(len(lignes) - 1, -1, -1):
            try:
                e = json.loads(lignes[i])
            except ValueError:
                continue
            statut = e.get("statut")
            if statut in ordre:
                candidates.append((ordre.index(statut), len(candidates), nom,
                                   chemin, lignes, i, e))
    if not candidates:
        print("[JARVIS] Aucune mission en attente.")
        return
    _, _, nom, chemin, lignes, i, e = min(candidates,
                                          key=lambda c: (c[0], -c[1]))
    e["statut"] = "REPRISE"
    e["date_reprise"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S")
    lignes[i] = json.dumps(e, ensure_ascii=False)
    chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"[JARVIS] Mission reprise depuis {nom} :")
    print(f"  Mission: {e.get('mission')}")
    if e.get("contexte_avant"):
        print(f"  Contexte avant mise en attente: {e['contexte_avant']}")
    historiser("jarvis",
               f"Reprise de mission depuis {nom}: "
               f"{e.get('mission', '')[:50]}",
               "R", session=getattr(args, "session", ""))
