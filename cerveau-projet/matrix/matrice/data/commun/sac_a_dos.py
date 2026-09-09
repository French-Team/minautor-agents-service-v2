"""Sac a dos embarque : chaque outil note LUI-MEME ses usages en BDD (M-076).

Porte unique respectee : la note part par l'outil bdd-usages (subprocess),
jamais d'ecriture directe du journal (proto-7). Un echec de notation
n'arrete JAMAIS l'outil (best-effort, comme la veille-flux).
bdd-usages ne se note pas lui-meme : le garde OUTIL_EXCLU interdit la recursion.

Amelioration (audit protections 2026-09-09, decision createur) : quand l'outil
REFUSE (code != 0), le message de protection (lignes REFUS) est note en DETAIL
dans la BDD -- le sac a dos devient le journal des protections declenchees
(raison tracee, pas seulement le code). La sortie console reste inchangee.
"""
import contextlib
import io
import subprocess
import sys
import time
from pathlib import Path

REPERTOIRE_COMMUN = Path(__file__).resolve().parent
REPERTOIRE_DATA = REPERTOIRE_COMMUN.parent
OUTIL_EXCLU = "bdd-usages"
TAGS_SAC_A_DOS = "sac-a-dos"
CHEMIN_BDD_USAGES = REPERTOIRE_DATA / "outils" / OUTIL_EXCLU
TIMEOUT_NOTATION = 30
LONGUEUR_MAX_DETAIL = 300


def extraire_protection(sortie):
    """Retourne le message de protection declenchee (lignes REFUS), tronque.

    Priorite aux lignes portant le marqueur REFUS (protection explicite) ;
    a defaut, la derniere ligne non vide (message d'erreur). Vide si aucune.
    """
    lignes = [ligne.strip() for ligne in sortie.splitlines() if ligne.strip()]
    refus = [ligne for ligne in lignes if "REFUS" in ligne]
    if refus:
        return (" | ".join(refus))[:LONGUEUR_MAX_DETAIL]
    if lignes:
        return lignes[-1][:LONGUEUR_MAX_DETAIL]
    return ""


def noter_usage(arguments, code, duree_ms, detail=""):
    """Note UN usage via bdd-usages (porte unique). Echec jamais bloquant."""
    nom_outil = Path(sys.argv[0]).resolve().parent.name
    if nom_outil == OUTIL_EXCLU:
        return
    commande = arguments[0] if arguments else "-"
    contenu = [
        sys.executable, "main.py", "noter",
        "--outil", nom_outil, "--commande", commande,
        "--code", str(code), "--duree", str(duree_ms),
        "--tags", TAGS_SAC_A_DOS,
    ]
    if detail:
        contenu += ["--detail", detail]
    try:
        termine = subprocess.run(
            contenu,
            cwd=str(CHEMIN_BDD_USAGES),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_NOTATION,
        )
    except (OSError, subprocess.TimeoutExpired) as erreur:
        print("sac-a-dos : notation impossible (" + type(erreur).__name__ + ")", file=sys.stderr)
        return
    if termine.returncode != 0:
        print("sac-a-dos : notation refusee (code " + str(termine.returncode) + ")", file=sys.stderr)


def envelopper(principal, arguments):
    """Execute principal(arguments), chronometre, note l'usage, retourne le code.

    La sortie console est capturee puis reaffichee a l'identique (rien ne
    change pour l'appelant) ; en cas de refus (code != 0), le message de
    protection est note en detail dans la BDD usages.
    """
    debut = time.monotonic()
    tampon = io.StringIO()
    with contextlib.redirect_stdout(tampon):
        code = principal(arguments)
    duree_ms = int((time.monotonic() - debut) * 1000)
    sortie = tampon.getvalue()
    if sortie:
        sys.stdout.write(sortie)
    detail = extraire_protection(sortie) if code != 0 else ""
    noter_usage(arguments, code, duree_ms, detail)
    return code