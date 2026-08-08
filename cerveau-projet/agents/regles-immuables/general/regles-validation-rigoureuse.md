---
identite:
  type: regle
  appartient_a: commun
  commun: true
---
# Regle Immuable -- Validation Rigoureuse
---

## Principe Fondamental
---

## Le probleme

| Comportement | Probleme |
|---|---|
| Ecrire des tests qui passent | L'agent se donne raison |
| Ne pas couvrir tous les cas | Les bugs restent caches |
| Utiliser des commandes sans comprendre | Les resultats ne sont pas analyses |
| Ne pas reverifier | Les erreurs passent inapercues |

---

## La solution : 4 niveaux de validation

### Niveau 1 -- Test automatise

```
1. Ecrire le test
2. Executer le test
3. Verifier que le test passe
4. MAIS ne pas s'arreter la
```

**Limite** : Le test peut passer sans que le code fonctionne vraiment.

---

### Niveau 2 -- Verification manuelle

```
1. Lire le code genere
2. Verifier que le code fait ce qu'on attend
3. Executer le code dans un cas reel
4. Comparer le resultat attendu avec le resultat obtenu
```

**Limite** : L'humain peut faire des erreurs de lecture.

---

### Niveau 3 -- Revue par un autre

```
1. Demander une revue (ou se mettre a la place de l'autre)
2. Lire le code avec un regard critique
3. Chercher explicitement les erreurs
4. Poser la question : "Est-ce que VRAIMENT ca marche ?"
```

**Limite** : Le reviewer peut avoir les memes biais.

---

### Niveau 4 -- Preuve par l'usage

```
1. Utiliser le code dans un cas reel
2. Verifier que le resultat est correct
3. Documenter ce qui a marche et ce qui n'a pas marche
4. Ajouter des tests pour les cas non couverts
```

**Limite** : Certains bugs n'apparaissent qu'en production.

---

## Regles de validation

### Regle 1 -- Jamais de test sans verification

```
[NON] Ecrire un test -> il passe -> c'est bon
[OUI] Ecrire un test -> il passe -> lire le code -> executer manuellement -> valider
```

---

### Regle 2 -- Toujours couvrir les cas limites

```
Pour chaque fonction, tester :
- Cas normal
- Cas limite (vide, nul, max, min)
- Cas d'erreur (invalide, manquant, corrompu)
- Cas de performance (grand nombre, lent)
```

---

### Regle 3 -- Toujours executer avant de valider

```
[NON] "J'ai ecrit le test, il devrait passer"
[OUI] "J'ai execute le test, voici le resultat"
```

---

### Regle 4 -- Documenter les echecs

```
Quand un test echoue :
1. Documenter l'erreur
2. Identifier la cause
3. Corriger
4. Re-executer
5. Valider que ca marche VRAIMENT
```

---

## Matrice de validation

| Type de code | Niveau 1 | Niveau 2 | Niveau 3 | Niveau 4 |
|---|---|---|---|---|
| **Fonction simple** | [OUI] Test | [OUI] Lecture | [NON] | [NON] |
| **Fonction critique** | [OUI] Test | [OUI] Execution | [OUI] Revue | [NON] |
| **Module complet** | [OUI] Tests | [OUI] Execution | [OUI] Revue | [OUI] Usage |
| **Protocole** | [OUI] Tests | [OUI] Verification | [OUI] Revue | [OUI] Validation |

---

## Checklist de validation

Avant de valider un travail :

- [ ] Les tests passent
- [ ] Le code a ete lu et compris
- [ ] Le code a ete execute manuellement
- [ ] Les cas limites sont testes
- [ ] Les erreurs sont documentees
- [ ] La revue a ete effectuee
- [ ] Le resultat est prouve par l'usage

---

## Pieges courants

| Piege | Solution |
|---|---|
| "Le test passe donc c'est bon" | Toujours verifier manuellement |
| "J'ai teste les cas normaux" | Tester les cas limites aussi |
| "Ca marche sur ma machine" | Tester dans un environnement similaire a la production |
| "Le code est simple, pas besoin de test" | Tout code a besoin de validation |
| "Je fais confiance au test" | Ne jamais faire confiance aveuglement |

---

## Exemple de bonne pratique

```
1. Ecrire la fonction `calculer-somme`
2. Ecrire un test qui verifie `calculer-somme(1, 2) == 3`
3. Executer le test -> il passe
4. Lire le code -> verifier la logique
5. Executer manuellement : calculer-somme(1, 2) -> 3 [OK]
6. Tester les cas limites :
   - calculer-somme(0, 0) == 0 [OK]
   - calculer-somme(-1, 1) == 0 [OK]
   - calculer-somme(1000000, 2000000) == 3000000 [OK]
7. Verifier les erreurs :
   - calculer-somme(null, 1) -> erreur documentee
8. Valider : la fonction fonctionne VRAIMENT
```

---

## Lien avec les autres regles

- [regles-choisir-agent](regles-choisir-agent.md) -- choisir le bon agent pour la validation
- [rvav-workflow](rvav-workflow.md) -- le workflow de validation
- [protocole-auto-correction](protocole-auto-correction/) -- corriger les erreurs trouvees

---

