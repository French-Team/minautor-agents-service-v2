"""Entree du verbe filtrer : le pilote detecte [mot] et route automatiquement.

Le pilote est un FILTRE ACTIF entre la Matrice et les agents.
Il detecte les demandes a crochets, les route vers la bonne porte,
et gere les taches routinieres que l'agent n'a pas besoin de faire.
"""
import re
import subprocess
import sys
import os
from pathlib import Path

# La racine de CE repertoire se DETECTE par le marqueur partage (L-013 / MO-088) :
# aucune chaine de niveaux comptee a la main -- le garde `chemins` l accuse, a raison.
# `commun.py` est le marqueur du pilote : `filtrer/` n en a pas (mesure 2026-09-18).
BORNES_REMONTEE = 30
MARQUEUR_PILOTE = Path("commun.py")


def trouver_repertoire_marqueur(depart, marqueur):
    """Remonte jusqu au dossier qui PORTE le marqueur ; l echec se DIT."""
    courant = Path(depart).resolve()
    for _ in range(BORNES_REMONTEE):
        if (courant / marqueur).is_file():
            return courant
        if courant.parent == courant:
            break
        courant = courant.parent
    raise RuntimeError("Marqueur " + str(marqueur) + " introuvable en remontant depuis "
                       + str(depart) + " : le pilote n a pas ete trouve.")


REPERTOIRE_PILOTE = trouver_repertoire_marqueur(Path(__file__).resolve().parent, MARQUEUR_PILOTE)
sys.path.insert(0, str(REPERTOIRE_PILOTE))

from commun import charger_file, extraire_options, horodater, mission_en_cours, noter_journal
# La liste FERMEE des types vit dans l ENTONNOIR (un seul domicile) : ce filtre
# la CONSOMME pour valider ce qu il transmet, il ne la recopie pas (L-029).
from entonnoir.listes import TYPES

# Le MOTEUR du cadrage (2026-09-21) : le crochet [???] n'imprime plus une route a
# jouer plus tard -- il JOUE le parcours de bout en bout. Le moteur vit a cote
# (filtrer/cadrage.py) et il CONSOMME les regles du theme CADRAGE (M-076).
from filtrer import cadrage

NOMS_OPTIONS = ("message", "theme", "source", "objectif", "urgence", "simuler")
# --objectif : la demande DEVELOPPEE (le cadrage la porte a chaque maillon) ;
# --urgence : la priorite declaree de la chaine (defaut normale, regle du theme) ;
# --simuler oui : JOUE le cadrage sans rien verser (la preuve d un process qui
#   depose six items ne peut pas se payer en items reels a chaque essai).

# --- DEPOT AUTOMATIQUE (MO-175, decision createur 2026-09-18) ----------------
# Avant, `filtrer` IMPRIMAIT la route et rendait 0 : le depot restait un geste
# MANUEL (mesure MO-174). Le pilote JOUE desormais la porte qu il vient de router.
PORTE_DEPOT = ("entonnoir", "deposer")
CHEMIN_DEPOT = REPERTOIRE_PILOTE / "entonnoir" / "main.py"
REFUS_THEME = ("REFUS : depot NON joue -- --theme requis (un depot automatique"
               " ne devine pas le theme).")
SOURCE_DEFAUT = "createur"


def jouer_depot(theme, objectif, source, type_declare=""):
    """JOUE la porte de depot et rend (code, sortie).

    Un theme ABSENT n est PAS devine : le refus se DIT (jamais un repli muet).
    Le TYPE DECLARE du crochet (`[outil]` -> `reparation`) est TRANSMIS a la
    porte : sans cela il etait annonce puis PERDU (`proposer_type` retombait
    sur `dev` faute de mot-cle) et le crochet ne routait rien (mesure MO-174).
    """
    if not theme:
        return 2, REFUS_THEME
    commande = [sys.executable, CHEMIN_DEPOT, "deposer", "--theme", theme,
                "--objectif", objectif, "--source", source]
    if type_declare:
        # Un type declare HORS de la liste fermee ne se transmet JAMAIS :
        # la porte le refuserait et le depot echouerait pour un mot mal
        # orthographie dans un crochet -- l echec se DIT ici, avant la porte.
        if type_declare not in TYPES:
            return 2, ("REFUS : le crochet declare un type INCONNU ("
                       + type_declare + ") -- types fermes : " + ", ".join(TYPES))
        commande += ["--type", type_declare]
    processus = subprocess.run(commande, capture_output=True, text=True)
    sortie = ((processus.stdout or "") + (processus.stderr or "")).strip()
    return processus.returncode, sortie

