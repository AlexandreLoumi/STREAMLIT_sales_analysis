import streamlit as st
import pandas as pd
import plotly.express as px
import components as ct
import theme as th
import plotly_theme as pt
import textwrap


# Activation layout large
st.set_page_config(layout="wide")


# Cache data
@st.cache_data
def load_data():
    df = pd.read_csv('./data/dunder_mifflin_sales_realiste.csv')
    return df

df = load_data()
df['order_date'] = pd.to_datetime(df['order_date'])


# Global background
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {th.BG};
            color: {th.TEXT};
        }}
    </style>
    """,
    unsafe_allow_html=True
)


# TITLE
st.title("Dunder Mifflin (The Office) - Tableau de bord commercial")


# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    'Présentation',
    'Performance commerciale',
    'Taux de retour',
    'Zone de chalandise'
])


tab1.subheader("Présentation des données")
tab1.markdown("""
              Les données utilisées dans ce tableau de bord proviennent d'un jeu de données fictif inspiré de la série télévisée "The Office".
              Il contient des informations sur les ventes de l'entreprise Dunder Mifflin, y compris les commandes, les revenus, les retours et les performances des commerciaux.
              :""")
tab1.write(df.head(50))

# ----------------------------
# TAB 2 - SALES PERFORMANCE
# ----------------------------
# KPIs

total_revenue = df['net_revenue'].sum()
total_orders = df['order_id'].nunique()
total_salespeople = df['salesperson'].nunique()
revenue_trend = df.groupby(df['order_date'].dt.to_period('M'))['net_revenue'].sum().reset_index()['net_revenue'].tolist()
orders_trend = df.groupby(df['order_date'].dt.to_period('M'))['order_id'].nunique().reset_index()['order_id'].tolist()
print(revenue_trend)

col1, col2, col3 = tab2.columns(3)

with col1:
    ct.metric_card("Chiffre d'affaires total", f"${total_revenue:,.0f}", "💰", th.SUCCESS, trend = revenue_trend)
with col2:
    ct.metric_card("Commandes totales", f"{total_orders:,}", "📦", th.PRIMARY, trend = orders_trend)
with col3:
    ct.metric_card("Commerciaux", total_salespeople, "🧑‍💼", th.INFO)


tab2.subheader("Quels commerciaux performent le mieux ?")

years_filter = tab2.multiselect(
    "Sélectionnez l'année",
    df['year'].unique()
)

df_filtered = df if not years_filter else df[df['year'].isin(years_filter)]


perf_salesperson = df_filtered.groupby('salesperson').agg({
    'net_revenue': 'sum',
    'quantity': 'sum',
    'unit_price': 'mean'
}).reset_index().sort_values(by='net_revenue', ascending=False)

# Revenue per salesperson chart

perf_salesperson['color'] = perf_salesperson['net_revenue'] == perf_salesperson['net_revenue'].max()

revenue_fig = px.bar(
    perf_salesperson,
    x='salesperson',
    y='net_revenue',
    title="Quels commerciaux rapportent le plus de chiffre d'affaires ?",
    labels={'salesperson': 'Commercial', 'net_revenue': "Chiffre d'affaires"},
    color = 'color',
    color_discrete_sequence={
        True: "#D9D9D9",
        False: th.SUCCESS,
    }
)

revenue_fig.update_layout(showlegend=False)
revenue_fig = pt.apply_plotly_defaults(revenue_fig)


# Quantity per salesperson chart

perf_salesperson['color'] = perf_salesperson['quantity'] == perf_salesperson['quantity'].max()

quantity_fig = px.bar(
    perf_salesperson,
    x='salesperson',
    y='quantity',
    title="Quels commerciaux vendent le plus de produits ?",
    labels={'salesperson': 'Commercial', 'quantity': 'Quantité'},
    color='color',
    color_discrete_sequence={
        True: "#D9D9D9",
        False: th.SUCCESS,
    }
)

quantity_fig.update_layout(showlegend=False)
quantity_fig = pt.apply_plotly_defaults(quantity_fig)


col1, col2 = tab2.columns(2)

col1.plotly_chart(revenue_fig, use_container_width=True)
col2.plotly_chart(quantity_fig, use_container_width=True)


# ----------------------------
# CLIENT SEGMENT
# ----------------------------

perf_per_client_segment = df_filtered.groupby('client_segment')['net_revenue'].sum().reset_index()
perf_per_client_segment = perf_per_client_segment.sort_values('net_revenue', ascending=True)

# Opacité proportionnelle au chiffre d'affaires pour mettre en évidence les segments les plus performants
min_op, max_op = 0.3, 1.0
rev_min = perf_per_client_segment['net_revenue'].min()
rev_max = perf_per_client_segment['net_revenue'].max()

perf_per_client_segment['opacity'] = min_op + (
    (perf_per_client_segment['net_revenue'] - rev_min) / (rev_max - rev_min)
) * (max_op - min_op)


segment_fig = px.bar(
    perf_per_client_segment,
    x='net_revenue',
    y='client_segment',
    title="Quel segment client rapporte le plus ?",
    labels={'net_revenue': "Chiffre d'affaires", 'client_segment': 'Segment'},
    color_discrete_sequence=pt.primary_color(),
    text='net_revenue'
)

segment_fig.update_traces(
    texttemplate='$%{text:,.0f}',
    textposition='outside',
    marker_opacity=perf_per_client_segment['opacity'].tolist()
)

segment_fig.update_layout(
    xaxis_tickprefix='$',
    xaxis_tickformat=',.0f'
)

segment_fig = pt.apply_plotly_defaults(segment_fig)

tab2.plotly_chart(segment_fig, use_container_width=True)


# ----------------------------
# TAB 3 - RETURNS
# ----------------------------

tab3.subheader("Quel est le taux de retour par région ?")

returns = df.groupby('region').agg(
    total_orders=('is_returned', 'count'),
    total_returns=('is_returned', 'sum')
).reset_index()

returns['return_rate'] = round(
    returns['total_returns'] / returns['total_orders'] * 100, 2
)

returns['color'] = returns['return_rate'] == returns['return_rate'].max()


return_fig = px.bar(
    returns,
    x='region',
    y='return_rate',
    title="Taux de retour par région",
    labels={'region': 'Région', 'return_rate': 'Taux de retour (%)'},
    color='color',
    color_discrete_map={
        True: th.DANGER,
        False: "#D9D9D9"
    }
)

return_fig.update_traces(
    width=0.5, texttemplate='%{text:,.0f}%',
    textposition='outside',
    text=returns['return_rate'])

return_fig.update_layout(showlegend=False)

return_fig = pt.apply_plotly_defaults(return_fig)

col1, col2 = tab3.columns([1, 1])

col1.plotly_chart(return_fig, use_container_width=True)

with col2:
    top_region = returns.loc[returns['return_rate'].idxmax(), 'region']
    top_rate = returns['return_rate'].max()
    avg_rate = returns['return_rate'].mean()
    ecart = top_rate - avg_rate
    
    st.markdown(
        textwrap.dedent(f"""
        <div style="
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 14px;
            border-left: 4px solid {th.DANGER};
            box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        ">
            <div style="font-size:22px; margin-bottom:12px;">🔍</div>
            <div style="color:{th.TEXT}; font-size:15px; opacity:0.6; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:12px;">
                Analyse des retours
            </div>
            <div style="color:{th.TEXT}; font-size:16px; line-height:1.6;">
                La région <strong>{top_region}</strong> affiche le taux de retour le plus élevé, 
                à <strong>{top_rate}%</strong> — soit <strong>{ecart:.1f} points</strong> au-dessus 
                de la moyenne nationale ({avg_rate:.1f}%).
            </div>
            <div style="color:{th.TEXT}; font-size:14px; opacity:0.7; margin-top:10px; line-height:1.5;">
                Recommandation : auditer les causes de retour spécifiques à cette région 
                (qualité produit, logistique, service client) pour identifier un levier d'amélioration ciblé.
            </div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )


