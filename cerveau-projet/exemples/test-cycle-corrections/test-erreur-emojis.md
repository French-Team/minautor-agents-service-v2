---
# Test d'erreur : Emojis dans un fichier
# Ce fichier contient une erreur volontaire

test:
  nom: "test-erreur-emojis"
  version: "0.1.0"
  statut: "test"
  cree: "2026-08-06"
  erreur: "Utilisation d'emojis (interdit)"

---

# Test d'erreur

## Description

Ce fichier contient des emojis qui sont interdits dans le cerveau-projet.

## Contenu avec erreur

Voici un texte avec des emojis :

- [OK] Ceci est correct
- [ERREUR] Ceci est incorrect
- [ATTENTION] Attention
- [DOCUMENT] Note importante
- [RECHERCHE] Recherche

## Erreur detectee

L'erreur est : **Utilisation d'emojis Unicode** alors que la regle immuable `regles-emojis-ascii.md` les interdit.

## Correction attendue

Les emojis doivent etre remplaces par des symboles ASCII :
- [OK] → [OK]
- [ERREUR] → [ERREUR]
- [ATTENTION] → [ATTENTION]
- [DOCUMENT] → [NOTE]
- [RECHERCHE] → [RECHERCHE]
