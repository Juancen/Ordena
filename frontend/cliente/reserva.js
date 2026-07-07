let state = {
    fecha: null,
    hoy: null,
    mañana: null,
    horarios: [],
    horarioSeleccionado: null,
    duracion: null,
    servicioNombre: null,
    profesionalId: null,
    profesional_nombre: null,
    cliente_nombre: "",
    telefono: "",
    fechaSeleccionadaPorUsuario: false,
    pasoActual: 0
};
const pasos = [
    "bloque-fecha",
    "bloque-servicio",
    "bloque-profesional",
    "bloque-horarios",
    "bloque-datos",
    "bloque-confirmacion",
    "bloque-exito"
];

const PASO_FECHA = 0;
const PASO_SERVICIO = 1;
const PASO_PROFESIONAL = 2;
const PASO_HORARIO = 3;
const PASO_DATOS = 4;
const PASO_CONFIRMACION = 5;
const PASO_EXITO = 6;
const configuracionWizard = {

    [PASO_FECHA]: {
        mostrarVolver: false,
        textoContinuar: "Continuar",
        mostrarResumen: false
    },

    [PASO_SERVICIO]: {
        mostrarVolver: true,
        textoContinuar: "Continuar",
        mostrarResumen: false
    },

    [PASO_PROFESIONAL]: {
        mostrarVolver: true,
        textoContinuar: "Continuar",
        mostrarResumen: false
    },

    [PASO_HORARIO]: {
        mostrarVolver: true,
        textoContinuar: "Continuar",
        mostrarResumen: false
    },

    [PASO_DATOS]: {
        mostrarVolver: true,
        textoContinuar: "Revisar reserva",
        mostrarResumen: false
    },

    [PASO_CONFIRMACION]: {
        mostrarVolver: true,
        textoContinuar: "Confirmar turno",
        mostrarResumen: true
    },

    [PASO_EXITO]: {
        mostrarVolver: false,
        textoContinuar: "Finalizar",
        mostrarResumen: false
    }

};
const btnHoy = document.getElementById("btn-hoy");
const btnManana = document.getElementById("btn-manana");
const inputNombre = document.getElementById("nombre");
const inputTelefono = document.getElementById("telefono");

function renderEstadoInicialProfesionales(container) {
    const containerProfesionales = document.getElementById("profesionales-container")

    containerProfesionales.innerHTML = `
  <p class="empty-state">
    Seleccioná un servicio para ver profesionales
  </p>`
}
// Cuando carga la página
window.onload = () => {

    irAlPaso(PASO_FECHA)
    const containerProfesionales = document.getElementById("profesionales-container")
    renderEstadoInicialProfesionales();
    // 🔹 Crear fechas base
    const hoy = new Date();
    const manana = new Date();
    manana.setDate(hoy.getDate() + 1);

    // 🔹 Formato ISO correcto (YYYY-MM-DD)
    const hoyISO = formatISO(hoy);
    const mananaISO = formatISO(manana);
    cargarServicios();

    // 🔹 Guardar en state
    state.hoy = hoyISO;
    state.mañana = mananaISO;
    state.fecha = null;
    state.fechaSeleccionadaPorUsuario = false;

    // 🔹 Actualizar UI (botones)
    document.getElementById("hoy-fecha").innerText = formatearFecha(state.hoy)
    document.getElementById("manana-fecha").innerText = formatearFecha(state.mañana);

    // 🔹 Marcar "Hoy" como activo por defecto

    // 🔹 Actualizar resumen
    document.getElementById("res-fecha").innerText = "-";
    //actualizarEstadoBoton()
};
function renderFormulario() {
    inputNombre.value = state.cliente_nombre;
    inputTelefono.value = state.telefono;
}
btnHoy.addEventListener("click", () => {
    actualizarFecha(state.hoy);
    setActivo(btnHoy);
});

btnManana.addEventListener("click", () => {
    actualizarFecha(state.mañana);
    setActivo(btnManana);
});

function abrirCalendario() {
    const input = document.getElementById("fecha-hidden");
    input.click(); // abre el selector de fecha
}

const inputFecha = document.getElementById("fecha-hidden");

inputFecha.addEventListener("change", (e) => {
    actualizarFecha(e.target.value)
});