# Liste fermee des mots-crochet reconnus (miroir convention-crochets.md)
CROCHETS = {
    "mission": {"porte": "entonnoir", "action": "deposer", "type": ""},
  # aucun type declare : le CLASSEMENT decide (voir A3, R5)
    "audit": {"porte": "entonnoir", "action": "deposer", "type": "audit"},
    "revision": {"porte": "entonnoir", "action": "deposer", "type": "revision"},
    "question": {"porte": "pilote", "action": "lot", "type": "question"},
    "alerte": {"porte": "machine-defcon", "action": "monter", "type": "alerte"},
    "pause": {"porte": "pause-session", "action": "pause", "type": "pause"},
    "bilan": {"porte": "bilan-periode", "action": "bilan", "type": "bilan"},
    "preparation": {"porte": "preparation", "action": "ouvrir", "type": "preparation"},
    # [outil] (R5, audit MO-174) : un OUTIL fautif trouve EN TRAVAILLANT.
    # Le type DECLARE est `reparation` : la demande part en reparation, jamais
    # en simple constat. Route complete : protocoles/proto-10-route-outil-defaillant.md.
    "outil": {"porte": "entonnoir", "action": "deposer", "type": "reparation"},
    # [corriger] (demande createur 2026-09-20, MO-303) : une CORRECTION demandee
    # explicitement. Le type DECLARE est `reparation` : comme [outil], la demande se
    # classe A LA NAISSANCE (file, categorie et role poses d'un coup) au lieu de ne
    # declencher RIEN (mesure : "ERREUR : [corriger] non reconnu").
    "corriger": {"porte": "entonnoir", "action": "deposer", "type": "reparation"},
    # [super-combos] NU (demande createur 2026-09-20, MO-303) : le mot nu LISTE les
    # super-combos disponibles -- la brique reelle est `lancer-super-combos` (--lister).
    # La forme d'ACTION reste `[super-combos: #N]` (crochet de TRAVAIL, MOTS-CLES.md).
    "super-combos": {"porte": "lancer-super-combos", "action": "lister", "type": ""},
    # [purification] REPARE (R5) : la convention le declarait, le code l ignorait
    # -- la liste fermee et sa convention avaient diverge SANS que rien ne le dise.
    # Le maillon 28 surveille desormais ce miroir.
    "purification": {"porte": "purification", "action": "ouvrir",
                     "type": "purification"},
    # [???] et son ALIAS [preparer] (MO-317, demande createur 2026-09-20) : le SEUL
    # crochet qui n est PAS un mot francais -- il dit que la demande n est pas encore
    # formulee. Il ouvre le PARCOURS DEDIE ou optimus CONSTITUE LA CHAINE de missions
    # (audit, nemesis, ...) avant de resoudre quoi que ce soit ; l ensemble devient UNE
    # mission contenant plusieurs missions a enchainer. Priorite : file NORMALE, sauf
    # urgence. Comme [preparation] et [purification], c est un THEME, pas une porte :
    # la route est IMPRIMEE (et le routeur le DIT) -- l agent ouvre le parcours ensuite.
    "???": {"porte": "cadrage", "action": "ouvrir", "type": "cadrage"},
    "preparer": {"porte": "cadrage", "action": "ouvrir", "type": "cadrage"},
    # [si] (demande createur du 2026-09-21) : INTERVENTION SUR LA MISSION EN COURS.
    # Ce crochet n ouvre AUCUN parcours et ne depose RIEN : il agit sur le round en
    # train. Sa porte le DIT (`PORTE_MISSION_EN_COURS`) pour que le routeur ne
    # l imprime pas comme une route a jouer plus tard : il imprime la MINI-REFLEXION
    # a tenir, et il TRACE l intervention au journal de la mission COURANTE
    # (choix du createur : une ligne, pas un item au vrac).
    "si": {"porte": "mission-en-cours", "action": "remise-en-question", "type": ""},
}

