# Proposition Gardien -- Exception Chiron auto-correction (zone protegee)

- **Date** : 2026-08-18
- **Gardien** : proposition de modification du marbre (c4)
- **Zone concernee** : `regles-groupes-agents`
  (`cerveau-projet/agents/regles-immuables/general/regles-groupes-agents.md`)
- **Validation utilisateur** : OUI (choix "Auto-correction complete" via
  ask_user 2026-08-18)
- **Statut** : PROPOSE -- en attente d'execution de la porte apres
  modification du contenu

## Raison

L'utilisateur demande que **Chiron** soit le premier agent (pilote) capable
d'**auto-corriger SA PROPRE carte** (parcours JSON) quand il detecte des
cases erronees ou obsoletes : protocole d'auto-correction immediate,
re-education de lui-meme, activation de Themis pour verification, reprise de
sa mission interrompue. Cela necessite de donner a Chiron le droit d'utiliser
`editer-parcours` sur SA carte uniquement.

## Modification proposee (contenu de la regle)

Dans la section "SEUL BUFFY CORRIGE LES FICHIERS DES AGENTS (IMMUABLE)" de
regles-groupes-agents.md, ajouter l'exception suivante :

> **EXCEPTION PILOTE (2026-08-18, decision utilisateur)** : Chiron est le
> SEUL agent autorise a CORRIGER SA PROPRE carte (`parcours-chiron.json`)
> via `editer-parcours`, dans le cadre de son parcours d'auto-correction
> (detection de case erronee/obsolete -> correction -> re-education ->
> activation de Themis pour verification -> reprise). Le verrou restreint
> cette habilitation a SA carte uniquement (jamais les cartes des autres
> agents, qui restent exclusives a Buffy). Les autres agents conservent la
> regle : ils signalent, Buffy corrige.

## Impact

- **Perimetre** : 1 fichier (regles-groupes-agents.md) + verrou
  d'habilitation (proteger-verrou-habilitation, cle exclusive chiron ->
  editer-parcours sur SA carte) + test-058 (exception chiron) + carte de
  Chiron (parcours d'auto-correction + indice editer-parcours).
- **Risques** : l'auto-correction doit rester limitee a SA carte (verrou par
  cible). Le Gardien reste le gardien du marbre ; Chiron ne touche JAMAIS
  les zones protegees du marbre.
- **Non-regression** : test-058 a adapter (Morpheus) pour l'exception
  chiron, valider-cartes, bumper, evaluateur.

## Execution prevue

1. Gardien : PROPOSITION (ce rapport) + validation utilisateur acquise.
2. Buffy : modification du contenu de regles-groupes-agents.md (ajout de
   l'exception) -- seule habilitee a corriger les fichiers structurels.
3. Gardien : execution de la porte `proteger-modifier-marbre --zone
   regles-groupes-agents` (re-empreinte + journalisation).
4. Suite de la chaine : Vulcain (verrou), Buffy (carte Chiron), Morpheus
   (test-058), Themis (audit), Janus (controle).
