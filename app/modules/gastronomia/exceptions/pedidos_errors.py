class ValidationError(Exception):
    pass

class PedidoInvalidError(Exception):
    pass

class NegocioNoEncontradoError(Exception):
    pass

class ProductosNoEncontradosError(Exception):
    def __init__(self, ids_faltantes):
        self.ids_faltantes = ids_faltantes
        super().__init__(f"Productos no encontrados: {ids_faltantes}")

class ProductoNoPerteneceAlNegocioError(Exception):
    pass

class DatabaseError(Exception):
    pass

class PedidoNoEncontradoError(Exception):
    pass