# PROTOCOLE 2 -- Modifier JARVIS (agent + serveur + tools)

> Ce protocole s'applique QUAND Mecano modifie jarvis.py,
> jarvis-server.py, ou tout fichier dans freelance/tools-commun/jarvis/.
> LIRE CE PROTOCOLE AVANT TOUTE ECRITURE.

---

## REGLE ABSOLUE

> JARVIS est le centre nevralgique de l'equipe freelance.
> Toute modification de JARVIS a un IMPACT SYSTEMIQUE : chaque agent
> freelance depend de JARVIS pour communiquer. Une erreur dans JARVIS
> peut BLOQUER TOUTE l'equipe.

---

## AVANT de commencer

1. **Lire jarvis.py EN ENTIER** (comprendre toutes les sous-commandes)
2. **Lire jarvis-server.py EN ENTIER** (comprendre le serveur MCP)
3. **Verifier les sous-commandes disponibles** :
   ```
   envoyer, recu, lire, acquitter, lister, bloques, activer,
   historiser, mettre-en-attente, file, reprendre, stop-dev,
   lancer-missions, defcon, changer-defcon, routines-etat
   ```
   NE PAS inventer de sous-commande qui n'existe pas.
4. **Verifier le format des arguments** de chaque sous-commande
5. **Verifier les inboxes/outboxes** dans tools-commun/jarvis/inbox/ et outbox/

---

## ECRIRE la modification

| Element | Regle |
|---|---|
| **Encodage** | UTF-8 + CRLF (comme tout fichier v2) |
| **Backward compatibility** | NE PAS casser les sous-commandes existantes |
| **Nouvelles sous-commandes** | Ajouter dans argparse + documenter dans le .md |
| **Args** | Utiliser les noms exacts (pas d'alias) |
| **Tests** | APRS modification, verifier que les commandes existantes fonctionnent toujours |

---

## STRUCTURE de jarvis.py

```
jarvis.py
|-- parser (argparse)
|   |-- envoyer    -> cmd_envoyer()
|   |-- recu       -> cmd_recu()
|   |-- lire       -> cmd_lire()
|   |-- acquitter  -> cmd_acquitter()
|   |-- lister     -> cmd_lister()
|   |-- bloques    -> cmd_bloques()
|   |-- activer    -> cmd_activer()
|   |-- historiser -> cmd_historiser()
|   |-- mettre-en-attente -> cmd_mettre_en_attente()
|   |-- file       -> cmd_file()
|   |-- reprendre  -> cmd_reprendre()
|   |-- stop-dev   -> cmd_stop_dev()
|   |-- lancer-missions -> cmd_lancer_missions()
|   |-- defcon     -> cmd_defcon()
|   |-- changer-defcon -> cmd_changer_defcon()
|   `-- routines-etat -> cmd_routines_etat()
```

---

## VERIFIER apres modification

1. **Syntaxe** : python3 jarvis.py --help (verifier que toutes les sous-commandes apparaissent)
2. **Sous-commande modifiee** : tester la commande avec des arguments reels
3. **Sous-commandes non modifiees** : verifier qu'elles fonctionnent toujours
4. **Inboxes/outboxes** : verifier que les fichiers JSONL sont toujours lisibles
5. **ASCII/encodage** : le fichier est-il toujours UTF-8 + CRLF ?

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| **Supprimer une sous-commande existante** | Casserait les agents qui l'utilisent |
| **Changer le format des arguments** | Casserait les appels existants |
| **Inventer des noms de commandes** | Utiliser les noms exacts du parser |
| **Modifier les inboxes/outboxes** | Donnees sacrees, jamais purgees sans demande |
| **Changer l'encodage** | UTF-8 + CRLF toujours |
