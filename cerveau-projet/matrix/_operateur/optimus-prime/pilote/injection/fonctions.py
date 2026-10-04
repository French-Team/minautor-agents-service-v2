"""Fonctions simples de la categorie injection : une seule tache chacune."""
import importlib.util
import json
import re
from pathlib import Path

from commun import (
    annoncer,
    annoncer_debut,
    armer_lot,
    bilan_consolide,
    charger_entonnoir_pilote,
    declarer_auto_validation,
    defcon_bloque_theme,
    deposer_message,
    enregistrer_file,
    horodater,
    ids_en_lot,
    item_du_vivier,
    item_id_de_la_source,
    mission_en_cours,
    noter_journal,
    declarer_borne_marbre,
    prochaine_du_lot,
    prochaine_en_attente,
    puiser_tresse,
    refus_serie_stricte,
    rafraichir_vue_suivi,
    resume_mission,
    session_en_pause,
    journaliser_mission,
    valider_theme,
)
from personnalites import role_de_mission
from injection.modes_emploi import mode_emploi_brique, noms_servables
from checklist.listes import OUTILS_COMMUNS, OUTILS_PAR_TYPE, OUTILS_TOUJOURS, TYPES
from checklist.stockage import fabrique_checklist
from entonnoir.listes import CHAMP_OUTILS, CHAMP_SOURCE_TRACE
from constants import (
    BOITE_PILOTE_OUT,
    CHAMP_AUTO_VALIDATION,
    CHAMP_PROFIL,
    CHAMP_SI_J_ETAIS_USER,
    CHAMP_RAPPEL,
    CHEMIN_THEMES,
    CLE_AUTO_VALIDEES,
    ENCODAGE,
    GABARIT_COMMANDE_RECHERCHE,
    RAPPEL_CHAINE,
    RAPPEL_ROUTE_OUTIL,
    RAPPEL_ROUND_SERVI,
    REPERTOIRE_DATA,
    REPERTOIRE_PILOTE,
    PLAFOND_OUTILS_MODE_EMPLOI,
    PLAFOND_PROFIL_TOKENS,
    STATUT_EN_ATTENTE,
    STATUT_EN_COURS,
    TYPE_ROUTE_OUTIL,
    VALEUR_AUTO_VALIDATION,
)

try:
    from tokens import peser_tokens
except ImportError:  # jamais bloquant : sans le motif, l'injection part sans poids
    peser_tokens = None

# MOTIF PARTAGE DE LA FICHE UTILISATEUR (M-076) : le chemin de la fiche, la liste
# des champs ATTENDUS et la lecture des valeurs vivent dans
# `data/commun/fiche_profil.py` -- la routine vigie-profil et le pilote les
# LISENT, ils ne les recopient jamais (deux copies = deux verites, L-029, et deux
# chemins dont l'un pointe un fichier mythique : c'est arrive, MO-043). Absent, le
# profil n'est pas injecte en silence : le bloc porte un avertissement NOMME
# (doctrine "jamais de degradation silencieuse") -- c'est le GARDE qui refuse,
# jamais le flux de travail.
try:
    import fiche_profil as motif_profil
except ImportError:
    motif_profil = None

# MOTEUR DE RECHERCHE (EO-131) : la QUESTION a poser vient du module PARTAGE
# (data/commun/recherche_mission.py) -- les DEUX flux consomment le meme, ils ne
# le recopient pas (lecon L-029). Absent, l'injection ne meurt pas : elle le DIT
# (doctrine du sac-a-dos : jamais bloquant) -- c'est le GARDE qui refuse, jamais
# le flux de travail.
try:
    from recherche_mission import preparer_recherche
except ImportError:
    preparer_recherche = None

# Espion de POIDS des injections (E-097, imperatif 56) : le sac-a-dos remis a
# l'agent est pese -- on voit combien de contexte la Matrice lui demande de lire
# (objectif + checklist + lecons + themes + role + recherche + rappel). Champs
# fermes : liste unique. Le RAPPEL (R5) est du contexte OFFERT : il se compte
# comme le reste -- un rappel qu'on ne pese pas serait du contexte en franchise.
# CHAMPS PESES (MO-314) : tout ce que le sac-a-dos PORTE doit etre pese, sinon la
# mesure se tait sur ce qui a grandi. `modes_emploi` a ete ajoute le 2026-09-20 : les
# modes d emploi injectes n entraient dans AUCUN poids, donc le sac-a-dos annoncait
# moins qu il ne livrait. MESURE 2026-09-20 (apres le plafond, MO-314) : les quatre
# cartes pesent 1792 tokens bornees (2373 completes, 51 briques sur 98 servies) et
# l injection avant-mission entiere 7435 -- la mesure se rejoue :
#   python injecter.py avant-mission --peser
# `profil` a ete ajoute le 2026-09-21 pour la MEME raison : le profil de
# l'utilisateur part desormais avec la mission, donc il se pese comme le reste --
# un champ livre sans poids est du contexte en franchise.
# LE ROLE DU PERSONNAGE (MO-539, EO-533, demande createur 2026-10-02).
# Le champ `role` de l injection porte la POSTURE de la mission (qui conduit,
# deduite du type) ; ce champ porte le PERSONNAGE de l agent -- celui que son nom
# promet. Les deux ne se confondent pas : une posture change a chaque mission,
# le personnage est le meme toujours. C est la distinction que la demande
# formuleait : < notre agent doit devenir Optimus Prime, cela ne doit pas juste
# etre le nom d un agent >.
CHAMP_ROLE_AGENT = "role_agent"

# LE DOMICILE du personnage : son PROPRE fichier, `role-optimus-prime.md`. Il est
# CONSOMME par chemin, jamais recopie (M-076) -- une recopie ne serait plus le
# personnage vivant, ce serait une etiquette de plus, exactement ce que la
# demande refuse. Il n est pas dans la fiche : celle-ci a un plafond DECLARE de
# 150 lignes, et le personnage n a pas besoin d etre lu une fois au demarrage
# (il est servi AVEC chaque mission). Mesure : ecrit dans la fiche, il la faisait
# passer a 168 lignes et `verifier-fiche.py` l a refusee.
CHEMIN_ROLE_AGENT = Path(__file__).resolve().parent.parent.parent / "role-optimus-prime.md"
TITRE_ROLE_AGENT = "# ROLE -- LE PERSONNAGE"


def section_role_agent(chemin=None):
    """La section ROLE de son domicile, et SA SEULE (jamais le reste du fichier).

    REND (texte, motif) : le texte est la section brute, le motif est vide si elle
    a ete lue. Une section absente ou illisible ne se rattrape pas en silence :
    elle DIT pourquoi elle manque, et l appelant decide -- une section ROLE
    absente est un agent sans personnage, et c est un fait, pas un detail.
    """
    cible = Path(chemin) if chemin else CHEMIN_ROLE_AGENT
    try:
        lignes = cible.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as erreur:
        return "", ("fiche PERSONNAGE ILLISIBLE : " + str(cible) + " ("
                    + type(erreur).__name__ + " : " + str(erreur) + ")")
    debut = None
    for numero, ligne in enumerate(lignes):
        # Le titre est lu par son DEBUT, pas par egalite : le domicile peut
        # porter une precision apres le tiret ("# ROLE -- LE PERSONNAGE (ce que
        # mon nom promet)"). Comparer a l egalite refusait un role correctement
        # ecrit -- mesure au premier essai.
        if ligne.startswith(TITRE_ROLE_AGENT):
            debut = numero
            break
    if debut is None:
        return "", ("le domicile " + str(cible) + " ne porte AUCUNE section `"
                    + TITRE_ROLE_AGENT + "` -- l agent n a pas de personnage")
    fin = len(lignes)
    for numero in range(debut + 1, len(lignes)):
        # La section s arrete au PROCHAIN titre, quel que soit son niveau :
        # un `##` suivant est deja une autre section. Regler sur `# ` seulement
        # laissait la fuite (mesure : un domicile <# ROLE ...> / <## SUITE>
        # rendait "## SUITE" comme personnage).
        if lignes[numero].startswith("#"):
            fin = numero
            break
    # Le TITRE ne fait pas partie du personnage : c est une etiquette. Un
    # domicile qui ne porte QUE le titre n en porte pas -- mesurer l aurait accepte
    # comme role (contre-temoin joue, puis repare).
    corps = chr(10).join(lignes[debut + 1:fin]).strip()
    section = chr(10).join([lignes[debut].strip(), corps]).strip() if corps else ""
    if not section:
        return "", ("la section `" + TITRE_ROLE_AGENT + "` est VIDE dans "
                    + str(cible) + " -- un personnage declare et vide n en est pas un")
    return section, ""


