# =============================================================================
# REGLE IMMUABLE DE NOMMAGE : le nom commence par le prefixe du dossier de
# categorie (tester-).
# =============================================================================
import argparse
import glob
import io
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime

VERSION = "0.2.0"
STATUT = "ebauche"

# Round 10 : 5 series thematiques. Chaque test appartient a une serie par son
# prefixe test-0XX. Un test trouve sur disque sans prefixe de serie est lance
# en queue avec un avertissement (il n est jamais oublie).
SERIES = {
    "a": ["test-001", "test-002", "test-003", "test-004", "test-019", "test-020"],
    "b": ["test-006", "test-009", "test-012", "test-013", "test-014", "test-015",
          "test-016", "test-018", "test-021", "test-022"],
    "c": ["test-005", "test-007", "test-008", "test-010", "test-011", "test-017"],
    "d": ["test-023", "test-024", "test-025", "test-026", "test-027",
          "test-030", "test-031"],
    "e": ["test-028", "test-029", "test-032", "test-033", "test-034", "test-035",
          "test-036", "test-037", "test-038", "test-039", "test-040", "test-041", "test-042"],
}
SERIES_NOMS = {
    "a": "Combos et coherence",
    "b": "Parcours et validateurs",
    "c": "Generateurs et catalogue",
    "d": "Registre et garde-fous",
    "e": "Coherence et anti-recurrence",
}
SERIES_ORDRE = ["a", "b", "c", "d", "e"]
# La serie D porte les GARDE-FOUS GLOBAUX (registre, sessions, scripts
# temporaires) - ils tournent toujours en serie apres le pool de workers,
# jamais en parallele avec les autres tests.
SERIES_PARALLELES = ["a", "b", "c"]

# Round 12 : garde-fous GLOBAUX - ils verifient l etat global du projet
# (registre vide, absence de scripts temporaires, sessions) et ne doivent
# JAMAIS tourner en parallele avec d autres tests (faux positifs assures).
# Ils sont toujours lances en serie, apres le pool de workers.
GARDE_FOUS_GLOBAUX = ["test-023", "test-024", "test-025", "test-027"]

# Round 12 : durees mesurees (profil individuel 2026-08-13, machine 16 coeurs)
# pour le tri decroissant du pool - les tests longs partent en premier sur
# les workers, les courts remplissent les creneaux restants.
DUREES_CONNUES = {
    "test-028": 13, "test-003": 8, "test-031": 5, "test-005": 5,
    "test-017": 4, "test-030": 3, "test-012": 3, "test-027": 2,
    "test-010": 2, "test-009": 2, "test-006": 2, "test-004": 2,
    "test-002": 2, "test-026": 1, "test-025": 1, "test-024": 1,
    "test-022": 1, "test-021": 1, "test-020": 1, "test-019": 1,
    "test-018": 1, "test-016": 1, "test-015": 1, "test-013": 1,
    "test-011": 1, "test-008": 1, "test-007": 1, "test-029": 0,
    "test-033": 0, "test-034": 0, "test-035": 0, "test-036": 0,
    "test-037": 0, "test-038": 0, "test-039": 0, "test-040": 0,
    "test-023": 0, "test-014": 0, "test-001": 0, "test-041": 0, "test-042": 0,
}

_COULEURS = {
    "rouge": "\033[0;31m",
    "vert": "\033[0;32m",
    "jaune": "\033[0;33m",
    "bleu": "\033[0;34m",
    "neutre": "\033[0m",
}


def _couleur(texte, nom="neutre"):
    return "%s%s%s" % (_COULEURS.get(nom, _COULEURS["neutre"]), texte, _COULEURS["neutre"])


def racine_projet():
    """Remonte jusqu'au dossier racine (contenant AGENTS.md)."""
    d = os.path.dirname(os.path.abspath(__file__))
    while not os.path.isfile(os.path.join(d, "AGENTS.md")):
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return d


def registre_defaut(racine):
    return os.path.join(racine, "cerveau-projet", "agents", "traces", "registre-usages-outils.jsonl")


def registre_historique(racine):
    """Chemin de l historique du registre (append, jamais ecrase)."""
    return os.path.join(racine, "cerveau-projet", "agents", "traces",
                        "registre-usages-outils.historique.jsonl")


