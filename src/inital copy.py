from database_manager import connect_database, create_database
from data_users_manager import get_users, sing_up_user, convert_datas, check_evoluction_day
from duolingo_api import get_user_datas
from score_calculator import score_calculator
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Carregar variáveis de ambiente
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Conectar ao MongoDB
client = MongoClient(MONGO_URI)
db = client["duolingo"]
db_jogadores = db["jogadores"]
db_evolucao = db["evolucao_diaria"]

conn, cursor = connect_database('assets/database/database.db')
create_database(conn, cursor)
users = get_users()

for index, row in users.iterrows():
    row_dict = row.to_dict()  # 🔹 Converte o Pandas Series para um dicionário
    player = db_jogadores.find_one({"username": row_dict['username']})  
    if player is not None:
        print("Jogador já existe")
        print(player)
    else:
        result = db_jogadores.insert_one(row_dict)  # 🔹 Insere o dicionário no MongoDB
        print(result)  # Mostra o ID do novo documento



    
    
    sing_up_user(cursor, conn, row['userId'], row['username'], row['displayName'], row['totalXp'], row['streak'])
    # json_datas = get_user_datas(row['userId'])
    # df_user = convert_datas(json_datas)
    # check_evoluction_day(cursor, conn, df_user['current_time'][0], df_user['id'][0], df_user['totalXp'][0], df_user['streak'][0])
    # score_calculator(conn, cursor, row['userId'], df_user['totalXp'][0], df_user['streak'][0])
    
# cursor.execute(f"""SELECT * FROM players""")
# result = cursor.fetchall()
# print(result)
    
