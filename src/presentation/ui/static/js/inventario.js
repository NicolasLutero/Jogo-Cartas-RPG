// inventario.js Revisar
import { criarCartaDiv } from "./carta.js";

const retornoInventario = localStorage.getItem("retornoInventario");

const cartasContainer = document.getElementById("cartas");
const filtroToggle = document.getElementById("filtroToggle");
const filtroIcon = document.getElementById("filtroIcon");
const filtroBox = document.querySelector(".filtro");
const filtroFundos = document.getElementById("filtroFundos");
const filtroPersonagens = document.getElementById("filtroPersonagens");
const filtroBordas = document.getElementById("filtroBordas");

const btnRetorna = document.getElementById("btn-retornar");
if (retornoInventario){
    if (retornoInventario === "selecionandoForja") {
        btnRetorna.addEventListener("click", () => window.location.href='/reforja');
    } else if (retornoInventario === "selecionandoBaseFundicao" ||
               retornoInventario === "selecionandoSacrificioFundicao") {
        btnRetorna.addEventListener("click", () => window.location.href='/fundicao');
    }
} else {
    btnRetorna.addEventListener("click", () => window.location.href='/home');
}

let fundos = [];
let personagens = [];
let bordas = [];

filtroToggle.addEventListener("click", () => {
    filtroBox.classList.toggle("aberto");
    filtroIcon.innerText = filtroBox.classList.contains("aberto") ? "▲" : "▼";
});


fetch("/api/inventario/tipos")
.then(r => r.json())
.then(res => {
    if (!res.sucesso) return;

    res.tipos.fundos.forEach(fundo => {
        fundos.push(fundo);

        const label = document.createElement("label");
        label.innerHTML = `
            <input type="checkbox" value="${fundo}">
            <span>${fundo}</span>
        `;

        const checkbox = label.querySelector("input");
        checkbox.checked = true;
        checkbox.addEventListener("change", () => {
            fundos = checkbox.checked
                ? [...new Set([...fundos, fundo])]
                : fundos.filter(f => f !== fundo);
            carregarCartas();
        });

        filtroFundos.appendChild(label);
    });

    res.tipos.personagens.forEach(personagem => {
        personagens.push(personagem);

        const label = document.createElement("label");
        label.innerHTML = `
            <input type="checkbox" value="${personagem}">
            <span>${personagem}</span>
        `;

        const checkbox = label.querySelector("input");
        checkbox.checked = true;
        checkbox.addEventListener("change", () => {
            personagens = checkbox.checked
                ? [...new Set([...personagens, personagem])]
                : personagens.filter(p => p !== personagem);
            carregarCartas();
        });

        filtroPersonagens.appendChild(label);
    });

    res.tipos.bordas.forEach(borda => {
        bordas.push(borda);

        const label = document.createElement("label");
        label.innerHTML = `
            <input type="checkbox" value="${borda}">
            <span>${borda}</span>
        `;

        const checkbox = label.querySelector("input");
        checkbox.checked = true;
        checkbox.addEventListener("change", () => {
            bordas = checkbox.checked
                ? [...new Set([...bordas, borda])]
                : bordas.filter(b => b !== borda);
            carregarCartas();
        });

        filtroBordas.appendChild(label);
    });

    carregarCartas();
});


function carregarCartas() {
    cartasContainer.innerHTML = "";

    fetch("/api/inventario", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fundos, personagens, bordas })
    })
    .then(r => r.json())
    .then(res => {
        if (!res.sucesso) return;

        res.cartas.forEach(c => {
            const div = document.createElement("div");
            criarCartaDiv(c, div);
            cartasContainer.appendChild(div);

            if (retornoInventario) {
                div.addEventListener("click", () => {
                    if (retornoInventario === "selecionandoForja") {
                        localStorage.setItem("cartaForja", c.id);
                        window.location.href = "/reforja";
                    } else if (retornoInventario === "selecionandoBaseFundicao") {
                        localStorage.setItem("cartaBaseFundicao", c.id);
                        window.location.href = "/fundicao";
                    } else if (retornoInventario === "selecionandoSacrificioFundicao") {
                        localStorage.setItem("cartaSacrificioFundicao", c.id);
                        window.location.href = "/fundicao";
                    }
                });
            }
        });
    });
}