def archiver_registre(racine):
    """Deplace les lignes du registre courant vers l historique (round 8 :
    la purge pure perdait la memoire des declarations, le detecteur devenait
    aveugle au passe). Les lignes deja presentes dans l historique ne sont
    pas re-ajoutees (dedoublonnage par ligne exacte)."""
    registre = registre_defaut(racine)
    historique = registre_historique(racine)
    if not os.path.isfile(registre):
        return
    try:
        with io.open(registre, encoding="utf-8") as fh:
            lignes = [l for l in fh if l.strip()]
    except Exception:
        return
    if not lignes:
        return
    deja = set()
    if os.path.isfile(historique):
        try:
            with io.open(historique, encoding="utf-8") as fh:
                deja = set(l for l in fh if l.strip())
        except Exception:
            deja = set()
    nouveaux = [l for l in lignes if l not in deja]
    if not nouveaux:
        return
    dossier = os.path.dirname(historique)
    if dossier and not os.path.isdir(dossier):
        os.makedirs(dossier, exist_ok=True)
    with io.open(historique, "a", encoding="utf-8", newline="\n") as fh:
        for l in nouveaux:
            fh.write(l.rstrip("\n") + "\n")


def trouver_tests(racine, filtre=None):
    """Retourne la liste des tests test-0XX (fichiers .py) tries."""
    pattern = os.path.join(racine, "cerveau-projet", "agents", "tools", "tester",
                           "tests", "test-0*", "test-0*.py")
    tests = sorted(glob.glob(pattern))
    if filtre:
        noms_filtres = [f.strip() for f in filtre.split(",") if f.strip()]
        tests = [t for t in tests if any(n in os.path.basename(t) for n in noms_filtres)]
    return tests


def compter_ko(sortie):
    return len(re.findall(r"\[KO\]", sortie))


def assigner_series(tests, serie="tous"):
    """Attribue chaque test a sa serie (par prefixe test-0XX).

    Retourne (par_serie, hors_serie) :
      - par_serie : dict serie -> liste de tests (serie vide si aucun test)
      - hors_serie : tests sans serie affectee (mode tous uniquement)
    """
    par_serie = {s: [] for s in SERIES}
    hors_serie = []
    for t in tests:
        nom = os.path.basename(t)
        affecte = None
        for s in SERIES_ORDRE:
            if any(nom.startswith(p) for p in SERIES[s]):
                affecte = s
                break
        if affecte:
            par_serie[affecte].append(t)
        else:
            hors_serie.append(t)
    if serie != "tous":
        return {serie: par_serie[serie]}, []
    return par_serie, hors_serie


def executer_lot(racine, tests, libelle="", header=True, fail_fast=False):
    """Execute une liste de tests en serie. Retourne (ok, ko, ko_liste).

    fail_fast (protection STOP, option --fail-fast) : des le premier test KO
    (ou ERREUR), la suite est STOPPEE - les tests restants ne sont pas lances
    et sont comptes comme non-lances.
    """
    if header:
        print(_couleur("=== %s : %d tests ===" % (libelle or "Non-regression", len(tests)), "bleu"))
    ok = ko = 0
    non_lances = 0
    ko_liste = []
    for i, t in enumerate(tests):
        try:
            r = subprocess.run([sys.executable, t], capture_output=True, text=True, timeout=180)
            nb_ko = compter_ko(r.stdout)
            if nb_ko == 0 and r.returncode == 0:
                ok += 1
                print("  %-50s %s" % (os.path.basename(t), _couleur("OK", "vert")))
            else:
                ko += 1
                ko_liste.append((os.path.basename(t), nb_ko))
                print("  %-50s %s (%d [KO])" % (os.path.basename(t), _couleur("KO", "rouge"), nb_ko))
                if fail_fast:
                    non_lances = len(tests) - i - 1
                    if non_lances > 0:
                        print(_couleur("  [FAIL-FAST] Test en erreur : la suite est STOPPEE, "
                                       "%d test(s) non lance(s)" % non_lances, "rouge"))
                    break
        except Exception as e:
            ko += 1
            ko_liste.append((os.path.basename(t), -1))
            print("  %-50s %s (%s)" % (os.path.basename(t), _couleur("ERREUR", "rouge"), str(e)[:40]))
            if fail_fast:
                non_lances = len(tests) - i - 1
                if non_lances > 0:
                    print(_couleur("  [FAIL-FAST] Erreur d execution : la suite est STOPPEE, "
                                   "%d test(s) non lance(s)" % non_lances, "rouge"))
                break
    suffixe = (" %s" % libelle) if libelle else ""
    lance_total = len(tests) - non_lances
    print("")
    print(_couleur("=== RESULTAT%s : %d OK / %d KO (sur %d tests, %d non lances) ==="
                   % (suffixe, ok, ko, lance_total, non_lances),
                   "vert" if ko == 0 else "rouge"))
    return ok, ko, ko_liste, non_lances


