import numpy as np
import pandas as pd

def score_calculator(conn, cursor, userId, xpDayNew, streakDayNew):
    check, data = first_evolution_day(conn, cursor, userId)
    if check:
        pontos_xp, pontos_streak, pontos_total = calcular_primeiro_registro(cursor, userId, xpDayNew, streakDayNew, data[0][2], data[0][3])
    else:
        cursor.execute(f"""SELECT xpDay, streakerDia FROM score_evolution WHERE userId = {userId} ORDER BY id DESC LIMIT 2""")
        result = cursor.fetchall()
        xpDayOld = result[1][0]
        streakOld = result[1][1]
        pontos_xp, pontos_streak, pontos_total = calcular_pontos(xpDayOld, xpDayNew, streakOld, streakDayNew)
        
    cursor.execute(f"""SELECT totalScore, id FROM score_evolution WHERE userId = {userId} ORDER BY id DESC LIMIT 1""")
    result = cursor.fetchall()
    old_score = result[0][0]
    id_register = result[0][1]
    
    if pontos_total != old_score:
        # atualizar registros no banco
        cursor.execute(f"""UPDATE score_evolution SET xpScore = {pontos_xp}, streakerScore = {pontos_streak}, totalScore = {pontos_total}, xpDay = {xpDayNew}, streakerDia = {streakDayNew} WHERE id = {id_register}""")
        # Fazer uma select no banco trazendo a soma de todos os totalScore do usuário
        conn.commit()
        cursor.execute(f"""SELECT SUM(totalScore) FROM score_evolution WHERE userId = {userId}""")
        result = cursor.fetchall()
        pontos_total = result[0][0]
        cursor.execute(f"""UPDATE players SET totalScore = {pontos_total} WHERE id = {userId}""")
        conn.commit()
    # else:
    
        



        
    
    
def first_evolution_day(conn, cursor, userId):
    # Verificar se o usuário já possui somente 1 registro de evolução
    cursor.execute(f"""SELECT * FROM score_evolution WHERE userId = {userId}""")
    result = cursor.fetchall()
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

def calcular_primeiro_registro(cursor, userId, xpDayNew, streakDayNew, xpOld, streakOld):
    cursor.execute(f"""SELECT startXp, startStreak FROM players WHERE id = {userId}""")
    result = cursor.fetchall()
    xpOld = result[0][0]
    streakOld = result[0][1]
    return calcular_pontos(xpOld, xpDayNew, streakOld, streakDayNew)