def charger_role_agent():
    """Le personnage dans le sac-a-dos, a CHAQUE mission (jamais conditionnel).

    CONTRAIREMENT a `si_j_etais_user` (qui se sert au moment ou elle sert), le
    personnage est servi TOUJOURS : c est la demande du createur, < il va etre
    important d injecter regulierement ce role qui doit toujours avoir en tete >.
    Une regle qu on n injecte que parfois est une regle qu on ne tient pas.

    Le REFUS est DIT, jamais avale : une fiche sans personnage rend une injection
    qui le nomme, et l agent sait alors qu il agit sans son role (L-055).
    """
    section, motif = section_role_agent()
    return {"personnage": section, "motif": motif, "applique": bool(section),
            "domicile": str(CHEMIN_ROLE_AGENT)}


CHAMPS_PESES = ("objectif", "checklist", "lecons_utiles", "themes_utiles", "role",
                "recherche", CHAMP_RAPPEL, "modes_emploi", CHAMP_PROFIL,
                CHAMP_SI_J_ETAIS_USER, CHAMP_ROLE_AGENT)


def poids_injection(injection):
    """Retourne le poids estime (tokens) du sac-a-dos remis a l'agent.

    0 si le motif tokens est absent : une injection n'echoue JAMAIS parce que
    l'espion manque (doctrine : jamais bloquant).
    """
    if peser_tokens is None:
        return 0
    morceaux = [
        json.dumps(injection.get(champ), ensure_ascii=True)
        for champ in CHAMPS_PESES
        if injection.get(champ)
    ]
    return peser_tokens(*morceaux)


def poids_fiche(injection):
    """Poids estime (tokens) de la FICHE -- ce que la remise imprime REELLEMENT.

    0 si le motif tokens manque (jamais bloquant). DISTINCT de `poids_injection`, qui
    mesure l injection DEPOSEE : la fiche est ce que l agent LIT a chaque round, donc
    la grandeur qui doit tenir le PLAFOND DE REMISE.
    """
    if peser_tokens is None:
        return 0
    return peser_tokens("\n".join(fiche_technique(injection)))


# --- LA FICHE TECHNIQUE DE TRAVAIL (MO-471, decisions D2/D3/D4) -------------
# Le cadrage < templates d injection > a reduit la demande a des DECISIONS (graves dans
# _operateur/optimus-prime/preparation/decisions-cadrage-templates-injection.md). En voici
# la PREMIERE LIVRAISON, MINIMALE et en LECTURE SEULE :
#   D2 : la fiche RESUME l injection (elle ne la remplace pas) ; le NOYAU est toujours dit,
#        les AJUSTABLES sont resumes et joignables par `ordres --complet`.
#   D3 : un PLAFOND GLOBAL d injection est DECLARE et la fiche DIT s il est depasse.
#   D4 : le NOYAU (jamais retire) et les AJUSTABLES (bornes) sont deux listes FERMEES.
# Un champ ABSENT se DIT (L-055) : la fiche crie sur un noyau manquant, jamais un silence.
NOYAU_FICHE = ("objectif", "checklist", "role", CHAMP_ROLE_AGENT, CHAMP_RAPPEL,
               CHAMP_AUTO_VALIDATION, "recherche")
# LES CHAMPS DU NOYAU QUI PEUVENT SE TAIRE, ET POURQUOI (EO-492). Un champ,
# UNE RAISON, ecrite UNE fois ici (M-076) : la fiche rend alors
# < vide par design -- raison > au lieu de <ABSENT>, et son KO ne nomme plus que
# les champs REELLEMENT absents. Mesure : sur 152 missions dev terminees, 9
# seulement portaient un rappel non vide -- le rappel VIDE est le cas COMMUN,
# donc le garde hurle sur la normale (proto-12 : un rouge qu on doit se rappeler
# normal ne garde rien, il brouille). Le rappel se tait parce que ni lot, ni
# suite auto-validee, ni type reparation : le silence EST la regle (EO-274,
# docstring de charger_rappel_route). Il ne rend pas l absence muette : une
# absence REELLE se crie toujours (L-055), et le maillon de la non-regression le
# prouve -- rappel plein, rappel vide, role absent.
CHAMPS_PEUVENT_SE_TAIRE = {
    CHAMP_RAPPEL: "ni lot, ni suite auto-validee, ni type reparation : c est le cas"
                  " COMMUN, pas une absence (mesure 2026-09-30 : 143 missions dev"
                  " sur 152 sans rappel). Un rappel toujours present ne se lit plus"
                  " (EO-274).",
}
CHAMPS_AJUSTABLES = ("lecons_utiles", "themes_utiles", "modes_emploi", CHAMP_PROFIL,
                     CHAMP_SI_J_ETAIS_USER)
PLAFOND_INJECTION_TOKENS = 12000
# PLAFOND DE REMISE (MO-473) : la fiche est ce que l agent LIT a chaque round ; elle a
# donc son PROPRE plafond, distinct de celui de l injection. Mesure du 2026-09-26 sur 20
# missions reelles : mediane 966 tokens, MAX 1278 -- le plafond est declare a 3000 (plus
# du DOUBLE du max mesure). Un depassement se DIT, jamais un tronquage muet : le NOYAU
# est ce qui DECIDE, on ne le coupe pas en silence (L-055).
PLAFOND_REMISE_TOKENS = 3000


def _taille_champ(valeur):
    """Taille (octets json) d un champ d injection, 0 s il est vide (jamais un faux 0 muet)."""
    return len(json.dumps(valeur, ensure_ascii=True)) if valeur else 0


def _lignes_noyau(champ, valeur):
    """Le NOYAU se DIT EN ENTIER (D2) : ce qui DECIDE ne se tronque JAMAIS.

    Un texte est rendu tel quel ; une liste en puces ; un objet en cles/valeurs.
    Un champ ABSENT sort en <ABSENT> (L-055, jamais un silence). C est ce qui
    distingue le NOYAU des AJUSTABLES, qui sont RESUMES.
    """
    etiquette = "  [noyau] " + champ
    if valeur is None or valeur == "" or valeur == [] or valeur == {}:
        return [etiquette + " : <ABSENT>"]
    if isinstance(valeur, str):
        return [etiquette + " : " + valeur.strip()]
    if isinstance(valeur, (list, tuple)):
        return ([etiquette + " (" + str(len(valeur)) + ") :"]
                + ["    - " + str(element) for element in valeur])
    if isinstance(valeur, dict):
        return ([etiquette + " (" + str(len(valeur)) + " cle(s)) :"]
                + ["    " + str(cle) + " : " + str(valeur[cle]) for cle in valeur])
    return [etiquette + " : " + str(valeur)]


def _resume_champ(valeur):
    """Resume COURTE d une valeur : jamais le contenu entier (c est le but de la fiche)."""
    if valeur is None:
        return ""
    if isinstance(valeur, str):
        return valeur.strip().replace(chr(10), " ")[:200]
    if isinstance(valeur, list):
        return str(len(valeur)) + " element(s)"
    if isinstance(valeur, dict):
        return ", ".join(str(cle) for cle in valeur)
    return str(valeur)[:200]


def fiche_technique(injection):
    """La FICHE TECHNIQUE DE TRAVAIL : BORNEE, SANS PERTE (MO-471).

    Rend une liste de lignes : le NOYAU (dit en entier, c est ce qui DECIDE), les
    AJUSTABLES (resumes, joignables par `ordres --complet`), le POIDS contre le PLAFOND
    GLOBAL, et une ligne KO si un champ du NOYAU manque. Aucune ecriture.
    """
    if not injection:
        return ["FICHE TECHNIQUE : injection INTROUVABLE -- rien a borner (le DIT, jamais le taire)"]
    lignes = ["FICHE TECHNIQUE DE TRAVAIL : " + str(injection.get("mission", ""))
              + " (" + str(injection.get("theme", "")) + ")"]
    manquants = []
    for champ in NOYAU_FICHE:
        valeur = injection.get(champ)
        raison = CHAMPS_PEUVENT_SE_TAIRE.get(champ)
        if not valeur and raison is not None:
            # UN SILENCE CONCU, DIT (EO-492) : la fiche nomme le champ et la
            # raison du silence. Ce n est pas une absence, donc ce n est pas
            # compte dans les manquants -- et le vrai manque reste crie.
            lignes.append("  [noyau] " + champ + " : vide par design -- " + raison)
            continue
        if not valeur:
            manquants.append(champ)
        lignes.extend(_lignes_noyau(champ, valeur))
    lignes.append("  [ajustables] resumes (joignables : pilote ordres --id <id> --complet) :")
    for champ in CHAMPS_AJUSTABLES:
        valeur = injection.get(champ)
        lignes.append("    " + champ + " : " + ("present" if valeur else "absent")
                      + " (" + str(_taille_champ(valeur)) + " o)")
    poids = injection.get("poids_tokens") or 0
    etat_poids = "DEPASSE" if poids > PLAFOND_INJECTION_TOKENS else "tenu"
    lignes.append("  POIDS : " + str(poids) + " tokens / PLAFOND GLOBAL "
                  + str(PLAFOND_INJECTION_TOKENS) + " -- " + etat_poids)
    if manquants:
        lignes.append("  KO : champ(s) du NOYAU ABSENT(S) : " + ", ".join(manquants))
    return lignes


