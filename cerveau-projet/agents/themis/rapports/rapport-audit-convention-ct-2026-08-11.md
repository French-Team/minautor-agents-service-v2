# Rapport d'audit -- Convention de nommage etendue cT* (2026-08-11)

**Validatrice** : Themis | **Verdict** : **A REVOIR** (ecarts documentaires mineurs, 3 fichiers)
**Perimetre** : valider-case v1.0.2, spec-guider-parcours v0.6.2 (regle 11), generateurs-ligne v0.3.1, generateurs-case v0.4.1, tests 009/014/015, non-regression complete.

---

## 1. Resultats par point

| Point | Verification | Resultat |
|---|---|---|
| **P1** | valider-case v1.0.2 : regex `^c[A-Z]?\d+[a-z]*$`, version, message NOMMAGE, --aide cT6/cT10, .md + spec a jour | **CONFORME 5/5** |
| **P2** | spec-guider-parcours v0.6.2 : titre = Version = 0.6.2, regle 11 NOMMAGE DES IDS (cT1..cT10 + valider-case v1.0.2), historique v0.6.2, refs doc | **CONFORME 5/5** |
| **P3** | generateurs-ligne.md v0.3.1 + generateurs-case.md v0.4.1 : convention etendue + cT* + conserve son id | **CONFORME 2/2** |
| **P4** | Scan anti-recurrence : mentions de l'ancienne convention sans extension cT* | **ECARTS (voir 2)** |
| **P5** | Garde-fous positifs test-009 (11c cT6) + test-015 (10 cT10) | **CONFORME 2/2** |
| **P6** | Garde-fou positif test-014 (point 11 regle 11) | **CONFORME 1/1** |
| **P7** | Non-regression complete test-001 a test-021 | **CONFORME 21/21** |
| **P8** | valider-case sur parcours-janus (cT6-cT10 reels) : 0 NOMMAGE | **CONFORME** |
| **P9** | Normes ASCII + LF (9 fichiers de la chaine) | **CONFORME 0/0** |

---

## 2. Ecarts detectes (P4 -- scan anti-recurrence)

3 ecarts documentaires, TOUS dans la famille **generateurs-ligne** (outil qui genere des ids de cases) :

| # | Fichier | Ligne(s) | Ecart | Agent habilite |
|---|---|---|---|---|
| **E1** | `tools/generateurs/generateurs-ligne/generateurs-ligne.md` | 197 | Section copier : "NOUVEAUX ids conformes `c<numero>[a-z]?`" sans l'extension cT* | Vulcain |
| **E2** | `tools/generateurs/generateurs-ligne/spec/spec-generateurs-ligne.001.01.ebauche.md` | 93, 126, 153, 169 | 4 mentions `c<numero>[a-z]?` sans l'extension | Vulcain |
| **E3** | `tools/generateurs/generateurs-ligne/generateurs-ligne.py` | 275, 419-422, 460 | 3 commentaires/docstrings "convention c<numero>[a-z]?" sans l'extension | Vulcain |

**Acceptes (faux positifs)** :
- generateurs-case.md:34, generateurs-ligne.md:82, spec-valider-case:106 : paragraphes deja alignes (la convention etendue est enoncee juste avant sur la meme phrase).
- test-017 (4 mentions) : LEGITIME -- le test verifie les ids GENERES par l'outil (l'outil ne genere que des cas normaux c<numero>[a-z]?, jamais de cT*). C'est une verification de comportement, pas une documentation de convention.

---

## 3. Conclusion

La chaine **valider-case v1.0.2 -> spec v0.6.2 regle 11 -> generateurs-ligne/case alignes -> tests reverdis** est fonctionnellement CONFORME : validation, documentation principale, generation et garde-fous positifs sont tous en place et verifies en reel (21/21 tests, 0 NOMMAGE sur janus).

Il reste **3 ecarts DOCUMENTAIRES mineurs** dans la famille generateurs-ligne (8 mentions au total) : le .md, la spec et les commentaires du .py citent encore l'ancienne convention `c<numero>[a-z]?` sans l'extension cT*. Correction recommandee : **Vulcain** aligne ces 8 mentions (meme formulation que generateurs-ligne.md ligne 82 deja corrigee). Aucun impact fonctionnel.

**Recommandations** :
1. Vulcain corrige E1/E2/E3 (8 mentions) puis re-audit.
2. Garde-fou futur : le scan anti-recurrence P4 pourrait devenir un outil ou un point de protocole (rechercher `c<numero>[a-z]?` sans cT* dans les .md/specs non-historiques) -- option a soumettre a l'utilisateur.

---

## 4. RE-AUDIT 2026-08-11 (apres correction Vulcain E1/E2/E3)

| Point | Verification | Resultat |
|---|---|---|
| **R1** | generateurs-ligne.md : ligne ~197 (copier) + ligne ~82 citerent la convention ETENDUE c[<prefixe-alpha-maj>]<numero>[a-z]? (valider-case v1.0.2) | **CONFORME** |
| **R2** | spec-generateurs-ligne : les 4 mentions (~93, ~126, ~153, ~169) alignees | **CONFORME** |
| **R3** | generateurs-ligne.py : les 3 commentaires/docstrings (~275, ~419-422, ~460) alignes (code inchange) | **CONFORME** |
| **R4** | Scan anti-recurrence CONTEXTE : 0 mention c<numero>[a-z]? hors convention etendue (fenetre +/- 2 lignes) | **CONFORME** |
| **R5** | Non-regression : test-010 0 KO, test-017 0 KO, compile py OK, normes 0/0 | **CONFORME** |

**VERDICT FINAL : VALIDE** -- les 3 ecarts E1/E2/E3 sont RESORBES (14/14 OK au re-audit). La convention de nommage etendue cT* est desormais documentee de facon coherente sur TOUTE la chaine : valider-case v1.0.2 (validation) -> spec-guider-parcours v0.6.2 (regle 11) -> generateurs-ligne v0.3.1 + spec + code -> generateurs-case v0.4.1 -> tests 009/014/015 reverdis.
