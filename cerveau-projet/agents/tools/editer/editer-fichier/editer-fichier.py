#!/usr/bin/env python3
# -*- coding: ascii -*-
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true
"""
editer-fichier.py

Remplace une chaine par une autre dans un fichier.
Premiere occurrence par defaut, toutes avec --global.

Utilisation:
  editer-fichier.py [OPTIONS] <fichier> <ancien> <nouveau>

Options :
  --global         Remplacer toutes les occurrences
  --backup         Creer une sauvegarde .bak avant
  --dry-run        Simuler sans modifier
  --verbose        Afficher les details
  --help           Afficher cette aide
  --version        Afficher la version

Retour : 0 si succes, 1 si erreur ou si AUCUNE occurrence trouvee
         (echec explicite : jamais 0 silencieux).

Proprietaire : Vulcain (outil partage)
Version : 0.5.0
Statut : prepare
"""

import io
import os
import shutil
import sys

VERSION = "0.5.0"
STATUT = "prepare"

NOM_ATTENDU = "editer-fichier.py"

# Securite (round 3) : force la sortie en UTF-8 pour ne jamais crasher sur
# l'encodage de la console (cp1252 sous Windows avec des caracteres non-ASCII).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass  # Python < 3.7 : la console gere l'encodage comme elle peut


def verifier_nommage(nom_script):
    """Refuse l'execution si le script est renomme (protection du nommage)."""
    if nom_script != NOM_ATTENDU:
        print("[ERREUR] Nom de fichier invalide : %s" % nom_script)
        print("  Attendu : %s" % NOM_ATTENDU)
        sys.exit(2)


def afficher_aide():
    print("=== editer-fichier v%s ===" % VERSION)
    print("")
    print("Usage: editer-fichier.py [OPTIONS] <fichier> <ancien> <nouveau>")
    print("")
    print("Options :")
    print("  --global         Remplacer toutes les occurrences")
    print("  --backup         Creer une sauvegarde .bak avant")
    print("  --dry-run        Simuler sans modifier")
    print("  --verbose        Afficher les details")
    print("  --help           Afficher cette aide")
    print("  --version        Afficher la version")
    print("")
    print("Exemples :")
    print("  editer-fichier.py fichier.md \"ancien\" \"nouveau\"")
    print("  editer-fichier.py --global fichier.md \"texte\" \"remplacement\"")
    print("")
    print("Retour : 0 si succes, 1 si erreur ou si AUCUNE occurrence trouvee.")


def afficher_messages_info(messages):
    """MESSAGES INFORMATIONNELS (regle immuable v0.3.0) : section
    '=== MESSAGES POUR L AGENT ===' avec une ligne ' > ' par message."""
    if not messages:
        return
    print("")
    print("=== MESSAGES POUR L AGENT ===")
    for message in messages:
        print("  > %s" % message)


def verrouiller_habilitation(agent, cible, audit=False):
    """Appelle proteger-verrou-habilitation (v0.2.1) avec la CIBLE : si le
    fichier est dans tester/tests/, seule morpheus peut le modifier (cle
    exclusive - regle immuable). Retourne (code, message)."""
    courant = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isfile(os.path.join(courant, "AGENTS.md")):
            break
        parent = os.path.dirname(courant)
        if parent == courant:
            return (2, "[ERREUR] Racine du projet introuvable (AGENTS.md absent)")
        courant = parent
    verrou = os.path.join(
        courant, "cerveau-projet", "agents", "tools", "proteger",
        "proteger-verrou-habilitation", "proteger-verrou-habilitation.py")
    if not os.path.isfile(verrou):
        return (2, "[ERREUR] Verrou introuvable : %s" % verrou)
    import subprocess
    cmd = [sys.executable, verrou, "--agent", agent, "--outil", "editer-fichier",
           "--cible", cible]
    if audit:
        cmd.append("--audit")
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    message = (r.stdout + r.stderr).strip()
    return (r.returncode, message)


# --- VERROU CIBLE TOOLS (v0.4.4, decision utilisateur 2026-08-22) ---
HABILITES_TOOLS = {
    "vulcain": None,          # tout tools/
    "morpheus": "tester" + os.sep + "tests",   # tests uniquement
    "buffy": None,            # via exceptions fichiers ci-dessous
}
FICHIERS_EXCEPTIONS = ("index-tools.md", "outil-template")

