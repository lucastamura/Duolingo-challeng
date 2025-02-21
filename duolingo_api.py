import requests 
def get_user_datas(userId):

    # URL da API
    api_url = f"https://www.duolingo.com/2017-06-30/users/{userId}?fields=courses,creationDate,fromLanguage,gemsConfig,globalAmbassadorStatus,hasPlus,id,learningLanguage,location,name,picture,privacySettings,roles,streak,streakData%7BcurrentStreak,previousStreak%7D,subscriberLevel,totalXp,username&_=1739902538389"

    # Cabeçalhos necessários
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.duolingo.com/",
        "X-Requested-With": "XMLHttpRequest"
    }

    # Fazer a requisição à API
    response = requests.get(api_url, headers=headers)
    #Salvar reonse.json
    with open(f'assets/json/{userId}.json', 'w') as f:
        f.write(response.text)
    if response.status_code == 200:
        print("Dados coletados com sucesso!")
        return(response.json())  # Exibir os dados em formato JSON
    else:
        print(f"Erro na requisição: {response.status_code}")