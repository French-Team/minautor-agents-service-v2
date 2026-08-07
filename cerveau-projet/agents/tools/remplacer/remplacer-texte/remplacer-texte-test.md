# Test de l'outil remplacer-texte

**Version testee** : 0.1.0-beta (sh + py)
**Date** : 2026-08-07
**Dossier de test** : `exemples/test-remplacer-texte/` (cree puis nettoye)

## Test formel (Morpheus)

**Script** : `tests/test-001-remplacer-texte.sh` (numerote selon protocole-tests)
**Protections** : boucles-infinies + erreurs-silencieuses + blocage (sourcees depuis `tools/tester/protections/`)

| Cas | Resultat |
|---|---|
| Test 1 : Remplacement nominal (py) | [OK] 2 fichiers modifies |
| Test 2 : Dry-run ne modifie rien | [OK] SERAIT MODIFIE, rien ecrit |
| Test 3 : Exclusions (AGENTS-historique.md) | [OK] journal intact |
| Test 4 : Idempotence (2e execution) | [OK] 0 modifie |
| Test 5 : Version sh | [OK] 2 fichiers modifies |
| Test 6 : Erreur dossier inexistant | [OK] ERREUR affichee |

**Verdict** : 6/6 tests reussis, 0 echec.

## Cas testes

| # | Cas | Methode | Resultat |
|---|---|---|---|
| 1 | **Nominal (py)** | `remplacer-texte.py dossier 'ancien-nom=nouveau-nom'` | [OK] 2 fichiers modifies, contenu verifie |
| 2 | **Dry-run (py)** | `remplacer-texte.py --dry-run dossier 'ancien-nom=nouveau-nom'` | [OK] 2 fichiers "SERAIT MODIFIE", aucun fichier ecrit |
| 3 | **Exclusions (py)** | Fichier `AGENTS-historique.md` dans le dossier de test | [OK] Non traite (intact apres wet) |
| 4 | **Idempotence (py)** | Re-execution de la meme commande | [OK] 0 fichier modifie a la 2e execution |
| 5 | **Version sh** | `remplacer-texte.sh dossier 'nouveau-nom=final-nom'` | [OK] 2 fichiers modifies |

## Validations techniques

| Controle | Resultat |
|---|---|
| `bash -n` sur le .sh | [OK] |
| `python3 -m py_compile` sur le .py | [OK] |
| ASCII strict (sh, py, md, spec) | [OK] 0 non conforme |
| `valider-nommage` (dossier remplacer/ -> prefixe remplacer-) | [OK] exit 0 |
| `--version` | [OK] affiche la version |
