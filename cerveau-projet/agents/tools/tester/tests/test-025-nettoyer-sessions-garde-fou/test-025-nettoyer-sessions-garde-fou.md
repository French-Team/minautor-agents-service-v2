# test-025-nettoyer-sessions-garde-fou

**Testeur :** Morpheus
**Date :** 2026-08-12
**Objet :** garde-fou anti-recurrence du bug de l'en-tete `## Sessions LLM`
(lecon 2026-08-12 : apres un nettoyage de session, `sidentifier` echouait
avec 'Section ## Sessions LLM introuvable').

**Contexte :** `nettoyer-sessions` v0.1.1 supprimait l'en-tete de section
`## Sessions LLM` en plus des blocs session et de la table `## Sessions
connues`. Corrige en v0.1.2 : l'en-tete est PRESERVE, seuls les blocs
`### Session : session-llm-N` et la section `## Sessions connues` sont
supprimes. Ce garde-fou verifie la boucle COMPLETE sur copies : nettoyage
-> en-tete conserve -> `activer-agent-principal.py sidentifier` recreer le
bloc (le bug etait invisible sans l'etape de re-identification).

**Execution :**

```bash
python3 test-025-nettoyer-sessions-garde-fou.py
```

**Cas couverts (11 points) :**

1. `nettoyer-sessions --version` py = v0.1.2
2. Parite `--version` py/sh
3. Nettoyage sur copies : blocs `### Session :` supprimes (0)
4. Nettoyage : en-tete `## Sessions LLM` PRESERVE (1) -- coeur du bug
5. Nettoyage : section `## Sessions connues` supprimee (0)
6. Nettoyage : lignes `profil-session-*` supprimees (0)
7. Nettoyage : frontmatter `identite` preserve
8. Integration : `sidentifier` sur la copie nettoyee fonctionne + bloc recree
9. Parite py/sh : fichiers resultants identiques (AGENTS + classeur)
10. ASCII strict : 0 non-ASCII (py/sh/md de l'outil + test)
11. LF pur : 0 CRLF (py/sh/md de l'outil + test)

**Verification :** 0 KO attendu. Toute regression (en-tete supprime,
`sidentifier` casse apres nettoyage, parite cassee) fera KO la non-regression.
