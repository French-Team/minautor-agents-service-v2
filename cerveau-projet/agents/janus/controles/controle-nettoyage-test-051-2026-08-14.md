# Controle croise : test-051 nettoie ses preuves tmp-t051 (2026-08-14)

**Controleur** : Janus (session-llm-1) -- chaine Cerberus -> Morpheus -> Janus -> Cerberus

## Verdict : VALIDE (J1-J5)

## J1 - Test-051 10/10 (2 runs consecutifs)
- point 8 ajoute : nettoyage des preuves tmp-t051 apres les preuves et le tri
- 0 entree restante apres CHAQUE run (plus d artefact)

## J2 - Registre-tests propre + trie
- 0 entree tmp-t051 | trie decroissant preserve | entrees reelles 832 apres non-regression

## J3 - Tests lies verts
- test-024 15/15 | test-031 10/10 | test-032 10/10

## J4 - Normes
- test-051 : 0 non-ASCII | 0 CRLF

## J5 - Non-regression complete (avec --agent janus)
- 52 OK / 0 KO (pool 46/46 + globaux 6/6) -- 49.3s, conforme reference (+5%)
- apres la non-regression : 0 entree tmp-t051 dans le registre (preuve durable)

## Note technique
- Le lanceur ecrit le JSON avec espaces apres les deux points ; le filtre du
  test detecte les preuves via json.loads (robuste aux 2 formats).
