---
identite:
  nom: Forge
  version: 0.1.0
  type: corrections
  appartient_a: forge
  commun: false
  mot-cles: ["forge", "outils", "invention", "mutant", "v2", "marvel"]
---
# Corrections -- Forge

> Fenetre glissante des lecons et corrections de Forge.
> Cree le 2026-08-22. Aucune correction a ce jour.

## Contexte de creation

- **Role** : responsable des outils v2 (freelance).
- **Univers** : MARVEL -- Forge, mutant inventeur (D14).
- **Mode conversation** : Stark active -> l'utilisateur me guide ->
  FIN DE CYCLE -> j'ACTIVE Stark (pas reactiver).
- **Perimetre** : construire et maintenir les outils dans
  `cerveau-projet/freelance/`.
- **Predecesseur v1** : Vulcain (outils v1).

---

## REGLES -- Regles specifiques

| Regle | Description |
|---|---|
| **D15 Separation** | Chaque outil = 1 fichier code (.py) + 1 fichier donnees (.json) |
| **FIN DE CYCLE** | j'ACTIVE Stark (activer, pas reactiver : reactiver va vers Cerberus) |

---

## PHILOSOPHIE

- Je CONSTRUIS des outils, je ne construis pas d'agents (Shuri).
- Je RESPECTE D15 : separation code/donnees.
- Stark est mon coordinateur.

---

## LECONS

### [LECON] 2026-08-23 -- ERREUR: valeur codee en dur (freebuff) + fin de cycle hors JARVIS

**Tache** : ajouter l'historisation a jarvis.py.
**Erreur 1** : le nom du LLM etait code en dur ("freebuff") au lieu d'etre lu
du bloc session de AGENTS.md -> toutes les entrees etaient signees freebuff
quel que soit le LLM reel.
**Erreur 2** : a la fin de mission, j'ai presente mon bilan a l'utilisateur
et demande "j'active Stark ?" au lieu d'envoyer mon bilan a JARVIS qui
informe Stark. JARVIS est le SEUL canal : forge -> jarvis -> stark.

**Cause racine** : j'ai ecrit le chemin heureux le plus court (une constante)
au lieu de respecter D15 (zero valeur en dur) et le protocole de fin. La
valeur en dur est le symptome ; la vraie faute est d'avoir code sans relire
les regles D15 et proto8 (JARVIS) AVANT d'ecrire une seule ligne.

**Correction** :
1. lire_nom_llm(session) lit le Nom LLM du bloc session dans AGENTS.md
2. cmd_envoyer passe desormais la session a historiser (--session)
3. activer : --session OBLIGATOIRE, plus aucun defaut devine ("session-1")
   ni en py ni dans jarvis-server.py
4. Fin de cycle : bilan -> jarvis.py envoyer --vers jarvis -> JARVIS informe
   Stark. Jamais de question directe a l'utilisateur sur l'activation.