function syncBotonesFecha() {
    const btnHoy = document.getElementById("btn-hoy");
    const btnManana = document.getElementById("btn-manana");
    const btnOtro = document.querySelector(".outline");

    btnHoy.classList.remove("active");
    btnManana.classList.remove("active");
    btnOtro.classList.remove("active");

    if (state.fecha === state.hoy) {
        btnHoy.classList.add("active");
        cargarHorarios();
    } else if (state.fecha === state.manana) {
        btnManana.classList.add("active");
        cargarHorarios();
    } else {
        btnOtro.classList.add("active");
        cargarHorarios();
    }
}

const containerProfesionales = document.getElementById("profesionales-container");
const bloqueProfesional = document.getElementById("bloque-profesional");


function onServicioSeleccionado(servicioId) {
    // 1. Mostrar bloque
    resetDesde("bloque-servicio");
    renderEstadoInicialHorarios()
    state.servicio_id = servicioId;

    bloqueProfesional.style.display = "block";

    containerProfesionales.innerHTML = `
    <div class="loading-container">
                        <img src="static/spinner.svg" width="40" />
                        <p>Cargando Profesionales...</p>
                    </div>
    `;

    // 2. Llamar API
    fetch(`http://127.0.0.1:8000/profesionales?servicio_id=${servicioId}`)
        .then(res => res.json())
        .then(data => {
            // 3. Limpiar contenedor
            containerProfesionales.innerHTML = "";

            if (data.length === 0) {
                containerProfesionales.innerHTML = `
    <p class="empty-state">
      No hay profesionales disponibles
    </p>
  `;
                return;
            }


            // 4. Renderizar profesionales
            data.forEach(prof => {

                const card = document.createElement("div");

                card.addEventListener("click", (e) => {
                    const id = e.currentTarget.dataset.id;
                    state.profesionalId = id;
                    state.profesional_nombre = prof.nombre
                    // 2. limpiar selección anterior

                    document.querySelectorAll(".profesional-card")
                        .forEach(c => c.classList.remove("active"));

                    card.classList.add("active");

                    actualizarFooter();

                    if (state.servicio_id && state.profesionalId && state.fecha) {
                        resetDesde("bloque-profesional");
                        renderResumen();
                        cargarHorarios();
                    }
                });

                card.classList.add("profesional-card");
                card.setAttribute("data-id", prof.id);

                card.innerHTML = `
                    <img src="https://i.pravatar.cc/100?u=${prof.id}" />
                    <h4>${prof.nombre}</h4>
                    <p>Profesional</p>
                `;
                containerProfesionales.appendChild(card);
            });

        })
        .catch(err => console.error("Error:", err));

}

function formatISO(date) {

    return date.toLocaleDateString("en-CA"); // 👈 formato YYYY-MM-DD
}

function formatearFecha(fechaISO) {
    const [year, month, day] = fechaISO.split("-");

    const fecha = new Date(year, month - 1, day); // 👈 LOCAL

    return fecha.toLocaleDateString("es-AR", {
        day: "numeric",
        month: "short"
    });
}

function abrirCalendario() {
    const input = document.getElementById("fecha-hidden");
    input.showPicker ? input.showPicker() : input.click();
}

function seleccionarHora(hora) {
    state.horarioSeleccionado = hora;

    document.getElementById("res-hora").innerText = hora;

    renderHorarios();
    renderResumen();
    renderTurnoSeleccionado();
    actualizarFooter();

}

function renderHorarios() {
    const contenedor = document.getElementById("horarios");
    contenedor.innerHTML = "";


    state.horarios.forEach(h => {
        const div = document.createElement("div");
        div.style.padding = "10px";
        div.style.margin = "5px";
        div.style.border = "1px solid #ccc";
        div.style.display = "inline-block";
        div.style.cursor = "pointer";
        div.innerText = h.inicio;

        if (state.horarioSeleccionado === h.inicio) {

            div.classList.add("selected");

            div.onclick = () => {
                seleccionarHora(h.inicio);
            };

        } else if (h.estado === "disponible") {

            div.classList.add("disponible");
            div.onclick = () => {
                seleccionarHora(h.inicio);
            };

        } else {
            div.classList.add("disabled");
            div.style.color = "gray";
            div.style.cursor = "not-allowed";
            div.style.opacity = "0.5";
        }

        contenedor.appendChild(div);
    });
}

