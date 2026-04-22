import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.title("🏠 Enxoval do Casal Jayne & Riann")

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(spreadsheet)


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

            # Campos de input de Quantidade e Preço
            quantidade = st.number_input("Quantidade", min_value=1, value=1, step=1)
            preco_unitario = st.number_input("Valor Unitário (R$)", min_value=0.0, format="%.2f")

            preco_total = quantidade * preco_unitario

            # Mostrar o total para o usuário 
            st.info(f"O valor total da compra será: R$ {preco_total:.2f}")

            if st.button("Confimar Compra ✔️"):
                # Localizar o item no DataFrame (Planilha) e mudar o status
                df.loc[df['Itens'] == item_selecionado, ['Status','Quantidade','Preço Unitário','Preço Total']] = ['Comprado', quantidade, preco_unitario, preco_total]
                # Salvar no Excel as alterações
                
                conn.update(data=df)

                st.success(f"Uhuul! {item_selecionado} marcado como comprado!")
                st.baloons()

                # Recarrega a página para atualizarr a lista
                st.rerun()
        else:
            st.info("PARABÉNS!! Todos os itens já foram comprados")
    
    case "Fotos":
        st.header("📸 Fotos")
        st.write("Fotos dos itens comprados")