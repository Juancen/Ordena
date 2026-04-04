from app.db.connection import get_connection
from mysql.connector import Error
from app.modules.gastronomia.exceptions.pedidos_errors import (
DatabaseError,
ValidationError
)
from typing import cast


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

def obtener_negocio_por_id(id_negocio):
    if not id_negocio:
        raise ValueError("id_negocio es obligatorio")
    
    cursor = None
    conn = None
    
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Error de conexión")   
        cursor = conn.cursor(dictionary=True)
        
        query = """
                    SELECT *
                    FROM negocios
                    WHERE id = %s
                    AND estado = 'activo' 
                
                """
        
        cursor.execute(query, (id_negocio, ))
        negocio = cursor.fetchone()
        return negocio
    
    except Error as e:
        raise DatabaseError(f"Error al obtener negocio: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def obtener_pedido_por_codigo_publico(codigo_publico):
    cursor = None
    conn = None
    
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Error de conexión")   
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT id,
                   codigo_publico,
                   nombre_cliente,
                   contacto_cliente,
                   direccion_cliente,
                   tipo_entrega,
                   origen,
                   estado,
                   precio_total
            FROM pedidos
            WHERE codigo_publico = %s
        """
        
        cursor.execute(query, (codigo_publico, ))
        pedido = cursor.fetchone()
        return pedido
    except Error as e:
        raise DatabaseError(f"Error al obtener el pedido: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def crear_pedido_con_items(id_negocio,nombre_cliente,contacto_cliente, direccion_cliente,tipo_entrega,origen,estado,precio_total,codigo_publico,items):
    
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Error de conexión") 
        cursor = conn.cursor()
        
        query_pedido = """
            INSERT INTO pedidos (
                id_negocio,
                nombre_cliente,
                contacto_cliente,
                direccion_cliente,
                tipo_entrega,
                origen,
                estado,
                precio_total,
                codigo_publico
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_pedido, (
            id_negocio,
            nombre_cliente,
            contacto_cliente,
            direccion_cliente,
            tipo_entrega,
            origen,
            estado,
            precio_total,
            codigo_publico
        ))
        id_pedido = cursor.lastrowid
        query_item = """
            INSERT INTO items_pedido (
                id_pedido,
                id_producto,
                cantidad,
                precio_unitario
            )
            VALUES (%s, %s, %s, %s)
        """
        for item in items:
            cursor.execute(query_item, (
                id_pedido,
                item["id_producto"],
                item["cantidad"],
                item["precio_unitario"]
            ))
        conn.commit()
        return {
            "id_pedido": id_pedido,
            "codigo_publico": codigo_publico
        }
    
    except Error as e:
        if conn:
            conn.rollback()
        raise DatabaseError(f"Error al crear pedido: {str(e)}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def obtener_pedido_por_id(id_pedido) -> dict | None:
    
    cursor = None
    conn = None
    
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Error de conexión")   
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT id,
                   codigo_publico,
                   nombre_cliente,
                   contacto_cliente,
                   direccion_cliente,
                   tipo_entrega,
                   origen,
                   estado,
                   precio_total
            FROM pedidos
            WHERE id = %s
        """
        
        cursor.execute(query, (id_pedido, ))
        pedido = cursor.fetchone()
        if not pedido:
            return None

        return cast(dict, pedido)
    except Error as e:
        raise DatabaseError(f"Error al obtener el pedido: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def repository_actualizar_estado_pedido(id_pedido, nuevo_estado):
    cursor = None
    conn = None
    
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Error de conexión")   
        cursor = conn.cursor()
        
        query = """ UPDATE pedidos
                    SET estado = %s
                    WHERE id = %s;
        """
        
        cursor.execute(query, (nuevo_estado, id_pedido ))
        filas_afectadas = cursor.rowcount
        conn.commit()
        return filas_afectadas > 0
    
    except Error as e:
        if conn:
            conn.rollback()
        raise DatabaseError(f"Error al actualizar el estado del pedido: {str(e)}")
    finally:
        if cursor:  
            cursor.close()
        if conn:
            conn.close()

def obtener_pedidos(id_negocio: int, estado: str | None = None):
    
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        if conn is None:
            raise Exception("Error de conexión") 
        cursor = conn.cursor(dictionary=True)
        
        query = """
                SELECT codigo_publico, nombre_cliente, tipo_entrega, estado, fecha_creacion, precio_total
                FROM pedidos
                WHERE id_negocio = %s
                """
        params: list = [id_negocio]

        if estado is not None:
            query += " AND estado = %s"
            params.append(estado)
            
        query += " ORDER BY fecha_creacion DESC"
        cursor.execute(query, params)
        lista_de_pedidos = cursor.fetchall()
        return lista_de_pedidos
    
    except Error as e:
        raise DatabaseError(f"Error al obtener los pedidos: {str(e)}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def obtener_items_por_pedido(id_pedido):
        cursor = None
        conn = None
        
        try:
            conn = get_connection()
            if conn is None:
                raise Exception("Error de conexión")   
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT 
                ip.id_producto,
                p.nombre AS nombre_producto,
                ip.cantidad,
                ip.precio_unitario,
                (ip.cantidad * ip.precio_unitario) AS subtotal
                FROM items_pedido ip
                INNER JOIN productos p ON p.id = ip.id_producto
                WHERE ip.id_pedido = %s
            """
            
            cursor.execute(query, (id_pedido, ))
            items = cursor.fetchall()
            return items
        except Error as e:
            raise DatabaseError(f"Error al obtener el pedido: {str(e)}")
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()