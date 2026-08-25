# CAHIER DE DEV -- Mecano

> Ce cahier est tenu a jour par Mecano entre chaque intervention.
> Il contient l'historique de TOUTES les modifications apportees
> au dossier freelance/ depuis l'arrivee de Mecano.
> CONSULTER CE CAHIER AVANT CHAQUE NOUVELLE INTERVENTION.

---

## Derniere intervention

| Champ | Valeur |
|---|---|
| **Date** | 2026-08-25 |
| **Agent** | Mecano v1.0.0 (test simule par Buffy) |
| **Mission** | Test de coherence conventions.md vs templates/ |

---

## Historique des interventions

### 2026-08-25 -- Test de coherence conventions vs templates

| Element | Detail |
|---|---|
| **Action** | Verification de la coherence entre conventions.md et templates/ |
| **Protocoles utilises** | Proto-12, Proto-14, Proto-15, Proto-10 |
| **Resultat** | 1 ecart detecte (doublon version/cree dans template-agent-v2.md) |
| **Modification freelance/** | AUCUNE (test seulement) |
| **Regressions** | Aucune |
| **Statut** | TERMINE |

**Ecart detecte** : `template-agent-v2.md` contient `version:` et `cree:` en DOUBLE (frontmatter + agent section). Stark suit le meme pattern. Risque d'incoherence futur.

### 2026-08-25 -- Creation de Mecano

| Element | Detail |
|---|---|
| **Action** | Creation de l'agent Mecano (v1 specialise freelance v2) |
| **Fichiers crees** | ferrari.md, corrections.md, parcours-ferrari.json, cahier-dev.md |
| **Protocoles** | proto-1 a proto-20 + index + combos + parcours |
| **Modifications freelance/** | Aucune (creation de l'agent uniquement) |
| **Regressions** | Aucune |
| **Statut** | TERMINE |

---

## Fichiers modifies (resume)

| Fichier | Version | Date | Modification |
|---|---|---|---|
| (aucune modification dans freelance/ pour l'instant) | - | - | - |

---

## Regressions detectees

| Date | Fichier | Description | Resolution |
|---|---|---|---|
| (aucune pour l'instant) | - | - | - |

---

## Ecarts detectes (non-corriges)

| Date | Fichier | Description | Priorite |
|---|---|---|---|
| 2026-08-25 | templates/template-agent-v2.md | Doublon version/cree (frontmatter + agent) | MOYENNE |

---

## Canaux de communication

| Canal | Statut | Derniere verification |
|---|---|---|
| **USER-DEMANDES.md** | Operationnel | 2026-08-25 |
| **jarvis.py** | Operationnel | 2026-08-25 |
| **activer-agent-principal** | Operationnel | 2026-08-25 |

---

## Notes de dev

> Ce cahier est consulte par Mecano AVANT chaque intervention
> pour eviter les regressions et se souvenir du contexte.
> Chaque ligne doit etre completee apres chaque intervention.
