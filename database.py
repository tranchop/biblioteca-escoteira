import sqlite3
from datetime import datetime

# Conexão com o banco de dados
def conectar():
    return sqlite3.connect("biblioteca.db")

# Cria as tabelas caso não existam
def criar_tabelas():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT,
            status TEXT DEFAULT 'disponível',
            descricao TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            celular TEXT,
            observacoes TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro_id INTEGER,
            usuario_id INTEGER,
            data_emprestimo TEXT,
            prazo INTEGER,
            FOREIGN KEY(livro_id) REFERENCES livros(id),
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro_id INTEGER,
            usuario_id INTEGER,
            data_emprestimo TEXT,
            data_devolucao TEXT,
            FOREIGN KEY(livro_id) REFERENCES livros(id),
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    conn.close()

# ----- CRUD de Livros -----
def adicionar_livro(titulo, autor, descricao):
    conn = conectar()
    c = conn.cursor()
    c.execute(
        "INSERT INTO livros (titulo, autor, descricao) VALUES (?, ?, ?)",
        (titulo, autor, descricao)
    )
    conn.commit()
    conn.close()

def listar_livros():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT id, titulo, autor, status, descricao FROM livros")
    livros = c.fetchall()
    conn.close()
    return livros

# Filtra livros pelo status ('disponível' ou 'emprestado')
def filtrar_livros_por_status(status):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT id, titulo, autor, status, descricao FROM livros WHERE status = ?", (status,))
    livros = c.fetchall()
    conn.close()
    return livros

# ----- CRUD de Usuários -----
def adicionar_usuario(nome, celular, observacoes):
    conn = conectar()
    c = conn.cursor()
    c.execute(
        "INSERT INTO usuarios (nome, celular, observacoes) VALUES (?, ?, ?)",
        (nome, celular, observacoes)
    )
    conn.commit()
    conn.close()

def listar_usuarios():
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT id, nome, celular, observacoes FROM usuarios")
    usuarios = c.fetchall()
    conn.close()
    return usuarios

# ----- Empréstimos -----
def emprestar_livro(livro_id, usuario_id, prazo):
    conn = conectar()
    c = conn.cursor()
    data_emprestimo = datetime.now().strftime("%Y-%m-%d")
    c.execute(
        "INSERT INTO emprestimos (livro_id, usuario_id, data_emprestimo, prazo) VALUES (?, ?, ?, ?)",
        (livro_id, usuario_id, data_emprestimo, prazo)
    )
    c.execute("UPDATE livros SET status='emprestado' WHERE id = ?", (livro_id,))
    conn.commit()
    conn.close()

# Retorna lista de empréstimos ativos
def listar_emprestimos():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        SELECT e.livro_id, l.titulo, u.nome, e.data_emprestimo, e.prazo
        FROM emprestimos e
        JOIN livros l ON e.livro_id = l.id
        JOIN usuarios u ON e.usuario_id = u.id
    ''')
    emprestimos = c.fetchall()
    conn.close()
    return emprestimos

# Devolve livro e registra no histórico
def devolver_livro(livro_id):
    conn = conectar()
    c = conn.cursor()
    # Busca empréstimo
    c.execute("SELECT usuario_id, data_emprestimo FROM emprestimos WHERE livro_id = ?", (livro_id,))
    row = c.fetchone()
    if row:
        usuario_id, data_emprestimo = row
        data_devolucao = datetime.now().strftime("%Y-%m-%d")
        # Insere histórico
        c.execute(
            "INSERT INTO historico (livro_id, usuario_id, data_emprestimo, data_devolucao) VALUES (?, ?, ?, ?)",
            (livro_id, usuario_id, data_emprestimo, data_devolucao)
        )
        # Remove empréstimo
        c.execute("DELETE FROM emprestimos WHERE livro_id = ?", (livro_id,))
        # Atualiza status do livro
        c.execute("UPDATE livros SET status='disponível' WHERE id = ?", (livro_id,))
        conn.commit()
    conn.close()

# Histórico completo de empréstimos
def listar_historico():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        SELECT l.titulo, u.nome, h.data_emprestimo, h.data_devolucao
        FROM historico h
        JOIN livros l ON h.livro_id = l.id
        JOIN usuarios u ON h.usuario_id = u.id
        ORDER BY h.data_devolucao DESC
    ''')
    historico = c.fetchall()
    conn.close()
    return historico