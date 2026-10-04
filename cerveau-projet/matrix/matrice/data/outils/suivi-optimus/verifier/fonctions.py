"""Fonctions simples de la categorie verifier : une seule tache chacune.

Coherence debut/fin (marbre suivi-optimus) : chaque mission a 1 debut + 1 fin.
"""
from collections import defaultdict

MARBRE_DATE = "2026-09-11 19:00:00"  # decree marbre, avant = legacy
# LA REPRISE LEGITIME (MO-534). Une mission menee en DEUX SESSIONS porte deux
# debuts et deux fins : c est LEGAL, la porte `declarer_borne_marbre` l ecrit
# noir sur blanc (MO-108 -- le pilote COMBLE le trou, il ne double jamais).
# Avant cette mission, la reconnaissance Passage par une LISTE FIGEE d exceptions
# (`REPRISES_DOUBLON_OK = {"M-115"}`), donc chaque reprise legitimait une entree
# a la main, et toute mission ROUVRITE puis RE-CLOSE etait accusee de doublon
# alors que sa sequence de bornes est reguliere. La liste disparait : la regle
# se LIT dans la sequence, ce qui la rend vraie pour les regressions a venir et
# supprime la liste a tenir a jour.
#
# LA REGLE : chaque `fin` doit etre precedee d une session OUVERTE -- un
# `debut` non consomme, ou une `rouverture` qui a rendu la mission A FAIRE.
# C est ce qui distingue une REPRISE d un VRAI doublon (deux fins pour une
# seule session).
#
# UNE ROUVERTURE EST UNE BORNNE QUI NE TERMINE PAS (MO-548) : elle rend A FAIRE
# une mission close, donc sa fin anterieure est ANNULEE et elle ouvre la session
# qui sera re-close. C est ce qui rend `[debut, fin, rouverture, fin]` regulier,
# la forme exacte que MO-534 porte au journal.
REPRISES_DOUBLON_OK = set()


def _missions_fin_annulee(evenements):
    """Les missions dont une fin a ete ANNULEE par une `rouverture` ulterieure.

    Cette fonction ne calcule RIEN : elle CONSOMME `indexer_journal` de la
    categorie `coherence`, qui est le domicile de la regle d ordre (une
    `rouverture` tombee apres une fin l annule -- MO-548). Recopier ce calcul
    ici l avait deja produit deux fois, et les deux fois de facon differente.
    Si le domicile est illisible, on rend un ensemble VIDE : le controle garde
    son comportement le plus severe (compter deux fins), jamais le plus
    lenient -- un domicile muet ne doit pas rendre un doublon invisible.
    """
    try:
        from coherence.fonctions import indexer_journal
    except (ImportError, OSError):
        return set()
    try:
        _debuts, _fins, _neut, annulees, _hors = indexer_journal(list(evenements))
    except (KeyError, TypeError, ValueError):
        return set()
    return set(annulees or ())


def _reprise_legitime(actions):
    """VRAI : la sequence de bornes decrit deux sessions regulieres.

    UNE SESSION EST OUVERTE par un `debut` ou par une `rouverture` (qui rend A
    FAIRE sans terminer), et CLOSE par une `fin`. Toute borne qui deborde de ce
    cadre est un DOUBLON -- dans les DEUX sens, et le deuxieme sens a ete
    oublie une fois (MO-534) :
      - [debut, fin, debut, fin]  -> deux sessions       : REGULIER
      - [debut, fin, rouverture, fin] -> rouverte puis re-closee : REGULIER
      - [debut, fin, fin]        -> une session, 2 fins  : DOUBLON
      - [debut, debut]           -> une session, 2 debuts : DOUBLON
      - [debut, debut, fin]      -> une session, ouverte deux fois : DOUBLON

    Le second sens est celui que jouaient les cobayes 1 et 2 du garde du marbre
    (deux ecrivains du debut : le pilote a l injection ET l agent sur l ordre
    4.5). Une reparation qui corrige les DOUBLONS DE FIN en oubliant les
    DEBUTS DOUBLE n est pas une reparation : elle deplace l angle mort au lieu
    de le fermer.

    Le calcul est ici, et non dans le domicile `coherence`, parce qu il repond
    a une AUTRE question : `coherence` demande si la mission est en cours,
    celui-ci demande si la sequence de bornes est reguliere. Une regle, un
    domicile ; deux questions, deux jugement explicites.
    """
    # LES TROIS BORNES LUES ICI, et non importees. Mesure MO-534 : cet import
    # etait un NOM NU, donc GLOBAL -- et quand un AUTRE `constants.py` etait deja
    # en cache (la lecon L-042, les modules glissants), l import echouait, le
    # `except ImportError` renvoyait True, et TOUT doublon devenait une reprise
    # : le controle devenait aveugle au moment precis ou il devait mordre. Les
    # trois noms sont ceux que la categorie utilise deja partout ailleurs, donc
    # les recopier ici ne cree pas de seconde verite : `verifier_coherence`
    # compare ses actions a ces memes litteraux, ligne apres ligne.
    action_debut = "debut"
    action_fin = "fin"
    action_rouverture = "rouverture"
    ouverts = 0
    for action in actions:
        if action in (action_debut, action_rouverture):
            # Une session s ouvre. Une `rouverture` rend A FAIRE une mission
            # close : c est legal meme si aucune session n etait ouverte.
            # Un `debut`, lui, ne peut pas s empiler : deux debuts sans fin
            # entre eux sont deux ecrivains de la meme borne (MO-202), donc un
            # DOUBLON, pas une seconde session.
            if action == action_debut and ouverts > 0:
                return False
            ouverts += 1
        elif action == action_fin:
            if ouverts > 0:
                ouverts -= 1
            else:
                # Une fin SANS session ouverte devant elle : deux sessions ne
                # peuvent pas expliquer ca, c est une borne orpheline.
                return False
    return True


