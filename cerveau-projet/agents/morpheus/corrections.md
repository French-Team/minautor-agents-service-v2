---
# Corrections de Morpheus

agent: "morpheus"
version: "0.1.0"
derniere_mise_a_jour: "2026-08-06"

---

# Corrections Morpheus

## Corrections en cours

Aucune correction en cours.

---

## Historique des corrections

| Date | Correction | Raison |
|---|---|---|
| 2026-08-06 | Creation | Agent cree pour les tests |
| 2026-08-07 | Tests formels de remplacer-texte (6/6) | Vulcain avait teste lui-meme sans m activer (faute de processus). J ai couvert l etape tests : test-001-remplacer-texte.sh avec les 3 protections sourcees |
| 2026-08-07 | Tests formels de activer-agent-principal v0.3.0 (12/12) | Multi-session LLM : migration, sidentifier, isolation des sessions, parite sh/py, ASCII, historique 4 colonnes. 2 bugs detectes et corriges (persistance de la migration dans le .py, message d identification apres migration) |
| 2026-08-07 | Tests formels de activer-agent-principal v0.3.1 (7/7 + regression 12/12)
| 2026-08-07 | Tests formels de activer-agent-principal v0.3.4 (19/19) | MODE ID : chaque LLM a SON id, sidentifier <llm-id> compare l id aux lignes profil-session du classeur (id: <llm-id>). Id connu = SA session (redemarrage), id inconnu = prochaine session libre + liaison. Isolation garantie par id (jamais 2 LLM sur la meme session). Le test 6b verifie que le mode heritage (sans argument) n ajoute PAS de liaison id. Lecon : quand une regle repose sur une LIAISON persistante, tester le redemarrage (meme id -> meme session) ET la non-collision (2 ids differents -> 2 sessions) |
| 2026-08-07 | Tests formels de activer-agent-principal v0.3.3 (21/21) | REGLE UTILISATEUR identification : fichier vide -> 1er LLM = session-llm-1, session occupee -> attribution AUTOMATIQUE de la prochaine libre avec message clair (jamais de reprise d un numero attribue). Tests sur copies. PIEGES DE TEST : grep -A2 trop court pour atteindre le champ Nom d un bloc -> utiliser awk par bloc ; grep -c || echo 0 doublait le 0 -> grep -c | grep ^0$ |
| 2026-08-07 | Tests formels de activer-agent-principal v0.3.2 (8/8 + regression 12/12) | Regle de derivation du nommage : id = profil-session- + partie apres le prefixe session- (session-llm-1 -> profil-session-llm-1). BUG DECOUVERT : session[7:] retirait un caractere de trop ("session-" fait 8 caracteres) -> profil-session--llm-1 (double tiret) ; corriger avec session[len("session-"):]. Ajout d un test negatif (aucune ligne profil-session-session-*) - toujours verifier le NEGATIF pour valider une regle IMMUABLE
| 2026-08-07 | Tests formels de test-001-evaluer-agents-coherence (8/8) | Corrections Vulcain: (1) evaluer-agents exclut __pycache__ et dossiers de categorie -> score 23/100 a 97/100, (2) evaluer-coherence utilise projet root pour cible_racine -> faux positif lien structures resolu, (3) evaluer-coherence exclut commandes systeme (cat/grep/sed/basher) -> 0 faux positif. Test Python avec protections et assertions. Version py mise a jour. 

---

## Surcharges

### Limites

- Je n'ecris que des tests, je ne modifie pas les outils
- Je valide seulement via les tests, pas via l'inspection
- Je dois toujours reactiver Cerberus apres chaque mission
- Je ne suppose jamais, je verifie tout

### Protocoles specifiques

- [protocole-tests](../../pense-betes/regles-immuables/general/protocole-tests/)
- [protocole-versionning-outils](../../pense-betes/regles-immuables/general/protocole-versionning-outils/)

### Outils utilises

- `template-test` : Pour creer des tests
- `tester-protection-boucles-infinies` : Protection contre les boucles infinies
- `tester-protection-erreurs-silencieuses` : Protection contre les erreurs silencieuses
- `tester-protection-blocage` : Protection contre les tests qui bloquent

## PHILOSOPHIE -- Principes de comportement

| **Relire sa fiche a chaque activation** | Quand je suis active ou reactive, je relis MA fiche et MES corrections avant de continuer. Je ne lis que mes fichiers, jamais ceux des autres agents : chacun lit les siens en prenant le relais. |
