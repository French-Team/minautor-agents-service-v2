# USER-DEMANDES -- canal direct utilisateur -> jarvis

> Ecris ta demande SOUS la section du declencheur choisi, puis sauvegarde.
> Le serveur de routines detecte le changement et transmet a jarvis.
> Protocole 19. (Traite quand la session incarne jarvis.)

---

## [urgent]

(traite immediatement - la mission en cours est mise de cote en priorite)

### 2026-08-25 -- URGENT : outil activer-agent-principal cree encore session-llm-N

**Contexte** : l'outil activer-agent-principal.py utilise encore `PREFIXE_SESSION = "session-llm-"` pour creer de nouvelles sessions. Les sessions devraient etre nommees `session-admin` ou `session-freelance` (pas `session-llm-N`).

**Fichier concerne** : cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py

**Lignes concernees** : 108, 341, 343, 404

**Action demandee a Vulcain** : corriger l'outil pour qu'il utilise les bons noms de sessions (`session-admin`, `session-freelance`) au lieu de `session-llm-N`.

## [attention]

(prepare et place juste apres la mission en cours)

### 2026-08-25 -- URGENT : verifier microsecondes dans freelance/

**Contexte** : les microsecondes (6 chiffres) doivent etre remplacees par des millisecondes (3 chiffres). Les fichiers v1 sont corriges. Les fichiers freelance/ doivent etre verifies.

**Fichiers concernes** : cerveau-projet/freelance/tools-commun/routines-server/observations/*.md (5 fichiers)

**Action demandee a Mecano** : verifier et corriger les microsecondes dans les fichiers freelance/ en appliquant le Proto-17 (securite) ou le Proto-5 (outils) selon le type de fichier.

### 2026-08-25 -- NETTOYAGE + COMMIT TERMINE

**Contexte** : session-admin a fait un nettoyage complet. Commit 254 fichiers (57k insertions, 3k suppressions). Agent Mecano v1.0.0 cree (20 protocoles pour corriger freelance/).

**Action demandee a JARVIS** : au prochain demarrage de session-freelance, verifie que les changements sont bien en place. Les agents v2 doivent respecter les 20 protocoles de Mecano si ils doivent etre modifies.

**Verification** : au demarrage, lis ce message et confirme que tu l'as vu.

### 2026-08-24 -- Encarts activites separes par session (v1)

**Contexte** : activer-agent-principal v0.7.2 est en place dans la session v1 (session-admin). Les encarts 'Activites recentes' dans AGENTS-historique.md sont maintenant SEPARES par session :
- `## Activites recentes -- session-admin` (equipe v1 : glm5, Cerberus, Buffy, Vulcain, Morpheus, Janus, Clio, Themis, Chiron, Atlas, Hermes, Hygie...)
- `## Activites recentes -- session-freelance` (equipe v2 : freebuff, Stark, Shuri, Forge, Rogers, Parker, JARVIS, Vision, Fury, EDITH)

**Action demandee a JARVIS** : quand tu vas lire cette demande, verifie que ton fonctionnement interne prend bien en compte cette separation. Les sessions v1 et v2 ecrivent dans LEURS propres encarts. Si tu as un mecanisme de lecture d'activites recentes, assure-toi qu'il lit le bon encart selon ta session (freelance pour toi).

**Verification** : au demarrage de la session freelance avec Stark, ce message devrait apparaitre dans ton inbox. Confirme que tu l'as vu.

### 2026-08-24 -- ERREUR commande jarvis.py : lire-message N EXISTE PAS

**Contexte** : la session freelance a produit cette erreur :
```
jarvis.py: error: argument commande: invalid choice: 'lire-message' (choose from envoyer, recu, lire, acquitter, lister, bloques, activer, historiser, mettre-en-attente, file, reprendre, stop-dev, lancer-missions, defcon, changer-defcon, routines-etat)
```
**Action demandee a JARVIS** : corrige les fiches et/ou corrections de Stark et JARVIS pour que les bonnes commandes soient utilisees. La commande correcte est `lire` (pas `lire-message`). Verifie que toutes les references a jarvis.py dans tes fiches utilisent les noms exacts des sous-commandes.

## [attente]

(parké avec contexte de reprise - ne sera pas perdu)

## [creer]

(dire quoi creer - routage vers les protocoles de creation)

## [probleme]

(decrire le probleme - routage vers l'habilite selon le type de fichier)

## [stop]

(raison de l'arret complet - DEFCON 5)

## [question]

(ta question - jarvis repond avec ses combos)