def executer_pool(racine, tests, workers, fail_fast=False):
    """Execute une liste de tests sur un pool de workers paralleles.

    Round 12 : les tests sont tries par DUREE DECROISSANTE (les plus longs
    partent en premier sur les workers, les courts remplissent les creneaux
    restants) puis distribues sur `workers` sous-processus simultanes.
    Retourne (ok, ko, ko_liste, non_lances).

    fail_fast : des le premier KO, le pool est stoppe - les tests restants
    ne sont pas lances (non_lances > 0).
    """
    if not tests:
        return 0, 0, [], 0
    if workers <= 1:
        return executer_lot(racine, tests, libelle="Serie unique",
                            fail_fast=fail_fast)

    def cle(t):
        return -DUREES_CONNUES.get(os.path.basename(t)[:8], 0)

    tries = sorted(tests, key=cle)
    print(_couleur("=== Pool de workers : %d tests sur %d workers (longs d abord) ==="
                   % (len(tries), workers), "bleu"))
    # ANTI-DEADLOCK (lecon 2026-08-13) : jamais de Popen(stdout=PIPE) dans le
    # pool - si un test ecrit plus de 64 Ko, le buffer du pipe se remplit et
    # le sous-processus se bloque en ecrivant (poll() ne passe jamais a None).
    # Chaque test redirige sa sortie vers un FICHIER temp unique, lu apres
    # terminaison : aucun pipe, aucun blocage possible.
    TIMEOUT_POOL = 300  # secondes par test (protection anti-blocage : un test
    # qui se bloque (verrou fichier, attente) est tue apres ce delai).
    ok = ko = 0
    non_lances = 0
    ko_liste = []
    actifs = []
    index = 0
    stoppe = False
    while index < len(tries) or actifs:
        # Lancer de nouveaux tests tant que des workers sont libres.
        while len(actifs) < workers and index < len(tries) and not stoppe:
            t = tries[index]
            index += 1
            # Fichier de sortie UNIQUE par test (jamais partage entre workers).
            fic_sortie = os.path.join(racine, "cerveau-projet", "agents", "tools",
                                      "tester", ".pool-%d-%d.out" % (os.getpid(), index))
            with io.open(fic_sortie, "w", encoding="utf-8", newline="\n") as fh:
                p = subprocess.Popen([sys.executable, t], cwd=racine,
                                     stdout=fh, stderr=subprocess.STDOUT)
            actifs.append([p, t, time.monotonic(), fic_sortie])
        # Attendre qu AU MOINS un processus se termine (ou depasse le timeout).
        finis = []
        for a in actifs:
            p = a[0]
            if p.poll() is not None:
                finis.append(a)
            elif time.monotonic() - a[2] > TIMEOUT_POOL:
                try:
                    p.kill()
                except Exception:
                    pass
                finis.append(a)
        if not finis:
            if not actifs:
                break  # rien a lancer, rien en cours : c est termine
            time.sleep(0.1)
            continue
        for a in finis:
            actifs.remove(a)
            p, t, _, fic_sortie = a
            try:
                with io.open(fic_sortie, encoding="utf-8", errors="replace") as fh:
                    sortie = fh.read()
            except Exception:
                sortie = ""
            try:
                os.remove(fic_sortie)
            except Exception:
                pass
            nb_ko = compter_ko(sortie)
            if nb_ko == 0 and p.returncode == 0:
                ok += 1
                print("  %-50s %s" % (os.path.basename(t), _couleur("OK", "vert")))
            else:
                ko += 1
                ko_liste.append((os.path.basename(t), nb_ko))
                print("  %-50s %s (%d [KO])" % (os.path.basename(t), _couleur("KO", "rouge"), nb_ko))
                if fail_fast:
                    stoppe = True
    if stoppe:
        non_lances = len(tries) - index
        if non_lances > 0:
            print(_couleur("  [FAIL-FAST] Test en erreur : le pool est STOPPE, "
                           "%d test(s) non lance(s)" % non_lances, "rouge"))
    print("")
    print(_couleur("=== RESULTAT Pool : %d OK / %d KO (sur %d tests, %d non lances) ==="
                   % (ok, ko, len(tries) - non_lances, non_lances),
                   "vert" if ko == 0 else "rouge"))
    return ok, ko, ko_liste, non_lances


