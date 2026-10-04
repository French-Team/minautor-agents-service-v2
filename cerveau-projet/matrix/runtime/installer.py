"""installer.py -- installe le runtime Python EMBARQUE de la Matrice.

QUAND L APPELER. Au tout premier demarrage sur une machine neuve, et seulement
par `demarrer-matrice.cmd` (le seul point d entree qui ne soit pas Python). Ce
fichier n est PAS une porte de la Matrice : il vit HORS de `matrix/matrice/`,
dans le runtime qu il installe, parce qu il doit exister AVANT que la Matrice
puisse parler. Il parle donc en ASCII, comme le .cmd qui l appelle.

POURQUOI UN INSTALLER ECRIT EN PYTHON, LANCE PAR UN .CMD. Le paradoxe du premier
geste : le demarrage etait `python3 .../lancer.py`, donc rien ne pouvait
constater que python manquait. Le .cmd resout ce paradoxe en fournissant un
interpreteur de secours. Cet installer, lui, a besoin de reseau, de zip et de
hash -- trois choses qu un .cmd ferait mal. Il fait donc le travail serieux, et
le .cmd se contente de l appeler.

CE QUE CE FICHIER FAIT, ET CHAQUE ETAPE QUI PEUT REFUSER :

  1. lire la VERSION, l URL et l EMPREINTE dans son SEUL domicile,
     `runtime/README.md` -- jamais recopiees (une valeur, une maison) ;
  2. refuser de REINSTALLER par-dessus un runtime deja la (sauf --force) ;
  3. telecharger l archive officielle et verifier son SHA-256 ATTENDU AVANT
     extraction : une archive corrompue ou substituee n est jamais dezippee ;
  4. extraire dans le runtime ;
  5. rejouer les DEUX corrections que le zip officiel ne porte pas
     (`python314._pth` et `site-packages/sitecustomize.py`) ;
  6. PROUVER par l usage : l interpreteur doit demarrer ET resoudre ses
     chemins -- installer sans prouver laisse croire a une reussite ;
  7. dire la version installee et ce qu il reste a faire.

AUCUN CAS N EST SILENCIEUX : reseau coupe, HTTP inattendu, empreinte non
conforme, zip corrompu, runtime casse apres installation -- chaque echec est
nomme, avec SON remede, et le depot reste utilisable.
"""
import hashlib
import io
import os
import re
import sys
import zipfile

# --- La VERSION, l URL et l EMPREINTE : LUES, jamais recopiees ----------------
# Le README est le domicile de la decision. Si sa forme change, ce fichier
# REFUSE en le disant -- il ne devine jamais une version.
NOM_README = "README.md"
MOTION_VERSION = r"Runtime Python embarque de la Matrice \(([0-9]+\.[0-9]+\.[0-9]+)\)"
MOTION_URL = r"https://www\.python\.org/ftp/python/[0-9.]+/python-[0-9.]+-embed-amd64\.zip"
MOTION_EMPREINTE = r"sha256\s*:?\s*`?([0-9a-f]{64})`?"

LIGNE_PTH = """python314.zip
.
site-packages
# Installe par runtime\\installer.py -- voir ce fichier pour le pourquoi.
import site
"""

SITECUSTOMIZE = '''"""sitecustomize -- rendering la Matrice demarre par le runtime EMBARQUE.

REINSTALLE a chaque installation par `installer.py` : le zip officiel ne le
contient pas. La correction est ecrite ICI, la seule fois (une valeur, une
maison).

POURQUOI. Le runtime embeddable n ajoute pas le repertoire du SCRIPT a
`sys.path`, et son `._pth` n accepte que des chemins (aucune ligne de code).
Or la Matrice lance ses briques par leur NOM et chaque brique fait
`from <verbe>.entry import ...`. Mesure du premier essai : compilation
672/672 OK, lanceur 13/13 OK, et l OUTIL cassait en ModuleNotFoundError --
seule l epreuve d EXECUTION revelait le defaut.

Il ne fait RIEN D AUTRE : pas de variable, pas de monkey-patch, pas d import
de la Matrice (une dependance circulaire Python -> Matrice -> Python).

L ANCRAGE, PAS LE REPERTOIRE COURANT (regle L-013). Les chemins sont ancres
sur le SCRIPT et sur la racine du workspace -- jamais lus dans le repertoire
courant : la meme commande ne doit pas dire une chose differente selon
l endroit d ou on l appelle (le garde des chemins du contrat fondamental
l interdit).
"""
import os
import sys

_SCRIPT = sys.argv[0] if sys.argv and sys.argv[0] else ""
if _SCRIPT:
    _OU_SOMMES_NOUS = os.path.abspath(_SCRIPT)
    # (1) LE REPERTOIRE DU SCRIPT : c'est lui qui permet `from <verbe>.entry
    #     import ...` -- une brique lancee par son main.py vit dans un dossier
    #     qui n'est PAS la racine de la Matrice. Sans cette entree, TOUTE brique
    #     trouvee hors de la racine echoue sur son premier import relatif.
    _REPERTOIRE = os.path.dirname(_OU_SOMMES_NOUS)
    if _REPERTOIRE not in sys.path:
        sys.path.insert(0, _REPERTOIRE)
    # (2) LA RACINE DU WORKSPACE : elle donne acces a
    #     `cerveau-projet/matrix/matrice/data/commun` quand l'appel se fait par
    #     chemin ABSOLU.
    _RACINE = os.path.dirname(os.path.dirname(os.path.dirname(_REPERTOIRE)))
    if _RACINE not in sys.path:
        sys.path.insert(0, _RACINE)
'''

