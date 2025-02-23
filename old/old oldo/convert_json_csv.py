
import os
import json
import csv
from datetime import datetime

def convert_datas():
        
    # Diretório contendo os arquivos JSON
    directory = 'historical_datas/json/'

    # Arquivo CSV de saída
    output_csv = 'historical_datas/database/users_data.csv'

    # Lista para armazenar os dados dos usuários
    users_data = []

    # Iterar sobre cada arquivo no diretório
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            # Extrair a data do nome do arquivo
            date_str = filename.replace('.json', '')
            date = datetime.strptime(date_str, '%d_%m_%Y').date()
            
            # Ler o arquivo JSON com a codificação correta
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                data = json.load(file)
                users = data['following']['users']
                
                # Adicionar a data a cada usuário e adicionar à lista users_data
                for user in users:
                    user_data = {
                        'date': date,
                        'displayName': user['displayName'],
                        'totalXp': user['totalXp'],
                        'userId': user['userId'],
                        'username': user['username']
                    }
                    users_data.append(user_data)

    # Escrever os dados dos usuários no arquivo CSV com a codificação correta
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['date', 'displayName', 'totalXp', 'userId', 'username']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for user in users_data:
            writer.writerow(user)

