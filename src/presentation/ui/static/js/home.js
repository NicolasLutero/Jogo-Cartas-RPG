// home.js Revisar

fetch("/api/usuario/status-diario")
.then(res => res.json())
.then(res => {

    if (!res.sucesso) {
        console.error("Erro ao carregar status diário:", res.mensagem);
        return;
    }

    const data = res.data;

    const btn_jogar = document.getElementById("jogar");
    const btn_inventario = document.getElementById("inventario");
    const btn_cartas = document.getElementById("cartas_diarias");
    const btn_reforjar = document.getElementById("reforjar");
    const btn_fundir = document.getElementById("fundir");

    btn_jogar.addEventListener("click", () => {
        window.location.href = btn_jogar.getAttribute("data-rota");
    });

    btn_inventario.addEventListener("click", () => {
        localStorage.removeItem("retornoInventario");
        window.location.href = btn_inventario.getAttribute("data-rota");
    });

    if (!data.cartas_diarias) {
        btn_cartas.classList.add("bloqueado");
    } else {
        btn_cartas.addEventListener("click", () => {
            window.location.href = btn_cartas.getAttribute("data-rota");
        });
    }

    if (!data.reforjar) {
        btn_reforjar.classList.add("bloqueado");
    } else {
        btn_reforjar.addEventListener("click", () => {
            localStorage.removeItem("cartaForja");
            window.location.href = btn_reforjar.getAttribute("data-rota");
        });
    }

    if (!data.fundir) {
        btn_fundir.classList.add("bloqueado");
    } else {
        btn_fundir.addEventListener("click", () => {
            window.location.href = btn_fundir.getAttribute("data-rota");
        });
    }
})
.catch(err => {
    console.error("Erro ao carregar status diário:", err);
});


const btn_logout = document.getElementById("btn-logout");

btn_logout.addEventListener("click", async () => {
    const response = await fetch("/api/logout", {
        method: "POST"
    });

    const data = await response.json();
    window.location.href = data.redirect;
});
