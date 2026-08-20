dans ce fichier , on va devoir expliquer ce que user va devoir composer comme demande initial pour demarrer le cerveau-projet:

- pour demarrer une session : "lire 'demarrer.md' | id= 'llm1'
cette commande va permettre de demarrer une session en cours exactement opu vous vous etiez arrete. votre systeme a bugger ?  pas de probleme, le cerveau-projet pourra facilement reprendre une mission en cours, meme si votre ide, cli a bugger et perdu tout l'historique de la conversation.

- pour demarrer une nouvelle session, on va ajouter un argument a notre demande initial : "lire 'demarrer.md' | id= 'llm-1' | nettoyer la session"
cette commande va nettoyer les traces deja existante des autres llm qui se serait connecte.

- pour demarrer un second llm en parallel qui va pouvoir travailler en ayant concience de la presence d'un autre llm deja present dans le cerveau-projet. cela va permettre de placer plusieurs llm pour travailler sans collision dans leur mission. il suffira juste de changer l'identifiant pour activer le second llm dans sa propre session qui sera commune au premier llm : "lire demarrer.md | id= 'kilo-s2'"

