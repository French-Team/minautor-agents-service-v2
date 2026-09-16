"""Fonctions simples de la categorie lister : une seule tache chacune."""
import json
from pathlib import Path

from commun import RACINE, lister_dossier


def executer_lister(dossier, filtre, recursif, as_json):
    """Execute le listage. Retourne code 0/1/2."""
    fichiers, dossiers, code, msg = lister_dossier(dossier, filtre, recursif, inclure_invisible=False)
    if code != 0:
        print(msg)
        return code

    total_f = len(fichiers)
    total_d = len(dossiers)
    print("Dossier " + dossier + " : " + str(total_f) + " fichier(s), " + str(total_d) + " dossier(s)" + (" [recursif]" if recursif else "") + (" [filtre " + filtre + "]" if filtre else ""))

    if as_json:
        # Sortie machine
        out = {
            "dossier": dossier,
            "recursif": recursif,
            "filtre": filtre,
            "fichiers": [],
            "dossiers": [],
        }
        for p in fichiers:
            try:
                rel = str(p.relative_to(RACINE)).replace("\\", "/")
            except ValueError:
                rel = str(p).replace("\\", "/")
            try:
                stat = p.stat()
                out["fichiers"].append({"chemin": rel, "mtime": stat.st_mtime, "taille": stat.st_size})
            except OSError:
                out["fichiers"].append({"chemin": rel, "mtime": 0, "taille": 0})
        for p in dossiers:
            try:
                rel = str(p.relative_to(RACINE)).replace("\\", "/")
            except ValueError:
                rel = str(p).replace("\\", "/")
            out["dossiers"].append({"chemin": rel})
        print(json.dumps(out, ensure_ascii=True, indent=2))
        return 0

    # Sortie humaine : tri mtime deja applique
    if fichiers:
        print("--- Fichiers (tri mtime) ---")
        for p in fichiers:
            try:
                rel = str(p.relative_to(RACINE)).replace("\\", "/")
            except ValueError:
                rel = str(p).replace("\\", "/")
            try:
                sz = p.stat().st_size
                print("  " + rel + " (" + str(sz) + " octets)")
            except OSError:
                print("  " + rel)
    if dossiers:
        print("--- Dossiers ---")
        for p in dossiers:
            try:
                rel = str(p.relative_to(RACINE)).replace("\\", "/")
            except ValueError:
                rel = str(p).replace("\\", "/")
            print("  " + rel + "/")
    if total_f == 0 and total_d == 0:
        if filtre:
            print("(aucun resultat pour filtre " + filtre + ")")
        else:
            print("(dossier vide)")

    return 0
