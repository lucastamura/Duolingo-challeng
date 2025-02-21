import sqlite3

def create_database(db_file):
    """
    Cria um banco de dados SQLite com uma tabela contendo as colunas especificadas.

    :param db_file: Caminho do arquivo de banco de dados (.db) a ser criado.
    """
    # Conectar ao banco de dados (ou criar se não existir)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query para criar a tabela
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        idRegister INTEGER PRIMARY KEY AUTOINCREMENT,
        id INTEGER,
        name TEXT,
        username TEXT,
        totalXp INTEGER,
        streak INTEGER,
        creationDate INTEGER,
        hasPlus BOOLEAN,
        fromLanguage TEXT,
        learningLanguage TEXT,
        subscriberLevel TEXT,
        current_time TEXT,
        pontosXp INTEGER,
        pontosOfensiva INTEGER,
        pontosTotal INTEGER
    );
    """

    # Executar a query para criar a tabela
    cursor.execute(create_table_query)

    # Commit para salvar as alterações
    conn.commit()

    # Fechar a conexão com o banco de dados
    conn.close()

    print(f"Banco de dados '{db_file}' criado com sucesso com a tabela 'users'.")
    
def insert_data(db_file, user_data):
    """
    Insere dados na tabela 'users' do banco de dados.

    :param db_file: Caminho do arquivo de banco de dados (.db).
    :param user_data: Dicionário contendo os dados do usuário.
    """
    # Conectar ao banco de dados
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Preparar a query de inserção
    columns = ', '.join(user_data.keys())
    placeholders = ', '.join(['?'] * len(user_data))
    query = f"INSERT INTO users ({columns}) VALUES ({placeholders})"

    # Executar a query com os valores do usuário
    cursor.execute(query, tuple(user_data.values()))

    # Commit para salvar as alterações
    conn.commit()

    # Fechar a conexão com o banco de dados
    conn.close()

    print("Dados inseridos com sucesso na tabela 'users'.")