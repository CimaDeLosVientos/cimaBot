from ..util.telegram_methods import *
from ..util.methods import *
from ..util.checkinator import *
from ..util.states_handler import *

###############
# MENÚ DE ROL #
###############
class RolHelpMenusHandler(object):
    def __init__(self, database):
        self.database = database


    def command_rol(self, arguments):
        if arguments['chat'] in USERS:
            items = [["Registrar un nuevo aventurero 🧙‍♂️"], ["Ascender a un aventurero 🧝‍♀️⏏️"], ["Calcular experiencia 🧮"], ["Repartir experiencia extra 🆓"], ["Repartir recompensas 💰"], ["Cobrar a un aventurero 🏦"], ["Buscar aventureros 🗂"], ["Publicar una misión 📰"], ["Registrar un informe de misión 📝"], ["Buscar misiones 📖"], ["Inscribirse en un torneo 🏆"], ["Ver torneos 📜"], ["Aposteitor 💸"]]
            keyboard = build_keyboard(items)
            send_message("Selecciona la opción que deseas realizar.", arguments['chat'], keyboard)
        send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    def command_nuevo_aventurero(self, arguments):
        if arguments['chat'] in USERS:
            send_message("Para añadir un nuevo aventurero, utiliza el comando /nuevo_aventurero seguido de su nombre, su nivel, su rango, sus puntos de experiencia y su dinero. Ejemplo: /nuevo_aventurero Jon Snow 5 Novato 16300 20.3. \nTen en cuenta que el aventurero se asignará a tu perfil, no registres aventureros de otros.", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    def command_ascender(self, arguments):
        if arguments['chat'] in USERS:
            send_message("Para ascender a un aventurero, utiliza el comando /ascender seguido del nombre del aventurero y su nuevo rango. Ejemplo: /ascender Jon Snow Veterano", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    def command_buscar_aventureros(self, arguments):
        if arguments['chat'] in USERS:
            send_message("Utiliza los comandos /personajes seguido del nombre de un jugador o /rango seguido de un rango para ver la lista de personajes con esas características. Ejemplos: /personajes Luis o /rango Novato", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])


    def command_calcular_experiencia(self, arguments):
        if arguments['chat'] in USERS:
            send_message("Para calcular la experiencia por combate, introduce los monstruos derrotados usando el comando /monstruo seguido de la cantidad de monstruos de ese tipo y de su Valor de Desafío (un comando por cada tipo de criatura). Ejemplo: /monstruo 2 8 añadiría dos monstruos de VD 8. \n A continuación añade los aventureros participantes usando el comando /aventurero seguido de su nombre (deben estar registrado en la base de datos). Ejemplo: /aventurero Jon Snow. \n Por último, utiliza el comando /calcular para indicar que has acabado de introducir los datos y recibirás la experiencia a repartir.", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    def command_repartir_experiencia(self, arguments):
        if arguments['chat'] in USERS:
            send_message("Para repartir experiencia extra por una partida, usa el comando /repartir_exp seguido del nombre del personaje y la cantidad de experiencia que quieres darle. Ejemplo: /repartir_exp Jon Snow 350.", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    def command_repartir_recompensas(self, arguments):
        if arguments['chat'] in USERS:
            send_message("Para repartir el dinero de una misión a un personaje, utiliza el comando /repartir_recompensa seguido del nombre del personaje y la cantidad que le corresponda. Ejemplo: /repartir_recompensa Jon Snow 10", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    def command_cobrar(self, arguments):
        if arguments['chat'] in USERS:
            send_message("Para cobrar dinero a un aventurero, utiliza el comando /cobrar seguido del nombre del personaje y la cantidad a retirar. Ejemplo: /cobrar Jon Snow 100", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    def command_publicar_mision(self, arguments):
        if arguments['chat'] in USERS:
            send_message("Para publicar una misión, envíame el texto comenzando con #nombreDeLaMision y a continuación el mensaje de la misión. Ejemplo: #orcosSexysEnTuZona blablabla. Si lo envías al grupo, anclaré el mensaje, si no, simplemente lo reenviaré.", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    def command_registrar_mision(self, arguments):
        if arguments['chat'] in USERS:
            send_message("Para registrar una misión, envíame el informe con el siguiente formato:\n /nueva_mision \n #nombreDeLaMision \n díaDeLaSemana dd/mm/aaa \n Lista de personajes que asistieron \n Pequeño resumen de la misión.", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    def command_buscar_mision(self, arguments):
        if arguments['chat'] in USERS:
            send_message("Para ver la lista de las últimas misiones, usa el comando /ultimas_misiones. Para buscar una misión concreta, utiliza el comando /mostrar_mision seguido del identificador. Por ejemplo: /mostrar_mision #ElVigiaSiniestro", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])


    def command_ver_torneos(self, arguments):
        if arguments['chat'] in USERS:
            t = TOURNAMENTS[0]
            for x in range(1,len(TOURNAMENTS)):
                t = t + ", " + TOURNAMENTS[x]
            send_message("Para ver las inscripciones a los torneos utiliza el comando /inscripciones. Si quieres consultar las inscripciones de un torneo concreto, añade el nombre del torneo después del comando. Los torneos disponibles son: {}".format(t), arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])


    def command_aposteitor(self, arguments):
        if arguments['chat'] in USERS:
            send_message("Para iniciar una ronda de apuestas, utiliza el comando /nueva_ronda indicando el nombre de los competidores. Ejemplo: /nueva_ronda Gandalf Saruman  \nUna vez hayas especificado los contendientes, se podrán realizar apuestas usando el comando /apostar seguido del nombre del personaje que apuesta y la cantidad apostada, se te pedirá a continuación que elijas por quién quieres apostar. Ejemplo: /apostar Frodo 100 \nCuando se haya determinado el ganador del combate, utiliza el comando /ganador para resolver las ganancias y pérdidas de cada uno de los apostantes. Ejemplo: /ganador Gandalf\n\n El módulo de apuestas funciona usando el framework «Aposteitor» de @Seind", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

