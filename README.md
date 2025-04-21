### Proyecto 1 Tópicos E. Telemática

### Asignatura: 
## Tópicos especiales en Telemática

### Docente: 
## Edwin Montoya Munera

### Por:
## Emanuel Patiño
## Esteban Muriel
## Tomás Pineda

### Escuela de ciencias e ingeniería Universidad EAFIT, sede Medellín 2025-1

## 1. Generalidades del proyecto
# Introducción

El objetivo de este proyecto es diseñar e implementar un middleware orientado a mensajería (MOM) que permita a un conjunto de clientes enviar y recibir mensajes de datos. Esto permitirá evidenciar, conocer y aplicar, muchas de las características subyacentes a los sistemas distribuidos que deben implementar las aplicaciones o los subsistemas base. En este caso, dicha complejidad y características del sistema distribuido serán diseñadas e implementadas en un MOM, de tal manera que para las aplicaciones usuarias sea transparente y seguro su uso.



# Objetivos
# Objetivo General: Diseñar e implementar un middleware MOM en cluster que permita a un conjunto de aplicaciones comunicarse por colas o tópicos.

## Objetivos Específicos:
 Diseñar e implementar un API entre Cliente y MOM para la gestión de colas y tópicos, así como el envío y recepción de mensajes.

 Implementar RPC basados en API REST y gRPC entre Cliente y MOM, y MOM a MOM.

Diseñar e implementar un mecanismo de particionamiento y replicación en el clúster MOM.

 Diseñar e implementar unas aplicaciones cliente sencillas para probar las funcionalidades del MOM.


### 1.1. Aspectos Cumplidos

Requerimientos funcionales

Fase 1: Conexión Cliente - MOM y API REST 


FR-01	Un cliente debe poder conectarse al MOM mediante una API REST.	
Un cliente envía una solicitud a la API y recibe una respuesta de conexión exitosa.

FR-02	Un cliente debe poder desconectarse del MOM mediante la API REST.	
El cliente envía una solicitud de desconexión y recibe confirmación.

FR-03	La API REST debe permitir la autenticación de usuarios.	
Un usuario debe iniciar sesión con credenciales y recibir un token de autenticación.

FR-04	Solo usuarios autenticados pueden crear colas y tópicos.	
Si un usuario no autenticado intenta crear un tópico o cola.

FR-05	Se debe permitir la creación y eliminación de tópicos en el MOM.	
Un usuario autenticado puede crear y eliminar tópicos mediante la API REST.

FR-06	Se debe permitir la creación y eliminación de colas en el MOM.	
Un usuario autenticado puede crear y eliminar colas mediante la API REST.

FR-07	Listar los tópicos y colas existentes.	
Un usuario autenticado puede ver la lista de colas y tópicos disponibles.

Fase 2: Envío y Recepción de Mensajes


FR-08	Un cliente debe poder enviar un mensaje a un tópico.	
Un mensaje es enviado a un tópico y se verifica su almacenamiento en el MOM.

FR-09	Un cliente debe poder enviar un mensaje a una cola.	
Un mensaje es enviado a una cola y se almacena correctamente.

FR-10	Un cliente debe poder recibir mensajes de un tópico.
Un cliente suscrito recibe un mensaje publicado en el tópico.

FR-11	Un cliente debe poder recibir mensajes de una cola.	
Un mensaje en la cola se entrega a un cliente en espera.

FR-12	Los mensajes enviados deben estar asociados a un usuario.	
Se almacena información del remitente en cada mensaje.
FR-13	Implementar un mecanismo de autenticación en los mensajes.	
Un usuario no autenticado no puede enviar ni recibir mensajes.

FR-14	Implementar la opción de recibir mensajes en modo pull o push.	
Los clientes pueden elegir entre recibir mensajes automáticamente o consultarlos manualmente.

Fase 3: Comunicación entre Servidores MOM y Seguridad

FR-15	Implementar comunicación de servidores mediante gRPC.	
Los nodos del MOM pueden intercambiar mensajes de manera eficiente.

FR-16	Implementar replicación de mensajes en varios nodos MOM.
Un mensaje enviado a un nodo MOM es replicado en otros nodos disponibles.

FR-18	Permitir eliminación de tópicos y colas solo por sus creadores.	
Si un usuario intenta borrar un tópico o cola que no creó, la API lo rechaza.

FR-19	Definir una estrategia para manejar mensajes en colas/tópicos eliminados.
Si se borra un tópico o cola, se decide si los mensajes se transfieren o eliminan.

