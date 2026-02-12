fetch("/api/usuario/cartas-diarias")
.then(res => res.json())
.then(res => {

    const container = document.getElementById("cartas");
    const msg = document.getElementById("mensagem");

    // Caso já tenha pego as cartas
    if (!res.sucesso) {
        msg.innerText = res.mensagem || "As cartas diárias já foram coletadas.";
        return;
    }

    const cartas = res.cartas; // array com 5 cartas

    // ===== Mapa de cores por raridade =====
    const raridadeStyle = {
        "Comum": {
            carta: "linear-gradient(180deg, #f2f2f2, #d9d9d9)",
            stats: "rgba(120,120,120,0.15)",
            borda: "#8a8a8a"
        },
        "Bom": {
            carta: "linear-gradient(180deg, #e6f7ee, #bfe8d5)",
            stats: "rgba(0,168,107,0.15)",
            borda: "#00a86b"
        },
        "Ótimo": {
            carta: "linear-gradient(180deg, #e6f0ff, #c2d9ff)",
            stats: "rgba(44,123,229,0.15)",
            borda: "#2c7be5"
        },
        "Top": {
            carta: "linear-gradient(180deg, #f1e6ff, #d6c2ff)",
            stats: "rgba(120,70,200,0.18)",
            borda: "#7a3fd1"
        },
        "Perfeito": {
            carta: "linear-gradient(180deg, #fff6d6, #f0d98c)",
            stats: "rgba(212,175,55,0.25)",
            borda: "#d4af37" // dourado
        }
    };

    cartas.forEach(c => {
        const div = document.createElement("div");
        div.classList.add("carta");

        div.innerHTML = `
            <h3 class="titulo">${c.personagem} da ${c.fundo} ${c.borda}</h3>

            <div class="imagem-container">
                <img alt="${c.personagem} da ${c.fundo} ${c.borda}" class="imagem-carta">
            </div>

            <div class="stats">
                <div><span>Força</span><span>${c.stats.for}</span></div>
                <div><span>Destreza</span><span>${c.stats.des}</span></div>
                <div><span>Constituição</span><span>${c.stats.con}</span></div>
                <div><span>Inteligência</span><span>${c.stats.int}</span></div>
                <div><span>Sabedoria</span><span>${c.stats.sab}</span></div>
                <div><span>Carisma</span><span>${c.stats.car}</span></div>
            </div>
        `;

        // ===== Aplicação visual por raridade =====
        const estilo = raridadeStyle[c.borda];

        if (estilo) {
            div.style.background = estilo.carta;
            div.style.borderColor = estilo.borda;

            const statsDiv = div.querySelector(".stats");
            statsDiv.style.background = estilo.stats;
            statsDiv.style.border = `1px solid ${estilo.borda}55`;
        }

        container.appendChild(div);

        // ==========================
        // BUSCA DA IMAGEM SEPARADA
        // ==========================
        fetch("/img", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                fundo: c.fundo,
                personagem: c.personagem,
                borda: c.borda
            })
        })
        .then(r => r.json())
        .then(imgRes => {
            if (imgRes.sucesso) {
                const img = div.querySelector(".imagem-carta");
                img.src = `data:image/png;base64,${imgRes.imagem}`;
            } else {
                console.error("Erro ao carregar imagem:", imgRes.mensagem);
            }
        })
        .catch(err => {
            console.error("Erro ao buscar imagem da carta:", err);
        });

    });

})
.catch(err => {
    console.error("Erro ao buscar cartas diárias:", err);
});

// Botão voltar
document.getElementById("btn-receber").addEventListener("click", () => {
    window.location.href = "/home";
});
