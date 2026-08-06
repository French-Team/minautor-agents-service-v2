# Protocole Immuable — Recherches Web
---

## Principe Fondamental
---

## Quand faire des recherches ?

| Situation | Action |
|---|---|
| Nouvelle technologie mentionnée | Rechercher |
| API inconnue | Rechercher |
| Comportement supposé | Rechercher |
| Dépendance non vérifiée | Rechercher |
| Fonctionnalité non documentée | Rechercher |

---

## Étape 1 — Identifier le besoin de recherche

```
1. Qu'est-ce que je ne sais pas ?
2. Qu'est-ce que je suppose ?
3. Qu'est-ce que je dois vérifier ?
4. Qu'est-ce que l'utilisateur demande ?
```

---

## Étape 2 — Rechercher dans le cerveau

```
1. Chercher dans recherches-web/
2. Chercher dans les conventions
3. Chercher dans les règles
4. Chercher dans les specs
```

### Si la recherche existe déjà

```
1. Lire la recherche existante
2. Vérifier qu'elle est encore valide
3. Mettre à jour si nécessaire
4. Utiliser comme preuve
```

### Si la recherche n'existe pas

```
1. Passer à l'étape 3
```

---

## Étape 3 — Rechercher sur le web

```
1. Utiliser researcher-web ou researcher-docs
2. Collecter les informations
3. Vérifier les sources
4. Documenter dans recherches-web/
```

### Sources prioritaires

| Priorité | Source | Fiabilité |
|---|---|---|
| 1 | Documentation officielle | Haute |
| 2 | GitHub officiel | Haute |
| 3 | Blog technique reconnu | Moyenne |
| 4 | Stack Overflow | Moyenne |
| 5 | Forums spécialisés | Basse |

---

## Étape 4 — Documenter la recherche

```
1. Créer le dossier recherches-web/[theme]/ si nécessaire
2. Copier le template recherche-template.md
3. Remplir toutes les sections
4. Citer les sources
5. Mettre à jour l'index du thème
6. Mettre à jour l'index principal
```

---

## Étape 5 — Vérifier la validité

```
1. Les informations sont-elles encore valides ?
2. Y a-t-il des changements récents ?
3. Sont-elles compatibles avec le projet ?
4. Comparer avec le code source
```

---

## Étape 6 — Appliquer les informations

```
1. Utiliser les informations comme preuve
2. Ne jamais avancer sans recherche
3. Documenter comment les informations sont utilisées
4. Mettre à jour le cerveau si nécessaire
```

---

## Structure des recherches

```
recherches-web/
├── index-recherches-web.md
├── [theme-1]/
│   ├── index.md
│   ├── [recherche-1].md
│   └── [recherche-2].md
├── [theme-2]/
│   └── ...
└── templates/
    └── recherche-template.md
```

---

## Règles de documentation

### Obligations

- [ ] Documenter chaque recherche
- [ ] Citer les sources
- [ ] Mettre à jour les recherches obsolètes
- [ ] Vérifier la validité des informations
- [ ] Comparer avec le code source

### Interdictions

- [ ] Utiliser des informations non vérifiées
- [ ] Inventer des sources
- [ ] Copier sans citer
- [ ] Utiliser des informations obsolètes
- [ ] Avancer sans recherche

---

## Validation

Avant de valider une recherche, vérifier :

- [ ] Sources citées
- [ ] Informations vérifiées
- [ ] Validité confirmée
- [ ] Comparaison avec code source effectuée
- [ ] Documenté dans recherches-web/

---

## Liens

- **Règle** : [regles-veracite.md](../regles-veracite.md) -- ne jamais mentir ou inventer
- **Convention** : [convention-protocoles.md](../../../conventions/protocoles/convention-protocoles.md)
- **Index** : [recherches-web/index-recherches-web.md](../../../../recherches-web/index-recherches-web.md)
- **Protocoles** : [protocole-installer-regles](../protocole-installer-regles/) -- installer les regles immuables
- **Protocoles** : [protocole-identification](../protocole-identification/) -- identification des agents

---

