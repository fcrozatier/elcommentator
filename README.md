# Elcommentator

Ce repo contient toute la logique du générateur de commentaires trimestriels elcommentator

Ce code est ensuite implémenté en un backend Flask, et un frontend Svelte.

## Comment utiliser ce repo ?

Il contient différents sous-dossiers avec des notebooks Jupyter d'expérimentations distinctes.

En parcourant les différents notebooks vous pourrez reproduire les résultats obtenus par elcommentator voire approfondir certaines expérimentations (génération de texte avec GPT-2)

- `gather_and_clean.csv` est le premier notebook, de récupération, nettoyage et normalisation des données de différentes sources (.pdf, google docs etc.)

- le dossier `nlp` rassemble différentes familles d'algorithmes pour générer des commentaires sur la base des données nettoyées.

  1. `rnn` est un réseau neuronal récurrent simple qui apprend à générer caractère par caractère des séquences de mots.
  Résultats médiocres, trop de mots n'existent pas, syntaxe approximative.

  2. `bert` réalise une analyse de sentiments pour catégoriser les commentaires en cinq familles selon leur positivité.

  3. `ranking` contient une exploration de la loi normale asymétrique dans `skew distribution` qui est ensuite utilisée pour prédire le décile de l'élève dans `skew based ranking`. La corrélation avec `bert` est bonne et un score basé sur la moyenne des deux est créé dans `custom score` permettant un lien solide entre ce score et la positivité du commentaire. La fonction prédisant ce score est enfin définie dans `grading function`.

  4. `regression` contient plusieurs types de modèles : un modèle de régression linéaire simple prédisant le score de l'élève uniquement à partir de sa moyenne ; un modèle multi-variables utilisant également la moyenne de la classe, le min et le max en entrée ; et un modèle de réseau neuronal avec un layer caché interne. Les prédictions du réseau de neuronnes sont meilleures que celles du modèle multi-variables, elles-mêmes meilleures que celles du modèle mono-variables. Cependant les résultats sont moins bons que ceux de la `grading function`.

  5. Différentes tentatives d'utilisation du modèle de génération de texte GPT-2 sont réparties dans le dossier `gpt`.
     - v1 met en oeuvre l'adaptation en français `belgpt` pour générer un commentaire aléatoire (sans distinction de positivité). Résultats corrects, des erreurs de syntaxe. Le modèle a besoin d'un prompt initial pour générer la suite du texte. Le même prompt initial génère le même texte.

     - v2 reprend v1 pour l'adapter à l'api tensorflow.

     - v3 essaie de fine tuner gpt à l'aide du script générique de HuggingFace mais parvient à bout des ressources allouées sur une session Google Colab Pro GPU P100 RAM 27G.

     - v4 essaie de reprendre v1 en ajoutant des tokens de fin de commentaire <|endoftext|> sans succès

     - v5 fine tune gpt2 sans script mais nécessite énormément de ressources : 4 jours de calculs sur Colab Pro. Génère des fichiers très volumineux ~1Go. Résultats décevants, le niveau de français est inutilisable.

## Quel est l'algorithme implémenté ?

La v1 de elcommentator utilise l'algorithme suivant :

1. Les commentaires obtiennent un score de positivité de 1 à 5 par analyse de sentiments (Bert)
2. Une fonction basée sur la loi normale asymétrique permet de prédire un score proche du score de positivité.
3. Un **score moyen** entre les deux précédents est créé pour améliorer la corrélation avec la prédiction pour les futurs essais.
4. Pour une ligne de données (moyenne élève, classe, min, max) une fois le score calculé avec la loi normale asymétrique, un commentaire ayant le même **score moyen** est récupéré et affiché.
