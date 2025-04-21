import streamlit as st
from database import *

st.set_page_config(page_title="Biblioteca Escoteira", layout="wide")

# Sidebar para navegação
pagina = st.sidebar.selectbox("Navegar para", [
    "Cadastrar Livro",
    "Cadastrar Usuário",
    "Emprestar/Devolver Livro",
    "Status dos Livros"
])

# Página 1: Cadastrar Livro
if pagina == "Cadastrar Livro":
    st.title("📚 Cadastrar Livro")
    titulo = st.text_input("Título do livro")
    autor = st.text_input("Autor")
    descricao = st.text_area("Descrição")

    if st.button("Adicionar Livro"):
        adicionar_livro(titulo, autor, descricao)
        st.success("Livro adicionado com sucesso!")

# Página 2: Cadastrar Usuário
elif pagina == "Cadastrar Usuário":
    st.title("🧑 Cadastrar Usuário")
    nome = st.text_input("Nome do usuário")
    celular = st.text_input("Celular")
    observacoes = st.text_area("Observações")

    if st.button("Cadastrar Usuário"):
        adicionar_usuario(nome, celular, observacoes)
        st.success("Usuário cadastrado com sucesso!")

# Página 3: Emprestar/Devolver Livro
elif pagina == "Emprestar/Devolver Livro":
    st.title("🔁 Emprestar ou Devolver Livro")

    livros_disponiveis = [livro for livro in listar_livros() if livro[3] == 'disponível']
    usuarios = listar_usuarios()

    st.subheader("📖 Emprestar Livro")
    if livros_disponiveis and usuarios:
        livro_escolhido = st.selectbox("Escolha o livro", livros_disponiveis, format_func=lambda x: x[1])
        usuario_escolhido = st.selectbox("Escolha o usuário", usuarios, format_func=lambda x: x[1])
        prazo = st.date_input("Prazo de devolução")

        if st.button("Emprestar"):
            emprestar_livro(livro_escolhido[0], usuario_escolhido[0], prazo)
            st.success("Livro emprestado com sucesso!")
    else:
        st.warning("Não há livros disponíveis ou usuários cadastrados.")

    st.subheader("📦 Devolver Livro")
    emprestados = status_livros()
    if emprestados:
        livro_para_devolver = st.selectbox("Escolha o livro para devolver", emprestados, format_func=lambda x: x[0])

        if st.button("Devolver"):
            devolver_livro(livro_para_devolver[0])
            st.success("Livro devolvido com sucesso!")
    else:
        st.info("Nenhum livro emprestado no momento.")

# Página 4: Status dos Livros
elif pagina == "Status dos Livros":
    st.title("📊 Status dos Livros")
    status = status_livros()

    st.subheader("🔍 Filtros")
    filtro_nome = st.text_input("Filtrar por nome do usuário")
    filtro_livro = st.text_input("Filtrar por título do livro")

    status_filtrado = [s for s in status if filtro_nome.lower() in s[1].lower() and filtro_livro.lower() in s[0].lower()]

    st.write("### 📋 Livros Emprestados")
    if status_filtrado:
        st.table(status_filtrado)
    else:
        st.info("Nenhum empréstimo encontrado com esses filtros.")
