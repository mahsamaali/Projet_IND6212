# Analyse de la Corrélation entre le Prix du Pétrole et le Sentiment des Tweets

Ce projet explore la relation entre les variations du prix du pétrole et les sentiments exprimés sur Twitter concernant le marché pétrolier.

## Objectif

L'objectif principal est de déterminer s'il existe une corrélation significative entre les fluctuations des prix du pétrole et les sentiments des tweets associés, en utilisant des techniques de web scraping, de traitement du langage naturel (NLP) et d'analyse de séries temporelles.

## Méthodologie

1. **Collecte des Données**:
   - Utilisation de `snscrape` pour extraire des tweets contenant des hashtags pertinents tels que `#oilprice`, `#CrudeOil`, `#fuelprices`, etc.
   - Récupération des données historiques des prix du pétrole sur la même période.

2. **Prétraitement des Données**:
   - Nettoyage des tweets : suppression des doublons, des caractères spéciaux et des liens.
   - Tokenisation et lemmatisation des textes pour une analyse plus précise.

3. **Analyse des Sentiments**:
   - Application de la bibliothèque `nltk` pour attribuer un score de sentiment à chaque tweet.
   - Agrégation des scores de sentiment sur des intervalles de temps définis (par exemple, quotidiennement).

4. **Analyse de la Corrélation**:
   - Comparaison des tendances des scores de sentiment avec les variations des prix du pétrole.
   - Utilisation de méthodes statistiques pour évaluer la force et la signification de la corrélation.

## Résultats

Les résultats de cette étude sont présentés dans le notebook Jupyter disponible dans ce dépôt. Ils incluent des visualisations des tendances des sentiments et des prix, ainsi que des analyses statistiques détaillées.

## Structure du Dépôt

- `data/`: Contient les jeux de données utilisés, y compris les tweets collectés et les prix historiques du pétrole.
- `notebooks/`: Inclut le notebook Jupyter avec le code et les analyses détaillées.
- `scripts/`: Contient les scripts Python pour la collecte, le prétraitement et l'analyse des données.
- `README.md`: Ce fichier, fournissant une vue d'ensemble du projet.

## Prérequis

Assurez-vous d'avoir les bibliothèques Python suivantes installées :

- `snscrape`
- `nltk`
- `pandas`
- `matplotlib`
- `seaborn`

Vous pouvez les installer en utilisant `pip` :

```bash
pip install snscrape nltk pandas matplotlib seaborn
