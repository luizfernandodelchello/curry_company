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

#-------------------------------------------------------------------------------------------
# Inicio funções
#-------------------------------------------------------------------------------------------

def clean_code(df1):
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

def highest_age(df1):
    age = df1.loc[:, 'Delivery_person_Age'].max()
    return age

def younger_age(df1):
    age = df1.loc[:, 'Delivery_person_Age'].min()
    return age

def better_condition(df1):
    better_condition = df1.loc[:, 'Vehicle_condition'].max()
    return better_condition

def worst_condition(df1):
    worst_condition =df1.loc[:, 'Vehicle_condition'].min()
    return worst_condition

def mean_driver(df1):
    mean_driver = df1.groupby('Delivery_person_ID')['Delivery_person_Ratings'].mean().reset_index()
    return mean_driver
    
df1 = clean_code(df1)

#Barra Lateral Streamlit
st.header('Marketplace - Visão Entregadores')

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
    with st.container():
        st.title('Overall Metrics')
        col1, col2, col3, col4 = st.columns(4, gap='large')
        with col1:
            maior_idade = highest_age(df1)
            col1.metric('Maior idade', maior_idade)
        with col2:
            menor_idade = younger_age(df1)
            col2.metric('Menor idade', menor_idade)
        with col3:
            melhor_condicao = better_condition(df1)
            col3.metric('Melhor condição', melhor_condicao)
        with col4:
            pior_condicao = worst_condition(df1)
            col4.metric('Pior condição', pior_condicao)

    
    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('Avaliações média por entregador')
            mean_driver = mean_driver(df1)
            st.dataframe(mean_driver)
        with col2:
            with st.container():
                st.markdown('Avaliações média por trânsito')
                #Fazendo o cálculo de média e de desvio padrão na mesma linha utilizando a função .agg() para executar tudo em uma linha
                mean_std = df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings': ['mean', 'std']})
                
                #Renomeando as colunas
                mean_std.columns = ['Delivery_mean', 'Delivery_std']
                
                #resetando index
                mean_std.reset_index()

                st.dataframe(mean_std)
                
            with st.container():
                st.markdown('Avaliações média por condições climáticas')
                #Fazendo o cálculo de média e de desvio padrão na mesma linha utilizando a função .agg() para executar tudo em uma linha
                mean_std = df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']].groupby('Weatherconditions').agg({'Delivery_person_Ratings': ['mean', 'std']})
               
                #Renomeando as colunas
                mean_std.columns = ['Delivery_Mean', 'Delivery_Std']
               
                #Resetando index
                mean_std.reset_index()  
                st.dataframe(mean_std)
                
    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de Entrega')
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('Top entregadores mais rápidos')
            df2 = df1.loc[:, ['Delivery_person_ID', 'Time_taken(min)', 'City']].groupby(['City', 'Delivery_person_ID']).mean().sort_values(['Time_taken(min)','Delivery_person_ID'], ascending = True).reset_index()

            dfaux1 = df2.loc[df2['City'] == 'Urban', :].head(10)
            dfaux2 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
            dfaux3 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

            df3 = pd.concat([dfaux1, dfaux2, dfaux3]).reset_index(drop=True)
            st.dataframe(df3)

        with col2:
            st.markdown('Top entregadores mais lentos')
            df2 = df1.loc[:, ['Delivery_person_ID', 'Time_taken(min)', 'City']].groupby(['City', 'Delivery_person_ID']).mean().sort_values(['Time_taken(min)','Delivery_person_ID'], ascending = False).reset_index()

            dfaux1 = df2.loc[df2['City'] == 'Urban', :].head(10)
            dfaux2 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
            dfaux3 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)
            
            df3 = pd.concat([dfaux1, dfaux2, dfaux3]).reset_index(drop = True)
            st.dataframe(df3)





































