# Rapport d'audit -- mettre-a-jour-versions v0.1.5 (resync cartes-lock)

**Date** : 2026-08-18
**Auditrice** : Themis
**Mission** : audit-fin-mission demande par Vulcain (c15f, evaluation croisee)
**Objet** : modification de `mettre-a-jour-versions` (ajout de
`resynchroniser_cartes_lock` apres bump de carte)

---

## Contexte

Pendant la correction de la carte themis (v0.4.9 -> v0.4.10, mission Buffy),
un bump de version via `mettre-a-jour-versions --parcours` a ecrit le parcours
JSON HORS editer-parcours : l empreinte de `cartes-lock.json` a diverge et
l anti-contournement (barrage n3, regle SEUL BUFFY) a BLOQUE les ecritures
suivantes jusqu a resynchronisation manuelle. L amelioration deleguee a
Vulcain (Pattern 17) : rendre le bumper auto-suffisant.

## Verification

### 1. Code (resynchroniser_cartes_lock)

- [OK] Fonction presente (ligne 177) : charge cartes-lock.json, verifie que la
  carte est verrouillee (`relatif not in cartes` -> skip, protege la fiche .md
  non verrouillee), recalcule l empreinte, reecrit le manifeste.
- [OK] Empreinte normalisee STRICTEMENT identique a editer-parcours
  (LF + rstrip, SHA-256 utf-8) : verifiee par test croise (MATCH).
- [OK] Appel place apres `--wet` reussi ET verification post-bump sans ecart,
  seulement pour `--parcours` (les cartes seules sont concernees).
- [OK] Import hashlib ajoute.

### 2. Versions

- [OK] .py : en-tete 0.1.5 + VERSION = "0.1.5" (2 remplacements).
- [OK] .md : champ 0.1.5 + ligne versionning 0.1.5 ajoutee.
- [OK] `--version` : v0.1.5.
- [OK] Bumper --tous : 0 outil incoherent, 0 remplacement (dry-run).

### 3. Normes

- [OK] ASCII : 0 caractere non-ASCII (.py, .md, corrections.md vulcain).
- [OK] LF : 0 CRLF, EOF newline (3 fichiers).
- [OK] py_compile : syntaxe valide.

### 4. Preuve reelle

- [OK] Lock themis resynchronise : empreinte MATCH avec editer-parcours.
- [OK] Test de perturbation : lock force a 0x64 puis resync -> MATCH avec
  l empreinte normalisee d editer-parcours (preuve du comportement).

### 5. Perimetre

- [OK] Fichiers modifies : .py + .md (outil), corrections.md (lecon vulcain),
  cartes-lock.json (resync themis), registre-usages, lecons.db.
- [OK] Aucun fichier de test touche par Vulcain (tests = Morpheus, conforme
  a la regle IMMUABLE de delegation).

### 6. Points a signaler (pas des defauts)

1. Test-066 et test-067 pinent encore `v0.1.4` (companions bumper) -> a
   adapter par Morpheus lors de la non-regression (maillon suivant).
2. Registre-usages-outils.jsonl contient une mention 0.1.4 (trace de la
   mission precedente) -> historique, sans action.
3. Rapport clio (maj-readme-massive) reference 0.1.4 -> document historique.
4. evaluer-coherence : 15 liens `protocole-X/` casses dans corrections.md
   (buffy, janus) + 11 dossiers vides -> PREEXISTANTS, hors perimetre de
   cette mission.

## Verdict

**CONFORME** -- la modification est correcte, verifiee par preuve reelle
(empreinte MATCH), les versions sont coherentes, les normes respectees.
Aucun defaut. Les tests de non-regression sont delegues a Morpheus (maillon
suivant de la chaine, qui adaptera les pins 0.1.4 de test-066/067).
