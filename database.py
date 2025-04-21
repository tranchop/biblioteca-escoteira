import sqlite3

def conectar():
    return sqlite3.connect('biblioteca.db')

def criar_tabelas():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            autor TEXT,
            status TEXT DEFAULT 'disponível',
            descricao TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            celular TEXT,
            observacoes TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livro INTEGER,
            id_usuario INTEGER,
            prazo TEXT,
            FOREIGN KEY(id_livro) REFERENCES livros(id),
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    conn.close()

criar_tabelas()

def adicionar_livro(titulo, autor, descricao):
    conn = conectar()
    c = conn.cursor()
    c.execute('INSERT INTO livros (titulo, autor, descricao) VALUES (?, ?, ?)', (titulo, autor, descricao))
    conn.commit()
    conn.close()

def adicionar_usuario(nome, celular, observacoes):
    conn = conectar()
    c = conn.cursor()
    c.execute('INSERT INTO usuarios (nome, celular, observacoes) VALUES (?, ?, ?)', (nome, celular, observacoes))
    conn.commit()
    conn.close()

def listar_livros():
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM livros')
    livros = c.fetchall()
    conn.close()
    return livros

def listar_usuarios():
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    usuarios = c.fetchall()
    conn.close()
    return usuarios

def emprestar_livro(id_livro, id_usuario, prazo):
    conn = conectar()
    c = conn.cursor()
    c.execute('UPDATE livros SET status = ? WHERE id = ?', ('emprestado', id_livro))
    c.execute('INSERT INTO emprestimos (id_livro, id_usuario, prazo) VALUES (?, ?, ?)', (id_livro, id_usuario, prazo))
    conn.commit()
    conn.close()

def devolver_livro(titulo_livro):
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT id FROM livros WHERE titulo = ?', (titulo_livro,))
    id_livro = c.fetchone()[0]
    c.execute('UPDATE livros SET status = ? WHERE id = ?', ('disponível', id_livro))
    c.execute('DELETE FROM emprestimos WHERE id_livro = ?', (id_livro,))
    conn.commit()
    conn.close()

def status_livros():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        SELECT livros.titulo, usuarios.nome, emprestimos.prazo
        FROM emprestimos
        JOIN livros ON emprestimos.id_livro = livros.id
        JOIN usuarios ON emprestimos.id_usuario = usuarios.id
        WHERE livros.status = 'emprestado'
    ''')
    status = c.fetchall()
    conn.close()
    return status