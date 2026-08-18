# Controle -- mettre-a-jour-versions v0.1.5 (resync cartes-lock)

**Date** : 2026-08-18
**Controleur** : Janus
**Objet** : modification de `mettre-a-jour-versions` (ajout de
`resynchroniser_cartes_lock` apres bump --parcours --wet), chaine
Vulcain -> Themis -> Morpheus -> Janus.

---

## 1. Contexte de la chaine

- **Vulcain** (Pattern 17, delegue par Buffy) : ajout de la fonction
  `resynchroniser_cartes_lock` (empreinte SHA-256 normalisee LF+rstrip
  STRICTEMENT identique a editer-parcours), appelee apres chaque bump
  `--parcours --wet` reussi. Bump 0.1.4 -> 0.1.5. Lecon dans corrections.md.
- **Themis** (audit-fin-mission) : VERDICT CONFORME, 0 defaut. Rapport :
  `themis/rapports/rapport-audit-mettre-a-jour-versions-resync-2026-08-18.md`.
- **Morpheus** (tests) : pins 0.1.4 -> 0.1.5 adaptes dans test-066/067,
  non-regression OK.

## 2. Verifications independantes

| Verif | Resultat |
|---|---|
| Combo controle-modification | EXECUTE (nommage, liens, separation, sante, tableaux, surcharge, traces) |
| evaluer-processus | 0 probleme (apres retrait de 2 usages hors carte) |
| detecter-residus | 0 residu (cerveau-projet + workspace) |
| Bumper --tous | 0 outil incoherent |
| detecter-divergences-version | 0 divergence (33 spec : 23 alignees, 10 sans version) |
| test-005 (sous janus) | 28/28 OK (le KO morpheus etait l artefact de verrou, reverdi) |
| test-066 | 11/11 OK (pins 0.1.5) |
| test-067 | 8/8 OK (pins 0.1.5, ligne 10 exemple historique preserve) |
| test-007 | 15/15 VALIDE |
| test-057 (marbre/lock) | 24/24 CONFORME |
| ASCII (py, md, tests, corrections) | 0 caractere non-ASCII |
| LF (py, md, tests) | 0 CRLF, EOF newline |
| Registre usages (JSONL) | valide 337/337 |
| Lock themis (cartes-lock.json) | empreinte MATCH avec editer-parcours |
| Versions py/md | 0.1.5 (en-tete + constante + doc + versionning) |
| py_compile | syntaxe valide |

## 3. Auto-corrections appliquees

- Retrait de 2 usages hors carte du registre (regle OUTIL_HORS_CARTE,
  lecon controle branchement-chiron) :
  - vulcain -> guider-parcours (fiche vulcain sans table P0 -> non couvert)
  - morpheus -> tester (carte morpheus a `tester-protections`, pas `tester`)

## 4. Points a signaler

1. **Fiche vulcain sans table P0** : contrairement aux autres fiches
   (morpheus, etc.), la section "Outils de base (P0)" de vulcain.md etait
   en prose sans tableau -> les P0 partages (guider-parcours,
   lire-activite-recente) n etaient pas reconnus par l evaluateur pour
   vulcain (OUTIL_HORS_CARTE a tort). **CORRIGE par Buffy (boucle KO) :
   table P0 ajoutee (modele morpheus.md) -> evaluer-processus 0 probleme,
   test-014 13/13, ASCII 0, LF pur. VERIFIE au re-controle.**
2. Registre-tentatives-bloquees.jsonl : traces du verrou d habilitation
   (valider-cartes-decision bloque pour morpheus) -> historiques, vertes
   sous Janus.
3. Rapport clio (maj-readme-massive) reference 0.1.4 -> document
   historique, sans action.
4. evaluer-coherence : 15 liens `protocole-X/` casses dans corrections.md
   (buffy, janus) + 11 dossiers vides -> PREEXISTANTS, hors perimetre.

## Verdict

**VALIDE** -- la chaine est conforme : modification correcte (preuve
reelle : empreinte lock MATCH), audit Themis CONFORME, tests 0 regression
(test-005 28/28 sous janus, test-066 11/11, test-067 8/8, test-057 24/24),
normes respectees, perimetre propre. Le signalement (fiche vulcain sans
table P0) a ete CORRIGE par Buffy et re-verifie (0 probleme). Aucun point
restant en suspens.
