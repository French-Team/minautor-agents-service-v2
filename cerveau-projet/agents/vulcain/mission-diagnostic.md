# Mission -- Outils de Diagnostic

**Agent** : Vulcain
**Date** : 2026-08-05
**Statut** : Termine

---

## Objectif

Creer des outils de diagnostic qui verifient que chaque fichier est utilise uniquement pour sa fonction prevue.

---

## Regle fondamentale

> **Aucun fichier ne doit etre utilise a autre chose que ce pour laquelle il a ete ecrit.**

---

## Outils crees

### 1. `verifier-role-fichier`

**Objectif** : Verifier qu'un fichier est utilise uniquement pour sa fonction

**Utilisation** :
```bash
verifier-role-fichier.sh [fichier]
```

**Resultat** :
```
[OK] Le fichier est conforme a son role
[ERREUR] Le fichier contient du contenu inapproprie
```

---

### 2. `detecter-surcharge-fichier`

**Objectif** : Detecter les fichiers qui grossissent trop

**Utilisation** :
```bash
detecter-surcharge-fichier.sh [dossier] [seuil]
```

**Seuil par defaut** : 250 lignes

**Resultat** :
```
[ATTENTION] Fichiers surcharges :
  - index-cerveau.md : 150 lignes (seuil: 250)
```

---

### 3. `verifier-separation-preoccupations`

**Objectif** : Verifier que chaque fichier a un role unique

**Utilisation** :
```bash
verifier-separation-preoccupations.sh [dossier]
```

**Resultat** :
```
[OK] Separation des preoccupations respectee
[ERREUR] Chevauchement detecte
```

---

## Criteres de validation

- [x] Chaque outil fonctionne sur le systeme de l'utilisateur
- [x] Chaque outil detecte les problemes identifies
- [x] Chaque outil produit une sortie claire
- [x] Chaque outil est documente
- [x] Chaque outil est teste

---

## Livrables

1. `verifier-role-fichier.sh` -- dans `agents/tools/verifier/`
2. `detecter-surcharge-fichier.sh` -- dans `agents/tools/detecter/`
3. `verifier-separation-preoccupations.sh` -- dans `agents/tools/verifier/`
4. Documentation pour chaque outil
5. Tests pour chaque outil
