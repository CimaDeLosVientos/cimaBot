# coding=utf-8
import json
import requests
import time
import urllib
import sys
import math
import random

from .config import *

from .util.methods import * #income, payment, total, member, last, characters, ranks, mergeMonsters, giveExp, giveMoney, takeMoney, showQuests, findQuest, showTriggers, showTournament, showInscriptions
from .util.telegram_methods import *
from .util.db_helper import DBHelper
from .util.db_helper_guild import DBHelperGuild
from .util.checkinator import *
from .util.states_handler import *

from .handlers import prueba
from .handlers.aposteitor_handler import AposteitorHandler
from .handlers.guild_handler import GuildHandler
from .handlers.rol_help_menus_handler import RolHelpMenusHandler
from .handlers.asoc_help_menus_handler import AsocHelpMenusHandler


db = DBHelper(
    finances      = "./data_base_files/finances.sqlite",                                                                                                                                   
    adventurers   = "./data_base_files/adventurers.sqlite",                                                     
    quests        = "./data_base_files/quests.sqlite",                                                                                                                                                                                       
    triggers      = "./data_base_files/triggers.sqlite",                                                                                                                                   
    log           = "./data_base_files/log.sqlite",                                                                                                                                                                                                                                                                     
    registrations = "./data_base_files/registrations.sqlite")

db.setup()
aposteitor = AposteitorHandler(db)
helen = GuildHandler(db)
rol = RolHelpMenusHandler(db)
asoc = AsocHelpMenusHandler(db)
tested = prueba.Tested(DBHelperGuild("./data_base_files/testing.sqlite"))

######################################################################
#################### PARÁMETROS MODIFICABLES #########################
######################################################################


RANGOS = ["Novato","Novata","Veterano","Veterana","Élite","Comandante"]

TOURNAMENTS = [str("Tiro 🏹"), str("Fuerza 🏋️‍♀️"), str("Obstáculos 🚧🏃‍♂️"), str("Magia 🔮")]

######################################################################

URL = "https://api.telegram.org/bot{}/".format(TOKEN)




betState = 0

# ronda = app.Ronda()
# ronda.loadPNJs()
MAXBETS = 20


### Añadidas por Adri

###






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


    if 'message' in update and 'text' in update["message"]:
            arguments = {
                'text' : update["message"]["text"],
                'chat' : update["message"]["chat"]["id"],
                'user' : update["message"]["from"]["id"],
                'message' : update["message"]["message_id"],
                'reply_to_message' : None
            }
            if 'reply_to_message' in update["message"].keys(): # Only replies have this field
                arguments['reply_to_message'] = update["message"]["reply_to_message"]
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
            answer = db.get_trigger(arguments['text'])
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


## AQUÍ ESTABA AVENTUREROS


## AQUÍ ESTABA LA CAJA DE LA ASOCIACIÓN


## AQUÍ ESTABAN MISIONES, TORNEOS Y LA CALCULADORA DE EXP

############
# TRIGGERS #
############
def command_set_trigger(update):
    data = update["message"]["text"].split(' ', 1)[1]
    #print(len(data))
    if len(data) > 0:
        if 'reply_to_message' in update["message"]:
            if 'text' in update["message"]["reply_to_message"]:                               
                db.add_trigger(data, "texto", update["message"]["reply_to_message"]["text"])
                send_message("Trigger añadido correctamente.", update["message"]["chat"]["id"])
            if 'photo' in update["message"]["reply_to_message"]:
                fileID =  update["message"]["reply_to_message"]["photo"][-1]["file_id"]
                db.add_trigger(data, "foto", fileID)
                send_message("Trigger añadido correctamente.", update["message"]["chat"]["id"])
            if 'animation' in update["message"]["reply_to_message"]:
                fileID =  update["message"]["reply_to_message"]["animation"]["file_id"]
                db.add_trigger(data, "gif", fileID)
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



## AQUI ESTABA EL MENU DE ROL

## AQUI ESTABA EL MENU DE de la asociación



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
	'/ingreso'              : asoc.inline_ingreso,
	'/pago'                 : asoc.inline_pago,
	'/miembro'              : asoc.inline_miembro,
	'/nuevo_aventurero'     : helen.inline_nuevo_aventurero,
	'/ascender'             : helen.inline_ascender,
	'/repartir_exp'         : helen.inline_repartir_exp,
	'/repartir_recompensa'  : helen.inline_repartir_recompensa,
	'/cobrar'               : helen.inline_cobrar,
	'/personajes'           : helen.inline_personajes,
	'/rango'                : helen.inline_rango,
	'/ultimas_misiones'     : helen.inline_ultimas_misiones,
	'/mostrar_mision'       : helen.inline_mostrar_mision,
	'/nueva_mision'         : helen.inline_nueva_mision,
	'/monstruo'             : helen.inline_monstruo,
	'/aventurero'           : helen.inline_aventurero,
	'/calcular'             : helen.inline_calcular,
	'/inscripciones'        : helen.inline_inscripciones,
    '/login'                : tested.command_registration
    
    
}

commands_without_backslash = {
    'ping'                                          : prueba.command_ping,
	'💶️ Finanzas 💶️'                                : asoc.command_finanzas,
	'Registrar un ingreso 📥'                       : asoc.command_ingreso,
	'Registrar un pago 📤'                          : asoc.command_pago,
	'Consultar saldo 📊'                            : asoc.command_saldo,
	'Consultar transacciones de un miembro 🧾👩‍💼'    : asoc.command_transacciones,
	'Consultar últimas transacciones 🧾👨‍👩‍👦‍👦'          : asoc.command_ultimas_transacciones,
	'Eliminar la última transacción'                : asoc.command_eliminar_transaccion,
	'⚔️ Rol ⚔️'                                     : rol.command_rol,
	'Registrar un nuevo aventurero 🧙‍♂️'              : rol.command_nuevo_aventurero,
	'Ascender a un aventurero 🧝‍♀️⏏️'                 : rol.command_ascender,
	'Buscar aventureros 🗂'                         : rol.command_buscar_aventureros,
	'Calcular experiencia 🧮'                       : rol.command_calcular_experiencia,
	'Repartir experiencia extra 🆓'                 : rol.command_repartir_experiencia,
	'Repartir recompensas 💰'                       : rol.command_repartir_recompensas,
	'Cobrar a un aventurero 🏦'                     : rol.command_cobrar,
	'Publicar una misión 📰'                        : rol.command_publicar_mision,
	'Registrar un informe de misión 📝'             : rol.command_registrar_mision,
	'Buscar misiones 📖'                            : rol.command_buscar_mision,
	'Inscribirse en un torneo 🏆'                   : helen.command_inscripcion_torneo,
	'Ver torneos 📜'                                : rol.command_ver_torneos,
	'Aposteitor 💸'                                 : rol.command_aposteitor
}

#TODO:  - Falta ponerlo a testar.
