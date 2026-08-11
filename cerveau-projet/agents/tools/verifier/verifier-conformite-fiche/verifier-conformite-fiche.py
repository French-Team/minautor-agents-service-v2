#!/usr/bin/env python3
# -*- coding: ascii -*-
"""
verifier-conformite-fiche.py
Verifie qu'une fiche agent (agents/<agent>/<agent>.md) est conforme au
template de fiche (agents/fiche-agent-template.md).

Principe : les sections '## X' du TEMPLATE sont lues DYNAMIQUEMENT. L'outil
reste donc valide apres toute mise a jour du template (ajout/suppression de
section). Cibles possibles :
  --agent <nom>          : une seule fiche
  --agents <a,b,c>       : selection de fiches
  --tous                 : les 11 fiches agents

MODELE PAR ROLE (v0.2.0) : chaque fiche doit contenir le NOYAU obligatoire
(fiche-agent-template.md) PLUS les sections de la VARIANTE de sa famille
(fiche-template-variante-cerveau.md pour les agents cerveau-projet,
fiche-template-variante-trio.md pour le trio redaction). La famille est :
  1. determinee par l'option --variante <cerveau-projet|trio> si fournie ;
  2. sinon lue DEPUIS le frontmatter de la fiche (cle 'famille:').

Pour chaque fiche, l'outil verifie :
  1. Frontmatter YAML present (--- en debut + cle 'agent:' ou 'nom-agent:')
  2. Chaque section du NOYAU et de la VARIANTE presente dans la fiche
     (SECTIONS MANQUANTES = ecarts BLOQUANTS)
  3. Sections en plus (ni noyau ni variante -- specifiques au role de
     l'agent, TOLEREES et NON BLOQUANTES, signalees en avertissement ~)
  4. Ordre des sections : verifie SEPAREMENT a l'interieur du noyau et de
     la variante (les fiches peuvent intercaler leurs sections specifiques)

Verdict CONFORME = 0 ecart bloquant (les sections specifiques tolerees
n'empechent pas la conformite).

Sortie : verdict par fiche (CONFORME / ECARTS) + rapport global.
Option --rapport <fichier.md> : ecrit un rapport markdown.
Option --dry-run : analyse seule (aucun fichier modifie -- l'outil ne modifie
jamais rien de toute facon, l'option est maintenue pour la coherence).
"""
import argparse
import io
import os
import sys

VERSION = "0.2.1"
RACINE = os.path.dirname(os.path.abspath(__file__))
while not os.path.isdir(os.path.join(RACINE, "cerveau-projet")):
    RACINE = os.path.dirname(RACINE)

CHEMIN_TEMPLATE = os.path.join(RACINE, "cerveau-projet", "agents",
                               "fiche-agent-template.md")
CHEMIN_VARIANTES = {
    "cerveau-projet": os.path.join(RACINE, "cerveau-projet", "agents",
                                   "fiche-template-variante-cerveau.md"),
    "trio": os.path.join(RACINE, "cerveau-projet", "agents",
                         "fiche-template-variante-trio.md"),
}
DOSSIER_AGENTS = os.path.join(RACINE, "cerveau-projet", "agents")

# Les 11 agents du cerveau-projet (sans les meta-fichiers)
AGENTS_DEFAUT = ["athena", "atlas", "buffy", "cerberus", "clio", "janus",
                 "minerve", "morpheus", "promethee", "themis", "vulcain"]

# Famille par defaut si la fiche ne declare rien et --variante absent
FAMILLES_DEFAUT = {
    "cerberus": "cerveau-projet", "buffy": "cerveau-projet",
    "vulcain": "cerveau-projet", "morpheus": "cerveau-projet",
    "janus": "cerveau-projet", "atlas": "cerveau-projet",
    "themis": "cerveau-projet", "clio": "cerveau-projet",
    "athena": "trio", "promethee": "trio", "minerve": "trio",
}


def lire_fichier(chemin):
    """Lit un fichier texte (UTF-8) et renvoie ses lignes."""
    with io.open(chemin, encoding="utf-8", errors="replace") as fh:
        return fh.read().split("\n")


def sections_du_fichier(chemin):
    """Extrait les titres '## X' d'un fichier dans l'ordre."""
    sections = []
    for ligne in lire_fichier(chemin):
        if ligne.startswith("## "):
            sections.append(ligne.strip())
    return sections


def famille_de_la_fiche(chemin_fiche):
    """Lit la cle 'famille:' du frontmatter de la fiche (None si absente)."""
    lignes = lire_fichier(chemin_fiche)[:60]
    for l in lignes:
        if l.strip().startswith("famille:"):
            val = l.split(":", 1)[1].strip().strip('"').strip("'")
            if val in CHEMIN_VARIANTES:
                return val
    return None


