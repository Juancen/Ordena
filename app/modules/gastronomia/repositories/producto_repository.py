from app.db.connection import get_connection
from mysql.connector import Error
from app.modules.gastronomia.exceptions.pedidos_errors import (
DatabaseError,
ValidationError
)
from decimal import Decimal

def obtener_productos_por_ids(ids_productos):
    
    if not ids_productos:
        return []
    
    cursor = None
    conn = None
    
    try:
            conn = get_connection()
            if conn is None:
                raise Exception("Error de conexión")   
            cursor = conn.cursor(dictionary=True)
            placeholders = ", ".join(["%s"] * len(ids_productos))
            query = f"""SELECT id, id_negocio, nombre, precio, estado 
                        FROM productos 
                        WHERE id IN ({placeholders})
                        AND estado = 'activo' """
            
            cursor.execute(query, ids_productos)
            return cursor.fetchall()
        
    except Error:
        raise 
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def existe_producto_con_mismo_nombre(id_negocio: int, nombre: str) -> bool:
    
    cursor = None
    conn = None
    
    
    
    
    try:
        conn = get_connection()
        if conn is None:
                raise Exception("Error de conexión")
        cursor = conn.cursor()
        
        query = """
            SELECT 1
            FROM productos
            WHERE id_negocio = %s
            AND LOWER(TRIM(nombre)) = LOWER(TRIM(%s))
            LIMIT 1
            """

        cursor.execute(query, (id_negocio, nombre))
        resultado = cursor.fetchone()
        
    except Error:
        raise 
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return resultado is not None

def crear_producto_repository(id_negocio: int, nombre: str, precio: Decimal, estado: str = "activo"):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Error de conexión")

        cursor = conn.cursor(dictionary=True)

        query = """
            INSERT INTO productos (id_negocio, nombre, precio, estado)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (id_negocio, nombre, precio, estado))
        conn.commit()

        id_producto = cursor.lastrowid

        query_select = """
            SELECT id, id_negocio, nombre, precio, estado
            FROM productos
            WHERE id = %s
        """
        cursor.execute(query_select, (id_producto,))
        producto = cursor.fetchone()

        return producto

    except Error as e:
        if conn:
            conn.rollback()
        raise DatabaseError(f"Error al crear el producto: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()