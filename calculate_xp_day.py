import pandas as pd

def calculate_xp():
    
    # Ler o arquivo CSV
    df = pd.read_csv('historical_datas/database/users_data.csv')

    # Ordenar os dados por username e date
    df = df.sort_values(by=['username', 'date'])

    # Calcular o totalXp inicial para cada username
    df['initial_totalXp'] = df.groupby('username')['totalXp'].transform('first')

    # Calcular a diferença entre o totalXp atual e o inicial
    df['diff_totalXp'] = df['totalXp'] - df['initial_totalXp']

    # Remover a coluna auxiliar
    df = df.drop(columns=['initial_totalXp'])

    df = df.drop_duplicates(subset=['userId'], keep='last')
    # Visualizar o DataFrame resultante
    print(df)

    # Salvar o DataFrame em um novo arquivo CSV (opcional)
    df.to_csv('historical_datas/database/dados_com_diff.csv', index=False)