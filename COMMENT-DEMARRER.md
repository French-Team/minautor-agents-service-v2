dans ce fichier , on va devoir expliquer ce que user va devoir composer comme demande initial pour demarrer le cerveau-projet:

- pour demarrer une session : "lire 'demarrer.md' | id= 'llm1'
cette commande va permettre de demarrer une session en cours exactement opu vous vous etiez arrete. votre systeme a bugger ?  pas de probleme, le cerveau-projet pourra facilement reprendre une mission en cours, meme si votre ide, cli a bugger et perdu tout l'historique de la conversation.

- pour demarrer une nouvelle session, on va ajouter un argument a notre demande initial : "lire 'demarrer.md' | id= 'llm-1' | nettoyer la session"
cette commande va nettoyer les traces deja existante des autres llm qui se serait connecte.

- pour demarrer un AUTRE llm (multi-llm) : chaque llm a SA propre session et SA propre conversation, et TRAVAILLE EN SERIE : un seul agent est incarne a la fois (jamais 2 missions relayees simultanement - TRAVAIL EN SERIE OBLIGATOIRE, decision utilisateur 2026-09-05). En mode single-llm, le meme llm incarne tous les maillons un par un. Il suffit de changer l'identifiant pour activer un autre llm dans sa propre session : "lire demarrer.md | id= 'kilo-s2'"

