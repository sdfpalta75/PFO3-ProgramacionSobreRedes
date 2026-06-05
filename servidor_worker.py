import socket
import threading
import json
import time
import random
import sys

HOST_WORKER = '127.0.0.1'

def verificar_puerto_libre(puerto):
    """Intenta abrir un socket temporal para verificar si el puerto está libre."""
    socket_prueba = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_prueba.bind((HOST_WORKER, puerto))
        return True
    except OSError:
        return False
    finally:
        socket_prueba.close()

if verificar_puerto_libre(65401):
    PORT_WORKER = 65401
elif verificar_puerto_libre(65402):
    PORT_WORKER = 65402
else:
    print("Ambos servidores se encuentran activos.")
    sys.exit(1)

def procesar_en_hilo(conexion):
    try:
        datos = conexion.recv(1024)
        if datos:
            solicitud = json.loads(datos.decode('utf-8'))
            id_tarea = solicitud.get("id")
            nombre_tarea = solicitud.get("tarea")
            
            print(f"[{PORT_WORKER}] Hilo {threading.current_thread().name} procesando tarea ID {id_tarea}")
            
            tiempo_espera = random.randint(1, 10)
            time.sleep(tiempo_espera)
            
            respuesta = {
                "estado": "COMPLETADA",
                "id_tarea": id_tarea,
                "nodo": f"Worker_Puerto_{PORT_WORKER}",
                "tiempo": tiempo_espera
            }
            conexion.sendall(json.dumps(respuesta).encode('utf-8'))
    except Exception as e:
        print(f"Error en worker: {e}")
    finally:
        conexion.close()

def iniciar_worker():
    socket_worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_worker.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_worker.bind((HOST_WORKER, PORT_WORKER))
    socket_worker.listen()
    
    print(f"[WORKER ACTIVO] Escuchando en puerto {PORT_WORKER}...")
    try:
        while True:
            conexion, _ = socket_worker.accept()
            hilo = threading.Thread(target=procesar_en_hilo, args=(conexion,))
            hilo.daemon = True
            hilo.start()
    except KeyboardInterrupt:
        print(f"\nApagando Worker {PORT_WORKER}...")
    finally:
        socket_worker.close()

if __name__ == "__main__":
    iniciar_worker()