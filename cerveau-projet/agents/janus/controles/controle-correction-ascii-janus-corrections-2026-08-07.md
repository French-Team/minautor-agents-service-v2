# Controle -- Correction ASCII janus/corrections.md (2026-08-07)

**Controleur** : Janus (second controle)
**Mission controlee** : correction des 3 caracteres non-ASCII pre-existants dans `janus/corrections.md` (Buffy)
**Fichier concerne** : `cerveau-projet/agents/janus/corrections.md`

**Mission de controle** :
1. Le fichier passe valider-conformite-ascii : 0 caractere non-ASCII
2. Sens preserve sur la ligne 313 : "cosmetiques" (accent e retire, sans alteration du reste)
3. Sens preserve sur la ligne 327 : guillemets francais remplaces par une formulation ASCII (caracteres U+00AB/U+00BB)
4. Aucun autre contenu du fichier n'a ete modifie (verifier via git diff)

**Verdict** : a determiner

---

## Resultat du controle

**Verdict** : VALIDE (4/4)

| Point | Verification | Resultat |
|---|---|---|
| 1 | 0 caractere non-ASCII | OK |
| 2 | Sens preserve ligne 313 | OK |
| 3 | Sens preserve ligne 327 | OK |
| 4 | Aucun autre contenu modifie | OK |

**Lecons** :
1. Un caractere non-ASCII pre-existant peut etre corrige sans perdre le sens : l'accent est retire du mot, les guillemets francais sont decrits par leur code (U+00AB/U+00BB)
2. La correction d'un fichier de corrections est elle-meme soumise au second controle -- meme quand le fichier appartient au controleur (independance controleur != auteur)
3. Validation : valider-conformite-ascii (0 non-conforme) + lecture integrale avant/apres (modifications limitees aux 2 lignes visees 313 et 327 -- le git diff vs HEAD montre tout le fichier car il n'a jamais ete commit)
4. Correction appliquee le 2026-08-07 : les 3 caracteres detectes au controle liste-parcours sont maintenant corriges, le fichier passe valider-conformite-ascii (0 non-conforme)
