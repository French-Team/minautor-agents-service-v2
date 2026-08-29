---
identite:
  type: pense-bete
  appartient_a: commun
  commun: true
---
# Pense-bete -- Veille de volume v2 (inbox JARVIS)

**Statut :** ebauche
**ID :** 001
**Class :** 01
**Cree :** 2026-08-29
**Theme :** veille-volume-v2

## 1. Idee (1-2 phrases)

Surveiller le volume des inbox/outbox de la v2 (JARVIS) qui grossissent
regulierement, et prevoir une rotation/purge des anciens messages avant
qu ils ne deviennent un probleme de place ou de lenteur.

## 2. Probleme / Question

Lors de l audit de corruption des inbox/outbox (2026-08-29), les fichiers
de la v2 se sont reveles SAINS mais VOLUMINEUX :

- `inbox/stark.jsonl` : ~2,2 Mo (~2676 messages)
- `inbox/jarvis.jsonl` : ~1,6 Mo (~2230 messages)
- autres inbox/outbox v2 (vision, edith, jarvis-harnais) : cumuls similaires
- `file-asap.jsonl` et `file-attente.jsonl` : BOM UTF-8 mais 100% lisibles

Chaque tic de routine v2 ecrit des entrees : c est un cumul legitime, pas
de la corruption. Mais sans rotation, ces fichiers grossiront indefiniment.

## 3. Contexte

- Decouvert pendant l audit de non-corruption des inbox/outbox v1 + v2
  (round 2026-08-29, incident corruption hub v1 resolu : cerberus.jsonl
  avait atteint 1 Go a cause d un bug de re-echappement du relais v1).
- Domaine v2 : agents freelance, JARVIS, EDITH -- le trio projet n est
  PAS concerne (le cerveau-projet est gere par Buffy).
- Sources : `cerveau-projet/freelance/` (agents), outils communs v2.

## 4. Liens

- Pense-betes connexes : *(aucun pour l instant)*
- Conventions applicables : `pense-betes/index-pense-bete.md`,
  `agents/conventions/renommage/convention-renommage.md`
- Regles immuables : regles de la v2 (perimetre write `freelance/`),
  exclusivite JARVIS (seul Vision modifie JARVIS)

## 5. Structure prevue (RVAV par sous-partie)

| Sous-partie | Fichier cible | Statut | RVAV |
|---|---|---|---|
| Idee | `veille-volume-v2.001.01.ebauche.md` | ebauche | [ ] recherche [ ] |
| Spec | `specs/spec-veille-volume-v2.001.01.ebauche.md` | -- | a creer |
| Todo | `specs/todo/todo-veille-volume-v2.001.01.ebauche.md` | -- | a creer |
| Liens | `liens/liens-veille-volume-v2.001.01.ebauche.md` | -- | a creer |

## 6. RVAV du pense-bete

- [rechercher] -- les tailles/volumes observes sont rassembles (voir section 2)
- [verifier] -- la structure (idee + probleme + contexte + liens) est complete
- [analyser] -- l idee est coherente avec le cerveau existant (pas de doublon)
- [valider] -- pret pour le statut suivant (`prepare`)