def verifier_cible_tools(chemin, agent):
    """Si la cible est sous agents/tools/, l agent doit etre habilite :
    vulcain = tout tools/ ; morpheus = tester/tests/ ; buffy = index-tools.md
    et outil-template*. Tout autre agent est bloque (domaine exclusif Vulcain).
    Retourne (code, message)."""
    if chemin is None:
        return (0, "")
    normalise = os.path.normpath(os.path.abspath(chemin)).replace("\\", "/")
    marqueur = "/agents/tools/"
    marqueur_combos = "/cerveau-projet/combos/"
    sous_combos = marqueur_combos in normalise.replace(os.sep, "/")
    if marqueur not in normalise.replace(os.sep, "/") and not sous_combos:
        return (0, "")
    if sous_combos:
        # DEFINITIONS DE COMBOS : VULCAIN exclusivement
        if agent != "vulcain":
            return (1, "[BLOQUE] Definition de combo sous cerveau-projet/combos "
                       "refusee : domaine EXCLUSIF de vulcain (agent appelant : "
                       "%s ; fichier : %s). Les combos sont plus puissants que "
                       "les outils." % (agent or "?",
                                        os.path.basename(chemin)))
        return (0, "")
    _dans_git = ("/agents/tools/git/" in
                 normalise.replace(os.sep, "/"))
    if _dans_git:
        if agent == "hades":
            return (0, "")
        return (1, "[BLOQUE] Categorie git reservee a HADES exclusivement (agent appelant : %s)." % (agent or "?"))
    if agent == "vulcain":
        return (0, "")
    relatif = normalise.split(marqueur, 1)[1]
    nom_fichier = os.path.basename(relatif)
    if agent == "buffy" and (nom_fichier in FICHIERS_EXCEPTIONS
                             or nom_fichier.startswith("outil-template")):
        return (0, "")
    if agent == "morpheus" and relatif.replace(os.sep, "/").startswith("tester/tests"):
        return (0, "")
    return (1, "[BLOQUE] Ecriture dans agents/tools/ refusee : domaine "
               "EXCLUSIF de vulcain (agent appelant : %s ; fichier : %s). "
               "Exceptions : morpheus = tester/tests/, buffy = index-tools.md "
               "+ outil-template*." % (agent or "?", relatif))

def verifier_perimetre(chemin, agent):
    """PERIMETRE PAR AGENT (v0.5.0, decision utilisateur 2026-08-22) :
    si cerveau-projet/agents/<agent>/perimetre.json existe, toute cible doit
    matcher au moins un motif (glob relatif racine projet). Sinon BLOQUE.
    Perimetre absent -> regles anterieures (verrou cible tools)."""
    if chemin is None or not agent:
        return (0, "")
    import glob as _glob
    import json as _json
    p = os.path.join("cerveau-projet", "agents", agent, "perimetre.json")
    if not os.path.isfile(p):
        return (0, "")
    try:
        with io.open(p, encoding="utf-8") as fh:
            donnees = _json.load(fh)
    except Exception:
        return (1, "[BLOQUE] perimetre.json de %s illisible" % agent)
    import fnmatch as _fn
    motifs = donnees.get("fichiers", [])
    normalise = os.path.normpath(os.path.abspath(chemin)).replace("\\", "/")
    racine = os.path.normpath(os.getcwd()).replace("\\", "/")
    if normalise.startswith(racine + "/"):
        relatif_racine = normalise[len(racine) + 1:]
    else:
        relatif_racine = normalise
    for m in motifs:
        motif_rel = m.replace("\\", "/")
        if relatif_racine == motif_rel:
            return (0, "")
        if _fn.fnmatch(relatif_racine, motif_rel):
            return (0, "")
    return (1, "[BLOQUE] %s hors du PERIMETRE de %s (voir "
               "cerveau-projet/agents/%s/perimetre.json)" % (
                   os.path.basename(chemin), agent, agent))

