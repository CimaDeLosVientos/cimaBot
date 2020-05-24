from ..util.telegram_methods import *
from ..util.db_helper_guild import *


registration_map_key = [
    "name",
    "complete_name",
    "birth_date_day",
    "birth_date_month",
    "birth_date_year",
    "registrer_date_day",
    "registrer_date_month",
    "registrer_date_year",
    "sex",
    "from",
    "formation",
    "especialiation",
    "work_experience",
    "testament",
#    "room",
#    "rank",
#    "on_service",
    "tags",
    "player",
    "experience_points",
    "money"
]

def command_ping(arguments):
    """
    Classic ping. Checks bot's state.
    
    :param      arguments:  The arguments
    :type       arguments:  Dictionary
    """
    send_message("Estoy vivo", arguments['chat'])

class Tested(object):
    """docstring for AposteitorHandler"""
    def __init__(self, database):
        self.database = database


    def command_registration(self, arguments):
        reply = arguments['reply_to_message']['text'].split(" || ")
        arguments_unformating = {}
        for argument in reply:
            key, value = argument.split(": ")
            arguments_unformating[key] = value

        db_arguments = {}
        db_arguments["name"] = arguments_unformating["name"].title()
        db_arguments["complete_name"] = arguments_unformating["complete_name"].title()

        birth_date_day = arguments_unformating["birth_date"].split("/")
        db_arguments["birth_date_day"] = int(birth_date_day[0])
        db_arguments["birth_date_month"] = int(birth_date_day[1])
        db_arguments["birth_date_year"] = int(birth_date_day[2])

        registrer_date_day = arguments_unformating["registrer_date"].split("/")
        db_arguments["registrer_date_day"] = int(registrer_date_day[0])
        db_arguments["registrer_date_month"] = int(registrer_date_day[1])
        db_arguments["registrer_date_year"] = int(registrer_date_day[2])

        db_arguments["sex"] = int(arguments_unformating["sex"])
        db_arguments["race"] = arguments_unformating["race"].title()
        db_arguments["from"] = arguments_unformating["from"].title()
        db_arguments["formation"] = arguments_unformating["formation"]
        db_arguments["especialiation"] = arguments_unformating["especialiation"]
        db_arguments["work_experience"] = arguments_unformating["work_experience"]
        db_arguments["testament"] = arguments_unformating["testament"]
        #db_arguments["room"] = 
        #db_arguments["rank"] = 
        #db_arguments["on_service"] = 
        db_arguments["tags"] = [x.title() for x in arguments_unformating["tags"].split(",")]
        db_arguments["player"] = arguments_unformating["player"].title()
        db_arguments["experience_points"] = int(arguments_unformating["experience_points"])
        db_arguments["money"] = int(arguments_unformating["money"])
        
        # Llamar al método de base de datos
        self.database.add_adventurer(db_arguments)

        message = "Se ha registrado un personaje con los siguientes datos:\n\n"
        for key, value in db_arguments.items():
            message += "{}: {}\n".format(key.title(), value)
        send_message(message, arguments['chat'])