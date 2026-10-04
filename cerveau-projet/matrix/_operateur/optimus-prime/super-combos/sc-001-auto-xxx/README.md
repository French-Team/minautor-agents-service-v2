---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# Super-Combos AUTO-XXX

## Description

Ce super-combos enchaine intelligement les themes AUTO-XXX dans l'ordre optimal pour garantir la qualite et la securite des modifications.

## Themes enchaines

0. **PREPARATION** : Analyse et comprehension du probleme avant correction
1. **AUTO-CORRECTION** : Correction automatique des erreurs detectees (ASCII, syntaxe, imports, conventions)
2. **AUTO-TESTING** : Tests automatiques post-modification (py_compile, tests unitaires, verification d'integrite)
3. **AUTO-OPTIMISATION** : Optimisation des performances (mesurer avant, optimiser, mesurer apres)
4. **AUTO-PERFORMANCE** : Mesure de performance apres creation (comparer aux seuils, detecter regressions)
5. **AUTO-AUDIT-NEMESIS** : Audit 3 axes avant validation (cas limites, optimisation, securite)

## Utilisation

```bash
# Execution simple
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/sc-001-auto-xxx/main.py executer --fichier <fichier>

# Execution complete avec toutes les phases
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/sc-001-auto-xxx/main.py executer-complet --fichier <fichier>

# LA CHAINE DU PILOTE : le super-combo sert le pilote d'Optimus
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/sc-001-auto-xxx/main.py pilote

# Verification du statut
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/sc-001-auto-xxx/main.py status
```

## Chaine du PILOTE (EO-275, demande du createur)

Le super-combo sert le PILOTE : il ne juge pas ses missions, il verifie que ses PORTES
repondent AVEC LEUR TEMOIN, et il nomme celles qui ne temoignent pas. Meme mecanique que
les six phases -- `un temoin ou rien` : une porte qui sort en 0 sans dire sa phrase est
ACCUSEE, parce qu'une porte muette et une porte aveugle se ressemblent.

| Porte | Ce qu'elle prouve | Temoin attendu |
|---|---|---|
| FLUX2 | Optimus travaille dans son flux reserve | `FLUX 2 RESPECTE` |
| MARBRE | la trace debut/fin est coherente | `Coherence debut/fin : OK` |
| TRACE | chaque cle de modification est canonique | `toutes relatives a la racine de la Matrice` |
| CARTES | chaque document dit QUOI il est | `VERDICT OK : tout document de la zone` |
| MACHINE | la fiche machine dit la machine | `VERDICT OK : la fiche dit la machine` |
| COMMANDES | aucune commande fautive dans les documents | `Commandes fautives : 0` |
| INTEGRITE | les BDD verrouillees sont intactes | `Passe complete : aucune alerte` |

Chaque porte est appelee par sa PORTE OFFICIELLE (`lancer.py`), jamais recopiee
(convention LIEN, 2). Les temoins sont des phrases MESUREES sur une sortie reelle le
2026-09-22, jamais devinees.

## Outils Associes

### garde-flux2.py
Verifie qu'Optimus ne travaille QUE dans le Flux 2 (maintenance).
```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/outils/garde-flux2.py --racine <chemin> [--verbose] [--strict]
```

### watchdog-flux2.py
Monitoring temps reel des violations Flux 2.
```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/outils/watchdog-flux2.py --racine <chemin> --interval <sec> --log <fichier>
```

### demarrer-watchdog.py
Script pour demarrer/arreter le watchdog en arriere-plan.
```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/outils/demarrer-watchdog.py demarrer [--interval <sec>]
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/outils/demarrer-watchdog.py arreter
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/outils/demarrer-watchdog.py status
python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/combos/outils/demarrer-watchdog.py violations [--dernieres <n>]
```

## Ordre d'execution

L'ordre est critique :
0. D'abord comprendre le probleme (PREPARATION)
1. Puis corriger les erreurs (AUTO-CORRECTION)
2. Ensuite tester les corrections (AUTO-TESTING)
3. Puis optimiser si necessaire (AUTO-OPTIMISATION)
4. Mesurer les performances (AUTO-PERFORMANCE)
5. Enfin, audit Nemesis avant validation (AUTO-AUDIT-NEMESIS)

## Garde-fou

- Si l'audit Nemesis echoue, la validation est bloquee
- Chaque phase est executee meme si la precedente a echoue (pour avoir le tableau complet)
- Le rapport final indique le nombre de succes/echecs
- Le watchdog detecte les violations en temps reel