def extraire_bilan(sortie):
    """Extrait (ok, ko) du bilan RESULTAT d une sortie de sous-processus.
    Le libelle d une serie ne contient jamais de deux-points, le premier ':'
    est donc le separateur du bilan."""
    m = re.search(r"RESULTAT[^:]*: (\d+) OK / (\d+) KO", sortie)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def afficher_etat_registre(racine):
    """Affiche l etat du registre apres une passe protegee (round 8)."""
    registre = registre_defaut(racine)
    if os.path.exists(registre):
        with io.open(registre, encoding="utf-8") as fh:
            lignes = sum(1 for l in fh if l.strip())
    else:
        lignes = 0
    hist = registre_historique(racine)
    n_hist = 0
    if os.path.isfile(hist):
        with io.open(hist, encoding="utf-8") as fh:
            n_hist = sum(1 for l in fh if l.strip())
    ligne_reg = "=== Registre d usage apres : %d lignes (archive dans l historique : %d) ===" % (lignes, n_hist)
    print(_couleur(ligne_reg, "vert" if lignes == 0 else "jaune"))
    if lignes != 0:
        print(_couleur("[AVERTISSEMENT] Des tests polluent le registre : "
                       "ajouter --no-journal a leurs appels generateurs-commande", "jaune"))
    return lignes


