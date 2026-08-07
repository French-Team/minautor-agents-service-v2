# Test de l'outil mettre-a-jour-agents-md

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

L'outil `mettre-a-jour-agents-md` passe les 4 tests reels. Le cycle complet
(activation -> reactivation -> retour a Cerberus) fonctionne, la limite de 150 entrees
est respectee et l'ordre decroissant est correct. Promotion en version 0.2.0 (statut prepare).

---
