---
identite:
  type: readme
  appartient_a: optimus-prime
  commun: false
---

# Systeme de Profil Utilisateur

## Description

Le systeme de profil utilisateur permet de personnaliser les interactions entre la Matrice et ses utilisateurs. Il comprend :

1. **USER-PROFIL.md** : Fiche de profil utilisateur
2. **verifier-profil.py** : Verification de l'etat du profil
3. **questionnaire.py** : Questionnaire de remplissage
4. **theme-user-profil.json** : Theme pour le remplissage

## Utilisation

### Verifier l'etat du profil
```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/pilote/main.py profil # etat + champs restants
python3 cerveau-projet/matrix/_operateur/optimus-prime/pilote/verifier-profil.py # meme etat, lecture directe
```

### Guidage sur le parcours (voie officielle)
```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/pilote/main.py profil --guider
```
Affiche le parcours **USER-PROFIL** (but + questions, une seule a la fois,
regle du theme) puis **charge la mission** de remplissage dans la file
(`--theme USER-PROFIL`). Une mission USER-PROFIL deja en attente suffit :
le guidage ne cree jamais de doublon. Fiche complete = silence.

### Remplir le profil (questionnaire direct)
```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/pilote/main.py profil --remplir
python3 cerveau-projet/matrix/_operateur/optimus-prime/pilote/profil/questionnaire.py
```

### Verification automatique au demarrage
Le gestionnaire de cycle verifie automatiquement le profil au demarrage :
```bash
python3 cerveau-projet/matrix/_operateur/optimus-prime/pilote/injection/cycle.py demarrer
```

### Alerte automatique (routine vigie-profil, Flux 1)
La routine `matrice/routines/vigie-profil/` surveille la fiche et depose une
ALERTE dans l'inbox de la Matrice quand elle est incomplete (porte officielle
`signaler`, anti-spam par signature d'etat). La Matrice route l'alerte vers la
maintenance, qui lance ce pilote -> `profil --guider`.

L'etat de la fiche n'est calcule qu'a UN endroit : le motif partage
`matrice/data/commun/fiche_profil.py`, importe par le pilote ET par la routine
(ne jamais recopier ce chemin : un chemin recopie se decale).

## Champs du profil

| Champ | Obligatoire | Description |
|---|---|---|
| Pseudo | Oui | Comment t'adresser a toi |
| Age | Non | Pour adapter le niveau |
| Style | Oui | Formel / Decontracte / Mixte |
| Interets | Non | Pour proposer du contenu adapte |
| Apprentissage | Non | Visuel / Texte / Pratique |
| Niveau | Non | Debutant / Intermediaire / Avance |

## Integration avec le cycle

Le gestionnaire de cycle verifie le profil :
- Si le profil n'est pas rempli, le questionnaire se lance automatiquement
- Si le profil est rempli, le cycle continue normalement

## Injection dans le sac-a-dos (2026-09-21)

Mesure du jour : la fiche etait **remplie** mais **aucun agent ne la lisait** --
le pilote ne l ouvrait qu au DEMARRAGE (`injection/cycle.py`), pour tester si la
ligne `**Pseudo**` etait remplie, puis jetait le contenu.

Le profil voyage desormais avec **chaque mission** d Optimus, sous le champ
`profil` de l injection (`injection/fonctions.py`, `charger_profil_utile`) :

- les **champs ATTENDUS remplis**, dans l ordre du motif partage ;
- **bornes** par `PLAFOND_PROFIL_TOKENS` (300 tokens, `pilote/constants.py`) et
  **peses** avec le reste du sac-a-dos (`CHAMPS_PESES`) ;
- les champs **vides** sont DITS (`a_remplir`), les champs **coupes** aussi
  (`ecartes_par_plafond`), et une fiche **absente ou illisible** rend un
  avertissement NOMME (le bloc ne se vide jamais en silence).

Garde : `verifier-profil-injection.py` (maillon 33 de la non-regression).

## Avantages

1. **Personnalisation** : Les agents adaptent leur style a l'utilisateur
2. **Amicalite** : Les conversations sont plus agreables
3. **Efficacite** : Les reponses sont plus pertinentes
4. **Flexibilite** : Aucun champ n'est obligatoire
