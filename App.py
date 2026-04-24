import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from streamlit_gsheets import GSheetsConnection
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import base64
from PIL import Image
import io
import time

# Definir a senha de login
SENHA_CORRETA = st.secrets["credentials"]["password"]

# Criamos uma função de login
def verificar_senha():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.title("Acesso Restrito 🔒")
        senha_digitada = st.text_input("Digite a senha para acessar:", type="password")
        
        if st.button("Entrar"):
            if senha_digitada == SENHA_CORRETA:
                st.session_state["autenticado"] = True
                st.write("✅Acesso Concedido, Bem-Vindo ao Enxoval")
                time.sleep(3)
                st.rerun()
            else:
                st.error("Senha incorreta! ❌")
        return False
    return True

# 3. Aplicamos a trava
if verificar_senha():
    
    st.title("🏠 Enxoval do Casal Jayne & Riann")

    conn = st.connection("gsheets", type=GSheetsConnection)
    # O conn já sabe ler o secrets.toml, então basta pedir o campo 'spreadsheet'
    df = conn.read(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], ttl=0)

    # O ID que você pegou na URL do navegador vai aqui
    folder_id = "10ZQcTVfFMHWNXgTyv5yyFU-UbXwzx3YK"

    # Criandp a Barra Lateral
    st.sidebar.title("Menu")
    aba = st.sidebar.radio("Selecione uma opção:", ["Dashboard","Ver Enxoval", "Carrinho de Compras", "Gerenciar & Excluir"])


    match aba:
        case "Dashboard":
            st.header ("📊Resumo e Valor Total")
            
            # Contagem de itens
            total_itens = len(df)
            comprados = len(df[df['Status'] == 'Comprado'])
            pendentes = len (df[df['Status'] == 'Pendente'])
            # Cáculo de valores 
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
            # Exibindo o valor total gastos no final (ou em destaque)
            st.info(f"💰 Valor Total Investido até agora: R$ {valor_gasto:,.2f}")

        case "Carrinho de Compras":
            st.header ("🛒 Registrar Compra ") 

            # Filtrar apenas os itens que ainda não foram comprados
            itens_pendentes = df[df['Status'] == 'Pendente']['Itens'].tolist()

            if itens_pendentes:
                # Criar a caixa de seleção com esses itens
                item_selecionado = st.selectbox("Qual item você comprou?", itens_pendentes, key="sb_comprar")

                # Campos de input de Quantidade, Preço e Foto
                quantidade = st.number_input("Quantidade", min_value=1, value=1, step=1)
                preco_unitario = st.number_input("Valor Unitário (R$)", min_value=0.0, format="%.2f")
            
                # Criamos duas abas para as opções de imagem
                aba_camera, aba_upload = st.tabs(["📸 Tirar Foto", "📁 Carregar Arquivo"])
                with aba_camera:
                    foto_tirada = st.camera_input("Tire a foto agora")

                with aba_upload:
                    foto_carregada = st.file_uploader("Selecione uma foto da galeria", type=['png', 'jpg', 'jpeg'])

                # Agora precisamos decidir qual das duas usar
                foto_final = foto_tirada if foto_tirada is not None else foto_carregada

                def converter_para_base64(foto_final):
                    try:
                        # 1. Abre a imagem com Pillow
                        img = Image.open(foto_final)
                        
                        # 2. Redimensiona para não estourar o limite da célula do Sheets
                        # (Largura máxima de 600px mantém a qualidade e reduz o tamanho do texto)
                        img.thumbnail((600, 600))
                        
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")
                        
                        # 3. Salva no buffer em formato JPEG comprimido
                        buffer_imagem = io.BytesIO()
                        img.save(buffer_imagem, format="JPEG", quality=70, optimize=True) 
                        
                        # 4. Transforma os bytes em String Base64
                        foto_b64 = base64.b64encode(buffer_imagem.getvalue()).decode('utf-8')
                        
                        # Retorna a string com o cabeçalho de imagem
                        return f"data:image/jpeg;base64,{foto_b64}"
                    
                    except Exception as e:
                        st.error(f"Erro na conversão: {e}")
                        return None

                preco_total = quantidade * preco_unitario
            
                # Mostrar o total para o usuário 
                st.info(f"O valor total da compra será: R$ {preco_total:.2f}")

             
                if st.button("✔️ Confimar Compra"):
                # VERIFICAÇÃO CRUCIAL: Só executa se foto_final não for None
                    if foto_final is not None:
                        
                        string_foto = converter_para_base64(foto_final)
                        df['Foto'] = df['Foto'].astype(str)
        
                        # 2. Localiza e atualiza os dados
                        df.loc[df['Itens'] == item_selecionado, ['Status','Quantidade','Preço Unitário','Preço Total', 'Foto']] = [
                            'Comprado', 
                            float(quantidade), 
                            float(preco_unitario), 
                            float(preco_total), 
                            str(string_foto) # Garante que entra como string
                        ]
                        
                        # 3. Limpeza de Segurança: Substituir valores NaN por vazio 
                        # (O Google Sheets odeia receber NaN do pandas)
                        df = df.fillna("")

                        # 4. Tenta o envio
                        try:
                            conn.update(worksheet="ENXOVAL", data=df)
                            st.success(f"O item {item_selecionado} foi comprado com sucesso!!")
                            st.balloons()
                            time.sleep(2)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erro na API do Sheets: {e}")
                    else:
                        st.warning("Não esqueça de registrar essa conquista incrível🥺")

            else:
                st.info("PARABÉNS!! Todos os itens já foram comprados🍾")
    
        case "Ver Enxoval":
            st.header("🎁 Ver Enxoval")
            st.write("Fotos dos itens comprados")

            ambiente_escolhido = st.selectbox("Escolha o ambiente: ", df['Ambiente'].unique())
            itens_galeria = df[(df['Status'] == 'Comprado') & (df['Ambiente'] == ambiente_escolhido)]

            if itens_galeria.empty:
                st.info("Nenhum item comprado neste ambiente ainda 🥺")
            else:
                # Grade percorrendo os itens de 3 em 3
                for i in range(0, len(itens_galeria), 3):
                    cols = st.columns(3) # Cria 3 contentores lado a lado

                    for j in range(3):
                        if i + j < len(itens_galeria): # Verifica se ainda há itens
                            item = itens_galeria.iloc[i + j]
                            with cols[j]:
                                # 1. Pegamos o valor da coluna Foto
                                link_foto = item['Foto']
                                
                                # 2. Verificamos se o link existe e não é nulo (NaN)
                                if pd.notna(link_foto) and str(link_foto).strip() != "":
                                    # Se o link for válido, exibe a foto
                                    st.image(link_foto, use_container_width=True)
                                else:
                                    # Se estiver vazio, exibe uma imagem padrão (Placeholder)
                                    st.image("https://via.placeholder.com/150?text=Sem+Foto", use_container_width=True)
                                    
                                st.caption(f"**{item['Itens']}**")

        case "Gerenciar & Excluir":
            st.header("📋 Lista Completa e Excluir Itens")

            st.write("Aqui estão os itens do seu enxoval:")
            def estilizar_linhas(linha):
                if linha['Status'] == 'Comprado':
                    # Define cor cinza e fundo suave para efeito "apagado"
                    return ['color: #9e9e9e; bacground-color: #007bff'] * len(linha)
                else:
                    #Destaque para pendentes: Negrito e Azul
                    return ['font-weight: bold; color: #ffffff'] * len(linha)    
                return [''] * len(linha)
            st.dataframe(df.style.apply(estilizar_linhas, axis=1))

            st.subheader("Excluir Compra")
            itens_comprado = df[df['Status'] == 'Comprado']['Itens'].tolist()
            item_para_deletar = st.selectbox("Selecione o item para excluir:", itens_comprado)


            if st.button("❌ Excluir a compra"):
                # Em vez de filtrar apenas pendentes para o delete, pegue a lista completa
                itens_comprado = df[df['Status'] == 'Comprado']['Itens'].tolist()

                item_para_deletar = st.selectbox("Selecione o item para excluir:", itens_comprado, key="sd_deletar")

                if item_para_deletar:
                    # 2. Localiza e atualiza os dados
                    df.loc[df['Itens'] == item_para_deletar, ['Status','Quantidade','Preço Unitário','Preço Total', 'Foto']] = [
                        'Pendente', 0, 0.0, 0.0, "" ]
                    
                    conn.update(worksheet="ENXOVAL", data=df)
                    st.success(f"O item {item_para_deletar} foi excluído com sucesso!!")
                    time.sleep(2)
                    st.rerun()


