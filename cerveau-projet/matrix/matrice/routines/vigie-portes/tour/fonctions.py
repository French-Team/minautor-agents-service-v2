"""Fonctions simples de la categorie tour : une seule tache chacune.

LA PASSE de la vigie-portes. Six familles de controles, du plus dur au plus fin :

  1. RECETTE  -- une porte a-t-elle ce qu'il faut pour etre utilisable
                 (main.py + DESCRIPTION.md, CV-010) ?
  2. SANTE    -- son main.py COMPILE-t-il (compile() en memoire, aucune execution) ?
  3. VERBES   -- chaque sous-dossier est un verbe : a-t-il son entry.py
                 (un sous-dossier sans entree = un verbe FANTOME) ?
  4. MOTEUR   -- le moteur de recherche (porte unique de recherche) repond-il
                 a une requete TEMOIN ? 0 resultat = il est AVEUGLE (MO-055).
  5. USAGE    -- ceux qui utilisent les portes : appels, refus (code 2).
                 Une porte que PERSONNE n'appelle est suspecte : morte, ou
                 inatteignable (le questionnaire du profil, MO-051).
  6. CITATION -- pour une porte muette, on demande au MOTEUR DE RECHERCHE si
                 elle est citee ailleurs. Citee mais jamais appelee = porte
                 INCOHERENTE ; citee nulle part = ORPHELINE (candidate a l'archivage).
"""
import hashlib
import json
from datetime import datetime, timedelta

from battement import ajouter_passe
from commun import (
    appeler_porte,
    ecrire_etat,
    ecrire_etat_passes,
    horodater,
    journaliser,
    lire_etat,
    lire_etat_passes,
)
from constants import (
    ANTI_SPAM_SECONDES,
    CHEMIN_RELATIF_ROUTINES,
    CLE_ANNEAU_PASSES,
    COMMANDES_AIDE,
    REPERTOIRE_ROUTINE,
    CHEMIN_RELATIF_OUTILS,
    CHEMIN_RELATIF_RECHERCHER,
    CHEMIN_RELATIF_SIGNALER,
    CHEMIN_RELATIF_USAGES,
    EXPEDITEUR_SIGNAL,
    FENETRE_JOURS,
    FICHIERS_RECETTE,
    FORMAT_DATE,
    MISSION_SIGNAL,
    MOTIF_DEJA_SIGNALE,
    MOTIF_DEPOT,
    MOTIF_PLANCHER,
    MOTIF_RESOLU,
    MOTIF_VIDE,
    NIVEAU_SIGNAL,
    NIVEAUX_ALERTES,
    NOM_ENTREE,
    OUTIL_SIGNAL,
    PART_REFUS_ALERTE,
    PASSES_GARDEES_ETAT,
    REQUETE_TEMOIN,
    SEUIL_REFUS_MIN,
    SEUIL_TEMOIN,
    ANTERIEURS_NEMESIS,
    CHAMP_STATUT_CARTE,
    CHAMP_TRACE_NEMESIS,
    CHEMIN_RELATIF_CONSTRUITS,
    ETATS_INITIAUX_NEMESIS,
    MARQUEURS_PASSAGE_NEMESIS,
    NIVEAU_NEMESIS,
    PORTE_NEMESIS,
    SEPARATEUR_CARTE,
)
from etat_histoire import decision_fait, signature_fait


def repertoires(racine):
    """Chemins de la passe, derives de la racine matrix/ (cobayables)."""
    return {
        "outils": racine / CHEMIN_RELATIF_OUTILS,
        "usages": racine / CHEMIN_RELATIF_USAGES,
        "rechercher": racine / CHEMIN_RELATIF_RECHERCHER,
        "signaler": racine / CHEMIN_RELATIF_SIGNALER,
    }


def lister_portes(repertoire_outils):
    """Noms des portes (dossiers d'outils), triees."""
    if not repertoire_outils.is_dir():
        return []
    return sorted(
        enfant.name for enfant in repertoire_outils.iterdir()
        if enfant.is_dir() and not enfant.name.startswith("__")
    )