# --- LA 4e FAMILLE : LES INTERVENTIONS SUR LA MISSION EN COURS ---------------
# Le createur : "un type de mot entre crochets qui va permettre d interferer sur la
# mission EN COURS seulement -- quand je te suis dans la conversation, je vois des
# incoherences ; ce type de mot doit declencher des mini-reflexions en rapport avec
# la mission".
#
# POURQUOI UNE FAMILLE A PART (et non un crochet de plus dans la liste des
# demandes) : un crochet de DEMANDE ouvre un traitement officiel -- il entre dans
# une file, il cree une mission. Une INTERVENTION ne cree rien : elle porte sur le
# round qui tourne, et elle est PERIMEE des que la mission est close. Les confondre
# ferait naitre une mission pour chaque remarque du createur -- exactement ce qu il
# ne demande pas.
PORTE_MISSION_EN_COURS = "mission-en-cours"
CROCHETS_MISSION = (
    "si",
)
# La MINI-REFLEXION de chaque mot : elle vit ICI, en UN exemplaire, et c est elle
# qui est IMPRIMEE au createur ET PORTEE au journal. Un texte recopie ailleurs
# (convention, lexique) est un resume, jamais la source.
MINI_REFLEXIONS = {
    "si": ("REMISE EN QUESTION : ce que le createur vient de decouvrir contredit-il"
           " ce que je viens de faire dans CETTE mission ? Reprendre l hypothese, la"
           " MESURER (jamais l admettre sur parole ni la refuser), puis optimiser les"
           " corrections EN COURS. Rien n est depose : l intervention vit et meurt"
           " avec la mission."),
}
# L ACTION portee au journal : le vocabulaire est libre (mesure du 2026-09-21 :
# debut, fin, decouverte, purge, report, porte, decision, depot), et une
# intervention ne se confond avec aucune des huit.
ACTION_INTERVENTION = "intervention"

# Detection : [mot] au debut de la ligne.
# Le `?` est admis pour UN crochet declare : `[???]` (MO-317, demande createur) --
# le seul qui n est PAS un mot francais, et qui dit que la demande n est pas encore
# formulee. SANS cette classe, `[???]` etait lu comme un message NORMAL (code 1) :
# un crochet employe qui ne declenche RIEN et ne le dit pas (L-055).
REGEX_CROCHET = re.compile(r"^\[([a-zA-Z0-9_?-]+)\]\s*(.*)", re.DOTALL)


def detecter_crochet(message):
    """Detecte un mot-crochet au debut du message.
    Retourne (mot, reste, config) ou (None, message, None) si aucun crochet.
    """
    message = message.strip()
    match = REGEX_CROCHET.match(message)
    if not match:
        return None, message, None

    mot = match.group(1).lower()
    reste = match.group(2).strip()

    if mot in CROCHETS:
        return mot, reste, CROCHETS[mot]

    # Mot inconnu dans la liste fermee
    return mot, reste, None


# Les DEUX mots du cadrage (le theme CADRAGE les declare : `[???]` et son alias
# officiel `[preparer]`). Declares une fois, ici : le routeur les JOUE.
CROCHETS_CADRAGE = ("???", "preparer")


