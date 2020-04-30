# coding=utf-8
import json
import requests
import time
import urllib
import sys
import math
import random

from .config import *

from .util.methods import income, payment, total, member, last, characters, ranks, mergeMonsters, giveExp, giveMoney, takeMoney, showQuests, findQuest, showTriggers, showTournament, showInscriptions
from .util.telegram_methods import *
from .util.db_helper import DBHelper
from .util.checkinator import *
from .util.states_handler import *

from .handlers import prueba
from .handlers.aposteitor_handler import AposteitorHandler



db = DBHelper("./data_base_files/finances.sqlite")
aventureros = DBHelper("./data_base_files/adventurers.sqlite")
misiones = DBHelper("./data_base_files/missions.sqlite")
triggers = DBHelper("./data_base_files/triggers.sqlite")
cambios = DBHelper("./data_base_files/log.sqlite")
inscripciones = DBHelper("./data_base_files/registrations.sqlite")

aposteitor = AposteitorHandler(aventureros)
######################################################################
#################### PARÁMETROS MODIFICABLES #########################
######################################################################


RANGOS = ["Novato","Novata","Veterano","Veterana","Élite","Comandante"]

TOURNAMENTS = [str("Tiro 🏹"), str("Fuerza 🏋️‍♀️"), str("Obstáculos 🚧🏃‍♂️"), str("Magia 🔮")]

######################################################################

URL = "https://api.telegram.org/bot{}/".format(TOKEN)

monsters = []
chars = []
monstersOK = []
charsOK = []


betState = 0
participantes = []
# ronda = app.Ronda()
# ronda.loadPNJs()
MAXBETS = 20


### Añadidas por Adri

###



expTable = [
[300,600,900,1350,1800,2700,3600,5400,7200,10800,0,0,0,0,0,0,0,0,0,0],
[300,600,900,1350,1800,2700,3600,5400,7200,10800,0,0,0,0,0,0,0,0,0,0],
[300,600,900,1350,1800,2700,3600,5400,7200,10800,0,0,0,0,0,0,0,0,0,0],
[300,600,800,1200,1600,2400,3200,4800,6400,9600,12800,0,0,0,0,0,0,0,0,0],
[300,500,750,1000,1500,2250,3000,4500,6000,9000,12000,18000,0,0,0,0,0,0,0,0],
[300,450,600,900,1200,1800,2700,3600,5400,7200,10800,14400,21600,0,0,0,0,0,0,0],
[263,394,525,700,1050,1400,2100,3150,4200,6300,8400,12600,16800,25200,0,0,0,0,0,0],
[200,300,450,600,800,1200,1600,2400,3600,4800,7200,9600,14400,19200,28800,0,0,0,0,0],
[0,225,338,506,675,900,1350,1800,2700,4050,5400,8100,10800,16200,21600,32400,0,0,0,0],
[0,0,250,375,563,750,1000,1500,2000,3000,4500,6000,9000,12000,18000,24000,36000,0,0,0],
[0,0,0,275,413,619,825,1100,1650,2200,3300,4950,6600,9900,13200,19800,26400,39600,0,0],
[0,0,0,0,300,450,675,900,1200,1800,2400,3600,5400,7200,10800,14400,21600,28800,43200,0],
[0,0,0,0,0,325,488,731,975,1300,1950,2600,3900,5850,7800,11700,15600,23400,31200,46800],
[0,0,0,0,0,0,350,525,788,1050,1400,2100,2800,4200,6300,8400,12600,16800,25200,33600],
[0,0,0,0,0,0,0,375,563,844,1125,1500,2250,3000,4500,6750,9000,13500,18000,27000],
[0,0,0,0,0,0,0,0,400,600,900,1200,1600,2400,3200,4800,7200,9600,14400,19200],
[0,0,0,0,0,0,0,0,0,425,638,956,1275,1700,2550,3400,5100,7650,10200,15300],
[0,0,0,0,0,0,0,0,0,0,450,675,1013,1350,1800,2700,3600,5400,8100,10800],
[0,0,0,0,0,0,0,0,0,0,0,475,713,1069,1425,1900,2850,3800,5700,8550],
[0,0,0,0,0,0,0,0,0,0,0,0,500,750,1000,1500,2000,3000,4000,6000]
]




# Aquí estaba el manejador de estados


########################
## HANDLER OF UPDATES ##
########################

