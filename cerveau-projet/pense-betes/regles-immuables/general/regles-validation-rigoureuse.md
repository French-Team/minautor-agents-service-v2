# Règle Immuable — Validation Rigoureuse
---

## Principe Fondamental
---

## Le problème

| Comportement | Problème |
|---|---|
| Écrire des tests qui passent | L'agent se donne raison |
| Ne pas couvrir tous les cas | Les bugs restent cachés |
| Utiliser des commandes sans comprendre | Les résultats ne sont pas analysés |
| Ne pas revérifier | Les erreurs passent inaperçues |

---

## La solution : 4 niveaux de validation

### Niveau 1 — Test automatisé

```
1. Écrire le test
2. Exécuter le test
3. Vérifier que le test passe
4. MAIS ne pas s'arrêter là
```

**Limite** : Le test peut passer sans que le code fonctionne vraiment.

---

### Niveau 2 — Vérification manuelle

```
1. Lire le code généré
2. Vérifier que le code fait ce qu'on attend
3. Exécuter le code dans un cas réel
4. Comparer le résultat attendu avec le résultat obtenu
```

**Limite** : L'humain peut faire des erreurs de lecture.

---

### Niveau 3 — Revue par un autre

```
1. Demander une revue (ou se mettre à la place de l'autre)
2. Lire le code avec un regard critique
3. Chercher explicitement les erreurs
4. Poser la question : "Est-ce que VRAIMENT ça marche ?"
```

**Limite** : Le reviewer peut avoir les mêmes biais.

---

### Niveau 4 — Preuve par l'usage

```
1. Utiliser le code dans un cas réel
2. Vérifier que le résultat est correct
3. Documenter ce qui a marché et ce qui n'a pas marché
4. Ajouter des tests pour les cas non couverts
```

**Limite** : Certains bugs n'apparaissent qu'en production.

---

## Règles de validation

### Règle 1 — Jamais de test sans vérification

```
[NON] Ecrire un test -> il passe -> c'est bon
[OUI] Ecrire un test -> il passe -> lire le code -> executer manuellement -> valider
```

---

### Règle 2 — Toujours couvrir les cas limites

```
Pour chaque fonction, tester :
- Cas normal
- Cas limite (vide, nul, max, min)
- Cas d'erreur (invalide, manquant, corrompu)
- Cas de performance (grand nombre, lent)
```

---

### Règle 3 — Toujours exécuter avant de valider

```
[NON] "J'ai ecrit le test, il devrait passer"
[OUI] "J'ai execute le test, voici le resultat"
```

---

### Règle 4 — Documenter les échecs

```
Quand un test échoue :
1. Documenter l'erreur
2. Identifier la cause
3. Corriger
4. Ré-exécuter
5. Valider que ça marche VRAIMENT
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
- [ ] Le code a été lu et compris
- [ ] Le code a été exécuté manuellement
- [ ] Les cas limites sont testés
- [ ] Les erreurs sont documentées
- [ ] La revue a été effectuée
- [ ] Le résultat est prouvé par l'usage

---

## Pièges courants

| Piège | Solution |
|---|---|
| "Le test passe donc c'est bon" | Toujours vérifier manuellement |
| "J'ai testé les cas normaux" | Tester les cas limites aussi |
| "Ca marche sur ma machine" | Tester dans un environnement similaire a la production |
| "Le code est simple, pas besoin de test" | Tout code a besoin de validation |
| "Je fais confiance au test" | Ne jamais faire confiance aveuglément |

---

## Exemple de bonne pratique

```
1. Écrire la fonction `calculer-somme`
2. Écrire un test qui vérifie `calculer-somme(1, 2) == 3`
3. Exécuter le test → il passe
4. Lire le code → vérifier la logique
5. Executer manuellement : calculer-somme(1, 2) -> 3 [OK]
6. Tester les cas limites :
   - calculer-somme(0, 0) == 0 [OK]
   - calculer-somme(-1, 1) == 0 [OK]
   - calculer-somme(1000000, 2000000) == 3000000 [OK]
7. Vérifier les erreurs :
   - calculer-somme(null, 1) → erreur documentée
8. Valider : la fonction fonctionne VRAIMENT
```

---

## Lien avec les autres règles

- [regles-choisir-agent](regles-choisir-agent.md) — choisir le bon agent pour la validation
- [rvav-workflow](rvav-workflow.md) — le workflow de validation
- [protocole-auto-correction](protocole-auto-correction/) — corriger les erreurs trouvées

---

