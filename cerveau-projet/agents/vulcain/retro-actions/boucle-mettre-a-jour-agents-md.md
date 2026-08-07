# Boucle de Retro-action : Modifier AGENTS.md

## Contexte

**QUAND** : Je dois modifier AGENTS.md (activer un agent ou reactiver Cerberus)
**ACTION** : Utiliser `mettre-a-jour-agents-md`
**PROBLEME RESOLU** : J'utilisais `str_replace` ou `write_file` au lieu de l'outil dedie

---

## La regle
---

## Le processus

### Etape 1 : Verifier que l'outil existe

```bash
ls cerveau-projet/agents/tools/mettre-a-jour/mettre-a-jour-agents-md/mettre-a-jour-agents-md.sh
```

### Etape 2 : Si l'outil n'existe pas

**ARRETER** -- l'outil doit etre cree avant de continuer.

### Etape 3 : Si l'outil existe

#### Pour activer un agent

```bash
cerveau-projet/agents/tools/mettre-a-jour/mettre-a-jour-agents-md/mettre-a-jour-agents-md.sh activer "Agent" "Raison" "Mission"
```

#### Pour reactiver Cerberus

```bash
cerveau-projet/agents/tools/mettre-a-jour/mettre-a-jour-agents-md/mettre-a-jour-agents-md.sh reactiver "Raison" "AgentPrecedent"
```

---

## Verification post-execution

1. Verifier que AGENTS.md a bien ete modifie
2. Verifier que la section "Agent Principal Actuel" est correcte
3. Verifier que l'historique a ete mis a jour

---

## Erreurs courantes

| Erreur | Correction |
|---|---|
| Utiliser `str_replace` sur AGENTS.md | Utiliser `mettre-a-jour-agents-md` |
| Utiliser `write_file` sur AGENTS.md | Utiliser `mettre-a-jour-agents-md` |
| Oublier de verifier l'existence de l'outil | Toujours verifier avant |

---