def afficher_ordres(charger_file, identifiant, complet=False, peser=False):
    """Affiche la FICHE (defaut), l injection ENTIERE (--complet) ou la MESURE (--peser).

    LECTURE SEULE : aucun etat modifie. `--peser` rend le poids de la fiche contre le
    PLAFOND DE REMISE, le poids de l injection entiere, et le GAIN de la remise -- avec
    le peseur du domicile partage. Une mesure REJOUABLE, jamais un chiffre recopie.
    """
    from commun import derniere_injection
    injection = derniere_injection(identifiant)
    if not injection:
        print("ORDURES : aucune injection pour " + str(identifiant)
              + " -- la porte ne l a pas retrouvee (le DIT, jamais le taire).")
        return 1
    if peser:
        fiche = poids_fiche(injection)
        entiere = poids_injection(injection)
        etat = "DEPASSE" if fiche > PLAFOND_REMISE_TOKENS else "tenu"
        print("MESURE DE REMISE -- " + str(identifiant))
        print("  FICHE TECHNIQUE   : " + str(fiche) + " tokens / plafond de remise "
              + str(PLAFOND_REMISE_TOKENS) + " -- " + etat)
        print("  INJECTION ENTIERE : " + str(entiere) + " tokens")
        if entiere:
            print("  GAIN DE LA REMISE : " + str(entiere - fiche) + " tokens ("
                  + str(int(100 * (entiere - fiche) / entiere)) + " pour cent)")
        return 0
    if complet:
        print(json.dumps(injection, ensure_ascii=True, indent=2))
        return 0
    for ligne in fiche_technique(injection):
        print(ligne)
    return 0


def afficher_statut(file_missions):
    """Affiche l'etat de la mission en cours (ou l'absence de mission en cours)."""
    mission = mission_en_cours(file_missions)
    if mission is None:
        en_attente = sum(1 for m in file_missions.get("missions", []) if m.get("statut") == STATUT_EN_ATTENTE)
        print("Aucune mission en cours. File : " + str(en_attente) + " en attente.")
        return 0
    print("Mission en cours : " + mission["id"] + " (theme : " + mission["theme"] + ") -- " + mission["objectif"])
    # MO-421 : la TRACE de provenance (la place du maillon dans sa chaine, ce que la
    # case [depot] met dans --trace) est AFFICHEE -- l ordre n etait lisible nulle
    # part (mesure : 0 maillon sur 7) ; un ordre qui ne se lit pas n ordonne rien.
    trace = str(mission.get(CHAMP_SOURCE_TRACE) or "").strip()
    if trace:
        print("Trace de chaine : " + trace)
    # AUTO-VALIDATION (EO-143) : la garantie est AFFICHEE, et son ABSENCE se DIT.
    # Une garantie qui ne vit que dans une absence se re-cree au premier garde qui
    # l ignore (ecart mesure par MO-160) ; un repli muet la rendrait invisible.
    auto_validation = mission.get(CHAMP_AUTO_VALIDATION, "")
    if auto_validation:
        print("Auto-validation : " + auto_validation
              + " -- mission deja vue avec le createur : enchaine sans redemander"
              + " (le CRITIQUE reste au createur).")
    else:
        print("Auto-validation : champ ABSENT (mission anterieure au champ, EO-143)"
              + " -- la regle immuable auto-validation-missions s applique.")
    return 0


def garder_theme_et_checklist(mission):
    """Garde le THEME (champ ferme) et fabrique la checklist. -> (code, checklist).

    UN SEUL endroit pour les DEUX chemins d'injection (mission simple et lot) :
    deux copies de ce garde recreeraient exactement le trou qu'on vient de
    fermer (deux implementations = deux comportements, un chemin protege et
    l'autre non).

    Garde du theme (trou ferme le 2026-09-13) : un theme hors vivier ne doit
    JAMAIS devenir du travail. C'est le POINT DE PASSAGE UNIQUE -- il couvre
    l'entonnoir, `charger` ET une file modifiee a la main -- sans dupliquer la
    lecture du vivier (une seule source : commun.valider_theme).
    La mission RESTE en attente : on ne la rejoue pas, on la corrige
    (`python main.py retiqueter --id MO-XXX --theme <nom>`).

    Checklist : le SPECIFIQUE vient du type (liste fermee de l'entonnoir), les
    garde-fous COMMUNS valent pour toute mission -- un type absent ne supprime
    plus les garde-fous (fabrique_checklist ne rend jamais une liste vide).

    code != 0 -> injection REFUSEE, mission laissee en attente.
    """
    code, theme_valide = valider_theme(mission.get("theme", ""))
    if code != 0:
        # Le refus NOMME la porte qui repare, selon l'ORIGINE de la mission :
        # une mission nee d'un item d'entonnoir se repare a la porte de
        # l'ENTONNOIR (son role, L-061/MO-076) -- retiqueter la mission ne
        # servirait a rien, elle serait re-ecrasee au prochain puisage du brin.
        # Le format de la provenance se LIT chez son domicile (commun.py, MO-339) :
        # cette porte le recomposait sur place, donc une troisieme copie du meme
        # format vivait ici -- et la decision d'enchainement, elle, ne l'utilisait
        # pas du tout (le defaut que MO-339 ferme).
        item_id = item_id_de_la_source(mission.get("source"))
        if item_id:
            porte = ("python entonnoir/main.py retiqueter --id " + item_id
                     + " --role <THEME du vivier>")
        else:
            porte = ("python main.py retiqueter --id " + mission.get("id", "?")
                     + " --theme <nom du vivier>")
        print("(mission " + mission.get("id", "?") + " laissee en attente : corrige son ROLE -- " + porte + ")")
        return code, []
    type_mission = mission.get("type") or theme_valide
    checklist = mission.get("checklist") or fabrique_checklist(type_mission)
    if type_mission not in TYPES:
        print(
            "ECART : " + mission["id"] + " sans type ferme (type/theme : " + type_mission
            + ") -- checklist REDUITE aux garde-fous communs (le specifique du type manque)."
        )
    return 0, checklist




def index_auto_valide():
    """L INDEX des missions auto-validees : une liste d IDS (3e jambe MO-175).

    L index vit dans l ETAT DE L ENTONNOIR : le pilote le LIT (pour decider de
    l enchainement), il ne l ecrit jamais -- la queue appartient a l entonnoir.
    Un etat illisible se DIT et rend une liste vide : la priorite continue, sans
    repli muet (une auto-validee ne disparait jamais en silence).
    """
    try:
        etat = charger_entonnoir_pilote()
    except Exception as erreur:
        print("[--] index auto-valide illisible (" + type(erreur).__name__
              + ") : aucun item auto-valide lu.")
        return []
    if not isinstance(etat, dict):
        return []
    return list(etat.get(CLE_AUTO_VALIDEES) or [])


def est_auto_validee(mission, index_auto):
    """Vrai si la mission est AUTO-VALIDEE -- par TROIS voies, jamais par supposition.

    (1) le CHAMP porte par l ENREGISTREMENT de la mission
        (constants.CHAMP_AUTO_VALIDATION, GO createur) ;
    (2) l INDEX de l entonnoir, quand il nomme la MISSION elle-meme ;
    (3) la PROVENANCE (MO-339, EO-264) : une mission nee d un item porte
        `source` = `entonnoir:<id>:...`, et c est l ID D ITEM qui figure dans
        l index -- jamais l id de la mission. Sans cette troisieme voie, le verdict
        se PERDAIT au pont : mesure du 2026-09-21, 45 missions sur 83 ne portaient
        aucun champ, dont MO-318 ne d EO-271 qui EST dans l index (55 ids) -- la
        chaine s arretait donc APRES CHAQUE mission sur une mission auto-validee.

    Aucun repli muet : une mission sans provenance lisible reste NON auto-validee
    (le createur reprend la main), et cette limite est DITE par la decision.
    """
    if not isinstance(mission, dict):
        return False
    if mission.get(CHAMP_AUTO_VALIDATION) == VALEUR_AUTO_VALIDATION:
        return True
    if mission.get("id") in index_auto:
        return True
    item_id = item_id_de_la_source(mission.get("source"))
    return bool(item_id) and item_id in index_auto


