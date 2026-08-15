# Controle Janus -- Diagnostic Morpheus + non-regression barriere

Date : 2026-08-15

## 1. Diagnostic : pourquoi Morpheus casse le round
- Carte morpheus SAINE (34 cases, 34 atteignables, CONFORME) - la case c0 n est
  pas le probleme.
- CAUSE RACINE : la mission confiee (Raison dans AGENTS.md) n est PAS relue au
  demarrage du parcours. La case c1 "Quelle est la mission ?" est une case
  ouverte SANS reference a AGENTS.md -> l agent active hesite/s arrete.
- demarrer.md ne couvre que le demarrage de session (-> Cerberus), pas la
  reprise d un agent reactive en milieu de session.
- Protocole-activation etape 5 : dit de "reprendre le controle (SA carte)" mais
  ne dit pas de relire SA Raison.
- Preuve : missions morpheus en double dans l historique (test-013 adapte 2x).
- DECISION UTILISATEUR : corriger SEULEMENT la carte de Morpheus (indice en c0 :
  "je lis la Raison de MA mission dans AGENTS.md avant de repondre a la case
  Mission"). Mission Buffy.

## 2. Incident rattrape : test-032 (4 KO en serie E)
- Oublie dans la liste Morpheus (etait "a verifier", vert avant le verrou).
- Corrige par Janus : version 0.4.1 + --agent janus sur 4 appels (8 remplacements).
- test-032 : 10/10.

## 3. Non-regression complete (mode barrieres)
- Serie E relancee seule : 5/5 OK (la boucle KO -> corriger -> relancer LA serie
  -> suite complete fonctionne).
- Suite complete : 56 OK / 0 KO, 5 barrieres franchies (A -> E).
- Chrono : 98.9s vs 97.6s (+1%, conforme).

## 4. Recommandation Cerberus
- Activer BUFFY : ajouter l indice "relire SA Raison dans AGENTS.md" dans la
  case c0 de parcours-morpheus.json (garde-fou anti-arret) + bump version + fiche.
