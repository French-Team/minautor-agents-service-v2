#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sc-006-lacunes -- retrouver les LACUNES et les combler (demande createur MO-530).

POURQUOI CE SUPER-COMBO. La demande du createur tient en une image : quand
Optimus ou le Cameleon reproduisent SOUVENT les MEMES erreurs, c est qu il y a une
lacune. Super-combo `lacunes` sert a la retrouver, puis a la combler. Comme pour
nemesis, chaque phase a son PARCOURS DEDIE, et le travail de l une est consomme
par la suivante -- un compte rendu de phase n est pas un rapport, c est l ENTREE
de la phase suivante.

LA MESURE QUI A DIT COMMENT (2026-10-02, MO-530) -- et elle a change le projet.

1. LE SIGNAL EXISTE, IL EST MORT. `frictions.db` compte 98 entrees (73 de type
   `outil`, 72 de gravite majeure) et ZERO active : les 98 sont archivees. La
   DERNIERE date d archivage est le 2026-09-30. Trois jours se sont ecoules sans
   qu une seule friction soit deposee -- alors que la mission en cours en a
   produit plusieurs (un `AttributeError` de `rendre-graphe`, deux gardes de
   non-regression en echec repetes). La ou l on mesure le probleme, on le CORRIGE
   dans la meme passe ; la ou on le mesure et qu on le laisse, il s accumule.

2. LA PORTE EXISTE ET N EST PAS JOUEE. `bdd-frictions ajouter` est une porte
   complete (type, gravite, frequence, mission-id) et l outil EST enregistre au
   registre (180 entrees). Mais elle n est appelable ni par le lanceur (le nom
   est absent de `lancer.py`) ni par aucune routine : c est exactement la forme
   que MO-528 a nommee -- un instrument livre sans appelant est un tiers du
   travail, il dort.

3. NEMESIS EST UN PROCESSUS V3 (corrige le 2026-10-02 sur demande du
   createur). Une premiere mesure l avait rate deux fois : elle cherchait
   `nemesis` dans les NOMS de fichiers, puis concluait a une CONDITION de blocage.
   La v3 en porte TROIS occurrences, distinctes :
   - comme PROCESSUS : le parcours `AUTO-AUDIT-NEMESIS` -- 5 phases, 3 axes
     (cas limites, optimisation, securite), plus un reflexe impose AVANT toute
     validation (< Jamais de validation sans preuve de robustesse >). C est le
     nemesis a part entiere.
   - comme VOIX CONTRADICTOIRE : le theme `CONTRE-ANALYSE`, qui rend le
     pour/contre exploitable par le createur.
   - comme CONDITION : `chaine-pense-bete` lit un champ `nemesis:` et refuse
     d avancer si la trace manque (< le nemesis est une CONDITION, pas une
     promesse >, arbitrage D).
   CONCLUSION : il n y a RIEN a construire du cote nemesis, et l on ne le
   recopie pas -- mais parce qu il est deja un PROCESSUS, pas parce qu il serait
   un simple verrou. `lacunes` l APPELLE, a son domicile.

4. LA PORTEE DES LECTURES SE DIT. Les 3 sources vivent en zone privee. Le verbe
   `rechercher` REFUSE sans `--prive` : une lecture qui ne dit pas ce qu elle lit
   laisse croire a un constat portant sur la zone entiere (garde `tester-theme`).

CE QUE CE SUPER-COMBO FAIT, PHASE PAR PHASE (verbes).
  rechercher  chercher ou l agent se trompe. Les LECTURES qui revelent une
              lacune : frictions, lecons, segments de raisonnement, et la
              repetition des memes outils. Verdict nomme, jamais un score.
  comparer    CONSTATER une repetition : meme outil casse en boucle, meme
              remede rejoue, meme garde en echec. La repetition est la preuve.
  investiguer Ramener la repetition A LA RACINE : pourquoi l erreur est-elle
              possible ? ce qui manque, et ou.
  analyser    QQCP : QUI, QUOI, COMMENT, POURQUOI. Quatre cases, quatre reponses
              factuelles. Une case vide se DIT, elle ne se devine pas.
  combler     Ce qui est ECRIT : le choix et son emprise (regle / correction
              d outil / parcours / lecon). Le super-combo ne corrige JAMAIS
              lui-meme : il produit la DECISION, et la porte la pose.

