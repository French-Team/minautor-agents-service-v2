# PROTOCOLE 16 -- Modifier defcon-server.py

> Ce protocole s'applique QUAND Mecano modifie
> cerveau-projet/freelance/tools-commun/defcon/defcon-server.py.
> LIRE CE PROTOCOLE AVANT TOUTE ECRITURE.

---

## IDENTITE DU COMPOSANT

| Champ | Valeur |
|---|---|
| **Chemin** | cerveau-projet/freelance/tools-commun/defcon/defcon-server.py |
| **Proprietaire** | Vision (habilitation exclusive JARVIS) |
| **Type** | Serveur MCP independant |
| **Taille** | ~100 lignes |
| **Encodage** | ASCII + LF (pas UTF-8) |

---

## POURQUOI CE COMPOSANT EST CRITIQUE

defcon-server est un SERVEUR MCP INDEPENDANT de jarvis-server.
Il gere l'echelle d'urgence (DEFCON 2-5).
Si il est casse, la gestion d'urgence est paralysée.

---

## STRUCTURE

```
defcon/
└── defcon-server.py    <- serveur MCP FastMCP
```

Le serveur ecrit dans : cerveau-projet/freelance/jarvis/files/defcon.jsonl

---

## ECHELLE DEFCON

| Niveau | Signification | Action |
|---|---|---|
| 5 | ARRET TOTAL | Tout est stoppe |
| 4 | VALIDATION DES REPARATIONS | Reparations en cours |
| 3 | REPRISE SURVEILLEE | Reprise partielle |
| 2 | REPRISE TOTALE | Normal |

---

## REGLE ABSOLUE

> JE NE MODIFIE JAMAIS defcon-server.py sans avoir VERIFIE
> que jarvis-server.py peut toujours l'interagir.
> La relation defcon <--> jarvis est BIDIRECTIONNELLE.

---

## AVANT de commencer

1. **Lire defcon-server.py EN ENTIER** (~100 lignes)
2. **Lire jarvis-server.py** : comprendre comment il appelle defcon
3. **Verifier les dependances** : fastmcp, json, pathlib
4. **Verifier le DEFCON_FILE** : chemin exact vers defcon.jsonl
5. **Verifier l'echelle** : 5->4->3->2 (pas de montee, pas de saut)

---

## APRES modification

1. **Tester le demarrage** : `python3 defcon-server.py` (pas d'erreur)
2. **Verifier la compatibilite** : jarvis-server peut toujours appeler defcon
3. **Verifier le DEFCON_FILE** : le chemin est toujours correct
4. **Mettre a jour le cahier de dev** : noter ce qui a change

---

## INTERDICTIONS

| Interdiction | Raison |
|---|---|
| Pas de changement de l'echelle | Les agents dependent des niveaux |
| Pas de changement du DEFCON_FILE | Jarvis ne trouve plus les donnees |
| Pas de suppression d'outils MCP | Les agents ne peuvent plus interroger |
| Pas de changement d'encodage | Casserait la compatibilite |
| Pas de modification sans verifier jarvis | Relation bidirectionnelle |
