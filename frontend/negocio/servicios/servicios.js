// Obtener elementos
const btnNuevo = document.getElementById('btn-nuevo-servicio');
const panelServicio = document.getElementById('panel-servicio');
const panelOverlay = document.getElementById('panel-overlay');
const btnCerrar = document.getElementById('btn-cerrar-panel');
const btnCancelar = document.getElementById('btn-cancelar-servicio');

// Función para abrir
btnNuevo.addEventListener('click', () => {
    panelServicio.classList.add('abierto');
    panelOverlay.classList.add('activo');
    panelOverlay.removeAttribute('hidden');
});

// Función para cerrar
const cerrarPanel = () => {
    panelServicio.classList.remove('abierto');
    panelOverlay.classList.remove('activo');
    setTimeout(() => { panelOverlay.setAttribute('hidden', ''); }, 300); // Espera a que termine la animación
};

btnCerrar.addEventListener('click', cerrarPanel);
btnCancelar.addEventListener('click', cerrarPanel);
panelOverlay.addEventListener('click', cerrarPanel); // Cierra si hacen clic fuera del panel