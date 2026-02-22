// fundicao.js Revisar
import { criarCartaDiv, carregarCarta } from "./carta.js";

const cartaBaseId = localStorage.getItem("cartaBaseFundicao");
const cartaSacrificioId = localStorage.getItem("cartaSacrificioFundicao");

const cartaBase = document.getElementById("carta-base");
const cartaSacrificio = document.getElementById("carta-sacrificio");
const cartaResultado = document.getElementById("carta-resultado");
const btnFundir = document.getElementById("btn-fundir");

const btnRetorna = document.getElementById("btn-retornar");
btnRetorna.addEventListener("click", () => window.location.href='/home');


function selecionarBase() {
    localStorage.removeItem("cartaBaseFundicao");
    localStorage.setItem("retornoInventario", "selecionandoBaseFundicao");
    window.location.href = "/inventario";
}


function selecionarSacrificio() {
    localStorage.removeItem("cartaSacrificioFundicao");
    localStorage.setItem("retornoInventario", "selecionandoSacrificioFundicao");
    window.location.href = "/inventario";
}


function bloquearInterface() {
    cartaBase.classList.add("bloqueado");
    cartaSacrificio.classList.add("bloqueado");
    btnFundir.classList.add("bloqueado");
    cartaBase.removeEventListener("click", selecionarBase);
    cartaSacrificio.removeEventListener("click", selecionarSacrificio);
    btnFundir.removeEventListener("click", fundir);
}


function fundir() {
    if (!cartaBaseId || !cartaSacrificioId) {
        alert("Escolha as duas cartas.");
        return;
    }

    bloquearInterface();

    fetch("/api/usuario/fundicao", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            base_id: cartaBaseId,
            sacrificio_id: cartaSacrificioId
        })
    })
    .then(r => r.json())
    .then(res => {
        criarCartaDiv(res.carta, cartaResultado);
    });
}


if (cartaBaseId !== null){
    carregarCarta(cartaBaseId, cartaBase);
}
if (cartaSacrificioId !== null){
    carregarCarta(cartaSacrificioId, cartaSacrificio);
}

cartaBase.addEventListener("click", selecionarBase);
cartaSacrificio.addEventListener("click", selecionarSacrificio);
btnFundir.addEventListener("click", fundir);


fetch("/api/usuario/status-diario")
.then(res => res.json())
.then(res => {

    if (!res.sucesso) {
        console.error("Erro ao carregar status diário:", res.mensagem);
        return;
    }

    const data = res.data;
    if (!data.fundir) {
        bloquearInterface();
    }
});