def ecrire_rapport(chemin, titre, bilan, ko_liste, lignes_registre):
    """Ecrit le rapport markdown du bilan."""
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("# Rapport non-regression\n\n")
        fh.write("Titre : %s\n\n" % titre)
        fh.write("Date : %s\n\n" % datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        fh.write("## Bilan\n\n%s\n\n" % bilan)
        if ko_liste:
            fh.write("## Tests en echec\n\n")
            for nom, nb in ko_liste:
                fh.write("- %s : %d [KO]\n" % (nom, nb))
        if lignes_registre is not None:
            fh.write("\nRegistre d usage apres : %d lignes\n" % lignes_registre)
    print(_couleur("[OK] Rapport ecrit : %s" % chemin, "vert"))


def chemin_reference(racine):
    """Chemin du fichier de reference de temps (dossier de l outil)."""
    return os.path.join(racine, "cerveau-projet", "agents", "tools", "tester",
                        "tester-lancer-non-regression", "temps-reference.json")


def lire_reference(racine):
    """Lit la reference persistee. Retourne (secondes, mode, nb_tests, date)
    ou (None, None, None, None) si absente ou illisible."""
    chemin = chemin_reference(racine)
    if not os.path.isfile(chemin):
        return None, None, None, None
    try:
        with io.open(chemin, encoding="ascii") as fh:
            d = json.load(fh)
        return (float(d.get("reference_secondes", 0)),
                d.get("mode", ""), d.get("nb_tests", 0), d.get("date", ""))
    except Exception:
        return None, None, None, None


def ecrire_reference(racine, duree, mode, nb_tests):
    """Persiste la reference de temps (meilleur temps ou rebase force)."""
    chemin = chemin_reference(racine)
    d = {
        "reference_secondes": round(duree, 1),
        "mode": mode,
        "nb_tests": nb_tests,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    with io.open(chemin, "w", encoding="ascii", newline="\n") as fh:
        json.dump(d, fh, ensure_ascii=True, indent=1)
        fh.write("\n")
    return chemin


def afficher_chrono(racine, duree, mode, nb_tests, seuil=25.0,
                    rebase=False, no_reference=False):
    """Affiche le temps ecoule, compare a la reference et met a jour si
    meilleur. Retourne True si un SIGNAL de ralentissement est emis.

    Regles (demande utilisateur) :
      - chrono demarre au debut de la premiere serie, s arrete a la fin de la
        derniere (mode tous) ;
      - pas de reference -> enregistree comme base ;
      - temps ameliore (plus bas) -> reference mise a jour automatiquement ;
      - temps trop eloigne (> seuil %, defaut 25) -> SIGNAL affiche ;
      - --rebase-reference force la mise a jour ;
      - --no-reference : sous-processus paralleles (jamais de course sur le fichier).
    """
    print(_couleur("=== Temps ecoule : %.1f s (%s, %d tests) ===" % (duree, mode, nb_tests), "bleu"))
    if no_reference:
        return False
    ref, ref_mode, ref_nb, ref_date = lire_reference(racine)
    # Nombre de tests different : la comparaison n a pas de sens (la suite a
    # change) -> nouvelle base enregistree sans SIGNAL (anti-faux positif).
    if ref is not None and ref_nb is not None and int(ref_nb) != nb_tests:
        chemin = ecrire_reference(racine, duree, mode, nb_tests)
        print(_couleur("[CHRONO] Nombre de tests change (%d -> %d) : nouvelle base enregistree : %.1f s"
                       % (int(ref_nb), nb_tests, duree), "jaune"))
        return False
    if ref is None or rebase:
        chemin = ecrire_reference(racine, duree, mode, nb_tests)
        print(_couleur("[CHRONO] Reference enregistree : %.1f s (%s) -> %s"
                       % (duree, mode, chemin), "vert"))
        return False
    pct = (duree - ref) / ref * 100.0 if ref else 0.0
    if duree < ref:
        chemin = ecrire_reference(racine, duree, mode, nb_tests)
        print(_couleur("[CHRONO] Temps ameliore : %.1f s (ancienne reference %.1f s) -> reference mise a jour"
                       % (duree, ref), "vert"))
        return False
    if pct > seuil:
        print(_couleur("[SIGNAL] RALENTISSEMENT : %.1f s vs reference %.1f s (%s, +%.0f%% depassement)"
                       % (duree, ref, ref_date, pct), "rouge"))
        print(_couleur("[SIGNAL] La suite est plus lente que la reference - verifier les tests lents"
                       " (la reference reste enregistree : %.1f s)" % ref, "rouge"))
        return True
    print(_couleur("[CHRONO] Conforme a la reference : %.1f s vs %.1f s (%s, +%.0f%%)"
                   % (duree, ref, ref_date, pct), "vert"))
    return False



def detecter_parent_temporaire(racine):
    """Detecte le script .tmp-*/.zz-* a la racine qui a LANCE ce processus
    (le processus parent direct, en cours d execution).

    Anti-artefact (lecon 2026-08-13, demande utilisateur) : quand on lance la
    non-regression DEPUIS un script temporaire legitime (ex .tmp-controle.py
    qui orchestre plusieurs appels), ce script existe a la racine pendant
    l execution et test-024 le detecte comme un residu -> KO a tort. Le
    parent direct est en cours d execution : ce n est PAS un residu, il doit
    etre exclu du scan de test-024. Un vrai residu (script temporaire laisse
    par erreur, plus utilise par aucun processus) n est jamais le parent
    direct : il reste KO (protection intacte).

    Retourne le nom du fichier temporaire parent, ou None.
    """
    try:
        ppid = os.getppid()
        cmdline = ""
        if os.path.exists("/proc"):
            try:
                with io.open("/proc/%d/cmdline" % ppid, "rb") as fh:
                    cmdline = fh.read().decode(errors="replace").replace("\x00", " ")
            except Exception:
                cmdline = ""
        else:
            # Windows : interroger la ligne de commande du processus parent.
            try:
                r = subprocess.run(
                    ["powershell", "-NoProfile", "-Command",
                     "(Get-CimInstance Win32_Process -Filter 'ProcessId=%d').CommandLine"
                     % ppid],
                    capture_output=True, text=True, timeout=10,
                )
                cmdline = (r.stdout or "").strip()
            except Exception:
                cmdline = ""
        for mot in cmdline.split():
            base = os.path.basename(mot.strip("\"'"))
            if base.startswith(".tmp-") or base.startswith(".zz-"):
                chemin = os.path.join(racine, base)
                if os.path.exists(chemin):
                    return base
    except Exception:
        pass
    return None



def main():
    parser = argparse.ArgumentParser(description="Lance la non-regression complete des tests formels")
    parser.add_argument("--series", type=str, default="tous",
                        choices=["a", "b", "c", "d", "e", "tous"],
                        help="Ne lancer qu une serie (a|b|c|d|e) ou toutes (tous, defaut)")
    parser.add_argument("--workers", type=int, default=0,
                        help="Nombre de workers paralleles (defaut : min(cpu_count, 16))")
    parser.add_argument("--parallele", action="store_true",
                        help="Mode pool de workers (defaut : distribue les tests, longs d abord)")
    parser.add_argument("--serial", action="store_true",
                        help="Force le mode serie complet (ancien comportement)")
    parser.add_argument("--fail-fast", action="store_true",
                        help="PROTECTION STOP : des le premier test KO, la suite est stoppee (les tests restants ne sont pas lances)")
    parser.add_argument("--seuil", type=float, default=25.0,
                        help="Pourcentage de depassement tolere avant SIGNAL de ralentissement (defaut 25)")
    parser.add_argument("--rebase-reference", action="store_true",
                        help="Force la mise a jour de la reference de temps (meme si plus lent)")
    parser.add_argument("--no-reference", action="store_true",
                        help="Ne pas lire ni ecrire la reference de temps (sous-processus paralleles)")
    parser.add_argument("--tests", type=str, default="",
                        help="Filtrer par noms de test separes par des virgules")
    parser.add_argument("--no-journal", action="store_true",
                        help="Purge le registre d usage avant et verifie 0 apres (defaut)")
    parser.add_argument("--journal", action="store_true",
                        help="Ne touche pas au registre d usage")
    parser.add_argument("--rapport", type=str, default="",
                        help="Chemin du rapport markdown (optionnel)")
    parser.add_argument("--version", action="version", version="tester-lancer-non-regression v%s" % VERSION)
    args = parser.parse_args()

    racine = racine_projet()
    # Anti-artefact test-024 (lecon 2026-08-13) : si le lanceur est execute
    # DEPUIS un script temporaire legitime (.tmp-*/.zz-* parent direct), le
    # declarer en exclusion pour test-024 (via l environnement, herite par
    # tous les sous-processus). Un vrai residu n est jamais le parent direct.
    parent_tmp = detecter_parent_temporaire(racine)
    if parent_tmp:
        os.environ["NON_REGRESSION_EXCLUSIONS"] = parent_tmp
        print(_couleur("[INFO] Script parent temporaire exclu du garde-fou "
                       "test-024 : %s" % parent_tmp, "jaune"))
    tests = trouver_tests(racine, args.tests)
    if not tests:
        print(_couleur("[ERREUR] Aucun test trouve", "rouge"))
        return 2

    # Round 11 (chrono) : le chrono demarre au debut de la premiere serie et
    # s arrete a la fin de la derniere. En mode mono-serie, il couvre la serie
    # (sans toucher a la reference globale).
    t0 = time.monotonic()

    if args.series != "tous":
        # Mode mono-serie : une passe en serie (comportement historique),
        # avec protection du registre si demandee.
        selection, _ = assigner_series(tests, args.series)
        selection = selection[args.series]
        if not selection:
            print(_couleur("[ERREUR] Aucun test trouve pour la serie %s" % args.series, "rouge"))
            return 2
        protege = not args.journal
        if protege:
            archiver_registre(racine)
            if os.path.exists(registre_defaut(racine)):
                with io.open(registre_defaut(racine), "w", encoding="utf-8", newline="\n") as fh:
                    fh.write("")
        ok, ko, ko_liste, non_lances = executer_lot(racine, selection,
                                                    libelle="Serie %s (%s)" % (args.series.upper(), SERIES_NOMS[args.series]),
                                                    fail_fast=args.fail_fast)
        duree = time.monotonic() - t0
        afficher_chrono(racine, duree, "serie-%s" % args.series, len(selection),
                        seuil=args.seuil, rebase=args.rebase_reference,
                        no_reference=True)
        lignes = None
        if protege:
            lignes = afficher_etat_registre(racine)
        if args.rapport:
            ecrire_rapport(args.rapport,
                           "Serie %s (%s)" % (args.series.upper(), SERIES_NOMS[args.series]),
                           "=== RESULTAT : %d OK / %d KO (sur %d tests, %d non lances) ==="
                           % (ok, ko, len(selection) - non_lances, non_lances),
                           ko_liste, lignes)
        return 1 if (ko or non_lances) else 0

    # Mode tous : protection du registre faite UNE fois par le parent.
    protege = not args.journal
    if protege:
        archiver_registre(racine)
        if os.path.exists(registre_defaut(racine)):
            with io.open(registre_defaut(racine), "w", encoding="utf-8", newline="\n") as fh:
                fh.write("")

    par_serie, hors_serie = assigner_series(tests, "tous")
    ko_liste = []
    tot_ok = tot_ko = 0
    tot_non_lances = 0

    # Round 12 : POOL DE WORKERS (le DEFAUT). Les tests hors garde-fous
    # globaux sont tries par duree decroissante et distribues sur N workers
    # paralleles ; les garde-fous globaux (test-023/024/025/027 : registre,
    # sessions, scripts temporaires) tournent en SERIE a la fin, jamais en
    # parallele. --serial ou --workers 1 force le mode serie complet.
    if args.workers and args.workers > 0:
        workers = args.workers
    else:
        workers = min(os.cpu_count() or 1, 16)
    parallele = (workers > 1) and not args.serial
    if parallele:
        # Separation : tests paralleles vs garde-fous globaux (serie finale).
        tests_pool = [t for t in tests
                      if not any(os.path.basename(t).startswith(g)
                                 for g in GARDE_FOUS_GLOBAUX)]
        tests_globaux = [t for t in tests
                         if any(os.path.basename(t).startswith(g)
                                for g in GARDE_FOUS_GLOBAUX)]
        if hors_serie:
            print(_couleur("[AVERTISSEMENT] %d test(s) sans serie affectee, lances avec le pool : %s"
                           % (len(hors_serie), ", ".join(os.path.basename(h) for h in hors_serie)), "jaune"))
        ok_p, ko_p, ko_liste_p, non_lances_p = executer_pool(
            racine, tests_pool + hors_serie, workers,
            fail_fast=args.fail_fast)
        tot_ok += ok_p
        tot_ko += ko_p
        tot_non_lances += non_lances_p
        ko_liste.extend(ko_liste_p)
        # Garde-fous globaux en serie finale (jamais en parallele).
        if tests_globaux and non_lances_p == 0:
            ok_g, ko_g, ko_liste_g, non_lances_g = executer_lot(
                racine, tests_globaux,
                libelle="Garde-fous globaux (registre, sessions, scripts temporaires)",
                fail_fast=args.fail_fast)
            tot_ok += ok_g
            tot_ko += ko_g
            tot_non_lances += non_lances_g
            ko_liste.extend(ko_liste_g)
    else:
        # Mode serie complet (--serial ou --workers 1 : ancien comportement).
        ok, ko, ko_liste, non_lances = executer_lot(racine, tests, libelle="",
                                                    fail_fast=args.fail_fast)
        tot_ok, tot_ko = ok, ko
        tot_non_lances = non_lances

    duree = time.monotonic() - t0
    if tot_non_lances:
        bilan = "=== RESULTAT GLOBAL : %d OK / %d KO (sur %d tests, %d non lances - FAIL-FAST) ===" \
                % (tot_ok, tot_ko, len(tests) - tot_non_lances, tot_non_lances)
    else:
        bilan = "=== RESULTAT GLOBAL : %d OK / %d KO (sur %d tests) ===" % (tot_ok, tot_ko, len(tests))
    print("")
    print(_couleur(bilan, "vert" if tot_ko == 0 else "rouge"))
    # La reference globale n est geree QUE par le run complet sans filtre :
    # un run cible (--tests) ou un appel interne ne doit jamais la lire ni
    # l ecrire (sinon une reference partielle fausserait la comparaison).
    reference_globale = not args.tests
    mode_chrono = "pool-%d" % workers if parallele else "serie"
    afficher_chrono(racine, duree, mode_chrono, len(tests),
                    seuil=args.seuil, rebase=args.rebase_reference,
                    no_reference=args.no_reference or not reference_globale)

    lignes = None
    if protege:
        lignes = afficher_etat_registre(racine)

    if args.rapport:
        ecrire_rapport(args.rapport, "Non-regression globale", bilan, ko_liste, lignes)

    return 1 if (tot_ko or tot_non_lances) else 0


if __name__ == "__main__":
    sys.exit(main())
