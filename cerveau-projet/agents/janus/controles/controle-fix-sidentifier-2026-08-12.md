# Controle croise : fix sidentifier v0.5.1 (bug de demarrage Morpheus)

- **Date** : 2026-08-12
- **Agent** : Janus (controle croise)
- **Session** : session-llm-1
- **Verdict** : VALIDE (J1-J7 tous verts)

## Contexte

L utilisateur a signale que Morpheus s arretait a chaque activation (rounds 8
et 9). Diagnostic : le parcours de Morpheus etait PROPRE (30/30 atteignables,
detecter-cablages-manquants OK, navigation OK). La cause racine etait dans
activer-agent-principal.py sidentifier v0.5.0 : il ECRASAIT le profil classeur
avec `agent: Cerberus` code en dur et affichait `(agent principal : Cerberus)`
meme quand la session retrouvee avait un AUTRE agent actif (morpheus).
Resultat : AGENTS.md et classeur en CONTRADICTION -> l agent qui demarrait
(Morpheus lance sidentifier selon sa fiche) recevait une identite fausse et
s arretait.

## Verifications

| Point | Verification | Resultat |
|---|---|---|
| J1 | Plus aucun `agent principal : Cerberus` en dur dans sidentifier (les occurences restantes sont les cas legitimes : nouvelle session, reactiver, docstring) | OK |
| J2 | `sidentifier llm-1` affiche l agent REEL du bloc (janus au moment du test, apres activation) | OK |
| J3 | Parite py/sh : les deux implementations donnent le meme agent | OK |
| J4 | Versions alignees 0.5.1 (py en-tete, VERSION py, sh, md) | OK |
| J5 | Non-regression complete 26/26 | OK |
| J6 | Catalogue dry-run : 0 a ajouter, 0 cle dupliquee | OK |
| J7 | Normes ASCII strict + LF : 0/0 sur 5 fichiers modifies | OK |

## Correction validee

- Nouvelle fonction `agent_actif_bloc()` (py + sh) : lit l agent REEL du bloc
  (champ Nom Agent) au lieu de Cerberus code en dur.
- Session retrouvee -> affiche + ecrit le profil + l historique avec l agent reel.
- Nouvelle session -> Cerberus par defaut conserve (comportement voulu).
- Bump 0.5.0 -> 0.5.1 (py/sh/md + table Versionning).

## Lecons

1. La source double (AGENTS.md + classeur) doit etre verifiee CROISEE : une
   ecriture en dur dans l une des deux cree une contradiction silencieuse que
   la non-regression ne detecte pas.
2. Le classeur est DERIVE du bloc AGENTS.md, jamais une constante : toute
   valeur codee en dur dans une fonction qui ECRIT le classeur est un bug.
3. Un parcours PROPRE n implique pas un demarrage PROPRE : le cycle
   d identification (sidentifier -> classeur) est une 3e source de verite.