def handle(update):
    """
    This function is called every time a message arrives to any chat.
    Extracts the key arguments of the update in a dictionary and evaluate what command it is or if is there ongoing process.
    Finally, executes the command invoked in the chat or the next step from ongoing process through the corresponding function and its parameters.
    It also handles exceptions during execution.

    
    :param      update:  The update
    :type       update:  Update
    """

    db.setup_finantial()
    aventureros.setup_adventurers()
    misiones.setup_quests()
    triggers.setup_triggers()
    cambios.setup_changes()
    inscripciones.setup_enrollment()

    if 'message' in update and 'text' in update["message"]:
            arguments = {
                'text' : update["message"]["text"],
                'chat' : update["message"]["chat"]["id"],
                'user' : update["message"]["from"]["id"],
                'message' : update["message"]["message_id"]
            }
            if not arguments['user'] in USERS:
                send_message("Aún no tienes acceso a este bot.", arguments['chat'])
                return
    else:
        return

    try:
        if arguments['text'] == "/abort":
            if arguments['chat'] in ongoing_processes.keys() and arguments['user'] in ongoing_processes[arguments['chat']].keys():
                ongoing_processes[arguments['chat']][arguments['user']].finish_ongoing_process()
                send_message("El proceso por pasos en curso de {} ha sido detenido.".format(update["message"]["from"]["first_name"]), arguments['chat'])
            else:
                send_message("{} no tienes ningún proceso por pasos en curso.".format(update["message"]["from"]["first_name"]), arguments['chat'])
        # Ongoing process
        if arguments['chat'] in ongoing_processes.keys() and arguments['user'] in ongoing_processes[arguments['chat']].keys():
            ongoing_processes[arguments['chat']][arguments['user']].run(arguments)
        else:
            # First, check if the message is a registered trigger
            answer = triggers.get_trigger(arguments['text'])
            if answer:
                if answer[0][1] == "texto":
                    send_message("{}".format(answer[0][2]), arguments['chat'])
                elif answer[0][1] == "foto":
                    print(answer)
                    send_photo("{}".format(answer[0][2]), arguments['chat'])
                elif answer[0][1] == "gif":
                    send_gif("{}".format(answer[0][2]), arguments['chat'])
                else:
                    send_message("Ese archivo no está soportado aún.", arguments['chat'])
            # New command without backslash
            elif arguments['text'] in commands_without_backslash.keys():
                commands_without_backslash[arguments['text']](arguments)
            # New mission to publish
            elif arguments['text'].startswith("#"):
                if chat in USERS:
                    forward_message(GROUPID, arguments['chat'], arguments['message'])
                    pin_message(GROUPID,message, False)
                else:
                    pin_message(GROUPID,message, False)
            # New command with backslash
            else:
                command = arguments['text'].split()
                if command[0] in commands_with_backslash.keys():
                    # print(command[0])
                    if command[0] == "/set_trigger":
                        arguments = update
                    commands_with_backslash[command[0]](arguments)    
  
    except (ValueError, TypeError, EnvironmentError, ReferenceError) as complaint: # Maybe names are not necessary
        print(complaint.args)
        send_message(complaint.args[0], arguments['chat'])
        


######################
## GENERIC COMMANDS ##
######################


## Generic comands

def command_ping(arguments):
    """
    Classic ping. Checks bot's state.
  
    :param      arguments:  The arguments
    :type       arguments:  Dictionary
    """
    send_message("Estoy vivo", arguments['chat'])


def command_echo(arguments):
    """
    Classic echo. Repeat message
    
    :param      arguments:  The arguments
    :type       arguments:  Dictionary
    """
    message = arguments['text'][5:] # Remove "/echo " from message
    send_message(message, arguments['chat'])


@checkinator(("roll", check_dices), contains_command=True)
def command_roll(arguments):
    """
    generates a dice roll according to the format <dice - <amount + <bonus>.
    The parameters "- <amount>" and "+ <bonus>" are optional.
    
    :param      arguments:          The arguments
    :type       arguments:          Dictionaryx
    :param      arguments['roll']:  Data of dice, amount and bonus
    :type       arguments['roll']:  Tuple
    """
    message = ""
    result = 0
    for individual_roll in range(arguments['roll'][1]):
        individual_roll = random.randrange(arguments['roll'][0]) + 1
        message += "{}\n".format(individual_roll)
        result += individual_roll
    message += "----\t+{}\n{}".format(arguments['roll'][2], result + arguments['roll'][2])
    send_message(message, arguments['chat'])


