# coding=utf-8
def checkinator(*templates, contains_command):
    def checkinator_decorator(function):
        def checked_function(arguments):
            """
            Evaluates each of the parameters given with the expected quantity and the required evaluation functions.
            
            :param      arguments:         The arguments
            :type       arguments:         Dictionary
            :param      templates:         Tuples with peers (name, evaluater_function) or triplets (name, evaluater_function, parameters)
            :type       templates:         List of Tuples
            :param      contains_command:  Indicator of the presence of a command in the text
            :type       contains_command:  Boolean
            """
            elements = arguments['text'].split()[1:] if contains_command == True else arguments['text'].split() 
            if len(elements) != len(templates):
                raise TypeError("El número de argumentos es incorrecto. La función utiliza {} y se han indicado {}".format(len(templates), len(elements)))
            for index in range(len(templates)):
                if len(templates[index]) == 2: # Without parameters
                    arguments[templates[index][0]] = templates[index][1](elements[index])
                else: # With parameters
                    arguments[templates[index][0]] = templates[index][1](elements[index], templates[index][2])
            return function(arguments)
        return checked_function
    return checkinator_decorator


def check_int(value):
    """
    Evaluates if the value can be converted to an integer and return it.
    
    :param      value:  The value
    :type       value:  String
    
    :returns:   The value
    :rtype:     Integer
    """
    try:
        return int(value)
    except ValueError:
        raise ValueError("El valor indicado debe ser un número")

def check_positive_int(value):
    """
    Evaluates if the value is a positive number (>0) and return it.
    
    :param      value:  The value
    :type       value:  String

    :returns:   The value
    :rtype:     Integer
    """
    value = check_int(value)
    if value > 0:
        return value
    else:
        raise ValueError("El número indicado debe ser mayor que 0. Ceporro")

def check_int_range(value, interval):
    """
    Evaluates if the value is between a interval and return it.
    
    :param      value:     The value
    :type       value:     String
    :param      interval:  The interval
    :type       interval:  Tuple with [min, max]
    
    :returns:   Value within the interval
    :rtype:     Integer
    """
    value = check_int(value)
    if interval[0] <= value and value <= interval[1]:
        return value
    else:
        raise ValueError("El número indicado debe tener un valor perteneciente al rango [{}-{}]".format(interval[0], interval[1]))

def check_unsigned_int(value):
    """
    Evaluates if the value is a unsigned number (>=0) and return it.
    
    :param      value:  The value
    :type       value:  String
    
    :returns:   The value
    :rtype:     Integer
    """
    value = check_int(value)
    if value >= 0:
        return value
    else:
        raise ValueError("El número indicado debe ser mayor o igual que 0. Ceporro")

def check_string(value): # Comprobación irrelevante
    if type(value) is str:
        return value
    return ValueError("El nombre no es una cadena")

def check_dices(value):
    """
    Builds and return the tuple for a dice roll and evaluates if all values are corrects.
    
    :param      value:  The value
    :type       value:  String

    :returns:   The group of values
    :rtype:     Tuple (Integer, Integer, Integer)
    """
    value += "+0"
    roll = value.split("+") # [0] = roll, [1] = bonus or bonus padding, [2] = bonus padding
    dices = roll[0].split("-")
    if len(dices) == 1:
        return (check_positive_int(dices[0]), 1, check_unsigned_int(roll[1]))
    elif len(dices) == 2:
        return (check_positive_int(dices[0]), check_positive_int(dices[1]), check_unsigned_int(roll[1]))
    else:
        raise TypeError("El formato de la tirada es incorrecto. Debe ser dado-cantidad+bonus, donde -cantidad y +bonus son opcionales")

def check_rank(value):
    RANGOS = ["Novato","Novata","Veterano","Veterana","Élite","Comandante"]
    if value in RANGOS:
        return value
    return ValueError("El rango introducido no es correcto. Debe ser uno de los siguientes {}".format(RANGOS))

def check_date(date):
    d = date.split("/")
    if len(d) == 3:
        day = d[0]
        month = d[1]
        year = d[2]
        return (check_int_range(day, (1,31)), check_int_range(month, (1,12)), check_positive_int(year))
    return ValueError("La fecha introducida no tiene el formato correcto.")

def check_turney(turney):
    TOURNAMENTS = [str("Tiro🏹"), str("Fuerza🏋️‍♀️"), str("Obstáculos🚧🏃‍♂️"), str("Magia🔮")]

    if turney == TOURNAMENTS[0]:       
        return("Tiro")

    elif turney == TOURNAMENTS[1]:
        return("Fuerza")

    elif turney == TOURNAMENTS[2]:        
        return("Obstáculos")

    elif turney == TOURNAMENTS[3]:    
        return("Magia")

    else:
        ValueError("El torneo seleccionado no es válido.")