async function cargarServicios() {
    const res = await fetch("http://127.0.0.1:8000/servicios");
    const servicios = await res.json();

    const contenedor = document.getElementById("servicios-container");
    contenedor.innerHTML = "";

    servicios.forEach(servicio => {
        const card = document.createElement("div");
        card.classList.add("servicio-card");

        // dataset ✔️
        card.dataset.id = servicio.id;
        card.dataset.nombre = servicio.nombre;

        // contenido
        card.innerHTML = `
        <h4>${servicio.nombre}</h4>
        <p>${servicio.duracion} min</p>
        <span>$${servicio.precio}</span>
    `;

        // 🔥 UN SOLO CLICK
        card.addEventListener("click", function () {

            // limpiar selección
            document.querySelectorAll(".servicio-card")
                .forEach(c => c.classList.remove("active"));

            // marcar actual
            this.classList.add("active");

            // guardar estado (usando dataset o servicio directo)
            state.servicioId = this.dataset.id;
            state.servicioNombre = this.dataset.nombre;
            state.duracion = servicio.duracion;

            onServicioSeleccionado(state.servicioId)
            renderResumen();
            renderDuracion();
            //actualizarEstadoBoton();
        });

        contenedor.appendChild(card);
    });
}
function renderEstadoInicialHorarios() {
    const contenedor = document.getElementById("horarios");
    contenedor.innerHTML = `
  <div class="empty-horarios">
    Seleccioná un profesional para ver horarios
  </div>
`;
}

async function cargarHorarios() {
    const contenedor = document.getElementById("horarios");
    const servicioId = state.servicioId
    const profesionalId = state.profesionalId;

    if (!profesionalId) {
        renderEstadoInicialHorarios();
        return
    }


    if (isNaN(servicioId) || !state.fecha) return;

    contenedor.innerHTML = `
    <div class="loading-container">
                        <img src="static/spinner.svg" width="40" />
                        <p>Cargando horarios...</p>
                    </div>
    `;
    try {
        // 1. Disponibilidad
        const res = await fetch(
            `http://127.0.0.1:8000/agenda-completa?fecha=${state.fecha}&profesional_id=${profesionalId}&servicio_id=${servicioId}`
        );


        if (!res.ok) throw new Error("Error en agenda");

        const data = await res.json();

        if (data.length === 0) {
            contenedor.innerHTML = "No hay horarios disponibles";
            return
        }
        // 2. Turnos ocupados
        const resTurnos = await fetch(
            `http://127.0.0.1:8000/turnos?fecha=${state.fecha}&profesional_id=${profesionalId}`
        );

        if (!resTurnos.ok) throw new Error("Error en turnos");

        const turnos = await resTurnos.json();
        // Guardar y renderizar
        state.horarios = data;
        state.profesionalId = profesionalId;


        renderHorarios();

    } catch (error) {
        console.error(error);

        contenedor.innerHTML = `
            <div style="color:red;">
                ❌ Error al cargar horarios
            </div>
        `;
    }
}

async function reservar() {

    const servicio = state.servicioId
    let data = null;
    const contError = document.getElementById("error-reserva");
    contError.classList.add("hidden");

    const error = validarAntesDeReservar();

    if (error) {

        contError.innerText = error;
        contError.classList.remove("hidden");
        return; // ⛔ cortar ejecución
    }
    const body = {
        fecha: state.fecha,
        hora_inicio: state.horarioSeleccionado,
        cliente_nombre: state.cliente_nombre,
        cliente_telefono: state.telefono,
        profesional_id: state.profesionalId,
        servicio_id: servicio,
        duracion: state.duracion
    };


    const textoOriginal = btnContinuar.innerText;
    btnContinuar.disabled = true
    btnContinuar.textContent = "Reservando..."

    try {
        const res = await fetch("http://127.0.0.1:8000/turnos", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });


        try {
            data = await res.json();
        } catch { }

        if (res.ok) {

            state.cliente_nombre = "";
            state.telefono = "";

            renderFormulario();

            //actualizarEstadoBoton();
            irAlPaso(PASO_EXITO);
            window.scrollTo({ top: 0, behavior: "smooth" });

            state.horarioSeleccionado = null;
        } else {
            contError.innerText = "Error al reservar";
            contError.classList.remove("hidden");
            btnContinuar.disabled = false;
            btnContinuar.textContent = textoOriginal;
        }

    } catch (err) {
        contError.innerText = "No se pudo reservar el turno";
        contError.classList.remove("hidden");
        btnContinuar.disabled = false;
        btnContinuar.textContent = textoOriginal;
    }
}
function renderExito() {

    document.getElementById("confirmacion-fecha").innerText = state.fecha;
    document.getElementById("confirmacion-hora").innerText = state.horarioSeleccionado;
    document.getElementById("confirmacion-duracion").innerText = `${state.duracion} min`;
    document.getElementById("confirmacion-profesional").innerText = state.profesional_nombre;
    document.getElementById("confirmacion-nombre").innerText = `Te esperamos, ${state.cliente_nombre}`;

}

