"""
import pdfplumber
import pandas as pd

nome_do_pdf = "checklist_enxoval_2025.pdf" 

with pdfplumber.open(nome_do_pdf) as pdf:
    # Vamos testar apenas a primeira página com dados (página 11 -> índice 10)
    pagina = pdf.pages[10]
    tabela = pagina.extract_table()
    
    if tabela:
        print("--- Estrutura da primeira linha encontrada ---")
        print(tabela[0]) # Isso mostra o cabeçalho que o PDF reconheceu
        print("\n--- Estrutura da segunda linha (dados) ---")
        print(tabela[1])
    else:
        print("ERRO: Nenhuma tabela detectada na página 11.")
"""
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Criar a conexão
conn = st.connection("gsheets", type=GSheetsConnection)

# Ler os dados da planilha 
df = conn.read()
st.title("Teste de Conexão")
st.write("Se você está vendo os dados abaixo, a conexão funcionou!")
st.dataframe(df)