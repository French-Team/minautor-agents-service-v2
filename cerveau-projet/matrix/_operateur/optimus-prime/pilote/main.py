"""Point d'entree global du pilote OPTIMUS (Flux 2, MO-001).

Pilote dedie _operateur/optimus-prime/pilote/ (Flux 2, invisible cameleon).
Miroir du pilote cameleon (matrice/pilote/) mais isole : meme interface,
file/historique/entonnoir/intercom dedies, prefix MO-001, vivier partage+prive.
Role : DIRIGER (parser la commande, router vers la categorie).
Aucune logique metier ici (convention-architecture-outils).

Usage :
    python main.py file
    python main.py charger --theme <nom> --type <t> --objectif "..."   (le TYPE
                                       est EXIGE : EO-120, sans lui la mission nait
                                       sans posture et la checklist perd son specifique)
    python main.py charger ... --conduire   (FORGE ET SERT la mission dans le MEME
                                       geste : c est L INTERRUPTION. Une courante
                                       parquee qui attend sa reprise interdit de
                                       forger une mission qui ATTENDRAIT son tour --
                                       le geste mesure le 2026-09-25 (report a
                                       09:54:00, charge a 09:54:01) laissait DEUX
                                       missions ouvertes dans la file et le suivi a
                                       accuse une cloture fausse ; EO-436 / MO-464)
    python main.py transformer --id MO-00X --theme <nom> --objectif "..."
    python main.py retiqueter --id MO-00X [--theme <nom>] [--type <t>]   (corrige le
                                       theme et/ou le TYPE, quel que soit le statut --
                                       trace conservee)
    python main.py reporter --raison "..."   (PARQUE la mission en cours : retour
                                       EN ATTENTE, TRACEE -- raison OBLIGATOIRE ; la zone
                                       jetable reste PLEINE, un report n est pas une
                                       cloture ; EO-182)
    python main.py statut
    python main.py injecter
    python main.py conduire --id MO-00X   (CONDUIT une mission chargee HORS lot :
                                       elle devient COURANTE et injectee, sans
                                       consommer un creneau de la chaine ; EO-185)
    python main.py ordres --id MO-00X [--complet]
                                       (affiche la FICHE TECHNIQUE DE TRAVAIL de
                                       l injection : noyau dit, ajustables resumes,
                                       POIDS contre le PLAFOND GLOBAL ; --complet rend
                                       l injection ENTIERE ; lecture seule, MO-471)
    python main.py prendre             (PREND le round ARME : note la PRISE de la
                                       mission EN COURS au marbre -- et, depuis MO-396,
                                       REMET AUSSI LES ORDRES du round a la console
                                       (l injection imprimee, comme la cloture),
                                       mission EN COURS au marbre -- c est le GESTE
                                       DE RECEPTION de la BOUCLE (ORDRE 4.7) :
                                       apres un fin la chaine a deja servi, donc
                                       injecter REFUSE ; prendre ne prepare rien,
                                       il DECLARE ; EO-360)
    python main.py fin --bilan "..."   (la mission suivante reste en attente)
                                       --bilan-fichier <chemin> lit le MEME recit
                                       dans un fichier (EO-132) : un argument
                                       traverse le shell, ou un accent grave
                                       EXECUTE du shell et troue la trace
    python main.py file consommer      (echelon 4 : tete du brin -> file du pilote)
    python main.py file verser         (echelon 4 BIS : le BRIN ENTIER -> UN lot, une
                                       seule fois -- numerotation k/n et retour
                                       consolide ; [--lot <nom>] ; EO-148)
    python main.py lot etat              (AFFICHE le lot ARME : rang k/n, item
                                       d'origine, type, urgence et statut de chaque
                                       maillon, lus dans sa source ; code 1 si un
                                       maillon n'a plus sa memoire de naissance ;
                                       MO-380)
    python main.py lot avancer --vers MO-XXX
                                       (PORTE DE SAUT : la mission visee passe
                                       EN TETE du lot et sera servie au prochain
                                       round -- pour une chaine dont les maillons
                                       sont entrelaces dans un lot arme ; EO-445)
    python main.py lot retirer --ids MO-001,MO-002 [--motif ...]
                                       (RETIRE des missions d un lot ARME : le lot
                                       garde ses autres ids et le k/n est recompose ;
                                       les retirees restent dans la file HORS lot,
                                       sous le statut retiree + date + motif ; refus
                                       NOMMES si l id est hors lot, s il est la
                                       mission en cours, s il est termine ou deja
                                       retire ; EO-265)
    python main.py enregistrer --id MO-XXX --theme <nom> [--type <t>] --objectif "..."
                                       --bilan "..."   (le TYPE est ACCEPTE EN OPTION --
                                       jamais exige : une porte de reparation ne refuse pas
                                       de reparer ; sans lui, la porte le DIT)
                                       (mission DEJA TERMINEE menee hors file :
                                       ecrit la file ET le journal, debut + fin)
    python main.py regulariser --id MO-XXX --motif "..."   (REGULARISE une mission
                                       de la file dont le JOURNAL porte DEJA la fin --
                                       MO-461 : `enregistrer` refuse un id deja present
                                       et `fin` ne close que la mission EN COURS, donc
                                       rien ne pouvait fermer la file. La fin doit DEJA
                                       vivre au journal : cette porte la CONSTATE, elle
                                       ne l'invente pas -- une mission terminee dans la
                                       file SANS fin au journal reste ACCUSEE par le
                                       controle de coherence. Motif OBLIGATOIRE ; la
                                       borne de fin n'est jamais doublee)
    python main.py rouvrir --id MO-XXX --motif "..."   (ROUVRE une mission CLOSE
                                       dont le bilan ne vaut pas pour elle -- MO-548 :
                                       `fin` clos la mission EN COURS et plus aucune
                                       porte ne rendait la main. Le bilan fautif est
                                       RETIRE et CONSERVE (jamais efface) ; le motif
                                       est OBLIGATOIRE et doit nommer ce qu'il retire :
                                       la porte imprime les faits AVANT d'ecrire)
    python main.py checklist --id MO-XXX [--reconstruire] (checklist selon le type ;
                                       --reconstruire l'enregistre si elle manque)
    python main.py mission --action <debut|pendant|fin> [--id ID] [--theme THEME] [--bilan BILAN]
    python main.py passerelle lire
                                       (LIT le canal du user (user-demandes/) et DIT tout,
                                       sans rien ecrire ; `extraire` depose un item par la
                                       porte de l entonnoir, archive les mots EXACTS du user
                                       au journal du canal, puis retire la demande du canal
                                       -- DRY par defaut, --appliquer pour ecrire)
    python main.py profil [--guider|--remplir]
"""
import sys