# ----------------------------
# TAB 4 - CLIENTS PER REGION
# ----------------------------
tab4.subheader("Clients uniques par région")

clients_region = df.groupby('region').agg(
    client_name=('client_name', 'nunique')
).reset_index()

clients_region['color'] = clients_region['client_name'] == clients_region['client_name'].min()


clients_fig = px.bar(
    clients_region,
    x='region',
    y='client_name',
    title="Clients uniques par région",
    labels={'region': 'Région', 'client_name': 'Clients'},
    color='color',
    color_discrete_map={
        True: th.DANGER,
        False: "#D9D9D9"
    },
    text='client_name'  # <-- passé ici, en tant que nom de colonne
)

clients_fig.update_layout(showlegend=False)
clients_fig.update_traces(
    width=0.5,
    texttemplate='%{text:,.0f}',
    textposition='outside'
)

clients_fig = pt.apply_plotly_defaults(clients_fig)

col1, col2 = tab4.columns([1, 1])

col2.plotly_chart(clients_fig, use_container_width=True)

with col1:
    low_clients_region = clients_region.loc[clients_region['client_name'].idxmin(), 'region']
    low_clients_count = clients_region['client_name'].min()
    avg_clients = clients_region['client_name'].mean()
    ecart_clients = avg_clients - low_clients_count
    
    st.markdown(
        textwrap.dedent(f"""
        <div style="
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 14px;
            border-left: 4px solid {th.SUCCESS};
            box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        ">
            <div style="font-size:22px; margin-bottom:12px;">🎯</div>
            <div style="color:{th.TEXT}; font-size:15px; opacity:0.6; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:12px;">
                Analyse des zones d'expansion commerciale
            </div>
            <div style="color:{th.TEXT}; font-size:16px; line-height:1.6;">
                La région <strong>{low_clients_region}</strong> est la région à privilégier, 
                avec seulement <strong>{low_clients_count} clients uniques</strong> — soit 
                <strong>{ecart_clients:.0f} de moins</strong> que la moyenne nationale ({avg_clients:.0f}).
            </div>
            <div style="color:{th.TEXT}; font-size:14px; opacity:0.7; margin-top:10px; line-height:1.5;">
                Recommandation : cette région représente un potentiel de croissance inexploité. 
                Une stratégie d'acquisition ciblée pourrait y générer un fort retour sur investissement. <br>
                Il faudrait analyser les raisons de cette sous-représentation (concurrence, notoriété, accessibilité) pour élaborer un plan d'action efficace, et
                vérifier quels commerciaux sont déjà actifs dans cette zone pour attribuer la zone aux meilleurs vendeurs.
            </div>
        </div>
        """).strip(),
        unsafe_allow_html=True
    )