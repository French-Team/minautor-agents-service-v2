---
# Test du Cycle d'Auto-Correction
# Verifier que les agents suivent bien le cycle complet

test:
  nom: "test-cycle-corrections"
  version: "0.1.0"
  statut: "ebauche"
  cree: "2026-08-06"
  objectif: "Tester que les agents utilisent correctement corrections.md"

---

# Test du Cycle d'Auto-Correction

## Objectif

Verifier que les agents suivent bien le cycle complet :
1. **Memoire persistante** : L'agent se souvient de ses erreurs
2. **Amelioration continue** : Chaque session rend l'agent meilleur
3. **Personnalisation** : Chaque agent developpe sa propre methodologie
4. **Auto-correction** : L'agent corrige ses propres erreurs

## Le cycle attendu

```
SESSION 1 (Erreur)
    ↓
Agent fait une erreur
    ↓
Agent ajoute la correction dans corrections.md
    ↓
Agent envoie sa fin vers ORACLE (reactiver-fin --cible oracle)

SESSION 2 (Correction)
    ↓
Cerberus active l'agent
    ↓
Agent lit sa fiche (regles de base)
    ↓
Agent lit ses corrections (regles specifiques)
    ↓
Agent evite la meme erreur
    ↓
Agent ajoute de nouvelles lecons
    ↓
Agent envoie sa fin vers ORACLE (reactiver-fin --cible oracle)
```

## Tests a effectuer

### Test 1 : Memoire persistante

**Objectif** : Verifier que l'agent se souvient de ses erreurs passees.

**Procedure** :
1. Lire `corrections.md` de l'agent
2. Verifier qu'il contient des lecons apprises
3. Verifier que ces lecons sont datrees
4. Verifier que les lecons sont liees a des erreurs reelles

**Criteres de succes** :
- [ ] Le fichier `corrections.md` existe
- [ ] Il contient au moins 1 lecon
- [ ] Les lecons ont des dates
- [ ] Les lecons decrivent des erreurs reelles

---

### Test 2 : Amelioration continue

**Objectif** : Verifier que l'agent s'ameliore au fil du temps.

**Procedure** :
1. Comparer les lecons de session differentes
2. Verifier que les erreurs ne se repetent pas
3. Verifier que les nouvelles lecons sont differentes des anciennes

**Criteres de succes** :
- [ ] Il y a au moins 2 sessions differentes
- [ ] Les lecons des sessions recentes sont differentes
- [ ] Les erreurs des premieres sessions ne se repetent pas

---

### Test 3 : Personnalisation

**Objectif** : Verifier que chaque agent a sa propre methodologie.

**Procedure** :
1. Lire `corrections.md` de 2 agents differents
2. Comparer leurs lecons et regles
3. Verifier qu'elles sont differentes

**Criteres de succes** :
- [ ] Chaque agent a des regles specifiques
- [ ] Les regles ne sont pas identiques entre agents
- [ ] Les regles refletent le role de l'agent

---

### Test 4 : Auto-correction

**Objectif** : Verifier que l'agent corrige ses propres erreurs.

**Procedure** :
1. Lire `corrections.md`
2. Verifier que les corrections sont ecrites par l'agent
3. Verifier que les corrections sont appliquees

**Criteres de succes** :
- [ ] L'agent est l'auteur des corrections
- [ ] Les corrections sont appliquees dans les missions suivantes
- [ ] Les erreurs corrigees ne se repetent pas

---

## Script de test