def frontmatter_valide(chemin_fiche):
    """Verifie la presence du frontmatter YAML (--- en debut + cle agent)."""
    lignes = lire_fichier(chemin_fiche)
    if not lignes or lignes[0].strip() != "---":
        return False, "pas de delimiteur --- en premiere ligne"
    tete = "\n".join(lignes[:60])
    if "agent:" not in tete and "nom-agent" not in tete:
        return False, "cle 'agent:' ou 'nom-agent:' absente du frontmatter"
    # un deuxieme --- doit cloturer le frontmatter (fenetre large : 100 lignes,
    # les fiches peuvent avoir un YAML detaille suivi des sections)
    cloture = [i for i, l in enumerate(lignes[:100])
               if l.strip() == "---" and i > 0]
    if not cloture:
        return False, "frontmatter non clos (pas de --- de cloture dans les 100 premieres lignes)"
    return True, ""


def verifier_ordre(sections_attendues, sections_fiche, nom_bloc):
    """Verifie l'ordre des sections attendues presentes dans la fiche."""
    ecarts = []
    positions = {s: i for i, s in enumerate(sections_fiche)}
    for i in range(len(sections_attendues) - 1):
        s1, s2 = sections_attendues[i], sections_attendues[i + 1]
        if s1 in positions and s2 in positions:
            if positions[s1] > positions[s2]:
                ecarts.append("ORDRE %s: '%s' devrait preceder '%s'"
                              % (nom_bloc, s1, s2))
    return ecarts


def verifier_fiche(chemin_fiche, sections_noyau, sections_variante):
    """Verifie une fiche contre noyau + variante.

    Retourne (ok, ecarts, avertissements) :
      - ok               : True si aucun ecart BLOQUANT
      - ecarts           : ecarts bloquants (frontmatter, manquantes, ordre)
      - avertissements   : sections specifiques (tolerees -- non bloquantes)
    """
    ecarts = []
    avertissements = []
    if not os.path.isfile(chemin_fiche):
        return False, ["fichier introuvable: %s" % chemin_fiche], []

    # 1. Frontmatter
    ok_front, raison = frontmatter_valide(chemin_fiche)
    if not ok_front:
        ecarts.append("FRONTMATTER: %s" % raison)

    sections_fiche = sections_du_fichier(chemin_fiche)
    autorisees = set(sections_noyau) | set(sections_variante)

    # 2. Sections manquantes (noyau + variante) -- BLOQUANT
    manquantes = []
    for s in list(sections_noyau) + list(sections_variante):
        if s not in sections_fiche:
            manquantes.append(s)
    if manquantes:
        ecarts.append("SECTIONS MANQUANTES: %s" % "; ".join(manquantes))

    # 3. Sections en plus (ni noyau ni variante -- TOLEREES, non bloquantes)
    en_plus = [s for s in sections_fiche if s not in autorisees]
    if en_plus:
        avertissements.append("SECTIONS SPECIFIQUES (tolerees): %s" % "; ".join(en_plus))

    # 4. Ordre (separe : noyau puis variante) -- BLOQUANT
    ecarts.extend(verifier_ordre(sections_noyau, sections_fiche, "NOYAU"))
    ecarts.extend(verifier_ordre(sections_variante, sections_fiche, "VARIANTE"))

    return (not ecarts), ecarts, avertissements


def cibles_agents(args):
    """Determine la liste des agents cibles selon le mode choisi."""
    if args.tous:
        return AGENTS_DEFAUT
    if args.agents:
        return [a.strip() for a in args.agents.split(",") if a.strip()]
    if args.agent:
        return [args.agent]
    return []


