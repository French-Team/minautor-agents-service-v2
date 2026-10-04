'''SERVICE DU PLANNING : ALLUMER, RECEVOIR, TRANSFORMER (MO-429).

Trois gestes, et rien d autre (demande createur du 2026-09-24) :
  1. ALLUMER individuellement la routine DUE (mode passe) -- sa commande vient
     du PLANNING, jamais d une table recopiee ;
  2. RECEVOIR son resultat -- code retour, trace du lancement (motif partage
     data/commun/lancement.py), et la passe PUBLIEE relue apres coup ;
  3. TRANSFORMER un ecart en MESSAGE par la PORTE UNIQUE signaler, niveau
     DECLARE (vie/constants), plus une montee defcon sur le CRITIQUE (D4b).

Ce module ne DETIENT ni cadence ni mode : il les LIT au planning
(data/commun/planning_routines.py), et le temoin de passe est lu CHEZ la
routine (TEMOIN_CADENCE, MO-479). Une seule verite par chose.
'''
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from constants import (
    ANTI_SPAM_SERVICE_SECONDES,
    BOUCLES,
    CAUSE_TRACEBACK,
    CHEMIN_ETAT_SERVICE,
    CHEMIN_OUTIL_DEFCON,
    CHEMIN_OUTIL_SIGNALER,
    DRAPEAU_PAR_NOM,
    ENCODAGE,
    EXPEDITEUR_SIGNAL,
    FORMAT_HORODATAGE,
    MAX_ALLUMAGES_PAR_TOUR,
    NIVEAU_DEFCON_CRITIQUE,
    NIVEAU_ECHEC,
    NIVEAU_PLANTAGE,
    NIVEAU_RETARD,
    NOM_ETAT_SERVICE,
    PLAFOND_PASSE_SECONDES,
    REPERTOIRE_MATRIX,
    SUFFIXE_TMP_SERVICE,
)
from battement import instants, lire_anneau  # noqa: E402  (data/commun via constants)
from planning_routines import (  # noqa: E402
    PlanningIllisible,
    cadence_planning,
    commande_passe,
    decalage,
    entrees,
    tolerance,
)

# Motifs partages (M-076) : le service ne refait AUCUN de ces gestes.
from lancement import chemin_journal_lancement, drapeaux_popen  # noqa: E402


# ---------------------------------------------------------------------------
# HORODATAGES (format unique, declare en constants)
# ---------------------------------------------------------------------------
def maintenant():
    '''L instant courant BORNE au format unique (les etats lisent la meme chose).'''
    return datetime.strptime(datetime.now().strftime(FORMAT_HORODATAGE), FORMAT_HORODATAGE)


def instant(texte):
    '''Un horodatage lisible, ou None (un texte casse ne fait jamais tomber le service).'''
    if not texte:
        return None
    try:
        return datetime.strptime(str(texte), FORMAT_HORODATAGE)
    except (TypeError, ValueError):
        return None


def horodatage(moment):
    return moment.strftime(FORMAT_HORODATAGE)


# ---------------------------------------------------------------------------
# ETAT DU SERVICE (ecriture atomique, forme d etat de routine)
# ---------------------------------------------------------------------------
def chemin_etat(racine=None):
    '''Ou vit l etat du service : CHEZ LE SERVICE en mode reel, et dans
    L ARBRE DU COBAYE quand une racine est donnee (un cobaye ne partage
    jamais l etat du systeme reel).'''
    if racine is None:
        return CHEMIN_ETAT_SERVICE
    return Path(racine) / 'matrice' / 'routines' / 'vie' / NOM_ETAT_SERVICE


def charger_etat(racine=None):
    try:
        donnees = json.loads(chemin_etat(racine).read_text(encoding=ENCODAGE))
    except (OSError, ValueError):
        donnees = {}
    if not isinstance(donnees, dict):
        donnees = {}
    if not isinstance(donnees.get('routines'), dict):
        donnees['routines'] = {}
    return donnees


def ecrire_etat(etat, racine=None):
    '''Etat ATOMIQUE : tmp puis remplacement (checklist MO-429), fins de ligne LF.'''
    cible_etat = chemin_etat(racine)
    cible = Path(str(cible_etat) + SUFFIXE_TMP_SERVICE)
    texte = json.dumps(etat, ensure_ascii=True, indent=2) + '\n'
    try:
        cible.write_text(texte, encoding=ENCODAGE, newline='\n')
        cible.replace(cible_etat)
        return True
    except OSError:
        return False


