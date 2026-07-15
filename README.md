# Dunder Mifflin — Tableau de bord commercial

Dashboard Streamlit interactif construit sur un jeu de données fictif inspiré de la série *The Office*, simulant l'activité commerciale de l'entreprise Dunder Mifflin (commandes, revenus, retours, performance des commerciaux).

## Objectif

Ce projet a été conçu comme démonstration technique pour illustrer la construction d'un dashboard de A à Z via *Streamlit*: ingestion de données, KPIs dynamiques, visualisations Plotly personnalisées, et composants UI sur mesure (cartes métriques, sparklines, encarts d'analyse).


## Contenu du dashboard

Le dashboard est organisé en 4 onglets :

1. **Présentation** — description du jeu de données et aperçu brut
2. **Performance commerciale** — KPIs globaux (CA, commandes, commerciaux) et graphiques sparklines, classement des commerciaux par CA et par quantité vendue, répartition du CA par segment client, filtre par année
3. **Taux de retour** — taux de retour par région avec mise en évidence de la région la plus problématique et analyse contextuelle
4. **Zone de chalandise** — nombre de clients uniques par région, identification des zones à potentiel de croissance


## Stack technique

- **Streamlit** — framework applicatif et interactivité
- **Pandas** — traitement et agrégation des données
- **Plotly Express** — visualisations (graphiques en barres)
- **SVG custom** — sparklines animées dans les cartes KPI (générées en Python, sans librairie graphique)
- **HTML/CSS inline** — cartes stylisées (KPI, encarts d'analyse) via `st.markdown`

## Lancer le projet

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Données attendues

Le CSV source doit contenir les colonnes suivantes :

| Colonne | Description |
|---|---|
| `order_id` | Identifiant de commande |
| `order_date` | Date de commande |
| `year` | Année de la commande |
| `salesperson` | Nom du commercial |
| `net_revenue` | Chiffre d'affaires net |
| `quantity` | Quantité vendue |
| `unit_price` | Prix unitaire |
| `client_segment` | Segment client |
| `client_name` | Nom du client |
| `region` | Région |
| `is_returned` | Indicateur de retour (0/1 ou bool) |

## Auteur

Projet réalisé par **Alexandre LOUMI** — Data Analyst