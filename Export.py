import pdfplumber
import pandas as pd

enxoval_pdf = "checklist_enxoval_2025.pdf" # Passando os valores do arquivo pdf para a variável "enxoval_pdf"
dados_para_excel = [] # Criando um Array para formartar as informações e lançar organizadamente para a planilha em excel

with pdfplumber.open(enxoval_pdf) as pdf:
    # Lendo da página 11 (índice 10) até a última página com tabela
    for i in range(10, 21):
        pagina = pdf.pages[i]
        tabela = pagina.extract_table()

        if tabela:
            for linha in tabela:
                # A 'Linha[0] pega a primeira coluna (Produtos)
                # Fazemos um 'if' para ignorar linhas vazias ou o cabeçalho "Produto"
                if linha and linha[0]:
                    produto_bruto = str(linha[0]).strip()

                    if produto_bruto.upper() != "PRODUTO" and produto_bruto != "":
                        dados_para_excel.append({ # Criando a base da planilha no excel, com apenas os 'Itens' já preenchido automáticamente
                            "Ambiente": "",
                            "Itens": produto_bruto,
                            "Quantidade": "",
                            "Preço Unitário.": "",
                            "Preço Total": "",
                        })   

if dados_para_excel:
    df = pd.DataFrame(dados_para_excel)
    df.to_excel("dados_projeto.xlsx", index=False)
    print(f"✅ Sucesso! Arquivo criado com {len(df)} itens.")
else:
    print("❌ Erro: Nada foi extraído. Verifique se as páginas contêm tabelas.")