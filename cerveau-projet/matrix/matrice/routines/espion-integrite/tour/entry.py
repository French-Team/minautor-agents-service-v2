"""Categorie tour : orchestre UNE passe de surveillance (ou un diagnostic).

Interface entre main.py et les fonctions simples (tour/fonctions.py).

Deux modes, MEME calcul, une seule difference : l'ecriture.
  - `tour`     : journalise la passe (observations quand le tableau CHANGE, plus
    un evenement `passe` a chaque fois) ;
  - `verifier` : rend le MEME verdict SANS rien ecrire -- c'est le mode des routes
    de diagnostic (cockpit `/sante`) et des suites. Un appel a la demande qui
    ecrit 15 lignes a chaque fois fait grossir un journal en ajout seul sans rien
    apporter a la surveillance : la boucle, elle, journalise ses passes.

MO-081 -- ETAT ET HISTOIRE. La passe journalisait 14 observations (une par BDD)
a CHAQUE tour, meme quand rien n'avait bouge : mesure du 2026-09-14, 504 134
observations pour 36 000 passes, 93 % du journal. Or l'integrite d'une BDD est un
ETAT : elle ne change pas entre deux passes. Le tableau des BDD part donc dans un
ETAT COURT (`espion-etat-bdds.json`, ecrit a chaque passe, ECRASE) ; l'HISTOIRE
ne recoit les observations que si le tableau CHANGE -- et ce changement EST le
fait. La ligne `passe`, elle, reste ecrite a chaque tour : elle est le TEMOIN DE
VIE que lit la non-regression du flux (lecon L-026 : une boucle qui ne finit plus
ses passes doit se voir), et un temoin n'a pas le droit de devenir aveugle.

Retourne 0 si rien a signaler, 1 si au moins un ECART.
"""
from commun import ecrire_etat_bdds, horodater, journaliser, lire_etat_bdds
from constants import BDDS
from etat_histoire import decision_fait as _decision_fait
from etat_histoire import signature_fait as _signature_fait_partage
from tour.fonctions import journaliser_observation, observer_bdd

CHAPITRE_INTEGRITE = 1
CHAPITRE_PRESENCE = 2


def chapitres_produits(bdds):
    """Les chapitres REELLEMENT produits par une passe sur ce registre.

    Un chapitre est annonce si -- et seulement si -- il peut PRODUIRE une ligne :
      - chapitre 1 (integrite) : une BDD faite a verifier (une BDD faite absente
        du disque = ECART) ;
      - chapitre 2 (presence) : une BDD a-construire a observer (INFO).
    Annoncer un chapitre sans production, c'est declarer un canal vide (mesure
    MO-072 : chapitre 2 annonce [1, 2] en dur alors qu'il etait muet depuis le
    2026-09-06, dernier a-construire construit depuis). L'annonce est donc
    CALCULEE du registre : le jour ou une BDD a-construire y est inscrite, le
    chapitre 2 se rallume TOUT SEUL, sans retoucher ce fichier.
    """
    faites = [nom for nom, faite in bdds.items() if faite]
    a_construire = [nom for nom, faite in bdds.items() if not faite]
    chapitres = []
    if faites:
        chapitres.append(CHAPITRE_INTEGRITE)
    if a_construire:
        chapitres.append(CHAPITRE_PRESENCE)
    return chapitres


def constater(bdds):
    """Passe le registre et rend (ecarts, constats). AUCUNE ecriture.

    Un SEUL chemin d'observation pour les deux modes : `verifier` et `tour`
    voient exactement la meme chose. Le chapitre est attache au constat -- c'est
    ce qui permet de le journaliser sans le recalculer, donc de ne pas le
    desynchroniser du constat.
    """
    ecarts = []
    constats = []
    for nom_bdd, faite in bdds.items():
        constat, chapitre = observer_bdd(nom_bdd, faite, CHAPITRE_INTEGRITE, CHAPITRE_PRESENCE)
        constat["chapitre"] = chapitre
        constats.append(constat)
        if constat["etat"] == "ECART":
            ecarts.append(nom_bdd)
    return ecarts, constats


