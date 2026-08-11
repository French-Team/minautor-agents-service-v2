---
# Rapport de controle -- Carte Themis v0.3.7 (piste defaut signale c12f/c12g)

agent:
  nom: "themis"
  type_controle: "second-controle"
  date: "2026-08-11"
  cible:
    - "cerveau-projet/agents/themis/parcours/parcours-themis.json"
    - "cerveau-projet/agents/themis/themis.md"
---

# Rapport de controle -- Second controle de ma propre carte v0.3.7

**Origine** : demande utilisateur -- apres l'ajout par Buffy de la piste
'defaut signale -> activer l'agent habilite pour reparer' (c12f/c12g, modele
Janus c9f/c9g + boucle KO ligne trio cT8-cT10), verification croisee de la
conformite (format, navigation, Pattern 12/14) et de la non-regression.

**Rappel de la modification controlee** (Buffy) :
- c12 (Lecons et retour) : suivant c12b -> c12f
- c12f (question) : 'Un rapport ou une lecon signale un defaut a corriger
  chez un autre agent ?' -- OUI -> c12g / NON -> c12b
- c12g (action) : 'Activer l'agent habilite pour reparer le defaut' --
  REGLE 4 (je signale, je ne corrige pas) + boucle KO (modele cT8-cT10) --
  suivant c12e (fin existante reutilisee, pas de duplication)
- Version : 0.3.6 -> 0.3.7

# Verification

## 1. Conformite format

| Case | Type | Cles | Resultat |
|---|---|---|---|
| c12 | action | titre, type, indices, suivant c12f | OK |
| c12f | question | titre, type, question, branches (OUI->c12g, NON->c12b) | OK |
| c12g | action | titre, type, indices (regle + outil), suivant c12e | OK |
| c12e | fin | titre, type, message (reutilisee) | OK |

- References : 34 refs, toutes resolues (35 cases) -- 0 reference morte.
- Aucun suivant mort.

## 2. Navigation reelle

- FLUX 1 (defaut signale) : c12 -> c12f -> c12g -> c12e : OK
- FLUX 2 (pas de defaut) : c12 -> c12f -> c12b -> c13 : OK
- FLUX 3 (auto-amelioration) : c12f NON -> c12b -> c12c -> c12d -> c12e : OK

## 3. Pattern 12 (CREATION LIMITEE)

- c12g : indices regle + outil (activer-agent-principal) -- AUCUNE
  creation de fichier (l'agent habilite cree son propre rapport) : OK.

## 4. Pattern 14 (fiche / parcours)

- Fiche themis.md cite v0.3.7, plus aucune mention de v0.3.6 : OK.
- Fins reelles de la carte (6) toutes citees dans le bloc FINS REELLES
  v0.3.7 : c12e, c13, c23, c23d, c24, c25b : OK.

## 5. Normes

- parcours-themis.json : 0 non-ASCII, 0 CRLF, JSON valide : OK.
- themis.md : 0 non-ASCII, 0 CRLF : OK.

## 6. Non-regression

- Suite complete (test-001 a test-021) : 21/21 OK.

# Verdict

**VALIDE** -- la piste c12f/c12g est conforme au modele de case, la
navigation est complete (3 flux OK), les Pattern 12 et 14 sont respectes,
les normes sont propres et la non-regression est verte (21/21). Aucun ecart
a signaler. Themis dispose desormais de la meme boucle complete que Janus :
defaut signale -> activation immediate de l'agent habilite.
