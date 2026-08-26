# Rapport -- Education JARVIS : "LE LLM EST L'AGENT" (2026-08-26)

## Mission

Le LLM s'incarne JARVIS, active Forge + Vision, puis dit
"Les agents travaillent. J'attends leurs retours." -- ILLUSION :
personne ne travaille en arriere-plan, le LLM EST l'agent.
Une mission en attente dans un inbox = le LLM doit s'incarner l'agent
pour l'executer. "Attendre des retours" = ne rien faire.

## Preuves du constat (disque)

- `outbox/jarvis.jsonl` : 17:39:02 ACTIVATION vision, 18:38:59
  ACTIVATION forge, 18:39:05 ACTIVATION vision (2x vision + 1x forge).
- Bloc session-freelance (AGENTS.md) : raison "Active par jarvis:
  Couvrir les erreurs Pylance dans le harnais JARVIS".
- Encart activites recentes : 20:35:29 | jarvis | R | Relai vers stark
  (JARVIS est le dernier agent actif, pas stark ni vision).

## Corrections appliquees

| Fichier | Correction |
|---|---|
| `freelance/jarvis/jarvis.md` | REGLE ABSOLUE -- LE LLM EST L'AGENT (marbre v2, 2026-08-26) : aucun travail en arriere-plan ; activer != faire travailler ; "j'attends leurs retours" = ne rien faire ; apres activation, poursuivre le round ou rendre la main pour l'incarnation suivante. |
| `freelance/jarvis/parcours/arbre-jarvis.json` | Regle D7 ajoutee (meme message, version guidee). |
| `freelance/jarvis/parcours/theme-distribuer.json` | Regle du theme DISTRIBUER : envoyer = placer EN ATTENTE dans l'inbox ; jamais "les agents travaillent" ; enchainer ou rendre la main. |
| `freelance/jarvis/corrections.md` | Lecon datee 2026-08-26 "LE LLM EST L'AGENT" en tete de la section LECONS. |

## Validations

- JSON valides : arbre-jarvis.json OK, theme-distribuer.json OK.
- Formats preserves : LF pur (fichiers jarvis en LF), accents v2
  preexistants intacts (jarvis.md 56 octets non-ascii = preexistants).
- Regle presente aux 4 endroits (fiche + arbre + theme + corrections).

## Note

Les fichiers JARVIS sont en LF (pas CRLF) : le format existant a ete
respecte, comme pour les fichiers Stark (convention : suivre le format
du fichier cible, pas une norme abstraite).
