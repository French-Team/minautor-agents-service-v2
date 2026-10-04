"""pid_serveur -- le PID du SERVEUR de vie : publie ET repare au meme domicile.

POURQUOI CE DOMICILE (M-076, L-029) : le serveur est l AUTORITE des PID files
(`recreer_pid_files`, server_matrice.py) -- il (re)publie le PID de toute routine
vivante qui n en a plus, et il nettoie les fantomes. Mais ce regime n allait QU AUX
ROUTINES : le PID du SERVEUR lui-meme etait ecrit UNE fois, a l allumage, et JAMAIS
repare. Mesure du 2026-09-28 : `server-matrice.pid` efface a la main fait dire a
`vie etat` (< serveur matrice : ARRET >) ET au maillon serveur du flux (< aucun PID
serveur : la Matrice n est pas demarree >) que la Matrice est MORTE alors que le
serveur VIT. C est exactement la deuxieme verite que le serveur ferme deja pour les
routines : un VIVANT lu comme MORT.

UNE SEULE LOI, UN SEUL DOMICILE : le fichier de PID appartient au processus qu il
nomme ; c est le SERVEUR qui le publie ET qui le repare ; et un PID ETRANGER
VIVANT n est JAMAIS ecrase -- deux serveurs ne doivent pas se croire seuls. La
regle vit ICI pour que le serveur et son cobaye de non-regression LISENT la meme
(jamais deux comportements sous un meme nom).

USAGE : publier(CHEMIN_PID_SERVER, os.getpid()) a chaque tour de supervision.
"""

from pathlib import Path

from vivacite import processus_vivant

ENCODAGE = "utf-8"


def publier(chemin, pid_processus, est_vivant=processus_vivant):
    """(Re)publie le PID du serveur si le fichier ne dit plus la verite.

    Trois cas, UN SEUL ecrit :
      1. le fichier dit DEJA ce PID           -> rien a faire (idempotent) ;
      2. le fichier est ABSENT, ILLISIBLE ou  -> le PID est (re)publie,
         dit un PID MORT (fantome)              c est la reparation ;
      3. le fichier dit un PID ETRANGER VIVANT -> RIEN n est ecrit : le refus
                                                  est NOMME, jamais silencieux.

    `est_vivant` est INJECTABLE : le cobaye eprouve la regle sans lancer ni tuer
    un processus. Retourne (message, a_ecrit) ; un disque qui refuse se DIT et
    laisse la cible intacte.
    """
    chemin = Path(chemin)
    try:
        contenu = chemin.read_text(encoding=ENCODAGE).strip()
    except OSError:
        contenu = ""
    try:
        pid_note = int(contenu) if contenu else None
    except ValueError:
        pid_note = None

    if pid_note == pid_processus:
        return "PID serveur deja publie (" + str(pid_processus) + ")", False

    if pid_note is not None and est_vivant(pid_note):
        return ("ALERTE : le PID publie (" + str(pid_note) + ") designe un processus"
                + " VIVANT -- je n ecrase pas ce fichier (mon PID "
                + str(pid_processus) + " reste non publie)"), False

    motif = "absent" if pid_note is None else "fantome " + str(pid_note)
    try:
        chemin.write_text(str(pid_processus) + "\n", encoding=ENCODAGE)
    except OSError as erreur:
        return "ALERTE : PID serveur non publie (" + motif + ") : " + str(erreur), False
    return "PID serveur republie (" + motif + " -> " + str(pid_processus) + ")", True
