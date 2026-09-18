"""Fonctions communes de l'outil executer : validation, lancement Python seul.

Chaque fonction fait UNE chose (convention-architecture-outils).
Regle absolue : Python seul, pas de shell.
"""
import subprocess
import sys
import time
from pathlib import Path

from constants import (
    CREATE_NO_WINDOW,
    COMMANDES_INTERDITES,
    ENCODAGE,
    EXTENSIONS_PYTHON,
    RACINE,
    REPERTOIRE_MATRIX,
    TIMEOUT_DEFAUT,
)


def valider_commande(cmd_str):
    """Valide que la commande est executble (Python seul, pas de shell).
    
    Retourne (est_valide, msg_erreur).
    
    Regles :
    - Pas de shell (bash/sh/cmd/powershell)
    - Pas de pipe (|)
    - Pas de redirection (>, >>, 2>/dev/null)
    - Pas de heredoc (<<)
    - Pas de curl/wget
    - Commande doit commencer par python3 ou python
    """
    cmd = cmd_str.strip()
    
    # Vide
    if not cmd:
        return False, "Commande vide"
    
    # Shell interdit
    premier_mot = cmd.split()[0] if cmd.split() else ""
    if premier_mot in COMMANDES_INTERDITES:
        return False, "Shell interdit : " + premier_mot + ". Python seul."
    
    # Pipe interdit
    if "|" in cmd:
        return False, "Pipe interdit. Executez chaque commande separement."
    
    # Redirection interdite
    if ">" in cmd or ">>" in cmd:
        return False, "Redirection interdite. Utilisez les outils ecrire/lire."
    
    # 2>/dev/null interdit (L-003)
    if "2>/dev/null" in cmd or "2> /dev/null" in cmd:
        return False, "2>/dev/null interdit (L-003). Les erreurs doivent etre visibles."
    
    # Heredoc interdit
    if "<<" in cmd:
        return False, "Heredoc interdit. Utilisez --contenu-chemin @file."
    
    # curl/wget interdits
    if premier_mot in ("curl", "wget"):
        return False, "curl/wget interdits. Utilisez les outils dedies."
    
    return True, ""


def parser_commande(cmd_str):
    """Parse la commande en liste d'arguments (sans shell).
    
    Gere :
    - Guillemets simples/doubles (pas de split)
    - Escaping basique
    - @file (anti-heredoc) -> lit le contenu
    
    Retourne (args_list, msg_erreur).
    """
    cmd = cmd_str.strip()
    if not cmd:
        return [], "Commande vide"
    
    # Gestion @file : remplace @chemin par le contenu du fichier
    if cmd.startswith("@"):
        chemin_str = cmd[1:].strip()
        p = Path(chemin_str)
        if not p.is_file():
            # Essai depuis RACINE
            p = RACINE / chemin_str
        if p.is_file():
            try:
                contenu = p.read_text(encoding=ENCODAGE)
                return contenu.strip().splitlines(), ""
            except OSError as e:
                return [], "Erreur lecture @file : " + str(e)
        return [], "Fichier @file introuvable : " + chemin_str
    
    # Parse basique : split sur espaces, respecte guillemets
    args = []
    courant = ""
    dans_guillemet = False
    char_guillemet = None
    
    i = 0
    while i < len(cmd):
        c = cmd[i]
        
        if dans_guillemet:
            if c == char_guillemet and (i == 0 or cmd[i-1] != "\\"):
                dans_guillemet = False
                i += 1
                continue
            courant += c
        else:
            if c in ("'", '"'):
                dans_guillemet = True
                char_guillemet = c
            elif c == " ":
                if courant:
                    args.append(courant)
                    courant = ""
            elif c == "\\" and i + 1 < len(cmd):
                courant += cmd[i+1]
                i += 2
                continue
            else:
                courant += c
        i += 1
    
    if courant:
        args.append(courant)
    
    return args, ""


def executer_python(args, timeout=None, cwd=None):
    """Execute une commande Python sans shell.
    
    Retourne (stdout, stderr, code_retour, duree_ms, msg_erreur).
    
    Garanties :
    - Pas de shell (subprocess.run sans shell=True)
    - CREATE_NO_WINDOW (win) / start_new_session (posix)
    - Timeout configurable
    - Collecte stdout + stderr + code
    - Zero zombie L-012 (pas de Popen + poll)
    """
    if timeout is None:
        timeout = TIMEOUT_DEFAUT
    if cwd is None:
        cwd = str(RACINE)
    
    debut = time.time()
    try:
        result = subprocess.run(
            args,
            capture_output=True,
            timeout=timeout,
            cwd=cwd,
            creationflags=CREATE_NO_WINDOW,
            start_new_session=True,  # anti-zombie L-012
        )
        duree_ms = int((time.time() - debut) * 1000)
        
        stdout = result.stdout.decode(ENCODAGE, errors="replace")
        stderr = result.stderr.decode(ENCODAGE, errors="replace")
        code = result.returncode
        
        return stdout, stderr, code, duree_ms, ""
        
    except subprocess.TimeoutExpired:
        duree_ms = int((time.time() - debut) * 1000)
        return "", "TIMEOUT apres " + str(timeout) + "s", -1, duree_ms, ""
    except FileNotFoundError as e:
        duree_ms = int((time.time() - debut) * 1000)
        return "", "Commande introuvable : " + str(e), -1, duree_ms, ""
    except OSError as e:
        duree_ms = int((time.time() - debut) * 1000)
        return "", "Erreur OS : " + str(e), -1, duree_ms, ""


def valider_fichier_cible(chemin_str):
    """Valide qu'un fichier cible est dans le perimetre matrix/.
    
    Retourne (est_valide, msg_erreur).
    """
    if not chemin_str:
        return True, ""  # pas de fichier cible = OK
    
    p = Path(chemin_str)
    if not p.is_absolute():
        p = RACINE / chemin_str
    p = p.resolve()
    
    # Verifie perimetre matrix/
    for base in (REPERTOIRE_MATRIX,):
        try:
            base_resolved = base.resolve()
            if str(p).startswith(str(base_resolved)):
                return True, ""
        except OSError:
            continue
    
    return False, "REFUS : fichier hors perimetre matrix/ : " + chemin_str


def formater_sortie(stdout, stderr, code, duree_ms, mode_json=False):
    """Formate la sortie d'execution."""
    if mode_json:
        import json
        resultat = {
            "stdout": stdout,
            "stderr": stderr,
            "code": code,
            "duree_ms": duree_ms,
            "succes": code == 0,
        }
        return json.dumps(resultat, ensure_ascii=False, indent=2)
    else:
        lignes = []
        if stdout:
            lignes.append("--- STDOUT ---")
            lignes.append(stdout.rstrip())
        if stderr:
            lignes.append("--- STDERR ---")
            lignes.append(stderr.rstrip())
        lignes.append("--- CODE : " + str(code) + " | DUREE : " + str(duree_ms) + "ms ---")
        return "\n".join(lignes)


def extraire_options(arguments, noms_connus):
    """Voir le CONTRAT du domicile partage (EO-158) : options CONSOMMEES ici."""
    from options import extraire_options as repartir  # domicile partage (EO-158)
    return repartir(arguments, noms_connus, drapeaux=("json", "verbose"))
