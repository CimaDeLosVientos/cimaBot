from ..util.telegram_methods import *
from ..util.methods import *
from ..util.checkinator import *
from ..util.states_handler import *

#########################
# MENÚ DE LA ASOCIACIÓN #
#########################
class AsocHelpMenusHandler(object):
    def __init__(self, database):
        self.database = database


    def command_finanzas(self, arguments):
        print("1")
        if arguments['chat'] in USERS:
            print("2")
            items = [["Registrar un ingreso 📥"], ["Registrar un pago 📤"], ["Consultar saldo 📊"], ["Consultar transacciones de un miembro 🧾👩‍💼"], ["Consultar últimas transacciones 🧾👨‍👩‍👦‍👦"]]
            keyboard = build_keyboard(items)
            send_message("Selecciona la opción que deseas realizar.", arguments['chat'], keyboard)
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])  
      
    def command_ingreso(self, arguments):
        if arguments['chat'] in USERS:
            send_message("Para realizar un ingreso, utiliza el comando /ingreso seguido del nombre de la persona que lo hizo, la fecha en formato dd/mm/aa y la cantidad aportada. Ejemplo: /ingreso Juan 12/03/19 5", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    def command_pago(self, arguments):
        if arguments['chat'] in USERS:
            send_message("Para realizar un pago, utiliza el comando /pago seguido del nombre de la persona a la que se pagó, la fecha en formato dd/mm/aa y la cantidad pagada. Ejemplo: /pago Juan 12/03/19 5", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    def command_saldo(self, arguments):
        if arguments['chat'] in USERS:
            total(db, arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    def command_transacciones(self, arguments):
        if arguments['chat'] in USERS:
            send_message("Para consultar las transacciones de un miembro, utiliza el comando /miembro seguido del nombre de la persona. Ejemplo; /miembro Juan", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    def command_ultimas_transacciones(self, arguments):
        if arguments['chat'] in USERS:
            last(db, arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    def command_eliminar_transaccion(self, arguments):
        if arguments['chat'] in ADMIN:
            db.del_last()
            send_message("Transacción eliminada con éxito", arguments['chat'])


#########################
# CAJA DE LA ASOCIACIÓN #
#########################

    @checkinator(("name", check_string), ("date", check_date), ("money", check_positive_int), contains_command=True)
    def inline_ingreso(self, arguments):
        print(arguments['date'])
        income(db, arguments['name'], arguments['date'], arguments['money'], arguments['chat'])
        cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
        write_log(USERSDICT[arguments['user']], arguments['text'])


    @checkinator(("name", check_string), ("date", check_date), ("money", check_positive_int), contains_command=True)
    def inline_pago(self, arguments):
        payment(db, arguments['name'], arguments['date'], arguments['money'], arguments['chat'])
        cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
        write_log(USERSDICT[arguments['user']], arguments['text'])

    def inline_miembro(self, arguments):
        data = arguments['text'].split()
        if len(data) == 2:
            member(db, data[1], arguments['chat'])
        else:
            send_message("Número de datos incorrecto. La sintaxis es /miembro nombre", arguments['chat'])    
