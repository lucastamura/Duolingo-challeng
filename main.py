from fastapi import FastAPI
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from inital import update_datas
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pymongo import MongoClient
import asyncio




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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os headers
)
# # Rota para obter a pontuação dos jogadores
# @app.get("/jogadores")
# def get_jogadores():
#     update_datas()
#     jogadores = list(db_jogadores.find({}, {"_id": 0}))  # Buscar todos os jogadores, excluindo o ID MongoDB
#     return {"jogadores": jogadores}

# @app.get("/evolucao")
# def get_evolucao():
#     jogadores = list(db_evolucao.find({}, {"_id": 0}))  # Buscar todos os jogadores, excluindo o ID MongoDB
#     return {"jogadoresss": jogadores}

# # Rota para atualizar os pontos (exemplo de lógica de atualização)
# @app.post("/atualizar_pontos")
# def atualizar_pontos():
#     db_jogadores.insert_one({"username": "lucas.tamura", "name": "Lucas Tamura", "startXp": 1000, "startStreak": 3, "totalScore": 0})
#     return {"message": "Pontos atualizados com sucesso!"}




# async def update_datas():
#     # Simulando demora na atualização (remova essa linha no código real)
#     await asyncio.sleep(15)
#     # Aqui vai sua lógica de atualização real

@app.get("/jogadores")
async def get_jogadores():
    await update_datas(db_jogadores, db_evolucao)  # Espera a atualização terminar antes de continuar
    jogadores = db_jogadores.find({}, {"_id": 0}).to_list(None)  
    return {"jogadores": jogadores}

