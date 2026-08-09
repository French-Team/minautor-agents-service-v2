import io, subprocess, sys

raison = (
    "MISSION TERMINEE (Vulcain) : SYMBOLES MANQUANTS COUVERTS - REUSSIE. "
    "MODIFICATIONS (7 fichiers) : dictionnaire partage corriger-dictionnaire-accents.txt "
    "+15 entrees (66 utiles) : fleches verticales et doubles (U+2191 -> ^, U+2193 -> v, "
    "U+2194 -> <->, U+21D0 -> <=, U+21D2 -> =>, U+21D4 -> <=>), box drawing "
    "(U+2500 -> -, U+2502 -> |, U+250C -> +-, U+2510 -> -+, U+2514 -> +-, U+2518 -> -+, "
    "U+251C -> |-, U+2524 -> -|), espace inse cable U+00A0 -> espace simple ; "
    "les 2 outils consommateurs en profitent automatiquement : bump 0.2.1-py -> 0.2.2-py "
    "(py+sh+md des 2 outils) + ligne historique + doc caracteres couverts elargie. "
    "TESTS REELS SEQUENTIELS (4 combinaisons py/sh x 2 outils) : fichier 60 non-ASCII "
    "(fleches + box drawing + NBSP + accents + guillemets) -> corriger-accents-zones-sensibles.py "
    "--all : 22 corrections 0 restant ; .sh : memes remplacements 0 restant ; "
    "corriger-dictionnaire-accents py+sh : 0 restant. "
    "PARITE DE COMPORTEMENT py/sh CONFIRMEE (memes remplacements partout). "
    "VALIDATIONS : ASCII 0 sur les 6 fichiers outils, LF pur, nommage 0 erreur, 0 residu .tmp. "
    "DIAGNOSTIC PREALABLE : scan propre decode UTF-8 avec normalisation des chemins "
    "(piege backslash Windows) confirme que le projet est 100% propre hors exemples/ "
    "et hors dictionnaire - l ajout est PREVENTIF. Lecon Vulcain ecrite ASCII 0."
)

non_ascii = [c for c in raison if ord(c) > 127]
if non_ascii:
    print('ERREUR non-ASCII:', [hex(ord(c)) for c in non_ascii])
    sys.exit(1)

cmd = [
    'python3',
    'cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py',
    'reactiver', 'session-llm-1', raison, 'vulcain'
]
r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
print(r.stdout)
if r.stderr:
    print(r.stderr)