# --- 1. RECETTE -----------------------------------------------------------------


def controler_recette(porte):
    """Constats sur la recette d'une porte (fichiers attendus presents ?)."""
    constats = []
    for nom_fichier in FICHIERS_RECETTE:
        if not (porte / nom_fichier).is_file():
            constats.append({
                "cle": "recette:" + porte.name,
                "niveau": "moyenne",
                "porte": porte.name,
                "detail": "recette incomplete : " + nom_fichier + " absent (CV-010)",
            })
    return constats


# --- 2. SANTE -------------------------------------------------------------------


def controler_sante(porte):
    """La porte compile-t-elle ? compile() en memoire : le code n'est PAS execute."""
    chemin = porte / "main.py"
    if not chemin.is_file():
        return []
    try:
        source = chemin.read_text(encoding="utf-8")
    except OSError as erreur:
        return [{
            "cle": "sante:" + porte.name,
            "niveau": "haute",
            "porte": porte.name,
            "detail": "main.py illisible : " + str(erreur),
        }]
    try:
        compile(source, str(chemin), "exec")
    except SyntaxError as erreur:
        return [{
            "cle": "sante:" + porte.name,
            "niveau": "critique",
            "porte": porte.name,
            "detail": "main.py NE COMPILE PAS (ligne " + str(erreur.lineno) + ") : " + str(erreur.msg),
        }]
    return []


# --- 3. VERBES ------------------------------------------------------------------


def controler_verbes(porte):
    """Chaque sous-dossier de la porte doit porter son entry.py."""
    constats = []
    for enfant in sorted(porte.iterdir() if porte.is_dir() else []):
        if not enfant.is_dir() or enfant.name.startswith("__"):
            continue
        if not (enfant / NOM_ENTREE).is_file():
            constats.append({
                "cle": "verbe:" + porte.name + ":" + enfant.name,
                "niveau": "haute",
                "porte": porte.name,
                "detail": "verbe fantome : " + enfant.name + "/ sans " + NOM_ENTREE,
            })
    return constats


# --- 4. MOTEUR DE RECHERCHE -----------------------------------------------------


def verifier_moteur(chemin_moteur):
    """Le moteur de recherche repond-il a une requete TEMOIN ?

    MO-055 : le moteur scannait un dossier disparu et repondait "0 resultat" a
    TOUTES les requetes -- indiscernable d'une absence de resultat. Ce temoin
    transforme cette panne silencieuse en alerte.
    """
    code, sortie, erreur = appeler_porte(
        chemin_moteur,
        ["rechercher", "--requete", REQUETE_TEMOIN, "--dans", "fichiers", "--json", "--limite", "1"],
    )
    if code == 2 or not sortie.strip():
        return [{
            "cle": "moteur:injoignable",
            "niveau": "haute",
            "porte": "rechercher",
            "detail": "moteur de recherche injoignable (" + (erreur.strip() or "code " + str(code)) + ")",
        }]
    try:
        resultat = json.loads(sortie)
    except ValueError:
        return [{
            "cle": "moteur:sortie",
            "niveau": "moyenne",
            "porte": "rechercher",
            "detail": "moteur de recherche : sortie --json illisible",
        }]
    if int(resultat.get("trouve", 0)) < SEUIL_TEMOIN:
        return [{
            "cle": "moteur:aveugle",
            "niveau": "critique",
            "porte": "rechercher",
            "detail": "moteur de recherche AVEUGLE : 0 resultat sur la requete temoin "
                      + repr(REQUETE_TEMOIN) + " (MO-055)",
        }]
    return []


