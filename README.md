# 🎀 Projeto Enxoval - Gestão Inteligente com Streamlit & Google Sheets

Este projeto nasceu da necessidade de organizar e gerenciar itens de um enxoval de forma colaborativa, visual e em tempo real. A aplicação permite o cadastro de itens, controle de status (Pendente/Comprado) e visualização de fotos, tudo integrado diretamente a uma planilha do Google Sheets como banco de dados.

## 🚀 Destaques Técnicos & Desafios Superados

O maior desafio técnico deste projeto foi o gerenciamento de mídias. Para contornar limitações de permissões e cotas de armazenamento do Google Drive API, implementei uma solução de **conversão de imagens para Base64**.

- **Otimização de Dados:** As imagens são redimensionadas e comprimidas via biblioteca `Pillow` antes da conversão para garantir que a string final respeite o limite de 50.000 caracteres das células do Google Sheets.
- **Segurança:** Implementação de `st.secrets` para proteção de credenciais de contas de serviço e uso de `.gitignore` para blindagem de arquivos sensíveis.
- **UX/UI:** Interface personalizada com paleta de cores exclusiva e feedback instantâneo ao usuário com mensagens de sucesso e toasts.

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem base do projeto.
- **Streamlit**: Framework para criação da interface web.
- **Pandas**: Manipulação e tratamento dos dados.
- **Google Sheets API**: Utilizado como backend para persistência de dados.
- **Pillow (PIL)**: Processamento e compressão de imagens.

## 📊 Estrutura do Projeto

- `App.py`: Arquivo principal com a lógica da aplicação.
- `.streamlit/config.toml`: Configurações de tema e identidade visual.
- `.gitignore`: Proteção de segredos e arquivos locais de teste.
