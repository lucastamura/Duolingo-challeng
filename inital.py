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



async def update_datas(db_jogadores, db_evolucao):
    users = get_users()

    def process_user(row):
        """ Função para processar um único usuário """
        
        player = sing_up_user(row, db_jogadores)
        json_datas = get_user_datas(row['userId'])  # Coleta os dados da API simultaneamente
        df_user = convert_datas(json_datas)

        check_evoluction_day(
            df_user['current_time'][0], 
            df_user['id'][0], 
            df_user['totalXp'][0], 
            df_user['streak'][0], 
            db_evolucao,
            df_user['name'][0],
            
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
    
    
    # for _, row in users.iterrows():
    #     process_user(row)