def chercher_citations(chemin_moteur, requete, exclure=()):
    """Hits du moteur, hors journaux data/ et hors zones exclues (motifs).

    Une citation dans un journal (data/) n'est pas un USAGE : on ne garde que
    les references vivantes (code, docs, conventions), et on retire les zones
    que l'appelant veut ignorer (le dossier de la porte, celui de la vigie).
    """
    code, sortie, _ = appeler_porte(
        chemin_moteur,
        ["rechercher", "--requete", requete, "--dans", "fichiers", "--json", "--limite", "80"],
    )
    if code == 2 or not sortie.strip():
        return None
    try:
        hits = json.loads(sortie).get("hits", [])
    except ValueError:
        return None
    vivants = []
    for hit in hits:
        chemin = str(hit.get("fichier", "")).replace("\\", "/")
        if "/data/" in chemin:
            continue
        if any(motif and motif in chemin for motif in exclure):
            continue
        vivants.append(chemin)
    return vivants


# --- 5. USAGE -------------------------------------------------------------------


def charger_usages(chemin_usages):
    """Evenements du journal d'usages (les entrees illisibles sont ignorees)."""
    if not chemin_usages.is_file():
        return []
    evenements = []
    try:
        lignes = chemin_usages.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            evenements.append(json.loads(ligne))
        except ValueError:
            continue
    return evenements


def usage_par_porte(evenements, maintenant=None, fenetre_jours=FENETRE_JOURS):
    """{outil: {appels, refus}} sur la fenetre glissante.

    DEUX PRECAUTIONS, apprises en regardant les vraies donnees :
      - les appels d'AIDE (`--help`) sortent en code 2 comme un refus. Les
        compter comme de la mauvaise utilisation faisait crier la vigie sur des
        outils parfaitement sains (`editer-agents-md` : 8 "refus" = 8 `--help`) ;
      - le journal d'usages n'est ecrit que par le harnais (sac-a-dos) : un appel
        lance a la main n'y figure PAS. "Aucun appel" ne veut donc pas dire
        "porte morte" (l'appelant le plus frequent de `rechercher` pendant cette
        session etait justement hors harnais).
    """
    maintenant = maintenant or datetime.now()
    debut = maintenant - timedelta(days=fenetre_jours)
    comptes = {}
    for evenement in evenements:
        outil = evenement.get("outil", "")
        if not outil:
            continue
        if str(evenement.get("commande", "")).strip().lower() in COMMANDES_AIDE:
            continue
        try:
            date = datetime.strptime(str(evenement.get("date", "")), FORMAT_DATE)
        except ValueError:
            continue
        if date < debut:
            continue
        case = comptes.setdefault(outil, {"appels": 0, "refus": 0})
        case["appels"] += 1
        if int(evenement.get("code", 0) or 0) == 2:
            case["refus"] += 1
    return comptes


def controler_usage(portes, comptes):
    """Portes mal utilisees (refus majoritaires) et portes MUETTES (observation).

    "Muette" est une OBSERVATION, jamais une alerte : le journal d'usages ne
    couvre que les appels passes par le harnais, donc le silence n'est pas une
    preuve de mort. Elle est croisee avec les citations (controler_citations).
    """
    constats = []
    muettes = []
    for nom in portes:
        case = comptes.get(nom)
        if not case or case["appels"] == 0:
            muettes.append(nom)
            constats.append({
                "cle": "muette-observation:" + nom,
                "niveau": "basse",
                "porte": nom,
                "detail": ("aucun appel en " + str(FENETRE_JOURS) + " jours (le journal d'usages"
                           " ne couvre que les appels passes par le harnais)"),
            })
            continue
        if case["refus"] >= SEUIL_REFUS_MIN and case["refus"] >= PART_REFUS_ALERTE * case["appels"]:
            constats.append({
                "cle": "refus:" + nom,
                "niveau": "moyenne",
                "porte": nom,
                "detail": ("mal utilisee : " + str(case["refus"]) + " refus (code 2) sur "
                           + str(case["appels"]) + " appel(s) en " + str(FENETRE_JOURS) + " jours"),
            })
    return constats, muettes


# --- 6. CITATION ----------------------------------------------------------------


