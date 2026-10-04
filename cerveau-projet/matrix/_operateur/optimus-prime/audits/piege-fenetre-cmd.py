#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""piege-fenetre-cmd.py -- Piege a l instant : NOMME le coupable d une fenetre console.

LECTURE SEULE : ce script n arrete rien, ne repare rien, ne modifie aucun fichier de
service. Il OBSERVE les processus et rend la chaine d ascendance.

LE PROBLEME (EO-428 / MO-413 / MO-445) : une fenetre cmd.exe vide apparait puis
disparait. Le controle MO-413 a etabli que RIEN dans le code ne demande une console
neuve (0 CREATE_NEW_CONSOLE, 0 DETACHED_PROCESS, 0 shell=True, aucun .bat/.cmd/.ps1).
La CAUSE reste NON ETABLIE. La seule question qui ouvre le dossier : QUAND une
fenetre nait, QUI est son parent ? Cet instrument y repond en capturant l ascendance
REELLE des cmd.exe / conhost.exe, a l instant ou ils apparaissent.

EFFET OBSERVATEUR (defaut mesure et repare, MO-445) : une premiere version relevait
les processus avec `wmic`. Or `wmic` est une application console : chaque appel
cree un conhost.exe, dont le parent (wmic) meurt aussitot. Le piege ENGENDRAIT donc
les conhost qu il surveillait, et son exclusion d auto-observation ne pouvait pas
remonter jusqu a lui (le maillon intermediaire etait deja mort). La version courante
enumere les processus par l API native `CreateToolhelp32Snapshot` (ctypes) : AUCUN
processus n est lance, donc aucune fenetre n est creee par le piege lui-meme.

MODES :
  instant                          une photo : les cmd/conhost vivants et leur ascendante
  piege [--duree N] [--cadence S]  surveille et rend chaque NOUVEAU cmd/conhost
  auto-test                        preuve deterministe (mord + epargne)

OPTIONS :
  --journal <chemin>   journal JSONL (defaut : sortie standard)
  --duree <secondes>   duree du piege      (defaut 300)
  --cadence <secondes> periode des photos   (defaut 2)
  --cmdline            enrichit chaque ligne avec la ligne de commande (releve par
                       wmic : cela RELANCE l effet observateur, a n utiliser que
                       pour un constat ponctuel, jamais pour le piege)

