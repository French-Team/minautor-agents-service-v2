---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# Test de l'outil activer-agent-principal

**Version testee** : 0.3.4
**Date** : 2026-08-07
**Agent** : Morpheus (tests formels)
**Statut** : Termine -- valide (19/19 v0.3.4)

---

## Test formel v0.3.4 (mode ID)

Script : `tests/test-004-activer-agent-principal-v034.sh` (3 protections). Tests sur copies.

| # | Cas | Resultat |
|---|---|---|
| 1 | sidentifier llm-atlas (id inconnu, fichier vide) -> session-llm-1 + liaison id | [OK] |
| 2 | Meme id relance -> Session retrouvee (meme session, pas de doublon) | [OK] |
| 3 | 2e LLM id inconnu (llm-athena) -> session-llm-2 + liaison id | [OK] |
| 4 | Deux LLM differents -> JAMAIS la meme session (isolation par id) | [OK] |
| 5 | Redemarrage llm-athena -> retrouve session-llm-2 (pas de doublon) | [OK] |
| 6 | sidentifier SANS argument -> compatibilite heritage (prochaine libre, sans liaison) | [OK] |
| 7 | Parite .sh (id inconnu -> llm-1 + liaison, relance -> retrouve) | [OK] |
| 8 | Regression v0.3.3 (attribution prochaine libre sans argument) | [OK] |
| 9 | Regression v0.3.2 (regle derivation profil-session, 0 ligne session-session-*) | [OK] |

**Verdict : 19/19 reussis, 0 echec -- VALIDE.**

## Test formel v0.3.3 (regle utilisateur identification)

Script : `tests/test-003-activer-agent-principal-v033.sh` (3 protections). Tests sur copies.

| # | Cas | Resultat |
|---|---|---|
| 1 | Fichier vide + sidentifier sans arg -> session-llm-1 (bloc + Cerberus) | [OK] |
| 2 | llm-1 existe + sidentifier sans arg -> session-llm-2 (jamais llm-1) | [OK] |
| 3 | sidentifier session-llm-1 (occupee) -> attribution AUTO prochaine libre + message clair | [OK] |
| 4 | sidentifier session-llm-5 (libre) -> attribuee telle quelle | [OK] |
| 5 | Historique utilise la NOUVELLE session (jamais la session occupee) | [OK] |
| 6 | Profil classeur suit la NOUVELLE session (0 ligne profil-session-session-*) | [OK] |
| 7 | Parite .sh (fichier vide -> llm-1, occupee -> prochaine libre + message) | [OK] |
| 8 | Regression v0.3.2 (profil session activer/reactiver) | [OK] |

**Verdict : 21/21 reussis, 0 echec -- VALIDE.**

## Test formel v0.3.2 (regle de derivation du nommage)

Script : `tests/test-002-activer-agent-principal-v031.sh` (adopte v0.3.2, 3 protections). Tests sur copies.

| # | Cas | Resultat |
|---|---|---|
| 1 | sidentifier -> ligne `profil-session-llm-1` (PAS profil-session-session-llm-1) avec Cerberus + format exact | [OK] |
| 2 | activer Buffy -> mise a jour sans doublon | [OK] |
| 3 | reactiver -> agent=Cerberus | [OK] |
| 4 | session session-llm-2 -> ligne `profil-session-llm-2` ajoutee | [OK] |
| 5 | Autres lignes intactes | [OK] |
| 6 | Parite .sh | [OK] |
| 7 | VERIFICATION NEGATIVE : aucune ligne profil-session-session-* | [OK] |
| 8 | Regression v0.3.0 (test-001, 12 cas) | [OK] |

**Verdict : 8/8 reussis, 0 echec -- VALIDE.**

Bug detecte et corrige pendant les tests : `session[7:]` retirait un caractere de trop ("session-" fait 8 caracteres) -> id `-llm-1` -> ligne `profil-session--llm-1` (double tiret). Corrige en `session[len("session-"):]` dans le .py et le python embarque du .sh.

---

## Test formel v0.3.1 (profil session classeur)

Script : `tests/test-002-activer-agent-principal-v031.sh` (3 protections sourcees). Tests sur copies via variables d'environnement `AGENTS_FILE` / `AGENTS_HISTORIQUE` / `CLASSEUR_STOCKAGE`.

| # | Cas | Resultat |
|---|---|---|
| 1 | sidentifier -> ligne `profil-session-llm-1` creee avec agent=Cerberus + format exact (5 colonnes, HH:MM, source, [OK]) | [OK] |
| 2 | activer Buffy -> mise a jour de la ligne (agent=Buffy), PAS de doublon | [OK] |
| 3 | reactiver -> agent=Cerberus | [OK] |
| 4 | Session inexistante (session-llm-2) -> ligne AJOUTEE a la fin du tableau | [OK] |
| 5 | Autres lignes du stockage intactes (aucune perte) | [OK] |
| 6 | Parite .sh : la version bash ecrit aussi le classeur | [OK] |
| 7 | Regression v0.3.0 : relance test-001 (12 cas) | [OK] |