# ---------------------------------------------------------------------------
# OU VIT UNE ROUTINE, ET CE QU ELLE PUBLIE
# ---------------------------------------------------------------------------
def dossier_de_routine(nom, racine=None):
    '''Le dossier d une routine : la TABLE DECLAREE en mode reel, le chemin du
    cobaye quand une racine est donnee (un cobaye ne se devine jamais).'''
    if racine is None:
        for nom_table, chemin in BOUCLES:
            if nom_table == nom:
                return chemin
        raise PlanningIllisible(
            'routine ' + nom + ' au planning mais ABSENTE de la table des '
            + 'routines (vie/constants.py)'
        )
    return Path(racine) / 'matrice' / 'routines' / nom


def temoin_de(dossier):
    '''(genre, fichier, cle) lus CHEZ la routine (TEMOIN_CADENCE, MO-479).

    Le module est charge sous un nom UNIQUE : six fichiers s appellent
    constants.py, les importer sous leur nom se mascheraient (L-029).
    '''
    import importlib.util

    chemin = dossier / 'constants.py'
    if not chemin.is_file():
        return None
    nom_module = 'temoin_' + dossier.name.replace('-', '_')
    try:
        specification = importlib.util.spec_from_file_location(nom_module, str(chemin))
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
    except Exception:
        return None
    temoin = getattr(module, 'TEMOIN_CADENCE', None)
    if (not isinstance(temoin, (tuple, list)) or len(temoin) != 3):
        return None
    return tuple(temoin)


def derniere_passe(dossier):
    '''(instant de la DERNIERE passe publiee, source) -- (None, source) si muet.

    On LIT ce que la routine a publie (anneau de passes ou journal borne) :
    une passe qui n a rien publie n a pas existe pour l observateur, et c est
    exactement ce que le service doit pouvoir dire.
    '''
    temoin = temoin_de(dossier)
    if temoin is None:
        return None, 'aucun TEMOIN_CADENCE lisible chez la routine'
    genre, fichier, cle = temoin
    chemin = dossier / fichier
    if genre == 'anneau':
        moments = instants(lire_anneau(chemin, cle), FORMAT_HORODATAGE)
        return (moments[-1] if moments else None), ('etat ' + fichier)
    if genre == 'journal':
        from rotation_journal import lire_queue_journal, octets_queue_du_journal

        try:
            lignes = lire_queue_journal(chemin, octets_queue_du_journal(chemin))
        except OSError:
            lignes = []
        for ligne in reversed(lignes):
            try:
                donnees = json.loads(ligne)
            except ValueError:
                continue
            if str(donnees.get('type')) != str(cle):
                continue
            moment = instant(donnees.get('date'))
            if moment is not None:
                return moment, ('journal ' + fichier)
        return None, ('journal ' + fichier)
    return None, 'genre de temoin inconnu (' + str(genre) + ')'



# ---------------------------------------------------------------------------
# TRANSFORMATION : un ecart devient un MESSAGE (porte unique signaler)
# ---------------------------------------------------------------------------
def outil_de(nom_outil, racine=None):
    '''Le chemin d un outil : celui de la RACINE donnee (le cobaye a les siens),
    sinon celui du vrai matrix -- jamais un chemin recopie a la main.'''
    base = Path(racine) if racine else REPERTOIRE_MATRIX
    return base / 'matrice' / 'data' / 'outils' / nom_outil / 'main.py'


def signaler(niveau, cible, description, erreur=None, racine=None):
    '''Depose le message par la PORTE UNIQUE signaler. Rend (code, sortie).'''
    commande = [
        sys.executable, str(outil_de('signaler', racine)), 'signaler',
        '--outil', cible, '--niveau', niveau, '--description', description,
        '--expediteur', EXPEDITEUR_SIGNAL,
    ]
    if erreur:
        commande += ['--erreur', str(erreur)]
    try:
        resultat = subprocess.run(
            commande, capture_output=True, text=True, timeout=30, **drapeaux_popen()
        )
    except (OSError, subprocess.SubprocessError) as echec:
        return 1, 'porte signaler injoignable : ' + str(echec)
    return resultat.returncode, ((resultat.stdout or resultat.stderr) or '').strip()