def command_start(arguments):
    if arguments['chat'] in USERS:
        send_message("Bienvenido al bot de ayuda de La Cima De Los Vientos. Para ver el Menú principal, usa el comando /menu", arguments['chat'])

def command_menu(arguments):
    if arguments['chat'] in USERS:
        items = [["💶️ Finanzas 💶️"], ["⚔️ Rol ⚔️"]]
        keyboard = build_keyboard(items)
        send_message("Selecciona una función", arguments['chat'], keyboard)

def command_help(arguments):
    send_message("Emosido engañados", arguments['chat'])

#def command_add_user():


@checkinator(("element_1", check_positive_int), contains_command=True)
def command_sum(arguments):
    """
    Example of step execution. Add two numbers

    :param      arguments:  The arguments
    :type       arguments:  Dictionary
    """
    send_message("dame mas", arguments['chat'])
    NextStep(arguments, result_sum)


@checkinator(("element_2", check_positive_int), contains_command=False)
def result_sum(arguments):
    """
    Example of step execution. Add two numbers
    
    :param      arguments:  The arguments
    :type       arguments:  Dictionary
    """
    print(arguments)
    send_message("El resultado de {} + {} es {}".format(arguments['element_1'], arguments['element_2'], arguments['element_1'] + arguments['element_2']), arguments['chat'])




## AQUI ESTABA EL APOSTEITOR





###############
# AVENTUREROS #
###############
@checkinator(("name", check_string), ("lvl", check_positive_int), ("rank", check_rank), ("exp", check_positive_int), ("money", check_positive_int), contains_command=True)
def inline_nuevo_aventurero(arguments):
    if arguments['chat'] in USERS:
        adv = aventureros.get_pj(arguments['name'])
        if not adv:
            aventureros.add_adventurer(USERSDICT[arguments['user']], arguments['name'], arguments['lvl'], arguments['rank'], arguments['exp'], arguments['money'])
            cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
            write_log(USERSDICT[arguments['user']], arguments['text'])
            send_message("Aventurero añadido con éxito.", arguments['chat'])
        else:
            send_message("Este aventurero ya ha sido registrado previamente.", arguments['chat'])


@checkinator(("name", check_string), ("rank", check_rank), contains_command=True)
def inline_ascender(arguments):
    auxChar = aventureros.get_pj(arguments['name'])
    if auxChar:   
        aventureros.rank_up(arguments['name'], arguments['rank'])
        cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
        write_log(USERSDICT[arguments['user']], arguments['text'])
        send_message("Ascenso realizado con éxito", arguments['chat'])
    else:
        send_message("El aventurero especificado no existe.", arguments['chat'])    


@checkinator(("name", check_string), ("exp", check_positive_int), contains_command=True)
def inline_repartir_exp(arguments):
    if arguments['chat'] in USERS:
        auxChar = aventureros.get_pj(arguments['name'])
        if auxChar:
            giveExp(aventureros, auxChar[0][0], auxChar[0][1], auxChar[0][2], arguments['exp'], arguments['chat'])
            cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
            write_log(USERSDICT[arguments['user']], arguments['text'])
            send_message("Experiencia repartida con éxito.", arguments['chat'])
            string = auxChar[0][1] + " ha recibido " + str(arguments['exp']) + " puntos de experiencia extra."
            send_personal_message(string, auxChar[0][0])
        else:
            send_message("El aventurero especificado no existe.", arguments['chat'])


@checkinator(("name", check_string), ("loot", check_positive_int), contains_command=True)
def inline_repartir_recompensa(arguments):
    if arguments['chat'] in USERS:
        auxChar = aventureros.get_pj(arguments['name'])
        if auxChar:
            giveMoney(aventureros, auxChar[0][1], arguments['loot'])
            cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
            write_log(USERSDICT[arguments['user']], arguments['text'])
            send_message("Recompensa añadida a la bolsa del personaje.", arguments['chat'])
        else:
            send_message("El aventurero especificado no existe.", arguments['chat'])


@checkinator(("name", check_string), ("invoice", check_positive_int), contains_command=True)
def inline_cobrar(arguments):
    auxChar = aventureros.get_pj(arguments['name'])
    if auxChar:
        takeMoney(aventureros, auxChar[0][1], arguments['invoice'])
        cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
        write_log(USERSDICT[arguments['user']], arguments['text'])
        send_message("La cantidad fue cobrada de la bolsa del personaje.", arguments['chat'])
    else:
        send_message("El aventurero especificado no existe.", arguments['chat'])