def tete_brin():
    """La TETE du brin en LECTURE SEULE -- meme source que le puisage (commun).

    Coup d oeil : on ne consomme rien tant que la decision n est pas prise (un
    puisage pour rien ferait disparaitre la tete du brin, donc l item).
    """
    try:
        etat = charger_entonnoir_pilote()
    except Exception:
        return None
    if not isinstance(etat, dict):
        return None
    brin = etat.get("brin") or []
    return brin[0] if brin else None


def decision_enchainement(mission, depuis_lot, enchainer, index_auto):
    """DECISION PURE (testable sans disque) : faut-il ARRETER l enchainement ?

    - un LOT arme est une decision EXPLICITE du createur : la chaine continue ;
    - une injection EXPLICITE (enchainer faux) n est pas un enchainement : elle
      passe (le verbe `injecter` reste un ordre, pas une decision automatique) ;
    - sinon -- c est la CHAINE -- une mission NON auto-validee ARRETE tout : le
      pilote rend la main (decision createur MO-175).
    Rend (arret, motif) : le motif est toujours DIT quand la chaine s arrete.
    """
    if mission is None or depuis_lot or not enchainer:
        return False, ""
    if est_auto_validee(mission, index_auto):
        return False, ""
    return True, (str(mission.get("id", "?")) + " n est PAS auto-validee --"
                  " la chaine s arrete ici (le createur reprend la main).")


def suite_auto_a_conduire(file_missions, index_auto, mission_courante=""):
    """L id de la SUITE auto-validee qu une fin lancera, ou "" (MO-318).

    Ce que le contrat de continuite ANNONCE a l agent doit etre EXACTEMENT ce que la
    decision fera a la fin : on lit donc la MEME regle, une seule fois -- la tete du
    brin d abord (si elle est auto-validee), puis la file (EO-175 : l auto-validee
    passe avant la file chargee). Deux lectures divergentes promettraient une suite
    qui n existe pas, et un rappel faux ne se lit plus (L-029).

    `mission_courante` est EXCLUE : a la fabrication de l injection, la mission qui
    part est encore `en-attente` dans la file (son statut ne bascule qu apres) --
    sans cette exclusion, une mission se promettrait ELLE-MEME comme suite.
    """
    tete = tete_brin()
    if tete is not None:
        identifiant = str(tete.get("id") or "")
        if identifiant and identifiant != str(mission_courante or ""):
            if est_auto_validee(tete, index_auto):
                return identifiant
    for candidate in file_missions.get("missions", []):
        if candidate.get("statut") != STATUT_EN_ATTENTE:
            continue
        identifiant = str(candidate.get("id") or "")
        if not identifiant or identifiant == str(mission_courante or ""):
            continue
        if est_auto_validee(candidate, index_auto):
            return identifiant
        # La PREMIERE mission en attente est celle que la fin servira : si elle
        # n est pas auto-validee, la chaine s ARRETERA la -- les suivantes ne
        # comptent pas, et le contrat ne doit donc pas etre annonce (c est le
        # contre-temoin exige par MO-318 : une fin qui ne reveille rien).
        return ""
    return ""


def _outils_declares_dans_objectif(mission):
    """Les outils que la mission AUTO-DECLARE dans son propre objectif.

    DECISION CREATEUR (2026-10-01, arbitree a la question "qui prepare la liste
    d outils par mission ?") : c est LA MISSION qui nomme ses outils, dans son
    objectif, et le pilote ne sert QUE ceux-la. Aucune preparation en amont.

    MESURE QUI A DIT QUE C ETAIT INERTE (EO-515 / EO-504) : la voie "item"
    (liste preparee) n etait jouee par PERSONNE -- 0 mission sur 85 en portait
    une, donc les 85 retombaient sur le repli generique par type, et le createur
    decrivait exactement les appels fautifs que cela produit. Le cable existait
    (preparer_outils) ; il ne manquait qu un ACTE. L acte, c est la mission
    elle-meme : elle ecrit ce qu elle va appeler.

    LA LECTURE EST PRUDENTE ET BORDEE :
      - elle ne cherche que des NOMS SERVABLES reels (un mot qui ressemble a un
        outil mais n en est pas un est ignore) ;
      - elle exige une FRONTIERE de mot, pour qu "ecrire" ne morde pas dans un
        mot plus long et qu un nom distinctif comme "garde-perimetre-write.py"
        ne soit pas tronque ;
      - elle rend les noms DANS L ORDRE OU L OBJECTIF LES NOMME, puis le
        plancher est ajoute en tete par _avec_plancher.
    Elle rend la liste vide si l objectif ne nomme aucun outil : c est alors le
    repli par type qui parle, et la voie est DITE.
    """
    objectif = " ".join([str(mission.get("objectif") or ""),
                         str(mission.get("titre") or "")])
    if not objectif.strip():
        return []
    trouves = []
    for nom in noms_servables():
        motif = r"(?<![A-Za-z0-9])" + re.escape(nom) + r"(?![A-Za-z0-9])"
        trouve = re.search(motif, objectif)
        if trouve and nom not in trouves:
            trouves.append(nom)
    # L ORDRE DE L OBJECTIF, pas celui du registre : ce que la mission dit
    # d abord est ce qu elle appelle d abord.
    trouves.sort(key=lambda nom: objectif.find(nom))
    return trouves


def _noms_des_outils(mission):
    """Les noms des outils de la mission, par la VOIE qui a parle. Rend (noms, voie).

    TROIS VOIES, dans cet ordre de priorite :
      - `objectif` : la mission AUTO-DECLARE ses outils dans son propre objectif
        (decision createur du 2026-10-01, arbitree a la question "qui prepare
        la liste ?"). C est la voie PRIMAIRE : la mission dit ce qu elle va
        appeler, et le pilote ne sert QUE cela.
      - `item` : la LISTE PREPAREE sur l item (porte `preparer` de l entonnoir),
        que le pont a RECOPIEE dans la mission (EO-313) ;
      - `type` : le REPLI par TYPE (OUTILS_PAR_TYPE), quand la mission ne
        declare rien et qu aucune liste n a ete preparee.
    La voie qui a parle est TOUJOURS DITE, jamais supposee. Un outil cite deux
    fois ne se sert QU UNE fois : premiere mention gagnante.
    """
    declares = _outils_declares_dans_objectif(mission)
    if declares:
        return _avec_plancher(declares), "objectif"
    prepares = []
    for nom in (mission.get(CHAMP_OUTILS) or []):
        nom = str(nom).strip()
        if nom and nom not in prepares:
            prepares.append(nom)
    if prepares:
        return _avec_plancher(prepares), "item"
    noms = []
    for nom in list(OUTILS_COMMUNS) + list(OUTILS_PAR_TYPE.get(str(mission.get("type", "")), ())):
        if nom not in noms:
            noms.append(nom)
    return _avec_plancher(noms), "type"


def _avec_plancher(noms):
    """Les outils du PLANCHER en TETE, puis la liste -- sans jamais de doublon.

    Le plancher (OUTILS_TOUJOURS) est ce que TOUTE mission doit avoir sous la main,
    quelle que soit la voie : un outil qu on veut voir utilise se SERT (mesure du
    2026-09-21 : le moteur de recherche etait absent de `dev` et `reparation`, donc
    l agent cherchait avec son outil natif -- qui ne connait ni les cartes, ni les
    BDD, ni les zones invisibles). En TETE et non a la fin : le plafond
    (PLAFOND_OUTILS_MODE_EMPLOI) coupe par la FIN, donc un outil essentiel place
    dernier pourrait etre ecarte en silence.
    """
    resultat = []
    for nom in list(OUTILS_TOUJOURS) + list(noms):
        if nom and nom not in resultat:
            resultat.append(nom)
    return resultat


def charger_modes_emploi(mission):
    """Les MINI modes d emploi des outils que la mission VA APPELER (proto-6, etape 2).

    POURQUOI (revision createur du 2026-09-20, MO-313) : l agent recevait une LISTE
    DE NOMS et devait relire chaque outil pour retrouver son usage -- c est de la que
    naissent les appels fautifs constates par le createur. Le mode d emploi est
    EXTRAIT de la brique elle-meme (injection/modes_emploi.py : jamais une fiche
    recopiee, M-076) et BORNE (PLAFOND_OUTILS_MODE_EMPLOI).

    QUELLE LISTE (EO-313) : celle PREPAREE sur l item quand elle existe, sinon le
    repli par TYPE -- et les champs `voie` et `source` DISENT laquelle a servi. Une
    liste servie sans dire d ou elle vient ne se relit pas : elle se croit.

    Une brique DECLAREE mais INTROUVABLE est DITE : elle ne disparait pas en silence,
    c est l ecart que le garde des contrats des outils accuse.
    """
    noms, voie = _noms_des_outils(mission)
    outils = []
    introuvables = []
    for nom in noms[:PLAFOND_OUTILS_MODE_EMPLOI]:
        texte, origine = mode_emploi_brique(nom)
        if not texte:
            introuvables.append(nom)
            continue
        outils.append({"nom": nom, "origine": origine, "mode_emploi": texte})
    return {
        "voie": voie,
        "source": ("les outils AUTO-DECLARES par la mission dans son objectif"
                   " (decision createur 2026-10-01)" if voie == "objectif"
                   else "la LISTE PREPAREE de l item (EO-313)" if voie == "item"
                   else "le repli par TYPE : la mission ne declare aucun outil"
                        " et aucune liste n est preparee"),
        "outils": outils,
        "introuvables": introuvables,
        "ecartes_par_plafond": noms[PLAFOND_OUTILS_MODE_EMPLOI:],
    }


CHEMIN_SOURCE_SI_J_ETAIS_USER = Path(__file__).resolve().parent / "si_j_etais_user.py"


def charger_si_j_etais_user(mission):
    """LA SOURCE D INJECTION < SI J ETAIS USER >, servie AU MOMENT ou elle sert (MO-416).

    Le createur a tranche le 2026-09-25 : la phase n est PAS un crochet -- c est le
    PILOTE qui sert ce genre de source quand on en a besoin, et le CONTROLE PERMANENT
    lit la TRACE DECLAREE. Le MOMENT (quand la source sert) vit a SON domicile
    (`injection/si_j_etais_user.py`) : il est CONSOMME par chemin, jamais recopie
    (M-076) -- comme l extracteur de modes d emploi charge deja le sien.

    DES QUE la source est servie, le pilote DECLARE sa trace par la porte `noter`
    (action `injection`, au vocabulaire FERME de suivi-optimus) : c est cette trace que
    la panne `source-non-injectee` LIT. Sans elle, une source servie partirait sans
    trace -- la lecon de `purge`, `intervention`, `charge` et `prise`.

    NON BLOQUANT : un decideur illisible se DIT dans le champ (motif du refus). Une
    source qui disparait en silence serait un angle mort de plus (L-055).
    """
    try:
        specification = importlib.util.spec_from_file_location(
            "si_j_etais_user", str(CHEMIN_SOURCE_SI_J_ETAIS_USER))
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except (ImportError, OSError, SyntaxError, AttributeError) as erreur:
        return {"applique": False, "moment": "", "questions": [],
                "motif": ("decideur de la source ILLISIBLE : "
                          + str(CHEMIN_SOURCE_SI_J_ETAIS_USER) + " ("
                          + type(erreur).__name__ + " : " + str(erreur) + ")")}
    decision = module.decider(mission.get("titre", ""), mission.get("objectif", ""))
    if decision.get("applique"):
        detail = ("source si-j-etais-user servie au moment <" + str(decision.get("moment"))
                  + "> : " + str(decision.get("motif")))
        code, sortie = noter_journal(mission["id"], mission.get("theme", "") or "PILOTE",
                                     "injection", detail, portes=["pilote:injection"])
        if code != 0:
            print("ALERTE trace : la source si-j-etais-user n a PAS pu etre declaree ("
                  + str(sortie)[:120] + ").")
    return decision


def preparer_injection(charger_file, enchainer=False, mission_forcee=None):
    """Prepare et depose l'injection ordonnee de la mission suivante.

    Serie stricte : REFUS si une mission est deja en cours.
    Protocole de pause (M-080) : REFUS si la session-matrix est EN PAUSE.
    Priorite au createur : 1) le lot arme, 2) l ITEM AUTO-VALIDE en tete du brin
    (decision MO-175 : l auto-validee passe AVANT la file chargee, juste apres
    le lot arme), 3) la file des missions chargees, 4) la TRESSE (puisage
    automatique : tisser si besoin, puis tete du brin).
    ENCHAINEMENT (3e jambe MO-175) : quand `enchainer` est vrai (appel depuis
    `fin`), la chaine s ARRETE des que la mission a injecter n est PAS
    auto-validee -- le createur reprend la main. Une injection EXPLICITE
    (`enchainer` faux, verbe `injecter`) n est pas un enchainement : elle passe.
    Un STOP NE CONSOMME RIEN (decision createur 2026-09-18) : le candidat est
    juge AVANT d etre tire -- la tete du brin reste en tete, la file garde sa
    mission. Un arret ne se paie donc d aucun effet de bord.
    """
    if session_en_pause():
        print("REFUS : session-matrix EN PAUSE (protocole M-080) -- aucune injection pendant la maintenance.")
        print("(reprise par l'outil pause-session, verbe reprendre, apres maintenance user)")
        return 1
    file_missions = charger_file()
    refus = refus_serie_stricte(file_missions)
    if refus:
        print(refus)
        return 1
    index_auto = index_auto_valide()
    mission = prochaine_du_lot(file_missions)
    if mission_forcee is not None:
        # EO-185 : une mission CONDUITE et NOMMEE (verbe `conduire`) passe AVANT
        # le lot arme -- c'est le SEUL chemin qui manquait pour conduire une
        # mission chargee HORS lot sans consommer un creneau de la chaine. Le
        # 2026-09-19, MO-200 est restee un FANTOME faute de ce chemin : `fin` a
        # clos MO-190, la mission courante du lot.
        mission = next((m for m in file_missions.get("missions", [])
                        if m.get("id") == mission_forcee), None)
        if mission is None:
            print("REFUS : mission inconnue : " + mission_forcee)
            return 2
        if mission.get("statut") != STATUT_EN_ATTENTE:
            print("REFUS : " + mission_forcee + " n'est pas en attente (statut : "
                  + str(mission.get("statut")) + ").")
            return 2
    if mission is None:
        # UN SEUL CANDIDAT, JUGE AVANT D ETRE TIRE (decision createur 2026-09-18) :
        # l auto-validee en TETE du brin passe avant la file chargee, et RIEN n est
        # consomme tant que la chaine a le droit d enchainer. Un STOP laisse donc
        # l etat EXACTEMENT comme il etait (la tete reste en tete).
        tete = tete_brin()
        auto_en_tete = tete is not None and est_auto_validee(tete, index_auto)
        en_file = None if auto_en_tete else prochaine_en_attente(file_missions)
        if auto_en_tete or en_file is None:
            candidat, origine = tete, "brin"
        else:
            candidat, origine = en_file, "file"
        # Aucun lot ici (la branche lot est sortie plus haut) : depuis_lot=False.
        arret, motif = decision_enchainement(candidat, False, enchainer, index_auto)
        if arret:
            print("STOP ENCHAINEMENT : " + motif)
            print("(RIEN n a ete consomme -- "
                  + ("la tete du brin reste EN PLACE" if origine == "brin"
                     else "la mission reste dans sa file") + " ;")
            print(" injection explicite : python main.py injecter)")
            return 0
        if candidat is not None:
            mission = puiser_tresse(file_missions) if origine == "brin" else candidat
    if mission is None:
        print("Aucune mission en attente (lot, file et tresse vides).")
        return 0
    code, message = defcon_bloque_theme(mission.get("theme", ""))
    if code != 0:
        print(message)
        print("(mission " + mission["id"] + " laissee en attente pendant la mise en securite)")
        return code
    code, checklist = garder_theme_et_checklist(mission)
    if code != 0:
        return code
    role = charger_role_mission(mission)
    if role.get("refus"):
        print("REFUS : la mission " + mission["id"] + " n'a pas de ROLE injectable (posture hors vivier).")
        for ecart in role.get("ecarts", []):
            print("  " + ecart)
        return 2
    for ecart in role.get("ecarts", []):
        print("ALERTE : " + ecart)
    # AUTO-VALIDATION (EO-143) : le champ est pose AVANT l injection -- l agent
    # doit le LIRE, il ne le devine pas (un champ que personne ne lit est une
    # absence, et c est exactement l ecart mesure par MO-160).
    declarer_auto_validation(mission)
    injection = {
        "type": "injection",
        "date": horodater(),
        "mission": mission["id"],
        "theme": mission["theme"],
        "role": role,
        # LE PERSONNAGE (MO-539) : servi a CHAQUE injection, jamais conditionnel.
        # Il passe AVANT l objectif dans la fiche technique : c est le cadre
        # dans lequel l objectif sera traite.
        CHAMP_ROLE_AGENT: charger_role_agent(),
        "objectif": mission["objectif"],
        CHAMP_AUTO_VALIDATION: mission[CHAMP_AUTO_VALIDATION],
        "checklist": checklist,
        "modes_emploi": charger_modes_emploi(mission),
        CHAMP_SI_J_ETAIS_USER: charger_si_j_etais_user(mission),
        CHAMP_PROFIL: charger_profil_utile(),
        "lecons_utiles": charger_lecons_utiles(mission),
        "themes_utiles": charger_themes_utiles(),
        "recherche": preparer_recherche_mission(mission),
        # MO-318 : le contrat de continuite est servi des qu une SUITE existe -- et
        # pas seulement dans un lot arme, ou il n atteignait jamais l agent.
        # MO-451 : quand la CLOTURE sert ce round (`enchainer`), l injection porte
        # EN PLUS le RAPPEL ROUND SERVI -- le round a ete servi et pris par la
        # machine, il se conduit dans le MEME tour (retour createur 2026-09-24).
        # MUET hors chaine : un rappel toujours present ne se lit plus.
        CHAMP_RAPPEL: (charger_rappel_route(
            mission, suite_auto_a_conduire(file_missions, index_auto,
                                          mission.get("id", "")))
            + ((" " + RAPPEL_ROUND_SERVI) if enchainer else "")).strip(),
    }
    injection["poids_tokens"] = poids_injection(injection)
    deposer_message(BOITE_PILOTE_OUT, injection)

    mission["statut"] = STATUT_EN_COURS
    mission["injectee_le"] = horodater()
    mission["checklist"] = checklist
    enregistrer_file(file_missions)
    annoncer_debut(file_missions, mission)
    # Suivi-optimus (MO-108) : le pilote DECLARE la borne de debut, en mode
    # `--si-absent oui` -- la porte n'ecrit QUE si l'evenement manque, donc le
    # doublon MO-030 (2e debut fabrique par l'appel automatique d'autrefois) est
    # impossible PAR CONSTRUCTION. Motif mesure le 2026-09-15 : MO-105 et MO-106
    # ont ete closes SANS fin au marbre parce que la declaration reposait sur la
    # MEMOIRE de l'agent. L'agent garde le droit de declarer lui-meme.
    declarer_borne_marbre(
        mission,
        "debut",
        "debut declare par le pilote (injection) : " + resume_mission(mission),
        portes=["pilote:injecter"],
    )
    # La VUE derivee est elle aussi rafraichie par le pilote : DEBUT.
    rafraichir_vue_suivi()
    print("Injection deposee pour " + mission["id"] + " -> " + str(BOITE_PILOTE_OUT))
    # MO-394 (EO-381) : ce qui vient d etre DEPOSE est AUSSI IMPRIME, TOUS les champs.
    # Sans cet appel, `injecter` et `conduire` servaient un round SANS ORDRES a l ecran
    # (mesure du 2026-09-23 : la seule remise vivait dans la cloture). La remise garde
    # UN domicile (remettre_les_ordres) et gagne DEUX chemins.
    from fin.fonctions import remettre_les_ordres
    remettre_les_ordres(charger_file)
    return 0


