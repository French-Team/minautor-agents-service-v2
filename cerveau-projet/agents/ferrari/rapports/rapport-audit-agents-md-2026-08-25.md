---
identite:
  type: rapport
  appartient_a: ferrari
  commun: false
---
# Rapport d'audit -- Incoherences AGENTS.md (fichier racine commun)

- **Date** : 2026-08-25
- **Agent** : ferrari (Mecano), couche superieure session-admin
- **Origine** : mission relayee par stark (diagnostic utilisateur "Mauvais tableau
  AGENTS.md = source des bugs", jarvis inbox jarvis.jsonl).
- **Nature** : AUDIT PUR -- AUCUNE modification effectuee (AGENTS.md ne doit
  etre modifie qu apres validation utilisateur ; AGENTS.md est hors de mon
  perimetre d ecriture).

## Perimetre audite

- Blocs session d AGENTS.md : session-admin (l.17-35) + session-freelance (l.37-53).
- Table "Sessions connues" (l.55-58).
- Fichiers reels de reference : arbre-stark.json, themes stark/parcours/,
  jarvis-data.json, activations.py (maj_bloc_session), fiches/corrections v2.

## Constats (decalages tableau vs realite)

| # | Ligne AGENTS.md | Tableau / contenu | Realite (disque/code) | Correction proposee |
|---|---|---|---|---|
| 1 | l.53 (bloc session-freelance, bloc DEMARRAGE V2) | "(themes : JARVIS -- point d'entree OBLIGATOIRE pour toute mission / LIRE / EXPLORER)" -- 3 themes | arbre-stark.json `racine.suivant` = "theme-jarvis.json" UNIQUEMENT ; regle D1 "JARVIS est mon UNIQUE branche" ; D6 "Je ne lis JAMAIS, je ne diagnostique JAMAIS" | Rafraichir le bloc avec le texte actuel de l outil ("themes : selon ton arbre ; JARVIS = point d'entree OBLIGATOIRE pour toute mission") |
| 2 | l.48 (bloc session-freelance, Raison) | "Active par stark: [BILAN VISION - activation 22a8d033] Diagnostic termine. Conclusion : JARVIS FON" (coupee en plein mot) | activations.py l.101-103 : `mission[:80]` dans historiser + maj_bloc_session -- la mission complete est perdue | Ne plus tronquer la raison (ou stocker la mission complete) -- correctif JARVIS (domaine Vision / couche superieure) |
| 3 | jarvis-data.json l.37 | agent "jarvis" : "corrections": "" (vide) | cerveau-projet/freelance/jarvis/corrections.md EXISTE sur disque ; tous les autres agents ont un chemin valide | "corrections": "cerveau-projet/freelance/jarvis/corrections.md" |
| 4 | (disque) | theme-lire.json + theme-explorer.json presents | NON references par arbre-stark.json (qui ne reference que theme-jarvis.json) | Supprimer (Hygie/ferrari) ou archiver -- a decider |
| 5 | l.55-58 (Sessions connues) | session-freelance | "Derniere activite 2026-08-24 19:52:52.328" MAIS bloc session-freelance "Derniere mise a jour 2026-08-25" -- deux ecrivains desynchronises (activer-agent-principal met a jour la table ; jarvis maj_bloc_session met a jour le bloc, PAS la table) | jarvis maj_bloc_session devrait aussi mettre a jour la table Sessions connues (ou mecanisme de sync) |
| 6 | l.20-21 (bloc session-admin, Role Agent) | "...CONFIDENTIEL (seul Cerberus le connait, absent volontairement d AGENTS.md)" | Paradoxe : le texte dit "absent d AGENTS.md" alors qu il EST dans AGENTS.md ; fuite de confidentialite (bloc lisible par les agents v2) | Nettoyer le role dans le dictionnaire d activer-agent-principal (texte neutre, sans mention CONFIDENTIEL/absent) |

## Cause racine commune

Les blocs session d AGENTS.md ont DEUX ecrivains qui ne se synchronisent pas :
1. `activer-agent-principal` (v1, via Cerberus) : ecrit le bloc COMPLET
   (incluant le bloc DEMARRAGE V2) et la table Sessions connues.
2. `jarvis.py` `maj_bloc_session` (v2, activations.py) : ne reecrit QUE les
   lignes de tableau du bloc (Nom Agent, Role, Date, Raison, Fiche, Corrections)
   -- jamais le bloc DEMARRAGE V2, jamais la table Sessions connues.

Le bloc DEMARRAGE V2 de session-freelance date donc d une epoque ou stark avait
3 themes (JARVIS/LIRE/EXPLORER) ; il n a jamais ete rafraichi depuis la
simplification de l arbre a 1 theme.

## Qui est habilite a modifier AGENTS.md ? (reponse a la question de perimetre)

- AGENTS.md est un fichier COMMUN (racine, ni agents/ ni freelance/).
- **Contenu des tables et du texte** : Buffy (responsable du cerveau-projet,
  developpeur principal) est l habile naturel ; le Gardien intervient pour les
  zones marbre (zone Constitution, geree par activer-agent-principal).
- **Blocs session** : mis a jour par activer-agent-principal (v1, via Cerberus)
  et par jarvis maj_bloc_session (v2).
- **Correctifs cote v2** (activations.py, jarvis-data.json, maj_bloc_session) :
  fichiers dans freelance/ -- Vision (exclusivite JARVIS) ou ferrari (couche
  superieure, n importe quel fichier freelance/) -- a trancher par l utilisateur.

## Mecanisme de validation automatique au demarrage (proposition)

Objectif : le LLM qui demarre detecte lui-meme les incoherences de son bloc.

1. **Cote v1 (outil dedie, domaine Vulcain + test Morpheus)** : creer
   `verifier-coherence-agents` qui verifie, pour CHAQUE bloc session d AGENTS.md :
   - fiche + corrections du bloc existent sur disque ;
   - le texte "(themes : ...)" du bloc DEMARRAGE V2 est coherent avec
     l arbre-<agent>.json (themes effectivement references) ;
   - la raison n est pas tronquee (pas de coupure suspecte en fin de chaine) ;
   - jarvis-data.json : fiche + corrections non vides et existantes ;
   - la table Sessions connues est coherente avec les blocs (dates).
   Brancher ce verificateur au demarrage (demarrer.md / case c0c de Cerberus)
   et a la non-regression (test dedie).

2. **Cote v2 (domaine Vision / jarvis)** : etendre `maj_bloc_session` pour :
   - rafraichir le bloc DEMARRAGE V2 (au moins la ligne themes) depuis l arbre ;
   - ne plus tronquer la raison (ou garder la mission complete dans l historique) ;
   - mettre a jour la table Sessions connues ;
   - ajouter une sous-commande `jarvis.py verifier-coherence` appelee au
     demarrage de session (le LLM v2 voit les avertissements).

3. **Anti-recurrence** : un garde-fou (test de non-regression) verifiant que
   le bloc DEMARRAGE V2 ne liste jamais plus de themes que l arbre n en
   reference, et qu aucune raison n est tronquee.

## SUITE : corrections APPLIQUEES (autorisation utilisateur 2026-08-25)

L utilisateur a autorise exceptionnellement la correction d AGENTS.md et
les corrections associees. Applique :

| # | Correction appliquee | Fichier |
|---|---|---|
| 1 | Bloc DEMARRAGE V2 : "themes : selon ton arbre ; JARVIS = point d'entree OBLIGATOIRE pour toute mission" | AGENTS.md |
| 2 | Raison debloquee : texte complet note + troncature SUPPRIMEE a la source (activations.py `mission[:80]` -> `mission`) | AGENTS.md + activations.py |
| 3 | jarvis corrections -> cerveau-projet/freelance/jarvis/corrections.md (existe sur disque) | jarvis-data.json |
| 4 | theme-lire.json + theme-explorer.json SUPPRIMES (orphelins, suivis git donc recuperables) | freelance/stark/parcours/ |
| 5 | Sessions connues session-freelance -> 2026-08-25 17:11:53 (derniere activite reelle) | AGENTS.md |
| 6 | Role session-admin nettoye (texte neutre, sans mention CONFIDENTIEL/absent) + dictionnaire activer-agent-principal (py + sh) aligne | AGENTS.md + activer-agent-principal |

**Validations** : test-092 9/9 OK (parite py/sh/AGENTS.md), test-101 11/11 OK
(arbres, themes orphelins sans impact), syntaxe py + bash OK, JSON valide,
CRLF v2 preserve (jarvis-data.json), ASCII 0/0 (fichiers v1), LF pur.

## MECANISME IMPLEMENTE (validation automatique au demarrage, 2026-08-25)

Demande utilisateur : implementer le mecanisme propose. Autorisation :
"Moi seul (autorisation)" (ferrari fait tout, couche superieure).

### Cote v1

| Element | Detail |
|---|---|
| Outil | `agents/tools/verifier/verifier-coherence-agents/` (py + sh + md) v0.1.0 : verifie pour chaque bloc session d AGENTS.md : fiches/corrections existantes, ligne themes du bloc DEMARRAGE V2 vs arbre-<agent>.json, raisons non tronquees, jarvis-data.json (fiche + corrections non vides), table Sessions connues. rc=0 coherent / rc>=1 incoherences. |
| Test | `test-103-coherence-agents-agents-md` : 17 OK / 0 KO (rc=0 sur reel, preuves negatives themes orphelins + raison tronquee, jarvis-data, normes ASCII/LF/doc). Enregistre en serie e + profils (outils + tests). |
| Branchement | Case c0c du parcours-demarrage.json (CONTEXTE OBLIGATOIRE) : ajout de l index outil `verifier-coherence-agents --dry-run` -- chaque LLM qui demarre voit l etat de coherence d AGENTS.md. |
| Index | `index-tools.md` : entree `verifier-coherence-agents` ajoutee. |

### Cote v2 (JARVIS, domaine Vision / couche superieure)

| Element | Detail |
|---|---|
| `maj_bloc_session` (activations.py) | v0.10.0 : **PAS de modification** du flux (hors troncature deja corrigee v0.6.2). Une tentative d extension (maj du profil-session du CLASSEUR v1 depuis JARVIS) a ete RETIREE : ecrire dans le classeur v1 depuis la v2 est une VIOLATION de frontiere (decision utilisateur 2026-08-25, "interdit"). Le decalage n 5 (Sessions connues desynchronisees) est a traiter cote v1 uniquement (activer-agent-principal reste la SEULE source d ecriture du classeur v1). |
| `jarvis.py verifier-coherence` | Nouvelle sous-commande (fonctions/verifier.py) qui invoque l outil v1 `verifier-coherence-agents --dry-run` : le LLM v2 detecte lui-meme les incoherences via l interface jarvis. rc=0 coherent. |
| Raison complete | Deja corrigee dans la phase corrections (mission[:80] -> mission) ; confirmee v0.6.2. |

### Validations

- test-103 : 17 OK / 0 KO ; test-092 : 9/9 ; test-101 : 11/11.
- test-005 : 5 KO PREEXISTANTS (parcours-atlas.json version 0.5.4 vs 0.5.7,
  navigation atlas) -- non lies a cette mission (aucun changement atlas).
- Normes : ASCII 0/0 + LF pur sur tous les fichiers crees/modifies (v1 et v2).

### Dette residuelle (hors perimetre)

- jarvis.md frontmatter (version: 0.5.0) et tableau (Version 0.1.0) en retard
  sur le code (v0.10.0) -- dette de versionnage preexistante, a arbitrer
  (Vision documente).
- parite atlas (test-005) : parcours-atlas.json a bumper 0.5.4 -> 0.5.7.

## Aucun fichier modifie (avant validation)

La version initiale de cet audit n a modifie AUCUN fichier -- conformement a
la consigne initiale (validation utilisateur avant toute correction).
Les corrections ci-dessus ont ete appliquees APRES l autorisation utilisateur.