def inline_personajes(arguments):
    data = arguments['text'].split()
    if len(data) == 2:
        characters(aventureros, data[1], arguments['chat'])
    else:
        send_message("Número de datos incorrecto. La sintaxis es /personajes NombreJugador", arguments['chat'])

def inline_rango(arguments):
    data = arguments['text'].split()
    if len(data) == 2:
        ranks(aventureros, data[1], arguments['chat'])
    else:
        send_message("Número de datos incorrecto. La sintaxis es /rango rangoABuscar", arguments['chat'])

#########################
# CAJA DE LA ASOCIACIÓN #
#########################

@checkinator(("name", check_string), ("date", check_date), ("money", check_positive_int), contains_command=True)
def inline_ingreso(arguments):
    print(arguments['date'])
    income(db, arguments['name'], arguments['date'], arguments['money'], arguments['chat'])
    cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
    write_log(USERSDICT[arguments['user']], arguments['text'])


@checkinator(("name", check_string), ("date", check_date), ("money", check_positive_int), contains_command=True)
def inline_pago(arguments):
    payment(db, arguments['name'], arguments['date'], arguments['money'], arguments['chat'])
    cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
    write_log(USERSDICT[arguments['user']], arguments['text'])

def inline_miembro(arguments):
    data = arguments['text'].split()
    if len(data) == 2:
        member(db, data[1], arguments['chat'])
    else:
        send_message("Número de datos incorrecto. La sintaxis es /miembro nombre", arguments['chat'])    

############
# MISIONES #
############

def inline_ultimas_misiones(arguments):
    data = arguments['text'].split()
    if len(data) == 1:
        showQuests(misiones, arguments['chat'])
    else:
        send_message("Número de datos incorrecto. La sintaxis es /ultimas_misiones", arguments['chat'])

def inline_mostrar_mision(arguments):
    data = arguments['text'].split()
    if len(data) == 2:
        findQuest(misiones, data[1], arguments['chat'])
    else:
        send_message("Número de datos incorrecto. La sintaxis es /mostrar_mision #mision", arguments['chat'])


def inline_nueva_mision(arguments):
    data = arguments['text'].splitlines()
    if len(data) == 5:
        if data[1].startswith("#"):
            date = data[2].split()
            if len(date) == 2:
                dateNums = date[1].split("/")
                if len(dateNums) == 3:
                    misiones.add_quest(data[1], date[0], dateNums[0], dateNums[1], dateNums[2], data[3], data[4])
                    cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
                    write_log(USERSDICT[arguments['user']], arguments['text'])
                    send_message("Informe de misión registrado. Gracias, aventureros.", arguments['chat'])
                else:
                    send_message("Formato incorrecto. La fecha debe separarse con /.", arguments['chat'])
            else:
                send_message("Formato incorrecto. El día debe separarse de la fecha por un espacio.", arguments['chat'])
        else:
            send_message("Formato incorrecto. El identificador de la misión debe empezar por #", arguments['chat'])  
    else:
        send_message("Número de datos incorrecto. Introduce el #identificador de la misión, la fecha, un pequeño resumen y los personajes que la realizaron separados por saltos de línea", arguments['chat'])



############
# TRIGGERS #
############
def command_set_trigger(update):
    data = update["message"]["text"].split(' ', 1)[1]
    #print(len(data))
    if len(data) > 0:
        if 'reply_to_message' in update["message"]:
            if 'text' in update["message"]["reply_to_message"]:                               
                triggers.add_trigger(data, "texto", update["message"]["reply_to_message"]["text"])
                send_message("Trigger añadido correctamente.", update["message"]["chat"]["id"])
            if 'photo' in update["message"]["reply_to_message"]:
                fileID =  update["message"]["reply_to_message"]["photo"][-1]["file_id"]
                triggers.add_trigger(data, "foto", fileID)
                send_message("Trigger añadido correctamente.", update["message"]["chat"]["id"])
            if 'animation' in update["message"]["reply_to_message"]:
                fileID =  update["message"]["reply_to_message"]["animation"]["file_id"]
                triggers.add_trigger(data, "gif", fileID)
                send_message("Trigger añadido correctamente.", update["message"]["chat"]["id"])
        else:
            send_message("Para crear un trigger, responde a un mensaje con el comando /set_trigger y el nombre.", update["message"]["chat"]["id"])
    else:
        send_message("Número de datos incorrecto", update["message"]["chat"]["id"])   
         
