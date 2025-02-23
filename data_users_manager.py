import pandas as pd

def get_users():
    with open('assets/database/users.csv', 'r') as file:
        # Carregar os dados do CSV
        data = pd.read_csv('assets/database/users.csv')
        data = pd.DataFrame(data)
        return data

def sing_up_user(row, db_jogadores):
    row_dict = row.to_dict()  # 🔹 Converte o Pandas Series para um dicionário
    player = db_jogadores.find_one({"userId": row_dict['userId']})  
    if player is not None:
        return player
    else:
        result = db_jogadores.insert_one(row_dict)  # 🔹 Insere o dicionário no MongoDB
        return result  # Mostra o ID do novo documento
        
        
import csv
import pandas as pd
from datetime import datetime

def convert_datas(json_datas):
    # Listas para armazenar os dados de todos os usuários e cursos
    all_users_data = []
    all_courses_data = []

    data = json_datas

    # Data e hora atual
    current_time = datetime.now().strftime("%Y-%m-%d")
    # current_time = '2025-02-23'

    # Adicionar os dados do usuário à lista
    user_data = {
        "id": data["id"],
        "name": data["name"],
        "username": data["username"],
        # "totalXp": 1800,
        # "streak": 3,
        "totalXp": data["totalXp"],
        "streak": data["streak"],
        "creationDate": data["creationDate"],
        "hasPlus": data["hasPlus"],
        "fromLanguage": data["fromLanguage"],
        "learningLanguage": data["learningLanguage"],
        "subscriberLevel": data["subscriberLevel"],
        "current_time": current_time
    }
    # Criar DataFrames a partir das listas
    df_users = pd.DataFrame(user_data, index=[0])

    # Salvar os DataFrames em arquivos CSV
    df_users.to_csv("assets/database/users_datas.csv", index=False)
    return df_users

def check_evoluction_day(current_time, userId, totalXp, streak, db_evolucao):
    result = db_evolucao.score_evolution.find_one({"date": current_time, "userId": int(userId)})
    if result is None:
        data = {
            "userId": int(userId),  # Certifique-se de converter para int, se necessário
            "date": current_time,  # Certifique-se de estar no formato correto (ex: "YYYY-MM-DD")
            "xpDay": int(totalXp),
            "streakerDia": int(streak),
            "xpScore": 0,
            "streakerScore": 0,
            "totalScore": 0
        }

        db_evolucao.score_evolution.insert_one(data)
    # else:
