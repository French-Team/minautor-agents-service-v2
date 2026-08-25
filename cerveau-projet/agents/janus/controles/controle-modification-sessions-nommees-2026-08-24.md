---
identite:
  type: controle
  appartient_a: janus
  commun: false
---

# Controle de modification -- Buffy : sessions nommees admin/freelance + detection IR auto

| Champ | Valeur |
|---|---|
| **Controleur** | Janus |
| **Mission controlee** | Corriger le demarrage des sessions (decision utilisateur 2026-08-24) |
| **Agent controle** | Buffy |
| **Date** | 2026-08-24 |
| **Statut** | EN COURS |

## Mission de controle AVANT

Verifier que la migration des sessions (session-llm-N -> session-admin/session-freelance)
est complete et coherente :

1. **Outil central** : activer-agent-principal v0.7.0 -- sidentifier <id> <session>,
   encarts d activite PAR SESSION, detection AUTO du type IR (prefixe INTER-ROUND /
   FIN D INTER-ROUND).
2. **Demarrage** : parcours-demarrage.json v0.3.0 + demarrer.md -- session explicite
   exigee (admin/freelance).
3. **Etat reel** : AGENTS.md (blocs session-admin/session-freelance + table Sessions
   connues), classeur (profil-session-admin/freelance), AGENTS-historique (encarts par
   session).
4. **Outils alignes** : 11 outils acceptant session-<nom> (verrou, lecons,
   nettoyer-sessions py+sh, editer-parcours, valider-cartes, evaluer-processus,
   generateurs, detecter-ecritures, analyser-tokens, .sh).
5. **Tests** : 056/090/025/024 verts (sans nouveau KO), les autres sans regression.
6. **Audit Themis** : CONFORME 0 defaut (rapport-audit-buffy-sessions-nommees-2026-08-24.md).
7. **Registre + lecons** : buffy complet (6 usages directs + lecon BDD #336 +
   corrections.md), themis present.
8. **Normes** : ASCII strict + LF pur sur les fichiers touches.

## VERDICT : VALIDE -- 0 defaut

Controle de la mission Buffy (sessions nommees admin/freelance + detection IR auto) :
**VALIDE**. Toutes les verifications passent :

1. **Outil central** v0.7.0 : sidentifier <id> <session> -> session-admin/session-freelance
   (test controle isole sur copie : bloc + profil + encart crees), repli heritage conserve,
   detection AUTO du type IR par prefixe INTER-ROUND / FIN D INTER-ROUND (entree
   `| buffy | glm5 | IR |` verifiee sur copie). v0.7.0 coherent py/sh/spec.
2. **Demarrage** : parcours-demarrage.json v0.3.0 (regle SESSION NOMMEE + commande
   sidentifier <id> <session>) + demarrer.md (syntaxe id + session, exemples admin/freelance).
3. **Etat reel** : AGENTS.md (2 blocs session-admin/session-freelance + table Sessions
   connues coherente avec le classeur), classeur (profil-session-admin/freelance),
   AGENTS-historique (encarts par session admin/freelance/autre).
4. **Outils alignes** : 11 outils acceptent session-<nom> (verrou-habilitation,
   enregistrer-lecon, consulter-lecons, nettoyer-sessions py+sh, editer-parcours,
   valider-cartes-decision, evaluer-processus, generateurs-commande, detecter-ecritures-
   hors-cycle, analyser-tokens, activer-agent-principal.sh).
5. **Tests** : test-056 18/18 OK, test-090 11/11 OK, test-025 11/11 OK, test-024 16/17
   (1 KO pre-existant catalogue 186 vs 187), test-018/test-021/test-033/test-043/test-052/
   test-070/test-078 sans NOUVEAU KO (KO restants pre-existants verifies par comparaison
   git stash avant/apres).
6. **Audit Themis** : CONFORME 0 defaut (rapport-audit-buffy-sessions-nommees-2026-08-24.md).
7. **Registre + lecons** : buffy 6 usages directs (18:31) + lecon BDD #336 + corrections.md ;
   themis lecon BDD #338 + corrections.md.
8. **Normes** : ASCII 0/0 + LF pur sur les 23 fichiers touches.
9. **Impacts** : evaluer-processus 8 problemes TOUS pre-existants (7 DECLARATION_FAUTIVE
   deja signales + 1 OUTIL_HORS_CARTE themis valider-cartes-decision deja signale a
   Vulcain) -- aucun nouveau flag ; 6 residus .bak pre-existants (domaine Hygie).
10. **Perimetre** : tous les fichiers modifies relevent de la mission (outils session,
    tests, demarrage, AGENTS, classeur, historique, lecons). Rapport + controle dans
    les dossiers dedies.

Point d attention : le flag `themis valider-cartes-decision` (OUTIL_HORS_CARTE) reste
pre-existant et signale a Vulcain -- hors perimetre de cette mission.