def conduire(charger_file, identifiant):
    """CONDUIT une mission chargee HORS lot : elle devient COURANTE et injectee.

    EO-185 (2026-09-19). Mesure : `injecter` et `fin` operent sur la mission
    COURANTE, et `preparer_injection` priorise TOUJOURS le lot arme -- une mission
    chargee hors lot ne pouvait donc JAMAIS etre conduite. Ce jour-la, MO-200
    (chargee pour EO-184) est restee un FANTOME, et `fin` a clos MO-190, la
    mission courante DU LOT : une demande du createur n'avait aucun chemin
    conforme, d'ou trois missions menees HORS FILE le meme jour.

    Refus NOMMES : une mission est deja en cours (parquer d'abord, `reporter`) ;
    identifiant inconnu ; mission pas en attente ; mission du LOT arme (la chaine
    a son propre chemin : `injecter`) -- `conduire` est fait pour le HORS lot.
    """
    file_missions = charger_file()
    # MO-341 : le meme refus que partout ailleurs, servi par son DOMICILE -- il
    # nommait deja la mission et le remede `reporter`, mais c etait une QUATRIEME
    # forme de la meme regle.
    refus = refus_serie_stricte(file_missions)
    if refus:
        print(refus)
        return 1
    mission = next((m for m in file_missions.get("missions", [])
                    if m.get("id") == identifiant), None)
    if mission is None:
        print("REFUS : mission inconnue : " + identifiant)
        return 2
    if mission.get("statut") != STATUT_EN_ATTENTE:
        print("REFUS : " + identifiant + " n'est pas en attente (statut : "
              + str(mission.get("statut")) + ").")
        return 2
    if identifiant in ids_en_lot(file_missions):
        print("REFUS : " + identifiant + " appartient au lot arme -- la chaine a son"
              " propre chemin (python main.py injecter). `conduire` est pour une"
              " mission HORS lot.")
        return 2
    return preparer_injection(charger_file, mission_forcee=identifiant)


def enchainer(charger_file):
    """Arme le round multiple : la premiere mission du lot passe en cours.

    Ensuite, chaque `fin` declenche automatiquement la mission suivante du lot
    (annonce FIN puis DEBUT), jusqu'au RETOUR consolide a la Matrice quand
    toutes les missions du lot sont terminees.
    Protocole de pause (M-080) : REFUS si la session-matrix est EN PAUSE.
    """
    if session_en_pause():
        print("REFUS : session-matrix EN PAUSE (protocole M-080) -- aucun enchainement pendant la maintenance.")
        return 1
    file_missions = charger_file()
    refus = refus_serie_stricte(file_missions)
    if refus:
        print(refus)
        return 1
    if not ids_en_lot(file_missions):
        print('Aucun lot arme. Chargez-en un : python main.py lot --lot "nom" --theme "t1,t2" --objectif "o1|o2"')
        return 1
    mission = prochaine_du_lot(file_missions)
    if mission is None:
        print("Le lot est deja termine (aucune mission en attente dans le lot).")
        return 0
    # Meme garde que l'injection simple : le chemin du LOT ne doit pas etre une
    # porte derobee (mise en securite defcon + champ ferme des themes).
    code, message = defcon_bloque_theme(mission.get("theme", ""))
    if code != 0:
        print(message)
        print("(mission " + mission["id"] + " laissee en attente pendant la mise en securite)")
        return code
    code, checklist = garder_theme_et_checklist(mission)
    if code != 0:
        return code
    role = charger_role_mission(mission)
    if role.get("refus"):
        print("REFUS : la mission " + mission["id"] + " n'a pas de ROLE injectable (posture hors vivier).")
        for ecart in role.get("ecarts", []):
            print("  " + ecart)
        return 2
    for ecart in role.get("ecarts", []):
        print("ALERTE : " + ecart)
    # Meme champ sur le chemin du LOT : le lot n est pas une porte derobee
    # (meme garde, meme declararation -- une seule fonction pour les deux).
    declarer_auto_validation(mission)
    injection = {
        "type": "injection",
        "date": horodater(),
        "mission": mission["id"],
        "theme": mission["theme"],
        "role": role,
        "objectif": mission["objectif"],
        "lot": True,
        CHAMP_AUTO_VALIDATION: mission[CHAMP_AUTO_VALIDATION],
        "checklist": checklist,
        CHAMP_PROFIL: charger_profil_utile(),
        "lecons_utiles": charger_lecons_utiles(mission),
        "themes_utiles": charger_themes_utiles(),
        "recherche": preparer_recherche_mission(mission),
        CHAMP_RAPPEL: charger_rappel_route(mission),
    }
    injection["poids_tokens"] = poids_injection(injection)
    deposer_message(BOITE_PILOTE_OUT, injection)

    mission["statut"] = STATUT_EN_COURS
    mission["checklist"] = checklist
    mission["injectee_le"] = horodater()
    enregistrer_file(file_missions)
    annoncer_debut(file_missions, mission)
    # Meme borne de debut que l'injection simple (MO-108, mode --si-absent oui).
    declarer_borne_marbre(
        mission,
        "debut",
        "debut declare par le pilote (chaine armee) : " + resume_mission(mission),
        portes=["pilote:injecter"],
    )
    rafraichir_vue_suivi()
    from fin.fonctions import remettre_les_ordres
    remettre_les_ordres(charger_file)
    print("Chaine armee : chaque 'fin' enchainra la mission suivante du lot.")
    return 0


