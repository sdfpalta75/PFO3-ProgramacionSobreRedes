import socket
import threading

HOST_BALANCEADOR = '127.0.0.1'
PORT_BALANCEADOR = 65432

# Lista de nodos Workers disponibles en el sistema distribuido
WORKERS = [
    ('127.0.0.1', 65401),
    ('127.0.0.1', 65402)
]
indice_nodo = 0
candado = threading.Lock() # Para evitar problemas de concurrencia al mover el índice

def redirigir_a_worker(conexion_cliente):
    global indice_nodo
    try:
        # Recibir la tarea del cliente
        datos_cliente = conexion_cliente.recv(1024)
        if not datos_cliente:
            conexion_cliente.close()
            return
        
        # Algoritmo Round Robin para elegir el Worker de turno
        with candado:
            nodo_elegido = WORKERS[indice_nodo]
            indice_nodo = (indice_nodo + 1) % len(WORKERS)
        
        print(f"[BALANCEADOR] Redirigiendo petición al nodo Worker: {nodo_elegido}")
        
        # Conectar al Worker elegido y pasarle la tarea
        socket_worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_worker.connect(nodo_elegido)
        socket_worker.sendall(datos_cliente)
        
        # Recibir la respuesta del Worker y mandársela directo al Cliente
        respuesta_worker = socket_worker.recv(1024)
        conexion_cliente.sendall(respuesta_worker)
        
        socket_worker.close()
    except Exception as e:
        print(f"[ERROR BALANCEADOR] {e}")
    finally:
        conexion_cliente.close()

def iniciar_balanceador():
    socket_bal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_bal.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_bal.bind((HOST_BALANCEADOR, PORT_BALANCEADOR))
    socket_bal.listen()
    
    print(f"[BALANCEADOR ACTIVO] Escuchando en {HOST_BALANCEADOR}:{PORT_BALANCEADOR}...")
    try:
        while True:
            conexion_cliente, _ = socket_bal.accept()
            # Cada redirección corre en su propio hilo para no bloquear el balanceador
            hilo_redireccion = threading.Thread(target=redirigir_a_worker, args=(conexion_cliente,))
            hilo_redireccion.daemon = True
            hilo_redireccion.start()
    except KeyboardInterrupt:
        print("\nApagando Balanceador...")
    finally:
        socket_bal.close()

if __name__ == "__main__":
    iniciar_balanceador()