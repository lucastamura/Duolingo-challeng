let carregando = false; // Variável para evitar múltiplas requisições
async function carregarJogadores() {
    try {
        let response = await fetch("http://127.0.0.1:8000/evolucao", {
        // let response = await fetch("http://127.0.0.1:8000/jogadores", {
            method: "GET"
        });
        let data = await response.json();
        let tabela = document.getElementById("tabela-jogadores");
        let loading = document.getElementById("loading");


        tabela.innerHTML = ""; // Limpa a tabela antes de adicionar novos dados
        console.log(data);
        data.evolucao.forEach(evolucao => {
            let linha = document.createElement("tr");
            linha.innerHTML = `
                <td class="left flex_col al_center js_between full_w">
                    <div class="title flex full_w al_center js_between">
                        <div class=" flex al_center">

                            <span>${evolucao.posicao}</span>
                            <h5 class="username">${evolucao.username}</h5>
                        </div>
                        <h5 class="xpscore">${evolucao.totalScore} DP</h5>
                    </div>
                    <div class="options_card flex al_center js_between full_w">
                        <div class="text flex al_center">
                            <img class='avatar_img' src="../assets/avatar/${evolucao.userId}.png" alt="D">
                            <div class="name_points">
                                <p>
                                    XP Diário
                                </p>
                                <p>
                                    Pontos XP
                                </p>
                                <p>
                                    Pontos Ofensiva
                                </p>
                            </div>
                        </div>
                        <div class="points">
                            <p>${evolucao.acumuladoXp} XP</p>
                            <p>${evolucao.xpScore} DP</p>
                            <p>${evolucao.streakerScore} DP</p>
                        </div>
                    </div>
                </td>
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