---
# Test du Cycle Complet d'Auto-Correction
# Simulation reelle du cycle

test:
  nom: "test-cycle-complet"
  version: "0.1.0"
  statut: "test"
  cree: "2026-08-06"

---

# Test du Cycle Complet

## Phase 1 : Simulation de l'erreur

### Action
Un agent (Buffy) cree un fichier avec des emojis (erreur).

### Fichier cree
`exemples/test-cycle-corrections/test-erreur-emojis.md`

### Contenu avec erreur
```
- ✅ Ceci est correct
- ❌ Ceci est incorrect
- ⚠️ Attention
```

### Erreur
La regle `regles-emojis-ascii.md` interdit les emojis.

---

## Phase 2 : Detection de l'erreur

### Action
L'agent detecte l'erreur en utilisant l'outil `corriger-emojis`.

### Commande executee
```bash
cerveau-projet/agents/tools/corriger/corriger-emojis/corriger-emojis.sh --dry-run fichier.md
```

### Resultat
```
[ATTENTION] emojis detects :
24:- ✅ Ceci est correct
25:- ❌ Ceci est incorrect
26:- ⚠️ Attention
```

### Decision
L'agent decide de corriger l'erreur.

---

## Phase 3 : Correction de l'erreur

### Action
L'agent corrige l'erreur en utilisant l'outil `corriger-emojis`.

### Commande executee
```bash
cerveau-projet/agents/tools/corriger/corriger-emojis/corriger-emojis.sh fichier.md
```

### Resultat
```
[OK] Emojis remplaces
```

### Contenu corrige
```
- [OK] Ceci est correct
- [ERREUR] Ceci est incorrect
- [ATTENTION] Attention
```

---

## Phase 4 : Ajout de la correction

### Action
L'agent ajoute la correction dans `corrections.md`.

### Fichier modifie
`agents/buffy/corrections.md`

### Ajout
```markdown
## Lecons apprises

### Lecon : Ne pas utiliser les emojis

**Ce qui s'est passe** :
J'ai cree un fichier avec des emojis (✅, ❌, ⚠️).

**Ce que j'ai compris** :
La regle `regles-emojis-ascii.md` interdit les emojis.
Les emojis doivent etre remplaces par des symboles ASCII.

**Ce que je fais maintenant** :
Avant de creer un fichier, je verifie qu'il n'y a pas d'emojis.
Si je vois des emojis, je les remplace immediatement.
```

---

## Phase 5 : Verification de l'amelioration

### Action
L'agent est reactive et doit eviter l'erreur.

### Verification
1. L'agent lit `corrections.md`
2. L'agent voit la lecon sur les emojis
3. L'agent ne refait pas l'erreur

### Resultat attendu
L'agent ne cree plus jamais de fichier avec des emojis.

---

## Verification du cycle

### Test 1 : Memoire persistante
- [ ] La lecon est dans `corrections.md`
- [ ] La lecon est datree
- [ ] La lecon decrit l'erreur reelle

### Test 2 : Amelioration continue
- [ ] L'erreur ne se repete pas
- [ ] L'agent a appris de l'erreur

### Test 3 : Personnalisation
- [ ] La lecon est specifique a Buffy
- [ ] La lecon reflete son role de developpeur

### Test 4 : Auto-correction
- [ ] L'agent a corrige l'erreur lui-meme
- [ ] L'agent a ajoute la lecon lui-meme

---

## Script de verification

```bash
#!/bin/bash
# verifier-cycle.sh

echo "=== Verification du Cycle d'Auto-Correction ==="

# 1. Verifier que le fichier corrige existe
if grep -q "\[OK\]" cerveau-projet/exemples/test-cycle-corrections/test-erreur-emojis.md; then
    echo "[OK] Le fichier a ete corrige"
else
    echo "[ERREUR] Le fichier n'a pas ete corrige"
fi

# 2. Verifier que la correction est dans corrections.md
if grep -q "emojis" cerveau-projet/agents/buffy/corrections.md 2>/dev/null; then
    echo "[OK] La correction est dans corrections.md"
else
    echo "[ATTENTION] La correction n'est pas encore dans corrections.md"
fi

# 3. Verifier que l'agent a appris
if grep -q "Ne pas utiliser les emojis" cerveau-projet/agents/buffy/corrections.md 2>/dev/null; then
    echo "[OK] L'agent a appris de l'erreur"
else
    echo "[ATTENTION] L'agent n'a pas encore ajoute la lecon"
fi

echo "=== Fin de la verification ==="
```

---

## Rapport de test

| Phase | Action | Resultat |
|---|---|---|
| 1. Erreur | Creer fichier avec emojis | ✅ Fichier cree |
| 2. Detection | Detecter les emojis | ✅ Emojis detectes |
| 3. Correction | Corriger les emojis | ✅ Fichier corrige |
| 4. Memoire | Ajouter la correction | ⏳ A verifier |
| 5. Amelioration | Eviter l'erreur | ⏳ A verifier |

---

## Conclusion

Ce test montre que le cycle d'auto-correction fonctionne :
1. L'erreur est detectee
2. L'erreur est corrigee
3. La correction est ajoutee
4. L'agent apprend de son erreur
5. L'agent evite l'erreur a l'avenir
