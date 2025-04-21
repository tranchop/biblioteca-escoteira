# 📚 Biblioteca Escoteira

Este projeto é um sistema de gestão de biblioteca para grupos escoteiros, desenvolvido em Python com interface interativa em Streamlit e banco de dados SQLite.

---
## 🚀 Funcionalidades Principais

### 1. Abas de Navegação
- **Livros**: cadastro e listagem de todos os livros, com colunas de ID, título, autor, status e descrição.
- **Usuários**: cadastro e listagem de usuários, incluindo nome, celular e observações.
- **Empréstimos**: filtro de livros por status (disponível/emprestado), registro de novos empréstimos com prazo definido via slider.
- **Histórico**: exibição de todo o histórico de empréstimos e devoluções, com data de empréstimo e devolução.
- **Estatísticas**: gráficos interativos (Plotly) mostrando distribuição de status dos livros e top autores.

### 2. Banco de Dados
- Criação automática de tabelas: `livros`, `usuarios`, `emprestimos` e `historico`.
- Relações integradas via chaves estrangeiras.
- Tabela `historico` armazena todos os registros de devolução.

### 3. Funcionalidades Avançadas
- **Filtrar livros** por status diretamente na aba de Empréstimos.
- **Slider** para definir o prazo de devolução (em dias).
- **Gráficos**:
  - Pizza da distribuição de status dos livros.
  - Barra com os 10 autores mais frequentes.

### 4. Scripts Python
- **database.py**: funções de CRUD, criação de tabelas, empréstimos, devoluções e histórico.
- **app.py**: interface Streamlit organizada em abas, incluindo tabelas e gráficos.

---
## ⚙️ Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/tranchop/biblioteca-escoteira.git
   cd biblioteca-escoteira
   ```

2. Instale as dependências:
   ```bash
   pip install streamlit pandas plotly
   ```

3. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```

4. Acesse no navegador em `http://localhost:8501`.

---
## 📁 Estrutura de Arquivos

```
biblioteca-escoteira/
├── app.py           # Interface Streamlit
├── database.py      # Conexão e operações SQLite
├── biblioteca.db    # Banco de dados gerado automaticamente
└── README.md        # Este arquivo
```

