import streamlit as st
import pandas as pd

st.title("🏠 Enxoval do Casal Jayne & Rian 🧑🏽‍❤️‍👩🏽")

df = pd.read_excel("dados_projeto.xlsx")


# Criandp a Barra Lateral
st.sidebar.title("Menu")
aba = st.sidebar.radio("Selecione uma opção:", ["Dashboard & Lista", "Carrinho de Compras"])

if aba == "Dashboard & Lista":
    st.header ("📊Resumo e Lista de Itens")
    st.write("Aqui estão os itens do seu enxoval:")
st.dataframe(df)

#Contagem de itens
total_itens = len(df)
comprados = len(df[df['Status'] == 'Comprado'])
pendentes = len (df[df['Status'] == 'Pendente'])
#Cáculo de valores 
valor_gasto = df[df['Status'] == 'Comprado']['Preço Total'].sum()

st.subheader("Resumo do Enxoval")

# Criando colunas para as métricas
col1, col2, col3 = st.columns(3)
col1.metric("Total de Itens", total_itens)
col2.metric("Itens Comprados", comprados, delta=f"{comprados/total_itens}")
col3.metric("Itens Pendentes", pendentes)
# Criandp um gráfico simples de barras
status_counts = df['Status'].value_counts()
st.bar_chart(status_counts)
#Exibindo o valor total gastos no final (ou em destaque)
st.info(f"💰 Valor Total Investido até agora: R$ {valor_gasto:,.2f}")

elif aba == "Carrinho de Compras":
    st.header ("🛒 Registrar Compra ou Deletar ") 