# Le VOCABULAIRE interdit vit dans son DOMICILE (data/commun/vocabulaire_invisible.py)
# depuis MO-153 : les DEUX pilotes et le moteur de recherche le CONSOMMENT, ils ne
# le recopient plus (M-076 ; L-100/L-102 : trois listes recopiees, trois longueurs).
from vocabulaire_invisible import MOTS_INTERDITS  # noqa: E402


def filtrer_pour_cameleon(items):
    """Filtre L-016/invisibilite : retire tout item lisible par le cameleon qui nomme l'invisible.

    Meme contrat que le pilote du Flux 1 : le vocabulaire vient du DOMICILE
    data/commun/vocabulaire_invisible.py -- deux copies divergeraient (MO-153).
    """
    interdits = MOTS_INTERDITS
    filtres = []
    for it in items:
        texte = " ".join([
            it.get("lecon", ""),
            it.get("but", ""),
            it.get("description", ""),
            it.get("nom", ""),
            " ".join(it.get("tags", [])),
            it.get("source", ""),
        ]).lower()
        if any(m in texte for m in interdits):
            continue
        filtres.append(it)
    return filtres


def charger_role_mission(mission):
    """Le ROLE de la mission, remis AVANT la mission (MAILLON 2/5, 2026-09-14).

    Le cameleon recoit UNE personnalite par mission (categorie PERSONNALITE du
    vivier) ; Optimus n'en recevait AUCUNE : ses missions n'avaient qu'un theme de
    chantier. Le role porte donc les DEUX, et chacun est NOMME :
      - `posture` : QUI conduit (PERSONNALITE deduite du TYPE par la table fermee
        du pilote, `personnalites.py`) -- jamais choisie par l'agent ;
      - `theme` : le chantier FERME de la mission (le QUOI toucher).
    Chaque nom est accompagne de son ITEM DU VIVIER (but + description) : le
    pilote fournit la CONDUITE au debut de la mission, jamais la fiche entiere.
    L'ecart (type absent, posture hors vivier) est DEPOSE dans le role : il est
    vu par l'agent au debut de sa mission, pas seulement dans un journal.
    """
    code, role, ecarts = role_de_mission(mission)
    role["posture_declaree"] = item_du_vivier(role.get("posture", "")) or {}
    role["chantier_declare"] = item_du_vivier(role.get("theme", "")) or {}
    role["ecarts"] = ecarts
    role["refus"] = code != 0
    return role


def preparer_recherche_mission(mission):
    """La QUESTION a poser au moteur, habillee de la commande de CE flux (EO-131).

    Le module PARTAGE (`data/commun/recherche_mission.py`) derive la question du
    sujet de la mission ; ICI on l'habille du chemin et des options du Flux 2 --
    dont `--prive`, qui ouvre la zone de l'operateur. Le cameleon consomme le
    MEME module avec SON gabarit : une seule derivation, deux habillages.

    Absent, le module ne fait pas mourir l'injection : le bloc porte un
    avertissement NOMME, et c'est le garde BLOQUANT (maillon 24) qui refuse.
    """
    if preparer_recherche is None:
        return {
            "quand": "module partage ABSENT",
            "question": "",
            "commande": "",
            "avertissement": ("recherche_mission.py introuvable dans data/commun : "
                              "la question de recherche n'est PAS injectee"),
        }
    return preparer_recherche(mission, GABARIT_COMMANDE_RECHERCHE)


def charger_rappel_route(mission, suite=""):
    """La ROUTE du defaut d'OUTIL, portee par le sac-a-dos de la mission (R5).

    Mesure de l'audit MO-174 : la regle que le createur venait d'enoncer (reparer
    DANS l'outil, jamais contourner a la main) n'etait ecrite NULLE PART ou
    l'agent la cherche -- c'est-a-dire AU MOMENT ou il en a besoin. Elle voyage
    donc AVEC la mission dont le TYPE est `reparation` : le type que declarent le
    crochet `[outil]` (filtrer/entry.py) et la liste fermee TYPES.

    Tout autre type rend une chaine VIDE, et c'est voulu : un rappel toujours
    present ne se lit plus. Le champ est PESE avec les autres (CHAMPS_PESES) --
    c'est du contexte offert a l'agent, il se compte comme le reste.
    """
    morceaux = []
    # CHAINE (EO-274, generalise MO-318) : le contrat DIT qu une suite existe -- soit
    # parce que la mission est dans un LOT arme, soit parce que la file ou le brin en
    # porte une AUTO-VALIDEE (`suite`). Aucune des deux : le rappel se tait (un rappel
    # permanent ne se lit plus), et c est le CONTRE-TEMOIN que MO-318 exige.
    if mission.get("lot") or suite:
        morceaux.append(RAPPEL_CHAINE)
    if str(mission.get("type", "") or "").strip() == TYPE_ROUTE_OUTIL:
        morceaux.append(RAPPEL_ROUTE_OUTIL)
    return " ".join(morceaux)


# PLAFOND DU SAC-A-DOS (EO-270) : la commande de travail pese 750 tokens ; le
# savoir injecte d office en pesait 23378, soit 89 pour cent de l injection
# (mesure MO-241). Le poids d une injection a ete multiplie par 5.4 en six jours
# (4865 tokens le 2026-09-13 contre 26295 le 2026-09-19) : le contexte d une
# session se remplissait donc en un a trois rounds, et la chaine k/n s arretait
# faute de place. Le sac-a-dos est desormais BORNE : les lecons PERTINENTES pour
# la mission d abord, puis les plus RECENTES, jusqu au plafond. Les ecartees ne
# sont PAS perdues : elles restent dans matrice/data/lecons.json et leur nombre
# est DIT a chaque injection (un reste tu redevient une absence).
PLAFOND_LEGONS_TOKENS = 6000
PLAFOND_LEGONS_NOMBRE = 30
FACTEUR_ESTIMATION = 4  # repli (caracteres -> tokens) si le motif tokens manque


def _vocabulaire_mission(mission):
    """Mots de la mission qui decident de la PERTINENCE d une lecon."""
    if not isinstance(mission, dict):
        return set()
    morceaux = [str(mission.get("theme", "")), str(mission.get("type", "")),
                str(mission.get("source", ""))]
    role = mission.get("role")
    if isinstance(role, dict):
        for cle in ("id", "nom", "theme", "but"):
            morceaux.append(str(role.get(cle, "")))
    elif role:
        morceaux.append(str(role))
    morceaux.append(str(mission.get("objectif", "")))
    mots = set()
    for morceau in morceaux:
        for mot in re.split(r"[^0-9A-Za-z_]+", morceau.lower()):
            if len(mot) >= 4:
                mots.add(mot)
    return mots


def _score_lecon(lecon, vocabulaire):
    """Nombre de tags de la lecon presents dans le vocabulaire de la mission."""
    tags = lecon.get("tags") or []
    if not isinstance(tags, list):
        return 0
    score = 0
    for tag in tags:
        if str(tag).lower() in vocabulaire:
            score += 1
    return score


