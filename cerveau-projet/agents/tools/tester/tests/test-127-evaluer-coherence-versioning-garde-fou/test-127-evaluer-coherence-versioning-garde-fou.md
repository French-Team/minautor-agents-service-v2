# Test: evaluer-coherence exclut les tableaux de versioning

- **Numero** : test-127
- **Outil teste** : evaluer-coherence (v0.3.0)
- **Date** : 2026-09-05
- **Mission** : cdd567d1 (volet 1/2, demande utilisateur suite rapport Themis
  evaluation-croisee-periodique-2026-09-05-1835.md)
- **Triplet** : protections + options on/off + chrono (regle immuable v0.3.0)

# Test: Corrections evaluer-coherence v0.3.0

## Contexte

Le rapport Themis evaluation-croisee-periodique-2026-09-05-1835.md signalait
une fausse alerte remontee a chaque scan racine : le placeholder documentaire
`protocole-X/` dans la ligne 63 du tableau de versioning d evaluer-coherence.md
etait compte comme lien casse. Cause : le .sh (appele par le combo
audit-general) portait une copie des motifs generiques SANS `protocole-X`, et
aucune logique n ignorait les lignes des tableaux de versioning.

## Corrections testees (v0.3.0)

1. **Ligne de tableau de versioning ignoree** : toute ligne commencant par
   `| <version>.<mineure>.<corrective>` est ignoree du scan des liens casses
   (les liens des changelogs sont documentaires, pas des liens reels)
2. **Vrai lien casse hors tableau** : toujours detecte (non-regression de la
   detection)
3. **Lien valide** : jamais signale (existence resolue)
4. **Parite py/sh** : le .sh porte sa propre logique de liens (parseur
   embarque) - meme fixture, meme verdict ; `protocole-X` ajoute aux motifs
   generiques du .sh (parite retablie)
5. **Versions alignees** : py 0.3.0-py / sh 0.3.0 / md 0.3.0

## Points

| # | Point | Detail |
|---|---|---|
| 1 | Lien du tableau de versioning ignore | fixture ligne versioning -> lien absent des liens casses |
| 2 | Lien protocole-X/ ignore | ligne versioning 0.3.0 -> lien absent |
| 3 | Vrai lien casse detecte | lien vers fiche inexistante hors tableau -> present |
| 4 | Lien valide non signale | lien vers fichier existant -> absent |
| 5 | Parite .sh : vrai lien casse detecte | le .sh remonte le lien casse |
| 6 | Parite .sh : lien versioning ignore | le .sh ne remonte ni ancien-ref ni protocole-X |
| 7 | Version py = 0.3.0-py | `--version` |
| 8 | Version sh = 0.3.0 | en-tete du .sh |
| 9 | Version md = 0.3.0 | champ Version du frontmatter |
| 10 | ASCII strict 0 non-ASCII | outils + test |
| 11 | LF pur 0 CRLF | outils + test |

## Preuve negative (regle immuable v0.3.2)

Sans le filtre PATTERN_LIGNE_VERSIONING (ancien scan), la fixture avec une
ligne de tableau de versioning portant un lien vers une cible inexistante fait
DETECTER ce lien comme casse. Avec le filtre v0.3.0, il est ignore. La preuve
a ete executee (script temporaire) : ancien scan detecte le lien, nouveau scan
vide. Le garde-fou attrape bien la violation qu il surveille.

## Verdict

11 OK / 0 KO (execution directe + sous protections), 0 residu (fixtures
purgees).