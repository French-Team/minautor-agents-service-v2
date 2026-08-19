# Rapport de tests - valider-tableaux (filtre fiche-agent + wrapper)

**Date** : 2026-08-18
**Agent** : Morpheus
**Mission** : non-regression de valider-tableaux apres correction par Vulcain
(filtre `type: fiche-agent` + .sh en wrapper pur) + creation du test manquant.

---

## 1. Verification de l outil (tous les modes)

| Mode | Resultat |
|---|---|
| `valider-tableaux.py --version` | v0.2.1-py |
| `valider-tableaux.sh --version` (wrapper bash) | v0.2.1-py - fonctionne (plus de bug stdin) |
| Fiche `cerberus.md` | CONFORME (1 fichier, 0 probleme) |
| Dossier agents complet | **CONFORME 23/23 - classeur-variables exclu** |
| `--agent argus` | CONFORME |
| Parite .sh/.py | identique (meme nombre de fichiers analyses) |
| Normes | ASCII 0 / LF pur (py + sh + md) |

## 2. Nouveau test cree : test-094-valider-tableaux-fiche-agent

- **Serie** : b (Parcours et validateurs) - affecte dans SERIES du lanceur.
- **Points** : presence+compile, --version, wrapper .sh (anti-regression bug
  stdin Windows), cerberus CONFORME, dossier agents sans classeur-variables
  (faux positif corrige), --agent argus, parite .sh/.py, normes ASCII/LF.
- **Resultat** : **7 OK / 0 KO** (0.54s).
- Conforme au template : protections importees (test-030 ne le signale pas),
  options on/off + chrono, ASCII strict, LF pur.

## 3. Non-regression

| Test | Resultat | Commentaire |
|---|---|---|
| test-058 (seul buffy corrige) | **6/6 OK** | registre OK avec mes declarations |
| test-027 (series garde-fou) | 6 OK / 5 KO | **KO preexistants** : verrou d'habilitation janus (points 5-8), pas lies a ma mission |
| test-030 (protections importees) | 8 OK / 2 KO | **KO preexistant** : test-093 sans bloc protections (pin mission combos-full-ascii) |

> Le lanceur officiel de non-regression est verrouille a Janus (verrou
> d'habilitation) : le lancement complet des series sera fait par Janus sous
> SA session.

## 4. Verdict

**CONFORME** - l outil est corrige et fiable, un test dedie couvre desormais
l anti-regression (faux positif classeur-variables + wrapper .sh). Aucune
regression causee par cette mission ; les KO observes sont preexistants
(documentes ci-dessus).
