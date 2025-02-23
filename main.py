from fastapi import FastAPI
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from inital import update_datas

# Carregar variáveis de ambiente
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Conectar ao MongoDB
client = MongoClient(MONGO_URI)
db = client["duolingo"]
db_jogadores = db["jogadores"]
db_evolucao = db["evolucao_diaria.score_evolution"]

# Criar a API
app = FastAPI()

# Rota para obter a pontuação dos jogadores
@app.get("/jogadores")
def get_jogadores():
    update_datas()
    jogadores = list(db_jogadores.find({}, {"_id": 0}))  # Buscar todos os jogadores, excluindo o ID MongoDB
    return {"jogadores": jogadores}

@app.get("/evolucao")
def get_evolucao():
    jogadores = list(db_evolucao.find({}, {"_id": 0}))  # Buscar todos os jogadores, excluindo o ID MongoDB
    return {"jogadoresss": jogadores}

# Rota para atualizar os pontos (exemplo de lógica de atualização)
@app.post("/atualizar_pontos")
def atualizar_pontos():
    db_jogadores.insert_one({"username": "lucas.tamura", "name": "Lucas Tamura", "startXp": 1000, "startStreak": 3, "totalScore": 0})
    return {"message": "Pontos atualizados com sucesso!"}
