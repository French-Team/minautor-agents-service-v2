# Routines -- le systeme de surveillance d'EDITH

> Les routines sont des scripts MECANIQUES (sans LLM) executes par le mini
> serveur routines-server selon le manifest.json (D15).

## Structure

```
routines/
|--- manifest.json            <- quelles routines tournent quand + seuils (D15)
|--- demarrage/               <- au lancement de jarvis
|--- arret/                   <- a l'extinction de jarvis
+--- surveillance/            <- en continu (boucle du serveur)
```

## Regles (protocole 16)

1. Les routines LISENT et OBSERVENT - elles ne modifient jamais le projet
2. Une alerte = rapport ecrit dans tools-commun/routines-server/observations/
   + message P1 [EDITH-REVEIL] depose via jarvis.py
3. Le serveur n'active jamais un agent lui-meme : Stark ouvre la cellule
4. Ajouter/retirer une routine = editer manifest.json (D15), pas le code

## Notes de veille

- 2026-08-29 (detection veille-volume) : BUG SIGNALE dans
  `tools-commun/jarvis/fonctions/historique.py` `_limiter_corps` - quand le
  corps AGENTS-historique-v2.md atteint 100 entrees (MAX_CORPS), la
  fonction supprime les entrees les PLUS RECENTES (fin de fichier, la
  nouvelle trace d historique) au lieu des plus anciennes : les nouvelles
  traces des routines disparaissent des la 101e entree. Reparation = domaine
  JARVIS (Vision exclusif), NON corrige ici.
