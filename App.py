#import streamlit as st
#import pandas as pd

#st.title("🛒 Enxoval Jayne & Rian 🛒")

#df = pd.read_excel("dados_projeto.xlsx")
#st.write("Aqui estão os itens do seu enxoval:")
#st.dataframe(df)

import streamlit as st
import pandas as pd
import os

st.title("Teste de Conexão do Arquivo")

# 1. Verificar se o arquivo existe na pasta
if os.path.exists("dados_projeto.xlsx"):
    st.success("✅ O arquivo 'dados_projeto.xlsx' foi encontrado!")
    
    # 2. Tentar ler apenas as primeiras linhas
    df = pd.read_excel("dados_projeto.xlsx")
    st.write("Aqui está uma prévia dos dados:")
    st.table(df.head())
else:
    st.error("❌ O arquivo 'dados_projeto.xlsx' NÃO foi encontrado no repositório.")
    st.write("Arquivos presentes na pasta atual:", os.listdir("."))
