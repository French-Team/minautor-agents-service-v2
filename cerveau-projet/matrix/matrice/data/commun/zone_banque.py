"""zone_banque -- le DOMICILE de la BANQUE DE RESSOURCES (v1/v2) (MO-497).

POURQUOI CE FICHIER EXISTE. Le garde ASCII (`garde-ascii.py`) rendu sur la RACINE du
workspace accusait 72 fichiers non-ASCII -- mesure du 2026-09-29 : 70 dans
`cerveau-projet/` (agents, freelance, exemples, docs-dev), 1 dans `outils-llm/`, 1 a la
racine (`AGENTS-activite-recente-v2.md`). AUCUN de ces fichiers n est de la v3, et
AUCUN n'est corrigeable : les corriger reviendrait a MUTER le cerveau v1/v2, ce qu'
ORDRE 3.4 de la loi du round interdit ("le cerveau v1/v2 est une BANK DE RESSOURCES :
lecture seule, jamais modifie"). Un garde qui accuse 72 fois un etat LEGAL est un
garde qu on apprend a ignorer -- c est le rouge que le createur a fait inverser
(MO-487, R-008 : tout controle dont l etat normal est rouge doit etre inverse).

CE QUE CE FICHIER DECLARE, ET SUR QUELLE MESURE. La zone est designee par son
PREDICAT, pas par une liste de fichiers : un chemin est dans la banque s il est HORS du
perimetre d'ecriture de la v3, et qu'il n'est ni un artefact externe DECLARE, ni une
zone jetable DECLAREE. Le perimetre est CONSOMME chez `cible.est_dans_perimetre` --
le meme domicile que la porte ECRIRE, la BDD et les cinq autres consommateurs (M-076) :
une liste de repertoires recopiee ici divergerait au premier ajout de la porte.

LES TROIS ZONES QUI ONT LEUR PROPRE DOMICILE NE SONT PAS DE LA BANQUE. Elles sont
citees et renvoyees telles quelles, pour que la banque n'absorbe jamais une zone dont
le motif est plus precis :
  - `docs/`           -- zone des SOURCES du createur (zone_sources, MO-377) ;
  - `user-demandes/`  -- passerelle USER, ecrite en clair (passerelle_user, MO-492) ;
  - `.kilo` et ses worktrees -- artefacts EXTERNES du harnais (artefacts_externes,
    EO-408/MO-487) ;
  - `tmp-*`           -- zones JETABLES, declarees et purgees a chaque cloture
    (zone_tmp, PREFIXE_ZONE -- le prefixe est CONSOMME, jamais recopie).

CE QUE LA BANQUE NE FAIT PAS, ET DIT. Elle n'exempte RIEN de l'ASCII a l'interieur du
perimetre : un fichier non-ASCII de la Matrice reste ACCUSE par le garde, et c'est le
seul test qui compte pour la v3. Inversement, un fichier non-ASCII ecrit HORS perimetre
n'est plus accuse PAR CE GARDE -- mais il reste accuse par `garde-perimetre-write`, qui
est le garde de la FRONTIERE : les deux gardes se partagent la frontiere, ils ne se
remplacent pas. C'est dit ici parce qu'une exemption sans garde qui la mord devient un
angle mort (L-104).
"""
import sys
from pathlib import Path

# Les domiciles sont lus a leur chemin (jamais recopies, M-076). Le sys.path est pose
# par l appelant comme par les autres consommateurs de data/commun ; le bloc ci-dessous
# ne sert que si le module est importe isolement (auto-test, mesure en ligne).
_DOSSIER_COMMUN = Path(__file__).resolve().parent
if str(_DOSSIER_COMMUN) not in sys.path:
    sys.path.insert(0, str(_DOSSIER_COMMUN))

from cible import est_dans_perimetre          # noqa: E402
from racine import detecter_racine            # noqa: E402
from zone_tmp import PREFIXE_ZONE             # noqa: E402
from artefacts_externes import artefact_de    # noqa: E402

NOM_ZONE_BANQUE = "banque-de-ressources"
MOTIF_ZONE_BANQUE = (
    "le cerveau v1/v2 et ses outils : BANK DE RESSOURCES, LECTURE SEULE -- la v3 "
    "n'y ecrit JAMAIS (ORDRE 3.1/3.4 de la loi du round) ; corriger un accent y "
    "serait MUTER le cerveau v1/v2, interdit. Hors perimetre d'ecriture de la v3 : "
    "garde-perimetre-write reste le garde de la FRONTIERE et accuse qui y ecrit"
)


def est_zone_jetable(chemin):
    """True si <chemin> est dans une zone JETABLE (prefixe DECLARE par zone_tmp)."""
    return any(part.startswith(PREFIXE_ZONE) for part in Path(chemin).parts)


def est_zone_banque(chemin):
    """True si <chemin> est dans la banque de ressources v1/v2 (HORS perimetre).

    Le predicat est le CONTRAIRE du perimetre consomme chez `cible` : un fichier que
    la v3 a le droit d ecrire n est JAMAIS dans la banque, quelle que soit sa forme --
    c'est ce qui garantit que l'exemption ne peut pas deborder sur la Matrice.
    """
    resolu = Path(chemin)
    try:
        resolu = resolu.resolve()
    except (OSError, RuntimeError):
        return False
    # TOUT CE QUI TOUCHE LA RACINE EST PROTEGE, ET LE DEFAUT EST L ACCUSATION.
    # `racine.detecter_racine` ne rend PAS None hors workspace : il LEVE
    # (RuntimeError, "AGENTS.md absent en remontant"). Mesure du jour : suppose non,
    # cet appel non protege faisait tomber le garde en FIN DE COURSE sur tout fichier
    # pose hors du workspace -- et le contre-temoin du maillon 67 s en apercut : son
    # fichier non-ASCII hors zone devenait muet (le garde rendait 1 par l exception,
    # sans jamais nommer la violation). Un garde qui rend le bon code pour la MAUVAISE
    # raison est plus dangereux qu un garde muet : il semble travailler.
    try:
        if est_dans_perimetre(resolu):
            return False
        racine = detecter_racine(resolu)
    except (OSError, RuntimeError, ValueError):
        return False                      # racine INDETECTABLE : on ACCUSE
    if racine is None:
        # HORS WORKSPACE : ce n'est PAS la banque, il n'y a pas de banque la-bas. Le
        # garde ACCUSE alors (fail-closed, MO-075). Mesure du jour : sans ce test, la
        # banque absorbait des chemins qui ne sont dans AUCUN workspace -- et le
        # contre-temoin du maillon 67 (un non-ASCII pose dans un dossier temporaire
        # du systeme, hors workspace) devenait muet. Une exemption qui s etend hors du
        # lieu ou elle est declaree cesse d etre une exemption : elle devient un
        # angle mort.
        return False
    if artefact_de(resolu, racine) is not None:
        return False                      # artefact EXTERNE declare : son propre motif
    if est_zone_jetable(resolu):
        return False                      # zone JETABLE declaree : la sienne
    return True
