fetch("/api/usuario/status-diario")
.then(res => res.json())
.then(res => {

    if (!res.sucesso) {
        console.error("Erro ao carregar status diário:", res.mensagem);
        return;
    }

    const data = res.data;

    const reforjar = document.getElementById("reforjar");
    const cartas = document.getElementById("cartas_diarias");
    const fundir = document.getElementById("fundir");

    // --- Reforjar ---
    if (!data.reforjar) {
        reforjar.classList.add("bloqueado");
        reforjar.addEventListener("click", () => {});
    } else {
        reforjar.addEventListener("click", () => {
            localStorage.removeItem("cartaForja");
            window.location.href = reforjar.getAttribute("data-rota");
        });
    }

    // --- Fundir ---
    if (!data.fundir) {
        fundir.classList.add("bloqueado");
        fundir.addEventListener("click", () => {});
    } else {
        fundir.addEventListener("click", () => {
            window.location.href = fundir.getAttribute("data-rota");
        });
    }

    // --- Cartas Diárias ---
    if (!data.cartas_diarias) {
        // 🔁 Substitui card por Inventário
        cartas.id = "inventario";
        cartas.className = "card inventario";   // remove estilos antigos
        cartas.innerHTML = "<span>Inventário</span>";
        cartas.setAttribute("data-rota", "/inventario");

        cartas.addEventListener("click", () => {
            window.location.href = "/inventario";
        });

    } else {
        // normal
        cartas.addEventListener("click", () => {
            window.location.href = cartas.getAttribute("data-rota");
        });
    }

})
.catch(err => {
    console.error("Erro ao carregar status diário:", err);
});
