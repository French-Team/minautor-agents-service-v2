# Controle croise : garde-fou test-052 anti-echappement activation (2026-08-14)

**Controleur** : Janus (session-llm-1) -- chaine Cerberus -> Morpheus -> Janus -> Cerberus

## Verdict : VALIDE (J1-J5)

## J1 - Test-052 : 5/5 OK
- scan des scripts temp (tmp-*/ et .tmp-*.py a la racine)
- tout script invoquant activer/reactiver-agent-principal DOIT utiliser
  subprocess.list2cmdline (sinon KO)
- preuve negative reelle validee (script fautif -> KO, suppression -> OK)

## J2 - Integration lanceur
- test-052 en serie e (24 tests) + garde-fou global (jamais en parallele)
- non-regression passe de 52 a 53 tests

## J3 - Tests lies verts
- test-029 14/14 | test-027 11/11 | test-030 10/10

## J4 - Normes
- test-052 + lanceur : 0 non-ASCII | 0 CRLF

## J5 - Non-regression complete (avec --agent janus)
- 53 OK / 0 KO (pool 46/46 + globaux 7/7) -- 49.4s, conforme reference (+1%)

## Note technique
- Le litteral subprocess.run( dans le docstring du test faisait KO test-030
  (auto-incrimination) -> concatene en deux morceaux (comme test-030).
- La detection de list2cmdline cherche l appel reel QUALIFIE, pas le mot
  seul (un commentaire contenant le mot ne suffit pas).