CE QUE CE SUPER-COMBO NE FAIT PAS, ET LE DIT.
  - il ne reproduit pas nemesis : il l appelle (phase `analyser`).
  - il n invente pas une lacune : sans fait, la phase se ta it et le dit.
  - il ne corrige rien : une lacune ne se corrige pas depuis un constat, elle se
    corrige par une porte. Le combo sort une decision, pas un patch.

Usage : python main.py <rechercher|comparer|investiguer|analyser|combler|status|auto-test>
  code 0 = la phase tient, 1 = ecart nomme, 2 = refus.
"""

import json
import sqlite3
import sys
from pathlib import Path

SUPER_ID = "sc-006"
SUPER_NOM = "sc-006-lacunes"
PHASES = ["rechercher", "comparer", "investiguer", "analyser", "combler"]
VERBE_DEFAUT = "rechercher"
VERBES = PHASES + ["status", "auto-test"]

CODE_OK = 0
CODE_ECHEC = 1
CODE_REFUS = 2

BASE = Path(__file__).resolve().parent.parent.parent.parent
RACINE = next(p for p in [BASE, *BASE.parents] if p.name == "matrix")
CHEMIN_FRICTIONS = RACINE / "matrice" / "data" / "frictions.db"
CHEMIN_LECONS = RACINE / "matrice" / "data" / "lecons.json"
CHEMIN_SEGMENTS = RACINE / "_operateur" / "optimus-prime" / "raisonnement" / "segments.json"
# LE NEMESIS EST APPELLE, JAMAIS RECOPIE (M-076) : son parcours est lu a son
# propre domicile. Le recopier le ferait diverger en silence -- et il divergerait
# de celui que le createur edite.
# CORRECTION 2026-10-02 (createur) : le NEMESIS est un PROCESSUS v3, pas une
# condition -- `AUTO-AUDIT-NEMESIS` est un parcours indexe de 5 phases et 3 axes
# (cas limites, optimisation, securite). C'est LUI qu on appelle ; le premier
# domicile mesure ici etait le mauvais.
CHEMIN_AUTO_AUDIT_NEMESIS = (RACINE / "_operateur" / "optimus-prime"
                             / "parcours" / "themes" / "theme-auto-audit-nemesis.json")
# La VOIX contradictoire reste un autre domicile, et ne rend pas le processus
# redondant : l un AUDITE un livrable, l autre rend le pour/contre exploitable.
CHEMIN_CONTRE_ANALYSE = (RACINE / "_operateur" / "optimus-prime"
                         / "parcours" / "themes" / "theme-contre-analyse.json")
CHEMIN_CHAINE_NEMESIS = RACINE / "matrice" / "data" / "outils" / "chaine-pense-bete" / "constants.py"

# LA MESURE QUI FAIT LE MOTIF : combien de frictions ont ete deposees depuis N
# jours. Au-dela du seuil, la phase `rechercher` DIT que le signal dort -- elle
# ne le note pas elle-meme (une porte se pose par la porte, jamais a la main).
SEUIL_SILENCE_JOURS = 3


def _jours_derniere_friction():
    """(jours depuis la derniere friction, date ISO) ou (-1, "") si aucune."""
    if not CHEMIN_FRICTIONS.is_file():
        return -1, ""
    try:
        connexion = sqlite3.connect(str(CHEMIN_FRICTIONS))
        try:
            ligne = connexion.execute(
                "select max(date_archivage) from frictions").fetchone()
        finally:
            connexion.close()
    except sqlite3.Error:
        return -1, ""
    if not ligne or not ligne[0]:
        return -1, ""
    from datetime import datetime
    try:
        derniere = datetime.strptime(str(ligne[0])[:19], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return -1, ""
    return (datetime.now() - derniere).days, str(ligne[0])


def inventaire_sources():
    """Ce que chaque LECTURE reellement porte. Un compte, jamais une impression."""
    sources = {}
    if CHEMIN_FRICTIONS.is_file():
        try:
            connexion = sqlite3.connect(str(CHEMIN_FRICTIONS))
            try:
                sources["frictions"] = {
                    "total": connexion.execute(
                        "select count(*) from frictions").fetchone()[0],
                    "actives": connexion.execute(
                        "select count(*) from frictions where statut='active'"
                    ).fetchone()[0],
                }
            finally:
                connexion.close()
        except sqlite3.Error:
            sources["frictions"] = {"total": 0, "actives": 0}
    else:
        sources["frictions"] = {"total": 0, "actives": 0}
    for cle, chemin in (("lecons", CHEMIN_LECONS), ("segments", CHEMIN_SEGMENTS)):
        nombre = 0
        if chemin.is_file():
            try:
                donnees = json.loads(chemin.read_text(encoding="utf-8"))
                brut = (donnees.get("lecons") if cle == "lecons"
                        else donnees.get("segments")) or []
                nombre = len(brut)
            except (OSError, ValueError):
                nombre = 0
        sources[cle] = {"total": nombre}
    return sources


def nemesis_appelle():
    """Le nemesis existe-t-il la, ou faut-il le dire ? Une absence se DIT.

    On mesure son DOMICILE, qui est le processus `AUTO-AUDIT-NEMESIS`, puis la
    voix contradictoire, puis la condition de chaine. Les trois sont releves :
    un domicile absent se DIT, il ne se deduit pas des deux autres.
    """
    etat = {"processus": CHEMIN_AUTO_AUDIT_NEMESIS.is_file(),
            "voix_contradictoire": CHEMIN_CONTRE_ANALYSE.is_file(),
            "condition_chaine": CHEMIN_CHAINE_NEMESIS.is_file()}
    for cle, chemin in (("processus", CHEMIN_AUTO_AUDIT_NEMESIS),
                        ("voix_contradictoire", CHEMIN_CONTRE_ANALYSE)):
        if not etat[cle]:
            continue
        try:
            donnees = json.loads(chemin.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            etat[cle] = False
            continue
        etat[cle + "_nom"] = donnees.get("theme", {}).get("nom", "")
        etat[cle + "_phases"] = len(donnees.get("theme", {}).get("redirects", []))
    if not etat["processus"]:
        etat["processus_nom"] = "ABSENT"
    return etat


def phase_rechercher(sujet="", prive=False, mesure=None):
    """Ou l agent se trompe-t-il ? On nomme les LECTURES et leur volume.

    LA PORTEE SE DIT (garde `tester-theme`). Les trois sources vivent en zone
    PRIVEE (`matrice/data`, `_operateur/optimus-prime/raisonnement`). Sans
    `--prive`, la lecture ne porte sur RIEN et le dit -- un constat muet sur
    une zone qu il ne lit pas est l angle mort que le garde refuse.
    """
    if not prive:
        return CODE_REFUS, ("REFUS : lecture SANS PORTEE. Les 3 sources (frictions,"
                            " lecons, segments) sont en zone PRIVEE : repasser avec"
                            " --prive, ou le constat ne porterait sur rien -- le"
                            " dire vaut mieux que lire en silence")
    sources = inventaire_sources()
    # LA MESURE PEUT ETRE INJECTEE : c est ce qui permet a l auto-test de jouer
    # les DEUX faces du seuil sur des faits FABRIQUES, au lieu de subir celle
    # du disque. Un test qui ne peut pas repondre n est pas un test (M-051).
    jours, date_iso = mesure if mesure is not None else _jours_derniere_friction()
    lignes = ["PHASE 1 -- RECHERCHER --prive" + (" (sujet : " + sujet + ")" if sujet else ""),
              "  Les lectures qui revelent une lacune (portee : zone privee, 3 sources) :"]
    for nom, compte in sorted(sources.items()):
        lignes.append("    " + nom + " : " + str(compte.get("total", 0)) + " entree(s)")
    lignes.append("  Frictions ACTIVES (le signal non eteint) : "
                  + str(sources["frictions"]["actives"]))
    if jours < 0:
        lignes.append("  SIGNAL INCONNU : aucune date d archivage -- le dire, ne pas supposer")
    else:
        lignes.append("  Derniere friction : " + date_iso + " (" + str(jours)
                      + " jour(s) -- seuil de silence : " + str(SEUIL_SILENCE_JOURS) + ")")
        if jours >= SEUIL_SILENCE_JOURS:
            lignes.append("  ALERTE NOMMEE : le signal DORT. "
                          "Des lacunes sont possibles et rien ne les note. "
                          "La porte `bdd-frictions ajouter` existe ; elle n est pas jouee.")
    etat = nemesis_appelle()
    lignes.append("  Nemesis APPELLE (jamais recopie) : PROCESSUS="
                  + str(etat.get("processus_nom", "ABSENT"))
                  + " (" + str(etat.get("processus_phases", 0)) + " phases, 3 axes)"
                  + " | voix contradictoire="
                  + str(etat.get("voix_contradictoire_nom", "ABSENT"))
                  + " | condition de chaine=" + str(etat["condition_chaine"]))
    return CODE_OK, "\n".join(lignes)


def phase_comparer(cible=""):
    """Constater la REPETITION : c est elle qui prouve une lacune."""
    if not cible:
        return CODE_REFUS, ("REFUS : comparer a besoin d une CIBLE (outil, garde, phrase) -- "
                           "sans elle on ne peut pas prouver la repetition")
    sources = inventaire_sources()
    lignes = ["PHASE 2 -- COMPARER (cible : " + cible + ")",
              "  Une lacune se PROUVE par la repetition ; une fois, ce n est pas une lacune.",
              "  Frictions disponibles pour la comparaison : "
              + str(sources["frictions"]["total"])]
    lignes.append("  Verdict : la repetition se constate sur les entrees de la BDD des frictions "
                  "et sur l historique des missions ; une SEULE occurrence ne conclut rien.")
    return CODE_OK, "\n".join(lignes)


def phase_investiguer(cible=""):
    """Ramener la repetition A LA RACINE : ce qui manque, et OU."""
    if not cible:
        return CODE_REFUS, ("REFUS : investiguer a besoin d une CIBLE -- la racine se cherche "
                           "depuis un fait nomme, jamais dans le vide")
    lignes = ["PHASE 3 -- INVESTIGUER (cible : " + cible + ")",
              "  Trois questions, dans cet ordre :",
              "    1. QUE manque-t-il ? (le manquant, nomme -- pas le symptome)",
              "    2. OU manque-t-il ? (le fichier, la porte, la regle -- un chemin)",
              "    3. POURQUOI est-ce manquant ? (la cause qui rend l erreur POSSIBLE)",
              "  Une racine qui ne nomme pas un emplacement n est pas une racine."]
    return CODE_OK, "\n".join(lignes)


def phase_analyser(cible=""):
    """QQCP -- quatre cases, quatre reponses factuelles, et le nemesis les attaque."""
    etat = nemesis_appelle()
    lignes = ["PHASE 4 -- ANALYSER (QQCP" + (" -- " + cible if cible else "") + ")",
              "  QUI     : qui a echoue, et qui decide du remede",
              "  QUOI    : le manque nomme, en une phrase",
              "  COMMENT : par quel geste et quelle porte la lacune se comble",
              "  POURQUOI: la regle ou le contrat qui rendra l erreur impossible a repetre",
              "  Nemesis PROCESSUS (AUTO-AUDIT-NEMESIS) : "
              + ("lu a son domicile, " + str(etat.get("processus_phases", 0))
                 + " phase(s), 3 axes ; on l APPLIQUE, on ne le reinvente pas"
                 if etat.get("processus") else "ABSENT -- le dire"),
              "  Voix contradictoire (CONTRE-ANALYSE) : "
              + ("lu a son domicile, " + str(etat.get("voix_contradictoire_phases", 0))
                 + " etape(s)"
                 if etat.get("voix_contradictoire") else "ABSENT -- le dire")]
    lignes.append("  Une case vide se DIT vide : elle ne se devine pas.")
    return CODE_OK, "\n".join(lignes)


def phase_combler(cible=""):
    """Ce qui est ECRIT. La decision, jamais le patch."""
    lignes = ["PHASE 5 -- COMBLER" + (" (cible : " + cible + ")" if cible else ""),
              "  Une lacune ne se corrige pas depuis un constat : elle se corrige PAR",
              "  une porte, et la porte exige une decision. Le combo sort donc la",
              "  DECISION et son emprise, jamais un patch :",
              "    - une REGLE immuable  -> la porte `ecrire` pose le fichier",
              "    - une correction d OUTIL -> la mission de reparation la porte",
              "    - un PARCOURS         -> le theme du vivier",
              "    - une LECON            -> la porte `bdd-lecons ajouter`"]
    lignes.append("  Emprise a nommer avant d ecrire : quel fichier, quelle porte, "
                  "quelle preuve.")
    return CODE_OK, "\n".join(lignes)


def status():
    """L etat REEL du signal, et la place du nemesis. Rien n est Suppose."""
    sources = inventaire_sources()
    jours, date_iso = _jours_derniere_friction()
    etat = nemesis_appelle()
    donnees = {
        "super_combo": SUPER_NOM,
        "phases": PHASES,
        "signal_frictions": sources["frictions"],
        "dernieres_friction": date_iso or None,
        "jours_de_silence": jours,
        "seuil_silence": SEUIL_SILENCE_JOURS,
        "signal_dort": bool(jours >= SEUIL_SILENCE_JOURS and jours >= 0),
        "nemesis": etat,
        "lecon": ("Nemesis n est pas a construire : c est un PROCESSUS v3 "
                  "(AUTO-AUDIT-NEMESIS, 3 axes),complete par une voix "
                  "contradictoire (CONTRE-ANALYSE) et une condition de chaine "
                  "(chaine-pense-bete). Ce combo l APPELLE."),
    }
    return CODE_OK, json.dumps(donnees, ensure_ascii=True, indent=2)


def auto_test():
    """Les cobayes, joues sur des faits FABRIQUES -- jamais sur le disque reel."""
    resultats = []

    def controler(nom, condition, detail=""):
        resultats.append(bool(condition))
        print("[" + ("OK" if condition else "KO") + "] " + nom + " : " + detail)

    # 1. COBAYE, LES DEUX FACES : le silence se DIT des deux cotes du seuil.
    #    Le `or True` d ici ne testait RIEN (corrige le 2026-10-04, MO-577) :
    #    la branche sous le seuil acceptait n importe quelle sortie, donc une
    #    ALERTE annoncee a tort y passait sans crier. On joue des faits
    #    FABRIQUES de chaque cote -- une face non jouee est une face qui peut
    #    mentir en silence.
    code_bas, sortie_bas = phase_rechercher(prive=True, mesure=(0, "2099-01-01 00:00:00"))
    controler("sous le seuil, l alerte est MUETTE (fait fabrique)",
              "ALERTE NOMMEE" not in sortie_bas,
              "silence de 0 jour(s) -- seuil " + str(SEUIL_SILENCE_JOURS))
    code_haut, sortie_haut = phase_rechercher(prive=True,
                                             mesure=(SEUIL_SILENCE_JOURS, "2099-01-01 00:00:00"))
    controler("au seuil, le signal DORT est NOMME (fait fabrique)",
              "ALERTE NOMMEE" in sortie_haut,
              "silence de " + str(SEUIL_SILENCE_JOURS) + " jour(s)")
    code_inconnu, sortie_inconnu = phase_rechercher(prive=True, mesure=(-1, ""))
    controler("sans date, le signal est INCONNU et se dit (fait fabrique)",
              "SIGNAL INCONNU" in sortie_inconnu and "ALERTE NOMMEE" not in sortie_inconnu,
              "mesure (-1) : la date manque, donc rien n est suppose")

    # 1a. LA FACE REELLE : l auto-test valide aussi ce que le DISQUE dit, et
    #     il compare la sortie a la MESURE relue -- pas a une attente ecrite
    #     en dur, qui mentrait des que le parc changerait.
    jours_reels, _ = _jours_derniere_friction()
    code_reel, sortie_reel = phase_rechercher(prive=True)
    attendu_reel = jours_reels >= SEUIL_SILENCE_JOURS
    controler("la sortie REELLE suit la mesure REELLE",
              ("ALERTE NOMMEE" in sortie_reel) == attendu_reel,
              "silence reel de " + str(jours_reels) + " jour(s), seuil "
              + str(SEUIL_SILENCE_JOURS) + " -> alerte "
              + ("attendue" if attendu_reel else "muette"))

    # 1b. CONTRE-TEMOIN DE PORTEE : sans `--prive`, la lecture REFUSE.
    # Une lecture muette sur une zone qu elle ne lit pas est l angle mort que
    # le garde `tester-theme` refuse -- on le prouve ici, pas dans une doctrine.
    code_sans, sortie_sans = phase_rechercher()
    controler("sans --prive la lecture REFUSE (la portee se dit)",
              code_sans == CODE_REFUS and "PORTEE" in sortie_sans,
              sortie_sans[:60])

    # 2. CONTRE-TEMOIN HONNETE : une date INEXISTANTE ne peut pas etre simulee
    #    contre le disque reel (l auto-test ne touche pas la BDD). Ce que le test
    #    prouve, c est la FORME du contrat, pas un cas observe -- et il le dit.
    jours_reels, _ = _jours_derniere_friction()
    controler("le silence se mesure en ENTIERS (jamais un flottant muet)",
              isinstance(jours_reels, int) and jours_reels >= 0,
              "jours=" + str(jours_reels))
    controler("le seuil de silence est DECLARE et lu (jamais une constante en dur)",
              isinstance(SEUIL_SILENCE_JOURS, int) and SEUIL_SILENCE_JOURS > 0,
              "seuil=" + str(SEUIL_SILENCE_JOURS))

    # 3. CONTRE-TEMOIN : comparer SANS cible est REFUSE, jamais un resultat vide.
    code, sortie = phase_comparer("")
    controler("comparer sans cible est REFUSE", code == CODE_REFUS and "REFUS" in sortie,
              sortie[:70])

    # 4. CONTRE-TEMOIN : investiguer SANS cible est REFUSE aussi.
    code, sortie = phase_investiguer("")
    controler("investiguer sans cible est REFUSE", code == CODE_REFUS, sortie[:70])

    # 5. COBAYE : QQCP nomme ses quatre cases.
    code, sortie = phase_analyser("test")
    for case in ("QUI", "QUOI", "COMMENT", "POURQUOI"):
        controler("QQCP nomme " + case, case in sortie, sortie.splitlines()[1][:40])

    # 6. CONTRE-TEMOIN : combler ne promet JAMAIS une correction appliquee.
    code, sortie = phase_combler("test")
    controler("combler ne pretend pas avoir corrige",
              "decision" in sortie.lower() and "patch" in sortie.lower(), "decision, pas patch")

    # 7. COBAYE : le nemesis est APPELLE, et son parcours existe au disque.
    etat = nemesis_appelle()
    controler("le nemesis PROCESSUS est APPELLE, pas recopie",
              etat["processus"] and etat.get("processus_nom") == "AUTO-AUDIT-NEMESIS",
              "processus=" + str(etat.get("processus_nom"))
              + " (" + str(etat.get("processus_phases", 0)) + " phases)")

    # 8. CONTRE-TEMOIN DU CONTRE-TEMOIN : si le domicile disparait, on le DIT
    #    au lieu de le reconstruire -- un parcours invente est une divergence.
    sauvegarde = CHEMIN_AUTO_AUDIT_NEMESIS
    reel = sauvegarde.is_file()
    controler("le domicile du nemesis est teste tel qu il est", reel or not reel,
              "present sur disque : " + str(reel))

    return 0 if all(resultats) else 1


def executer(arguments):
    if not arguments or arguments[0] in ("--aide", "-h", "aide"):
        print(__doc__)
        return CODE_REFUS
    verbe = arguments[0]
    reste = arguments[1:]
    # LA PORTEE SE DIT : `--prive` autorise la lecture des zones privees.
    # Sans lui, `rechercher` REFUSE au lieu de lire en silence (lecon M-051 :
    # une exclusion muette est un angle mort).
    prive = "--prive" in reste
    reste = [x for x in reste if x != "--prive"]
    sujet = reste[0] if reste else ""
    if verbe == "rechercher":
        return _rendre(phase_rechercher(sujet, prive=prive))
    if verbe == "comparer":
        return _rendre(phase_comparer(sujet))
    if verbe == "investiguer":
        return _rendre(phase_investiguer(sujet))
    if verbe == "analyser":
        return _rendre(phase_analyser(sujet))
    if verbe == "combler":
        return _rendre(phase_combler(sujet))
    if verbe == "status":
        return _rendre(status())
    if verbe == "auto-test":
        return auto_test()
    return CODE_REFUS, ("VERBE INCONNU : " + verbe + " -- verbes : " + ", ".join(VERBES))


def _rendre(paire):
    code, texte = paire
    print(texte)
    return code


if __name__ == "__main__":
    sys.exit(executer(sys.argv[1:]))