def command_mostrar_triggers(arguments):
    data = arguments['text'].split()
    if len(data) == 1:
        showTriggers(triggers, arguments['chat'])
    else:
        send_message("Número de datos incorrecto. La sintaxis es /mostrar_triggers", arguments['chat'])

##############################
# CALCULADORA DE EXPERIENCIA #
##############################
def inline_monstruo(arguments):
    if arguments['chat'] in USERS:
        data = arguments['text'].split()
        if len(data) == 3:
            d = float(data[2])
            if float(d > 0 and d < 21):
                if d >= 1:
                    d = int(data[2])
                aux = [arguments['user'],int(data[1]),d]
                monsters.append(aux)
                yourMonsters = ""
                for x in monsters:
                   if x[0] == arguments['user']:
                        if arguments['user'] not in monstersOK:
                            monstersOK.append(arguments['user'])
                        yourMonsters = yourMonsters + str(x[1]) + " monstruos de VD " + str(x[2]) + "\n"
                send_message("Monstruos añadidos: \n {}".format(yourMonsters), arguments['chat']);
            else:
                send_message("El VD del monstruo introducido no es válido. Debe estar comprendido entre 1 y 20.", arguments['chat'])
        else:
            send_message("Número de datos incorrecto. La sintaxis es /monstruo Cantidad VD", arguments['chat'])
        yourMonsters = ""


def inline_aventurero(arguments):
    if arguments['chat'] in USERS:
        data = arguments['text'].split()
        l = len(data)
        if l > 1:
            name = data[1]
            if l > 2:
                for x in range (2,l):
                    name = name + data[x]
            auxChar = aventureros.get_pj(name)
            if auxChar:
                k = len(auxChar[0])
                aux = [arguments['user'], name, int(auxChar[0][k-4]), 0]
                chars.append(aux)
                yourChars = ""
                for x in chars:
                    if x[0] == arguments['user']:
                        if arguments['user'] not in charsOK: 
                            charsOK.append(arguments['user'])
                        yourChars = yourChars + x[1] + " de nivel " + str(x[2]) + "\n"
                send_message("Aventureros añadidos: \n {}".format(yourChars), arguments['chat']);
            else:
                send_message("El nombre que has introducido no corresponde a ningún aventurero existente", arguments['chat'])
        else:
            send_message("Número de datos incorrecto. La sintaxis es /aventurero NombrePJ", arguments['chat'])
        yourChars = ""

def inline_calcular(arguments):
    if arguments['chat'] in USERS:
        data = arguments['text'].split()
        if len(data) == 1:
            if arguments['user'] in monstersOK and arguments['user'] in charsOK:
                yourMonsters = []
                for x in monsters:
                    if x[0] == arguments['user']:
                        yourMonsters.append(x)
                yourChars = []
                for x in chars:
                    if x[0] == arguments['user']:
                        yourChars.append(x)
                VDs = mergeMonsters(yourMonsters, arguments['chat'])
                exp = 0
                report = ""
                l = len(yourChars)
                for c in yourChars:
                    for monster in VDs:
                        exp = exp + expTable[c[2]-1][monster-1]
                    c[3] = exp / l
                    exp = 0
                    string = c[1] + " recibe: " + str(round(c[3])) + " puntos de experiencia \n"
                    report = report + string
                    giveExp(aventureros, c[0], c[1], c[2], round(c[3]), arguments['chat'])
                    send_personal_message(string, c[0])
                send_message(report, arguments['chat'])
                cambios.add_change(USERSDICT[arguments['user']], report)
                write_log(USERSDICT[arguments['user']], report)
    
                f = 1
                while f == 1:
                    f = 0
                    for x in range (0,len(monsters)):
                        if arguments['user'] in monsters[x]:
                            monsters.pop(x)
                            f = 1
                            break
                            
                f = 1
                while f == 1:
                    f = 0
                    for x in range (0, len(chars)):
                        if arguments['user'] in chars[x]:
                            chars.pop(x)
                            f = 1
                            break
    
                monstersOK.remove(arguments['user'])
                charsOK.remove(arguments['user'])
                yourMonsters.clear()
                yourChars.clear() 
                #print(monsters)
                #print(chars)                         
                
            else:
                send_message("El número de monstruos y/o aventureros que has introducido no es válido", arguments['chat']) 
        else:
            send_message("Número de datos incorrecto. La sintaxis es /calcular", arguments['chat'])