def controler_portes_fantomes(portes, comptes, repertoire_routines):
    """Un nom APPELE qui n'est ni une porte ni une routine = a regarder.

    C'est le cote "ceux qui les utilisent" : quelqu'un appelle quelque chose qui
    n'est plus la (renomme, supprime, ou jamais cree). Autre exemple reel :
    `bdd-suivi-optimus` figure au journal d'usages alors qu'aucun dossier de ce
    nom n'existe.

    OBSERVATION, jamais une alerte : le journal d'usages ne logue pas que des
    portes -- les COMBOS (`c-001-lecons`, `combo-lecons`) et les ROUTINES
    (`veille-flux`) y figurent aussi sous le meme champ. Faute de pouvoir
    trancher depuis le Flux 1 (les combos vivent en zone Optimus), on signale
    sans crier : c'est au createur de dire si le nom est mort ou vivant.
    """
    routines = set()
    if repertoire_routines.is_dir():
        routines = {enfant.name for enfant in repertoire_routines.iterdir() if enfant.is_dir()}
    constats = []
    for nom in sorted(comptes):
        if nom in portes or nom in routines:
            continue
        constats.append({
            "cle": "nom-inconnu:" + nom,
            "niveau": "basse",
            "porte": nom,
            "detail": ("nom INCONNU au journal d'usages (" + str(comptes[nom]["appels"])
                       + " appel(s)) : ni porte (outils/) ni routine (routines/) --"
                       " combo, renommage ou porte morte ?"),
        })
    return constats


def controler_citations(muettes, chemin_moteur, exclusions):
    """Pour chaque porte muette : citee ailleurs (= vivante) ou orpheline ?

    On exclut deux zones, sinon la vigie se cite ELLE-MEME : son dossier (etat +
    journal, qui contiennent les noms d'outils en clair) et le dossier de la
    porte cherchee. Reste ce qui compte : le code, les docs, les conventions.
    """
    constats = []
    for nom in muettes:
        vivants = chercher_citations(chemin_moteur, nom, exclure=exclusions + ("/outils/" + nom + "/",))
        if vivants is None:
            continue  # moteur injoignable : deja signale par le temoin
        if vivants:
            constats.append({
                "cle": "muette-vivante:" + nom,
                "niveau": "basse",
                "porte": nom,
                "detail": ("citee par " + str(len(vivants)) + " fichier(s) vivant(s) sans aucun"
                           " appel enregistre (ex : " + vivants[0].split("/")[-1] + ")"),
            })
        else:
            constats.append({
                "cle": "orpheline:" + nom,
                "niveau": "basse",
                "porte": nom,
                "detail": "ORPHELINE : aucun appel et citee nulle part (candidate a l'archivage)",
            })
    return constats


# --- SYNTHESE -------------------------------------------------------------------


def signature(alertes):
    """Signature stable d'un jeu d'alertes (anti-spam) : 1 alerte bouge = 1 alerte."""
    brut = "|".join(sorted(alerte["niveau"] + ":" + alerte["cle"] for alerte in alertes))
    return hashlib.sha256(brut.encode("utf-8")).hexdigest()


def alertes_notables(alertes):
    """Les alertes qui partent REELLEMENT dans l'inbox (niveaux notables).

    La borne anti-spam porte sur CE jeu-la : c'est lui la "mission" de la vigie.
    Une observation "basse" (porte muette, nom inconnu) qui bouge ne declenche
    donc plus un depot qui n'aurait rien a dire.
    """
    return [alerte for alerte in alertes if alerte["niveau"] in NIVEAUX_ALERTES]


def secondes_depuis(horodatage, maintenant):
    """Secondes ecoulees depuis un horodatage du journal (None si absent/illisible)."""
    if not horodatage:
        return None
    try:
        moment = datetime.strptime(horodatage, FORMAT_DATE)
    except ValueError:
        return None
    return (maintenant - moment).total_seconds()


