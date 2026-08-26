# RAPPORT FERRARI -- Audit Stark : il fait le travail au lieu de transmettre a JARVIS

- **Date** : 2026-08-26
- **Agent** : Ferrari (Mecano, v1)
- **Session** : session-admin
- **Mission** : verifier pourquoi Stark fait le travail au lieu de communiquer la mission a JARVIS
- **Perimetre** : `cerveau-projet/freelance/stark/` (lecture + correction v2)

---

## SYMPTOME

L'utilisateur observe : quand une mission arrive, Stark l'execute lui-meme au lieu de la transmettre a JARVIS. L'arbre et les themes documentent pourtant la passerelle JARVIS.

## CAUSES RACINES (3, toutes verifiees sur le disque)

### 1. theme-files.json (branche DECLANCHEUR, arbre v0.3.0) -- PIEGE --activer

- **Ligne 16, bloc [urgent]** : la commande documentee etait
  `jarvis.py envoyer --de stark --vers jarvis --priorite 1 --objet '[URGENT] ...' --corps '...' --activer`
- **Probleme** : `--activer` sur un `envoyer` active le DESTINATAIRE du `envoyer`. Donc `--vers jarvis --activer` active JARVIS, PAS l'agent final. La mission n'arrive jamais a l'agent habilite.
- **Ce fichier a ete restaure le 2026-08-26 07:19** (branche DECLANCHEUR), donc APRÈS la lecon du 25/08 qui documentait ce piege. La restauration a rejoue une version anterieure a la lecon.

### 2. theme-jarvis.json (branche MISSION) -- etape d'incarnation JARVIS absente

- La commande d'envoi etait `envoyer --de stark --vers jarvis --priorite N ...` SANS `--activer` (correct pour un message), mais AUCUNE etape ne disait a Stark d'INCARNER JARVIS ensuite pour lire/acquitter/activer.
- Resultat (lecon 25/08) : les messages restent NON-LUS dans inbox/jarvis.jsonl, jamais routes -> Stark se decourage et fait le travail.

### 3. stark.md v0.4.0 -- fiche en retard sur l'arbre v0.3.0

- La fiche disait « J'ai DEUX visages » (MISSION/DISCUSSION) alors que l'arbre v0.3.0 a TROIS branches (DECLANCHEUR -> theme-files.json).
- `theme-files.json` etait ABSENT de la structure documentee dans la fiche.
- Stark demarre en lisant SA fiche : il ne connait pas la branche FILES -> declencheurs mal traites.

## CORRECTIONS APPLIQUEES (perimetre freelance/ uniquement)

| Fichier | Correction |
|---|---|
| `stark/parcours/theme-files.json` | `--activer` retire du `envoyer --vers jarvis` ; etape INCARNER JARVIS ajoutee (lire, acquitter, puis `jarvis.py activer --agent <X> --session <Y> --mission '...'`) |
| `stark/parcours/theme-jarvis.json` | Commande SANS `--activer` + etape d'incarnation JARVIS explicite ; INTERDIT recentre sur « EN TANT QUE STARK » |
| `stark/stark.md` v0.5.0 | TROIS branches documentees (DECLANCHEUR/MISSION/DISCUSSION), theme-files.json ajoute a la structure, piege `--activer` note dans la regle absolue ARBRE |
| `stark/corrections.md` | Lecon 2026-08-26 « PIEGE RESTAURE » ajoutee |

## VALIDATIONS

| Test | Resultat |
|---|---|
| JSON valides (arbre + 3 themes + fins) | OK 5/5 |
| Liens arbre -> themes existants | OK 3/3 (DECLANCHEUR, MISSION, DISCUSSION) |
| Plus aucun `--vers jarvis --activer` dans les themes | OK (plus que les citations de lecon dans corrections.md) |
| Normes v2 | LF conserve (format existant), accents UTF-8 preexistants |

## LECON POUR L'EQUIPE

1. Quand on RESTAURE un fichier de parcours, le verifier contre les lecons recentes (le piege `--activer` date du 25/08).
2. Quand l'arbre gagne une branche, la fiche doit etre mise a jour dans la MEME intervention (jamais l'arbre sans la fiche).
3. La regle « je ne fais jamais le travail » est deja ecrite dans la fiche de Stark : le vrai probleme etait que les COMMANDES documentees ne permettaient pas de transmettre correctement.