FR-20	Implementar mecanismos básicos de tolerancia a fallos en el MOM.	
Si un nodo MOM falla, otro debe tomar su lugar sin perder datos.


Fase 4: Escalabilidad, Despliegue y Monitoreo

FR-21	Implementar particionamiento de colas y tópicos para mejorar escalabilidad.
Los mensajes se distribuyen eficientemente entre diferentes nodos MOM.

FR-22	Implementar balanceo de carga en los nodos MOM.	
Si un nodo MOM está sobrecargado, las nuevas conexiones son redirigidas a otro nodo.

FR-23	Implementar logs y monitoreo del sistema.	
Se generan registros detallados de las conexiones, mensajes y fallos en el MOM.

FR-24	Desplegar el sistema en AWS y documentar el proceso.	
El sistema está funcionando en AWS y se proporciona documentación detallada.

FR-25	Implementar métricas de rendimiento y estadísticas del uso del MOM.	Los administradores pueden consultar estadísticas de tráfico y uso de colas/tópicos.


Requerimientos no funcionales

1. Rendimiento y Escalabilidad
NFR-01: Alto rendimiento en el procesamiento de mensajes
NFR-02: Escalabilidad horizontal
2. Seguridad
NFR-04: Autenticación de usuarios
3. Tolerancia a Fallos
NFR-07: Persistencia de mensajes
NFR-08: Replicación y recuperación ante fallos

### 1.2. Aspectos NO Cumplidos

FR-17	Implementar mecanismos de encriptación en el transporte de mensajes.	Los mensajes transmitidos entre clientes y MOM están cifrados.

### 2. Diseño general

### Buenas prácticas y diseño de alto nivel

Para el diseño del sistema se optó por una arquitectura modular distribuida que permite una clara separación de responsabilidades, lo cual mejora significativamente la mantenibilidad, escalabilidad y testeo del código. La lógica del cliente y del servidor se organizó en módulos independientes, lo que facilita su desarrollo y evolución por separado. Dentro del servidor, se implementó una estructura basada en el patrón Modelo-Controlador, dividiendo la lógica de acceso a datos (database) y el control del flujo de operaciones (controller). Esta separación favorece la reutilización del código y la reducción del acoplamiento entre componentes. La comunicación entre servidores se realizó mediante gRPC, una tecnología elegida por su eficiencia en entornos distribuidos y por permitir llamadas remotas de alto rendimiento. Por otro lado, la interacción entre los clientes y el sistema se hizo a través de una API REST, que aporta simplicidad, compatibilidad y escalabilidad en la comunicación HTTP. Además, el uso de archivos .env para manejar variables de entorno refuerza la seguridad y la portabilidad del sistema, permitiendo adaptar fácilmente la configuración a distintos entornos de despliegue sin modificar el código fuente. Estas decisiones reflejan una orientación hacia buenas prácticas modernas de ingeniería de software, centradas en la flexibilidad, la eficiencia y la resiliencia del sistema.

### Funcionamiento General

El sistema consta de tres servidores MOM que se comunican entre sí mediante gRPC. Cada uno de estos servidores posee su propia base de datos MongoDB para la persistencia de datos. Todas las colas y tópicos creados por los clientes están particionados entre los servidores. Además, cada cola y cada tópico cuenta con una réplica en otro de los servidores, lo que permite soportar posibles fallos.

Se implementó Zookeeper para gestionar el registro de servidores activos, servidores caídos, colas disponibles, tópicos disponibles, clientes y tokens, así como las respectivas réplicas de colas y tópicos previamente mencionados.

Cada servidor mantiene el registro de seis clientes que pueden autenticarse en el sistema. Cada uno de estos clientes cuenta con un token único de conexión, el cual se conserva para validar futuras peticiones.

### Comunicación entre Clientes y Servidores

La comunicación entre los clientes y los servidores se realiza mediante peticiones HTTP usando una API REST. Cada vez que un cliente desea realizar una petición (inicio de sesión, creación de colas o tópicos, suscripción o cancelación de suscripción, envío o recepción de mensajes, manipulación de recursos, cierre de sesión, etc.), Zookeeper se encarga de asignar al azar uno de los servidores activos en ese momento.

El servidor asignado atenderá la petición si posee los recursos necesarios, o en su defecto, se encargará de realizar llamadas a procedimientos remotos (gRPC) hacia los servidores que contienen los recursos requeridos, devolviendo al cliente la respuesta correspondiente. Este servidor puede variar en cada nueva solicitud, ya que Zookeeper realiza una asignación aleatoria por cada petición, lo que añade tolerancia a fallos.

## Tareas Específicas

