from ..util.telegram_methods import *

def command_ping(arguments):
    """
    Classic ping. Checks bot's state.
    
    :param      arguments:  The arguments
    :type       arguments:  Dictionary
    """
    send_message("Estoy vivo", arguments['chat'])