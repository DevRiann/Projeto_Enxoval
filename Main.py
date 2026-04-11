import pdfplumber

with pdfplumber.open("checklist_enxoval_2025.pdf") as pdf:
    # Acessando a página 11 (índice 10), onde começa a tabela no pdf
    pagina = pdf.pages[10]
    tabela = pagina.extract_table()

if tabela:
    for linha in tabela[:5]:
        print(linha)
else:
    print("Nenhuma tabela encontrada nesata página. Verifique o índice!")        
