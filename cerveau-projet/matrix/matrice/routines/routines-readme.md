# routines : VIE DE LA MATRICE

> Routines de vie de la Matrice. A revoir avec le createur (IMPERATIF).

## Familles prevues

| Famille | Dossier prevu | Role |
|---|---|---|
| vie | routines/vie/ | demarrage et arret PROPRES de la Matrice (zero processus fantome, zero machine instablee) |
| securite | routines/securite/ | garde-fous : verification d'integrite SHA-256, controles de perimetre d'ecriture, etats des BDD |
| orchestration | routines/orchestration/ | chargement des themes, file de missions en SERIE stricte, transmission au pilote |
| observateurs | routines/observateurs/ | espions : pistage temps/tokens, surveillance du FLUX (non-regression flux, pas fichiers) |

> Premier espion POSE le 2026-09-06 : `espion-integrite/` (tour + boucle, integrite
> de toutes les BDD du registre, journal en ajout seul, arret cooperatif par drapeau).
> Il vit directement dans routines/ ; les familles ci-dessus accueillront les suivantes.

## Regles

1. Chaque routine = un outil Python avec protections d'ouverture/fermeture propres
   (regles-immuables/python-seul.md).
2. Non-regression : les suites surveillent le FLUX (pilote qui ne fonctionne plus,
   Matrice qui ne demarre plus, processus fantomes), pas les fichiers un par un
   (source : IMPERATIF).
3. Securite AVANT le reste : une routine qui detecte un defaut d'integrite signale
   et bloque, elle ne repare pas en douceur.
4. Demarrage dedie : `demarrer-optimus-prime.md` (racine) restera le point d'entree
   de l'operateur ; les routines de vie s'y raccrocheront plus tard (revue commune).

## Statut : EN CONSTRUCTION (3 routines posees, veille PERMANENTE)

Faits : espion-integrite (surveillance BDD), veille-flux (veille en arriere-plan :
corriger-ascii + py_compile, marbre en VIGILE, alertes graves -> intercom, correction
sans interrompre le LLM -- doctrine auto-correction). Chaque passe veille-flux se note
elle-meme dans la BDD usages-outils-combos (outil bdd-usages) et se depose dans la
section passes des activites-recentes (outil bdd-activites) -- tags veille-flux,passe,auto.
Prochaines routines prevues : garde-fous de securite, orchestration des themes,
espions temps/tokens.

VIE (2026-09-06, M-046) : `vie/` -- activateur des boucles de fond. Lancement
DETACHE (survit a la session), etat (ARRET/ACTIVE/fantome nettoye), garde de
double lancement (chaque routine porte SON PID et refuse le second), arret
cooperatif par drapeau (zero processus tue). La veille-flux + l'espion
sont ACTIVEES EN PERMANENT : `python vie/main.py activer` au demarrage de la
Matrice (raccord `demarrer-optimus-prime.md` a poser par le createur). Le bug
de routage `veille arret` (routait vers passe, le drapeau n'etait jamais pose)
a ete attrape et repare au passage (M-046).
