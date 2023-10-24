#Importing Libraries
from haversine import haversine
from datetime import datetime
from streamlit_folium import folium_static

#Bibliotecas necessárias
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium

#Importando dataset
df = pd.read_csv('dataset/train.csv')

#Copiando dataframe
df1 = df.copy()

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

#Barra Lateral Streamlit
st.header('Marketplace - Visão Restaurantes')

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
linhas = df1['Order_Date'] < data_slider
df1 = df1.loc[linhas, :]

#Filtro de trânsito
linhas = df1['Road_traffic_density'].isin(traffic_option)
df1 = df1.loc[linhas, :]

#Layout no Streamlit
tab1, tab2 , tab3 = st.tabs (['Visão Gerencial', '_', '_'])

with tab1:
    col1, col2, col3, col4, col5, col6 = st.columns (6)
    with col1:
        st.container()
        entregadores_unicos = df1.loc[:, 'Delivery_person_ID'].nunique()
        col1.metric('###### Entregadores', entregadores_unicos)
    with col2:
        st.container()
        distance = df1['Distance'] = (df1.loc[:, ['Restaurant_latitude', 'Restaurant_longitude', 
                                       'Delivery_location_latitude', 'Delivery_location_longitude']]
                                       .apply(lambda x: haversine( (x['Restaurant_latitude'],   x['Restaurant_longitude']), 
                                                                  (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1))

        destance_mean = np.round(df1['Distance'].mean(), 2)
        col2.metric('###### Distância média', destance_mean)
    with col3:
        st.container()
        df1_aux = df1.loc[df1['Festival'] == 'Yes ']

        df2 = df1_aux.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']})
        
        df2.columns = ['Mean', 'Std']
        
        df2.reset_index()

        df3 = np.round(df2.loc[:, 'Mean'],2 )
        
        col3.metric('###### Tempo médio com festival',df3)
    with col4:
        st.container()

        df1_aux = df1.loc[df1['Festival'] == 'Yes ']

        df2 = df1_aux.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']})
        
        df2.columns = ['Mean', 'Std']
        
        df2.reset_index()

        df3 = np.round(df2.loc[:, 'Std'],2 )
        
        col4.metric('###### Desvio padrão das entregas com festival', df3)
        
    with col5:
        st.container()

        df1_aux = df1.loc[df1['Festival'] == 'No ']

        df2 = df1_aux.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']})
        
        df2.columns = ['Mean', 'Std']
        
        df2.reset_index()

        df3 = np.round(df2.loc[:, 'Mean'], 2)
        
        col5.metric('###### Tempo de Entrega médio sem festival', df3)
    with col6:
        st.container()

        df1_aux = df1.loc[df1['Festival'] == 'No ']

        df2 = df1_aux.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)': ['mean', 'std']})
        
        df2.columns = ['Mean', 'Std']
        
        df2.reset_index()

        df3 = np.round(df2.loc[:, 'Std'], 2)
        
        col6.metric('###### Desvio padrão das entregas sem festival', df3)

    st.container()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('###### Distribuição do tempo por cidade')
        tempo_medio = df1.loc[:, ['Time_taken(min)', 'City']].groupby('City').agg({'Time_taken(min)':['mean','std']})
        
        tempo_medio.columns = ['Mean', 'Std']
                
        df_aux = tempo_medio.reset_index()
        
        fig = go.Figure()
        
        fig.add_trace( go.Bar (name='Control', 
                                       x = df_aux['City'],
                                       y = df_aux['Mean'],
                                       error_y = dict(type = 'data', array=df_aux['Std'])))
        fig.update_layout(barmode='group')
            
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.container()
        st.markdown('###### Tempo médio por cidade')
        df2 = df1.loc[:, ['Time_taken(min)', 'City', 'Type_of_order']].groupby(['City', 'Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']})
    
        df2.columns = ['Mean', 'Std']
        
        df_aux = df2.reset_index()
    
        st.dataframe(df_aux)
        
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('###### Tempo de entrega médio por cidade')
    
        df1['Distance'] = df1.loc[:, ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']].apply(lambda x: haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1)
    
        avg_distance = df1.loc[:, ['City', 'Distance']].groupby('City').mean().reset_index()
        
        fig = go.Figure (data=[ go.Pie( labels = avg_distance['City'], values=avg_distance['Distance'], pull=[0.1, 0, 0])])
    
        st.plotly_chart(fig, use_container_width=True)
            
    with col2:
        st.container()
        st.markdown('###### Tempo médio por tipo de entrega')
           
        df2 = df1.loc[:, ['Time_taken(min)', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})

        df2.columns = ['Mean', 'Std']
           
        df_aux = df2.reset_index()

        fig = px.sunburst (df_aux, path=['City', 'Road_traffic_density'], values = 'Mean', color = 'Std', color_continuous_scale = 'RdBu', color_continuous_midpoint=np.average(df_aux['Std']))

        st.plotly_chart(fig, use_container_width=True)
                               














































