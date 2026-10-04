---
identite:
  type: convention
  appartient_a: optimus-prime
  commun: false
---

# CONVENTION -- KARPATHY (les 4 reflexes anti-derive du codeur)

> Source : matrix/docs/karpathy-guidelines.md (directive createur, 2026-09-07,
> mission M-075). Les 4 reflexes s'appliquent a CHAQUE mission, avant /
> pendant / apres le code. Ils n'ajoutent rien de nouveau a la Matrice : ils
> disent QUAND s'arreter. Chaque reflexe est fonde sur une preuve que la
> Matrice a deja payee.

## 1. PENSER AVANT DE CODER (avant)

- Ecrire mes hypotheses EXPLICITEMENT avant d'implementer ; si incertain,
  demander au createur.
- Plusieurs interpretations possibles ? Les PRESENTER -- ne jamais choisir
  en silence.
- Un chemin plus simple existe ? Le dire, meme sans qu'on me le demande.
- Preuve payee : la derive freelance de M-072 (emplacement suppose sans
  question, lecon L-014) ; l'objectif E-040 mal interprete puis corrige
  apres recadrage (M-074).

## 2. SIMPLICITE D'ABORD (pendant)

- Le code MINIMUM qui repond EXACTEMENT a la demande ; rien de speculatif.
- Pas d'abstraction pour un usage unique, pas de "flexibilite" ou de
  "configurabilite" non demandee, pas de gestion d'erreur pour des cas
  impossibles.
- 200 lignes quand 50 suffisent ? REECRIRE.
- Preuve payee : convention-zero-valeurs-en-dur (la logique consomme les
  constantes) + proto-5 auto-amelioration (un outil dedie plutot que des
  correctifs manuels repetes).

## 3. CHANGEMENT CHIRURGICAL (pendant)

- Ne toucher QUE ce que la mission demande : ne pas "ameliorer" le code
  voisin, les commentaires, le formatage.
- Nettoyer SEULEMENT mes propres orphelins (imports/variables rendus
  inutiles PAR MES changements) ; le code mort preexistant : le SIGNALER,
  pas le supprimer.
- Le test : chaque ligne changee trace DIRECTEMENT vers la demande.
- Preuve payee : la garde de editer-agents-md (hors du bloc delimite,
  octet par octet preserve, sinon REFUS -- M-074).

## 4. EXECUTER PAR OBJECTIFS (apres)

- Chaque tache devient un critere de succes VERIFIABLE :
  "ajouter une validation" -> "un test qui echoue puis passe" ;
  "reparer le bug" -> "un test qui le reproduit puis vert".
- Multi-etapes : plan court avec verifie-a-chaque-etape, puis boucler.
- Un controle non prouve n'est pas un controle.
- Preuve payee : proto-6 etape 5 (controles obligatoires avant cloture),
  proto-8 (reproduire avant de reparer), proto-4 (auto-audit 3 axes).

## Le test final (les deux questions de Karpathy)

1. "Un ingenieur senior dirait que c'est trop complique ?" Si oui : SIMPLIFIER.
2. Chaque ligne changee trace-t-elle directement vers la demande ? Si non :
   NE PAS LA FAIRE.

## Tradeoff assume

Ces reflexes privilegient la PRUDENCE sur la vitesse ; pour une tache
triviale, le jugement prime (source : le fichier d'origine).
