# Controle croise -- Protections importees + protection STOP (fail-fast)

- Date : 2026-08-12
- Controleur : Janus (session-llm-1)
- Objet : verifier la mission de branchement des protections dans les tests
  (demande utilisateur : chaque test DOIT importer les protections via un
  point d entree unique importable + protection STOP fail-fast)

## Contexte

L audit precedent (template-test) avait revele que les 29 tests-0XX
n importaient AUCUNE protection : les anciennes protections
(tester-protection-*) etaient des wrappers autonomes (shell=True) NON
IMPORTABLES depuis un test .py, et aucune protection STOP (fail-fast)
n existait.

## Corrections (Vulcain + Morpheus)

| Element | Changement |
|---|---|
| tester-protections v0.1.0 | POINT D ENTREE UNIQUE importable : lancer_protege (remplacement direct de subprocess.run : timeout + tuer l arbre + erreurs silencieuses), verifier_critique (protection STOP : leve ArretProtection sur echec critique), ArretProtection, CLI --version/--liste |
| 30 tests migres | bloc PROTECTIONS = charger_protections() (importlib) + subprocess.run -> PROTECTIONS.lancer_protege dans chaque test |
| template-test.md v0.2.1 | import OBLIGATOIRE des protections + canevas avec verifier_critique + try/except ArretProtection + checklist |
| protocole-tests v0.3.0 | reecrit : format Python + protections importables + protection STOP + codes de retour ArretProtection |
| fiche morpheus.md | REGLE ABSOLUE PROTECTIONS v0.1 : import obligatoire + lancer_protege + verifier_critique |
| lanceur v0.1.4 | option --fail-fast : des le premier test KO, la suite est STOPPEE (tests restants non lances, bilan dedie) |
| garde-fou test-030 | cree : 10 points (module importable, chaque test avec bloc protections, 0 subprocess.run restant, STOP verifiee reellement, timeout verifie, lanceur --fail-fast, template impose l import, normes) - serie D |
| catalogue / index | 147 / 116 |

## Preuves reelles

- Protection STOP : verifier_critique leve bien ArretProtection sur echec
- Protection timeout : une boucle infinie (while True) est arretee en ~3s
- FAIL-FAST : test KO au milieu -> message "suite STOPPEE, X test(s) non
  lance(s)" + bilan dedie (prouve avec des tests simules, supprimes ensuite)

## Verifications (J1-J8)

| Verif | Resultat |
|---|---|
| J1 : module importable (VERSION, 4 protections actives) | VALIDE (0.1.0, boucles-infinies/erreurs-silencieuses/blocage/stop) |
| J2 : 30 tests avec bloc protections + 0 subprocess.run restant | VALIDE (0 sans bloc, 0 restant) |
| J3 : template v0.2.1 impose l import | VALIDE (Version 0.2.1 + bloc dans le canevas) |
| J4 : protocole v0.3.0 a jour (verifier_critique) | VALIDE (version 0.3.0 + 6 mentions) |
| J5 : lanceur --fail-fast | VALIDE (2 occurrences) |
| J6 : garde-fou test-030 | VALIDE (10 OK / 0 KO) |
| J7 : non-regression complete | VALIDE (30 OK / 0 KO sur 30 tests) |
| J8 : normes ASCII + LF | VALIDE (0 KO sur 36 fichiers) |

## Verdict

**VALIDE (J1-J8)**. Chaque test importe desormais les protections via le
point d entree unique `tester-protections` ; toute execution passe par
`lancer_protege` ; la protection STOP (verifier_critique/ArretProtection)
arrete un test au premier echec critique ; le lanceur supporte --fail-fast
pour stopper la suite. Le garde-fou test-030 empeche toute derive future
(anti-recurrence) : un test sans protections ne peut plus etre cree.

## Lecons Janus

1. UNE PROTECTION NON IMPORTABLE EST UNE PROTECTION MORTE : les wrappers
   autonomes n etaient jamais charges - seul un module importable via un
   point d entree unique rend la protection reelle et verifiable.
2. FAIL-FAST PROUVABLE : la preuve reelle (test KO -> suite stoppee) est
   indispensable - un test qui passe sans preuve ne prouve rien.
3. LA MIGRATION DE TOUS LES TESTS CASCADE : bump catalogue/index/lanceur/
   template -> les tests de compteurs et de versions doivent etre adaptes
   dans la meme mission.
4. UN GARDE-FOU NE DOIT PAS S AUTO-INCRIMINER : le motif verifie (subprocess
   .run, [KO]) ne doit jamais apparaitre litteralement dans son propre code.
