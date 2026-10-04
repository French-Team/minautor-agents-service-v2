#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
espion-sondes-optimus.py -- L AGENT NOTE SES PROPRES SONDES (axe B, 2026-09-23)

POURQUOI CE DOMICILE EXISTE
Le createur voit des tracebacks dans les resultats et ne peut pas distinguer une
VRAIE panne d une SONDE qui n a pas survecu a son environnement. Aucune porte
n enregistrait les commandes de l agent : la question ne pouvait donc PAS se
repondre par une mesure (mesure du 2026-09-23 : bdd-activites porte 4 sections --
missions, alertes, passes, decisions -- et AUCUNE ne dit ce que l agent a TAPE).

CE QU IL MESURE
Chaque sonde passee par lui : sa commande, son code de sortie, et si un traceback
en est sorti. Le CRITERE du traceback est DECLARE une seule fois ici, jamais devine.

CE QU IL FAIT EN PLUS, ET C EST LE REMEDE
Une sonde qui plante REND UNE LIGNE (type d erreur + derniere ligne) ; la pile est
ECRITE au registre, tronquee et DITE tronquee. Une sonde ne peut donc plus se lire
comme une panne : c est exactement ce que le createur a demande.

PORTEE, DITE UNE FOIS POUR TOUTES (elle borne TOUT ce rapport)
Cet espion ne voit QUE les sondes passees par lui. Une sonde lancee a cote n est NI
notee NI accusee : c est pourquoi le rapport dit toujours sur COMBIEN de sondes il
parle. Un registre vide ne dit pas qu il n y a pas de sonde, il dit qu aucune n a
ete NOTEE -- un taux ne se calcule pas sur zero.

Usage:
  python espion-sondes-optimus.py executer -- <commande...>
  python espion-sondes-optimus.py rapport [--n N]
  python espion-sondes-optimus.py auto-test
