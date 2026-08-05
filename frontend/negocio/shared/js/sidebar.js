async function cargarSidebar() {
    const sidebar = document.getElementById("sidebar");

    if (!sidebar) return;

    const response = await fetch("../shared/components/sidebar.html");
    const html = await response.text();

    sidebar.innerHTML = html;
}