### Inicio de sesión

El cliente ingresa sus credenciales (usuario y contraseña). Zookeeper le asigna aleatoriamente un servidor, el cual se encargará de autenticar al usuario y generar su token de conexión.

### Creación de colas/tópicos

El cliente puede crear las colas/tópicos que considere necesarias ingresando el nombre deseado. Esta información se envía al servidor asignado mediante la API REST. El servidor crea la cola/tópico en su base de datos local y selecciona otro servidor para crear una réplica de la cola/tópico mediante gRPC. En ese servidor se crea una cola/tópico con el mismo nombre seguido del sufijo "_replica". Al finalizar, se notifica al cliente que la cola/tópico ha sido creada y replicada exitosamente.

### Envío de mensajes a colas/tópicos

El cliente puede enviar mensajes a cualquier cola/tópico disponible, sin necesidad de estar suscrito a ella. Para esto, proporciona el nombre de la cola/tópico a la que desea enviar el mensaje. El servidor asignado verifica si tiene la cola/tópico localmente. Si es así, añade el mensaje a la lista de mensajes pendientes. De lo contrario, consulta a Zookeeper para identificar el servidor responsable y utiliza gRPC para insertar el mensaje. Luego, también se actualiza la réplica correspondiente mediante gRPC. Finalmente, se notifica al cliente que el mensaje fue enviado exitosamente.

### Recepción de mensajes

El cliente puede recibir mensajes de cualquier cola/tópico a la que esté suscrito. Para ello, proporciona el nombre de la cola. El servidor asignado busca la cola localmente o realiza una consulta remota si es necesario. También se actualiza la réplica correspondiente. Además, este proceso incorpora una política de reparto equitativo (Round Robin) entre los suscriptores: un cliente no puede recibir dos mensajes consecutivos si hay otros suscriptores pendientes por atender. Al finalizar, se entrega al cliente el mensaje solicitado.

En el caso de los tópicos, cuando el cliente entra a la sección de tópicos se crea un hilo que se encarga de preguntar a los servidores correspondientes si tienen algún mensaje pendiente para este usuario. El mensaje no se borrará hasta que todos los clientes suscritos a dicho tópico lo reciban.

Inicialmente, siempre se trata de comunicar con quien tenga la versión original de la cola/tópico (nombre sin ‘_replica’), sin embargo, en caso de que este servidor se encuentre caído, se tratará de localizar el servidor que tenga la réplica (nombre con ‘_replica’).

### Suscripción / Cancelación de suscripción a colas/tópicos

El cliente indica el nombre de la cola/tópico a la que desea suscribirse o de la que desea retirarse. El servidor asignado verifica si puede procesar la solicitud localmente. En caso contrario, identifica el servidor correspondiente mediante Zookeeper y realiza la operación vía gRPC. Posteriormente, se actualiza también la réplica del recurso. Finalmente, se envía una confirmación al cliente.

### Eliminación de colas/tópicos

El cliente selecciona la cola/tópico que desea eliminar. Si es el propietario de dicha cola/tópico, el servidor asignado la elimina junto con su réplica, siempre y cuando ambas existan y estén registradas correctamente en Zookeeper. En caso de que el cliente no sea el dueño de la cola/tópico que desea eliminar, no podrá realizar la acción, ya que el servidor se encarga de verificarlo.

Cuando el creador del tópico lo elimina, se informa a todos los suscriptores conectados que el tópico ha sido borrado.

## Tolerancia a Fallos y Redistribución Automática

El sistema cuenta con un mecanismo de tolerancia a fallos diseñado para garantizar alta disponibilidad y continuidad del servicio, incluso ante la caída de uno de los servidores MOM. Este mecanismo se basa en el uso de ZooKeeper para la detección de fallos y la coordinación entre servidores.

### Detección de caídas

Cada servidor MOM registra un nodo efímero en ZooKeeper que representa su estado activo. Estos nodos se eliminan automáticamente si el servidor se cae o pierde conexión, lo cual permite a los demás servidores detectar rápidamente la caída. Esta verificación se realiza mediante un proceso de vigilancia (watcher) activo sobre el conjunto de servidores.

### Redistribución automática

Una vez detectada la caída de un servidor MOM, se ejecuta un proceso de redistribución automática, liderado por el servidor que asume el rol de líder, el cual también fue seleccionado mediante ZooKeeper. Un servidor se considera caído en el momento en que pasa más de 10 minutos desconectado. Durante esos diez minutos, el sistema sigue funcionando adecuadamente gracias a las réplicas de las colas y tópicos.

