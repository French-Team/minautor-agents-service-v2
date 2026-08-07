# Boucle de Retro-action : Modifier AGENTS.md

## Contexte

**QUAND** : Je dois modifier AGENTS.md (activer un agent ou reactiver Cerberus)
**ACTION** : Utiliser `activer-agent-principal`
**PROBLEME RESOLU** : J'utilisais `str_replace` ou `write_file` au lieu de l'outil dedie

---

## La regle
---

## Le processus

### Etape 1 : Verifier que l'outil existe

```bash
ls python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py
```

### Etape 2 : Si l'outil n'existe pas

**ARRETER** -- l'outil doit etre cree avant de continuer.

### Etape 3 : Si l'outil existe

#### Pour activer un agent

```bash
python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py activer <session> "Agent" "Raison" "Mission"
```

#### Pour reactiver Cerberus

```bash
python3 cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py reactiver <session> "Raison" "AgentPrecedent"
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
| Utiliser `str_replace` sur AGENTS.md | Utiliser `activer-agent-principal` |
| Utiliser `write_file` sur AGENTS.md | Utiliser `activer-agent-principal` |
| Oublier de verifier l'existence de l'outil | Toujours verifier avant |

---