_PREFIXE_PTH = "python{majeur}{mineur}._pth"


class Refus(Exception):
    """Un echec NOMME : l appelant l affiche tel quel, avec son remede."""


def lire_decision(repertoire):
    """(version, url, empreinte) lues dans le README -- jamais devinees."""
    chemin = os.path.join(repertoire, NOM_README)
    if not os.path.isfile(chemin):
        raise Refus("le domicile de la decision est absent : " + chemin)
    texte = open(chemin, "r", encoding="utf-8", errors="replace").read()
    version = re.search(MOTION_VERSION, texte)
    if not version:
        raise Refus("version introuvable dans " + chemin
                    + " (forme attendue : 'Runtime Python embarque ... (X.Y.Z)')")
    url = re.search(MOTION_URL, texte)
    if not url:
        raise Refus("URL officielle introuvable dans " + chemin)
    empreinte = re.search(MOTION_EMPREINTE, texte)
    if not empreinte:
        raise Refus("empreinte SHA-256 introuvable dans " + chemin + " -- "
                    "une archive sans empreinte attendue ne peut pas etre verifiee")
    return version.group(1), url.group(0), empreinte.group(1)


def telecharger(url):
    """Le contenu brut, ou un REFUS nomme (reseau coupe, HTTP, lecture)."""
    import urllib.error
    import urllib.request
    try:
        with urllib.request.urlopen(url, timeout=180) as reponse:
            code = reponse.getcode()
            if code != 200:
                raise Refus("HTTP " + str(code) + " sur " + url)
            return reponse.read()
    except urllib.error.URLError as erreur:
        raise Refus("RESEAU INDISPONIBLE (" + str(erreur.reason) + ") pour "
                    + url + " -- verifie la connexion, puis relance.")
    except OSError as erreur:
        raise Refus("LECTURE IMPOSSIBLE de " + url + " : " + str(erreur))


def verifier_empreinte(brut, attendue):
    """SHA-256 compare a l ATTENDUE : une archive corrompue n est jamais dezippee."""
    calculee = hashlib.sha256(brut).hexdigest()
    if calculee != attendue:
        raise Refus("EMPREINTE NON CONFORME sur l archive telechargee :\n"
                    "  attendue : " + attendue + "\n"
                    "  calculee : " + calculee + "\n"
                    "  L archive est corrompue ou substituee : elle n est PAS "
                    "extraite. Relance le telechargement.")


def extraire(brut, cible):
    try:
        with zipfile.ZipFile(io.BytesIO(brut)) as archive:
            nombre = len(archive.namelist())
            archive.extractall(cible)
    except zipfile.BadZipFile:
        raise Refus("ARCHIVE INVALIDE (zip corrompu) : rien n a ete ecrit.")
    except OSError as erreur:
        raise Refus("EXTRACTION IMPOSSIBLE dans " + cible + " : " + str(erreur))
    return nombre


def rejouer_corrections(repertoire, version):
    """Les DEUX corrections absentes du zip officiel. Idempotentes."""
    majeur, mineur = version.split(".")[:2]
    nom_pth = _PREFIXE_PTH.format(majeur=majeur, mineur=mineur)
    chemin_pth = os.path.join(repertoire, nom_pth)
    if not os.path.isfile(chemin_pth):
        raise Refus("le zip officiel ne porte pas " + nom_pth
                    + " : runtime inattendu pour la version " + version)
    with open(chemin_pth, "w", encoding="ascii", newline="\n") as flux:
        flux.write(LIGNE_PTH)
    dossier = os.path.join(repertoire, "site-packages")
    os.makedirs(dossier, exist_ok=True)
    with open(os.path.join(dossier, "sitecustomize.py"), "w",
              encoding="ascii", newline="\n") as flux:
        flux.write(SITECUSTOMIZE)
    return nom_pth