Una vez un servidor se determina como caído, el líder es el encargado de lo siguiente:

- Identificar todas las colas y tópicos del servidor que ha caído (estas se redistribuirán).
- Buscar entre los servidores activos un servidor adecuado para redistribuir el recurso o su réplica.
- Verificar que el servidor candidato no cuente con la réplica del recurso a redistribuir, o en caso tal que el recurso sea una réplica, verificar que el candidato no cuente con la versión principal del recurso.
- Crear el recurso en el otro servidor activo seleccionado para volver a cumplir con el modelo de redundancia.
- Actualizar los registros en ZooKeeper para reflejar la nueva ubicación del recurso principal y su nueva réplica.

Este procedimiento asegura que todos los recursos siguen estando disponibles a pesar de la caída de un servidor.

Cuando el servidor pasa más de diez minutos desconectado y es marcado como un servidor caído, este se agrega al path "fallen servers" del Zookeeper.

### Reincorporación de un servidor caído

- **Antes de 10 minutos**: El servidor se comunica con los servidores que cuentan con una réplica de sus tópicos o colas y con los dueños de las réplicas que él posee para verificar si ha habido actualizaciones desde su caída. Si es necesario, actualiza sus datos con los más recientes.

- **Después de 10 minutos**: Se registra nuevamente en ZooKeeper mediante un nodo efímero, pero no recupera automáticamente sus recursos anteriores (colas, tópicos ni sus réplicas). Esto se debe a que, durante su ausencia, sus recursos ya fueron reasignados y actualizados por los otros servidores, y permitir que el servidor regresara con una versión antigua podría introducir inconsistencias.

Por lo tanto, el servidor reintegrado se une al clúster en estado limpio, esperando que se le asignen nuevas colas/tópicos o réplicas si el sistema lo requiere.

### Este enfoque garantiza que:

- No haya conflictos de versiones de colas o tópicos.
- No se pierda información ni se dupliquen mensajes.
- El sistema se mantenga coherente y funcional en todo momento.

## Generalidad Arquitectonicas del proyecto

