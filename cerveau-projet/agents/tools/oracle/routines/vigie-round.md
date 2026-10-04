# Routine vigie-round (v1)

**Version :** 0.1.0
**Dossier :** `agents/tools/oracle/routines/`
**Declenchement :** routines-server v1 (manifest.json, toutes les 60 s)

## Role

Partie DETECTION de la decision utilisateur 2026-08-28 ("les deux en
cascade") : la vigie surveille en continu les rounds casses et alerte
Cerberus. **LECTURE SEULE** : elle ne corrige jamais, elle signale.

## C'est quoi un round casse ?

| Type | Detection | Format |
|---|---|---|
| **Session orpheline** | Un agent actif (non Cerberus) sans activite historisee depuis X minutes alors qu il a une mission en cours | Alerte 4W |
| **Chaine en attente** | Etat de carte de l agent actif a `etape=fin` depuis X minutes : le round est termine mais la fin n a pas ete rendue (reactiver-fin --cible oracle non execute, modele aero) | Alerte 4W |

Cas normal jamais alerte : Cerberus actif en accueil (attente utilisateur).

## Sources

- Classeur : `profil-session-admin` -> agent actif
- `AGENTS-activite-recente.md` : derniere activite de l agent
- `oracle/etat-cartes/<agent>.json` : etat de carte du pilote Oracle

## Alerte

Ecrit dans `oracle/inbox/cerberus.jsonl` (meme canal que le harnais
Oracle) avec le format 4W : QUI, QUOI, QUAND, OU.

Anti-spam : le meme cas (memes types d ecart) n est pas re-alerte avant
30 minutes (fichier d etat `etat-vigie.json`).

## Prevention (regle d engagement, decision utilisateur 2026-08-28)

LA DETECTION ALIMENTE LA PREVENTION : toute casse detectee de facon
recurrente doit etre transformee en blocage mecanique (lecon 2026-08-20 :
un garde-fou sans blocage est un garde-fou incomplet).

Premier cas traite (2026-08-28) : le pilote Oracle deroulait tout l arbre
d un agent en un seul appel et activait les maillons de controle
(morpheus/janus/themis) sans aucun travail fait. BLOCAGE MECANIQUE realise
en amont : limite par defaut 1 pas + delegations laissees a l agent
(fonctions/pilote.py). La vigie surveille desormais les residus.

Cycle : 1 detection vigie -> 2 alerte Cerberus -> 3 reparation mecanique
-> 4 nouveau garde-fou (test Morpheus si besoin).

## Usage

```bash
# Scan normal (seuil par defaut 10 minutes)
python3 vigie-round.py

# Seuil personnalise + simulation sans envoi
python3 vigie-round.py --dry-run --seuil-minutes 1

# Sans chrono
python3 vigie-round.py --no-chrono
```

Retour : 0 si succes (alerte envoyee ou rien a signaler), 1 si erreur.

## Option

| Option | Defaut | Description |
|---|---|---|
| `--seuil-minutes N` | 10 | Age minimal (minutes) sans activite avant alerte |
| `--dry-run` | false | Simuler sans envoyer l alerte |
| `--no-chrono` | false | Desactiver le chrono |

## Historique

| Version | Date | Description |
|---|---|---|
| 0.1.0 | 2026-08-28 | Creation : detection session orpheline + chaine en attente, alerte 4W via inbox Oracle, triplet protections/options/chrono |