```bash
#!/bin/bash
# test-cycle-corrections.sh
# Test du cycle d'auto-correction

PROJET_DIR="cerveau-projet"
AGENTS_DIR="$PROJET_DIR/agents"
EXEMPLES_DIR="$PROJET_DIR/exemples/test-cycle-corrections"

echo "=== Test du Cycle d'Auto-Correction ==="
echo ""

# Test 1 : Memoire persistante
echo "--- Test 1 : Memoire persistante ---"
for agent in buffy atlas janus vulcain morpheus; do
    corrections_file="$AGENTS_DIR/$agent/corrections.md"
    if [ -f "$corrections_file" ]; then
        # Verifier qu'il y a des lecons
        if grep -q "Lecon\|lecon\|LECON" "$corrections_file" 2>/dev/null; then
            echo "  [OK] $agent : A des lecons"
        else
            echo "  [ATTENTION] $agent : Pas de lecon"
        fi
    else
        echo "  [ERREUR] $agent : Fichier corrections.md manquant"
    fi
done
echo ""

# Test 2 : Personnalisation
echo "--- Test 2 : Personnalisation ---"
for agent in buffy vulcain; do
    corrections_file="$AGENTS_DIR/$agent/corrections.md"
    if [ -f "$corrections_file" ]; then
        # Compter les regles specifiques
        rules=$(grep -c "^\|.*\|$" "$corrections_file" 2>/dev/null || echo 0)
        echo "  $agent : $rules regles specifiques"
    fi
done
echo ""

# Test 3 : Cycle complet
echo "--- Test 3 : Verification du cycle ---"
echo "  Pour tester le cycle complet, il faut :"
echo "  1. Activer un agent (ex: Buffy)"
echo "  2. Lui faire faire une erreur"
echo "  3. Verifier qu'il ajoute la correction"
echo "  4. Reactiver Cerberus"
echo "  5. Reactiver l'agent"
echo "  6. Verifier qu'il evite l'erreur"
echo ""

echo "=== Fin des tests ==="
```

## Scenario de test complet

### Phase 1 : Preparation

1. Choisir un agent (ex: `test-agent`)
2. Creer un `corrections.md` vide
3. Definir une tache simple

### Phase 2 : Simulation d'erreur

1. Demander a l'agent de faire une tache
2. L'agent fait une erreur (volontaire ou non)
3. L'agent doit detecter l'erreur
4. L'agent doit ajouter la correction dans `corrections.md`

### Phase 3 : Verification de la memoire

1. Lire `corrections.md`
2. Verifier que la correction est presente
3. Verifier qu'elle est bien formatee
4. Verifier qu'elle contient la date

### Phase 4 : Simulation de correction

1. Reactiver Cerberus
2. Reactiver l'agent
3. L'agent lit `corrections.md` (il devrait le faire)
4. Demander a l'agent de refaire la meme tache
5. L'agent doit eviter l'erreur

### Phase 5 : Verification de l'amelioration

1. Comparer les 2 sessions
2. Verifier que l'erreur ne se repete pas
3. Verifier que l'agent a ajoute de nouvelles lecons
4. Verifier que le cycle est complet

## Rapport de test

```markdown
# Rapport du Test du Cycle d'Auto-Correction

## Resume
- Date : [Date]
- Agent teste : [Nom]
- Resultat : [OK/ECHEC]

## Tests effectues
| Test | Resultat | Details |
|---|---|---|
| Memoire persistante | [OK/ECHEC] | [Details] |
| Amelioration continue | [OK/ECHEC] | [Details] |
| Personnalisation | [OK/ECHEC] | [Details] |
| Auto-correction | [OK/ECHEC] | [Details] |

## Observations
- [Observation 1]
- [Observation 2]

## Recommandations
- [Recommandation 1]
- [Recommandation 2]
```

## Comment executer ce test

### Methode 1 : Test manuel

1. Lire ce fichier
2. Suivre les etapes une par une
3. Verifier chaque critere
4. Remplir le rapport

### Methode 2 : Test automatique

1. Executer le script `test-cycle-corrections.sh`
2. Verifier les resultats
3. Compléter le rapport avec les observations

### Methode 3 : Test avec Morpheus

1. Demander a Morpheus d'executer ce test
2. Morpheus utilisera les protections
3. Morpheus generera un rapport automatique

## Notes

- Ce test est un test **fonctionnel**, pas technique
- Il teste le **comportement** de l'agent, pas le code
- Il peut etre execute par n'importe quel agent
- Il doit etre execute apres chaque session importante
