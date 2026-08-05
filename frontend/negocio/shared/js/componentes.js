async function initComponents() {
    await cargarComponente(
        "#sidebar",
        "../shared/components/sidebar.html"
    );

    await cargarComponente(
        "#topbar",
        "../shared/components/topbar.html"
    );
}

async function cargarComponente(selector, ruta) {
    const contenedor = document.querySelector(selector);

    if (!contenedor) return;

    const response = await fetch(ruta);

    if (!response.ok) {
        console.error(`No se pudo cargar: ${ruta}`);
        return;
    }

    contenedor.innerHTML = await response.text();
}

async function init() {

    await initComponents();

    cargarSidebar();

    cargarTopbar();

}
init();