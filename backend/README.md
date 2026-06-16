# 🚀 Nexo

**Sistema de gestión simple para negocios locales**  
Pedidos y turnos organizados, sin caos ni pérdida de tiempo.

## 📌 Descripción

**Sistema de gestión simple para negocios locales**  
Pedidos y turnos organizados, sin caos ni pérdida de tiempo.

## 🎯 Objetivo

Ordena busca reducir el desorden operativo en negocios locales, evitando pérdida de tiempo, mensajes innecesarios y problemas de organización en la gestión diaria de pedidos y turnos.

## 🎯 Problema

Muchos negocios locales trabajan así:

- Pedidos por WhatsApp desordenados  
- Turnos anotados en papel o mensajes  
- Clientes preguntando constantemente el estado  
- Errores humanos que generan pérdida de dinero  

👉 Resultado: desorganización, estrés y mala experiencia.

---

## 💡 Solución

**Nexo centraliza la gestión del negocio en una sola plataforma**, adaptándose al rubro:

- Gastronomía → gestión de pedidos  
- Servicios → gestión de turnos  

Sin necesidad de conocimientos técnicos.

## 🧩 Funcionalidades principales

### 🍔 Gastronomía
- Gestión de productos (menú)
- Creación de pedidos
- Estados del pedido (flujo controlado)
- Código público único para que el cliente pueda consultar el estado de su pedido sin necesidad de registrarse
- Paginación y filtros por estado y fecha

### 📅 Servicios (en desarrollo)
- Agenda de turnos
- Gestión de disponibilidad
- Historial de clientes


## 🧩 Módulos
Gastronomia:
Gestión de pedidos para locales, permitiendo tomar pedidos y seguir su estado hasta la entrega.

Turnos:
Gestión de agenda para profesionales, permitiendo a clientes reservar turnos y al negocio administrar su disponibilidad.

### Decisiones clave

- El backend calcula precios (no el frontend)
- Validaciones centralizadas en la capa service
- Uso de transacciones para asegurar que un pedido se guarde completo (pedido + items) o no se guarde nada
- Código público único para consulta de pedidos sin login


## 🛠️ Stack tecnológico

- **Backend:** Python + FastAPI (API REST para la lógica del sistema)
- **Base de datos:** MySQL (gestión y persistencia de datos)
- **Frontend:** HTML5, CSS3 y JavaScript (interfaz web simple y funcional)

## 📁 Estructura del proyecto

```text
backend_ordena/
├── app/
│   ├── core/
│   ├── db/
│   ├── modules/
│   │   ├── gastronomia/
│   │   │   ├── routes/
│   │   │   ├── services/
│   │   │   ├── repositories/
│   │   │   ├── schemas/
│   │   │   ├── exceptions/
│   │   │   └── utils/
│   │   └── turnos/
│   │       ├── routes/
│   │       ├── services/
│   │       ├── repositories/
│   │       ├── schemas/
│   │       ├── exceptions/
│   │       └── utils/
│   └── main.py
├── docs/
│   ├── vision-general.md
│   ├── arquitectura.md
│   └── flujo-git.md
├── .gitignore
├── README.md
├── requirements.txt
└── run.py

## 🚀 Estado del proyecto

- ✅ Módulo de pedidos funcional (backend completo)
- ✅ Validaciones de negocio implementadas
- ✅ Paginación y filtros avanzados
- ⏳ Frontend en desarrollo
- ⏳ Módulo de turnos pendiente

## 🧪 Ejemplo de uso

### Obtener un pedido por código público

GET /pedidos/{codigo_publico}

### Respuesta

```json
{
  "codigo_publico": "PED-AB123CD4",
  "nombre_cliente": "Juan",
  "estado": "en_preparacion",
  "precio_total": 3500
}

# Clonar repositorio
git clone https://github.com/Juancen/Ordena.git

# Entrar al proyecto
cd Ordena

# Crear entorno virtual
python -m venv venv

# Activar entorno
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app.main:app --reload

🧭 Roadmap
🔜 PedidoLive (creación de pedidos en tiempo real)
🔜 Múltiples profesionales por negocio
🔜 Notificaciones automáticas
🔜 Aplicación mobile

🧠 Filosofía del proyecto
Simplicidad antes que complejidad
Resolver problemas reales
Construir algo mantenible por una sola persona
Escalar sin reescribir

📌 Visión

Convertirse en una herramienta clave para negocios locales en ciudades medianas, facilitando su digitalización sin fricción.

