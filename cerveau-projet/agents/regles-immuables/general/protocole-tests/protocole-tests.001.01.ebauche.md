---
identite:
  type: protocole
  appartient_a: commun
  commun: true
---

# Protocole de Tests avec Protections
# Comment tester les outils du cerveau-projet

protocole:
  nom: "protocole-tests"
  version: "0.3.2"
  statut: "ebauche"
  cree: "2026-08-06"

---

# Protocole de Tests avec Protections

## Objectif

Definir comment tester les outils du cerveau-projet avec des protections qui
garantissent que les tests ne se bloquent pas, ne mentent pas et s arretent
des qu une erreur critique survient.

> **REGLE ABSOLUE (demande utilisateur 2026-08-12)** : CHAQUE test DOIT etre
> protege. Les protections se chargent via le POINT D ENTREE UNIQUE importable
> `tester-protections` (fusion des anciennes protections autonomes, non
> importables, jamais chargees par les tests). Le garde-fou test-030 verifie
> que chaque test-0XX importe les protections.

## Principe fondamental

> **REGLE ABSOLUE** : Les tests doivent etre ENVELOPPES par des protections qui
> controlent, analysent et interviennent sur leur deroulement. Un test sans
> protection (timeout, arret de l arbre, STOP fail-fast) n est pas un test.

## REGLE IMMUABLE : PROTECTIONS + OPTIONS ON/OFF + CHRONO (v0.3.2)

> **REGLE ABSOLUE (demande utilisateur 2026-08-13)** : TOUT fichier contenant
> des fonctions, des tests ou des workflows DOIT embarquer le TRIPLET :
>
> | Element | Exigence | Leviers |
> |---|---|---|
> | **Protections** | Anti-erreurs : timeout, tuer l arbre, STOP fail-fast | `tester-protections` (lancer_protege, verifier_critique) |
> | **Options on/off** | Isoler un test, une fonction ou un workflow complet SANS toucher au code | `--isoler N`, `--desactiver 1,3,5` |
> | **Chrono** | Mesure de duree par etape + bilan en fin de test | `--no-chrono` (defaut : actif), `chrono_etape`, `bilan_chrono` |
>
> Les durees mesurees alimenteront les futurs outils de suivi (detecter les
> lenteurs, ameliorer les procedures). Le template-test.md v0.3.0 impose ce
> triplet dans son canevas : chaque NOUVEAU test copie `point_actif`,
> `chrono_etape`, `bilan_chrono`. Les tests EXISTANTS ne sont PAS migres
> (decision utilisateur) : ils restent valides sans chrono, mais tout test
> cree apres la v0.3.0 DOIT embarquer le triplet.

## Structure des tests

```
tester/
  tester-protections/            # POINT D ENTREE UNIQUE importable
    tester-protections.py        # lancer_protege + verifier_critique (STOP)
    tester-protections.md
  tests/
    test-001-nom-outil/
      test-001-nom-outil.py      # Script du test (format Python canonique)
      test-001-nom-outil.md      # Documentation du test
    test-002-nom-outil/
      ...
```

Les anciennes protections autonomes (`tester/protections/tester-protection-*`)
restent disponibles pour compatibilite mais NE SONT PAS importables depuis un
test .py : c est le module `tester-protections` qui fait foi.

## Numerotation des tests

| Element | Format | Exemple |
|---|---|---|
| **Script de test** | `test-0XX-nom-outil.py` | `test-001-valider-ascii.py` |
| **Documentation** | `test-0XX-nom-outil.md` | `test-001-valider-ascii.md` |
| **Tests dans le fichier** | points numerotes `1.`, `2.`, ... | `1. Detection des accents` |
| **Repertoire du test** | `test-0XX-nom-outil/` | `test-001-valider-ascii/` |

## Protections

### Principe

Les protections sont un MODULE PYTHON importable qui : `tester-protections.py`

1. **Enveloppent** chaque execution (lancer_protege)
2. **Surveillent** le deroulement (timeout, stderr, mots-cles d erreur)
3. **Detectent** les problemes (boucles, blocages, erreurs silencieuses)
4. **Interviennent** (arret force de l arbre de processus, protection STOP)

### Types de protections (module tester-protections)

| Protection | Detection | Action |
|---|---|---|
| **boucles-infinies** | Depassement delai (timeout) | Arret force de l arbre + ArretProtection |
| **erreurs-silencieuses** | stderr non vide, mots-cles d erreur | Signalement (le test juge via verifier) |
| **blocage** | Pas de reponse pendant X sec | Arret force + ArretProtection |
| **stop** | Point critique en echec (verifier_critique) | ARRET IMMEDIAT du test (fail-fast) |

### Import OBLIGATOIRE dans chaque test

```python
import importlib.util
import os

def charger_protections():
    chemin = os.path.join(TOOLS_DIR, "tester", "tester-protections",
                          "tester-protections.py")
    spec = importlib.util.spec_from_file_location("tester_protections", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

PROTECTIONS = charger_protections()
```

## Utilisation des protections

### Dans un fichier de test (format Python canonique)

```python
# 1. Toute execution passe par lancer_protege (timeout + tuer l arbre)
r = PROTECTIONS.lancer_protege([PYTHON, OUTIL_PY, "--version"], timeout=60)
verifier("1. --version affiche la version", "vX.Y.Z" in r.stdout, r.stdout)

# 2. Les points CRITIQUES passent par verifier_critique (PROTECTION STOP)
PROTECTIONS.verifier_critique(
    "2. La fonctionnalite principale reussit",
    "MOTIF ATTENDU" in (r.stdout + r.stderr), r.stdout[-120:])

# 3. main() attrape ArretProtection : le test s arrete proprement
try:
    # ... points du test ...
except PROTECTIONS.ArretProtection as e:
    print("  [KO] ARRET PROTECTION : %s" % e.message)
    NB_KO += 1
```

La structure complete est dans `tester/template-test.md` (v0.3.0+) : le TEMPLATE
est LA reference pour chaque nouveau test, pas les tests precedents.

### Protection STOP (fail-fast)

Quand un point critique echoue, `verifier_critique` leve `ArretProtection` :
le test s arrete IMMEDIATEMENT au lieu de continuer betement les points
suivants (qui produiraient des erreurs en cascade illisibles). Le `main()`
attrape l exception, affiche le bilan et retourne 1.

## Processus de test

### 1. Preparation

- [ ] Lire le template-test.md (LA reference) AVANT d ecrire le test
- [ ] Numeroter le test (test-0XX, numero jamais reutilise)
- [ ] Creer le dossier de test
- [ ] Ecrire la documentation du test

### 2. Execution

- [ ] Charger les protections (PROTECTIONS = charger_protections())
- [ ] Executer chaque commande via lancer_protege (timeout configure)
- [ ] Utiliser verifier_critique sur les points critiques (protection STOP)
- [ ] Capturer les codes de retour et verifier les sorties

### 3. Rapport

- [ ] Generer le bilan RESULTAT : N OK / M KO
- [ ] Identifier les problemes
- [ ] Documenter les erreurs
- [ ] Proposer des corrections

### 4. Preuve negative OBLIGATOIRE (v0.3.2, demande utilisateur 2026-08-14)

REGLE IMMUABLE -- PREUVE NEGATIVE : TOUT GARDE-FOU DOIT PROUVER QU IL
ATTRAPE SA VIOLATION, PAS SEULEMENT QU IL PASSE SUR L ETAT SAIN.

Un test qui passe sur l etat sain peut ne RIEN detecter : la seule facon de
prouver qu un garde-fou attrape reellement ce qu il doit attraper est
D INSERER TEMPORAIREMENT la violation qu il surveille et de constater le KO.

- Apres avoir cree ou renforce un garde-fou, inserer UNE violation reelle du
  type surveille (declaration fautive au registre, outil interdit dans une
  carte, case orpheline, trace CRLF, faute d orthographe...).
- Executer le test : le point dedie doit passer de OK a KO.
- RETIRER la violation : le test doit revenir a OK.
- Documenter la preuve dans la lecon de mission : "preuve negative : violation
  X inseree -> KO sur le point Y, retiree -> OK".
- Un garde-fou sans preuve negative documentee est CONSIDERE NON VERIFIE :
  il faut le prouver avant de valider la mission.

EXEMPLE (test-037 point 2b, 2026-08-14) : fausse declaration
`themis -> tester-lancer-non-regression` inseree au registre -> point 2b KO
(5 OK / 1 KO) -> declaration retiree -> 6 OK / 0 KO. La preuve a revele que
le garde-fou attrapait bien la violation (et que le TROU initial - le point
2b n existait pas - laissait passer les declarations fautives).

## Codes de retour des protections

| Code | Signification |
|---|---|
| 0 | Test reussi |
| 1 | Test echoue (ou ArretProtection) |
| 124 | Timeout (boucle infinie detectee - anciennes protections) |
| 137 | Processus tue (blocage detecte - anciennes protections) |
| 255 | Erreur de protection |

