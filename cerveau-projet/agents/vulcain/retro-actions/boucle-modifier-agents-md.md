# Boucle de Rétro-action : Modifier AGENTS.md

## Contexte

**QUAND** : Je dois modifier AGENTS.md (activer un agent ou réactiver Cerberus)
**ACTION** : Utiliser `modifier-agents-md`
**PROBLÈME RÉSOLU** : J'utilisais `str_replace` ou `write_file` au lieu de l'outil dédié

---

## La règle
---

## Le processus

### Étape 1 : Vérifier que l'outil existe

```bash
ls cerveau-projet/agents/tools/corriger/modifier-agents-md/modifier-agents-md.sh
```

### Étape 2 : Si l'outil n'existe pas

**ARRÊTER** — l'outil doit être créé avant de continuer.

### Étape 3 : Si l'outil existe

#### Pour activer un agent

```bash
cerveau-projet/agents/tools/corriger/modifier-agents-md/modifier-agents-md.sh activer "Agent" "Raison" "Mission"
```

#### Pour réactiver Cerberus

```bash
cerveau-projet/agents/tools/corriger/modifier-agents-md/modifier-agents-md.sh reactiver "Raison" "AgentPrecedent"
```

---

## Vérification post-exécution

1. Vérifier que AGENTS.md a bien été modifié
2. Vérifier que la section "Agent Principal Actuel" est correcte
3. Vérifier que l'historique a été mis à jour

---

## Erreurs courantes

| Erreur | Correction |
|---|---|
| Utiliser `str_replace` sur AGENTS.md | Utiliser `modifier-agents-md` |
| Utiliser `write_file` sur AGENTS.md | Utiliser `modifier-agents-md` |
| Oublier de vérifier l'existence de l'outil | Toujours vérifier avant |

---