def journaliser_passe(portes, alertes, notables, signature_notable, motif):
    """ETAT et HISTOIRE d'une passe : le journal ne recoit la passe que si elle CHANGE.

    MO-082 -- mesure du 2026-09-14 : 105 lignes identiques sur 204 (51,5 %), une
    par tour de 900 s. La photo complete d'une passe (le nombre d'ALERTES compris)
    part dans l'ETAT court, ecrit a CHAQUE passe et ECRASE ; l'HISTOIRE ne recoit
    que ce que la vigie a A DIRE : `portes`, `notables`, `signature`.

    Les observations BASSES (porte muette, nom inconnu, orpheline) n'entrent donc
    PAS dans la signature du fait : elles bougent sans rien dire (lecon MO-073),
    et leur mouvement ne doit ni deposer une alerte ni gonfler le journal. Elles
    restent dans l'etat court, ou elles sont la photo du moment.
    """
    vu = {"portes": len(portes), "notables": len(notables), "signature": signature_notable}
    passe_avant = lire_etat_passes()
    signature_passe = signature_fait(vu)
    notable, mode = decision_fait(signature_passe, passe_avant.get("signature_passe"))
    absorbes = int(passe_avant.get("passes_absorbes") or 0)

    if notable:
        journaliser({
            "type": "passe", **vu, "alertes": len(alertes), "motif": motif,
            "mode": mode, "passes_absorbes": absorbes,
        })

    # L'ETAT court : ecrit a CHAQUE passe, ECRASE. Il porte ce que la passe a vu,
    # ce qu'elle a decide, et le compte des passes absorbees depuis la derniere
    # ligne d'histoire -- la redondance supprimee est TRACEE, jamais silencieuse.
    maintenant = horodater()
    ecrire_etat_passes({
        **vu,
        # LA DATE DE LA PASSE : sans elle, le battement REEL d'une routine
        # absorbante n'est mesurable nulle part (friction 28 : rien ne comparait
        # le battement reel a la cadence declaree).
        "date": maintenant,
        "alertes": len(alertes),
        "motif": motif,
        "mode": mode,
        "signature_passe": signature_passe if notable else (passe_avant.get("signature_passe") or ""),
        "passes_absorbes": 0 if notable else absorbes + 1,
        "derniere_ecriture": maintenant if notable else (passe_avant.get("derniere_ecriture") or ""),
        # L'ANNEAU DES PASSES : c'est LUI qui rend le battement mesurable en
        # MEDIANE. `passes_absorbes` / `derniere_ecriture` disent COMBIEN de
        # passes ont ete absorbees ; ils ne disent pas QUAND -- une moyenne sur
        # ces deux nombres est fausse des qu'une passe n'est pas a l'heure.
        CLE_ANNEAU_PASSES: ajouter_passe(
            passe_avant.get(CLE_ANNEAU_PASSES), maintenant, PASSES_GARDEES_ETAT
        ),
    })
    return notable, mode


def decision_depot(signature_actuelle, signature_alertee, secondes_ecoulees):
    """(deposer, motif) : decision PURE du depot (testable sans disque ni horloge).

    Le depot est borne par MISSION et par le TEMPS :
      - jeu notable INCHANGE depuis le dernier depot -> aucun depot ;
      - jeu notable different mais dernier depot plus recent que
        ANTI_SPAM_SECONDES -> RETENU (motif "plancher") : la passe suivante le
        reprendra, rien n'est perdu ;
      - sinon -> depot.
    """
    if signature_actuelle == signature_alertee:
        return False, MOTIF_DEJA_SIGNALE
    if secondes_ecoulees is not None and secondes_ecoulees < ANTI_SPAM_SECONDES:
        return False, MOTIF_PLANCHER
    return True, MOTIF_DEPOT


def deposer_alertes(chemin_signaler, alertes):
    """Depose les alertes notables dans l'inbox de la Matrice par la PORTE signaler."""
    notables = [alerte for alerte in alertes if alerte["niveau"] in NIVEAUX_ALERTES]
    if not notables:
        return 0, "aucune alerte de niveau " + "/".join(NIVEAUX_ALERTES)
    # L'alerte NOMME la porte : une alerte qui ne dit pas QUI est en cause
    # n'est pas actionnable (constate a la premiere passe, ou les 7 recettes
    # incompletes sont parties sans nommer les 7 outils).
    lignes = ["vigie-portes -- " + str(len(notables)) + " alerte(s) :"]
    for alerte in notables:
        lignes.append("[" + alerte["niveau"] + "] " + alerte["porte"] + " : " + alerte["detail"])
    code, sortie, erreur = appeler_porte(
        chemin_signaler,
        [
            "signaler",
            "--outil", OUTIL_SIGNAL,
            "--niveau", NIVEAU_SIGNAL,
            "--description", " | ".join(lignes),
            "--mission", MISSION_SIGNAL,
            "--expediteur", EXPEDITEUR_SIGNAL,
        ],
    )
    return code, (sortie.strip() or erreur.strip())


