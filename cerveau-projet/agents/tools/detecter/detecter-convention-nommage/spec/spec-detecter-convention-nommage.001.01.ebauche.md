# Spec -- detecter-convention-nommage (garde-fou anti-recurrence)

**Version** : 0.1.0
**Statut** : ebauche
**Date creation** : 2026-08-11
**Agent** : Vulcain (creation, suite recommandation Themis 2026-08-11)
**Historique** : v0.1.0 (creation, 2026-08-11) : scan recursif des .md/.py/.sh,
detection des mentions `c<numero>[a-z]?` hors contexte etendu cT* (fenetre
+/- 2 lignes contenant `c[<prefixe-alpha-maj>]` ou cT1..cT10), exclusions
corrections.md + tests/ par defaut (--tout pour lever), --rapport optionnel
(Pattern 12 CREATION LIMITEE), verdict CONFORME/ECARTS.

---

## 1. Objectif

Empecher la recurrence de l'ecart detecte par l'audit Themis 2026-08-11 : des
mentions de l'ancienne convention `c<numero>[a-z]?` SANS l'extension cT*
restaient dans les specs et commentaires (8 mentions dans generateurs-ligne,
corrigees par Vulcain). L'outil scanne les fichiers pour signaler toute mention
hors contexte etendu.

## 2. Convention de nommage ETENDUE (source de verite)

`c[<prefixe-alpha-maj>]<numero>[a-z]?` (valider-case v1.1.0) :
- cas normal : `c<numero>[a-z]?` (`c0`, `c12b`, `c29d`) ;
- prefixe thematique MAJUSCULE optionnel d'UNE lettre : `cT1`..`cT10`
  (ligne Trio de Janus, decision utilisateur 2026-08-11) ;
- le suffixe reste en minuscules ; aucune ponctuation (jamais de point).

## 3. Regles de scan

1. Scan recursif sous `--racine` (defaut : `cerveau-projet`), extensions .md, .py, .sh
   (hors `__pycache__`).
2. Une ligne contenant `c<numero>[a-z]?` est une MENTION.
3. La mention est CONFORME si la fenetre +/- 2 lignes contient
   `c[<prefixe-alpha-maj>]` ou `cT1`..`cT10` (cas normal = partie de la convention
   etendue). Sinon ECART.
4. Exclusions par defaut (--tout pour lever) : `corrections.md` (lecons
   historiques legitimes), dossiers `tests/` (verification des ids generes),
   dossiers `rapports/` et fichiers `rapport-audit-*` (documentent l'historique
   des ecarts).
5. Verdict : CONFORME (code 0, 0 ecart) ou ECART(S) DETECTE(S) (code 1).
6. **CREATION LIMITEE (Pattern 12)** : aucun fichier cree sans `--rapport
   <fichier>` explicite (rapport ecrit exactement au chemin fourni).

## 4. Resultat attendu

- Sur le cerveau-projet actuel : **0 ecart** (8 mentions de generateurs-ligne
  corrigees, corrections.md + tests/ exclus).
- Test negatif : un fichier temporaire avec une mention isolee sans contexte
  etendu doit etre DETECTE (verdict ECARTS, code 1).
