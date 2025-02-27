from datetime import datetime
from fastapi import FastAPI
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from inital import update_datas
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pymongo import MongoClient
import asyncio
import pytz





# Carregar variáveis de ambiente
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Conectar ao MongoDB
client = MongoClient(MONGO_URI)
db = client["duolingo"]
db_jogadores = db["jogadores"]
db_evolucao = db["evolucao_diaria"]

# Criar a API
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

@app.get("/evolucao")
def get_evolucao():
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    current_time = datetime.now(brasilia_tz).strftime("%Y-%m-%d")

    jogadores = list(db_evolucao.find({"date": current_time}, {"_id": 0}))  # Buscar todos os jogadores, excluindo o ID MongoDB
    jogadores.sort(key=lambda x: x["totalScore"], reverse=True)

    # Adiciona o campo de posição
    medals = ['🥇', '🥈', '🥉']
    for i, jogador in enumerate(jogadores, start=1):
        jogador["posicao"] = medals[i-1] if i <= 3 else f"{i}º"
    return {"evolucao": jogadores}


@app.get("/jogadores")
async def get_jogadores():
    await update_datas(db_jogadores, db_evolucao)  # Espera a atualização terminar antes de continuar
    jogadores = db_jogadores.find({}, {"_id": 0}).to_list(None) 
    # Ordena os jogadores pelo totalScore do maior para o menor
    jogadores.sort(key=lambda x: x["totalScore"], reverse=True)

    # Adiciona o campo de posição
    medals = ['🥇', '🥈', '🥉']
    for i, jogador in enumerate(jogadores, start=1):
        jogador["posicao"] = medals[i-1] if i <= 3 else f"{i}º"

    # Exibe o JSON atualizado
    return {"jogadores": jogadores}