function actualizarFecha(fecha) {
    if (!fecha) return;

    state.fecha = fecha;
    state.horarioSeleccionado = null;
    state.fechaSeleccionadaPorUsuario = true;
    resetSeleccionHorario()
    renderResumen()
    syncBotonesFecha();
    cargarHorarios();
    actualizarFooter();

}

function setActivo(btn) {
    document.querySelectorAll(".fecha-btn").forEach(b => {
        b.classList.remove("active");
    });

    btn.classList.add("active");
}

function renderDuracion() {
    const div = document.getElementById("duracion");

    if (!state.duracion) {
        div.innerText = "";
        return;
    }


    div.innerHTML = `<i class="fa-regular fa-clock"></i> Duración estimada: ${state.duracion || "-"} min`;
}

function renderTurnoSeleccionado() {
    const div = document.getElementById("turno-seleccionado");
    const contenedor = document.querySelector(".info-turno");

    if (!state.horarioSeleccionado || !state.fecha) {
        div.innerText = "";
        contenedor.classList.remove("show");
        return;
    }

    div.innerHTML = `<i class="fa-regular fa-calendar"></i> Turno seleccionado: ${state.fecha} a las ${state.horarioSeleccionado}`;

    contenedor.classList.add("show");
}

function renderResumen() {
    document.getElementById("res-servicio").innerText =
        state.servicioNombre || "-";

    document.getElementById("res-fecha").innerText =
        state.fecha || "-";

    document.getElementById("res-hora").innerText =
        state.horarioSeleccionado || "-";

    document.getElementById("res-duracion").innerText =
        state.duracion + " " + "min" || "-";

    document.getElementById("res-profesional").innerText =
        state.profesional_nombre + " " || "-";
}

function resetFlujo() {
    // 1. resetear state
    state.fecha = null;
    state.horarioSeleccionado = null;
    state.duracion = null;
    state.servicioNombre = null;
    state.profesionalId = null;
    state.profesional_nombre = null;

    // 2. mostrar flujo
    document.querySelector(".container").style.display = "";

    // 4. limpiar UI (inputs, selección, etc)
    state.cliente_nombre = "";
    state.telefono = "";

    renderFormulario();

    // remover clases activas
    document.getElementById('profesionales-container').innerHTML = '';
    document.querySelectorAll(".profesional-card").forEach(c => c.classList.remove("active"));
    document.querySelectorAll(".servicio-card").forEach(c => c.classList.remove("active"));
    document.querySelectorAll(".selected").forEach(c => c.classList.remove("selected"));

    // Limpiar Resumen
    document.getElementById("res-servicio").innerText = "-";
    document.getElementById("res-fecha").innerText = "-";
    document.getElementById("res-hora").innerText = "-";
    document.getElementById("res-duracion").innerText = "-";
    document.getElementById("res-profesional").innerText = "-";

    irAlPaso(PASO_FECHA)
    actualizarFooter();
    renderEstadoInicialHorarios()
    renderEstadoInicialProfesionales()
}

function validarAntesDeReservar() {

    if (!state.servicioNombre) {
        return "Seleccioná un servicio";
    }

    if (!state.profesionalId) {
        return "Seleccioná un profesional";
    }

    if (!state.fecha) {
        return "Seleccioná una fecha";
    }

    if (!state.horarioSeleccionado) {
        return "Seleccioná un horario";
    }

    if (!state.cliente_nombre.trim()) {
        document.getElementById("nombre").classList.add("error");
        return "Ingresá tu nombre";
    }

    if (!state.telefono.trim()) {
        document.getElementById("telefono").classList.add("error");
        return "Ingresá tu teléfono";
    }

    return null; // todo OK
}

