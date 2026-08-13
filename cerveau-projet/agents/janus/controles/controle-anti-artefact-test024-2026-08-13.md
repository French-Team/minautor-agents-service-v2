---
identite:
  type: rapport-janus
  date: 2026-08-13
  objet: controle croise anti-artefact test-024
---

# Controle Janus : anti-artefact test-024 (Morpheus)

**Contexte** : mission Janus (dernier maillon, active par Themis) - controle
croise final de la correction de l artefact test-024 (non-regression lancee
depuis un script temporaire legitime).

## Verifications (J1-J5)

| Check | Resultat |
|---|---|
| J1. Code lanceur | detecter_parent_temporaire + fallback /proc/powershell + env NON_REGRESSION_EXCLUSIONS : OK |
| J2. Code test-024 | lecture env + exclusion du scan : OK |
| J3. Protection efficace | residu reel non exclu -> KO (12/13) : les vrais residus restent detectes |
| J4. Normes | 0/0 |
| J5. Non-regression complete | 37/37 OK (44.9 s) - lancee depuis .tmp-janus3-controle.py : [INFO] parent exclu + test-024 OK = artefact elimine |

## Analyse

1. La correction est complete et portable : detection du parent via
   os.getppid() + ligne de commande (/proc sur Unix, Get-CimInstance sur
   Windows), fallback sur (aucune exclusion si detection impossible).
2. La protection anti-residus reste INTACTE : seul le parent direct (en
   cours d execution) est exclu ; tout autre .tmp-*/.zz-* reste KO.
3. Preuve finale : la non-regression complete elle-meme a ete lancee depuis
   un script temporaire et a passe 37/37 - le scenario exact qui KO 3 fois
   auparavant est desormais sans friction.

## Verdict : VALIDE

Correction conforme, artefact elimine, protection intacte, normes 0/0,
non-regression complete 37/37 OK. Fin de chaine : reactivation Cerberus.