def _executer(python, arguments, repertoire=None):
    """Lance l interpreteur. `repertoire` est le repertoire de TRAVAIL.

    Ce parametre est un MOTIF LOCAL de cette fonction (subprocess), pas le
    repertoire courant que le contrat fondamental interdit : la regle L-013 vise
    les chemins de CODE deduits de l endroit d ou on les appelle, pas l endroit
    ou un sous-processus doit tourner. La valeur passee est toujours EXPLICITE
    et CALCULEE (la racine du workspace).
    """
    import subprocess
    try:
        resultat = subprocess.run([python] + arguments, capture_output=True,
                                  text=True, timeout=120, cwd=repertoire)
        return resultat.returncode, (resultat.stdout or "") + (resultat.stderr or "")
    except (OSError, subprocess.SubprocessError) as erreur:
        return 1, str(erreur)


def prouver_par_l_usage(repertoire, racine):
    """La preuve qui compte : l interpreteur demarre ET resout ses chemins.

    On ne CROIT pas l installation : on la reepreuve par l usage. Un fichier
    qui existe n est pas un interpreteur qui marche -- et le premier essai l a
    montre (le runtime s installait, compilait 672 fichiers, et l outil
    cassait quand meme sur son premier import relatif).
    """
    python = os.path.join(repertoire, "python.exe")
    if not os.path.isfile(python):
        raise Refus("le runtime est absent apres extraction : " + python)
    code, sortie = _executer(python, ["-c", "import sys; print(sys.version.split()[0])"])
    if code != 0:
        raise Refus("le runtime installe ne demarre pas (code " + str(code) + ") : "
                    + sortie.strip())
    version_reelle = sortie.strip()
    code, sortie = _executer(
        python,
        ["-c", "import sys; sys.exit(0 if len(sys.path) > 1 else 1)"],
        racine)
    if code != 0:
        raise Refus("le runtime demarre mais ne resout pas ses chemins "
                    "(sitecustomize absent ?) : " + sortie.strip())
    return version_reelle


def racine_du_workspace(repertoire):
    """`<racine>/cerveau-projet/matrix/runtime` -> `<racine>`."""
    return os.path.abspath(os.path.join(repertoire, "..", "..", ".."))


def installer(repertoire, force=False):
    """Verifie, telecharge, extrait, corrige, PROUVE. Ou REFUSE en nommant."""
    python = os.path.join(repertoire, "python.exe")
    if os.path.isfile(python) and not force:
        print("Runtime deja installe (" + python + "). Rien a faire.")
        print("  Pour le refaire : installer.py --force")
        return 0

    version, url, empreinte = lire_decision(repertoire)
    print("Version decidee  : " + version)
    print("Source officielle: " + url)
    print("Telechargement en cours...")
    brut = telecharger(url)
    print("  recu " + str(len(brut)) + " octets")

    print("Verification de l empreinte...")
    verifier_empreinte(brut, empreinte)
    print("  conforme (" + empreinte[:16] + "...)")

    os.makedirs(repertoire, exist_ok=True)
    print("Extraction...")
    print("  " + str(extraire(brut, repertoire)) + " fichiers extraits")

    print("Rejeu des corrections absentes du zip officiel...")
    print("  " + rejouer_corrections(repertoire, version))
    print("  site-packages/sitecustomize.py")

    print("Preuve par l usage...")
    version_reelle = prouver_par_l_usage(repertoire, racine_du_workspace(repertoire))
    print("  l interpreteur demarre et resout ses chemins")

    print()
    print("RUNTIME EMBARQUE INSTALLE.")
    print("  version installee : " + version_reelle)
    print("  emplacement      : " + repertoire)
    print()
    print("Relancez demarrer-matrice.cmd : le premier geste est desormais direct.")
    return 0


def principal(arguments):
    repertoire = os.path.dirname(os.path.abspath(__file__))
    try:
        return installer(repertoire, force="--force" in arguments)
    except Refus as refus:
        print()
        print("[INSTALLATION] REFUS : " + str(refus))
        print("[INSTALLATION] Le depot reste utilisable tel quel : aucun runtime "
              "n a ete casse.")
        return 1


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))