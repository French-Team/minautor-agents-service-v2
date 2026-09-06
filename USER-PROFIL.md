# USER-PROFIL -- profil racine de l'utilisateur

> Fiche racine contenant la langue de l'utilisateur. Lue par le pilote
> Oracle (fonctions/pilote.py) qui injecte un rappel de langue au debut
> des messages servis aux agents : un agent ne doit JAMAIS deriver dans
> une autre langue que celle de l'utilisateur.

---

## Langue

| Champ | Valeur |
|---|---|
| Langue | francais |

---

## Utilisation

- Le pilote lit ce fichier a chaque vol et prefixe ses messages du rappel
  de langue (ex : `[LANGUE] Repondre dans la langue de l utilisateur : francais`).
- Pour changer la langue : modifier la valeur du tableau `Langue`, sauvegarder.
- Le fichier est extensible (pseudo, description, etc.) sans changer le pilote :
  seul le champ `Langue` est lu.

---

## Historique

| Date | Action |
|---|---|
| 2026-09-05 | Creation (mission Socrate 6ad81eda restee en plan, reprise par l'utilisateur) |