def monter_defcon(raison, racine=None):
    '''Montee defcon par la PORTE machine-defcon monter (decision D4b).

    Jamais une ecriture directe : la porte journalise chaque transition, c est
    elle qui dit QUI a monte et POURQUOI. Niveau DECLARE en constants.
    '''
    commande = [
        sys.executable, str(outil_de('machine-defcon', racine)), 'monter',
        '--niveau', str(NIVEAU_DEFCON_CRITIQUE), '--raison', raison,
    ]
    try:
        resultat = subprocess.run(
            commande, capture_output=True, text=True, timeout=30, **drapeaux_popen()
        )
    except (OSError, subprocess.SubprocessError) as echec:
        return 1, 'porte machine-defcon injoignable : ' + str(echec)
    return resultat.returncode, ((resultat.stdout or resultat.stderr) or '').strip()


def ecrire_trace_lancement(dossier, texte):
    '''La sortie du fils va dans le JOURNAL DE LANCEMENT de la routine (motif
    partage EO-409) : c est la que se lit la CAUSE d un plantage.'''
    try:
        with open(str(chemin_journal_lancement(dossier)), 'w', encoding=ENCODAGE) as flux:
            flux.write(texte + '\n' if texte and not texte.endswith('\n') else texte)
        return True
    except OSError:
        return False


def depot_frais(anti_spam, motif):
    '''True si ce MOTIF n a pas ete signale depuis le plancher declare.

    Le meme probleme n a pas le droit de crier a chaque tour : le plancher est
    en secondes MURALES (il ne depend jamais du nombre de tours) -- lecon
    L-062. Un depot refuse n est jamais silencieux : le motif reste ecrit dans
    l etat du service et le service le DIT.
    '''
    if anti_spam.get('motif') != motif:
        return True
    date = instant(anti_spam.get('date'))
    if date is None:
        return True
    return (maintenant() - date).total_seconds() >= ANTI_SPAM_SERVICE_SECONDES


def signaler_si_frais(courant, niveau, motif, nom, racine, messages, erreur=None):
    '''Depose le message SI le plancher l autorise. Rend True si depose.'''
    if not depot_frais(courant.get('anti_spam') or {}, motif):
        messages.append(
            nom + ' : signal DEJA emis (plancher ' + str(ANTI_SPAM_SERVICE_SECONDES)
            + ' s pour ' + motif + ')'
        )
        return False
    description = 'Service du planning : ' + nom + ' -- ' + motif
    code, sortie = signaler(niveau, nom, description, erreur=erreur, racine=racine)
    courant['anti_spam'] = {
        'motif': motif, 'date': horodatage(maintenant()), 'niveau': niveau, 'code': code,
    }
    messages.append(nom + ' : MESSAGE ' + niveau + ' depose (' + sortie[:150] + ')')
    if niveau == NIVEAU_PLANTAGE:
        code_defcon, sortie_defcon = monter_defcon(description, racine=racine)
        messages.append(
            nom + ' : defcon ' + str(NIVEAU_DEFCON_CRITIQUE) + ' (code '
            + str(code_defcon) + ') ' + sortie_defcon[:100]
        )
    return True


