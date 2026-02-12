const cartasContainer = document.getElementById("cartas");
const filtroToggle = document.getElementById("filtroToggle");
const filtroIcon = document.getElementById("filtroIcon");
const filtroBox = document.querySelector(".filtro");

const filtroFundos = document.getElementById("filtroFundos");
const filtroPersonagens = document.getElementById("filtroPersonagens");
const filtroBordas = document.getElementById("filtroBordas");

let fundos = [];
let personagens = [];
let bordas = [];

const imageCache = new Map();

// ===== Toggle filtro =====
filtroToggle.addEventListener("click", () => {
    filtroBox.classList.toggle("aberto");
    filtroIcon.innerText = filtroBox.classList.contains("aberto") ? "▲" : "▼";
});

// ===== Carregar tipos =====
fetch("/api/inventario/tipos")
.then(r => r.json())
.then(res => {
    if (!res.sucesso) return;

    // ===== Cenários (fundo) =====
    res.tipos.fundos.forEach(fundo => {
        fundos.push(fundo)

        const label = document.createElement("label");
        label.innerHTML = `
            <input type="checkbox" value="${fundo}">
            <span>${fundo}</span>
        `;

        const checkbox = label.querySelector("input");
        checkbox.checked = true;
        checkbox.addEventListener("change", () => {
            if (checkbox.checked) fundos.push(fundo);
            else fundos = fundos.filter(f => f !== fundo);
            carregarCartas();
        });

        filtroFundos.appendChild(label);
    });

    // ===== Personagens =====
    res.tipos.personagens.forEach(personagem => {
        personagens.push(personagem)

        const label = document.createElement("label");
        label.innerHTML = `
            <input type="checkbox" value="${personagem}">
            <span>${personagem}</span>
        `;

        const checkbox = label.querySelector("input");
        checkbox.checked = true;
        checkbox.addEventListener("change", () => {
            if (checkbox.checked) personagens.push(personagem);
            else personagens = personagens.filter(p => p !== personagem);
            carregarCartas();
        });

        filtroPersonagens.appendChild(label);
    });

    // ===== Raridades (borda) =====
    res.tipos.bordas.forEach(borda => {
        bordas.push(borda)

        const label = document.createElement("label");
        label.innerHTML = `
            <input type="checkbox" value="${borda}">
            <span>${borda}</span>
        `;

        const checkbox = label.querySelector("input");
        checkbox.checked = true;
        checkbox.addEventListener("change", () => {
            if (checkbox.checked) bordas.push(borda);
            else bordas = bordas.filter(b => b !== borda);
            carregarCartas();
        });

        filtroBordas.appendChild(label);
    });

    carregarCartas();
});

carregarCartas();

// ===== Buscar cartas =====
function carregarCartas(){
    cartasContainer.innerHTML = "";

    fetch("/api/inventario", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            fundos: fundos,
            personagens: personagens,
            bordas: bordas
        })
    })
    .then(r => r.json())
    .then(res => {
        if (!res.sucesso) return;

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

        res.cartas.forEach(c => {
            const div = document.createElement("div");
            div.classList.add("carta");

            div.innerHTML = `
                <h3 class="titulo">${c.personagem} da ${c.fundo} ${c.borda}</h3>

                <div class="imagem-container">
                    <img alt="${c.personagem}" class="imagem-carta">
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

            const estilo = raridadeStyle[c.borda];

            if (estilo) {
                div.style.background = estilo.carta;
                div.style.borderColor = estilo.borda;

                const statsDiv = div.querySelector(".stats");
                statsDiv.style.background = estilo.stats;
                statsDiv.style.border = `1px solid ${estilo.borda}55`;
            }

            cartasContainer.appendChild(div);

            const key = `${c.personagem}|${c.fundo}|${c.borda}`;
            if (imageCache.has(key)) {
                // usa do cache
                div.querySelector(".imagem-carta").src = `data:image/png;base64,${imageCache.get(key)}`;
            } else {
                // busca no servidor
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
                        imageCache.set(key, imgRes.imagem);  // salva no cache
                        div.querySelector(".imagem-carta").src = `data:image/png;base64,${imgRes.imagem}`;
                    }
                })
                .catch(err => {
                    console.error("Erro ao buscar imagem:", err);
                });
            }
        });
    });
}