def executer_tour(racine, signaler_actif=True):
    """UNE passe complete de la vigie-portes. Retourne un code (0 = sain)."""
    chemins = repertoires(racine)
    portes = lister_portes(chemins["outils"])

    alertes = []
    alertes += verifier_moteur(chemins["rechercher"])
    for nom in portes:
        porte = chemins["outils"] / nom
        alertes += controler_recette(porte)
        alertes += controler_sante(porte)
        alertes += controler_verbes(porte)

    comptes = usage_par_porte(charger_usages(chemins["usages"]))
    constats_usage, muettes = controler_usage(portes, comptes)
    alertes += constats_usage
    alertes += controler_portes_fantomes(portes, comptes, racine / CHEMIN_RELATIF_ROUTINES)
    alertes += controler_citations(muettes, chemins["rechercher"], (str(REPERTOIRE_ROUTINE).replace("\\", "/"),))

    alertes += controler_nemesis(racine)
    alertes.sort(key=lambda alerte: (alerte["niveau"], alerte["cle"]))
    # BORNE ANTI-SPAM (MO-073) : la "mission" de la vigie, c'est le jeu des
    # alertes NOTABLES -- celles qui partent dans l'inbox. La signature porte sur
    # CE jeu, plus sur l'ensemble des observations : une porte muette qui bouge
    # (niveau "basse") ne repose plus un depot identique a l'inbox.
    notables = alertes_notables(alertes)
    etat_precedent = lire_etat()
    signature_notable = signature(notables)
    ecoule = secondes_depuis(etat_precedent.get("alerte_le", ""), datetime.now())

    print("VIGIE-PORTES -- racine : " + str(racine))
    print("  portes : " + str(len(portes)) + " | alertes : " + str(len(alertes))
          + " | notables : " + str(len(notables)) + " | muettes : " + str(len(muettes)))
    for alerte in alertes:
        print("  [" + alerte["niveau"] + "] " + alerte["porte"] + " : " + alerte["detail"])

    if not signaler_actif:
        # PASSE A BLANC : elle REGARDE, elle ne consomme RIEN. Ecrire l'etat ici
        # marquerait les alertes comme "deja signalees" et la premiere vraie
        # passe ne deposerait plus rien -- la vigie se serait rendue muette
        # toute seule, exactement la panne qu'elle est censee detecter.
        print("  PASSE A BLANC : rapport + journal seulement, etat inchange (rien n'est consomme).")
        journaliser({
            "type": "passe-blanche", "portes": len(portes),
            "alertes": len(alertes), "notables": len(notables),
            "signature": signature_notable,
        })
        return 0 if not alertes else 1

    if not notables:
        # RIEN A DEPOSER : l'etat n'est PAS horodate comme un depot. Avant cette
        # correction, une simple variation d'observations "basses" faisait
        # ecrire alerte_le = maintenant -- le plancher anti-spam etait repousse a
        # chaque mouvement d'usage, et la vigie se rendait muette elle-meme.
        print("  aucune alerte notable (" + "/".join(NIVEAUX_ALERTES) + ") : rien a deposer.")
        precedent_notables = alertes_notables(etat_precedent.get("alertes") or [])
        if precedent_notables:
            print("  ALERTES RESOLUES depuis la derniere passe.")
            journaliser({"type": MOTIF_RESOLU, "portes": len(portes), "alertes": len(alertes)})
        else:
            # Une passe sans rien a dire n'est un fait que si la photo des portes
            # a change : sinon elle part dans l'etat court (MO-082).
            journaliser_passe(portes, alertes, notables, signature_notable, MOTIF_VIDE)
        if etat_precedent.get("signature") or precedent_notables:
            # alerte_le est CONSERVEE : le plancher traverse les episodes
            # (une alerte qui disparait puis revient en moins de 15 min ne
            # repose pas un depot aussitot).
            ecrire_etat({"signature": "", "alerte_le": etat_precedent.get("alerte_le", ""),
                         "alertes": []})
        return 0 if not alertes else 1

    deposer, motif = decision_depot(signature_notable, etat_precedent.get("signature", ""), ecoule)
    if not deposer:
        print("  aucun depot (" + motif + ") : " + str(len(notables))
              + " alerte(s) notable(s), bilan " + ("au journal." if motif == MOTIF_PLANCHER else "a l'etat court."))
        journaliser_passe(portes, alertes, notables, signature_notable, motif)
        return 1

    code, message = deposer_alertes(chemins["signaler"], notables)
    print("  depot alerte : code " + str(code) + " -- " + message[:160])
    journaliser({
        "type": "alerte", "portes": len(portes), "signature": signature_notable,
        "depot_code": code, "motif": motif,
        "alertes": [alerte["cle"] for alerte in notables],
    })

    ecrire_etat({
        "signature": signature_notable,
        "alerte_le": datetime.now().strftime(FORMAT_DATE),
        "alertes": [{"cle": alerte["cle"], "niveau": alerte["niveau"], "detail": alerte["detail"]} for alerte in notables],
    })
    return 1


