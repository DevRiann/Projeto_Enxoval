import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("🏠 Enxoval do Casal Jayne & Riann")

conn = st.connection("gsheets", type=GSheetsConnection)
# O conn já sabe ler o secrets.toml, então basta pedir o campo 'spreadsheet'
df = conn.read(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"])


# Criandp a Barra Lateral
st.sidebar.title("Menu")
aba = st.sidebar.radio("Selecione uma opção:", ["Dashboard & Lista","Fotos", "Carrinho de Compras"])


match aba:
    case "Dashboard & Lista":
        st.header ("📊Resumo e Lista de Itens")
        st.write("Aqui estão os itens do seu enxoval:")

        def estilizar_linhas(linha):
            if linha['Status'] == 'Comprado':
                # Define cor cinza e fundo suave para efeito "apagado"
                return ['color: #9e9e9e; bacground-color: #007bff'] * len(linha)
            else:
                #Destaque para pendentes: Negrito e Azul
                return ['font-weight: bold; color: #007bff'] * len(linha)    
            return [''] * len(linha)
        st.dataframe(df.style.apply(estilizar_linhas, axis=1))

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

    case "Carrinho de Compras":
        st.header ("🛒 Registrar Compra ou Deletar ") 

        # Filtrar apenas os itens que ainda não foram comprados
        itens_pendentes = df[df['Status'] == 'Pendente']['Itens'].tolist()

        if itens_pendentes:
            # Criar a caixa de seleção com esses itens
            item_selecionado = st.selectbox("Qual item você comprou?", itens_pendentes)

            # Campos de input de Quantidade, Preço e Foto
            quantidade = st.number_input("Quantidade", min_value=1, value=1, step=1)
            preco_unitario = st.number_input("Valor Unitário (R$)", min_value=0.0, format="%.2f")
            foto_capturada = st.camera_input("Tire uma foto do item comprado")

            preco_total = quantidade * preco_unitario

            if foto_capturada:
                st.success("Compra registrada com foto! 🎉")
            else:
                    st.warning("Que tal tirar uma para a galeria antes de ")
            
            # Mostrar o total para o usuário 
            st.info(f"O valor total da compra será: R$ {preco_total:.2f}")

            
            if st.button("Confimar Compra ✔️"):
                if foto_capturada:
                    # Localizar o item no DataFrame (Planilha) e mudar o status
                    df.loc[df['Itens'] == item_selecionado, ['Status','Quantidade','Preço Unitário','Preço Total']] = ['Comprado', quantidade, preco_unitario, preco_total]
                    # Utilizando API para salvar as alterações na nuvem (Planilha do Google Sheets)
                    conn.update(data=df)

                    st.success(f"Uhuul! {item_selecionado} marcado como comprado!")
                    st.baloons()
                
                else:
                    st.warning("Que tal tirar uma para a galeria antes de ")
            
                

                # Recarrega a página para atualizarr a lista
                st.rerun()
        else:
            st.info("PARABÉNS!! Todos os itens já foram comprados")
    
    case "Fotos":
        st.header("📸 Fotos")
        st.write("Fotos dos itens comprados")

        ambiente_escolhido = st.selectbox("Escolha o ambiente: ", df['Ambiente'].unique())
        itens_galeria = df[(df['Status'] == 'Comprado') & (df['Ambiente'] == ambiente_escolhido)]

        # Grade percorrendo os itens de 3 em 3
        for i in range(0, len(itens_galeria), 3):
            cols = st.columns(3) # Cria 3 contentores lado a lado

            for j in range(3):
                if i + j < len(itens_galeria): # Verifica se ainda há itens
                    item = itens_galeria.iloc[i + j]
                    with cols[j]:
                        st.imagem(item['Foto'], use_column_width=True)
                        st.caption(f"**{item['Itens']}**")

