import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from database import (
    criar_tabelas, adicionar_livro, listar_livros,
    filtrar_livros_por_status, adicionar_usuario, listar_usuarios,
    emprestar_livro, listar_emprestimos, devolver_livro,
    listar_historico
)

# Inicialização
st.set_page_config(page_title="Biblioteca Escoteira", layout="wide")
criar_tabelas()
st.title("📚 Sistema Biblioteca Escoteira")

# Menu lateral
menu = st.sidebar.selectbox(
    "Menu", ["Livros", "Usuários", "Empréstimos", "Histórico", "Estatísticas"]
)

if menu == "Livros":
    st.header("📔 Livros Cadastrados")
    livros = listar_livros()
    df_livros = pd.DataFrame(livros, columns=["ID", "Título", "Autor", "Status", "Descrição"])
    st.dataframe(df_livros)

    st.subheader("Adicionar Novo Livro")
    titulo = st.text_input("Título", key="livro_titulo")
    autor = st.text_input("Autor", key="livro_autor")
    descricao = st.text_area("Descrição", key="livro_desc")
    if st.button("Adicionar Livro"):
        if titulo and autor:
            adicionar_livro(titulo, autor, descricao)
            st.experimental_rerun()
        else:
            st.error("Preencha título e autor.")

elif menu == "Usuários":
    st.header("👤 Usuários Cadastrados")
    usuarios = listar_usuarios()
    df_usuarios = pd.DataFrame(usuarios, columns=["ID", "Nome", "Celular", "Observações"])
    st.dataframe(df_usuarios)

    st.subheader("Adicionar Novo Usuário")
    nome = st.text_input("Nome", key="user_nome")
    celular = st.text_input("Celular", key="user_celular")
    observacoes = st.text_area("Observações", key="user_obs")
    if st.button("Adicionar Usuário"):
        if nome:
            adicionar_usuario(nome, celular, observacoes)
            st.experimental_rerun()
        else:
            st.error("Preencha o nome.")

elif menu == "Empréstimos":
    st.header("🔄 Gerenciar Empréstimos")
    status = st.selectbox("Filtrar status dos livros", ["Disponível", "Emprestado"])
    livros_disp = filtrar_livros_por_status(status)
    df_disp = pd.DataFrame(livros_disp, columns=["ID", "Título", "Autor", "Status", "Descrição"])
    st.write(df_disp)

    st.subheader("Novo Empréstimo")
    if not df_disp.empty:
        sel_livro = st.selectbox("Livro", df_disp['Título'])
        sel_usuario = st.selectbox("Usuário", [u[1] for u in listar_usuarios()])
        prazo = st.slider("Prazo (dias)", 1, 30, 7)
        if st.button("Emprestar Livro"):
            livro_id = int(df_disp[df_disp['Título'] == sel_livro]['ID'].iloc[0])
            usuario_id = int([u[0] for u in listar_usuarios() if u[1] == sel_usuario][0])
            emprestar_livro(livro_id, usuario_id, prazo)
            st.success("Empréstimo registrado!")
            st.experimental_rerun()
    else:
        st.info("Nenhum livro disponível para empréstimo.")

elif menu == "Histórico":
    st.header("📜 Histórico de Empréstimos")
    hist = listar_historico()
    df_hist = pd.DataFrame(hist, columns=["Título", "Usuário", "Data Empréstimo", "Data Devolução"])
    st.dataframe(df_hist)

elif menu == "Estatísticas":
    st.header("📊 Estatísticas de Livros")
    df_livros = pd.DataFrame(listar_livros(), columns=["ID", "Título", "Autor", "Status", "Descrição"])
    if not df_livros.empty:
        # Pizza de status
        fig1 = px.pie(df_livros, names='Status', title='Distribuição de Status')
        st.plotly_chart(fig1)
        # Barra de autores
        top_autores = df_livros['Autor'].value_counts().nlargest(10).reset_index()
        top_autores.columns = ['Autor', 'Quantidade']
        fig2 = px.bar(top_autores, x='Autor', y='Quantidade', title='Top 10 Autores')
        st.plotly_chart(fig2)
    else:
        st.info("Nenhum livro cadastrado para gerar estatísticas.")