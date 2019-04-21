# cimaBot
Bot de Telegram para ayudarnos en nuestras tareas cotidianas. #Python #SQLite #TelegramAPI
El bot cuenta con dos módulos:
## Módulo de finanzas
Diseñado para llevar el registro de compras e ingresos de las cuotas de miembro
## Módulo de Rol
Diseñado para simplificar las tareas del máster. Incluye un registro de personajes, una calculadora de experiencia y una función para publicar una nueva misión en el tablón del gremio.
## Instrucciones de instalación y puesta en marcha
### Herramientas necesarias
Para poder ejecutar el bot, deberás tener instalado en tu ordenador python3, pip3 y el paquete requests (puedes instalarlo escribiendo "pip3 install requests" en una terminal una vez tengas lo anterior)
### Registrar tu bot en Telegram
Deberás iniciar un chat con @BotFather y seguir los pasos que te indica para registrar tu bot. Al final del proceso recibirás un TOKEN, un identificador del bot, que deberás guardar y no compartir con nadie. A través de él controlarás tu bot.
### Ejecución de tu bot
- Descarga los archivos .py del repositorio y guárdalos juntos en un directorio que puedas localizar fácilmente. Este será el directorio de trabajo del bot. 
- A continuación, abre el archivo cdlv.py con un editor de textos. Verás una serie de campos que puedes modificar para adaptar el bot a tu criterio. El más importante es la variable TOKEN, donde deberás poner el código que obtuviste en el paso anterior.
- También puedes, y debes, rellenar las listas de miembros con acceso al bot con los IDs de Telegram de cada miembro. Para hallar el ID de una persona, puedes reenviar un mensaje suyo al bot @ForwardInfoBot, que te responderá con un mensaje en el que aparecerá el ID como un código numérico al lado del @username
- Opcionalmente, puedes elegir un administrador, añadiendo su ID a la variable ADMIN
- Para usar la función "Publicar una misión en el tablón", deberás añadir tu bot a un grupo y concederle permisos de administrador. Además, deberás añadir el ID del grupo a la variable GROUPID. Para localizar el ID del grupo, deberás poner en marcha el bot y añadirlo a dicho grupo. Recibirás una actualización en la consola de comandos y deberás localizar el texto '"chat":{"id":-xxxxxx}' donde "-xxxxxxxxx" es el número que buscas.
- Para ejecutar el bot, navega desde la terminal hasta el directorio donde guardaste los archivos .py y ejecuta el comando "python3 cdlv.py". A partir de ese momento, tu bot estará operativo y podrá responder a tus mensajes. Podrás ver en la terminal todos los mensajes que le lleguen y, en caso de surgir algún problema, se te notificará también en la terminal.
### Acerca del cimaBot
El bot ha sido desarrollado por @Luis_gar y @Seind como parte de la actividad de la Asociación https://t.me/cimadelosvientos (@CimaDelViento en Twitter)