/*function actualizarEstadoBoton() {

    const btnReservar = document.getElementById("btnReservar");
    const nombreInput = state.cliente_nombre.trim();
    const telefonoInput = state.telefono.trim();

    const completo =
        state.servicioNombre &&
        state.profesionalId &&
        state.fechaSeleccionadaPorUsuario &&
        state.horarioSeleccionado &&
        nombreInput &&
        telefonoInput;

    btnReservar.disabled = !completo;
}*/

function activarPaso() {
    const bloquesFlujo = document.querySelectorAll(".bloque-flujo")

    bloquesFlujo.forEach(bloque => {
        bloque.classList.remove("active-step")
    })
    const bloqueActivo = document.getElementById(pasos[state.pasoActual]);

    bloqueActivo.classList.add("active-step");

}

function resetSeleccionHorario() {
    state.horarioSeleccionado = null
    document.getElementById("turno-seleccionado").innerHTML = ""
    document.getElementById("duracion").innerHTML = ""

    renderDuracion();
    renderTurnoSeleccionado();
    cargarHorarios();

    //actualizarEstadoBoton();

}
function resetBloqueProfesional() {

    state.profesionalId = null
    state.profesional_nombre = null
    document.querySelector(".profesional-card.active")?.classList.remove("active");
    renderResumen()
}

function resetBloqueHorarios() {
    state.horarioSeleccionado = null
    document.querySelector("#horarios .selected")?.classList.remove("selected");
    renderHorarios();
    renderDuracion();
    renderTurnoSeleccionado();
    renderResumen()
}

function resetBloqueDatos() {
    state.cliente_nombre = "";
    state.telefono = "";

    renderFormulario();

    document.getElementById("error-reserva")?.classList.add("hidden");

    //actualizarEstadoBoton()
}

const flujo = [
    "bloque-fecha",
    "bloque-servicio",
    "bloque-profesional",
    "bloque-horarios",
    "bloque-datos"
];
const resets = {
    "bloque-profesional": resetBloqueProfesional,
    "bloque-horarios": resetBloqueHorarios,
    "bloque-datos": resetBloqueDatos
};

function resetDesde(bloque) {
    const indiceBloque = flujo.indexOf(bloque);
    flujo.slice(indiceBloque + 1).forEach(bloqueActual => { resets[bloqueActual]?.() });
}

const wizardTrack = document.querySelector(".wizard-track");
const btnContinuar = document.getElementById("btn-continuar");
const btnVolver = document.getElementById("btn-volver");

btnContinuar.addEventListener("click", siguientePaso);

btnVolver.addEventListener("click", anteriorPaso);

inputNombre.addEventListener("input", (e) => {
    state.cliente_nombre = e.target.value;
    actualizarFooter();
});

inputTelefono.addEventListener("input", (e) => {
    state.telefono = e.target.value;
    actualizarFooter();
});

async function siguientePaso() {

    if (!validarPaso()) return;

    switch (state.pasoActual) {

        case PASO_CONFIRMACION:
            await reservar();
            break;

        case PASO_EXITO:
            resetFlujo();
            break;

        default:
            irAlPaso(state.pasoActual + 1);
    }

}

function anteriorPaso() {
    if (state.pasoActual <= 0) return;

    irAlPaso(state.pasoActual - 1);

}

function renderWizard() {

    activarPaso();
    moverSlider();
    actualizarFooter();
    renderExito();

}
function moverSlider() {
    const wizardTrack = document.querySelector(".wizard-track");
    wizardTrack.style.transform = `translateX(-${state.pasoActual * 100}%)`;
}

function irAlPaso(numeroPaso) {

    state.pasoActual = numeroPaso;
    renderWizard();

}
function actualizarFooter() {
    const config = configuracionWizard[state.pasoActual];

    btnVolver.classList.toggle("hidden", !config.mostrarVolver);
    btnContinuar.textContent = config.textoContinuar;
    btnContinuar.disabled = !validarPaso();

}
function validarPaso() {

    switch (state.pasoActual) {

        case PASO_FECHA:
            return state.fechaSeleccionadaPorUsuario;

        case PASO_SERVICIO:
            return state.servicioId !== null;

        case PASO_PROFESIONAL:
            return state.profesionalId !== null;

        case PASO_HORARIO:
            return state.horarioSeleccionado !== null;

        case PASO_DATOS:
            return (
                state.cliente_nombre.trim() !== "" &&
                state.telefono.trim() !== ""
            );

        default:
            return true;
    }
}