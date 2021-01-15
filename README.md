# Projet_Prog_Avancée

Pour la première exécution de notre programme il faut d'abord vérifier que les deux lignes suivantes :

> import nltk
> nltk.download()

situées au tout début de notre programme soient bien décommentées.

Ensuite, il vous suffit d'exécuter le programme, une fenêtre va alors s'afficher : elle se nomme "NLTK Downloader".

Ensuite, il faut cliquer sur l'onglet "Corpora".
Puis, il vous faut descendre jusqu'à la ligne "Stopwords Corpus" ; la sélectionner et cliquer sur le bouton "Download".

Il est alors possible de (re)commenter les 2 lignes précédentes.

La liste des "stopwords" est désormais download, cette étape n'est donc plus nécessaire lors de nouvelles exécutions !

Pour tester les deux fonctions, celles pour l'étude de la fréquence et celles pour l'étude du TF, il faut les décommenter.

Aussi, pour changer les paramètres des corpus (thème et nombre d'articles) il faut modifier cela dans le code:
Pour Reddit : ligne 355 : ...subreddit('VOTRE THEME').hot(limit=NOMBRE D'ARTICLES VOULUS)
Pour Arxiv : ligne 368 : ...search_query=all:VOTRE THEME&start=0&max_results=NOMBRE D'ARTICLES VOULUS
