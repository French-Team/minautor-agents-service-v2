# Protocole PLACEHOLDER -- Stark interroge JARVIS (v0.1.0)

> "JARVIS, qu'est-ce qu'on a ici ?" -- JARVIS repond SANS deleguer.

| Champ | Valeur |
|---|---|
| **Version** | 0.1.0 |
| **Type** | protocole + combos exclusifs JARVIS |
| **Perimetre** | `tools-commun/jarvis/combos/` |

---

## Principe

Stark pose ses questions A JARVIS (objet `JARVIS <COMMANDE> [args]`).
JARVIS utilise SES combos : le combo lui demande son besoin (temps 1),
l'outil travaille pour lui (temps 2), il retourne une reponse prete (temps 3).
JARVIS ne code pas et ne cherche pas lui-meme : les combos font le travail.

**Exclusif** : ces combos n'appartiennent qu'a JARVIS. Aucun autre agent
ne les lance. Toute modification = Vision exclusif.

---

## Les 5 placeholders

| Commande | Besoin | Statut |
|---|---|---|
| `JARVIS ETAT` | Etat du systeme | **OK v0.2.0** (sessions, activite, bloques P1 - verifie) |
| `JARVIS CHERCHE <motif> [--dossier X]` | Recherche locale fichiers/contenu | **OK v0.2.0** (noms + occurrences avec lignes). Web : JARVIS complete par sa capacite web si le sujet sort du projet |
| `JARVIS RAPPELLE <sujet>` | Memoire | PLACEHOLDER (etape 4, partiel: attend BDD Forge) |
| `JARVIS RESUME <fichier>` | Synthese d'un fichier | **OK v0.2.0** (sections, apercu, nb lignes) |
| `JARVIS ? <question>` | Question libre | PLACEHOLDER (etape 5, en dernier) |

## Format de reponse (temps 3)

```json
{"combo": "...", "besoin": "...", "statut": "PLACEHOLDER",
 "travail_prevu": [...], "reponse_placeholder": "...", "date": "..."}
```

`statut` passera de PLACEHOLDER a OK quand le temps 2 sera implemente.

## Round type avec question

```
stark: envoyer --vers jarvis --activer  (objet: "JARVIS ETAT")
jarvis: lit -> lance combo ETAT -> reponse prete
jarvis: envoyer --vers stark --activer  (corps = la reponse)
stark: actif, informe, pret pour la suite
```
