from get_datas import get_user_datas
import csv
import pandas as pd
from datetime import datetime

def collet_convert_datas():
    # Listas para armazenar os dados de todos os usuários e cursos
    all_users_data = []
    all_courses_data = []

    # Ler o arquivo CSV de usuários
    with open('assets/database/users.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = row['userId']
            # Obter os dados do usuário
            data = get_user_datas(user_id)

            # Data e hora atual
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Adicionar os dados do usuário à lista
            user_data = {
                "id": data["id"],
                "name": data["name"],
                "username": data["username"],
                "totalXp": data["totalXp"],
                "streak": data["streak"],
                "creationDate": data["creationDate"],
                "hasPlus": data["hasPlus"],
                "fromLanguage": data["fromLanguage"],
                "learningLanguage": data["learningLanguage"],
                "subscriberLevel": data["subscriberLevel"],
                "current_time": current_time
            }
            all_users_data.append(user_data)

            # Adicionar os dados dos cursos à lista
            for course in data["courses"]:
                course_data = {
                    "user_id": data["id"],
                    "course_id": course["id"],
                    "title": course["title"],
                    "learningLanguage": course["learningLanguage"],
                    "fromLanguage": course["fromLanguage"],
                    "xp": course["xp"],
                    "crowns": course["crowns"],
                    "healthEnabled": course["healthEnabled"],
                    "preload": course["preload"],
                    "placementTestAvailable": course["placementTestAvailable"],
                    "authorId": course["authorId"],
                    "current_time": current_time
                }
                all_courses_data.append(course_data)

    # Criar DataFrames a partir das listas
    df_users = pd.DataFrame(all_users_data)
    df_courses = pd.DataFrame(all_courses_data)

    # Salvar os DataFrames em arquivos CSV
    df_users.to_csv("assets/database/users_datas.csv", index=False)
    df_courses.to_csv("assets/database/courses.csv", index=False)

    print("Arquivos CSV atualizados com sucesso!")