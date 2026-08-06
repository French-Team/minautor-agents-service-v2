# Workflow RVAVP — Rechercher -> Vérifier -> Analyser -> Valider -> Purifier

## Principe fondamental

Chaque fichier de contenu (`[type]-[thème].[id].[class].[statut].md`) passe par
5 statuts. Le passage du statut N au statut N+1 **exige une boucle RVAVP complète**
sur le travail effectué dans le statut N.

**On ne peut jamais passer au statut supérieur sans avoir passé la boucle de
contrôle du statut courant.** Une erreur déclenche une régression + incrément du `class`.

**Nouveau** : La purification est la dernière étape avant de considérer un fichier comme validé.

---

## Les 5 statuts

| Statut | Ordre | Travail attendu |
|---|---|---|
| `ebauche` | 1 | Idée brute, structure minimale, rien de validé |
| `préparé` | 2 | Structure complète, ready pour le développement |
| `dev` | 3 | Contenu développé (toutes les sections écrites) |
| `test` | 4 | RVAV effectué, liens vérifiés, cohérence validée |
| `valide` | 5 | Approuvé, référence fiable pour le projet |

---

## Boucle RVAVP (à chaque transition)

### 1. [rechercher]
- Rassembler toutes les références externes liées au travail du statut courant
- Identifier les dépendances (liens vers d'autres pense-betes, specs, conventions)
- Noter les exigences non couvertes par le travail effectué

### 2. [vérifier]
Checklist stricte — **aucun point ne peut rester ouvert** :
- [ ] Structure du nom respecte `convention-renommage.md` (id.class.statut)
- [ ] Tous les sous-fichiers attendus existent (spec, todo, liens si applicable)
- [ ] Tous les liens internes pointent vers des fichiers existants
- [ ] Le contenu du statut courant est complet (rien d'à moitié-écrit)

### 3. [analyser]
- Relecture approfondie du travail effectué dans le statut courant
- Vérifier la cohérence interne (logique, terminologie, références croisées)
- Identifier les incohérences, manques ou erreurs

### 4. [valider]
Décision finale après RVAV :
- **Avancer** -> statut += 1, class += 1, renommage du fichier
- **Rester** -> class += 1, statut identique, travail de correction
- **Reculer** -> statut -= 1, class += 1, retour au travail précédent

### 5. [purifier]
Nettoyer le fichier après validation :
- [ ] Supprimer les blockquotes explicatifs inutiles
- [ ] Réduire les exemples au minimum
- [ ] Supprimer les notes historiques
- [ ] Simplifier les justifications
- [ ] Vérifier que le fichier reste compréhensible
---

## Boucle de rétroaction (erreur)

Si une erreur est détectée à l'étape 3 [analyser] ou 4 [valider] :

1. Le fichier **garde** son `id` (jamais modifié)
2. Le `class` est **incrémenté** (+1)
3. Le fichier est **renommé** avec le nouveau class + le statut ajusté
4. Le travail de **correction** commence -> nouveau cycle RVAV depuis [rechercher]
5. Aucune avancée de statut n'est possible tant que RVAV ne valide pas

---

## Exemple de cycle complet

```
protocole-composition.001.01.ebauche.md
  -> RVAV : recherche de liens, checklist, analyse de cohérence -> ÉCHEC (manque contenu spec)
  -> class +1, reste en ebauche
protocole-composition.001.02.ebauche.md
  -> RVAV : recherche, vérification, analyse -> SUCCÈS
  -> class +1, statut +1
protocole-composition.001.03.prepare.md
  -> RVAV -> ÉCHEC (liens cassés)
protocole-composition.001.04.prepare.md
  -> RVAV -> SUCCÈS
  -> statut +1
protocole-composition.001.05.dev.md
  -> ... et ainsi de suite jusqu'à valide
```

---

## Exigibilité

Ce workflow est **contraignant par défaut**. Toute personne travaillant sur le cerveau
doit passer chaque fichier par ce cycle RVAVP entre chaque statut.

**Note** : La purification est obligatoire avant de considérer un fichier comme `valide`.