# ---------------------------------------------------------------------------
# ALLUMAGE : la routine DUE tourne UNE fois, puis rend la main
# ---------------------------------------------------------------------------
def allumer(entree, dossier, racine=None):
    '''Allume la routine EN PASSE et RECOIT son resultat.

    Le resultat est RECU a trois sources : le code retour du fils, sa sortie
    (journalisee au motif partage), et la passe PUBLIEE relue apres coup. Un
    des trois qui ne va pas = un ecart, avec son niveau DECLARE.
    '''
    from lancement import cause_du_dernier_lancement

    nom = entree['nom']
    script, arguments = commande_passe(nom, racine)
    # CHEMINS ABSOLUS TOUS LES DEUX : avec un cwd et un script RELATIFS, le
    # fils resout son script PAR RAPPORT au cwd et le chemin se DOUBLE (mesure
    # du 2026-09-26 sur le cobaye : cobaye-passe/_operateur/.../main.py).
    repertoire = Path(dossier).resolve()
    commande = [sys.executable, str(repertoire / script)] + list(arguments)
    # DRAPEAU D ARRET : en mode PASSE, le service est MAITRE de l allumage. Un
    # drapeau laisse sur la disque (arret cooperatif d avant la bascule, arret
    # pose a la main) etoufferait la passe : la routine s arreterait en tete de
    # boucle sans rien publier, et le service lirait "aucune passe publiee" --
    # un faux ecart qui cacherait le vrai probleme. On le RETIRE et on le DIT
    # (jamais en silence) : l arret defini d une routine en passe est le MODE
    # du planning, pas un drapeau de boucle.
    drapeau = DRAPEAU_PAR_NOM.get(nom)
    retire = False
    if drapeau:
        chemin_drapeau = repertoire / drapeau
        if chemin_drapeau.exists():
            try:
                chemin_drapeau.unlink()
                retire = True
            except OSError:
                retire = False
    avant, _source = derniere_passe(dossier)
    debut = time.monotonic()
    code_retour = None
    sortie = ''
    suspendue = False
    try:
        resultat = subprocess.run(
            commande, cwd=str(repertoire), capture_output=True, text=True,
            timeout=PLAFOND_PASSE_SECONDES, **drapeaux_popen()
        )
        code_retour = resultat.returncode
        sortie = ((resultat.stdout or '') + (resultat.stderr or '')).strip()
    except subprocess.TimeoutExpired:
        suspendue = True
        sortie = ('passe suspendue : plafond de ' + str(PLAFOND_PASSE_SECONDES)
                  + ' s depasse')
    except OSError as erreur:
        sortie = 'allumage impossible : ' + str(erreur)
    duree = int((time.monotonic() - debut) * 1000)
    ecrire_trace_lancement(dossier, sortie)
    cause = cause_du_dernier_lancement(dossier) or ''
    apres, source = derniere_passe(dossier)
    publiee = (apres is not None) and (avant is None or apres != avant)

    probleme = None
    niveau = None
    if suspendue:
        probleme = 'passe suspendue (plafond ' + str(PLAFOND_PASSE_SECONDES) + ' s)'
        niveau = NIVEAU_RETARD
    elif code_retour is None:
        probleme = 'allumage impossible'
        niveau = NIVEAU_PLANTAGE
    elif code_retour != 0:
        probleme = 'code retour ' + str(code_retour)
        niveau = NIVEAU_PLANTAGE if CAUSE_TRACEBACK in sortie else NIVEAU_ECHEC
    elif not publiee:
        probleme = 'aucune passe publiee apres la commande (' + source + ')'
        niveau = NIVEAU_RETARD
    return {
        'probleme': probleme,
        'niveau': niveau,
        'cause': cause,
        'code': code_retour,
        'duree_ms': duree,
        'source': source,
        'publiee': publiee,
        'drapeau_retire': retire,
    }



