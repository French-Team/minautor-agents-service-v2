# Rapport d'ecart - docs v2 vs decisions du 2026-08-22

**Agent** : Redacteur-v2 (round SOLO)
**Date** : 2026-08-22
**Objet** : mise a niveau du perimetre avant reprise des missions de redaction.

## Etat actuel

`cerveau-projet/freelance/proposition-v2.md` capture les decisions D1 a D10
du 2026-08-21 (arbre des decisions, outils dynamiques + non-regression freelance
separee, activation automatisee, standard UTF8+CRLF+emojis, redirections,
commande simple + formulaires, formulaire d'outil, 9 themes de l'arbre,
historique par agent + tokens-historique, BDD des lecons bible).

## Ecarts detectes (decisions du 2026-08-22 NON capturees)

| # | Gravite | Ecart | Source de verite |
|---|---|---|---|
| E1 | MAJEURE | Le flux ROUND / INTER-ROUND / REPRISE est absent des docs v2 (0 occurrence) : remplace le garde-fou obsolete, cascade autorisee, reparation exclusive par l'habilite | protocole-fin-mission v0.2.0, spec-guider-parcours v0.6.3 P13 r5 |
| E2 | MAJEURE | La colonne R/IR de l'historique est absente (activer-agent-principal v0.5.25 --type r/ir) - impacte la section historique/tokens (D9) | activer-agent-principal v0.5.25 |
| E3 | MAJEURE | Le routage de la porte du marbre (STANDARD -> Socrate / EXCEPTIONNEL -> utilisateur) est absent - impacte la section verrous/garde-fous | protocole-securite-marbre v0.2.0 |
| E4 | MINEURE | L'empreinte constitution a change (c78d5df3) et la ligne 5 du cycle fondamental inclut desormais l'INTER-ROUND | AGENTS.md zone marbre |
| E5 | INFO | valider-relecture v0.2.1 filtre les agents reels ; 18 agents au total (Socrate, Redacteur-v2 inclus) | audit E4 du 2026-08-22 |

## Contradiction a arbitrer par l'utilisateur

**D4 (UTF8+CRLF+emojis)** contredit la pratique reelle du 2026-08-22 :
toutes les ecritures du jour sont restees **ASCII strict + LF pur**
(protocole-fin-mission v0.2.0, spec, rapports, lecons). A trancher avant
redaction : soit D4 s'applique seulement aux documents grand public, soit il
est revise.

## Plan de mise a jour propose (prochaine mission de redaction)

1. Section 0 journal : capturer les decisions du 2026-08-22 (INTER-ROUND,
   R/IR, routage marbre) comme D11/D12/D13.
2. Mettre a jour les sections impactees : arborescence (historique R/IR),
   verrous et garde-fous (routage marbre), regles de coordination.
3. Resoudre la contradiction D4 avec l'utilisateur AVANT d'ecrire.
4. Re-audit croise Themis + Janus apres redaction (hors round SOLO).

## Verdict

PERIMETRE HORS DE PERIODE : les docs v2 s'arretent aux decisions du 2026-08-21.
Plan de mise a niveau pret - en attente de mission de redaction.
