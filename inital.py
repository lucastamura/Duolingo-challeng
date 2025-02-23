from database_manager import connect_database, create_database
from data_users_manager import get_users, sing_up_user, convert_datas, check_evoluction_day
from duolingo_api import get_user_datas
from score_calculator import score_calculator
import time
from fastapi import FastAPI
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import concurrent.futures




# # Carregar variáveis de ambiente
# load_dotenv()
# MONGO_URI = os.getenv("MONGO_URI")

# # Conectar ao MongoDB
# client = MongoClient(MONGO_URI)
# db = client["duolingo"]
# db_jogadores = db["jogadores"]
# db_evolucao = db["evolucao_diaria.score_evolution"]



# conn, cursor = connect_database('assets/database/database.db')
# create_database(conn, cursor)

async def update_datas(db_jogadores, db_evolucao):
    users = get_users()

    # for index, row in users.iterrows():
    #     print('rodou')
    #     player = sing_up_user(row, db_jogadores)
    #     json_datas = get_user_datas(row['userId'])
    #     df_user = convert_datas(json_datas)
    #     check_evoluction_day(df_user['current_time'][0], df_user['id'][0], df_user['totalXp'][0], df_user['streak'][0], db_evolucao)
    #     score_calculator(conn, cursor, row['userId'], df_user['totalXp'][0], df_user['streak'][0], db_evolucao, db_jogadores)


    def process_user(row):
        """ Função para processar um único usuário """
        print(f'Rodando para {row["userId"]}')
        
        player = sing_up_user(row, db_jogadores)
        json_datas = get_user_datas(row['userId'])  # Coleta os dados da API simultaneamente
        df_user = convert_datas(json_datas)

        check_evoluction_day(
            df_user['current_time'][0], 
            df_user['id'][0], 
            df_user['totalXp'][0], 
            df_user['streak'][0], 
            db_evolucao
        )

        score_calculator(
            row['userId'], 
            df_user['totalXp'][0], 
            df_user['streak'][0], 
            db_evolucao, db_jogadores
        )

    # Usa ThreadPoolExecutor para rodar em paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(process_user, [row for _, row in users.iterrows()])


# while True:
#     # esperar 5 minutos
#     time.sleep(120)
#     update_datas(db_jogadores, db_evolucao)  # Espera a atualização terminar antes de continuar