###########
# TORNEOS #
###########
def command_inscripcion_torneo(arguments):
    if arguments['chat'] in USERS:
        keyboard = build_keyboard([["Tiro🏹"], ["Fuerza🏋️‍♀️"], ["Obstáculos🚧🏃‍♂️"], ["Magia🔮"]])
        send_message("Selecciona el torneo al que deseas inscribirte.", arguments['chat'], keyboard)

        NextStep(arguments, turney_selection, False)

@checkinator(("turney", check_turney), contains_command=False)
def turney_selection(arguments):
    if arguments['chat'] in USERS:
        send_message("¿Qué aventurero deseas inscribir?", arguments['chat'])
        if arguments['turney'] == "Tiro":
            NextStep(arguments, adventurer_selection_tiro, False)

        else:
            NextStep(arguments, adventurer_selection, True)

@checkinator(("name", check_string), contains_command=False)
def adventurer_selection(arguments):
    print("1")
    if arguments['chat'] in USERS:
        inscripciones.add_enrollment(arguments['turney'], arguments['name'], "-")
        send_message("Aventurero inscrito con éxito.", arguments['chat'])
        send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

@checkinator(("name", check_string), contains_command=False)
def adventurer_selection_tiro(arguments):
    print("1")
    if arguments['chat'] in USERS:
        send_message("¿Con qué arma va a competir?", arguments['chat'])
        NextStep(arguments, weapon_selection, True)

@checkinator(("weapon", check_string), contains_command=False)
def weapon_selection(arguments):
    if arguments['chat'] in USERS:
        inscripciones.add_enrollment(arguments['turney'], arguments['name'], arguments['weapon'])
        send_message("Aventurero inscrito con éxito.", arguments['chat'])
        send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])


def inline_inscripciones(arguments):
    data = arguments['text'].split()
    if len(data) == 1:
        showInscriptions(inscripciones, arguments['chat'])
    elif len(data) == 2:
        showTournament(inscripciones, data[1], arguments['chat'])
    else:
        send_message("Número de datos incorrecto. La sintaxis es /inscripciones [nombreDelTorneo]", arguments['chat'])

###############
# MENÚ DE ROL #
###############

def command_rol(arguments):
	if arguments['chat'] in USERS:
		items = [["Registrar un nuevo aventurero 🧙‍♂️"], ["Ascender a un aventurero 🧝‍♀️⏏️"], ["Calcular experiencia 🧮"], ["Repartir experiencia extra 🆓"], ["Repartir recompensas 💰"], ["Cobrar a un aventurero 🏦"], ["Buscar aventureros 🗂"], ["Publicar una misión 📰"], ["Registrar un informe de misión 📝"], ["Buscar misiones 📖"], ["Inscribirse en un torneo 🏆"], ["Ver torneos 📜"], ["Aposteitor 💸"]]
		keyboard = build_keyboard(items)
		send_message("Selecciona la opción que deseas realizar.", arguments['chat'], keyboard)
	send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