def main():
    global VERSION
    parser = argparse.ArgumentParser(
        description="Verifier la conformite des fiches agents au template (noyau + variante)")
    cible = parser.add_mutually_exclusive_group()
    cible.add_argument("--agent", metavar="NOM",
                       help="Verifier UNE fiche agent (ex: buffy)")
    cible.add_argument("--agents", metavar="A,B,C",
                       help="Verifier une SELECTION de fiches (ex: buffy,cerberus)")
    cible.add_argument("--tous", action="store_true",
                       help="Verifier les %d fiches agents" % len(AGENTS_DEFAUT))
    parser.add_argument("--variante", metavar="FAMILLE",
                        choices=sorted(CHEMIN_VARIANTES.keys()),
                        help="Famille (cerveau-projet|trio). Si absent: lue du "
                             "frontmatter de la fiche (cle famille:), defaut par agent")
    parser.add_argument("--template", metavar="CHEMIN",
                        default=CHEMIN_TEMPLATE,
                        help="Chemin du template (defaut: fiche-agent-template.md)")
    parser.add_argument("--rapport", metavar="FICHIER",
                        help="Ecrire le rapport markdown dans ce fichier")
    parser.add_argument("--dry-run", action="store_true",
                        help="Analyse seule (l'outil ne modifie jamais rien)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Afficher les details")
    parser.add_argument("--version", action="store_true",
                        help="Afficher la version")
    args = parser.parse_args()

    if args.version:
        print("verifier-conformite-fiche v%s" % VERSION)
        return 0

    if not os.path.isfile(args.template):
        print("[ERREUR] Template introuvable: %s" % args.template)
        return 1

    sections_noyau = sections_du_fichier(args.template)
    if not sections_noyau:
        print("[ERREUR] Aucune section '## ' trouvee dans le template: %s"
              % args.template)
        return 1

    # Precharge les sections des variantes (si les fichiers existent)
    sections_variantes = {}
    for famille, chemin in CHEMIN_VARIANTES.items():
        if os.path.isfile(chemin):
            sections_variantes[famille] = sections_du_fichier(chemin)
        else:
            sections_variantes[famille] = []

    cibles = cibles_agents(args)
    if not cibles:
        print("[ERREUR] Choisir une cible: --agent <nom> | --agents <a,b,c> "
              "| --tous")
        return 1

    print("=== verifier-conformite-fiche v%s ===" % VERSION)
    print("Noyau   : %s (%d sections)" % (args.template, len(sections_noyau)))
    print("Cibles  : %d fiche(s): %s" % (len(cibles), ", ".join(cibles)))
    if args.variante:
        print("Variante: %s (%d sections)"
              % (args.variante, len(sections_variantes[args.variante])))
    if args.verbose:
        print("Sections du noyau :")
        for s in sections_noyau:
            print("  - %s" % s)
        for famille, secs in sections_variantes.items():
            if secs:
                print("Sections variante %s :" % famille)
                for s in secs:
                    print("  - %s" % s)
    print("")

    lignes_rapport = [
        "# Rapport conformite des fiches agents",
        "",
        "Date      : %s" % "2026-08-11",
        "Outil     : verifier-conformite-fiche v%s" % VERSION,
        "Noyau     : %s" % args.template,
        "Sections noyau : %d (lues dynamiquement)" % len(sections_noyau),
        "Note      : sections specifiques (ni noyau ni variante) = tolerees, non bloquantes",
        "Cibles    : %d fiche(s)" % len(cibles),
        "",
        "| Agent | Variante | Verdict | Ecarts |",
        "|---|---|---|---|",
    ]

    nb_ok = 0
    nb_ko = 0
    for agent in cibles:
        chemin = os.path.join(DOSSIER_AGENTS, agent, "%s.md" % agent)
        # determination de la famille : --variante > frontmatter > defaut
        famille = args.variante
        if famille is None:
            famille = famille_de_la_fiche(chemin)
        if famille is None:
            famille = FAMILLES_DEFAUT.get(agent, "")
        secs_var = sections_variantes.get(famille, [])
        ok, ecarts, avertissements = verifier_fiche(chemin, sections_noyau, secs_var)
        affiche_famille = famille if famille else "-"
        if ok:
            nb_ok += 1
            print("[OK] %s (%s) : CONFORME" % (agent, affiche_famille))
            for a in avertissements:
                print("     ~ %s" % a)
            lignes_rapport.append("| %s | %s | CONFORME | - |"
                                  % (agent, affiche_famille))
        else:
            nb_ko += 1
            print("[KO] %s (%s) : ECARTS" % (agent, affiche_famille))
            for e in ecarts:
                print("     - %s" % e)
            for a in avertissements:
                print("     ~ %s" % a)
            lignes_rapport.append("| %s | %s | ECARTS | %s |"
                                  % (agent, affiche_famille, "; ".join(ecarts)))

    print("")
    print("=== RESULTAT : %d CONFORME / %d ECARTS (sur %d fiche(s)) ==="
          % (nb_ok, nb_ko, len(cibles)))

    lignes_rapport.append("")
    lignes_rapport.append("=== RESULTAT : %d CONFORME / %d ECARTS ==="
                          % (nb_ok, nb_ko))

    if args.rapport:
        contenu = "\n".join(lignes_rapport) + "\n"
        with io.open(args.rapport, "w", encoding="utf-8", newline="") as fh:
            fh.write(contenu)
        print("[RAPPORT] ecrit dans %s" % args.rapport)

    return 1 if nb_ko else 0


if __name__ == "__main__":
    sys.exit(main())
