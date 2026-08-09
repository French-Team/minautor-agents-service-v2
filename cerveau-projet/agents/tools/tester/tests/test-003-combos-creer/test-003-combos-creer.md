---
identite:
  type: test
  appartient_a: morpheus
  commun: false
---
# Test 003 -- Combos creer-* v0.2.0

**Outil teste** : `combos-moteur` (execution des definitions combo-creer-*)
**Agent** : Morpheus
**Version** : 0.1.0
**Statut** : valide (86/86 REUSSI)

---

## Objectif

Tester formellement les 3 combos `creer-*` v0.2.0 convertis en cases
`generateur` (Pattern 3 : chaque commande en dur devient une paire
case generateur catalogue+entrees+sortie + case outil commande `{cmdN}`).

Combos couverts (`cerveau-projet/agents/tools/combos/`) :

| Combo | Version | Cases | Controle | Branche NON |
|---|---|---|---|---|
| `combo-creer-fichier-cerveau` | 0.2.0 | 10 | c7 | -> c10 (fin) |
| `combo-creer-agent` | 0.2.0 | 10 | c3 | -> c10 (fin) |
| `combo-creer-protocole` | 0.2.0 | 8 | c3 | -> c8 (fin) |

---

## Cas couverts (pour CHAQUE combo)

1. **Structure JSON** : version 0.2.0, case_depart c1, nom correct,
   4 types de cases presents (generateur/outil/controle/fin), autant de
   cases generateur que de cases outil, au moins 2 generateurs.
2. **`--liste`** : code 0, case de depart listee, controle listee,
   4 types affiches.
3. **Variable manquante** : sans `--var`, erreur claire
   `Variable non trouvee`, code 1 (protection : le combo ne peut pas
   etre lance sans ses variables).
4. **Navigation chemin OUI** (controle `=OUI`) : code 0, `COMBO TERMINE`,
   commandes generees correctes (valider-nommage `--type outil`,
   valider-conventions, rechercher-fichier, copier-dossier,
   copier-fichier, creer-fichier selon le combo).
5. **Navigation chemin NON** (controle `=NON`) : code 0, `COMBO TERMINE`
   (la branche NON est non bloquante, elle atteint la case fin) et
   AUCUNE commande `creer-fichier` generee (le NON court-circuite la creation).
6. **Parite .py / .sh** : memes sorties `--liste` et meme navigation
   (chemin OUI) entre `combos-moteur.py` et `combos-moteur.sh`.
7. **Dry-run sans effet** : navigation en `--dry-run`, aucun fichier cree
   (protection anti-effets : cible verifiee absente).
8. **Nommage** : comportement attendu documente (2 faux positifs connus) :
   - definitions `combo-*` vs convention `combos-*` (identique a tous les combos existants) ;
   - fichier de test dans `tests/` exige un prefixe `tests-` absent des
     tests formels `test-XXX-nom-outil` (identique a `test-002-combos-moteur.py`,
     reference validee 31/31).
9. **ASCII** : 0 caractere non-ASCII sur la definition et la doc de chaque combo.

---

## Protections utilisees

- Navigation systematique en `--dry-run` : aucune commande outil executee.
- Verification qu'aucun fichier n'est cree (cible absente apres le run).
- Variables fournies via `--var` (pas de dependance a l'environnement reel).
- Execution limitee a `combos-moteur` (jamais d'appel direct des outils de creation).

---

## Script

```bash
python3 cerveau-projet/agents/tools/tester/tests/test-003-combos-creer/test-003-combos-creer.py
```

**Resultat** : 86/86 REUSSI, 0 ECHEC, code retour 0.

---

## Verdict

**VALIDE** -- les 3 combos creer-* v0.2.0 fonctionnent conformement a la
spec-combos-moteur : structure JSON correcte, generateur AUTO compose les
commandes via le catalogue, navigation OUI et NON aboutissent a la fin,
parite .py/.sh conservee, dry-run sans effet. Aucun bug detecte dans les combos.

---

## Lecons

1. Les combos creer-* exigent leurs variables (`--var chemin=...`, `--var contenu=...`,
   `--var agent=...`) : sans elles, le moteur renvoie `Variable non trouvee` code 1 --
   c'est une protection saine (jamais de commande partielle).
2. La branche NON d'un controle ne doit PAS generer la commande de creation :
   c'est la preuve que le court-circuit fonctionne (verifie pour les 3 combos).
3. Deux faux positifs de nommage documentes (definitions combo-* et fichiers de
   test tests/) : ne pas corriger, comportement identique aux references validees.
4. Le test formel confirme les validations rapides de Buffy (json.load, navigation,
   ASCII) mais ajoute ce qu'elles ne couvraient pas : parite py/sh, dry-run sans
   effet, branches NON, variables manquantes.
