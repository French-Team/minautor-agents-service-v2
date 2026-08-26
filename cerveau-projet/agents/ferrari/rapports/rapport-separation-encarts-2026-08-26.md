# Rapport -- Separation encarts / corps (v1 + v2) -- 2026-08-26

## Mission

AGENTS-historique.md ne doit contenir QUE le corps chronologique
(100 dernieres actions). Les 2 encarts "Activites recentes"
(session-admin + session-freelance) vivent UNIQUEMENT dans
AGENTS-activite-recente.md (50 entrees/section). Verifier et corriger
les 2 cotes (v1 et v2) qui ecrivaient l'encart au mauvais endroit.

## Constat initial (utilisateur)

AGENTS-historique.md contenait encore les 2 sections d'encarts alors
que sa description dit : "Corps chronologique (100 dernieres actions).
Les encarts sont dans AGENTS-activite-recente.md (50 lignes)."

## Causes racines (4, verifiees sur le disque)

### 1. v1 -- activer-agent-principal.py (L652)
`maj_encart_activites(contenu, ...)` mettait a jour l'encart DANS
AGENTS-historique.md, en PLUS de `_ecrire_encart_v1` qui l'ecrit dans
AGENTS-activite-recente.md -> encart duplique dans les 2 fichiers.
**Correction** : appel supprime (l'encart ne vit plus que dans
AGENTS-activite-recente.md via _ecrire_encart_v1).

### 2. v2 -- historique.py `_ecrire_corps`
La fonction modifiait le contenu en memoire mais ne JAMAIS ecrivait le
fichier : elle deleguait a `_limiter_corps`, qui n'ecrit QUE si le
corps depasse MAX_CORPS (100). -> Toute entree ajoutee avec un corps
<= 100 etait PERDUE (bug invisible, confirme par test instrumente :
contenu modifie puis write_text final sans l'entree).
**Correction** : `_ecrire_corps` ecrit TOUJOURS le fichier a la fin ;
`_limiter_corps` retourne le contenu limite (plus d'ecriture interne).

### 3. v2 -- historique.py `_limiter_corps`
Supprimait `idx_entrees[:a_supprimer]` = le DEBUT de la liste. Or le
corps est en ordre DECROISSANT (plus recent en haut) -> il supprimait
les PLUS RECENTES, dont la nouvelle entree, des la premiere insertion
des que le corps depassait 100.
**Correction** : supprimer la FIN (`idx_entrees[-a_supprimer:]`) = les
vraies plus vieilles.

### 4. AGENTS-historique.md -- structure chaotique
2 sections pour le 26/08 (`## 26/08/2026` vide + `## 2026-08-26` ISO
avec les entrees), sections non triees, blocs agent vides, ordre
incoherent (26/08 au milieu de 25/08-21/08).
**Correction** : restaure depuis HEAD (385 entrees) + reconstruction
propre : dates triees decroissantes, agents tries, entrees par heure
decroissante, blocs vides supprimes.

## Validations

| Test | Resultat |
|---|---|
| v1 (oracle historiser) | entree dans corps + encart, 0 encart dans corps |
| v2 (jarvis historiser) | entree dans corps + encart, 0 encart dans corps |
| Limite 100 (5 insertions) | 100 max, nouvelles gardees, plus vieilles evincees |
| verifier-coherence-agents (v1) | 0 incoherence |
| verifier-coherence (v2 jarvis) | 0 incoherence |
| Formats | CRLF preserves, ASCII 0 |

## Fichiers touches

- AGENTS-historique.md : corps 95 entrees, 0 encart, sections propres
- AGENTS-activite-recente.md : 2 encarts (session-admin + freelance)
- cerveau-projet/agents/tools/activer/activer-agent-principal/activer-agent-principal.py
- cerveau-projet/freelance/tools-commun/jarvis/fonctions/historique.py
