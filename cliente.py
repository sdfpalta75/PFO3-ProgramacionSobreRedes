import socket
import json
import os

HOST_BALANCEADOR = '127.0.0.1'
PORT_BALANCEADOR = 65432
PID = os.getpid()

contador_tareas = 0

def generar_id_tarea():
    global contador_tareas
    contador_tareas+=1
    tarea_formateada = f"{contador_tareas:03d}"
    return f"{PID}{tarea_formateada}"

def enviar_tarea(id_tarea, nombre_tarea):
    try:
        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[CLIENTE] Conectando al balanceador en {HOST_BALANCEADOR}:{PORT_BALANCEADOR}...")
        socket_cliente.connect((HOST_BALANCEADOR, PORT_BALANCEADOR))
        
        # Datos de la tarea a enviar
        datos_tarea = {"id": id_tarea, "tarea": nombre_tarea}
        
        print(f"[CLIENTE] Enviando: '{nombre_tarea}' (ID: {id_tarea})")
        socket_cliente.sendall(json.dumps(datos_tarea).encode('utf-8'))
        
        # Esperar la respuesta que viene reenviada desde el worker
        datos_recibidos = socket_cliente.recv(1024)
        respuesta = json.loads(datos_recibidos.decode('utf-8'))
        
        print("\n================ RESPUESTA RECIBIDA ================")
        print(f"ID Tarea     : {respuesta.get('id_tarea')}")
        print(f"Estado       : {respuesta.get('estado')}")
        print(f"Procesado por: {respuesta.get('nodo')}")
        print(f"Tiempo tomado: {respuesta.get('tiempo')} segundos")
        print("====================================================\n")
        
        socket_cliente.close()
    except ConnectionRefusedError:
        print("[ERROR] No se pudo conectar. Asegurate de que el balanceador esté activo.")
    except Exception as error:
        print(f"[ERROR] Ocurrió un problema: {error}")

if __name__ == "__main__":
    print("--- INICIANDO PETICIÓN DE USUARIO ---")
    enviar_tarea(id_tarea:=generar_id_tarea(), nombre_tarea=f"Procesamiento de tarea {id_tarea}")
    enviar_tarea(id_tarea:=generar_id_tarea(), nombre_tarea=f"Procesamiento de tarea {id_tarea}")