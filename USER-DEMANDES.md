# USER-DEMANDES -- canal direct utilisateur -> jarvis

> Ecris ta demande SOUS la section du declencheur choisi, puis sauvegarde.
> Le serveur de routines detecte le changement et transmet a jarvis.
> Protocole 19. (Traite quand la session incarne jarvis.)

---

## [urgent]

(traite immediatement - la mission en cours est mise de cote en priorite)

## [attention]

(prepare et place juste apres la mission en cours)

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
