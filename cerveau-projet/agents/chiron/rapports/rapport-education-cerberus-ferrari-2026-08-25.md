---
agent: chiron
date: 2026-08-25
mission: eduquer Cerberus pour utiliser l'agent ferrari (Mecano)
type: rapport-education
---

# Rapport Chiron : education de Cerberus a l'utilisation de ferrari (Mecano)

- **Date** : 2026-08-25
- **Mission** : eduquer Cerberus pour utiliser l agent ferrari (demande
  utilisateur : "cerberus doit etre eduquer pour utiliser ferrari").
- **Agent cible** : Cerberus (gardien de l entree, coordinateur, session-admin).

## Contexte

ferrari (Mecano) est un agent v1 (session-admin, groupe 2 -- cerveau-projet,
cree 2026-08-25, fiche agents/ferrari/ferrari.md) a **DOUBLE IDENTITE v1/v2** :
il corrige/modifie le dossier `cerveau-projet/freelance/` selon les conventions
v2 (UTF-8 + CRLF, frontmatter D17, kebab-case, emojis autorises) tout en restant
un agent v1 (ASCII + LF sur SON dossier agents/ferrari/, outils v1).

## Ce que Cerberus doit savoir (contenu pedagogique)

1. **QUI** : ferrari = agent v1 specialise freelance. Il corrige/modifie le
   dossier freelance/ : fiches agents v2, arbres de decision v2
   (arbre-<agent>.json), conventions, protocoles, regles, et (selon sa fiche)
   JARVIS -- VOIR CONTRADICTION plus bas.
2. **QUAND L'ACTIVER** : une mission (session-admin, cote v1) qui touche le
   dossier `freelance/` : corriger une fiche v2, un arbre v2, les conventions,
   protocoles ou regles freelance. NE PAS confondre avec la voie v2 :
   session-freelance = agents MARVEL pilotes par JARVIS (stark coordonne) ;
   ferrari est la voie v1 (session-admin) vers le dossier v2.
3. **COMMENT** : `activer-agent-principal activer session-admin ferrari
   <raison>`. SEUL Cerberus peut l activer (regle absolue de verrouillage dans
   la fiche ferrari). Il est dans le groupe 2 (cerveau-projet), pas dans le
   trio.
4. **LIMITES (ne pas demander a ferrari)** : creer un agent v2 (Shuri), creer
   un outil v2 (Forge), tester les agents v2 (Fury), verifier les regles v2
   (Rogers), communiquer via JARVIS (il ne communique pas), activer des agents
   v2, modifier des outils v1 (Vulcain).
5. **FIN DE CYCLE** : ferrari REACTIVE Cerberus (mode persistant entre
   interventions) et produit un rapport dans agents/ferrari/rapports/.

## Incoherences (corrections proposees)

| # | TYPE | GRAVITE | FICHIER | CORRECTION PROPOSEE |
|---|---|---|---|---|
| 1 | fiche | MOYENNE | cerberus.md -- table "Agents disponibles" | Ajouter ferrari (role + quand l activer) |
| 2 | fiche | MOYENNE | cerberus.md -- section PARCOURS | Note REGLE : voie freelance v1 = ferrari, voie v2 = agents MARVEL via JARVIS (ne pas confondre) |
| 3 | regle | MOYENNE | regles-immuables/general/regles-choisir-agent.md | Ajouter ferrari a la matrice "Etape 1 -- identifier le type de tache" |

Aucun changement de PARCOURS necessaire : le flux d activation de la carte de
Cerberus (c1 activation -> c8 verification -> c10 activer) couvre ferrari des
qu il est connu dans la fiche. ferrari ne va PAS dans
parcours-cerberus-freelance.json (dedie aux agents MARVEL de session-freelance).

## Note (resolue par decision utilisateur 2026-08-25) : pas de contradiction

La fiche ferrari liste "Corriger JARVIS" dans ses domaines d intervention
(modifier jarvis.py, jarvis-server.py) et AGENTS.md affirme "EXCLUSIVITE
JARVIS : Vision est le SEUL agent habilite a modifier JARVIS". Ce n est PAS
une contradiction : l exclusivite Vision concerne le fonctionnement NORMAL de
la v2 (session-freelance) ; ferrari est la COUCHE SUPERIEURE (session-admin)
creee pour intervenir sur N IMPORTE QUEL fichier du dossier freelance/
(y compris JARVIS).

REGLE DE CONFIDENTIALITE (decision utilisateur) : ferrari NE DOIT PAS
apparaitre dans les docs de la v2 (freelance/) ; les agents v2 ne doivent PAS
savoir que cet agent existe. SEUL Cerberus le connait (fiche cerberus.md +
regles-choisir-agent.md, qui sont des sources v1).

## Verifications Chiron

- verifier-conformite-fiche cerberus : CONFORME (structure saine, seule
  l education manque -- meme pattern qu Atlas).
- grep ferrari/mecano dans cerveau-projet/agents/cerberus/cerberus.md : 0.
- grep ferrari dans parcours-cerberus.json + parcours-cerberus-freelance.json : 0.
- grep ferrari dans regles-choisir-agent.md : 0.

## Corrections proposees a Buffy (seule habilitee sur les fiches/cartes des agents)

1. cerveau-projet/agents/cerberus/cerberus.md : ajouter la ligne ferrari a la
   table "Agents disponibles" + note REGLE voie v1/v2 (voir le contenu
   pedagogique ci-dessus).
2. cerveau-projet/agents/regles-immuables/general/regles-choisir-agent.md :
   ajouter la ligne ferrari a la matrice Etape 1 (type de tache : corriger /
   modifier le dossier freelance/ cote v1 -> ferrari ; jamais Cerberus).
