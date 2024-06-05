import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_execution(func):
    """Decorador para loguear la ejecución de una función."""
    def wrapper(*args, **kwargs):
        logging.info(f"Ejecutando {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Finalizó {func.__name__}")
        return result
    return wrapper

def time_execution(func):
    """Decorador para medir el tiempo de ejecución de una función."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"{func.__name__} ejecutado en {execution_time:.4f} segundos")
        return result
    return wrapper