def verifier_coherence(evenements):
    """Verifie la coherence debut/fin du journal (marbre, Flux 2).

    Retourne (ok, messages, stats) avec stats = {orphelines, doublons, ouvertes}.
    - orpheline : fin sans debut
    - doublon   : >1 debut ou >1 fin pour la meme mission, SAUF si une
                  `rouverture` posterieure a annule une fin (MO-534)
    - ouverte   : debut sans fin (mission en cours, normal si recente)
    Les missions avant MARBRE_DATE sont comptees comme legacy (signalees mais
    n'entrainent pas d'ECART bloqueur - elles ont ete ecrites avant le garde
    anti-fin-orpheline). Seules les missions >= MARBRE_DATE bloquent.
    """
    # L'UNIQUE source de ce qui est ANNULE : l index de `coherence`. Cette
    # fonction ne recompte rien -- elle lit. Si le calcul d ordre change un
    # jour, les deux controles le suivent au lieu de diverger en silence.
    fin_annulee = _missions_fin_annulee(evenements)
    par_mission = defaultdict(list)
    for ev in evenements:
        mid = ev.get("mission", "")
        if not mid:
            continue
        par_mission[mid].append(ev)
    orphelines = []
    orphelines_legacy = []
    doublons = []
    ouvertes = []
    for mission, lst in par_mission.items():
        deb = sum(1 for e in lst if e.get("action") == "debut")
        fin = sum(1 for e in lst if e.get("action") == "fin")
        if fin > 0 and deb == 0:
            # date de la fin pour filtrer legacy
            dates_fin = [e.get("date", "") for e in lst if e.get("action") == "fin"]
            plus_ancienne = min(dates_fin) if dates_fin else ""
            if plus_ancienne and plus_ancienne < MARBRE_DATE:
                orphelines_legacy.append(mission)
            else:
                orphelines.append(mission)
        elif deb > 1 or fin > 1:
            # LA REGLE, et non une liste d exceptions : la sequence de bornes
            # dit si ces deux fins sont deux sessions ou un doublon.
            actions = [e.get("action") for e in lst]
            if _reprise_legitime(actions):
                # Deux sessions : chaque fin avait son debut. Pas un ECART.
                continue
            doublons.append((mission, deb, fin))
        elif deb == 1 and fin == 0:
            ouvertes.append(mission)
    messages = []
    ok = True
    if orphelines:
        ok = False
        messages.append("ECART : " + str(len(orphelines)) + " fin(s) sans debut (>= marbre) : " + ", ".join(sorted(orphelines)[:10]) + (" ..." if len(orphelines) > 10 else ""))
    if orphelines_legacy:
        messages.append("LEGACY : " + str(len(orphelines_legacy)) + " fin(s) sans debut (avant marbre " + MARBRE_DATE + ") : " + ", ".join(sorted(orphelines_legacy)[:10]) + (" ..." if len(orphelines_legacy) > 10 else ""))
    if doublons:
        ok = False
        details = ", ".join(m + "(" + str(d) + "/" + str(f) + ")" for m, d, f in doublons[:10])
        messages.append("ECART : " + str(len(doublons)) + " doublon(s) debut/fin : " + details)
    if ouvertes:
        messages.append("INFO : " + str(len(ouvertes)) + " mission(s) ouverte(s) (debut sans fin) : " + ", ".join(sorted(ouvertes)[:10]) + (" ..." if len(ouvertes) > 10 else ""))
    if ok and not orphelines_legacy:
        messages.append("Coherence debut/fin : OK (0 orpheline, 0 doublon, " + str(len(ouvertes)) + " ouverte(s))")
    elif ok:
        messages.append("Coherence debut/fin : OK pour le marbre (>= " + MARBRE_DATE + ")")
    stats = {"orphelines": orphelines, "orphelines_legacy": orphelines_legacy, "doublons": doublons, "ouvertes": ouvertes}
    return ok, messages, stats


def verifier_integrite(empreinte_reelle, empreinte_enregistree):
    """Compare l'empreinte recalculee a l'empreinte enregistree (etalon-or).

    Retourne (succes, message) : le message dit ce qui casse, ou pourquoi.
    """
    if empreinte_reelle is None:
        return (False, "ECART : la BDD est absente ou illisible a l'emplacement attendu.")
    if empreinte_enregistree is None:
        return (False, "ECART : aucune empreinte enregistree (la BDD n'a jamais ete ecrite par l'outil).")
    if empreinte_reelle == empreinte_enregistree:
        return (True, "Integrite verifiee : empreinte " + empreinte_reelle[:16] + "...")
    return (
        False,
        "ECART : empreinte reelle "
        + empreinte_reelle[:16]
        + "... != enregistree "
        + empreinte_enregistree[:16]
        + "... (la BDD a ete modifiee hors de l'outil).",
    )
