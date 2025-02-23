import pandas as pd

def get_users():
    with open('assets/database/users.csv', 'r') as file:
        # Carregar os dados do CSV
        data = pd.read_csv('assets/database/users.csv')
        data = pd.DataFrame(data)
        return data

def sing_up_user(cursor, conn, userId, username, name, startXp, streak):
    cursor.execute(f""" SELECT * FROM players WHERE username = '{username}' """)
    result = cursor.fetchall()
    if result == []:
        cursor.execute(f"""
        INSERT INTO players (id, username, name, startXp, startStreak)
        VALUES ({userId}, '{username}', '{name}', {startXp}, {streak});
        """)
        conn.commit()
    else:
        print(f'Usuário {name} já cadastrado')
        
        
import csv
import pandas as pd
from datetime import datetime

def convert_datas(json_datas):
    # Listas para armazenar os dados de todos os usuários e cursos
    all_users_data = []
    all_courses_data = []

    data = json_datas

    # Data e hora atual
    # current_time = datetime.now().strftime("%Y-%m-%d")
    current_time = '2025-02-23'

    # Adicionar os dados do usuário à lista
    user_data = {
        "id": data["id"],
        "name": data["name"],
        "username": data["username"],
        "totalXp": 5000,
        "streak": 3,
        # "totalXp": data["totalXp"],
        # "streak": data["streak"],
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

def check_evoluction_day(cursor, conn, current_time, userId, totalXp, streak):
    cursor.execute(f"""SELECT * FROM score_evolution WHERE date = '{current_time}' AND userId = {userId}""")
    if cursor.fetchone() is None:
        cursor.execute(f"""INSERT INTO score_evolution (userId, date, xpDay, streakerDia) VALUES ({userId}, '{current_time}', {totalXp}, {streak})""")
        conn.commit()
    else:
        print('Registro de evolução já criado para o dia de hoje')