Le module tester-protections leve `ArretProtection` (exception Python) au lieu
de codes 124/137 : le test l attrape et retourne 1 avec un bilan propre.

## Delegation des tests

REGLE IMMUABLE -- DELEGATION : SEUL MORPHEUS ECRIT ET EXECUTE LES TESTS.

- Seul l'agent Morpheus (testeur) cree, adapte et execute les fichiers de test
  `test-XXX-*` : la creation, la mise a jour et meme l'adaptation mineure d'un
  test existant (version, nombre de points, attentes) sont son role.
- Aucun autre agent ne touche a un fichier de test, meme pour une correction
  rapide ou un simple controle (bash -n, py_compile, cas dans exemples/).
- Quand une mission implique des tests, l'agent d'origine transmet le besoin a
  Morpheus dans la mission : test-XXX a creer/adapter + points a couvrir.
- Morpheus donne son verdict uniquement via les tests executes et revient a
  l'agent qui l'a active (chaine bout-en-bout).

### Garde-fous de non-regression

REGLE IMMUABLE -- GARDE-FOU FIN DE PARCOURS : APRES TOUTE MODIFICATION D'UNE FIN
DE PARCOURS, LE TEST-018 DOIT RESTER VERT.

- Une fin de parcours = toute case de type `fin` (titre `FIN - Reactiver Cerberus`
  ou `FIN - Activer X`) dans les 11 parcours agents (parcours-*.json).
- Apres CHAQUE creation, edition ou suppression d'une fin de parcours (titre,
  message, commande, suivant), executer :
  `python3 cerveau-projet/agents/tools/tester/tests/test-018-fins-reactivation/test-018-fins-reactivation.py`
- Le test-018 verifie : regle Pattern 13 (toute fin REACTIVER porte la condition
  `activation directe par Cerberus` OU est le dernier maillon avec bilan
  consolide), les 4 fins precisees (atlas c11, clio c12, minerve c10, themis
  c13) et l'anti-regression du piege reactiver (aucune fin `Activer X` ne doit
  contenir la commande reactiver).
- Verdict attendu : 0 KO. Si KO, corriger la fin modifiee (condition manquante,
  piege reactiver reintroduit) AVANT de valider la mission.
- Ce garde-fou s'ajoute aux tests de navigation existants (test-013, test-016).

REGLE IMMUABLE -- RE-SCAN COMPLET : APRES CHAQUE REFONTE D'OUTIL OU DE PARCOURS,
RE-SCANNER TOUTE LA SUITE (TEST-009 A TEST-018) ET EXIGER 0 KO.

- Une refonte d'outil = bump de version d'un .py/.sh/.md/spec, modification
  d'interface (options, sous-commandes) ou de comportement.
- Une refonte de parcours = migration (indices references + cases action),
  ajout/suppression de cases ou de fins, changement de version du parcours.
- Apres CHAQUE refonte, re-scanner TOUTE la suite formelle (test-009 a
  test-018) :
  `for d in cerveau-projet/agents/tools/tester/tests/test-0*/; do
   python3 $d/$(basename $d).py || break; done`
  (chaque test-0XX-nom/ contient test-0XX-nom.py a executer)
- Verdict attendu : 0 KO partout. Si KO :
  1. versions attendues obsoletes (lecon : verifier apres chaque bump
     d'outil -- la version affichee par --version doit correspondre a celle
     attendue par le test),
  2. temoins de test obsoletes (lecon : verifier apres chaque migration de
     parcours -- un temoin A ALLEGER peut devenir CONFORME).
- Seul Morpheus adapte les tests obsoletes (REGLE IMMUABLE DELEGATION), et
  ce AVANT de valider la mission.

## Checklist de validation

Avant de valider un test :

- [ ] Les protections sont chargees (PROTECTIONS = charger_protections())
- [ ] Le template-test.md est la reference (pas les tests precedents)
- [ ] Chaque test est numerote et affiche [OK]/[KO]
- [ ] Le timeout est configure (lancer_protege)
- [ ] Les erreurs sont capturees (ArretProtection)
- [ ] La protection STOP est utilisee sur les points critiques
- [ ] Le rapport est genere (bilan RESULTAT : N OK / M KO)
- [ ] Les problemes sont identifies
- [ ] PREUVE NEGATIVE : une violation du type surveille a ete inseree, le
  KO constate sur le point dedie, puis la violation retiree et le vert
  retabli (v0.3.2, REGLE IMMUABLE PREUVE NEGATIVE)
