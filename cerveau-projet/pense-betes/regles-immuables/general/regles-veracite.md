# Règle Immuable — Véracité et Honnêteté

> Un agent ne doit JAMAIS mentir, inventer, ou supposer.

---

## Principe Fondamental
---

## Pourquoi ?

| Problème | Solution |
|---|---|
| Code qui ne fonctionne pas | Vérifier avant d'affirmer |
| Dépendances inventées | Rechercher la documentation |
| APIs inexistantes | Vérifier l'existence |
| Comportements supposés | Tester avant de valider |
| Informations obsolètes | Rechercher les mises à jour |

---

## Règles détaillées

### Règle 1 — Jamais de supposition

```
[NON] "Je pense que cette bibliothèque fait X"
[OUI] "J'ai vérifié la documentation, cette bibliothèque fait X"
```

### Règle 2 — Jamais d'invention

```
[NON] "Cette API existe et fait X"
[OUI] "J'ai cherché, cette API n'existe pas / fait Y"
```

### Règle 3 — Toujours documenter les recherches

```
[ ] Recherches effectuées dans recherches-web/
[ ] Sources vérifiées
[ ] Informations validées
```

### Règle 4 — Comparer code et recherches

```
[ ] Code source = ce que disent les recherches ?
[ ] Comportements = ce que disent les docs ?
[ ] Dépendances = ce qui existe vraiment ?
```

---

## Application

### Pendant l'analyse

```
1. Lire la demande de l'utilisateur
2. Rechercher dans le cerveau
3. Rechercher sur le web si nécessaire
4. Documenter les recherches dans recherches-web/
5. Ne passer à la phase suivante qu'avec des certitudes
```

### Pendant le développement

```
1. Vérifier chaque API utilisée
2. Vérifier chaque dépendance
3. Vérifier chaque comportement
4. Documenter les vérifications
5. Ne jamais avancer sur des suppositions
```

### Pendant les tests

```
1. Tester chaque fonctionnalité
2. Vérifier chaque résultat
3. Comparer avec les attentes
4. Documenter les écarts
5. Ne jamais déclarer "ça marche" sans preuve
```

---

## Conséquences du non-respect

| Infraction | Conséquence |
|---|---|
| Supposition non vérifiée | Revenir à la phase de recherche |
| Invention détectée | Supprimer et corriger |
| Mensonge sur le statut | Réviser tout le travail |
| Recherche manquante | Ajouter la recherche |

---

## Validation

Avant de valider tout travail, vérifier :

- [ ] Aucune supposition non vérifiée
- [ ] Aucune invention
- [ ] Toutes les recherches documentées
- [ ] Code = ce que disent les recherches
- [ ] Comportements = ce que disent les docs

---

## Liens

- [regles-validation-rigoureuse.md](regles-validation-rigoureuse.md) — validation rigoureuse
- [regles-choisir-agent.md](regles-choisir-agent.md) — choisir le bon agent
- [rvav-workflow.md](rvav-workflow.md) — workflow de validation
- [protocole-recherches-web](protocole-recherches-web/) — protocole de recherches

---

## Navigation

- **Parent** : [index-regles-general.md](index-regles-general.md)
- **Regles** : [index-regles-immuables.md](../index-regles-immuables.md)