def command_nuevo_aventurero(arguments):
	if arguments['chat'] in USERS:
		send_message("Para añadir un nuevo aventurero, utiliza el comando /nuevo_aventurero seguido de su nombre, su nivel, su rango, sus puntos de experiencia y su dinero. Ejemplo: /nuevo_aventurero Jon Snow 5 Novato 16300 20.3. \nTen en cuenta que el aventurero se asignará a tu perfil, no registres aventureros de otros.", arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

def command_ascender(arguments):
	if arguments['chat'] in USERS:
		send_message("Para ascender a un aventurero, utiliza el comando /ascender seguido del nombre del aventurero y su nuevo rango. Ejemplo: /ascender Jon Snow Veterano", arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

def command_buscar_aventureros(arguments):
	if arguments['chat'] in USERS:
		send_message("Utiliza los comandos /personajes seguido del nombre de un jugador o /rango seguido de un rango para ver la lista de personajes con esas características. Ejemplos: /personajes Luis o /rango Novato", arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])


def command_calcular_experiencia(arguments):
	if arguments['chat'] in USERS:
		send_message("Para calcular la experiencia por combate, introduce los monstruos derrotados usando el comando /monstruo seguido de la cantidad de monstruos de ese tipo y de su Valor de Desafío (un comando por cada tipo de criatura). Ejemplo: /monstruo 2 8 añadiría dos monstruos de VD 8. \n A continuación añade los aventureros participantes usando el comando /aventurero seguido de su nombre (deben estar registrado en la base de datos). Ejemplo: /aventurero Jon Snow. \n Por último, utiliza el comando /calcular para indicar que has acabado de introducir los datos y recibirás la experiencia a repartir.", arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

def command_repartir_experiencia(arguments):
	if arguments['chat'] in USERS:
		send_message("Para repartir experiencia extra por una partida, usa el comando /repartir_exp seguido del nombre del personaje y la cantidad de experiencia que quieres darle. Ejemplo: /repartir_exp Jon Snow 350.", arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

def command_repartir_recompensas(arguments):
	if arguments['chat'] in USERS:
		send_message("Para repartir el dinero de una misión a un personaje, utiliza el comando /repartir_recompensa seguido del nombre del personaje y la cantidad que le corresponda. Ejemplo: /repartir_recompensa Jon Snow 10", arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

def command_cobrar(arguments):
	if arguments['chat'] in USERS:
		send_message("Para cobrar dinero a un aventurero, utiliza el comando /cobrar seguido del nombre del personaje y la cantidad a retirar. Ejemplo: /cobrar Jon Snow 100", arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

def command_publicar_mision(arguments):
	if arguments['chat'] in USERS:
		send_message("Para publicar una misión, envíame el texto comenzando con #nombreDeLaMision y a continuación el mensaje de la misión. Ejemplo: #orcosSexysEnTuZona blablabla. Si lo envías al grupo, anclaré el mensaje, si no, simplemente lo reenviaré.", arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

def command_registrar_mision(arguments):
	if arguments['chat'] in USERS:
		send_message("Para registrar una misión, envíame el informe con el siguiente formato:\n /nueva_mision \n #nombreDeLaMision \n díaDeLaSemana dd/mm/aaa \n Lista de personajes que asistieron \n Pequeño resumen de la misión.", arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

def command_buscar_mision(arguments):
	if arguments['chat'] in USERS:
		send_message("Para ver la lista de las últimas misiones, usa el comando /ultimas_misiones. Para buscar una misión concreta, utiliza el comando /mostrar_mision seguido del identificador. Por ejemplo: /mostrar_mision #ElVigiaSiniestro", arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])


def command_ver_torneos(arguments):
    if arguments['chat'] in USERS:
        t = TOURNAMENTS[0]
        for x in range(1,len(TOURNAMENTS)):
            t = t + ", " + TOURNAMENTS[x]
        send_message("Para ver las inscripciones a los torneos utiliza el comando /inscripciones. Si quieres consultar las inscripciones de un torneo concreto, añade el nombre del torneo después del comando. Los torneos disponibles son: {}".format(t), arguments['chat'])
        send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])


def command_aposteitor(arguments):
	if arguments['chat'] in USERS:
		send_message("Para iniciar una ronda de apuestas, utiliza el comando /nueva_ronda indicando el nombre de los competidores. Ejemplo: /nueva_ronda Gandalf Saruman  \nUna vez hayas especificado los contendientes, se podrán realizar apuestas usando el comando /apostar seguido del nombre del personaje que apuesta y la cantidad apostada, se te pedirá a continuación que elijas por quién quieres apostar. Ejemplo: /apostar Frodo 100 \nCuando se haya determinado el ganador del combate, utiliza el comando /ganador para resolver las ganancias y pérdidas de cada uno de los apostantes. Ejemplo: /ganador Gandalf\n\n El módulo de apuestas funciona usando el framework «Aposteitor» de @Seind", arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])


#########################
# MENÚ DE LA ASOCIACIÓN #
#########################

def command_finanzas(arguments):
	print("1")
	if arguments['chat'] in USERS:
		print("2")
		items = [["Registrar un ingreso 📥"], ["Registrar un pago 📤"], ["Consultar saldo 📊"], ["Consultar transacciones de un miembro 🧾👩‍💼"], ["Consultar últimas transacciones 🧾👨‍👩‍👦‍👦"]]
		keyboard = build_keyboard(items)
		send_message("Selecciona la opción que deseas realizar.", arguments['chat'], keyboard)
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])  
  
def command_ingreso(arguments):
	if arguments['chat'] in USERS:
		send_message("Para realizar un ingreso, utiliza el comando /ingreso seguido del nombre de la persona que lo hizo, la fecha en formato dd/mm/aa y la cantidad aportada. Ejemplo: /ingreso Juan 12/03/19 5", arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

def command_pago(arguments):
	if arguments['chat'] in USERS:
		send_message("Para realizar un pago, utiliza el comando /pago seguido del nombre de la persona a la que se pagó, la fecha en formato dd/mm/aa y la cantidad pagada. Ejemplo: /pago Juan 12/03/19 5", arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

def command_saldo(arguments):
	if arguments['chat'] in USERS:
		total(db, arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

def command_transacciones(arguments):
	if arguments['chat'] in USERS:
		send_message("Para consultar las transacciones de un miembro, utiliza el comando /miembro seguido del nombre de la persona. Ejemplo; /miembro Juan", arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

def command_ultimas_transacciones(arguments):
	if arguments['chat'] in USERS:
		last(db, arguments['chat'])
		send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

def command_eliminar_transaccion(arguments):
	if arguments['chat'] in ADMIN:
		db.del_last()
		send_message("Transacción eliminada con éxito", arguments['chat'])


# Command dictionaries
commands_with_backslash = {
    '/ping'                 : prueba.command_ping,
    '/echo'                 : command_echo,
    '/roll'                 : command_roll,
    '/sum'                  : command_sum,
    '/new_betting_round'    : aposteitor.command_new_betting_round,
    '/nueva_ronda'          : aposteitor.command_new_betting_round,
    '/bet'                  : aposteitor.command_bet,
    '/apostar'              : aposteitor.command_bet,
    '/winner'               : aposteitor.command_winner,
    '/ganador'              : aposteitor.command_winner,
	'/start'                : command_start,
	'/menu'                 : command_menu,
	'/help'                 : command_help,
	#'/add_user'             : command_add_user,
	'/set_trigger'          : command_set_trigger,
	'/mostrar_triggers'     : command_mostrar_triggers,
	'/ingreso'              : inline_ingreso,
	'/pago'                 : inline_pago,
	'/miembro'              : inline_miembro,
	'/nuevo_aventurero'     : inline_nuevo_aventurero,
	'/ascender'             : inline_ascender,
	'/repartir_exp'         : inline_repartir_exp,
	'/repartir_recompensa'  : inline_repartir_recompensa,
	'/cobrar'               : inline_cobrar,
	'/personajes'           : inline_personajes,
	'/rango'                : inline_rango,
	'/ultimas_misiones'     : inline_ultimas_misiones,
	'/mostrar_mision'       : inline_mostrar_mision,
	'/nueva_mision'         : inline_nueva_mision,
	'/monstruo'             : inline_monstruo,
	'/aventurero'           : inline_aventurero,
	'/calcular'             : inline_calcular,
	'/inscripciones'        : inline_inscripciones
    
    
}

commands_without_backslash = {
    'ping'                                          : prueba.command_ping,
	'💶️ Finanzas 💶️'                                : command_finanzas,
	'Registrar un ingreso 📥'                       : command_ingreso,
	'Registrar un pago 📤'                          : command_pago,
	'Consultar saldo 📊'                            : command_saldo,
	'Consultar transacciones de un miembro 🧾👩‍💼'    : command_transacciones,
	'Consultar últimas transacciones 🧾👨‍👩‍👦‍👦'          : command_ultimas_transacciones,
	'Eliminar la última transacción'                : command_eliminar_transaccion,
	'⚔️ Rol ⚔️'                                     : command_rol,
	'Registrar un nuevo aventurero 🧙‍♂️'              : command_nuevo_aventurero,
	'Ascender a un aventurero 🧝‍♀️⏏️'                 : command_ascender,
	'Buscar aventureros 🗂'                         : command_buscar_aventureros,
	'Calcular experiencia 🧮'                       : command_calcular_experiencia,
	'Repartir experiencia extra 🆓'                 : command_repartir_experiencia,
	'Repartir recompensas 💰'                       : command_repartir_recompensas,
	'Cobrar a un aventurero 🏦'                     : command_cobrar,
	'Publicar una misión 📰'                        : command_publicar_mision,
	'Registrar un informe de misión 📝'             : command_registrar_mision,
	'Buscar misiones 📖'                            : command_buscar_mision,
	'Inscribirse en un torneo 🏆'                   : command_inscripcion_torneo,
	'Ver torneos 📜'                                : command_ver_torneos,
	'Aposteitor 💸'                                 : command_aposteitor
}

#TODO:  - Falta ponerlo a testar.