def _poids_texte(texte):
    """Poids d un texte, ET l'INSTRUMENT qui l'a mesure (jamais un 0 muet).

    Le peseur vit au DOMICILE partage (matrice/data/commun/tokens.py, M-076) ;
    absent, le repli (FACTEUR_ESTIMATION) est DECLARE et son nom VOYAGE avec la
    mesure : une mesure dont on ne sait pas qui l'a faite ne se relit pas. Ce
    helper est le SEUL endroit du module ou la formule de repli est ecrite (L-029).
    """
    if peser_tokens is None:
        return (max(1, len(texte) // FACTEUR_ESTIMATION),
                "repli caracteres/" + str(FACTEUR_ESTIMATION))
    return peser_tokens(texte), "domicile tokens.py"


def _poids_lecon(lecon):
    """Poids d une lecon (motif partage si present, repli declare sinon).

    Consomme `_poids_texte` : une seule formule de repli dans le module.
    """
    return _poids_texte(json.dumps(lecon, ensure_ascii=True))[0]


def selectionner_lecons(lecons, mission=None, plafond_tokens=None, plafond_nombre=None):
    """LE PLAFOND (EO-270) : rend (retenues, ecartees), ordre stable et dicte.

    Ordre : pertinence (tags de la lecon presents dans la mission) d abord, puis
    recence (date, puis id) -- deux passes ne prennent donc jamais une autre
    suite. Un plafond atteint ECARTE la suite sans la perdre : l appelant la DIT.
    La premiere lecon passe toujours, meme plus lourde que le plafond : un
    plafond qui viderait le sac-a-dos serait pire que pas de plafond.
    """
    if plafond_tokens is None:
        plafond_tokens = PLAFOND_LEGONS_TOKENS
    if plafond_nombre is None:
        plafond_nombre = PLAFOND_LEGONS_NOMBRE
    vocabulaire = _vocabulaire_mission(mission)
    classees = sorted(lecons, key=lambda l: (str(l.get("date", "")), str(l.get("id", ""))),
                      reverse=True)
    classees.sort(key=lambda l: -_score_lecon(l, vocabulaire))
    retenues = []
    ecartees = []
    poids = 0
    for lecon in classees:
        cout = _poids_lecon(lecon)
        if retenues and (len(retenues) >= plafond_nombre or poids + cout > plafond_tokens):
            ecartees.append(lecon)
            continue
        retenues.append(lecon)
        poids += cout
    return retenues, ecartees


def charger_lecons_utiles(mission=None):
    """Charge les lecons de la BDD lecons.json, BORNEES par le plafond (EO-270).

    BDD en cours de construction : jamais de faux blocage, jamais de type surprenant.
    Format prevu (contrat data) : {"lecons": [{...tags...}, ...]}.
    Filtre L-016 : les lecons qui nomment l invisible sont retirees de l injection
    (le cameleon ne doit jamais lire _operateur/optimus/suivi-optimus -- audit-invisibilite).
    Le plafond ne bloque rien : il selectionne, et il DIT combien il ecarte.
    """
    chemin_lecons = REPERTOIRE_DATA / "lecons.json"
    if not chemin_lecons.exists():
        return []
    try:
        with open(chemin_lecons, "r", encoding=ENCODAGE) as flux:
            donnees = json.load(flux)
        lecons = donnees.get("lecons", []) if isinstance(donnees, dict) else []
        lecons = filtrer_pour_cameleon(lecons)
    except (OSError, ValueError):
        return []
    retenues, ecartees = selectionner_lecons(lecons, mission)
    if ecartees:
        print("lecons_utiles : " + str(len(retenues)) + " injectees / " + str(len(ecartees))
              + " ecartees (plafond " + str(PLAFOND_LEGONS_TOKENS) + " tokens, EO-270)"
              + " -- pertinentes d abord puis recentes ; les ecartees restent lisibles"
              + " dans matrice/data/lecons.json.")
    return retenues


def charger_themes_utiles():
    """Charge les themes du registre vivier-themes.json (liste vide si absent).

    Meme doctrine que lecons_utiles : garde jamais bloquant, type toujours sur.
    Format (moule theme-bdd) : {"themes": [{"id", "nom", "but", ...}, ...]}.
    Filtre L-016 : un theme qui nommerait l'invisible est retire (meme regle que lecons).
    """
    if not CHEMIN_THEMES.exists():
        return []
    try:
        with open(CHEMIN_THEMES, "r", encoding=ENCODAGE) as flux:
            donnees = json.load(flux)
        themes = donnees.get("themes", []) if isinstance(donnees, dict) else []
        return filtrer_pour_cameleon(themes)
    except (OSError, ValueError):
        return []


def charger_profil_utile(chemin=None, plafond_tokens=None):
    """Le PROFIL DE L'UTILISATEUR dans le sac-a-dos (demande createur, 2026-09-21).

    POURQUOI (mesure du jour) : la fiche `matrix/USER-PROFIL.md` etait remplie
    avec le createur, mais AUCUN agent ne la lisait. Le pilote ne l'ouvrait qu'au
    DEMARRAGE (`injection/cycle.py`), pour tester si la ligne `**Pseudo**` etait
    remplie, puis jetait le contenu : les 8 champs (style, interets, niveau
    technique...) n'atteignaient donc aucune mission -- alors que la fiche annonce
    elle-meme etre lue par Optimus et le cameleon. Un profil qui n'arrive pas
    jusqu'a la mission ne personnalise rien : il voyage donc AVEC la mission,
    comme la posture et la question de recherche.

    QUELLE MATIERE (jamais la fiche entiere) : les champs ATTENDUS remplis, dans
    l'ordre declare par le MOTIF PARTAGE (`CHAMPS_ATTENDUS`) -- frontmatter, intro
    et tableaux optionnels ne sont pas du contexte utile. Les champs attendus
    VIDES sont DITS (`a_remplir`) : l'agent voit ce qui manque, donc il peut
    guider le remplissage (`python main.py profil --guider`).

    BORNE (`PLAFOND_PROFIL_TOKENS`) : la fiche est ouverte a l'ecriture manuelle ;
    une valeur collee ferait grossir CHAQUE injection, a chaque mission. Les
    champs sont donc additionnes DANS L'ORDRE du motif et la suite est ECARTEE ET
    DITE (`ecartes_par_plafond`) -- un plafond muet se lirait comme un profil
    complet. Le PREMIER champ passe toujours, meme plus lourd que le plafond :
    un plafond qui viderait le bloc serait pire que pas de plafond (meme regle
    que les lecons, EO-270).

    AUCUN SILENCE : fiche absente, illisible ou sans ligne de tableau -> un
    AVERTISSEMENT NOMME dans le bloc, jamais un bloc vide (un bloc vide se
    lirait comme "profil complet" alors que rien n'a ete lu).

    `chemin` et `plafond_tokens` sont INJECTABLES (repli sur la fiche reelle et
    sur la constante du pilote) : le cobaye du garde eprouve donc la borne sur une
    fiche obese, sans jamais toucher a la vraie fiche.
    """
    if plafond_tokens is None:
        plafond_tokens = PLAFOND_PROFIL_TOKENS
    if motif_profil is None:
        return {
            "present": False,
            "champs": {},
            "a_remplir": [],
            "ecartes_par_plafond": [],
            "avertissement": ("motif partage ABSENT (matrice/data/commun/fiche_profil.py) : "
                              "le profil n'est PAS lu, donc pas injecte -- a reparer"),
        }
    chemin = Path(chemin) if chemin is not None else motif_profil.chemin_profil(REPERTOIRE_PILOTE)
    if not chemin.is_file():
        return {
            "source": str(chemin),
            "present": False,
            "champs": {},
            "a_remplir": list(motif_profil.CHAMPS_ATTENDUS),
            "ecartes_par_plafond": [],
            "avertissement": ("fiche " + chemin.name + " ABSENTE : aucun profil injecte -- "
                              "la remplir avec l'utilisateur (python main.py profil --guider)"),
        }
    valeurs = motif_profil.lire_valeurs(chemin)
    if not valeurs:
        return {
            "source": str(chemin),
            "present": False,
            "champs": {},
            "a_remplir": list(motif_profil.CHAMPS_ATTENDUS),
            "ecartes_par_plafond": [],
            "avertissement": ("fiche " + chemin.name + " PRESENTE mais SANS champ lisible "
                              "(illisible, ou aucune ligne de tableau) : aucun profil injecte"),
        }
    champs = {}
    a_remplir = []
    ecartes = []
    poids = 0
    instrument = ""
    for libelle in motif_profil.CHAMPS_ATTENDUS:
        valeur = str(valeurs.get(libelle, "")).strip()
        if not valeur:
            a_remplir.append(libelle)
            continue
        cout, instrument = _poids_texte(valeur)
        if champs and poids + cout > plafond_tokens:
            ecartes.append(libelle)
            continue
        champs[libelle] = valeur
        poids += cout
    if ecartes:
        print("profil : " + str(len(ecartes)) + " champ(s) ecarte(s) par le plafond ("
              + str(plafond_tokens) + " tokens) -- " + ", ".join(ecartes)
              + " ; la fiche reste lisible : " + str(chemin))
    return {
        "source": str(chemin),
        "present": True,
        "complet": not a_remplir,
        "champs": champs,
        "a_remplir": a_remplir,
        "ecartes_par_plafond": ecartes,
        "poids_champs_tokens": poids,
        "mesure": instrument,
    }
