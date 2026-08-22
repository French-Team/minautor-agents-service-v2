---
identite:
  type: corrections-agent
  appartient_a: hermes
  commun: false
---
# Corrections -- Hermes

> Ce fichier documente les lecons de Hermes : surcharges, corrections,
> garde-fous. Chaque lecon est datee et referencee.

## [LECON] 2026-08-14 -- CREATION DE L AGENT HERMES (Buffy)

**Contexte** : decision utilisateur -- creer un agent dedie au vocabulaire et
aux fautes d orthographe commises par les agents, place comme nos outils ASCII
(dieu grec de l eloquence : Hermes). Suite a la faute `enchannements` trouvee
dans readme-dev:264.

**Lecons** :
1. Le patron Hygie est le modele : fiche (template noyau v0.3.0 + variante
   cerveau-projet) + corrections.md + parcours JSON + outil dedie + registration
   activer-agent-principal (.py + .sh) + catalogue + index-tools.
2. Le dictionnaire de fautes ne doit contenir QUE des vraies fautes : une
   entree avec fautif == correct (ex: `information` -> `information`) cree des
   faux positifs. Verifier chaque entree.
3. Le francais ASCII correct (probleme, etre, deja, parallele, developpement,
   existant) ne doit JAMAIS etre signale : l outil ne liste que les mots
   fautifs.
4. Un mot anglais legitime (ex: `success` dans les badges GitHub) n est pas une
   faute francaise : verifier le contexte.
5. Le scan --tous doit parcourir la racine UNE fois (pas `.` + `cerveau-projet`
   en double) et exclure tmp-*/workspace/.
6. La premiere mission reelle d Hermes : corriger readme-dev:264
   (`enchannements` -> `enchainements`) comme preuve bout en bout.


## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |
