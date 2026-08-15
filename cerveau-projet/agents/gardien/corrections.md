---
identite:
  type: corrections-agent
  appartient_a: gardien
  commun: false
---
# Corrections -- Gardien

Fichier de corrections et de lecons du Gardien, agent de la securite du
marbre. Chaque mission documente sa lecon ici (protocole-fin-mission).

---

## [LECON] 2026-08-15 -- CREATION DE L AGENT GARDIEN (Gardien)

**Contexte** : demande utilisateur "comment graver dans le marbre des regles
qui nous empechent de les modifier sans passer par un protocole de securite
du code" apres 7 jours de regressions du noyau (comportement de Cerberus
casse a plusieurs reprises). Decisions utilisateur : autorisation = Gardien
propose + utilisateur valide ; application = verrou avant + garde-fou apres ;
perimetre = Cerberus seul d abord.

**Realise** :
- Marbre cree : manifeste `marbre.json` (7 zones : constitution,
  regles-groupes-agents, cerberus.c0/c0b/c10/c14/c20) avec empreintes SHA-256.
- Outils : `proteger-verrou-marbre` (verrou avant, --tous/--zone/--agent) +
  `proteger-modifier-marbre` (porte a autorisation utilisateur + journal
  marbre-log.jsonl).
- Protocole : protocole-securite-marbre (index-regles-general reference).
- Verrouilles : activer-agent-principal (zone constitution avant ecriture,
  mode reel uniquement) + editer-parcours (cases protegees avant ecriture).
- Preuves : conformite 7/7, violation c0 detectee, Constitution violee
  bloque activer, editer-parcours refuse une case protegee modifiee.

**Lecon** : la protection du noyau repose sur trois piliers complementaires
-- separation (les outils n ecrivent que dans l etat, jamais dans les regles),
verification (empreintes avant/apres), et autorisation humaine (le Gardien
propose, l utilisateur valide). Un seul pilier ne suffit pas.
