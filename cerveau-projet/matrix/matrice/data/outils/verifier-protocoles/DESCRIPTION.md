---
identite:
  type: outil
  appartient_a: matrice-data-outils
  commun: true
---

# OUTIL -- verifier-protocoles -- signale les ecarts du marbre des protocoles

> Outil de la Matrice (lot marbre 3/3) : verification du marbre des
> protocoles de l'operateur. LECTURE SEULE : il signale les ecarts, il ne
> repare JAMAIS le marbre.

## Ce qu'il verifie (dossier `_operateur/optimus-prime/protocoles/`)

1. ASCII strict : tout caractere non-ASCII est signale (ligne:colonne).
2. Front-matter : bloc `identite` present, avec `type: protocole` et
   `appartient_a: optimus-prime` (index exclu).
3. Index synchronise : `protocoles-readme.md` liste chaque protocole
   (lignes de tableau seulement). Un `.md` cite n'est mort que s'il
   n'existe ni dans le dossier ni a son chemin relatif (les liens vers
   la fiche sont legimitimes).

## Ce qu'il MESURE sans le JUGER (groupe `DIT`, marque imprimee `HORS CHAMP`)

Les citations qui designent la ZONE DES SOURCES du createur (`docs/`) sont
MESUREES et DITES (`cible PRESENTE` / `cible ABSENTE`) sous la marque
`HORS CHAMP`, et JAMAIS accusees : elles ne comptent pas dans le verdict.

Pourquoi (MO-489, mesure du 2026-09-29) : la porte ECRIRE -- le seul passage
d'ecriture de la Matrice -- REFUSE toute ecriture dans `docs/` en la nommant
(domicile de la decision : `matrice/data/commun/zone_sources.py`, MO-377).
Un garde qui exigerait qu'une citation vers cette zone soit maintenue
demanderait donc une ecriture que la porte du MEME domaine interdit : il
fabriquerait un rouge que personne ne peut reparer, et le recouvrement par
git n'a pas tenu (recouvre en MO-320, retire a nouveau par le commit du
createur du 2026-09-27).

L'exemption est ETROITE : seul le PREMIER segment du chemin canonique compte,
donc `docs/` est hors champ mais `matrice/docs/` reste juge, comme tout le
reste de la Matrice. Elle est CONSOMMEE chez son domicile, jamais recopiee
(M-076). Et elle est DITE : une exemption muette serait un angle mort.

## Racine (pattern v1)

La racine du workspace se DETECTE en remontant jusqu'au dossier contenant
`AGENTS.md` (elle ne se compte jamais) : l'outil tourne depuis n'importe
quel repertoire courant.

## Commande

    python main.py verifier

## Sortie

- `OK` / `ECART` par groupe de controle, detail fichier:ligne:colonne.
- Code 0 si conforme, code 1 si au moins un ecart.
