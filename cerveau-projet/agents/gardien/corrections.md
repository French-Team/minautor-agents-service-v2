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
## [LECON] 2026-08-18 -- PORTE MARBRE : EXCEPTION PILOTE CHIRON (Gardien)

**Mission** : proposer puis executer la modification de la zone protegee
regles-groupes-agents (exception pilote Chiron : auto-correction de SA carte
via editer-parcours, decision utilisateur).

**Actions** :
1. Proposition documentee (rapport proposition-exception-chiron-auto-
   correction-2026-08-18.md : zone + raison + impact) + validation
   utilisateur acquise via ask_user (auto-correction complete).
2. Activation de Buffy pour la modification du CONTENU de
   regles-groupes-agents.md (exception pilote ajoutee, seule habilitee a
   corriger les fichiers structurels).
3. Execution de la porte : proteger-modifier-marbre --zone
   regles-groupes-agents --autorisation UTILISATEUR-2026-08-18 -> audit
   Argus PROPRE, re-empreinte 33429f9f -> 320274ff, journalisee.
4. Verrou : proteger-verrou-marbre --tous = 8/8 conforme.

**Lecons** :
1. Le Gardien PROPOSE et EXECUTE la porte, mais il ne modifie PAS le
   contenu des fichiers de regles (pas habilite editer-fichier-agents) :
   il active Buffy pour le contenu, puis re-empreinte. L'ordre est
   critique : contenu modifie AVANT la porte, sinon l'empreinte ne
   correspond pas a la modification souhaitee.
2. Une zone de REGLES (regles-immuables/) exige l'audit Argus
   (detecter-contradictions --regles) avant gravure : la porte refuse si
   l'audit n'est pas PROPRE. Ici audit PROPRE (0 contradiction).
3. L'exception Chiron est RESTREINTE a SA carte (parcours-chiron.json) :
   le verrou d'habilitation doit porter la cle exclusive par cible (chiron
   -> editer-parcours sur SA carte uniquement), sinon violation de SEUL
   BUFFY. Suite : Vulcain (verrou), Buffy (carte chiron), Morpheus
   (test-058), Themis, Janus.

**Verdict** : marbre mis a jour (8/8 conforme), en attente de la suite de
la chaine (verrou Vulcain + carte chiron + test-058).
