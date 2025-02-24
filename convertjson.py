# import json
# import csv

# # Carregar o JSON do arquivo
# with open("assets/json/users.json", "r", encoding="utf-8") as file:
#     data = json.load(file)

# # Definir os campos desejados na ordem correta
# fields = ["displayName", "userId", "username", "totalXp"]

# # Ordenar os usuários pelo userId
# sorted_users = sorted(data["following"]["users"], key=lambda x: x.get("userId", 0))

# # Criar e escrever no arquivo CSV
# with open("assets/database/duolingo_following.csv", "w", newline="", encoding="utf-8") as csvfile:
#     writer = csv.writer(csvfile)
    
#     # Escrevendo o cabeçalho
#     writer.writerow(fields)
    
#     # Escrevendo os dados ordenados
#     for user in sorted_users:
#         writer.writerow([user.get(field, "") for field in fields])

# print("CSV gerado com sucesso, ordenado por userId!")


import csv
import json
import os

# Caminhos dos diretórios
csv_path = "assets/database/duolingo_following.csv"
json_dir = "assets/json/"

# Ler o CSV e armazenar os dados em uma lista
with open(csv_path, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    users = list(reader)

# Atualizar o campo streakStart com os valores dos JSONs
for user in users:
    user_id = user["userId"]
    json_file = os.path.join(json_dir, f"{user_id}.json")

    if os.path.exists(json_file):  # Verifica se o JSON existe
        with open(json_file, "r", encoding="latin-1") as jsonfile:
            data = json.load(jsonfile)
            user["streakStart"] = data.get("streak", user["streakStart"])  
            user["totalXp"] = data.get("totalXp", user["totalXp"])  

# Escrever os dados de volta para o CSV atualizado
with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = users[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    writer.writerows(users)

print("CSV atualizado com sucesso!")