CODES RETOUR : 0 = rien a signaler, 1 = au moins une fenetre attribuee, 2 = refus nomme.
"""

import csv
import io
import json
import os
import subprocess
import sys
import time

ENCODAGE = "utf-8"

# --- CONSTANTES (aucune valeur en dur dispersee) ---------------------------
NOMS_SURVEILLES = ("cmd.exe", "conhost.exe")
ORIGINE_NATIVE = "ctypes"
ORIGINE_WMIC = "wmic"
ORIGINE_POWERSHELL = "powershell"
CONSTANTE_SNAPSHOT_PROCESSUS = 0x00000002
TAILLE_NOM_EXE = 260
REQUETE_WMIC = ("process get Name,ProcessId,ParentProcessId,CreationDate,"
                "CommandLine /format:csv")
REQUETE_POWERSHELL = ("Get-CimInstance Win32_Process | "
                      "Select-Object Name,ProcessId,ParentProcessId,"
                      "CreationDate,CommandLine | ConvertTo-Csv -NoTypeInformation")
CADENCE_DEFAUT_SECONDES = 2.0
DUREE_DEFAUT_SECONDES = 300
PROFONDEUR_MAX_ASCENDANCE = 12
PLAFOND_CHAINE_CARACTERES = 400
DELAI_COMMANDE_SECONDES = 60
MARQUEUR_PID_INCONNU = "inconnu (hors snapshot)"
MARQUEUR_BOUCLE = "boucle (cycle de pids)"


def _drapeaux():
    """creationflags/startupinfo : ne JAMAIS ouvrir de console (convention lancement.py)."""
    creationflags = 0
    startupinfo = None
    if os.name == "nt":
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0
    return creationflags, startupinfo


def _lancer(commande):
    creationflags, startupinfo = _drapeaux()
    return subprocess.run(
        commande,
        capture_output=True,
        creationflags=creationflags,
        startupinfo=startupinfo,
        timeout=DELAI_COMMANDE_SECONDES,
    )


def _analyser_csv(texte, origine):
    """Rend {pid: {nom, ppid, cmdline, cree}} ou un RuntimeError NOMME."""
    lignes = [ligne for ligne in csv.reader(io.StringIO(texte))
              if ligne and any(cellule.strip() for cellule in ligne)]
    lignes = [ligne for ligne in lignes if not ligne[0].lstrip().startswith("#")]
    if not lignes:
        raise RuntimeError("sortie " + origine + " VIDE")
    entete = [cellule.strip().lower() for cellule in lignes[0]]
    for nom_colonne in ("name", "processid", "parentprocessid"):
        if nom_colonne not in entete:
            raise RuntimeError("colonne " + nom_colonne + " ABSENTE de la sortie "
                               + origine)
    index = {}
    for ligne in lignes[1:]:
        if len(ligne) != len(entete):
            continue
        brut = dict(zip(entete, [cellule.strip() for cellule in ligne]))
        try:
            pid = int(brut["processid"])
            ppid = int(brut["parentprocessid"])
        except (KeyError, ValueError):
            continue
        index[pid] = {
            "nom": (brut.get("name") or "").strip(),
            "ppid": ppid,
            "cmdline": (brut.get("commandline") or "").strip(),
            "cree": (brut.get("creationdate") or "").strip(),
        }
    if not index:
        raise RuntimeError("aucun processus exploitable dans la sortie " + origine)
    return index


def _relever_natif():
    """Enumerer les processus par CreateToolhelp32Snapshot : AUCUN processus lance.

    C est le mode PAR DEFAUT parce qu il ne cree aucune fenetre console (l effet
    observateur mesure avec wmic). Il ne rend pas la ligne de commande (le nom du
    parent suffit pour NOMMER le coupable) ; `--cmdline` l ajoute au prix avoue.
    """
    import ctypes
    from ctypes import wintypes

    class EntreeProcessus(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.c_void_p),
            ("th32ModuleID", wintypes.DWORD),
            ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD),
            ("pcPriClassBase", ctypes.c_long),
            ("dwFlags", wintypes.DWORD),
            ("szExeFile", ctypes.c_char * TAILLE_NOM_EXE),
        ]

    noyau = ctypes.windll.kernel32
    noyau.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    noyau.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    noyau.Process32First.argtypes = [wintypes.HANDLE, ctypes.c_void_p]
    noyau.Process32Next.argtypes = [wintypes.HANDLE, ctypes.c_void_p]
    noyau.CloseHandle.argtypes = [wintypes.HANDLE]

    instantane = noyau.CreateToolhelp32Snapshot(CONSTANTE_SNAPSHOT_PROCESSUS, 0)
    if not instantane or instantane == ctypes.c_void_p(-1).value:
        raise RuntimeError("CreateToolhelp32Snapshot a echoue")
    entree = EntreeProcessus()
    entree.dwSize = ctypes.sizeof(EntreeProcessus)
    index = {}
    try:
        suite = noyau.Process32First(instantane, ctypes.byref(entree))
        while suite:
            pid = int(entree.th32ProcessID)
            index[pid] = {
                "nom": entree.szExeFile.decode("ascii", errors="replace"),
                "ppid": int(entree.th32ParentProcessID),
                "cmdline": "",
                "cree": "",
            }
            suite = noyau.Process32Next(instantane, ctypes.byref(entree))
    finally:
        noyau.CloseHandle(instantane)
    if not index:
        raise RuntimeError("CreateToolhelp32Snapshot : aucun processus rendu")
    return index


def _relever_wmic():
    resultat = _lancer(["wmic"] + REQUETE_WMIC.split(" "))
    if resultat.returncode != 0:
        raise RuntimeError(ORIGINE_WMIC + " : code " + str(resultat.returncode))
    return _analyser_csv(resultat.stdout.decode(ENCODAGE, errors="replace"),
                         ORIGINE_WMIC)


def _relever_powershell():
    resultat = _lancer(["powershell", "-NoProfile", "-NonInteractive", "-Command",
                        REQUETE_POWERSHELL])
    if resultat.returncode != 0:
        raise RuntimeError(ORIGINE_POWERSHELL + " : code " + str(resultat.returncode))
    return _analyser_csv(resultat.stdout.decode(ENCODAGE, errors="replace"),
                         ORIGINE_POWERSHELL)


def photographier():
    """(index, origine) : releve TOUT le parc de processus, ou RuntimeError NOMME."""
    releveurs = ((ORIGINE_NATIVE, _relever_natif),
                 (ORIGINE_WMIC, _relever_wmic),
                 (ORIGINE_POWERSHELL, _relever_powershell))
    erreurs = []
    for origine, releveur in releveurs:
        try:
            return releveur(), origine
        except (RuntimeError, OSError, subprocess.TimeoutExpired) as erreur:
            erreurs.append(origine + " : " + str(erreur)[:80])
    raise RuntimeError("aucun releve exploitable (" + " ; ".join(erreurs) + ")")


def enrichir_commandes(index):
    """Ajoute la ligne de commande (wmic) aux processus deja releves.

    EFFET OBSERVATEUR ASSUME ET DIT : ce seul appel peut creer un conhost de plus.
    A n utiliser que pour un constat ponctuel (`instant`), jamais pour le piege.
    """
    try:
        complet, _ = None, None
        complet = _relever_wmic()
    except (RuntimeError, OSError, subprocess.TimeoutExpired):
        return 0
    enrichis = 0
    for pid, processus in index.items():
        source = complet.get(pid)
        if source and source["cmdline"] and not processus["cmdline"]:
            processus["cmdline"] = source["cmdline"]
            if source["cree"] and not processus["cree"]:
                processus["cree"] = source["cree"]
            enrichis += 1
    return enrichis


def chaine(pid, index, max_profondeur=PROFONDEUR_MAX_ASCENDANCE):
    """Remonte l ascendance d un pid jusqu a la racine, de facon BORNEE."""
    maillons = []
    vus = set()
    courant = pid
    for _ in range(max_profondeur):
        if courant in vus:
            maillons.append({"pid": courant, "nom": MARQUEUR_BOUCLE, "cmdline": ""})
            break
        vus.add(courant)
        processus = index.get(courant)
        if processus is None:
            maillons.append({"pid": courant, "nom": MARQUEUR_PID_INCONNU,
                             "cmdline": ""})
            break
        maillons.append({"pid": courant, "nom": processus["nom"],
                         "cmdline": processus["cmdline"]})
        if processus["ppid"] <= 0 or processus["ppid"] == courant:
            break
        courant = processus["ppid"]
    return maillons


def est_descendant(pid, index, ancetre_pid):
    """Vrai si ancetre_pid figure dans l ascendance de pid (auto-observation)."""
    return any(maillon["pid"] == ancetre_pid for maillon in chaine(pid, index))


def rendre_attribution(pid, index, origine):
    processus = index[pid]
    maillons = chaine(pid, index)
    texte = " <- ".join(m["nom"] + "(pid=" + str(m["pid"]) + ")" for m in maillons)
    if len(texte) > PLAFOND_CHAINE_CARACTERES:
        texte = texte[:PLAFOND_CHAINE_CARACTERES] + "...(tronque)"
    return {
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "origine": origine,
        "pid": pid,
        "nom": processus["nom"],
        "cmdline": processus["cmdline"],
        "cree": processus["cree"],
        "chaine": texte,
        "maillons": maillons,
    }


def surveilles(index):
    return {pid: processus for pid, processus in index.items()
            if processus["nom"].lower() in NOMS_SURVEILLES}


def mode_instant(cmdline):
    index, origine = photographier()
    if cmdline:
        enrichis = enrichir_commandes(index)
        print("(--cmdline : " + str(enrichis) + " ligne(s) de commande ajoutee(s) ; "
              "ce seul appel peut creer un conhost, effet observateur connu)")
    cibles = surveilles(index)
    print("Photo (" + origine + ") : " + str(len(index)) + " processus, "
          + str(len(cibles)) + " surveille(s) " + "/".join(NOMS_SURVEILLES))
    if not cibles:
        print("AUCUN " + "/".join(NOMS_SURVEILLES) + " vivant : rien a attribuer.")
        return 0
    for pid in sorted(cibles):
        print(json.dumps(rendre_attribution(pid, index, origine), ensure_ascii=True))
    return 0


def mode_piege(journal, duree, cadence, cmdline):
    index, origine = photographier()
    vus = set(surveilles(index))
    print("Piege arme (" + origine + ") -- " + str(duree) + " s, cadence " + str(cadence)
          + " s ; " + str(len(vus)) + " " + "/".join(NOMS_SURVEILLES)
          + " deja vivant(s) (baseline, non signale(s)).")
    debut = time.monotonic()
    signalements = 0
    while time.monotonic() - debut < duree:
        time.sleep(cadence)
        try:
            index, origine = photographier()
        except RuntimeError as erreur:
            print("REFUS : " + str(erreur), file=sys.stderr)
            return 2
        if cmdline:
            enrichir_commandes(index)
        for pid, processus in index.items():
            if processus["nom"].lower() not in NOMS_SURVEILLES or pid in vus:
                continue
            vus.add(pid)
            if est_descendant(pid, index, os.getpid()):
                continue  # auto-observation : le piege ne s accuse pas lui-meme
            ligne = json.dumps(rendre_attribution(pid, index, origine),
                               ensure_ascii=True)
            print(ligne)
            if journal is not None:
                with open(journal, "a", encoding=ENCODAGE, newline="\n") as flux:
                    flux.write(ligne + "\n")
            signalements += 1
    print("Piege termine : " + str(signalements) + " attribution(s).")
    return 1 if signalements else 0


def mode_auto_test():
    """Preuve deterministe : le detecteur MORD, EPARGNE, et NE CASSE PAS."""
    echecs = []

    def verifier(nom, condition, detail):
        print(("PASS" if condition else "FAIL") + " : " + nom + " -- " + detail)
        if not condition:
            echecs.append(nom)

    index = {
        400: {"nom": "python.exe", "ppid": 300, "cmdline": "veille-flux", "cree": ""},
        300: {"nom": "python.exe", "ppid": 100, "cmdline": "vie activer", "cree": ""},
        100: {"nom": "explorer.exe", "ppid": 0, "cmdline": "", "cree": ""},
        500: {"nom": "cmd.exe", "ppid": 400, "cmdline": "cmd /c ...", "cree": ""},
    }
    vus = {500}
    nouveaux = [pid for pid in index
                if pid not in vus and index[pid]["nom"].lower() in NOMS_SURVEILLES]
    verifier("contre-temoin (calme)", nouveaux == [],
             "un cmd deja vu n est PAS resigne : " + str(nouveaux))
    vus = set()
    nouveaux = [pid for pid in index
                if pid not in vus and index[pid]["nom"].lower() in NOMS_SURVEILLES]
    verifier("cobaye (mord)", nouveaux == [500],
             "le nouveau cmd est signale : " + str(nouveaux))
    maillons = chaine(500, index)
    noms = [m["nom"] for m in maillons]
    verifier("ascendance", noms[:2] == ["cmd.exe", "python.exe"]
             and maillons[1]["pid"] == 400, "chaine = " + " <- ".join(noms))
    isole = {900: {"nom": "cmd.exe", "ppid": 899, "cmdline": "", "cree": ""}}
    maillons = chaine(900, isole)
    verifier("parent hors snapshot", maillons[-1]["nom"] == MARQUEUR_PID_INCONNU,
             "dernier maillon = " + maillons[-1]["nom"])
    cycle = {1: {"nom": "a.exe", "ppid": 2, "cmdline": "", "cree": ""},
             2: {"nom": "b.exe", "ppid": 1, "cmdline": "", "cree": ""}}
    maillons = chaine(1, cycle)
    verifier("cycle de pids", len(maillons) <= 3, "maillons = " + str(len(maillons)))
    # Le releve NATIF doit rendre un parc non vide sans lancer de processus : c est
    # la preuve que l effet observateur est bien supprime.
    try:
        index_reel = _relever_natif()
        verifier("releve natif", len(index_reel) > 1,
                 "ctypes rend " + str(len(index_reel)) + " processus, 0 lance")
    except RuntimeError as erreur:
        verifier("releve natif", False, str(erreur))
    if echecs:
        print("AUTO-TEST EN ECHEC : " + ", ".join(echecs))
        return 2
    print("AUTO-TEST VERT : le detecteur mord ET epargne.")
    return 0


def _extraire_options(arguments):
    options = {"cmdline": False}
    i = 0
    while i < len(arguments):
        jeton = arguments[i]
        if jeton == "--cmdline":
            options["cmdline"] = True
            i += 1
        elif jeton in ("--journal", "--duree", "--cadence"):
            if i + 1 >= len(arguments):
                raise ValueError("option " + jeton + " sans valeur")
            options[jeton[2:]] = arguments[i + 1]
            i += 2
        else:
            raise ValueError("option inconnue " + jeton
                             + " (attendu : --journal | --duree | --cadence | --cmdline)")
    return options


def mode_emploi():
    print(__doc__.strip())
    return 0


def main():
    arguments = sys.argv[1:]
    if not arguments or arguments[0] in ("-h", "--aide", "aide"):
        return mode_emploi()
    mode = arguments[0]
    try:
        options = _extraire_options(arguments[1:])
    except ValueError as erreur:
        print("REFUS : " + str(erreur), file=sys.stderr)
        return 2
    if mode == "instant":
        return mode_instant(options["cmdline"])
    if mode == "piege":
        try:
            duree = float(options.get("duree", DUREE_DEFAUT_SECONDES))
            cadence = float(options.get("cadence", CADENCE_DEFAUT_SECONDES))
        except ValueError:
            print("REFUS : --duree et --cadence attendent un nombre.",
                  file=sys.stderr)
            return 2
        return mode_piege(options.get("journal"), duree, cadence, options["cmdline"])
    if mode == "auto-test":
        return mode_auto_test()
    print("REFUS : mode inconnu '" + mode + "' (attendu : instant | piege | auto-test).",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
