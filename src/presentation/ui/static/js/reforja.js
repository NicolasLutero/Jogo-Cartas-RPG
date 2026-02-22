// reforja.js Revisar
import { criarCartaDiv, carregarCarta } from "./carta.js";

const cartaForjaId = localStorage.getItem("cartaForja");

const cartaForja = document.getElementById("carta-reforja");
const cartaResultado = document.getElementById("carta-resultado");
const btnReforja = document.getElementById("btn-reforjar");

const btnRetorna = document.getElementById("btn-retornar");
btnRetorna.addEventListener("click", () => window.location.href='/home');


function selecionarForja(){
    localStorage.removeItem("cartaForja")
    localStorage.setItem("retornoInventario", "selecionandoForja");
    window.location.href='/inventario';
}


function bloquearInterface() {
    cartaForja.removeEventListener("click", selecionarForja);
    btnReforja.removeEventListener("click", reforjar);
    cartaForja.classList.add("bloqueado");
    btnReforja.classList.add("bloqueado");
}


function reforjar(){
    if (!cartaForjaId) {
        alert("É necessario escolher uma carta!");
        return;
    }

    bloquearInterface();

    fetch("/api/usuario/reforja", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id: cartaForjaId
        })
    })
    .then(r => r.json())
    .then(res => {
        criarCartaDiv(res.carta, cartaResultado);
    });
}


if (cartaForjaId !== null){
    carregarCarta(cartaForjaId, cartaForja);
}


fetch("/api/usuario/status-diario")
.then(res => res.json())
.then(res => {
    if (!res.sucesso) {
        console.error("Erro ao carregar status diário:", res.mensagem);
        return;
    }

    let podeReforjar = res.data.reforjar;
    if (!podeReforjar) {
        bloquearInterface();
    } else {
        cartaForja.addEventListener("click", selecionarForja);
        btnReforja.addEventListener("click", reforjar)
    }
});