Codes de sortie : le code de la sonde ; 3 = un traceback a ete capture ;
2 = mauvais usage de l espion. L espion SIGNALE, il ne repare jamais.
'''

import json
import subprocess

import sys
from pathlib import Path

# --- DOMICILE DU LANCEMENT (EO-430 / MO-414, vague 4 du lot) -----------------
# La racine se DETECTE par marqueur (MO-088 : aucun parents[N] nu) : on remonte
# jusqu au dossier `matrix`, et on REFUSE plutot que de deviner (garde-foi L-006).
_RACINE_LANCEMENT = Path(__file__).resolve().parent
while _RACINE_LANCEMENT.name != "matrix":
    if _RACINE_LANCEMENT.parent == _RACINE_LANCEMENT:
        raise RuntimeError("racine `matrix` introuvable en remontant depuis " + __file__)
    _RACINE_LANCEMENT = _RACINE_LANCEMENT.parent
_REPERTOIRE_COMMUN_LANCEMENT = _RACINE_LANCEMENT / "matrice" / "data" / "commun"
if not (_REPERTOIRE_COMMUN_LANCEMENT / "lancement.py").is_file():
    raise RuntimeError("Structure inattendue : " + str(_REPERTOIRE_COMMUN_LANCEMENT)
                       + " ne porte pas le domicile du lancement")
if str(_REPERTOIRE_COMMUN_LANCEMENT) not in sys.path:
    sys.path.insert(0, str(_REPERTOIRE_COMMUN_LANCEMENT))
from lancement import drapeaux_popen  # noqa: E402


def lancer_enfant(*arguments, **options):
    """Le SEUL lancement de processus de cet outil : jamais de fenetre."""
    return subprocess.run(*arguments, **options, **drapeaux_popen())

import sys
import tempfile
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
REGISTRE = BASE / 'registre' / 'sondes.jsonl'

# LE CRITERE, declare une seule fois (jamais recopie ailleurs).
MARQUEUR_TRACEBACK = 'Traceback (most recent call last)'
CODE_TRACEBACK = 3
CODE_USAGE = 2
TIMEOUT_SONDE = 120
LONGUEUR_SIGNATURE = 160
LONGUEUR_PILE_MAX = 1200
LIMITE_SIGNATURES_RAPPORT = 5
SEPARATEUR = '--'
VERBES = ('executer', 'rapport', 'auto-test')


def horodater():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def lire_registre(chemin=None):
    chemin = chemin or REGISTRE
    if not chemin.is_file():
        return []
    entrees = []
    for ligne in chemin.read_text(encoding='utf-8', errors='replace').splitlines():
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            entrees.append(json.loads(ligne))
        except json.JSONDecodeError:
            continue
    return entrees


def noter(entree, chemin=None):
    chemin = chemin or REGISTRE
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin, 'a', encoding='utf-8', newline=chr(10)) as fichier:
        fichier.write(json.dumps(entree, ensure_ascii=False) + chr(10))


def executer_sonde(commande, chemin=None, timeout=TIMEOUT_SONDE):
    '''Lance la sonde, la NOTE, et ne laisse JAMAIS la pile en console.

    Retourne (code_rendu, a_traceback, sortie_a_afficher). Le code rendu est celui
    de la sonde, ou CODE_TRACEBACK des qu un traceback a ete capture : un plantage
    ne se lit donc jamais comme un refus ordinaire.
    '''
    debut = time.monotonic()
    try:
        termine = lancer_enfant(commande, capture_output=True, text=True,
                                 encoding='utf-8', errors='replace', timeout=timeout)
        code = termine.returncode
        sortie = (termine.stdout or '') + (termine.stderr or '')
    except subprocess.TimeoutExpired:
        code = CODE_TRACEBACK
        sortie = 'SONDE INTERROMPUE : delai depasse (' + str(timeout) + ' s)'
    except OSError as erreur:
        code = CODE_TRACEBACK
        sortie = 'SONDE IMPOSSIBLE A LANCER : ' + type(erreur).__name__ + ' : ' + str(erreur)
    a_traceback = MARQUEUR_TRACEBACK in sortie
    lignes = [ligne.strip() for ligne in sortie.splitlines() if ligne.strip()]
    signature = (lignes[-1] if lignes else '')[:LONGUEUR_SIGNATURE]
    code_rendu = CODE_TRACEBACK if a_traceback else code
    entree = {
        'date': horodater(),
        'commande': ' '.join(commande),
        'code': code_rendu,
        'code_brut': code,
        'traceback': 'oui' if a_traceback else 'non',
        'signature': signature,
        'duree_ms': int((time.monotonic() - debut) * 1000),
        'pile_tronquee': 'oui' if a_traceback and len(sortie) > LONGUEUR_PILE_MAX else 'non',
    }
    if a_traceback:
        entree['pile'] = sortie[:LONGUEUR_PILE_MAX]
    noter(entree, chemin)
    if a_traceback:
        affichage = 'SONDE EN ECHEC (ce n est PAS une panne de la Matrice) : ' + signature
    else:
        affichage = sortie.rstrip()
    return code_rendu, a_traceback, affichage


def rapport(entrees, n=None):
    if not entrees:
        print('AXE B -- SONDES DE L AGENT : registre VIDE.')
        print('  Un registre vide ne dit pas qu il n y a pas de sonde : il dit')
        print('  qu aucune sonde n a ete NOTEE. Le taux ne se calcule pas sur 0.')
        return 0
    vues = entrees[-n:] if n else entrees
    mauvaises = [e for e in vues if e.get('traceback') == 'oui']
    familles = {}
    for entree in vues:
        morceaux = (entree.get('commande') or '').split(' ')
        racine = morceaux[0] if morceaux and morceaux[0] else '(vide)'
        compte = familles.setdefault(racine, [0, 0])
        compte[0] += 1
        if entree.get('traceback') == 'oui':
            compte[1] += 1
    taux = (100.0 * len(mauvaises) / len(vues)) if vues else 0.0
    print('AXE B -- SONDES DE L AGENT (' + horodater() + ')')
    print('  sondes NOTees : ' + str(len(vues)) + '  |  tracebacks : ' + str(len(mauvaises)))
    print('  TAUX : ' + str(int(round(taux))) + ' % des sondes notees ont rendu un traceback')
    print('  par famille de commande :')
    for nom, (total, mauvais) in sorted(familles.items(), key=lambda x: -x[1][1]):
        print('    ' + nom + ' : ' + str(mauvais) + ' traceback(s) sur ' + str(total))
    if mauvaises:
        print('  dernieres signatures :')
        for entree in mauvaises[-LIMITE_SIGNATURES_RAPPORT:]:
            print('    ' + entree.get('date', '') + '  ' + entree.get('signature', ''))
    print('  PORTEE : seules les sondes passees par cet espion sont comptees.')
    return 1 if mauvaises else 0


def auto_test():
    '''Cobaye qui MORD, et contre-temoins qui EPARGNENT -- sur un registre JETABLE.'''
    jetable = Path(tempfile.mkdtemp(prefix='sondes-auto-test-')) / 'registre.jsonl'
    resultats = []

    def cas(nom, condition, detail=''):
        resultats.append((nom, bool(condition), detail))

    code, vu, affichage = executer_sonde([sys.executable, '-c', 'print(1 / 0)'], chemin=jetable)
    cas('cobaye : le traceback est VU', vu, affichage[:70])
    cas('cobaye : code 3 rendu', code == CODE_TRACEBACK, 'code ' + str(code))
    cas('cobaye : LA PILE N EST PAS EN CONSOLE', MARQUEUR_TRACEBACK not in affichage)
    cas('cobaye : l echec se DIT', 'SONDE EN ECHEC' in affichage)
    cas('cobaye : la pile est ECRITE au registre', bool(lire_registre(jetable)[0].get('pile')))

    code, vu, affichage = executer_sonde([sys.executable, '-c', 'print(40 + 2)'], chemin=jetable)
    cas('contre-temoin : propre -> aucun traceback', not vu)
    cas('contre-temoin : code de la sonde rendu', code == 0, 'code ' + str(code))
    cas('contre-temoin : la sortie est LISIBLE', '42' in affichage, affichage[:40])

    code, vu, affichage = executer_sonde(
        [sys.executable, '-c', 'import sys;print(77);sys.exit(2)'], chemin=jetable)
    cas('contre-temoin : un refus ne devient pas une panne', (not vu) and code == 2,
        'code ' + str(code))

    entrees = lire_registre(jetable)
    cas('memoire : les 3 sondes sont notees', len(entrees) == 3, str(len(entrees)) + ' entree(s)')
    cas('memoire : le verdict est ecrit sur chacune',
        all(e.get('traceback') in ('oui', 'non') for e in entrees))

    import contextlib
    import io
    tampon = io.StringIO()
    with contextlib.redirect_stdout(tampon):
        rapport(entrees)
    texte = tampon.getvalue()
    ligne_taux = [l for l in texte.splitlines() if 'TAUX' in l]
    cas('rapport : le taux est calcule (1 sur 3 = 33 %)',
        bool(ligne_taux) and '33' in ligne_taux[0], ligne_taux[0] if ligne_taux else '')
    cas('rapport : la PORTEE est dite', 'PORTEE' in texte)

    reussis = sum(1 for _, bon, _ in resultats if bon)
    for nom, bon, detail in resultats:
        print(('  OK  ' if bon else '  KO  ') + nom + (('  [' + detail + ']') if detail else ''))
    print('AUTO-TEST : ' + str(reussis) + '/' + str(len(resultats)) + ' OK')
    return 0 if reussis == len(resultats) else 1


def principal(arguments):
    if not arguments or arguments[0] not in VERBES:
        print(__doc__)
        return CODE_USAGE
    verbe, suite = arguments[0], arguments[1:]
    if verbe == 'executer':
        if SEPARATEUR in suite:
            suite = suite[suite.index(SEPARATEUR) + 1:]
        if not suite:
            print('EXECUTER : aucune commande -- forme : executer -- <commande...>')
            return CODE_USAGE
        code, _, affichage = executer_sonde(suite)
        if affichage:
            print(affichage)
        return code
    if verbe == 'rapport':
        nombre = None
        if suite and suite[0] == '--n' and len(suite) > 1 and suite[1].isdigit():
            nombre = int(suite[1])
        return rapport(lire_registre(), nombre)
    return auto_test()


if __name__ == '__main__':
    sys.exit(principal(sys.argv[1:]))
# LES PRODUCTIONS DE L ESPION (MO-534) : les fichiers qu il ECRIT et qui ne sont
# ni ses etats courts de forme conventionnelle, ni un fichier ecrit a la main.
# Cette case est VIDE PARCE QUE C EST VRAI : mesure du 2026-10-03 sur ce
# fichier, il ne contient aucun site d ecriture -- un espion LIT et SIGNE, il
# n enregistre rien de lui-meme. Les trois fichiers de `registre/` (registre,
# sondes, tracebacks) sont ecrits par les ESPIONS VOISINS qui les possedent, et
# chacun declare ce qu il ecrit de son cote. Cette case dit le silence au lieu
# de le laisser : une case ABSENTE et une case VIDE ne se distinguent pas pour le
# controle d attribution, qui peut alors prendre l absence pour un oubli.
PRODUCTIONS = ()
