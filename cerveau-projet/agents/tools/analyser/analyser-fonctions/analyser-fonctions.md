---
identite:
  type: outil
  appartient_a: commun
  commun: true
---
# analyser-fonctions

**Categorie** : Analyser
**Version** : 0.1.1
**Statut** : ebauche

---

## Objectif

Profiler un script cible (outil ou test) avec `cProfile` et afficher les
fonctions les plus couteuses (temps cumule, temps propre, nombre d appels),
pour cibler les goulots INTERNES d un fichier au-dela du simple temps mural.

---

## Pourquoi cet outil ?

- `analyser-performance-tests` dit QUEL test est lent ; `analyser-fonctions`
  dit POURQUOI (quelle fonction a l interieur du fichier consomme).
- Le profil temporaire est ecrit dans `workspace/tmp-analyser-fonctions/`
  puis supprime a la fin : aucun residu a la racine.

---

## Utilisation

```bash
# Top 20 fonctions (tri temps cumule) d un test
python3 analyser-fonctions.py cerveau-projet/agents/tools/tester/tests/test-032-pool-workers/test-032-pool-workers.py

# Passer des options a tiret au script cible (--agent, --tests, ...)
python3 analyser-fonctions.py cerveau-projet/agents/tools/tester/tester-lancer-non-regression/tester-lancer-non-regression.py --agent janus --journal --tests test-041

# Tri par temps propre (ce que la fonction consomme elle-meme)
python3 analyser-fonctions.py --sort tottime --top 10 <script>

# Tri par nombre d appels
python3 analyser-fonctions.py --sort ncalls <script>

# Version
python3 analyser-fonctions.py --version
```

## Options

| Option | Description |
|---|---|
| `<script> [args...]` | Script a profiler - les arguments a tiret (--agent, --tests, ...) sont acceptes APRES le script ; les options de cet outil (--top/--sort/--no-chrono) se placent AVANT |
| `--top <N>` | N fonctions a afficher (defaut 20) |
| `--sort <cle>` | cumtime (defaut), tottime, ncalls |
| `--no-chrono` | Coupe le chrono de l outil |
| `--version` | Affiche la version |

---

## Sortie

```
[PROFIL] python -m cProfile -o workspace/tmp-analyser-fonctions/xxx.prof <script>
[PROFIL] fin : 12.30s (rc=0)

=== TOP 20 FONCTIONS (tri : cumtime) ===
Appels  Cumule(s)  Propre(s)  Fonction
...
```

---

## Historique

| Version | Date | Description |
|---|---|---|
| 0.1.1 | 2026-08-17 | Accepte les arguments a tiret passes au script cible (argparse.REMAINDER) - un profilage du lanceur avec --agent/--tests ne produit plus d erreur |
| 0.1.0 | 2026-08-17 | Creation : profilage cProfile, tri cumtime/tottime/ncalls, profil temporaire nettoye |
