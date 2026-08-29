# Rapport -- SEPARATION DES FICHIERS V1/V2 (2026-08-26)

**Agent** : Ferrari (session-admin)
**Decision utilisateur** : "au lieu de se compliquer la vie, on va les separer" -
la v2 est l'evolution de la v1, chaque session a SES fichiers avec SON format.

## Pourquoi

Les fichiers partages AGENTS-activite-recente.md / AGENTS-historique.md
etaient ecrits par la v1 (ASCII+LF) ET la v2 (UTF8+CRLF) -> corruptions
croisees en cascade (doublons CR, sections vides, formats alternants).
C'etait une consequence de la v2 = evolution de la v1 : les 2 sessions
partageaient les memes fichiers sans partager le format.

## Fichiers

| Fichier | Session | Format | Contenu |
|---|---|---|---|
| AGENTS-activite-recente.md | session-admin (v1) | ASCII+LF | 50 entrees |
| AGENTS-activite-recente-v2.md | session-freelance (v2) | UTF8+CRLF | 50 entrees |
| AGENTS-historique.md | session-admin (v1) | ASCII+LF | 100 entrees |
| AGENTS-historique-v2.md | session-freelance (v2) | UTF8+CRLF | 100 entrees |

## Corrections code

1. **v2 historique.py v0.15.0** : ACTIVITE_FILE/HISTORIQUE_FILE -> fichiers
   -v2 ; helpers _lire/_ecrire (lecture normalisee LF interne, ecriture CRLF
   explicite -> plus jamais de doublement \r sur Windows).
2. **v2** : harnais-jarvis (2 lectures encart -> -v2), manifest.json
   (perimetre EDITH -> -v2), themes-lire edith/vision/fury, etat.py
   (dernieres_lignes -> -v2), jarvis.md + corrections.md jarvis.
3. **v1 activer-agent-principal** : fallback encart ne cree plus que la
   section session-admin.
4. **outils-llm/demarrer-llm.py** : choisit les fichiers selon la session ;
   ecrit ASCII+LF (v1) ou UTF8+CRLF (v2) ; format corps ## JJ/MM/AAAA
   (JAMAIS ISO YYYY-MM-DD -> sections vides KO test-098).
5. **battement-dev.py** : SIGNAL VISUEL serveur en ORANGE (demande
   utilisateur) - la routine reste visible dans l'encart v2 pour prouver
   que le serveur tourne en arriere-plan ; print securise console cp1252.

## Tests

- test-097 fichiers racine : 3/3 OK (liste blanche + fichiers -v2 +
  USER-DEMANDES + outils-llm)
- test-098 format historique : 7/7 OK (extraction agents par dossier,
  oracle ajoute)
- test-102 timestamps : 6/6 OK
- nr-commun (NR v2) : 6/6 CONFORME
- verifier-coherence v1 : 0 incoherence ; v2 : COHERENT
- Flux bout en bout : v1 ecrit v1, v2 ecrit v2, aucun croisement

## Emoji orange

Le DEV-BATTEMENT affiche desormais : `Tony Stark -- Je suis Iron Man.
[DEV-BATTEMENT 21:47] ORANGE` dans AGENTS-activite-recente-v2.md. Le fichier
v2 etant UTF8+CRLF (convention v2 D4), l'emoji est parfaitement stocke.
