// Carregando Carta da Forja
const cartaForja = localStorage.getItem("cartaForja");

// Pegando elementos
const carta_selecao = document.getElementById("carta-selecao");
const carta_resultado = document.getElementById("carta-resultado");
const btn_reforja = document.getElementById("btn-reforjar")

// Funções da carta e do botão
function carta_selecao_click(){
    localStorage.removeItem("cartaForja")
    localStorage.setItem("retornoInventario", "selecionandoCartaReforja");
    window.location.href='/inventario';
}

function btn_reforja_click(){
    if (cartaForja) {
        carta_selecao.removeEventListener("click", carta_selecao_click);
        btn_reforja.removeEventListener("click", btn_reforja_click);
        carta_selecao.classList.add("bloqueado");
        btn_reforja.classList.add("bloqueado");

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

        fetch("/api/usuario/reforja/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                id: cartaForja
            })
        })
        .then(r => r.json())
        .then(res => {
            const c = res.carta;

            // Gerando Div da Carta
            const div = carta_resultado;

            div.innerHTML = `
                <h3 class="titulo">${c.personagem} da ${c.fundo} ${c.borda}</h3>

                <div class="imagem-container">
                    <img alt="${c.personagem}" class="imagem-carta">
                </div>

                <div class="stats">
                    <div><span>Força</span><span>${c.stats.for[0]} (${c.stats.for[1]}%)</span></div>
                    <div><span>Destreza</span><span>${c.stats.des[0]} (${c.stats.des[1]}%)</span></div>
                    <div><span>Constituição</span><span>${c.stats.con[0]} (${c.stats.con[1]}%)</span></div>
                    <div><span>Inteligência</span><span>${c.stats.int[0]} (${c.stats.int[1]}%)</span></div>
                    <div><span>Sabedoria</span><span>${c.stats.sab[0]} (${c.stats.sab[1]}%)</span></div>
                    <div><span>Carisma</span><span>${c.stats.car[0]} (${c.stats.car[1]}%)</span></div>
                </div>
            `;

            const estilo = raridadeStyle[c.borda];

            if (estilo) {
                div.style.background = estilo.carta;
                div.style.borderColor = estilo.borda;

                const statsDiv = div.querySelector(".stats");
                statsDiv.style.background = estilo.stats;
                statsDiv.style.border = `1px solid ${estilo.borda}55`;
            }

            // Pegando imagem da carta
            fetch("/img", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    fundo: c.fundo,
                    personagem: c.personagem,
                    borda: c.borda
                })
            })
            .then(r => r.json())
            .then(imgRes => {
                if (imgRes.sucesso) {
                    div.querySelector(".imagem-carta").src = `data:image/png;base64,${imgRes.imagem}`;
                }
            })
            .catch(err => {
                console.error("Erro ao buscar imagem:", err);
            });
        });
    }
    else {
        alert("É necessario escolher uma carta!");
    }
}

let pode_reforjar = false;
fetch("/api/usuario/status-diario")
.then(res => res.json())
.then(res => {
    if (!res.sucesso) {
        console.error("Erro ao carregar status diário:", res.mensagem);
        return;
    }
    pode_reforjar = res.data.reforjar;

    // --- Reforjar ---
    if (!pode_reforjar) {
        carta_selecao.classList.add("bloqueado");
        btn_reforja.classList.add("bloqueado");
    } else {
        // Evento de click da carta
        carta_selecao.addEventListener("click", carta_selecao_click);

        // Evento de click no botão de reforja
        btn_reforja.addEventListener("click", btn_reforja_click)
    }
});

// Substitue carta selecionada
if (cartaForja){
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

    fetch("/api/inventario/carta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id: cartaForja
        })
    })
    .then(r => r.json())
    .then(res => {
        const c = res.carta;

        // Gerando Div da Carta
        const div = carta_selecao;

        div.innerHTML = `
            <h3 class="titulo">${c.personagem} da ${c.fundo} ${c.borda}</h3>

            <div class="imagem-container">
                <img alt="${c.personagem}" class="imagem-carta">
            </div>

            <div class="stats">
                <div><span>Força</span><span>${c.stats.for[0]} (${c.stats.for[1]}%)</span></div>
                <div><span>Destreza</span><span>${c.stats.des[0]} (${c.stats.des[1]}%)</span></div>
                <div><span>Constituição</span><span>${c.stats.con[0]} (${c.stats.con[1]}%)</span></div>
                <div><span>Inteligência</span><span>${c.stats.int[0]} (${c.stats.int[1]}%)</span></div>
                <div><span>Sabedoria</span><span>${c.stats.sab[0]} (${c.stats.sab[1]}%)</span></div>
                <div><span>Carisma</span><span>${c.stats.car[0]} (${c.stats.car[1]}%)</span></div>
            </div>
        `;

        const estilo = raridadeStyle[c.borda];

        if (estilo) {
            div.style.background = estilo.carta;
            div.style.borderColor = estilo.borda;

            const statsDiv = div.querySelector(".stats");
            statsDiv.style.background = estilo.stats;
            statsDiv.style.border = `1px solid ${estilo.borda}55`;
        }

        // Pegando imagem da carta
        fetch("/img", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                fundo: c.fundo,
                personagem: c.personagem,
                borda: c.borda
            })
        })
        .then(r => r.json())
        .then(imgRes => {
            if (imgRes.sucesso) {
                div.querySelector(".imagem-carta").src = `data:image/png;base64,${imgRes.imagem}`;
            }
        })
        .catch(err => {
            console.error("Erro ao buscar imagem:", err);
        });
    });
}