**Verdict : 7/7 reussis, 0 echec -- VALIDE.**

Correction pendant les tests (Morpheus) : chemin des protections corrige dans test-001 ET test-002 (`tests/../../../tester/protections` au lieu de `tests/../../../../tester/protections` -- les protections n'etaient pas reellement chargees avant).

---

## Test formel v0.3.0 (multi-session LLM)

Script : `tests/test-001-activer-agent-principal.sh` (3 protections sourcees : boucles-infinies, erreurs-silencieuses, blocage). Tests sur copies via variables d'environnement `AGENTS_FILE` / `AGENTS_HISTORIQUE`.

| # | Cas | Resultat |
|---|---|---|
| 1 | Migration ancienne structure + sidentifier auto (py) : bloc session-llm-1, valeurs conservees, historique | [OK] |
| 2 | Deuxieme sidentifier auto -> session-llm-2 | [OK] |
| 3 | sidentifier nom explicite (session-llm-5) | [OK] |
| 4 | Isolation : activer session-llm-1 ne change pas session-llm-2 | [OK] |
| 5 | activer : tous les champs (Nom, Role, Fiche, Corrections, Active par, Raison) | [OK] |
| 6 | reactiver : Cerberus remis + Active par = agent precedent | [OK] |
| 7 | Historique 4 colonnes + ordre decroissant | [OK] |
| 8 | Parite .sh : migration + activer via bash | [OK] |
| 9 | Raison non-ASCII REFUSEE (exit 1, fichier intact) | [OK] |
| 10 | Action sessions : liste correcte | [OK] |
| 11 | Syntaxe bash -n + py_compile | [OK] |
| 12 | Conventions : ASCII strict + nommage | [OK] |

**Verdict : 12/12 reussis, 0 echec -- VALIDE.**

Bugs detectes et corriges pendant les tests (boucle Morpheus -> Vulcain) :
1. `sidentifier` apres migration ne persistait pas le contenu migre (fichier restait en ancienne structure) -- corrige dans le .py (ecrire_agents dans la branche migre).
2. Message "Session attribuee" jamais affiche apres migration (migration creait deja le bloc session-llm-1) -- corrige (migre -> utiliser session-llm-1 + message identification).

---

## Tests v0.2.0 (historique)

**Version testee** : 0.2.0
**Date** : 2026-08-06
**Agent** : Cerberus (passage V2)
**Statut** : Termine -- valide

---

## Environnement de test

Test reel dans un environnement isole (copies dans `exemples/`) pour ne pas toucher les fichiers reels.
Protections appliquees : timeout 10s sur chaque appel (tester-protection-boucles-infinies).

---

## Test 1 : Activation d'un agent

### Appel reel

```bash
outil-test.sh activer "Buffy" "Test V2 pilote" "Verifier le cycle"
```

### Resultat observe

```
Historique mis a jour dans .../AGENTS-historique.md
Agent Buffy active avec succes
```

AGENTS.md verifie :
- Nom : Buffy
- Active par : Cerberus (automatique)
- Raison : Test V2 pilote

**Statut du test** : [OK] Reussi

---

## Test 2 : Reactivation de Cerberus

### Appel reel

```bash
outil-test.sh reactiver "Test termine" "Buffy"
```

### Resultat observe

```
Lecture de .../cerveau-projet/agents/cerberus/cerberus.md...
Historique mis a jour dans .../AGENTS-historique.md
Cerberus reactive avec succes
```

AGENTS.md verifie :
- Nom : Cerberus
- Active par : Buffy (retour de mission)

**Statut du test** : [OK] Reussi

---

## Test 3 : Limite de 150 entrees

### Verification

Nombre d'entrees dans AGENTS-historique.md apres les 2 tests : 150 (maximum respecte).

**Statut du test** : [OK] Reussi

---

## Test 4 : Ordre decroissant

### Verification

Les entrees les plus recentes sont en HAUT du tableau (la derniere intervention apparait en premiere ligne).

**Statut du test** : [OK] Reussi

---

## Optimisations appliquees lors du passage V2

| Optimisation | Avant | Apres |
|---|---|---|
| Version dans le script | absente | `VERSION="0.2.0"` |
| En-tete du .md | Version 0.1.0-beta, Statut beta | Version 0.2.0, Statut prepare |
| Tableau versionning | 0.2.0-beta mentionne sans ligne de promotion | entree 0.2.0 ajoutee (tests reels + promotion) |

---

## Conclusion

L'outil `activer-agent-principal` passe les 12 tests formels v0.3.0. Le cycle multi-session
complet (identification -> activation -> isolation -> reactivation -> retour a Cerberus dans
sa session) fonctionne, l'historique 4 colonnes est correct, la limite de 150 entrees est
respectee et l'ordre decroissant est correct. Promotion en version 0.3.0 (statut prepare).

---
