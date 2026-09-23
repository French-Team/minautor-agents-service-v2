---
identite:
  type: mots-cles
  appartient_a: optimus-prime
  commun: false
---

# Mots-Cles de Demande

## Mots-Cles Standard

| Mot-cle | Usage | Exemple |
|---|---|---|
| [question] | Question ouverte | [question] Comment faire X ? |
| [preparation] | Demande de preparation | [preparation] Explique-moi Y |
| [revision] | Demande de revision | [revision] Verifie Z |
| [mission] | Demande de mission | [mission] Creer W |

## Crochets officiels (la liste FERMEE -- source : conventions/convention-crochets.md)

> Tous reconnus par le routeur (`pilote/filtrer/entry.py`). Le controle
> `crochets` du contrat fondamental tient DEUX miroirs : code <-> convention
> (egalite stricte) et liste fermee <-> CETTE PAGE -- un crochet officiel absent
> d'ici est ACCUSE (MO-303, demande createur : six officiels y manquaient).

| Mot | Porte | Effet (resume) |
|---|---|---|
| [mission] | entonnoir `deposer` | verse une mission au vrac (--theme EXIGE) |
| [question] | pilote `lot` | le theme en 4 parts de LOT |
| [audit] | entonnoir `deposer` (type audit) | lance un audit (constat, lecture seule) |
| [revision] | entonnoir `deposer` (type revision) | relit en entier et propose les changements |
| [outil] | entonnoir `deposer` (type reparation) | un OUTIL fautif trouve en travaillant |
| [corriger] | entonnoir `deposer` (type reparation) | demande une CORRECTION explicite |
| [si] | AUCUNE porte : la mission EN COURS (`mission-en-cours`, verbe `remise-en-question`) | INTERVENTION sur la mission qui tourne : le createur a vu une incoherence, le mot declenche une MINI-REFLEXION -- ce qu'il vient de decouvrir contredit-il ce que je viens de faire dans CETTE mission ? Reprendre l'hypothese, la MESURER, puis optimiser les corrections EN COURS. Rien n'est depose (aucune file, aucune mission) : l'intervention vit et meurt avec la mission, et elle est TRACEE au journal de la mission courante (action `intervention`). Ajoute le 2026-09-21, demande createur. |
| [alerte] | outil machine-defcon | defcon 5 (ou la variante [alerte=defcon:N]) |
| [pause] | outil pause-session, verbe pause | maintenance manuelle de l'operateur |
| [bilan] | outil bilan-periode | bilan d'une periode fermee |
| [preparation] | theme PREPARATION | discussion et preparation hors code |
| [purification] | theme PURIFICATION | la chaine de purification (case [decision] obligatoire) |
| [super-combos] | brique lancer-super-combos --lister | le mot NU liste les super-combos |
| [???] | theme CADRAGE | le parcours qui CONSTITUE la chaine de missions avant de resoudre (le seul crochet hors mot francais : il dit que la demande n'est pas encore formulee) |
| [preparer] | theme CADRAGE | ALIAS officiel de [???] : deux mots, une seule route |

## Mots-Cles de Detection

| Mot-cle | Usage | Exemple |
|---|---|---|
| [bug] | Bug detecte | [bug] Le script ne fonctionne pas |
| [probleme] | Probleme dans les flux | [probleme] Le pilote ne demarre pas |
| [incoherence] | Incoherence percue | [incoherence] Les fichiers sont contradictoires |

## Mots-Cles d'Action

| Mot-cle | Usage | Exemple |
|---|---|---|
| [super-combos: #N] | Lancer un super-combos par numero | [super-combos: #1] Executer sur les dernieres missions |
| [tache] | Tache specifique | [tache] Modifier le fichier X |
| [correction] | Correction necessaire | [correction] Corriger l'erreur Y |
| [test-reel] | Lancer un processus de validation reel | [test-reel] Valider les changements |

## Super-Combos Disponibles

| Numero | Nom | Description |
|---|---|---|
| #1 | AUTO-XXX | Enchainement intelligent des themes AUTO-XXX |

## Commandes Utiles

| Commande | Description |
|---|---|
| `python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/lancer-super-combos.py --lister` | Lister les super-combos |
| `python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/lancer-super-combos.py --numero #N` | Lancer un super-combos |
| `python3 <test-reel.py> --fichier <fichier>` | Tester un fichier |
| `python3 <test-reel.py> --tout` | Tester tous les fichiers |

## Regles

1. **Toujours utiliser les mots-cles** quand ils s'appliquent
2. **Un seul mot-cle par demande** (sauf super-combos avec parametres)
3. **Les mots-cles de detection** ont la priorite sur les autres
4. **Les super-combos** utilisent le format `#N` pour le numero
5. **Pour lancer un super-combos** : `python3 cerveau-projet/matrix/_operateur/optimus-prime/super-combos/lancer-super-combos.py --numero <#N>`
   (chemins relatifs a `_operateur/optimus-prime/` ; le lanceur vit avec SES objets,
   dans `super-combos/`, depuis le rangement corrige par MO-067 (2026-09-13))
6. **Pour un test reel** : executer le processus de validation complete
