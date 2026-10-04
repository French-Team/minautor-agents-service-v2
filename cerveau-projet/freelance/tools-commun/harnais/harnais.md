# harnais-v2

> Harnais de securite GENERALISE aux outils v2 (decision utilisateur
> 2026-08-25) : chaque outil v2 importe un mini-test de conformite qui
> emet des messages par situation (OK / WARN / ERR / CRIT). Plus rien
> n est fait par un agent v2 sans le harnais correspondant. Les scripts
> temporaires sont proteges par leur harnais.

| Version | 0.2.0 | Proprietaire | Forge (outils) / Rogers (protocoles) |

## Principe

```
AGENT v2 veut utiliser un outil ou un script
    |
    v
HARNAIS s active (import verifier_outil / verifier_script)
    |
    +---> SIG OK   : conforme -> tu continues
    +---> SIG WARN : anomalie mineure -> tu continues mais tu signales
    +---> SIG ERR  : erreur -> tu STOPPES et tu corriges
    +---> SIG CRIT : critique -> arret immediat
```

**Les messages sont INTUITIFS** : chaque signal dit ce qui ne va pas ET
quoi faire ensuite. L agent n a pas a reflechir pour savoir comment
reagir : le harnais lui donne la reponse.

## Integration dans un outil v2 (OBLIGATOIRE)

Chaque outil v2 DOIT importer et appeler le harnais en debut de traitement :

```python
# entry.py de l outil
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "tools-commun", "harnais", "fonctions"))
try:
    from harnais import verifier_outil
    _CHEMIN = os.path.dirname(os.path.abspath(__file__))
except ImportError:
    verifier_outil = None

def main():
    args = parse_args()
    if verifier_outil is not None:
        verifier_outil(_CHEMIN, agent="<outil>")
    # ... suite du traitement
```

## CLI

```
python3 tools-commun/harnais/entry.py outil <chemin_outil> [--agent A]
python3 tools-commun/harnais/entry.py script <chemin_script> [--agent A] [--raison R]
python3 tools-commun/harnais/entry.py exec <chemin_script> [--agent A] [--raison R] [--timeout S]
python3 tools-commun/harnais/entry.py aide
```

## Execution protegee (AVANT -> PENDANT -> APRES)

L agent appelle UNE commande (`harnais exec`) ; le harnais fait tout le
reste, transparent pour l agent :

| Phase | Fonctions du harnais |
|---|---|
| **AVANT** | verifications (agent, raison) ; securites (zone, isolation) ; imports obligatoires ; syntaxe Python (compile) ; backup empreinte + etat de la zone ; journalisation ; LECONS APPRISES diffusees (BDD v2) |
| **PENDANT** | execution via subprocess avec PYTHONPATH INJECTE (os_path, bdd-lecons, harnais) ; timeout ; capture stdout/stderr |
| **APRES** | verdict rc ; detection d effets (fichiers crees hors zone, script modifie) ; rappels (lifecycle, promotion, entonnoir) ; lecons diffusees ; journalisation finale |

### Transparence totale (PROTOCOLE 22 : l agent n a PAS a reflechir)

- **Le script s execute sans sys.path manuel** : le harnais injecte les
  chemins v2 (os_path, bdd-lecons, harnais) dans PYTHONPATH avant de
  lancer. L agent ecrit `from racine import trouver_racine` directement.
- **Les lecons apprises sont diffusees automatiquement** : avant chaque
  execution, le harnais affiche les lecons recentes de l agent (BDD
  v2, D10) -- `=== LECONS APPRISES (BDD v2) ===`. L agent voit ce que
  les autres (et lui) ont appris, sans avoir a chercher.

## Scripts temporaires (PROTOCOLE 21 + proto-13 v1 + REGLE D ORIGINE v1)

> REGLE D ORIGINE (v1, demandee pour la v2 par l utilisateur 2026-08-25) :
> chaque agent cree SON dossier temporaire a la RACINE du workspace,
> `tmp-<agent>/` (ex: tmp-stark/, tmp-vision/), comme dans la v1.

| Regle | Detail |
|---|---|
| **Dossier dedie a l agent** | `tmp-<agent>/` a la RACINE du workspace (jamais le /tmp systeme) |
| **Jamais ailleurs** | Un script dans /tmp systeme, a la racine, ou dans un dossier d outil = ERR |
| **Isolation** | Pas de chemin absolu suspect : le script ne touche QUE son dossier |
| **Lifecycle** | Creer -> executer -> verifier -> SUPPRIMER (`rm -rf tmp-<agent>` en fin de mission) |

## Signaux

| Signal | Signification | Action de l agent |
|---|---|---|
| `SIG OK` | Tout est conforme | Continuer |
| `SIG WARN` | Anomalie mineure | Continuer + signaler |
| `SIG ERR` | Erreur detectee | STOPPER + corriger |
| `SIG CRIT` | Critique | Arret immediat + restauration |

## Architecture DYNAMIQUE (D15 : separation code/donnees)

> " On importe le harnais, le harnais fait le reste. " Le harnais est
> pilote par la CONFIGURATION, jamais par des editions de code.

Le harnais lit `harnais-data.json` a CHAQUE appel et applique 4 categories :

| Categorie | Cle config | Role |
|---|---|---|
| Securites | `securites[]` | fonctionnement du script (zone tmp-<agent>/, isolation) |
| Verifications | `verifications[]` | agent obligatoire, raison obligatoire (bloquantes) |
| Imports obligatoires | `imports_obligatoires[]` | trouver_racine (P10) present dans le script |
| Rappels | `rappels[]` | utilisation, commande, lifecycle, promotion, entonnoir |

**REGLE (anti-edition) :** ajouter un import obligatoire, une verification,
un rappel ou une securite = editer `harnais-data.json` UNIQUEMENT. Jamais
le code, jamais les scripts. Le harnais fait le reste.

## Diffusion des lecons (BDD v2, D10)

> Les harnais rappellent les LECONS APPRISES par les agents : la BDD des
> lecons v2 (outil `bdd-lecons`, SQLite) est une bible consultable au
> moment du besoin (decision utilisateur 2026-08-25).

| Module | Role |
|---|---|
| `fonctions/lecons.py` | lit la BDD (bdd-lecons) et formate les rappels : priorite aux lecons de l agent, puis categorie, puis globales |
| Tolerant | si la BDD est absente, message discret au lieu de planter (le harnais ne bloque JAMAIS sur une lecon) |

## Emplacement

```
cerveau-projet/freelance/tools-commun/harnais/
  harnais.md           <- ce document
  harnais-data.json    <- CONFIG DYNAMIQUE (D15 : la seule chose a editer)
  entry.py             <- CLI directe
  fonctions/harnais.py <- logique (signaux, verifier_outil, verifier_script)
  fonctions/lecons.py  <- diffusion des lecons (BDD v2, D10)
  fonctions/nettoyage.py <- compensation (nettoyage tmp-<agent> orphelins)
```