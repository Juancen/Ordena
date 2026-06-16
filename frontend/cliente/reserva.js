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
    cliente_nombre: null
};

const btnHoy = document.getElementById("btn-hoy");
const btnManana = document.getElementById("btn-manana");

// Cuando carga la página
window.onload = () => {
    // 🔹 Crear fechas base
    const hoy = new Date();

    const manana = new Date();

    manana.setDate(hoy.getDate() + 1);

    // 🔹 Formato ISO correcto (YYYY-MM-DD)
    const hoyISO = formatISO(hoy);
    const mananaISO = formatISO(manana);

    // 🔹 Guardar en state
    state.hoy = hoyISO;
    state.mañana = mananaISO;
    state.fecha = hoyISO;

    // 🔹 Actualizar UI (botones)
    document.getElementById("hoy-fecha").innerText = formatearFecha(state.hoy)
    document.getElementById("manana-fecha").innerText = formatearFecha(state.mañana);

    // 🔹 Marcar "Hoy" como activo por defecto
    setActivo(btnHoy);

    // 🔹 Actualizar resumen
    document.getElementById("res-fecha").innerText = hoyISO;
};

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


document.getElementById("servicio").addEventListener("change", (e) => {
    const select = e.target;
    const option = select.options[select.selectedIndex];

    state.servicioNombre = select.options[select.selectedIndex].text;
    state.duracion = option.dataset.duracion;

    renderResumen();
    renderDuracion();
    if (state.profesionalId) {
        cargarHorarios(state.profesionalId);
    }
});

const inputFecha = document.getElementById("fecha-hidden");

inputFecha.addEventListener("change", (e) => {
    state.fecha = e.target.value;
    const fecha = e.target.value;

    syncBotonesFecha();
    renderResumen();
    if (state.profesionalId) {
        cargarHorarios(state.profesionalId);
    }
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
    state.servicio_id = servicioId;
    bloqueProfesional.style.display = "block";

    // 2. Llamar API
    fetch(`http://127.0.0.1:8000/profesionales?servicio_id=${servicioId}`)
        .then(res => res.json())
        .then(data => {

            // 3. Limpiar contenedor
            containerProfesionales.innerHTML = "";

            // 4. Renderizar profesionales
            data.forEach(prof => {
                console.log(data)

                const card = document.createElement("div");

                card.addEventListener("click", (e) => {
                    const id = e.currentTarget.dataset.id;
                    state.profesional_id = id;
                    state.profesional_nombre = prof.nombre
                    // 2. limpiar selección anterior
                    document.querySelectorAll(".profesional-card")
                        .forEach(c => c.classList.remove("active"));

                    card.classList.add("active");
                    if (state.servicio_id && state.profesional_id && state.fecha) {
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

containerProfesionales.addEventListener("click", async (e) => {

    const card = e.target.closest(".profesional-card");
    if (!card) return;

    const profesionalId = card.dataset.id;

    cargarHorarios(profesionalId);
});


const selectServicio = document.getElementById("servicio");

selectServicio.addEventListener("change", (e) => {
    const servicioId = e.target.value;

    onServicioSeleccionado(servicioId);
});

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

async function cargarHorarios(profesionalId) {
    const servicioId = parseInt(document.getElementById("servicio").value);
    if (!profesionalId) return; //
    if (isNaN(servicioId) || !state.fecha) return;

    // 1. Disponibilidad
    const res = await fetch(
        `http://127.0.0.1:8000/agenda-completa?fecha=${state.fecha}&profesional_id=${profesionalId}&servicio_id=${servicioId}`
    );
    const data = await res.json();

    // 2. Turnos ocupados
    const resTurnos = await fetch(`http://127.0.0.1:8000/turnos?fecha=${state.fecha}&profesional_id=${profesionalId}`);
    const turnos = await resTurnos.json();

    if (!res.ok) {
        state.horarios = [];
        renderHorarios();
        return;
    }

    // 4. Guardar y renderizar
    state.horarios = data;
    state.profesionalId = profesionalId
    renderHorarios();
}

async function reservar() {
    const nombre = document.getElementById("nombre").value;
    const telefono = document.getElementById("telefono").value;
    const servicio = parseInt(document.getElementById("servicio").value)
    const duracion = document.getElementById("res-duracion").value


    if (!state.horarioSeleccionado || !nombre || !telefono) {
        alert("Completá todos los campos");
        return;
    }

    const body = {
        fecha: state.fecha,
        hora_inicio: state.horarioSeleccionado,
        cliente_nombre: nombre,
        cliente_telefono: telefono,
        profesional_id: state.profesionalId,
        servicio_id: servicio,
        duracion: state.duracion
    };

    try {
        const res = await fetch("http://127.0.0.1:8000/turnos", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        const data = await res.json();

        if (res.ok) {
            state.cliente_nombre = nombre;
            mostrarConfirmacion()
            cargarHorarios();
        } else {
            document.getElementById("mensaje").innerText = "Error al reservar";
        }

        document.getElementById("nombre").value = "";
        document.getElementById("telefono").value = "";
        state.horarioSeleccionado = null;


    } catch (err) {
        console.log("ERROR:", err);
    }
}

function mostrarConfirmacion() {

    // 🔹 BLOQUES
    const bloqueHorarios = document.getElementById("horarios");
    const bloqueInfo = document.getElementById("info-turno");
    const bloqueConfirmacion = document.getElementById("confirmacion-turno");

    // 🔹 OCULTAR
    bloqueHorarios.classList.add("hidden");
    bloqueInfo.classList.add("hidden");

    // 🔹 INSERTAR DATOS
    document.getElementById("confirmacion-fecha").innerText = state.fecha;
    document.getElementById("confirmacion-hora").innerText = state.horarioSeleccionado;
    document.getElementById("confirmacion-duracion").innerText = state.duracion + " min";
    document.getElementById("confirmacion-profesional").innerText = state.profesional_nombre;
    document.getElementById("confirmacion-nombre").innerText = `Te esperamos, ${state.cliente_nombre}`;

    // 🔹 MOSTRAR
    bloqueConfirmacion.classList.remove("hidden");
}

function actualizarFecha(fecha) {
    if (!fecha) return;

    state.fecha = fecha;
    state.horarioSeleccionado = null;
    document.getElementById("res-hora").innerText = "-";
    document.getElementById("res-fecha").innerText = fecha;
    syncBotonesFecha();
    //cargarHorarios();
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


    div.innerHTML = `<i class="fa-regular fa-clock"></i> Duración estimada: ${state.duracion || "-"}`;
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
}