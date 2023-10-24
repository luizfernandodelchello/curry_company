import streamlit as st

st.set_page_config(
    page_title="Home",
)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write("# Curry Company Growth Dashboard")

st.markdown(
    """
        Este dashboard foi construído ao fim do módulo "Analisando dados com Python" do curso de formação de cientista de dados da Comunidade DS.

        ### Como utilizar este dashboard?

        Visão Empresa:
        
            Visão Gerencial: Métricas gerais de comportamento.
            Visão Tática: Indicadores semanais de crescimento.
            Visão Geográfica: Insights de geolocalização
            
        Visão Entregador:
        
            Acompanhamento dos indicadores semanais de crescimento
            
        Visão Restaurante:
        
            Indicadores semanais de crescimento dos restaurantes
    """
)