# ---------------------------------------------------------------------------
# LE TOUR DE SERVICE : la rotation d allumage
# ---------------------------------------------------------------------------
def servir_un_tour(racine=None):
    '''UN tour du service : (allumages, messages, code).

    Rotation d allumage : les entrees sont servies dans l ordre du PLANNING
    (priorite decroissante, puis decalage initial) et AU PLUS UNE allumage par
    tour -- jamais le pic des sept en meme temps. Une routine NON DUE n est
    pas allumee : c est le coeur de la demande du createur.
    '''
    heure = maintenant()
    etat = charger_etat(racine)
    routines = etat['routines']
    if not etat.get('demarrage_service'):
        etat['demarrage_service'] = horodatage(heure)
        ecrire_etat(etat, racine)
    demarrage = instant(etat.get('demarrage_service')) or heure
    messages = []
    code = 0
    allumages = 0

    for entree in entrees(racine):
        nom = entree['nom']
        if entree['mode'] != 'passe':
            continue  # mode boucle : c est le serveur qui la surveille
        dossier = dossier_de_routine(nom, racine)
        courant = routines.setdefault(nom, {})

        # 1. Une passe deja en cours ? JAMAIS deux de la meme routine.
        allume_le = instant(courant.get('allume_le'))
        if allume_le is not None:
            attente = (heure - allume_le).total_seconds()
            if attente <= PLAFOND_PASSE_SECONDES:
                continue
            courant['allume_le'] = None
            suspendu = ('passe suspendue : aucun retour apres '
                        + str(PLAFOND_PASSE_SECONDES) + ' s')
            if signaler_si_frais(courant, NIVEAU_RETARD, suspendu, nom, racine, messages):
                code = max(code, 1)
            ecrire_etat(etat, racine)

        # 2. Est-elle DUE ? (compare, jamais d attente : attente-ne-prouve-rien)
        dernier, source = derniere_passe(dossier)
        age = (heure - dernier).total_seconds() if dernier else None
        if dernier is None:
            decal = decalage(nom, racine)
            if (heure - demarrage).total_seconds() < decal:
                messages.append(nom + ' : decalage initial en cours (' + str(decal) + ' s)')
                continue
        elif age is not None and age < cadence_planning(nom, racine):
            continue  # PAS DUE : on n allume pas

        # 3. DUE : plafond de rotation, puis allumage.
        if allumages >= MAX_ALLUMAGES_PAR_TOUR:
            messages.append(
                'rotation : ' + str(MAX_ALLUMAGES_PAR_TOUR) + ' allumage par tour -- '
                + nom + ' attend le tour suivant'
            )
            break
        courant['allume_le'] = horodatage(heure)
        ecrire_etat(etat, racine)
        verdict = allumer(entree, dossier, racine)
        courant['allume_le'] = None
        courant['dernier_allumage'] = horodatage(heure)
        allumages += 1
        if verdict['probleme'] is None:
            courant['passe_publiee_le'] = horodatage(heure)
            courant['compteur'] = int(courant.get('compteur') or 0) + 1
            messages.append(
                nom + ' : passee en ' + str(verdict['duree_ms']) + ' ms ('
                + verdict['source'] + ', ' + str(courant['compteur']) + ' au total)'
                + (' ; drapeau d arret retire avant la passe'
                   if verdict.get('drapeau_retire') else '')
            )
        else:
            courant['dernier_echec'] = {
                'motif': verdict['probleme'], 'date': horodatage(heure),
                'code': verdict['code'],
            }
            messages.append(
                nom + ' : ECART ' + verdict['probleme']
                + (' | cause : ' + verdict['cause'] if verdict['cause'] else '')
            )
            depose = signaler_si_frais(
                courant, verdict['niveau'], verdict['probleme'], nom, racine,
                messages, erreur=verdict['cause'],
            )
            if depose:
                code = max(code, 1)
        ecrire_etat(etat, racine)

    ecrire_etat(etat, racine)
    return allumages, messages, code


def resume_etat(racine=None):
    '''Lignes de lecture : planning, derniere passe, age, due -- SANS rien attendre.'''
    heure = maintenant()
    etat = charger_etat(racine)
    lignes = ['SERVICE DU PLANNING (MO-429) -- ' + horodatage(heure)]
    lignes.append(
        '  service : demarre le ' + str(etat.get('demarrage_service') or 'jamais')
        + ' | etat ' + str(chemin_etat(racine).name)
    )
    for entree in entrees(racine):
        nom = entree['nom']
        cadence = cadence_planning(nom, racine)
        if entree['mode'] != 'passe':
            lignes.append(
                '  ' + nom + ' : BOUCLE (cadence ' + str(cadence)
                + ' s, supervisee par le serveur)'
            )
            continue
        try:
            dossier = dossier_de_routine(nom, racine)
        except PlanningIllisible as refus:
            lignes.append('  ' + nom + ' : REFUS -- ' + str(refus))
            continue
        dernier, source = derniere_passe(dossier)
        age = int((heure - dernier).total_seconds()) if dernier else None
        due = age is None or age >= cadence
        depuis = ('il y a ' + str(age) + ' s via ' + source) if age is not None             else 'JAMAIS (' + source + ')'
        lignes.append(
            '  ' + nom + ' : PASSE, cadence ' + str(cadence) + ' s, derniere '
            + depuis + ' -> ' + ('DUE' if due else 'pas due')
        )
    return lignes
