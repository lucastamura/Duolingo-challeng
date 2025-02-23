from database_manager import connect_database, create_database
from data_users_manager import get_users, sing_up_user, convert_datas, check_evoluction_day
from duolingo_api import get_user_datas
from score_calculator import score_calculator
import os
from dotenv import load_dotenv
from pymongo import MongoClient


def update_datas():
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

        player = sing_up_user(row, db_jogadores)
        json_datas = get_user_datas(row['userId'])
        df_user = convert_datas(json_datas)
        check_evoluction_day(df_user['current_time'][0], df_user['id'][0], df_user['totalXp'][0], df_user['streak'][0], db_evolucao)
        score_calculator(conn, cursor, row['userId'], df_user['totalXp'][0], df_user['streak'][0], db_evolucao, db_jogadores)
        
    # cursor.execute(f"""SELECT * FROM players""")
    # result = cursor.fetchall()
    # print(result)
    
