from app.db.connection import get_connection
from mysql.connector import Error

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