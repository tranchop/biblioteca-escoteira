import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect("biblioteca.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro_id INTEGER NOT NULL,
            usuario_id INTEGER NOT NULL,
            data_emprestimo TEXT NOT NULL,
            prazo_dias INTEGER NOT NULL,
            data_devolucao TEXT,
            FOREIGN KEY (livro_id) REFERENCES livros(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        );
    """)

    conn.commit()
    conn.close()

def adicionar_livro(titulo, autor, ano):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO livros (titulo, autor, ano) VALUES (?, ?, ?)", (titulo, autor, ano))
    conn.commit()
    conn.close()

def listar_livros():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livros")
    livros = cursor.fetchall()
    conn.close()
    return livros

def adicionar_usuario(nome):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome) VALUES (?)", (nome,))
    conn.commit()
    conn.close()

def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def registrar_emprestimo(livro_id, usuario_id, prazo_dias):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO emprestimos (livro_id, usuario_id, data_emprestimo, prazo_dias)
        VALUES (?, ?, ?, ?)
    """, (livro_id, usuario_id, datetime.now().strftime("%Y-%m-%d"), prazo_dias))
    conn.commit()
    conn.close()

def registrar_devolucao(emprestimo_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE emprestimos SET data_devolucao = ?
        WHERE id = ?
    """, (datetime.now().strftime("%Y-%m-%d"), emprestimo_id))
    conn.commit()
    conn.close()

def listar_emprestimos(pendentes=True):
    conn = conectar()
    cursor = conn.cursor()
    if pendentes:
        cursor.execute("""
            SELECT e.id, l.titulo, u.nome, e.data_emprestimo, e.data_devolucao, e.prazo_dias
            FROM emprestimos e
            JOIN livros l ON e.livro_id = l.id
            JOIN usuarios u ON e.usuario_id = u.id
            WHERE e.data_devolucao IS NULL
        """)
    else:
        cursor.execute("""
            SELECT e.id, l.titulo, u.nome, e.data_emprestimo, e.data_devolucao, e.prazo_dias
            FROM emprestimos e
            JOIN livros l ON e.livro_id = l.id
            JOIN usuarios u ON e.usuario_id = u.id
        """)
    emprestimos = cursor.fetchall()
    conn.close()
    return emprestimos
