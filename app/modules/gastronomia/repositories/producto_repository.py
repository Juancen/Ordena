from app.db.connection import get_connection
from mysql.connector import Error
from app.modules.gastronomia.exceptions.pedidos_errors import (
DatabaseError,
ValidationError
)
from decimal import Decimal
from typing import cast
from typing import Optional, Dict


def obtener_producto_por_id(id_producto)-> dict | None:
    
    if id_producto is None:
        return None
    
    cursor = None
    conn = None
    
    try:
            conn = get_connection()
            if conn is None:
                raise Exception("Error de conexión")   
            cursor = conn.cursor(dictionary=True)
            
            query = """SELECT id, id_negocio, nombre, precio, estado 
                        FROM productos
                        WHERE id = %s
                        """
            
            cursor.execute(query, (id_producto,))
            
            producto =  cursor.fetchone()
            if producto is None:
                return None
            
            return cast(dict, producto)
        
    except Error:
        raise 
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        

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

def listar_productos_por_negocio(id_negocio):
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Error de conexión")

        cursor = conn.cursor(dictionary=True)
        query_select = """
            SELECT id, id_negocio, nombre, precio, estado
            FROM productos
            WHERE id_negocio = %s
            AND estado = 'activo'
            """
        cursor.execute(query_select, (id_negocio,))
        lista_productos = cursor.fetchall()
        
        return lista_productos
    
    except Error as e:
        raise DatabaseError(f"Error al obtener los productos: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def actualizar_estado_repository(id_producto: int, estado: str):
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Error de conexión")

        cursor = conn.cursor()
        query_select = """
            UPDATE productos
            SET estado = %s
            WHERE id = %s
            """
        cursor.execute(query_select, (estado,id_producto))
        filas = cursor.rowcount
        
        if filas == 0:
            raise ValidationError("los cambios no fueron afectados")
        
        conn.commit()
        
        return filas
        
    except Error as e:
        raise DatabaseError(f"Error al obtener los productos: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def editar_producto_repository(id_producto: int, nombre: str, precio: Decimal):
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Error de conexión")

        cursor = conn.cursor()
        query_update = """
            UPDATE productos
            SET nombre = %s, precio = %s
            WHERE id = %s
            """
        cursor.execute(query_update, (nombre,precio,id_producto))
        filas = cursor.rowcount
        
        conn.commit()
        
        return filas
        
    except Error as e:
        raise DatabaseError(f"Error al actualizar el producto: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
