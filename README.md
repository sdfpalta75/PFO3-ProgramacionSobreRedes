# PFO3 - Programacion Sobre Redes

# Sistemas Distribuidos

## Alumno, Sebastián Fernández

## Comisión A

## Repositorio github: https://github.com/sdfpalta75/PFO3-ProgramacionSobreRedes.git


### Sobre el proyecto:

Acorde a los requerimientos de la cátedra, el presente proyecto simula de forma básica el funcionamiento de un sistema distribuido, por lo que no posee dependencias a objetos o servicios ajenos a este entorno de desarrollo, motivo por el cual el archivo de dependencias se encuentra vacío, no obstante lo cual se incluyó por buena práctica y ante la eventualidad de expansión del sistema.

![Diagrama de Sistema Distribuido](/img/DiagSistDist.png)

### Primeros pasos:

1) Clonar el repositorio del proyecto con

    git clone https://github.com/sdfpalta75/PFO3-ProgramacionSobreRedes.git

2) No obligatorio (ya que el proyecto emplea la librería estándar), pero aconsejable, es crear un entorno virtual dentro de la carpeta de la solución mediante: 

    python -m venv env (env es el nombre que se le da al entorno virtual, por lo que puede reemplazarse)

3) Activar el entrono virtual:

desde windows:

    env\Scripts\activate

desde linux/macOS:

    source env/bin/activate

4) Si bien no aplica actualmente, ya que en principio el funcionamiento básico del proyecto emplea solo la librería estándar de Python y no existen dependencias externas, eventualmente en este momento se instalarían estas últimas mediante:

    pip install -r requirements.txt

### Puesta en servicio:

1) En una terminal, inicializar el primer servidor worker:

    python servidor_worker.py

2) Una vez en servicio, en otra terminal inicializar el segundo servidor worker mediante el mismo comando (el código propuesto contiene un algoritmo que asigna automáticamente los puertos a emplear por los servidores).

***NOTA:*** El presente proyecto está pensado para que dos servidores trabajen en los puertos 65401 y 65402, respectivamente, sin control en relación al estado de uso de los mismos por parte de otros procesos. En caso de necesidad, deberán cambiarse manualemnte los mismos en el código del archivo *servidor_worker.py* y también en el código del balanceador (*balanceador.py*), el cual escucha en el puerto 65432, el que asimismo deberá modificarse en situaciones análogas, tanto en su código, como en el código del cliente (*cliente.py* y/o *cliente_concurrente.py*).

3) En una nueva terminal se debe poner en servicio el balanceador de carga:

    python balanceador.py

4) En este punto, deben levantarse en terminales propias los clientes, los que contienen código para enviar como tarea y poner en marcha el proyecto. Los mismos se ponen en servicio mediante:

    python cliente.py

**En este punto es importante destacar que para notar una mejor experiencia de concurrencia y distribución en los workers, es conveniente preparar la sentencia en dos o tres terminales divididas en la misma pantalla y ejecutar todas a la mayor celeridad posible.**

Alternativamente, para una ejecución más limpia, se incluye a manera de test el código de un cliente que funciona con concurrencia y permite enviar varias tareas al balanceador y esperar las respuestas, permitienddo observar la concurrencia y distribución de tareas, al costo de perder la simultaneidad de varios clientes. Comando de servicio:

    python cliente_concurrente.py

Para una experiencia más real, se empleó la función *randint()* para simular cargas aleatoriamente distintas para cada tarea.
