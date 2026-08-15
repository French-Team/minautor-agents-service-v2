#!/usr/bin/env python3
# -*- coding: ascii -*-
# detecter-divergences-version.py
# Detecte les spec/ dont la version diverge de celle du .py associe
# (regle des 5 fichiers, lecon Vulcain / controle Janus 2026-08-09).
# Version : 0.2.0
# Statut : ebauche
# v0.2.0 : champ spec 'Version outil' prioritaire (cas spec de conventions
# dont la version documente des patterns au-dela de l outil, ex: guider-
# parcours spec 0.6.2 / outil 0.5.0) ; constante VERSION ajoutee (resout
# le SANS VERSION de sa propre spec). Round 11 coherence documentaire.
# identite:
#   type: outil
#   appartient_a: commun
#   commun: true

"""
detecter-divergences-version.py
detecter-divergences-version

Usage:
  detecter-divergences-version.py [OPTIONS]
"""

"""detecter-divergences-version.py

Scanne les dossiers spec/ sous une racine, extrait la version declaree
dans chaque spec (tous les formats : en-tete, tableau frontmatter,
versionning, tableau historique) et la croise avec la version du .py
associe dans le meme dossier outil (VERSION = ...).

Verdicts :
  ALIGNE               : version spec == version py (ou meme base)
  DIVERGENT (base)     : version spec != version py (base differente)
  DIVERGENT (suffixe)  : meme base (X.Y.Z) mais suffixe different
  SANS VERSION         : version spec non trouvee ou version py absente
  SANS PY              : aucun .py dans le dossier outil

Lecons Janus integrees :
  1. La version d'EN-TETE de la spec prime sur le tableau d'historique.
  2. Distinguer divergence de BASE vs de SUFFIXE.
  3. Cas particulier guider-parcours (spec versionne les patterns,
     pas l'outil) : le rapporter mais ne pas conclure seul.

v0.2.0 (round 11) : une spec peut declarer **Version outil** : X.Y.Z pour
comparer la version du .py contre la version de l OUTIL (au lieu de la
version de la spec, qui documente les conventions/patterns). Si le champ
est present, il PRIME sur la version de la spec pour le verdict.
"""

import argparse
import io
import os
import re
import sys

VERSION = "0.2.0"


def extraire_version_spec(chemin_spec):
    """Version declaree dans une spec (formats multiples).

    Ordre de priorite (lecon Janus) :
      0. **Version outil** : X.Y.Z (v0.2.0, round 11) : champ explicite
         declarant la version de l OUTIL associe (spec de conventions dont
         la version documente des patterns au-dela de l outil, ex:
         guider-parcours spec 0.6.2 / outil 0.5.0). Il PRIME sur la version
         de la spec pour le verdict.
      1. En-tete : **Version :** X / **Version** : X / Version: X
      2. Tableau frontmatter : | **Version** | X |
      3. Section Versionning : | Version | Date | / 1re ligne X | ...
      4. Titre : # Spec -- ... vX.Y.Z
      5. Tableau historique : | Date | Version | Auteur | (derniere ligne)
    """
    try:
        with io.open(chemin_spec, encoding='utf-8', errors='replace') as fh:
            txt = fh.read()
    except (IOError, OSError):
        return None
    lignes = txt.split('\n')

    # 0) Version outil (30 premieres lignes, v0.2.0) : PRIME sur la version
    #    de la spec (cas spec de conventions, ex: guider-parcours)
    for l in lignes[:30]:
        m = re.search(
            r'\*{0,2}Version outil\*{0,2}\s*:?\s*\*{0,2}\s*'
            r'([0-9]+\.[0-9]+\.[0-9]+[0-9a-zA-Z_.-]*)', l)
        if m:
            return m.group(1)

    # 1) En-tete (30 premieres lignes)
    for l in lignes[:30]:
        m = re.search(
            r'\*{0,2}Version\*{0,2}\s*:?\s*\*{0,2}\s*'
            r'([0-9]+\.[0-9]+\.[0-9]+[0-9a-zA-Z_.-]*)', l)
        if m and not re.search(r'\|\s*Date\s*\|', l):
            return m.group(1)

    # 2) Tableau frontmatter : | **Version** | 0.2.2 |
    m = re.search(
        r'\|\s*\*{0,2}Version\*{0,2}\s*\|\s*([0-9]+\.[0-9]+\.[0-9]+[0-9a-zA-Z_.-]*)',
        txt[:2000])
    if m:
        return m.group(1)

    # 3) Section Versionning : | Version | Date | ... puis lignes X | date |
    m = re.search(
        r'\|\s*Version\s*\|\s*Date\s*\|(?:\s*Changements\s*\|)?'
        r'\s*\n\s*\|\s*-+\s*\|\s*-+\s*\|'
        r'\s*\n\s*\|\s*([0-9]+\.[0-9]+\.[0-9]+[0-9a-zA-Z_.-]*)\s*\|', txt)
    if m:
        return m.group(1)

    # 4) Titre : # Spec -- ... vX.Y.Z
    m = re.search(r'v([0-9]+\.[0-9]+\.[0-9]+[0-9a-zA-Z_.-]*)', txt[:500])
    if m:
        return m.group(1)

    # 5) Tableau historique (derniere ligne non vide)
    for l in reversed(lignes):
        m = re.search(
            r'\|\s*[0-9]{4}-[0-9]{2}-[0-9]{2}\s*\|\s*'
            r'([0-9]+\.[0-9]+\.[0-9]+[0-9a-zA-Z_.-]*)\s*\|', l)
        if m:
            return m.group(1)

    return None


