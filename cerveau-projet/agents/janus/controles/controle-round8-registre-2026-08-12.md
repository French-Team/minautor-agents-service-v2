# Controle croise -- Round 8 : theme REGISTRE ET TRACES (fiabilite de la journalisation)

**Date** : 2026-08-12 | **Controleur** : Janus (session-llm-1) | **Agent corrige** : Vulcain
**Verificateur** : Morpheus (non-regression)

---

## Verdict : VALIDE (J1-J7 verts)

| # | Verification | Resultat |
|---|---|---|
| J1 | Archivage au lieu de purge : registre courant vide + historique enrichi + idempotence (pas de doublon au 2e lancement) | 4/4 OK |
| J2 | Detecteur : filtre .py/.sh (dossiers de tests exclus), sortie sans faux positifs, croisement registre + historique | 7/7 OK |
| J3 | Enregistrer : --agent/--outil vides -> ERREUR rc=1, doublon -> AVERTISSEMENT, registre corrompu -> AVERTISSEMENT sans crash | 5/5 OK |
| J4 | Versions py/sh/md coherentes : tester-lancer 0.1.1, detecter 0.1.1, enregistrer 0.2.1 | 3/3 OK |
| J5 | test-024 13/13 (avec garde-fou memoire) + non-regression complete 26/26 | OK |
| J6 | Catalogue 146 entrees triees, 0 doublon, dry-run 0 a ajouter | OK |
| J7 | Normes : ASCII 0 + LF pur sur 12 fichiers | 0/0 |

---

## Corrections verifiees (mesures reelles, pas lectures)

### A. tester-lancer-non-regression v0.1.1 -- ARCHIVAGE au lieu de purge
DECISION UTILISATEUR. La purge pure (fh.write('')) detruisait la memoire des
declarations a chaque non-regression : le detecteur devenait aveugle au passe
et signalait 12 faux ecarts permanents. Desormais : les lignes du registre
courant sont archivees vers registre-usages-outils.historique.jsonl (append,
dedoublonnage par ligne exacte) puis le registre courant est vide. Verifie par
J1a-J1d : registre 0, historique enrichi, message 'archive dans l historique',
relance sans doublon (13 lignes stables apres 2 lancements).

### B. detecter-usage-scripts-temporaires v0.1.1 -- filtre + memoire
- est_script_temporaire : un script est un FICHIER .py/.sh dont le basename
  commence par .zz-/.tmp-. Les dossiers de tests (.tmp-eol-test/,
  .tmp-gc-test/, .tmp-morpheus-test/) et les .md/.json ne sont PAS des
  scripts : 12 -> 8 non declares (les 8 restants sont de vrais scripts
  historiques jamais declares - ecart honnete).
- scanner_registre croise le registre COURANT et l HISTORIQUE : les
  declarations archivees restent verifiables.

### C. enregistrer-usage-outil v0.2.1 -- garde-fous de fiabilite
- --agent vide / --outil vide : [ERREUR] + code 1 (avant : accepte
  silencieusement rc=0, entree inexploitable)
- doublon (agent+outil+mode+commande+contexte identiques) : [AVERTISSEMENT]
- lignes non-JSON dans le registre cible : [AVERTISSEMENT] avant ajout,
  sans ecraser ni planter

### D. Versions alignees
- tester-lancer-non-regression 0.1.1 (py + md)
- detecter-usage-scripts-temporaires 0.1.1 (py + md)
- enregistrer-usage-outil 0.2.1 (py + sh + md) - le md etait reste en 0.1.0
  alors que le py etait deja en 0.2.0 (divergence pre-existante)

---

## Impacts sur la non-regression
- test-024 : versions mises a jour (v0.1.1/v0.2.1) + nouveau point 13
  'garde-fou memoire' : l historique du registre doit exister (anti-retour
  de la purge pure). 13/13 OK.

## Fichiers modifies (12)
tester-lancer-non-regression py/md, detecter-usage-scripts-temporaires py/md,
enregistrer-usage-outil py/sh/md, test-024, registre-usages-outils.jsonl,
registre-usages-outils.historique.jsonl (cree), corrections vulcain et
morpheus.

## Conclusion
Round 8 VALIDE. Le theme registre/traces a corrige le probleme le plus
insidieux de la journalisation : la PURGE qui faisait perdre la memoire. La
source de verite est desormais archivable et idempotente, le detecteur
distingue les vrais scripts des artefacts de tests, et l'ecrivain refuse les
entrees inexploitables. L'historique du registre (13 lignes) temoigne des
usages des rounds precedents.