# --- 7. NEMESIS (EO-219, regle createur du 2026-09-19) --------------------------


def lire_document(chemin):
    """Lecture sans exception : un document illisible n'est pas un constat de
    nemesis (la porte porte deja son controle de sante)."""
    try:
        return chemin.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def statut_carte(texte):
    """Statut DECLARE dans la carte d'identite -- jamais un statut de texte libre."""
    lignes = texte.splitlines()
    if not lignes or lignes[0].strip() != SEPARATEUR_CARTE:
        return ""
    for ligne in lignes[1:]:
        nu = ligne.strip()
        if nu == SEPARATEUR_CARTE:
            break
        if nu.startswith(CHAMP_STATUT_CARTE):
            return nu.split(CHAMP_STATUT_CARTE, 1)[1].strip()
    return ""


def a_trace_nemesis(texte):
    """DEUX conditions : la trace est DECLAREE (champ de carte) ET le passage est
    ECRIT dans le corps. Un champ seul serait une promesse (L-055)."""
    if not any(marqueur in texte for marqueur in MARQUEURS_PASSAGE_NEMESIS):
        return False
    return any(ligne.strip().startswith(CHAMP_TRACE_NEMESIS) for ligne in texte.splitlines())


def controler_nemesis(racine):
    """EO-219 : un document CONSTRUIT (carte + statut) doit porter son nemesis.

    Le controle lit le DOMICILE DECLARE seulement : il ne juge pas tout matrix/,
    sinon il accuserait a vie des documents construits avant la regle. Les
    ANTERIEURS declares sont sautes et leur raison est ECRITE dans les constantes."""
    constats = []
    repertoire = racine / CHEMIN_RELATIF_CONSTRUITS
    if not repertoire.is_dir():
        return constats
    for chemin in sorted(repertoire.rglob("*.md")):
        if chemin.name in ANTERIEURS_NEMESIS:
            continue
        texte = lire_document(chemin)
        statut = statut_carte(texte)
        if not statut or statut in ETATS_INITIAUX_NEMESIS:
            continue
        if a_trace_nemesis(texte):
            continue
        constats.append({
            "cle": "nemesis:" + chemin.relative_to(racine).as_posix(),
            "niveau": NIVEAU_NEMESIS,
            "porte": PORTE_NEMESIS,
            "detail": "construction sans NEMESIS : statut " + statut
                      + " declare sans trace de contre-analyse (EO-219)",
        })
    return constats
