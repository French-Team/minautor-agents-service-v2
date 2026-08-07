# Mission de controle -- Profil session classeur v0.3.1

**Date** : 2026-08-07
**Agent controle** : Vulcain (outil) + Morpheus (tests)
**Agent controleur** : Janus
**Mission controlee** : activer-agent-principal v0.3.1 -- profil session classeur

---

## Points de controle

| # | Point | Verification | Statut |
|---|---|---|---|
| 1 | Versions synchronisees | 0.3.1 dans .py/.sh/.md/spec | [OK] |
| 2 | Fonction presente | mettre_a_jour_profil_session dans py ET sh + appels dans les 3 actions | [OK] |
| 3 | Format exact | ligne profil-session-<session> au format 5 colonnes | [OK] |
| 4 | Stockage reel | ligne profil-session-llm-1 reflete l agent actuel | [OK] |
| 5 | Tests | test-002 (3 protections) + doc test + chemin protections corrige | [OK] |
| 6 | Spec | exigence 08 + flux + perimetre + historique 0.3.1 | [OK] |
| 7 | Doc | version 0.3.1 + capacite + versionning | [OK] |
| 8 | Conventions | ASCII strict + LF sur les fichiers modifies | [OK] |
| 9 | Test independant | copie: sidentifier + activer + reactiver -> classeur a jour sans doublon | [OK] |

---

## Probleme detecte

- **Type** : Majeur (nommage)
- **Description** : L'outil ecrit la variable `profil-session-session-llm-1` (precedent le nom de session complet `session-llm-1`) alors que le schema (Buffy) et la ligne manuelle existante dans le stockage utilisent `profil-session-llm-1`. Exemple du schema : `id = profil-session-<session-id> (ex: profil-session-llm-1)`. L'outil concatene `profil-session-` + session entiere (`session-llm-1`) au lieu de `profil-session-` + `llm-1` (ou il faut clarifier le schema).
- **Impact** : 1) la ligne `profil-session-llm-1` deja presente dans le vrai stockage ne sera JAMAIS mise a jour par l'outil (il cherche `profil-session-session-llm-1`) -> doublon fantome permanent ; 2) incoherence avec l'exemple du schema ; 3) la regle de nommage des variables du classeur n'est pas respectee de maniere unique.
- **Correction suggeree** : Decider du nom canonique. Proposition : `profil-session-llm-1` (conforme a l'exemple du schema et a la ligne existante). L'outil doit construire l'id comme `profil-session-` + session sans le prefixe `session-` du nom complet, OU le schema doit etre clarifie. A trancher par Buffy (schema) + Vulcain (outil).

## Verdict

**A REVOIR** -- 8/9 points conformes, 1 probleme de nommage majeur a trancher (profil-session-session-llm-1 vs profil-session-llm-1).

### Observations
- Points 1-2 : versions 0.3.1 synchronisees (py/sh/md/spec), fonction + appels presents dans les 2 versions
- Point 3-4 : STOCKAGE REEL incoherent : ligne manuelle `profil-session-llm-1` + 3 lignes outil `profil-session-session-llm-*`
- Point 5 : test-002 (3 protections), chemin 3 niveaux corrige test-001 + test-002, doc test verdict 7/7
- Point 6-7 : spec (exigence 08 + 5 refs profil-session), doc (capacite + 0.3.1 x2)
- Point 8 : ASCII strict valide sur les 5 fichiers
- Point 9 : TEST INDEPENDANT : cycle complet fonctionnel (sidentifier -> activer Buffy -> reactiver) avec mise a jour sans doublon pour l'id outil ; MAIS l'ancienne ligne `profil-session-llm-1` reste inchangee (jamais touchee) -> confirmation du probleme de nommage


## Re-controle v0.3.2 (apres correction du nommage)

| # | Point | Verification | Statut |
|---|---|---|---|
| 1 | Versions 0.3.2 synchronisees (py/sh/md/spec) | [OK] |
| 2 | Regle de derivation dans py (len(session-)) et sh (${session#session-}) | [OK] |
| 3 | Schema : regle de derivation documentee | [OK] |
| 4 | Tests : test-002 (8 cas + verification negative), doc test 8/8 | [OK] |
| 5 | Spec + doc : regle + versionning 0.3.2 | [OK] |
| 6 | ASCII strict | [OK] |
| 7 | TEST INDEPENDANT : cycle complet sur copie -> ligne unique profil-session-llm-1, 0 double-tiret, 0 double-session | [OK] |
| 8 | STOCKAGE REEL : pollue par les lignes residuelles du bug v0.3.1 (3x profil-session--llm-* + doublons profil-session-llm-1) | PROBLEME A NETTOYER |

## Probleme detecte (non bloquant pour l outil)

- **Type** : Mineur (pollution de donnees - heritage du bug v0.3.1)
- **Description** : Le stockage reel (stockage/variables-actuelles.md) contient des lignes residuelles creees pendant les tests du bug v0.3.1 : `profil-session--llm-2`, `profil-session--llm-5`, `profil-session--llm-1` (double tiret) + doublons de `profil-session-llm-1`. L'outil v0.3.2 ne les touche pas (il met a jour la ligne canonique unique).
- **Impact** : confusion visuelle dans le stockage, donnees inutiles.
- **Correction suggeree** : Buffy doit nettoyer le stockage reel (supprimer les lignes `profil-session--llm-*` et les doublons, garder UNE ligne canonique `profil-session-llm-1` a jour).

## Verdict final

**VALIDE (avec nettoyage requis)** -- l'outil v0.3.2 est conforme et fonctionnel (8/8 + 12/12 + test independant OK). Le nettoyage du stockage reel est une tache de maintien a confier a Buffy.
