const pages = {
    dashboard: {
        title: "Dashboard",
        subtitle: "Bienvenido nuevamente."
    },
    agenda: {
        title: "Agenda",
        subtitle: "Gestioná los turnos de tu negocio."
    },
    turnos: {
        title: "Turnos",
        subtitle: "Administrá todos los turnos."
    },
    servicios: {
        title: "Servicios",
        subtitle: "Gestioná los servicios del negocio."
    },
    profesionales: {
        title: "Profesionales",
        subtitle: "Administrá tu equipo."
    },
    configuracion: {
        title: "Configuración",
        subtitle: "Personalizá tu negocio."
    }
};

function cargarTopbar() {
    page = document.body.dataset.page
    const info = pages[page];

    const elementoTitulo = document.getElementById('page-title');
    const elementoSubtitulo = document.getElementById('page-subtitle');
    elementoTitulo.textContent = info.title;
    elementoSubtitulo.textContent = info.subtitle;
}

