import pandas as pd
from IPython.display import HTML, display
import base64
import os

def generate_html():
    

    # Ler o arquivo CSV
    df = pd.read_csv('historical_datas/database/dados_com_diff.csv')

    # Ordenar pelo totalXp em ordem decrescente
    df = df.sort_values(by='totalXp', ascending=False)


    # Função para codificar a imagem em base64
    def encode_image_to_base64(image_path):
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        return None
    medalhas = ['🥇', '🥈', '🥉']

    # Codificar as imagens dos avatares em base64
    df['Avatar'] = [f"data:image/png;base64,{encode_image_to_base64(f'avatar/{username}.png')}" for username in df['username']]
    df['Posição'] = [medalhas[i] if i < 3 else f"{i+1}º" for i in range(len(df))]


    # Criar a tabela HTML
    html = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

            * {
                font-family: 'Poppins', sans-serif;
                color: #F1F7FB;
            }
            body{
                background-color: #131F24;
                display: flex;
                justify-content: center;
            }
            img{
                width: 50px;
                border-radius: 120px;
            }
            tr{
                height: 70px;
                width: 500px;
                justify-content: space-between;
                display: flex;
                align-items: center;
                border-radius: 18px;
                margin-bottom: 4px;
                transition: 0.3s;
            }
            tr:hover{
                background-color: #202F36;
            }

            .container{
                width: 500px;
            }
            span{
                width: 50px;
                height: 50px;
                margin-right: 10px;
                font-size: 24px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .left{
                display: flex;
                align-items: center;
            }
            .username{
                margin-left: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                font-weight: 500;
            }
            .xpscore{
                font-size: 16px;
                font-weight: 500;
                margin-right: 8px;
            }
            h1, h3{
                width: 100%;
                text-align: center;
            }


        </style>
        <div class="container">

            <div class="title">
                <h1>Intensiva DITIE</h1>
                <p>Pronto para a maratona de XP no Duolingo? Em 3 meses, é hora de virar um mestre dos idiomas, acumular
                    pontos como um viciado em lições e deixar seus amigos pra trás! Quem vai ser o rei ou a rainha do XP?
                    Bora aprender e competir! 🏆✨</p>
                <div>
                    <h3>Hanking Geral</h3>
                    <table>
    """

    # Adicionar as linhas da tabela
    for _, row in df.iterrows():
        html += f"""

        <tr>
            <td class="left">
                <span>{row['Posição']}</span>
                <img src="avatar/{row['username']}.png" alt="{row['username']}">
                <h5 class="username">{row['displayName']}</h5>
            </td>
            <td class="xpscore">{row['totalXp']} XP</td>
        </tr>
        """

    html += """
                    </table>
                </div>
            </div>
        </div>
    """

    # Exibir a tabela no Jupyter Notebook
    display(HTML(html))

    # Salvar a tabela em um arquivo HTML
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)