def main(argv):
    verifier_nommage(os.path.basename(sys.argv[0]))

    fichier = ""
    ancien = ""
    nouveau = ""
    global_remplacement = False
    backup = False
    dry_run = False
    verbose = False
    help_demande = False
    agent = ""

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--global":
            global_remplacement = True
        elif arg == "--backup":
            backup = True
        elif arg == "--dry-run":
            dry_run = True
        elif arg == "--verbose":
            verbose = True
        elif arg == "--agent":
            if i + 1 < len(argv):
                agent = argv[i + 1]
                i += 1
        elif arg in ("--aide", "--help", "-h"):
            help_demande = True
        elif arg == "--version":
            print("editer-fichier v%s (%s)" % (VERSION, STATUT))
            return 0
        elif arg.startswith("-"):
            print("[ERREUR] Option inconnue : %s" % arg)
            afficher_aide()
            return 1
        else:
            if not fichier:
                fichier = arg
            elif not ancien:
                ancien = arg
            elif not nouveau:
                nouveau = arg
        i += 1

    if help_demande:
        afficher_aide()
        return 0

    if not fichier or not ancien:
        print("[ERREUR] Arguments manquants")
        afficher_aide()
        return 1

    # PERIMETRE PAR AGENT (v0.5.0) : si perimetre.json existe pour l agent,
    # la cible doit y matcher (sinon BLOQUE). Prime sur tout le reste.
    code_p, msg_p = verifier_perimetre(fichier, agent)
    if code_p != 0:
        print(msg_p)
        return 1

    # VERROU CIBLE TOOLS (v0.4.4, decision utilisateur 2026-08-22) : toute
    # cible sous agents/tools/ exige un agent HABILITE (vulcain = tout,
    # morpheus = tester/tests/, buffy = index-tools.md + outil-template*).
    # Le controle s applique MEME sans --agent (breche fermee).
    code_tools, msg_tools = verifier_cible_tools(fichier, agent)
    if code_tools != 0:
        print(msg_tools)
        return 1

    # VERROU D HABILITATION (v0.2.1) : la modification d un fichier de test
    # (tester/tests/) est EXCLUSIVE a morpheus. Pour une cible sous tools/,
    # la verification CIBLE TOOLS ci-dessus REMPLACE ce verrou-carte (sinon
    # vulcain serait bloque par sa propre exclusivite).
    sous_tools = "/agents/tools/" in os.path.abspath(
        fichier).replace(os.sep, "/")
    if agent and not sous_tools:
        code_verrou, msg_verrou = verrouiller_habilitation(agent, fichier)
        if code_verrou != 0:
            print(msg_verrou)
            return 1

    # Securite (round 3) : octet nul dans le chemin -> refus explicite
    if "\x00" in fichier:
        print("[ERREUR] Chemin non sur (octet nul present)")
        return 1

    # Securite (round 3) : refus de modifier a travers un lien symbolique
    # (l'ecriture suivrait le lien vers la cible a l'insu de l'agent)
    if os.path.islink(fichier):
        print("[ERREUR] Chemin est un lien symbolique (refus securite): %s" % fichier)
        return 1

    if not os.path.isfile(fichier):
        print("[ERREUR] Fichier non trouve: %s" % fichier)
        return 1

    # Lecture robuste (round 3) : UTF-8 puis fallback latin-1, jamais de crash
    contenu = None
    try:
        with io.open(fichier, encoding="utf-8-sig") as fh:
            contenu = fh.read()
    except (UnicodeDecodeError, OSError):
        try:
            with io.open(fichier, encoding="latin-1") as fh:
                contenu = fh.read()
        except Exception:
            contenu = None
    if contenu is None:
        print("[ERREUR] Impossible de lire le fichier : %s" % fichier)
        return 1

    if ancien not in contenu:
        print("[ERREUR] Aucune occurrence de '%s' dans %s" % (ancien, fichier))
        print("  (verifiez l'indentation exacte et le contenu de la chaine)")
        return 1

    if global_remplacement:
        nb = contenu.count(ancien)
    else:
        nb = 1

    if dry_run:
        print("[DRY-RUN] %d occurrence(s) trouvee(s)" % nb)
        for num, ligne in enumerate(contenu.split("\n"), 1):
            if ancien in ligne:
                print("  %d: %s" % (num, ligne.strip()))
        return 0

    if backup:
        shutil.copy2(fichier, fichier + ".bak")
        if verbose:
            print("[INFO] Sauvegarde: %s.bak" % fichier)

    # UNE SEULE PASSE (performance round 2) : le test d'existence 'ancien in
    # contenu' est fait avant (aucun double scan complet du fichier). Pour un
    # remplacement simple, replace(..., 1) ne scanne que jusqu'a la premiere
    # occurrence ; count n'est calcule que pour --global.
    if global_remplacement:
        nouveau_contenu = contenu.replace(ancien, nouveau)
    else:
        nouveau_contenu = contenu.replace(ancien, nouveau, 1)

    with io.open(fichier, "w", encoding="utf-8", newline="") as fh:
        fh.write(nouveau_contenu)

    if verbose:
        print("[OK] %d occurrence(s) remplacee(s) dans %s" % (nb, fichier))

    # MESSAGES INFORMATIONNELS (regle immuable v0.3.0) : selon le type de
    # fichier modifie, rappeler les fichiers compagnons a mettre a jour.
    nom_base = os.path.basename(fichier)
    messages = []
    if nom_base.endswith(".py") or nom_base.endswith(".sh"):
        messages.append("script modifie : bumpe la version (mettre-a-jour-versions) + .md de l outil a jour")
        messages.append("script modifie : adapter les tests qui pinent la version (Morpheus)")
    elif nom_base.endswith(".json") and "parcours" in fichier:
        messages.append("carte modifiee : verifier valider-cartes-decision + synchroniser la fiche (Pattern 14)")
    elif nom_base.endswith(".md"):
        messages.append("document modifie : verifier la coherence avec index-tools.md / README si outil")
    else:
        messages.append("fichier modifie : verifier les fichiers qui le referencent (tests, index, docs)")
    afficher_messages_info(messages)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