def signature_controle(constats):
    """Signature COMPARABLE du controle : ce que la passe a VU, et rien d'autre.

    Le DETAIL entre dans la signature : une BDD a-construire qui APPARAIT change
    de detail sans changer d'etat, et c'est un fait (la presence se suit). Les
    empreintes sont lues a chaque passe, mais elles sont STABLES tant qu'aucune
    BDD ne bouge : c'est ce qui rend la comparaison utile.
    """
    # Le tri est fait ICI (la signature partagee ne reordonne pas une liste : un
    # dictionnaire reordonne n'est pas un fait, une liste reordonnee en est un).
    # La signature elle-meme vient du moteur PARTAGE (data/commun/etat_histoire.py,
    # MO-082) : quatre implementations de la meme idee divergent (lecon L-029).
    return _signature_fait_partage(
        sorted(
            (
                {
                    "bdd": constat["bdd"],
                    "chapitre": constat.get("chapitre"),
                    "etat": constat["etat"],
                    "detail": constat["detail"],
                }
                for constat in constats
            ),
            key=lambda constat: constat["bdd"],
        )
    )


def fait_notable(constats, signature_ecrite):
    """DECISION PURE : cette passe laisse-t-elle un FAIT a l'historique ?

    Vrai si le TABLEAU DES BDD change (une integrite se casse, un etalon est
    pose, une BDD a-construire apparait ou disparait). Faux = la passe a vu
    exactement la meme chose que la derniere fois : c'est un ETAT, il part dans
    l'etat court, et l'histoire n'a rien a y gagner -- elle n'y gagnerait qu'une
    ligne de plus a lire pour retrouver la seule qui dise quelque chose.

    La fonction est PURE (meme reponse pour memes constats) : elle se teste sans
    disque, et c'est ce qui permet au cobaye de la pieger (lecon L-032).
    """
    return _decision_fait(signature_controle(constats), signature_ecrite)[0]


def ecarts_reveles(ecarts):
    """Rend (code, message) du verdict commun aux deux modes."""
    if ecarts:
        return 1, "ECARTS detectes : " + ", ".join(ecarts)
    return 0, "Passe complete : aucune alerte."


def executer(arguments):
    """Passe de surveillance : FAIT au journal, ETAT a part. Rend le code.

    L'etat est ecrit AVANT la ligne `passe` : si l'ecriture de l'etat echoue, la
    passe se voit (la ligne manque) plutot que de laisser croire a un tableau
    ecrit. La signature enregistree est celle du tableau REELLEMENT journalise :
    c'est elle qui decide de la passe suivante.
    """
    ecarts, constats = constater(BDDS)
    etat_avant = lire_etat_bdds()
    signature_ecrite = etat_avant.get("signature")
    absorbes = int(etat_avant.get("passes_absorbes") or 0)
    changement = fait_notable(constats, signature_ecrite)

    if changement:
        # Un FAIT : le tableau a change. On journalise le tableau COMPLET -- c'est
        # lui qui dit ce qui a change, observation par observation.
        for constat in constats:
            journaliser_observation(constat)
        signature_ecrite = signature_controle(constats)

    # L'ETAT : ecrit a CHAQUE passe, ecrase. Il porte le tableau COMPLET (ce que le
    # journal ne repete plus), le compte des passes absorbees depuis la derniere
    # observation ecrite et la date de la derniere observation -- la redondance
    # supprimee est TRACEE, jamais silencieuse.
    ecrire_etat_bdds(
        {
            "type": "controle",
            "date": horodater(),
            "observations": {
                constat["bdd"]: {
                    "chapitre": constat.get("chapitre"),
                    "etat": constat["etat"],
                    "detail": constat["detail"],
                }
                for constat in constats
            },
            "signature": signature_ecrite,
            "passes_absorbes": 0 if changement else absorbes + 1,
            "derniere_observation": horodater()
            if changement
            else str(etat_avant.get("derniere_observation") or ""),
            "ecarts": ecarts,
        }
    )

    # Le TEMOIN DE VIE : une ligne `passe` a chaque tour, avec le nombre de passes
    # absorbees AVANT ce qu'elle rapporte. Elle n'est pas l'observation repetee :
    # elle dit qu'une passe a EU LIEU et quel verdict elle a rendu.
    journaliser(
        {
            "type": "passe",
            "chapitres": chapitres_produits(BDDS),
            "bdds_surveillees": len(BDDS),
            "ecarts": ecarts,
            "motif": "changement" if changement else "absorbee",
            "passes_absorbes": absorbes,
        }
    )
    code, message = ecarts_reveles(ecarts)
    print(message)
    return code


def verifier(arguments):
    """Diagnostic LECTURE SEULE : meme verdict, ZERO ligne ecrite."""
    ecarts, constats = constater(BDDS)
    code, message = ecarts_reveles(ecarts)
    for constat in constats:
        print(
            "  " + constat["etat"].ljust(5) + " " + constat["bdd"] + " : " + constat["detail"]
        )
    print(message + " (diagnostic sans ecriture : le journal n'a pas bouge)")
    return code
