---
# Documentation de Test -- detecter-usage-outils-externes
# Version : 0.1.0
# Statut : prepare

test:
  nom: "test-001-detecter-usage-outils-externes"
  version: "0.1.0"
  outil_teste: "detecter-usage-outils-externes"
  cree: "2026-08-07"
  verdict: "VALIDE (41/41)"

---

# Test: detecter-usage-outils-externes

## Objectif

Verifier que l'outil detecte les traces d'utilisation d'outils EXTERNES dans
les fichiers (BOM UTF-8, CRLF, non-ASCII) et respecte la regle de nommage,
la parite .py/.sh et les conventions ASCII/LF.

## Protections utilisees

- [x] tester-protection-boucles-infinies/tester-protection-boucles-infinies.sh
- [x] tester-protection-erreurs-silencieuses/tester-protection-erreurs-silencieuses.sh
- [x] tester-protection-blocage/tester-protection-blocage.sh

## Cas couverts (41/41 VALIDE)

### 1. Fichier propre (ASCII + LF)
**Objectif**: Verifier qu'un fichier conforme (ASCII strict + LF) est PROPRE
et que l'outil retourne 0.
**Verifie**: PROPRE, aucun SUSPECT, exit 0.

### 2. Fichier CRLF
**Objectif**: Verifier que la trace CRLF est detectee.
**Verifie**: SUSPECT avec signe CRLF, exit 1.

### 3. Fichier avec accents (non-ASCII)
**Objectif**: Verifier que la trace non-ASCII est detectee.
**Verifie**: SUSPECT avec signe non-ASCII, exit 1.

### 4. Fichier avec BOM UTF-8
**Objectif**: Verifier que la trace BOM est detectee.
**Verifie**: SUSPECT avec signe BOM UTF-8, exit 1.

### 5. Fichier multi-signes (BOM + CRLF + accents)
**Objectif**: Verifier que les 3 signes sont detectes simultanement.
**Verifie**: SUSPECT avec BOM UTF-8 + CRLF + non-ASCII, exit 1.

### 6. Fichier sans extension supportee (.exe)
**Objectif**: Verifier que les extensions hors liste sont ignorees.
**Verifie**: aucun SUSPECT, exit 0.

### 7. Dossier vide
**Objectif**: Verifier le comportement sur un dossier sans fichier.
**Verifie**: 0 fichier analyse, exit 0.

### 8. Cible inexistante
**Objectif**: Verifier la gestion d'erreur.
**Verifie**: message ERREUR, exit 1.

### 9. Parite .sh / .py
**Objectif**: Verifier que les versions .sh et .py donnent les memes verdicts
sur les memes fichiers (propre, multi-signes, crlf, cible inexistante).
**Verifie**: verdicts identiques, codes de retour identiques.

### 10. Mode --recursive
**Objectif**: Verifier que le mode recursif trouve les fichiers dans les
sous-dossiers.
**Verifie**: sous.md trouve et PROPRE, exit 0.

### 11. Regle de nommage
**Objectif**: Verifier que le nom de l'outil commence par le prefixe de la
categorie (detecter-).
**Verifie**: prefixe detecter- present sur .sh et .py.

### 12. Conformite de l'outil lui-meme
**Objectif**: Verifier que les fichiers de l'outil respectent ASCII strict
et LF (nos propres regles).
**Verifie**: .py et .sh ASCII strict + LF.

## Resultat

- OK: 41
- ECHEC: 0
- VERDICT: VALIDE

---

## Fichiers lies

- Outil: detecter-usage-outils-externes.py / .sh / .md
- Test: tests/test-001-detecter-usage-outils-externes.sh
- Spec: spec/ (a creer si necessaire)
