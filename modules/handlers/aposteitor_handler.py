
################
## APOSTEITOR ##
################

from ..aposteitor import aposteitor
from ..util.telegram_methods import *
from ..util.methods import *
from ..util.checkinator import *
from ..util.states_handler import *


class AposteitorHandler(object):
    """docstring for AposteitorHandler"""
    def __init__(self, db_adventures):
        self.db_adventures = db_adventures
        self.aposteitor_rounds = {} # Dictionary of Aposteitor.Round objects (chat : Aposteitor.Round instance)
        self.bettors = {}           # Dictionary of Aposteitor.Player objects (chat : Aposteitor.Player instance)
            

    def command_new_betting_round(self, arguments):
        """
        Initializes a betting round with a group of competitors.
        With the command, the user must provide the name of the competitors separated by spaces.
        
        :param      arguments:  The arguments
        :type       arguments:  Dictionary
        """
        competitors_names = arguments['text'].split()[1:]
        if len(competitors_names) <= 1:
            raise ValueError("Número de datos incorrecto. La sintaxis es /nueva_ronda [contendiente1] [contendiente2]. Por ejemplo: /nueva_ronda Saruman Gandalf")
        if arguments['chat'] in self.aposteitor_rounds:
            raise EnvironmentError("Ya existe una ronda de apuestas activa en estos momentos. Espera a que termine o finalizala manualmente para crear una nueva.")
        competitors_objects = []
        for name in competitors_names:
            # Código para recuperar de la base de datos
            competitors_objects.append(aposteitor.Competitor(name))
        self.aposteitor_rounds[arguments['chat']] = aposteitor.Round(competitors_objects)
        send_message("Ronda de apuestas creada con éxito.", arguments['chat'])
        send_message("¿Cuántas apuestas de personajes no jugadores van a ser realizadas?", arguments['chat'])
        NextStep(arguments, self.generate_padding_bets)


    @checkinator(("amount_padding_bets", check_unsigned_int), contains_command=False)
    def generate_padding_bets(self, arguments):
        """
        Generates padding bets from pnjs for a bets rounds. The list of pnjs and their bets range is in pnjs.txt file from aposteitor module.
        
        :param      arguments:  The arguments
        :type       arguments:  Dictionary
        """
        self.aposteitor_rounds[arguments['chat']].generate_padding_bets(arguments['amount_padding_bets'])
        send_message("Se han registrado {} apuestas realizadas por pnjs.".format(arguments['amount_padding_bets']), arguments['chat'])
        send_message("Ahora puedes realizar apuestas utilizando el comando /apostar o declarar a los ganadores con el comando /ganador seguido del nombre de los ganadores separados por espacios", arguments['chat'])



    def command_bet(self, arguments):
        """
        Starts a bet. Depending on the number of arguments, it will be a simple bet, composed or made in steps.
        
        :param      arguments:  The arguments
        :type       arguments:  Dictionary
        """
        if arguments['chat'] not in self.aposteitor_rounds:
            raise EnvironmentError("No existe ninguna ronda de apuestas en curso. Puedes crearla mediante el comando /nueva_ronda o /new_betting_round")
        arguments_amount = arguments['text'].count(" ")
        if arguments_amount == 0: # Step to step bet
            reply = "Vamos a iniciar una apuesta guiada. \n\n¿Quién va a realizar la apuesta"
            NextStep(arguments, self.guided_bet_set_bettor, last_step = False)
        elif arguments_amount == 4: # Inline simple bet
            reply = self.inline_simple_bet(arguments)
        elif arguments_amount == 5: # Inline composite bet
            reply = self.inline_composite_bet(arguments)
        else:
            reply = "Número de datos incorrecto. La sintaxis es /apostar [nombre de tu personaje] [cantidad]"
        send_message(reply, arguments['chat'])


    @checkinator(("bettor_name", check_string), contains_command=False)
    def guided_bet_set_bettor(self, arguments):
        """
        Includes bettor object in arguments and makes a request for amount in a step to step bet.
        
        :param      arguments:  The arguments
        :type       arguments:  Dictionary
        """
        if not (arguments['bettor_name'] in self.bettors.keys()):
            adv = self.db_adventures.get_pj(arguments['bettor_name'])
            if adv: # Registered Adventurer
                self.bettors[arguments['bettor_name']] = aposteitor.Player(arguments['bettor_name'], int(adv[0][5]))
            else:
                self.bettors[arguments['bettor_name']] = aposteitor.Player(arguments['bettor_name'], 335000) # Exporadical bettor
        arguments['bettor'] = self.bettors[arguments['bettor_name']]
        send_message("Perfecto. ¿Cuántas monedas de oro va a apostar?", arguments['chat'])
        NextStep(arguments, self.guided_bet_set_amount, last_step = False)


    @checkinator(("amount", check_positive_int), contains_command=False)
    def guided_bet_set_amount(self, arguments):
        """
        Includes amount in arguments and makes a request for bet type in a step to step bet.
        
        :param      arguments:  The arguments
        :type       arguments:  Dictionary
        """
        # Revisar AQUÍ que tiene dinero cuando esté integrado con la base de datos
        adv = self.db_adventures.get_pj(arguments['bettor_name'])
        if adv: # Registered Adventurer
            if (adv[0][5]) >= arguments['amount']:
                takeMoney(self.db_adventures, arguments['bettor_name'], arguments['amount']) #Sustract money from character's account

                reply = """Recibido. ¿Qué tipo de apuesta va a realizar? (indica el número del 1 al 4)
                1 - Ganador. Si por quién apostaste queda primero, participas en el premio con el 100% de tu apuesta.
                2 - Colocado. Si por quién apostaste queda primero o segundo, participas en el premio con el 70% de tu apuesta.
                3 - Tercero. Si por quién apostaste queda primero, segundo o tercero participas en el premio con el 40% de tu apuesta.
                4 - Tripleta. Si aciertas los tres finalistas en orden participas en un bote especial con el 100% de tu apuesta."""
                send_message(reply, arguments['chat'], build_keyboard([["1"], ["2"], ["3"], ["4"]]))
                NextStep(arguments, self.guided_bet_set_bet_type, last_step = False)

            else:
                send_message("A mí no me engañas, {} no tiene tanto dinero. ¿Cuánto quieres apostar?".format(arguments['bettor_name']), arguments['chat'])
                NextStep(arguments, self.guided_bet_set_amount, last_step = False)

        else: 
            reply = """Recibido. ¿Qué tipo de apuesta va a realizar? (indica el número del 1 al 4)
                1 - Ganador. Si por quién apostaste queda primero, participas en el premio con el 100% de tu apuesta.
                2 - Colocado. Si por quién apostaste queda primero o segundo, participas en el premio con el 70% de tu apuesta.
                3 - Tercero. Si por quién apostaste queda primero, segundo o tercero participas en el premio con el 40% de tu apuesta.
                4 - Tripleta. Si aciertas los tres finalistas en orden participas en un bote especial con el 100% de tu apuesta."""
            send_message(reply, arguments['chat'], build_keyboard([["1"], ["2"], ["3"], ["4"]]))
            NextStep(arguments, self.guided_bet_set_bet_type, last_step = False)


    @checkinator(("bet_type", check_int_range, (1,4)), contains_command=False)
    def guided_bet_set_bet_type(self, arguments):
        """
        Includes bet type in arguments and makes a request for a competitor depending on the bet type in a step to step bet.
        
        :param      arguments:  The arguments
        :type       arguments:  Dictionary
        """
        keyboard = build_keyboard([[competitor] for competitor in self.aposteitor_rounds[arguments['chat']].competitors.keys()])
        if arguments["bet_type"] == 4: # Composite bet
            send_message("¿Quién apuestas que quedará primero?", arguments['chat'], keyboard)
            NextStep(arguments, self.guided_bet_set_first_competitor, last_step = False)
        else:
            send_message("¿Por quién va a realizar la apuesta?", arguments['chat'], keyboard)
            NextStep(arguments, self.guided_bet_set_competitor, last_step = True)


    @checkinator(("name_competitor", check_string), contains_command=False)
    def guided_bet_set_competitor(self, arguments):
        """
        Includes competitor in arguments and registers bet in a step to step bet when is a simple bet.
        
        :param      arguments:  The arguments
        :type       arguments:  Dictionary
        """
        reply = self.aposteitor_rounds[arguments['chat']].register_simple_bet(
            arguments['bettor'],
            arguments['amount'],
            self.aposteitor_rounds[arguments['chat']].get_competitor_by_name(arguments['name_competitor']),
            arguments['bet_type']
            )
        send_message(reply, arguments['chat'])
        send_message("Si quieres seguir apostando usa el comando /apostar y si quieres declarar los ganadores usa el comando /ganador seguido del nombre de o de los ganadores separados por espacios", arguments['chat'])


    @checkinator(("name_competitor_in_first_position", check_string), contains_command=False)
    def guided_bet_set_first_competitor(self, arguments):
        """
        Includes competitor in first postion in arguments and makes a request for a competitor in second postion in a step to step bet when is a composite bet.
        
        :param      arguments:  The arguments
        :type       arguments:  Dictionary
        """
        arguments['competitor_in_first_position'] = self.aposteitor_rounds[arguments['chat']].get_competitor_by_name(arguments['name_competitor_in_first_position'])
        competitors = list(self.aposteitor_rounds[arguments['chat']].competitors.keys())
        competitors.remove(arguments['name_competitor_in_first_position']) # Because this competitor has been beted already
        keyboard = build_keyboard([[competitor] for competitor in competitors])
        send_message("¿Quién apuestas que quedará segundo?", arguments['chat'], keyboard)
        NextStep(arguments, self.guided_bet_set_second_competitor, last_step = False)


    @checkinator(("name_competitor_in_second_position", check_string), contains_command=False)
    def guided_bet_set_second_competitor(self, arguments):
        """
        Includes competitor in second postion in arguments and makes a request for a competitor in third postion in a step to step bet when is a composite bet.
        
        :param      arguments:  The arguments
        :type       arguments:  Dictionary
        """
        arguments['competitor_in_second_position'] = self.aposteitor_rounds[arguments['chat']].get_competitor_by_name(arguments['name_competitor_in_second_position'])
        competitors = list(self.aposteitor_rounds[arguments['chat']].competitors.keys())
        competitors.remove(arguments['name_competitor_in_first_position']) # Because this competitor has been beted already
        competitors.remove(arguments['name_competitor_in_second_position']) # Because this competitor has been beted already
        keyboard = build_keyboard([[competitor] for competitor in competitors])
        send_message("¿Quién apuestas que quedará tercero?", arguments['chat'], keyboard)
        NextStep(arguments, self.guided_bet_set_third_competitor, last_step = True)


    @checkinator(("name_competitor_in_third_position", check_string), contains_command=False)
    def guided_bet_set_third_competitor(self, arguments):
        """
        Includes competitor in third postion in arguments and registes bet in a step to step bet when is a composite bet.
        
        :param      arguments:  The arguments
        :type       arguments:  Dictionary
        """
        arguments['competitor_in_third_position'] = self.aposteitor_rounds[arguments['chat']].get_competitor_by_name(arguments['name_competitor_in_third_position'])
        reply = self.aposteitor_rounds[arguments['chat']].register_composite_bet(
            arguments['bettor'],
            arguments['amount'], [
            arguments['competitor_in_first_position'],
            arguments['competitor_in_second_position'],
            arguments['competitor_in_third_position']
            ])
        send_message(reply, arguments['chat'])
        send_message("Si quieres seguir apostando usa el comando /apostar y si quieres declarar los ganadores usa el comando /ganador seguido del nombre de o de los ganadores separados por espacios", arguments['chat'])



    @checkinator(("bettor_name", check_string), ("amount", check_positive_int), ("competitor_name", check_string), ("bet_type", check_positive_int), contains_command=True)
    def inline_simple_bet(self, arguments):
        """
        Registes a simple bet make inline.
        
        :param      arguments:  The arguments
        :type       arguments:  Dictionary

        :returns:   The text of susccessful
        :rtype:     String
        """
        if not (arguments['bettor_name'] in self.bettors.keys()):
            adv = self.db_adventures.get_pj(arguments['bettor_name'])
            if adv: # Registered Adventurer
                self.bettors[arguments['bettor_name']] = aposteitor.Player(arguments['bettor_name'], adv[0][5])
            else:
                self.bettors[arguments['bettor_name']] = aposteitor.Player(arguments['bettor_name'], 335000) # Exporadical bettor
        bettor = self.bettors[arguments['bettor_name']]
        competitor = self.aposteitor_rounds[arguments['chat']].get_competitor_by_name(arguments['competitor_name'])
        if bettor.money >= arguments['amount']:
            takeMoney(self.db_adventures, arguments['bettor_name'], arguments['amount']) #Sustract money from character's account
            return self.aposteitor_rounds[arguments['chat']].register_simple_bet(bettor, arguments['amount'], competitor, arguments['bet_type'])
        else:
            send_message("A mí no me engañas, {} no tiene tanto dinero. ¿Cuánto quieres apostar?".format(arguments['bettor_name']), arguments['chat'])

    @checkinator(("bettor_name", check_string), ("amount", check_positive_int), ("name_competitor_in_first_position", check_string), ("name_competitor_in_second_position", check_string), ("name_competitor_in_third_position", check_string), contains_command=True)
    def inline_composite_bet(self, arguments):
        """
        Registes a composite bet make inline.
        
        :param      arguments:  The arguments
        :type       arguments:  Dictionary

        :returns:   The text of susccessful
        :rtype:     String
        """
        if not (arguments['bettor_name'] in self.bettors.keys()):
            adv = self.db_adventures.get_pj(arguments['bettor_name'])
            if adv: # Registered Adventurer
                self.bettors[arguments['bettor_name']] = aposteitor.Player(arguments['bettor_name'], adv[0][5])
            else:
                self.bettors[arguments['bettor_name']] = aposteitor.Player(arguments['bettor_name'], 335000) # Exporadical bettor
        bettor            = self.bettors[arguments['bettor_name']]
        first_competitor  = self.aposteitor_rounds[arguments['chat']].get_competitor_by_name(arguments['name_competitor_in_first_position'])
        second_competitor = self.aposteitor_rounds[arguments['chat']].get_competitor_by_name(arguments['name_competitor_in_second_position'])
        third_competitor  = self.aposteitor_rounds[arguments['chat']].get_competitor_by_name(arguments['name_competitor_in_third_position'])
        if bettor.money >= arguments['amount']:
            takeMoney(self.db_adventures, arguments['bettor_name'], arguments['amount']) #Sustract money from character's account
            return self.aposteitor_rounds[arguments['chat']].register_composite_bet(bettor, arguments['amount'], [first_competitor, second_competitor, third_competitor])
        else:
            send_message("A mí no me engañas, {} no tiene tanto dinero. ¿Cuánto quieres apostar?".format(arguments['bettor_name']), arguments['chat'])

    def command_winner(self, arguments):
        """
        Set winner or winners of the current round and reports the prizes.
        
        :param      arguments:  The arguments
        :type       arguments:  Dictionary
        """
        winners_names = arguments['text'].split()[1:]
        if not (
                (len(self.aposteitor_rounds[arguments['chat']].competitors.items()) > 2 and len(winners_names) == 3) or
                (len(self.aposteitor_rounds[arguments['chat']].competitors.items()) == 2 and len(winners_names) == 1)):
            raise EnvironmentError("El número de ganadores no es consistente con el número de participantes")
        winners = []
        for winner_name in winners_names:
            winners.append(self.aposteitor_rounds[arguments['chat']].get_competitor_by_name(winner_name))
        self.aposteitor_rounds[arguments['chat']].proclaim_winner(winners)
        reply = self.aposteitor_rounds[arguments['chat']].distribute_prize(winners)

        ### SIN IMPLEMENTAR!!!!! ###
        # Aquí se reparten los dineros a los juegadores
        earnings = []

        for x in earnings: # Add money to the winning characters' accounts
            adv = self.db_adventures.get_pj(x[0])
            if adv:
                giveMoney(self.db_adventures, x[0], x[1])


        send_message(reply, arguments['chat'])
        del self.aposteitor_rounds[arguments['chat']]