# Ordena

## 📌 Descripción

“Plataforma simple para gestionar pedidos y turnos en negocios locales sin complicaciones.”

## 🎯 Objetivo

Ordena busca reducir el desorden operativo en negocios locales, evitando pérdida de tiempo, mensajes innecesarios y problemas de organización en la gestión diaria de pedidos y turnos.

## 🧩 Módulos
Gastronomia:
Gestión de pedidos para locales, permitiendo tomar pedidos y seguir su estado hasta la entrega.

Turnos:
Gestión de agenda para profesionales, permitiendo a clientes reservar turnos y al negocio administrar su disponibilidad.

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

El proyecto está organizado como un monolito modular, separando la lógica por dominios de negocio. Cada módulo contiene sus propias rutas, servicios, acceso a datos, validaciones y utilidades, con el objetivo de mantener una estructura clara, escalable y fácil de mantener.

## 📅 Estado del proyecto

Ordena se encuentra en una fase inicial de desarrollo. En esta etapa se está construyendo la base del backend, definiendo la estructura del proyecto y avanzando sobre la lógica principal del módulo de gastronomía, especialmente en la creación y gestión de pedidos.