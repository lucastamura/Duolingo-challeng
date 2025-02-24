import numpy as np
import pandas as pd

def score_calculator( userId, xpDayNew, streakDayNew, db_evolucao, db_jogadores):
    check, data = first_evolution_day(db_evolucao, userId)
    if check:
        pontos_xp, pontos_streak, pontos_total = calcular_primeiro_registro(userId, xpDayNew, streakDayNew, data[0]["xpDay"], data[0]["streakerDia"], db_jogadores)
    else:
        results = list(db_evolucao.find({"userId": userId}).sort("_id", -1).limit(2))

        # Verifica se há pelo menos dois registros
        if len(results) < 2:
            return None, None  # Retorna valores nulos se não houver registros suficientes

        xp_day_old = results[1]["xpDay"]
        streak_old = results[1]["streakerDia"]
        pontos_xp, pontos_streak, pontos_total = calcular_pontos(xp_day_old, xpDayNew, streak_old, streakDayNew)
        
    result = db_evolucao.find({"userId": userId}).sort("date", -1).limit(1)
    result = list(result)
    if result:  # Se existir algum registro
        old_score = result[0]["totalScore"]
        id_register = result[0]["_id"]  # MongoDB usa _id como identificador único
    else:
        old_score = 0
        id_register = None

    acumulado = xpDayNew - data[0]["xpDay"]
    
    if pontos_total != old_score:
        db_evolucao.update_one(
            {"_id": id_register},
            {"$set": {
                "xpScore": int(pontos_xp),
                "streakerScore": int(pontos_streak),
                "totalScore": int(pontos_total),
                "xpDay": int(xpDayNew),
                "streakerDia": int(streakDayNew),
                "acumuladoXp":int(acumulado)
            }}
        )

        # Calcula a soma de todos os 'totalScore' do usuário
        result = db_evolucao.aggregate([
            {"$match": {"userId": userId}},
            {"$group": {"_id": None, "totalScoreSum": {"$sum": "$totalScore"}}}
        ])

        # Obtém o valor total somado
        result = list(result)
        pontos_total = result[0]["totalScoreSum"] if result else 0

        # Atualiza o totalScore na coleção 'players'
        db_jogadores.update_one(
            {"userId": userId},
            {"$set": {"totalScore": int(pontos_total)}}
        )

    # else:
        



        
    
    
def first_evolution_day(db_evolucao, userId):
    # Verificar se o usuário já possui somente 1 registro de evolução
    result = list(db_evolucao.find({"userId": int(userId)}))
    if len(result) == 1:
        return True, result
    else:
        return False, result

    
    
def calcular_pontos(xpDayOld, XpDayNew, streakOld, streakNew):
    # Calcular pontosXp (usando log10)
    diferenca_xp = XpDayNew - xpDayOld
    if diferenca_xp > 0:
        pontos_xp = int(10 * np.log10(diferenca_xp))  # Log na base 10
    else:
        pontos_xp = 0  # Se a diferença for <= 0, pontosXp = 0
    # Calcular pontosOfensiva
    diferenca_streak = streakNew - streakOld
    if diferenca_streak > 0:
        # pontos_streak = diferenca_streak + streakOld 
        # pontos_streak = pontos_streak * 5
        pontos_streak = 5
    else:
        pontos_streak = 0
    
    pontos_total = pontos_xp + pontos_streak

    return pontos_xp, pontos_streak, pontos_total

def calcular_primeiro_registro(userId, xpDayNew, streakDayNew, xpOld, streakOld, db_jogadores):
    result = db_jogadores.find_one({"userId": int(userId)}, {"xpStart": 1, "streakStart": 1, "_id": 0})
    if result:
        xpOld = result.get("xpStart", None)
        streakOld = result.get("streakStart", None)
        return calcular_pontos(xpOld, xpDayNew, streakOld, streakDayNew)
    
    return None  # Retorna None se não encontrar o usuário