![Image](https://github.com/user-attachments/assets/a3683fe3-42f7-4886-918b-8ff99a17499f)

El diagrama representa una arquitectura distribuida que simula un sistema MOM (Message-Oriented Middleware). Los clientes se conectan primero a Zookeeper, que actúa como coordinador central para gestionar la disponibilidad y descubrimiento de los servidores. Luego, los mensajes se enrutan hacia uno de los tres servidores disponibles (Server1, Server2 y Server3), cada uno con su propia base de datos para almacenamiento local y procesamiento independiente. Esta estructura permite escalabilidad, tolerancia a fallos y una comunicación eficiente entre componentes desacoplados.

## Componente de colas

![Image](https://github.com/user-attachments/assets/032ffc26-c969-49fb-b33a-c7c077fe4e66)

El diagrama muestra el funcionamiento de un sistema de colas FIFO (First In, First Out) dentro de una arquitectura de tipo MOM (Message-Oriented Middleware). Los Message Producers (productores de mensajes) generan mensajes que son enviados a una cola central, donde se almacenan en el orden en que llegan. Los Message Consumers (consumidores de mensajes) luego extraen los mensajes de la cola en ese mismo orden para procesarlos. Este mecanismo desacopla la producción y el consumo de mensajes, permitiendo mayor flexibilidad, escalabilidad y tolerancia a fallos en sistemas distribuidos.

## Componente de tópicos

![Image](https://github.com/user-attachments/assets/52432901-6197-4323-bb82-1d692d61bda9)

Este diagrama representa el modelo de comunicación Publish/Subscribe (publicar/suscribirse), típico en arquitecturas orientadas a mensajes. En este esquema, los Publishers envían mensajes a un Topic (tópico) sin conocer quién los recibirá. Por su parte, los Subscribers se suscriben al tópico y reciben automáticamente todos los mensajes publicados en él. Esta arquitectura permite una comunicación desacoplada, escalable y eficiente, ideal para sistemas con múltiples emisores y receptores que deben compartir información de forma simultánea.

### 3. Ambiente de ejecución y desarrollo

## Configuración de los servidores en AWS (EL proceso es el mismo para todos los servidores)

a. Crear una instancia con Ubuntu en AWS

b. Editar las reglas de entrada de la instancia y habilitar los siguientes puertos:

![Image](https://github.com/user-attachments/assets/046e3577-d976-47ad-afbc-b9f57fd155e1)

c. Ingresar a la MV ya sea por la terminal integrada en AWS o por SSH y ejecutar los siguientes comandos:

Para instalar la base de datos Mongo:

wget -qO - https://pgp.mongodb.com/server-7.0.asc | sudo tee /etc/apt/trusted.gpg.d/mongodb-server-7.0.asc

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list

sudo apt update && sudo apt install -y mongodb-org

Para ejecutar Mongo cada que se prenda la instancia:

sudo systemctl enable mongod

Inicializar el servicio:

sudo systemctl start mongod

Verificar que Mongo este corriendo correctamente:

sudo systemctl status mongod

Debería verse un mensaje: Active: active (running)

Instalación y configuración del proyecto:

git clone https://github.com/estebanm30/Proyecto-MOM.git

cd Proyecto-MOM/server/

Crear y editar el archivo .env

touch .env

nano .env

configurar el .env de la siguiente manera

DB_ADDRESS = ""  (dirección para conexión con mongo)
ZOOKEEPER_ADDRESS = "” (dirección IP de la instancia zookeeper)
SERVER_ID = ""    (dirección IP pública (elástica) del servidor)

Crear un environment e instalar dependencias:

sudo apt install python3 python3-venv -y

mkdir myapp && cd myapp

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

Hacer seed de la base de datos:

cd database

python3 seed.py

Ya estaría configurado el servidor, únicamente habría que ejecutar en el directorio server

python3 main.py 

## Configuración del zookeeper en AWS:

a. Crear una instancia con Ubuntu en AWS

b. Editar las reglas de entrada de la instancia y habilitar los siguientes puertos:

![Image](https://github.com/user-attachments/assets/4ec2dbf9-68ad-4d73-8b96-e96fbd4066d1)

c. Ingresar a la MV ya sea por la terminal integrada en AWS o por SSH y ejecutar los siguientes comandos:

sudo apt update && sudo apt upgrade -y

Instalar Java, ya que zookeeper lo requiere:

sudo apt install openjdk-17-jre -y
Verificar la correcta instalación con 	java -version
Descargar e instalar apache Zookeeper:

wget https://downloads.apache.org/zookeeper/stable/apache-zookeeper-3.8.3-bin.tar.gz

Descomprimir el archivo

tar -xvzf apache-zookeeper-3.8.3-bin.tar.gz

Renombrar la carpeta:

mv apache-zookeeper-3.8.3-bin zookeeper

Copiar el archivo de configuración del zookeeper

cp zookeeper/conf/zoo_sample.cfg zookeeper/conf/zoo.cfg

Editar el archivo:

nano zookeeper/conf/zoo.cfg

Asegurarse de que este así:
tickTime=2000
dataDir=/var/lib/zookeeper
clientPort=2181
initLimit=5
syncLimit=2

Crear la carpeta de datos:

sudo mkdir -p /var/lib/zookeeper

sudo chown ubuntu:ubuntu /var/lib/zookeeper

Configurar para que el zookeeper corra al iniciar la instancia:

sudo nano /etc/systemd/system/zookeeper.service

Añadir lo siguiente:
[Unit]
Description=Apache Zookeeper Server
After=network.target

[Service]
Type=forking
User=ubuntu
ExecStart=/home/ubuntu/zookeeper/bin/zkServer.sh start
ExecStop=/home/ubuntu/zookeeper/bin/zkServer.sh stop
Restart=always

[Install]
WantedBy=multi-user.target
Guardar y ejecutar lo siguiente:
sudo systemctl daemon-reload
sudo systemctl enable zookeeper
sudo systemctl start zookeeper
Verificar que el zookeeper este activo
sudo systemctl status zookeeper


### 5. Información relevante


Estructura de colas y tópicos:

{
	_id,
	name: ‘ ’,
	subscribers = [],
	messages: [],
	pending_messages: {},
	owner: ‘ ’,
	update_date: ISODate()
}

Rutas Zookeeper:
/fallen_servers (Indica los servidores que cayeron por más de 10 minutos)
/leader (Solo uno de los servidores mom es el lider y encargado de la redistribución en caso de fallas permanentes)
/mom_queues (Localiza quienes tienen las colas originales)
/mom_queues_replicas (Localiza quienes tienen las réplicas de las  colas originales)
/mom_topics (Localiza quienes tienen los tópicos originales) 
/mom_topics_replicas (Localiza quienes tienen las réplicas de los tópicos originales)
/round_robin_index (Permite usar el RB para la replicación de los datos)
/servers (indica cuáles servidores están disponibles en el momento)
/tokens (Almacena los tokens de usuarios autenticados, para cada operación se verifica que el token del cliente que hace la petición esté guardada acá)

