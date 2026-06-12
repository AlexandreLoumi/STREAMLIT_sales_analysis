import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# Activation du mode "Écran large" sur Streamlit
st.set_page_config(layout = "wide") 


# Chargement du dataset et mise en cache
@st.cache_data
def load_data():
    df = pd.read_csv('./data/dunder_mifflin_sales_realiste.csv')
    return df

df = load_data()

st.title("Dunder Mifflin (The Office) - Tableau de bord commercial")

# Création de tabs pour faciliter la navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Présentation', 'Performance des commerciaux', 'Taux de retour', 'Évolution des ventes', 'Zone de chalandise'])


# Affichage des KPIs principaux et du jeu de données

# Création des KPIs
total_revenue = df['net_revenue'].sum()
total_orders = df['order_id'].nunique()
total_salespeople = df['salesperson'].nunique()

col1, col2, col3 = tab1.columns(3)
col1.metric("Chiffre d'affaires total", f"${total_revenue:,.0f}")
col2.metric("Commandes totales", f"{total_orders:,}")
col3.metric("Commerciaux", total_salespeople)

tab1.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #1e1e1e;
        border: 1px solid #2dd606;
        border-radius: 10px;
        padding: 16px;
    }
    [data-testid="stMetricLabel"] {
        color: #aaaaaa;
        font-size: 0.85rem;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: bold;
    }
    [data-testid="stMetricDelta"] {
        color: #2dd606;
    }
    </style>
""", unsafe_allow_html=True)


tab1.subheader("Présentation des données de ventes")
tab1.write(df.head(50))


# Affichage de la performance des vendeurs
tab2.subheader("Quels commerciaux performent le mieux ?")

best_salesperson_filter = tab2.multiselect("Sélectionnez l'année que vous souhaitez afficher", df['year'].unique())

if not best_salesperson_filter:
    df_filtered = df
else:
    df_filtered = df[df['year'].isin(best_salesperson_filter)]


perf = df_filtered.groupby('salesperson').agg({
    'net_revenue': 'sum',
    'quantity': 'sum',
    'unit_price' : 'mean'
}).reset_index().sort_values(by='net_revenue', ascending=False)

revenue_per_salesperson = px.bar(perf,
              x = 'salesperson',
              y = 'net_revenue',
              title = 'Performance des vendeurs par chiffre d\'affaires',
              barmode = 'group',
              labels = {'salesperson': 'Vendeur ', 'net_revenue': 'Chiffre d\'affaires ' },
              hover_data = {'net_revenue': ':,.0f'}
              )

quantity_per_salesperson = px.bar(perf, x = 'salesperson',
              y = 'quantity',
              title = 'Performance des vendeurs par quantité vendue',
              barmode = 'group',
              labels = {'salesperson': 'Vendeur ', 'quantity': 'Quantité vendue '},
              hover_data = {'quantity': ':,.0f'}
              )

perf_styled = perf.style.format({
    'net_revenue': '${:,.2f}',
    'unit_price': '${:,.2f}'
})

col1, col2 = tab2.columns(2)

with col1:
    st.plotly_chart(revenue_per_salesperson)

with col2:
    st.plotly_chart(quantity_per_salesperson)


# Affichage du taux de retour par région
tab3.subheader("Quel est le taux de retour par région ?")

returns = df.groupby('region').agg(
    total_orders = ('is_returned', 'count'),
    total_returns = ('is_returned', 'sum')
).reset_index()


returns['return_rate'] = round(returns['total_returns'] / returns['total_orders'] * 100, 2)

returns['color'] = returns['return_rate'] == returns['return_rate'].max()

return_rate = px.bar(returns,
              x = 'region',
              y = 'return_rate',
              title = 'Taux de retour par région',
              labels = {'region': 'Région', 'return_rate': 'Taux de retour (%)'},
              color = 'color',
              color_discrete_map={True: '#ff4489', False: '#d9d9d9'}
)

return_rate.update_traces(width=0.5)
return_rate.update_layout(showlegend=False)
tab3.plotly_chart(return_rate)


# Affichage de l'évolution des ventes au fil du temps
tab4.subheader("Comment les ventes évoluent-elles au fil du temps ?")

# Transformation des colonnes de date en format datetime
date_cols = ['order_date', 'return_date']
for col in date_cols:
    df[col] = pd.to_datetime(df[col])


monthly_sales = df.groupby(df['order_date'].dt.to_period('M')).agg({
    'net_revenue': 'sum',
    'quantity': 'sum'
}).reset_index()

monthly_sales['order_date'] = monthly_sales['order_date'].astype(str)

sales_evolution = px.line(monthly_sales,
               x = 'order_date',
               y = 'net_revenue',
                title = 'Évolution du chiffre d\'affaires au fil du temps',
                labels = {'order_date': 'Date ', 'net_revenue': 'Chiffre d\'affaires'},
                color_discrete_sequence = ['#2dd606'],
                hover_data = {'net_revenue': ':,.0f'}
)


tab4.plotly_chart(sales_evolution)


# Affichage du nombre de clients par région
tab5.subheader("Combien de clients uniques avons-nous dans chaque région ?")

clients_region = df.groupby('region').agg({
    'client_name': 'nunique'
}).reset_index()

clients_region['color'] = clients_region['client_name'] == clients_region['client_name'].min()

clients_per_region = px.bar(clients_region,
              x = 'region',
              y = 'client_name',
              title = 'Nombre de clients uniques par région',
              labels = {'region': 'Région', 'client_name': 'Nombre de clients uniques'},
              color_discrete_sequence = ['#1b02a8'],
              color = 'color',
              color_discrete_map={True: '#ff4489', False: '#d9d9d9'},
)


# Identifier la région avec le moins de clients 
idx = clients_region['client_name'].idxmin()
region_min = clients_region.loc[idx, 'region']
value_min = clients_region.loc[idx, 'client_name']

clients_per_region.add_annotation(
    x=region_min,
    y=value_min,
    text="Région sous-exploitée",
    showarrow=True,
    arrowhead=1,
    ax=0,
    ay=-40
)

clients_per_region.update_layout(showlegend=False)

tab5.plotly_chart(clients_per_region)