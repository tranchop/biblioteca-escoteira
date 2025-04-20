import streamlit as st
from database import (
    criar_tabela, adicionar_livro, listar_livros,
    adicionar_usuario, listar_usuarios,
    registrar_emprestimo, registrar_devolucao,
    listar_emprestimos
)
from datetime import datetime, timedelta

criar_tabela()

st.title("📚 Sistema da Biblioteca Escoteira")

menu = ["Cadastrar Livro", "Cadastrar Usuário", "Registrar Empréstimo", "Registrar Devolução", "Visualizar Empréstimos"]
escolha = st.sidebar.selectbox("Menu", menu)

if escolha == "Cadastrar Livro":
    st.header("Cadastrar Livro")
    titulo = st.text_input("Título")
    autor = st.text_input("Autor")
    ano = st.number_input("Ano", min_value=0, max_value=2100, step=1)

    if st.button("Salvar"):
        if titulo and autor and ano:
            adicionar_livro(titulo, autor, ano)
            st.success("Livro cadastrado com sucesso!")
        else:
            st.error("Preencha todos os campos.")

elif escolha == "Cadastrar Usuário":
    st.header("Cadastrar Usuário")
    nome = st.text_input("Nome")

    if st.button("Salvar"):
        if nome:
            adicionar_usuario(nome)
            st.success("Usuário cadastrado com sucesso!")
        else:
            st.error("Digite um nome.")

elif escolha == "Registrar Empréstimo":
    st.header("Registrar Empréstimo")
    livros = listar_livros()
    usuarios = listar_usuarios()

    if livros and usuarios:
        livro_opcao = st.selectbox("Escolha o livro", livros, format_func=lambda x: x[1])
        usuario_opcao = st.selectbox("Escolha o usuário", usuarios, format_func=lambda x: x[1])
        prazo = st.number_input("Prazo de devolução (dias)", min_value=1, max_value=60, value=7)

        if st.button("Emprestar"):
            registrar_emprestimo(livro_opcao[0], usuario_opcao[0], prazo)
            st.success(f"Livro '{livro_opcao[1]}' emprestado para {usuario_opcao[1]} por {prazo} dias!")
    else:
        st.info("Cadastre livros e usuários primeiro.")

elif escolha == "Registrar Devolução":
    st.header("Registrar Devolução")
    emprestimos = listar_emprestimos()

    if emprestimos:
        emprestimo_opcao = st.selectbox("Selecione o empréstimo", emprestimos,
            format_func=lambda x: f"{x[1]} - {x[2]} ({x[3]})")

        if st.button("Registrar Devolução"):
            registrar_devolucao(emprestimo_opcao[0])
            st.success("Devolução registrada com sucesso!")
    else:
        st.info("Nenhum empréstimo pendente.")

elif escolha == "Visualizar Empréstimos":
    st.header("Todos os Empréstimos")
    emprestimos = listar_emprestimos(pendentes=False)

    if emprestimos:
        for emp in emprestimos:
            data_emprestimo = datetime.strptime(emp[3], "%Y-%m-%d")
            data_limite = data_emprestimo + timedelta(days=emp[5])
            status = (
                f"⏳ Pendente até {data_limite.strftime('%d/%m/%Y')}"
                if emp[4] is None else f"✅ Devolvido em {emp[4]}"
            )
            st.write(f"📘 {emp[1]} - {emp[2]} ({emp[3]}) → {status}")
    else:
        st.info("Nenhum empréstimo registrado.")
