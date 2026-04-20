import streamlit as st
import pandas as pd

st.title("🛒 Enxoval Jayne & Rian 🛒")

df = pd.read_excel("dados_projeto.xlsx")
st.write("Aqui estão os itens do seu enxoval:")
st.dataframe(df)

