from app.modules.gastronomia.services.productos_service import crear_producto

try:
    resultado = crear_producto(1, "Empanadas", 0)
    print("OK:", resultado)

except Exception as e:
    print("ERROR:", e)