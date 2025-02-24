let carregando = false; // Variável para evitar múltiplas requisições
async function carregarJogadores() {
    try {
        let response = await fetch("https://duolingo-challeng.onrender.com/jogadores", {
        // let response = await fetch("http://127.0.0.1:8000/jogadores", {
            method: "GET"
        });
        let data = await response.json();
        let tabela = document.getElementById("tabela-jogadores");
        let loading = document.getElementById("loading");


        tabela.innerHTML = ""; // Limpa a tabela antes de adicionar novos dados
        console.log(data);
        data.jogadores.forEach(jogador => {
            let linha = document.createElement("tr");
            linha.innerHTML = `
                <tr>
                    <td class="left">
                        <span>${jogador.posicao}</span>
                        <img class='avatar_img' src="../assets/avatar/${jogador.userId}.png" alt="D">
                        <h5 class="username">${jogador.displayName}</h5>
                    </td>
                    <td class="xpscore">${jogador.totalScore} DP</td>
                </tr>
            `;
            tabela.appendChild(linha);
        });
    } catch (error) {
        console.error("Erro ao carregar jogadores:", error);
    }
    loading.style.display = "none"; // Esconde o loading
    carregando = false; // Libera a variável após a requisição

}

carregarJogadores();