from app.db.connection import get_connection
from mysql.connector import Error
from app.modules.gastronomia.exceptions.pedidos_errors import DatabaseError

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