import json
import csv

# Carregar o JSON do arquivo
with open("assets/json/users.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Definir os campos desejados na ordem correta
fields = ["displayName", "userId", "username", "totalXp"]

# Criar e escrever no arquivo CSV
with open("assets/database/duolingo_following.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    
    # Escrevendo o cabeçalho
    writer.writerow(fields)

    # Escrevendo os dados dos usuários
    for user in data["following"]["users"]:
        writer.writerow([user.get(field, "") for field in fields])

print("Arquivo CSV gerado com sucesso: duolingo_following.csv")
