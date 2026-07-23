# Dunder Mifflin - Tableau de bord commercial

Dashboard Streamlit interactif construit sur un jeu de données fictif inspiré de la série *The Office*, simulant l'activité commerciale de l'entreprise Dunder Mifflin (commandes, revenus, retours, performance des commerciaux).

## Objectif

L'objectif de ce projet était avant tout de découvrir Streamlit pour la réalisation de dashboards.

## Contenu du dashboard

Le dashboard est organisé en 4 onglets :

1. **Présentation** - description du jeu de données et aperçu brut
2. **Performance commerciale** - KPIs globaux (CA, commandes, commerciaux) et graphiques sparklines, classement des commerciaux par CA et par quantité vendue, répartition du CA par segment client, filtre par année
3. **Taux de retour** - taux de retour par région avec mise en évidence de la région la plus problématique et analyse contextuelle
4. **Zone de chalandise** - nombre de clients uniques par région, identification des zones à potentiel de croissance

## Stack technique

- **Streamlit** - pour la partie visuelle
- **Pandas** - traitement et agrégation des données
- **Plotly Express** - visualisations
- **SVG custom** - sparklines dans les cartes KPI
- **HTML/CSS inline** - cartes KPIs stylisées `st.markdown`

## Lancer le projet

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Données attendues

Le CSV source doit contenir les colonnes suivantes :

```
order_id
order_date
year
salesperson
net_revenue
quantity
unit_price
client_segment
client_name
region
is_returned
```
## Auteur

**Alexandre LOUMI** - Data Analyst
alexandreloumi1995@gmail.com