from checklist.entry import executer as checklist_executer
from file.entry import executer as file_executer
from injection.entry import executer as injection_executer
from fin.entry import executer as fin_executer
from filtrer.entry import executer as filtrer_executer
from profil.entry import executer as profil_executer

from regulariser.entry import executer as regulariser_executer  # noqa: E402
from passerelle.entry import executer as passerelle_executer  # noqa: E402
from reporter.entry import executer as reporter_executer  # noqa: E402
from rouvrir.entry import executer as rouvrir_executer  # noqa: E402

COMMANDES = {
    "file": file_executer,
    "charger": file_executer,
    "lot": file_executer,
    "transformer": file_executer,
    "retiqueter": file_executer,
    "enregistrer": file_executer,
    "regulariser": regulariser_executer,
    "reporter": reporter_executer,
    "rouvrir": rouvrir_executer,
    "statut": injection_executer,
    "injecter": injection_executer,
    "enchainer": injection_executer,
    "conduire": injection_executer,
    "ordres": injection_executer,
    "prendre": injection_executer,
    "mission": injection_executer,
    "fin": fin_executer,
    "checklist": checklist_executer,
    "filtrer": filtrer_executer,
    "profil": profil_executer,
    "passerelle": passerelle_executer,
}


def principal(arguments):
    if not arguments or arguments[0] not in COMMANDES:
        print(__doc__)
        return 2
    # Le verbe est transmis aux categories qui en gerent plusieurs (file/charger).
    return COMMANDES[arguments[0]](arguments)


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
