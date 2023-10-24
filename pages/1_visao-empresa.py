#Importing Libraries
from haversine import haversine
from datetime import datetime
from streamlit_folium import folium_static

#Bibliotecas necessárias
import pandas as pd
import streamlit as st
import pandas as pd
import plotly.express as px
import folium

#Importando dataset
df = pd.read_csv('dataset/train.csv')

#Copiando dataframe
df1 = df.copy()

def clean_code(df1):
    """
        Esta função é responsável pela limpeza do dataframe passado por parametro

        1º - Converte a coluna Age de texto para número
        2º - Exclui valores 'NaN '  presente na coluna 'Road Trafic Density'
        3º - Converte a coluna Ratings de texto para numero decimal (float)
        4º - Converte a coluna Order_date de texto para data
        5º - Converte a coluna Multiple_deliveries de texto para número inteiro (int)
        6º - Remove os espacos dentro de strings/texto/object
        7º - Remove "min()" da coluna time_taken

    """
    #1 - Convertendo a coluna Age de texto para número
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)
    
    #2 - Excluindo valores 'NaN ' coluna 'Road Trafic Density'
    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    #3 - Convertendo a coluna Ratings de texto para numero decimal (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)
    
    #4 - Convertendo a coluna Order_date de texto para data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y')
    
    #5 - Convertendo a coluna Multiple_deliveries de texto para número inteiro (int)
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)
    
    #6 - Removendo os espacos dentro de strings/texto/object
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    
    #7 - Removendo "min()" da coluna time_taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1

def order_metric(df1):
    # Quantidade de pedidos por dia
    df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby( 'Order_Date' ).count().reset_index()
    df_aux.columns = ['order_date', 'qtde_entregas']
    df_aux.head()
    
    fig = px.bar( df_aux, x='order_date', y='qtde_entregas' )

    return fig

def traffic_order_share(df1):
    columns = ['ID', 'Road_traffic_density']
    df_aux = df1.loc[:, columns].groupby( 'Road_traffic_density' ).count().reset_index()
    df_aux['perc_ID'] = 100 * ( df_aux['ID'] / df_aux['ID'].sum() )
    fig = px.pie( df_aux, values='perc_ID', names='Road_traffic_density' )

    return fig

def traffic_order_city(df1):
    columns = ['ID', 'City', 'Road_traffic_density']
    df_aux = df1.loc[:, columns].groupby( ['City', 'Road_traffic_density'] ).count().reset_index()
    df_aux['perc_ID'] = 100 * ( df_aux['ID'] / df_aux['ID'].sum() )
    # gráfico
    fig = px.bar( df_aux, x='City', y='ID', color='Road_traffic_density', barmode='group')
    
    return fig
   
def order_by_week(df1):
    # Quantidade de pedidos por Semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()  
    # gráfico
    fig = px.bar( df_aux, x='week_of_year', y='ID' )

    return fig

def order_share_by_week(df1):
    # Quantidade de pedidos por entregador por Semana
    # Quantas entregas na semana / Quantos entregadores únicos por semana
    df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index()
    df_aux = pd.merge( df_aux1, df_aux2, how='inner' )
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    # gráfico
    fig = px.line( df_aux, x='week_of_year', y='order_by_delivery' )
    
    return fig

def country_maps(df1):
            
    columns = [
        'City',
        'Road_traffic_density',
        'Delivery_location_latitude',
        'Delivery_location_longitude'
        ]
    columns_groupby = ['City', 'Road_traffic_density']
    data_plot = df1.loc[:, columns].groupby( columns_groupby ).median().reset_index()
    data_plot = data_plot[data_plot['City'] != 'NaN']
    data_plot = data_plot[data_plot['Road_traffic_density'] != 'NaN']
    # Desenhar o mapa
    map = folium.Map( zoom_start=11 )
    for index, location_info in data_plot.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']] ).add_to( map )
        
    folium_static( map, width=1024, height=600)

    
df1 = clean_code(df1)

#-------------------------------------------------------------------------------------------
# Fim funções
#-------------------------------------------------------------------------------------------

#Barra Lateral Streamlit
st.header('Marketplace - Visão Cliente')

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')

data_slider = st.sidebar.slider(
    'Até qual valor?',
    value = datetime (2022, 4, 13),
    min_value = datetime(2022, 2, 11),
    max_value = datetime(2022, 4, 6),
    format = 'DD-MM-YYYY'
)

st.sidebar.markdown("""---""")

traffic_option = st.sidebar.multiselect(
    'Condições de trânsito', #Título 
    ['Low', 'Medium', 'High', 'Jam'], #Opções para serem selecionadas 
    ['Low', 'Medium', 'High', 'Jam']  #Opções padrão
)

st.sidebar.markdown("""---""")

#Filtro de datas
linhas = (df1['Order_Date'] < data_slider)
df1 = df1.loc[linhas, :]

#Filtro de trânsito
linhas = df1['Road_traffic_density'].isin(traffic_option)
df1 = df1.loc[linhas, :]


#Layout no Streamlit
tab1, tab2 , tab3 = st.tabs (['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        fig = order_metric(df1)    
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('# Traffic Order Share')
            fig = traffic_order_share(df1)
            # gráfico
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown('# Traffic Order City')
            fig = traffic_order_city(df1)
            # gráfico
            st.plotly_chart(fig, use_container_width=True)
            
with tab2:
    st.markdown('# Order by Week')
    fig = order_by_week(df1)
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('# Order Share by Week')
    fig = order_share_by_week(df1)

    st.plotly_chart(fig, use_container_width=True)

with tab3:
    with st.container():
        st.markdown('# Country Maps')
        country_maps(df1)


































