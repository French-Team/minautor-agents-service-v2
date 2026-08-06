# Mission — Outils de Diagnostic

**Agent** : Vulcain
**Date** : 2026-08-05
**Statut** : Terminé

---

## Objectif

Créer des outils de diagnostic qui vérifient que chaque fichier est utilisé uniquement pour sa fonction prévue.

---

## Règle fondamentale

> **Aucun fichier ne doit être utilisé à autre chose que ce pour laquelle il a été écrit.**

---

## Outils créés

### 1. `verifier-role-fichier`

**Objectif** : Vérifier qu'un fichier est utilisé uniquement pour sa fonction

**Utilisation** :
```bash
verifier-role-fichier.sh [fichier]
```

**Résultat** :
```
[OK] Le fichier est conforme à son rôle
[ERREUR] Le fichier contient du contenu inapproprié
```

---

### 2. `verifier-surcharge-fichier`

**Objectif** : Détecter les fichiers qui grossissent trop

**Utilisation** :
```bash
verifier-surcharge-fichier.sh [dossier] [seuil]
```

**Seuil par défaut** : 250 lignes

**Résultat** :
```
[ATTENTION] Fichiers surchargés :
  - index-cerveau.md : 150 lignes (seuil: 250)
```

---

### 3. `verifier-separation-preoccupations`

**Objectif** : Vérifier que chaque fichier a un rôle unique

**Utilisation** :
```bash
verifier-separation-preoccupations.sh [dossier]
```

**Résultat** :
```
[OK] Séparation des préoccupations respectée
[ERREUR] Chevauchement détecté
```

---

## Critères de validation

- [x] Chaque outil fonctionne sur le système de l'utilisateur
- [x] Chaque outil détecte les problèmes identifiés
- [x] Chaque outil produit une sortie claire
- [x] Chaque outil est documenté
- [x] Chaque outil est testé

---

## Livrables

1. `verifier-role-fichier.sh` — dans `agents/tools/valider/`
2. `verifier-surcharge-fichier.sh` — dans `agents/tools/valider/`
3. `verifier-separation-preoccupations.sh` — dans `agents/tools/valider/`
4. Documentation pour chaque outil
5. Tests pour chaque outil