def titres_du_vrac():
    """Les titres deja presents au vrac (pour la REGLE de doublon).

    Lu dans l'etat de l'entonnoir du pilote. Un etat illisible rend une liste VIDE
    et le fait est DIT par l'appelant -- jamais une exception qui empecherait le
    cadrage de tourner (un process autonome ne meurt pas sur une lecture).
    """
    import json as _json
    base = Path(__file__).resolve().parent.parent
    titres = []
    for nom in ("entonnoir-files-optimus.json", "file-missions-optimus.json"):
        chemin = base / nom
        if not chemin.is_file():
            continue
        try:
            donnees = _json.loads(chemin.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        pile = [donnees]
        while pile:
            noeud = pile.pop()
            if isinstance(noeud, dict):
                for cle, valeur in noeud.items():
                    if cle in ("theme", "titre", "objectif") and isinstance(valeur, str):
                        titres.append(valeur)
                    elif isinstance(valeur, (dict, list)):
                        pile.append(valeur)
            elif isinstance(noeud, list):
                pile.extend(noeud)
    return titres


def jouer_cadrage(mot, reste, options, resultat, mode_json):
    """JOUE le cadrage de bout en bout : la chaine est constituee PUIS versee.

    Trois litiges s'eteignent ici : le parcours est joue (1), les maillons sont
    TYPES a la naissance donc executables (3), et la chaine EXISTE comme liste (5).
    Le doublon (2) est resolu par la REGLE du moteur (>= 2 mots significatifs
    communs), jamais rendu au lecteur. Ce qui reste a dire est DIT -- un process
    autonome qui cache ce qu'il n'a pas pu faire se lit comme un process complet.
    """
    titre = options.get("theme", "").strip() or reste.split(".")[0][:120]
    demande = options.get("objectif", "").strip() or reste
    urgence = options.get("urgence", "").strip() or "normale"
    source = options.get("source", "").strip() or SOURCE_DEFAUT
    simuler = str(options.get("simuler", "")).strip().lower() in ("oui", "true", "1")
    if not titre:
        print("REFUS : le cadrage exige un TITRE -- --theme \"...\" (le titre du")
        print("  depot ; sans lui rien ne peut etre constitue ni retrouve).")
        return 2
    maillons = cadrage.constituer_la_chaine(titre, demande)
    jumeau, communs = cadrage.doublon_avec(titre, titres_du_vrac())
    texte = cadrage.texte_de_la_chaine(maillons)
    if jumeau:
        texte += ("\n  JUMEAU EXISTANT, RESOLU PAR REGLE : "
                  + jumeau[:90] + " (mots communs : " + ", ".join(communs)
                  + ") -- la chaine le COMPLETE (un item n'est pas une suite de"
                  " missions) : aucun item jumeau n'est redepose, les maillons si.")
    deposes, refus = cadrage.verser(
        maillons, CHEMIN_DEPOT, titre, urgence, source,
        trace="cadrage [%s] du createur, 2026-09-21" % mot, simuler=simuler)
    if mode_json:
        import json as _json
        resultat["cadrage"] = {"titre": titre, "maillons": maillons,
                               "simule": simuler, "deposes": deposes, "refus": refus,
                               "doublon": jumeau}
        print(_json.dumps(resultat, ensure_ascii=False, indent=2))
        return 0
    print("[" + mot + "] CADRAGE JOUE DE BOUT EN BOUT (aucune question au createur)")
    print("  " + texte.replace("\n", "\n  "))
    print()
    for case, sortie in deposes:
        print("  VERSE  [" + case + "] " + sortie[:120])
    for case, sortie in refus:
        print("  REFUS  [" + case + "] " + sortie[:160])
    print("  " + str(len(deposes)) + " maillon(s) verse(s), " + str(len(refus))
          + " refus nomme(s) -- la chaine se poursuit sans intervention.")
    return 0


def jouer_intervention(mot, reste, resultat, mode_json):
    """Tient une INTERVENTION : imprime la mini-reflexion et la TRACE sur la mission.

    RIEN N EST DEPOSE (choix du createur) : une intervention ne fabrique pas de
    mission. Elle est portee au journal de la mission COURANTE, avec la decouverte
    du createur qui l a declenchee -- sans quoi elle ne serait relisible nulle part
    apres coup.

    S IL N Y A AUCUNE MISSION EN COURS, l acte est joue quand meme (la reflexion
    s applique au round) mais la trace le DIT, au lieu de l ecrire sous une mission
    inventee ou de la taire (L-055).
    """
    reflexion = MINI_REFLEXIONS.get(mot, "")
    fichiers = charger_file()
    mission = mission_en_cours(fichiers) if fichiers else None
    identifiant = str((mission or {}).get("id", ""))
    theme = str((mission or {}).get("theme", ""))
    detail = reflexion + (" -- DECOUVERTE DU CREATEUR : " + reste if reste else "")
    if identifiant:
        code, _sortie = noter_journal(identifiant, theme, ACTION_INTERVENTION, detail)
        trace = ("TRACE : " + identifiant + " (journal suivi-optimus, action "
                 + ACTION_INTERVENTION + ") -- code " + str(code))
        if code != 0:
            trace += " -- la porte a REFUSE la trace, elle n est pas posee"
    else:
        trace = ("AUCUNE TRACE : aucune mission n est en cours -- la reflexion"
                 " s applique au round, il n y a pas de journal ou la poser")
    if mode_json:
        import json
        resultat["intervention"] = {"reflexion": reflexion, "mission": identifiant,
                                    "trace": trace}
        print(json.dumps(resultat, ensure_ascii=False, indent=2))
        return 0
    print("[" + mot + "] INTERVENTION sur la MISSION EN COURS (aucun depot, aucune file)")
    print("  Mini-reflexion : " + reflexion)
    if reste:
        print("  Decouverte du createur : " + reste[:200])
    print("  " + trace)
    return 0


def executer(arguments):
    """Verbe filtrer : --message <texte> [--json]

    Detecte [mot] et route vers la bonne porte.
    Retourne 0 = route OK, 1 = aucun crochet, 2 = crochet inconnu.
    """
    options = extraire_options(arguments, NOMS_OPTIONS)
    message = options.get("message", "").strip()
    mode_json = "--json" in arguments

    if not message:
        print("Usage : python main.py filtrer --message \"[mission] faire quelque chose\"")
        return 2

    mot, reste, config = detecter_crochet(message)

    if mot is None:
        # Pas de crochet = message normal, pas de routage
        if mode_json:
            import json
            print(json.dumps({"detected": False, "message": message}))
        else:
            print("Aucun crochet detecte. Message normal.")
        return 1

    if config is None:
        # Crochet inconnu
        if mode_json:
            import json
            print(json.dumps({
                "detected": True,
                "mot": mot,
                "known": False,
                "error": "Crochet inconnu : [" + mot + "]. Liste fermee : " + ", ".join(sorted(CROCHETS.keys())),
            }))
        else:
            print("ERREUR : [" + mot + "] non reconnu.")
            print("Liste fermee : " + ", ".join(sorted(CROCHETS.keys())))
        return 2

    # Crochet reconnu = routage
    resultat = {
        "detected": True,
        "mot": mot,
        "known": True,
        "porte": config["porte"],
        "action": config["action"],
        "type": config["type"],
        "reste": reste,
        "date": horodater(),
    }

    # INTERVENTION SUR LA MISSION EN COURS : elle ne passe par AUCUNE porte (il n y
    # a rien a jouer ailleurs) -- elle est TENUE ici, imprimee et tracee.
    if mot in CROCHETS_MISSION:
        return jouer_intervention(mot, reste, resultat, mode_json)

    # CADRAGE AUTONOME (2026-09-21, crochet [corriger] du createur) : [???] et son
    # alias [preparer] ne sont PLUS imprimes ("ROUTE IMPRIMEE, PAS JOUEE" etait le
    # litige 1 : l'agent devait jouer le parcours, et il pouvait s'arreter). Le
    # moteur CONSTITUE LA CHAINE et la VERSE par la porte -- sans aucune question au
    # createur : une incertitude devient un MAILLON MESURABLE, jamais une question.
    if mot in CROCHETS_CADRAGE:
        return jouer_cadrage(mot, reste, options, resultat, mode_json)

    # MO-175 : la DETECTION ne suffit pas -- le pilote JOUE la porte routee.
    code_depot, sortie_depot = None, ""
    if (config["porte"], config["action"]) == PORTE_DEPOT:
        code_depot, sortie_depot = jouer_depot(
            options.get("theme", ""), reste, options.get("source", SOURCE_DEFAUT),
            config.get("type", ""))

    if mode_json:
        import json
        print(json.dumps(resultat, ensure_ascii=False, indent=2))
    else:
        print("[" + mot + "] detected -> " + config["porte"] + "/" + config["action"])
        if reste:
            print("  Contenu : " + reste[:120])
        print("  Porte : " + config["porte"])
        print("  Action : " + config["action"])

    if code_depot is not None:
        if sortie_depot:
            print(sortie_depot)
        print("  DEPOT JOUE (porte " + config["porte"] + "/" + config["action"]
              + ") : code " + str(code_depot))
    else:
        # MO-303 : une route DETECTEE mais non JOUEE ne peut plus etre un silence.
        # Mesure : un [preparation] ne faisait RIEN (la route pointait un theme, pas
        # une porte) et rien ne le disait -- la demande n'entrait dans aucune file et
        # se lisait comme traitee (L-055 : un defaut muet se lit comme un fait).
        print("  ROUTE IMPRIMEE, PAS JOUEE : cette porte n'est pas un depot --"
              " c'est l'agent qui la joue ensuite (la demande n'est dans aucune file).")
    return code_depot if code_depot is not None else 0