def extraire_version_py(chemin_py):
    """Version VERSION = 'X' dans un .py (recherche sur les 3000 premiers caracteres)."""
    try:
        with io.open(chemin_py, encoding='utf-8', errors='replace') as fh:
            contenu = fh.read()
    except (IOError, OSError):
        return None
    m = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', contenu[:3000])
    return m.group(1) if m else None


def base_version(v):
    """Base X.Y.Z sans suffixe (lecon Janus : distinguer base/suffixe)."""
    m = re.match(r'([0-9]+\.[0-9]+\.[0-9]+)', v or '')
    return m.group(1) if m else (v or '')


def scanner(racine):
    """Parcourt les spec/ sous racine et croise les versions."""
    resultats = []
    for dossier, sous_dossiers, fichiers in os.walk(racine):
        sous_dossiers[:] = [d for d in sous_dossiers if d != '__pycache__']
        if os.path.basename(dossier) != 'spec':
            continue
        outil_dir = os.path.dirname(dossier)
        spec_files = [f for f in fichiers if f.endswith('.md')]
        py_files = [f for f in os.listdir(outil_dir) if f.endswith('.py')]
        if not spec_files:
            continue
        for spec_f in sorted(spec_files):
            spec_chemin = os.path.join(dossier, spec_f)
            v_spec = extraire_version_spec(spec_chemin)
            if not py_files:
                verdict = 'SANS PY'
                v_py = None
            else:
                v_py = None
                for py_f in py_files:
                    v_py = extraire_version_py(os.path.join(outil_dir, py_f))
                    if v_py:
                        break
                if v_spec and v_py:
                    if v_spec == v_py:
                        verdict = 'ALIGNE'
                    elif base_version(v_spec) == base_version(v_py):
                        verdict = 'DIVERGENT (suffixe)'
                    else:
                        verdict = 'DIVERGENT (base)'
                else:
                    verdict = 'SANS VERSION'
            resultats.append({
                'outil': os.path.basename(outil_dir),
                'spec': spec_f,
                'v_spec': v_spec,
                'v_py': v_py,
                'verdict': verdict,
            })
    return resultats


def afficher(resultats, colonnes_larges=False):
    """Affiche le tableau des resultats + synthese."""
    print('%-30s %-42s %-14s %-14s %s' % (
        'OUTIL', 'SPEC', 'V.SPEC', 'V.PY', 'VERDICT'))
    print('-' * 110)
    for r in resultats:
        print('%-30s %-42s %-14s %-14s %s' % (
            r['outil'][:30], r['spec'][:42],
            r['v_spec'] or '-', r['v_py'] or '-', r['verdict']))
    total = len(resultats)
    print('')
    print('SYNTHESE : %d spec | %d ALIGNEES | %d DIVERGENTES | %d SANS VERSION/SPEC' % (
        total,
        sum(1 for r in resultats if r['verdict'] == 'ALIGNE'),
        sum(1 for r in resultats if 'DIVERGENT' in r['verdict']),
        sum(1 for r in resultats if r['verdict'] not in ('ALIGNE', 'DIVERGENT (base)', 'DIVERGENT (suffixe)')),
    ))


def main():
    parser = argparse.ArgumentParser(
        prog='detecter-divergences-version',
        description='Detecte les spec/ dont la version diverge de leur .py (regle des 5 fichiers).')
    parser.add_argument('--racine', default='cerveau-projet',
                        help='Racine du scan (defaut: cerveau-projet)')
    parser.add_argument('--liste', action='store_true',
                        help='Lister les spec trouvees sans croiser')
    parser.add_argument('--export', metavar='FICHIER',
                        help='Exporter le rapport en markdown')
    parser.add_argument('--version', action='store_true',
                        help='Afficher la version')
    parser.add_argument("--aide", action="help",
                  help="Afficher cette aide (alias de -h)")
    args = parser.parse_args()

    if args.version:
        print('detecter-divergences-version v%s' % VERSION)
        return 0

    if not os.path.isdir(args.racine):
        print('ERREUR : la racine %s n existe pas' % args.racine)
        return 1

    resultats = scanner(args.racine)

    if args.liste:
        for r in resultats:
            print('  %-30s %s' % (r['outil'], r['spec']))
        print('TOTAL : %d spec' % len(resultats))
        return 0

    afficher(resultats)

    if args.export:
        try:
            with io.open(args.export, 'w', encoding='utf-8', newline='') as fh:
                fh.write('# Rapport detecter-divergences-version\n\n')
                fh.write('| Outil | Spec | V.Spec | V.Py | Verdict |\n')
                fh.write('|---|---|---|---|---|\n')
                for r in resultats:
                    fh.write('| %s | %s | %s | %s | %s |\n' % (
                        r['outil'], r['spec'], r['v_spec'] or '-',
                        r['v_py'] or '-', r['verdict']))
            print('Rapport exporte : %s' % args.export)
        except (IOError, OSError) as e:
            print('ERREUR export : %s' % e)
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
