---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# protocoles : INDEX

> Protocoles de l'operateur. Relis celui qui correspond a la situation,
> avant d'agir. Sources : docs/IMPERATIF.md + docs/conversation-unslot-gemma-4.md.

| Protocole | Fichier | Quand l'utiliser |
|---|---|---|
| 1. Reprise de mission | proto-1-reprise-mission.md | Au demarrage / redemarrage de session |
| 2. Auto-evolution | proto-2-auto-evolution.md | Evoluer UN changement reversible a la fois, APRES la mission, avec validation du createur |
| 3. Debug D.A.G. | proto-3-debug-dag.md | Des qu'un probleme apparait : chercher dans le code AVANT de creer |
| 4. Auto-audit 3 axes | proto-4-auto-audit-3-axes.md | Avant toute livraison / validation d'une proposition |
| 5. Auto-amelioration | proto-5-auto-amelioration.md | Des qu'un outil natif fait galerer : declencher la creation de l'outil dedie |
| 6. Route mission | proto-6-route-mission.md | A CHAQUE mission du pilote : injection -> reconnaissance -> execution -> controles -> note -> fin (coeur du mode direct cameleon) |
| 7. Route BDD | proto-7-route-bdd.md | A chaque ecriture vers une BDD : porte unique, atomique, empreinte |
| 8. Route reparation veille | proto-8-route-reparation-veille.md | A chaque mission bloquante deposee par la veille : reproduire, diagnostiquer, reparer, retour vert |
| 9. Mini-missions + inter-round | proto-9-mini-missions-inter-round.md | Decoupage 2-5 minis en serie + inter-round (serie, une preuve par mini, revert 1 retry -> escalade) |
| 10. Route outil defaillant | proto-10-route-outil-defaillant.md | Des qu'un OUTIL se comporte mal PENDANT que je travaille : reproduire, reparer DANS l outil, prouver, tracer, reprendre |
| 11. Raisonnement progressif par segments | proto-11-raisonnement-progressif.md | Pour tout sujet de raisonnement qui DURE (plus d un tour, plus d une session) : ecrire des SEGMENTS traces, a carte d identite, retrouvables par le moteur |
| 12. Loi du round | proto-12-loi-du-round.md | LA LOI DU ROUND sortie du fichier de demarrage (ORDRE 3 les limites, ORDRE 4 le round 4.1 a 4.7, ORDRE 5 quand une porte refuse, annexe des portes et des crochets) : lue UNE FOIS au demarrage, a l ORDRE 2, avant de conduire |
| 13. Si j'etais user | proto-13-si-j-etais-user.md | La phase de REMISE EN QUESTION pendant le travail : quels gestes ingrats le createur (puis optimus et le cameleon) doit refaire pour obtenir un resultat, chiffres dans la BDD des corvees -- le pilote l'injecte AU MOMENT ou on en a besoin |
| 14. Evolution decidee puis executee | proto-14-evolution-decidee.md | Des qu une evolution SIGNIFICATIVE ou OBLIGATOIRE se presente : QUALIFIER, DECIDER (createur si critique ou obligatoire ; auto-evolution tracee si faible/moyen, proto-2), EXECUTER en mission, PROUVER, TRACER -- sa REGLE JUMELLE est lue A L ALLUMAGE (regles-immuables : evolution-decidee, source obligatoire du catalogue demarrage) |

| Ressource | Fichier |
|---|---|
| Discussion d'origine des protocoles 3-4 et des conventions | ../../../docs/conversation-unslot-gemma-4.md (zone des SOURCES du createur, LECTURE SEULE : la Matrice ne l'ecrit ni ne le repare ; recouvrable par git, commit du 2026-09-25) |
