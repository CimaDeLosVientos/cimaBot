####################################
##############CIMABOT###############
###ASOCIACIÓN CIMA DE LOS VIENTOS###
# @Luis_gar # @Seind # @DarkSaytan #
####################################

import json
import requests
import time
import urllib

from dbhelper import DBHelper

######################################################################
#################### PARÁMETROS MODIFICABLES #########################
######################################################################

TOKEN = "XXXXXXXXXX:YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"

GROUPID = "-xxxxxxxxxx"

ADMIN = 0000000000

USERS = [000000000,00000000001]

USERNAMES = ["AAAAA","BBBBBB"]

USERSDICT = {00000000000:"AAAAA",00000000001:"BBBBBBB"}

RANGOS = ["Novato","Novata","Veterano","Veterana","Élite","Comandante"]

######################################################################

URL = "https://api.telegram.org/bot{}/".format(TOKEN)

db = DBHelper("cuentas.sqlite")
aventureros = DBHelper("aventureros.sqlite")

monsters = []
chars = []
monstersOK = []
charsOK = []

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

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=html".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def pin_message(chat_id, messageID, notif = False):
    url = URL + "pinChatMessage?chat_id={}&message_id={}".format(chat_id, messageID)
    if notif:
        url += "&disable_notification={}".format(notif)
    get_url(url)

def income(name, date, money, chat):
    dateInt = date.split("/")
    if name in USERNAMES:
        db.add_transaction("Ingreso", name, int(dateInt[0]), int(dateInt[1]), int(dateInt[2]), abs(float(money)))
        send_message("Ingreso realizado con éxito", chat)
    else:
        send_message("El nombre introducido no es un miembro válido", chat)

def payment(name, date, money, chat):
    dateInt = date.split("/")
    moneyFloat = float(money)
    if name in USERNAMES:
        db.add_transaction("Pago", name, int(dateInt[0]), int(dateInt[1]), int(dateInt[2]), -abs(moneyFloat))
        send_message("Pago realizado con éxito", chat)
    else:
        send_message("El nombre introducido no es un miembro válido", chat)

def total(chat):
    saldo = db.get_total()
    send_message("El saldo de la cuenta es {}€".format(saldo), chat)

def member(name, chat):
    string = ""
    t = db.get_transactions(name)
    for w in t:
        string = string + w[0] + " " + w[1] + " " + str(w[2]) + "/"+ str(w[3]) + "/"+ str(w[4]) + " " + str(w[5]) + "€" + "\n"
    send_message(string, chat)

def last(chat):
    string = ""
    t = db.get_last()
    for w in t:
        string = string + w[0] + " " + w[1] + " " + str(w[2]) + "/"+ str(w[3]) + "/"+ str(w[4]) + " " + str(w[5]) + "€" +"\n"
    send_message(string, chat)

def characters(player, chat):
    t = aventureros.get_characters(player)
    string = ""
    if not t:
        send_message("El jugador introducido no es correcto. Debe ser uno de los siguientes {}".format(USERNAMES), chat)
    else:
        for w in t:
            l = len(w)
            rank = w[l-1]
            lvl = int(w[l-2])
            name = w[1]
            if l-3 > 1:
                for x in range(2, l-2):
                    name = name + " " + w[x]
            string = string + "Jugador: " + w[0] + " PJ: " + name + " " + "Nivel: " + str(lvl) + " " + "Rango: " + rank +"\n"
        send_message(string, chat)

def ranks(rank, chat):
    t = aventureros.get_ranks(rank)
    string = ""
    if not t:
        send_message("El rango introducido no es correcto. Debe ser uno de los siguientes {}".format(RANGOS), chat)
    else:
        for w in t:
            l = len(w)
            rank = w[l-1]
            lvl = int(w[l-2])
            name = w[1]
            if l-3 > 1:
                for x in range(2, l-2):
                    name = name + " " + w[x]
            string = string + "Jugador: " + w[0] + " PJ: " + name + " "  + "Nivel: " + str(lvl) + " " + "Rango: " + rank +"\n"
        send_message(string, chat)

def mergeMonsters(monsters, chat): 
    vdVector = []
    for m in monsters:
        exponent = math.log(m[1],2) #Para monstruos iguales, se halla el bonus por cantidad mediante interpolación logarítmica
        if m[2] < 1:
            auxVD = (1 + 2*exponent)*m[2]
        else:
            auxVD = m[2] + 2*exponent
        if auxVD > 20:
            auxVD = 20
            send_message("El VD de uno de los encuentros introducidos supera VD20. Considera repartir experiencia adicional.", chat)
        vdVector.append(round(auxVD))
    print(vdVector)
    send_message("Se han reducido los monstruos de igual VD a monstruos únicos de VDs: {}".format(vdVector), chat)
    return vdVector

def menu(updates):
    for update in updates["result"]:
        if 'text' in update["message"]:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            user = update["message"]["from"]["id"]
            message = update["message"]["message_id"]
            if user in USERS:            
                if text == "/start" and chat in USERS:
                    send_message("Bienvenido al bot de ayuda de La Cima De Los Vientos. Para ver el Menú principal, usa el comando /menu", chat)

                elif text == "/menu" and chat in USERS:
                    items = ["💶️ Finanzas 💶️", "⚔️ Rol ⚔️"]
                    keyboard = build_keyboard(items)
                    send_message("Selecciona una función", chat, keyboard)

                elif text == "/help" and chat in USERS:
                    send_message("Emosido engañados", chat)

                elif text.startswith("/add_user") and user == ADMIN:
                    data = text.split()
                    if len(data) == 2:
                        USERS.append(data[1])
                    else:
                        send_message("Número de datos incorrecto", chat)

                elif text.startswith("/ingreso"):
                    data = text.split()
                    if len(data) == 4:
                        income(data[1], data[2], data[3], chat)
                    else:
                        send_message("Número de datos incorrecto. La sintaxis es /ingreso nombre dd/mm/aa dinero", chat)

                elif text.startswith("/pago"):
                    data = text.split()
                    if len(data) == 4:
                        payment(data[1], data[2], data[3], chat)
                    else:
                        send_message("Número de datos incorrecto. La sintaxis es /pago nombre dd/mm/aa dinero", chat)

                elif text.startswith("/miembro") and chat in USERS:
                    data = text.split()
                    if len(data) == 1:
                        member(data[1], chat)
                    else:
                        send_message("Número de datos incorrecto. La sintaxis es /miembro nombre", chat)

                elif text.startswith("#"):
                    if chat in USERS:
                        send_message(text,GROUPID)
                        pin_message(GROUPID,message, False)
                    else:
                        pin_message(GROUPID,message, False)

                elif text.startswith("/nuevo_aventurero") and chat in USERS:
                    data = text.split()
                    l = len(data)
                    if l > 3:
                        rank = data[l-1]
                        lvl = int(data[l-2])
                        if rank not in RANGOS:
                            send_message("El rango introducido no es correcto. Debe ser uno de los siguientes {}".format(RANGOS), chat)
                        elif lvl < 1 or lvl > 20:
                            send_message("El nivel debe estar comprendido entre 1 y 20.", chat)
                        else:
                            name = data[1]
                            if l-3 > 1:
                                for x in range(2, l-2):
                                    name = name + " " + data[x]
                            aventureros.add_adventurer(USERSDICT[user], name, lvl, rank)
                            send_message("Aventurero añadido con éxito", chat)
                    else:
                        send_message("Número de datos incorrecto. La sintaxis es /nuevo_aventurero Nombre Nivel Rango", chat)

                elif text.startswith("/ascender") and chat in USERS:
                    data = text.split()
                    l = len(data)
                    if l > 2:
                        rank = data[l-1]
                        name = data[1]
                        if l-2 > 1:
                            for x in range(2, l-1):
                                name = name + " " +data[x]
                        aventureros.rank_up(name, rank)
                        send_message("Ascenso realizado con éxito", chat)
                    else:
                        send_message("Número de datos incorrecto. La sintaxis es /ascender NombrePJ Rango", chat)

                elif text.startswith("/subir_nivel") and chat in USERS:
                    data = text.split()
                    l = len(data)
                    if l > 2:
                        level = int(data[l-1])
                        name = data[1]
                        if l-2 > 1:
                            for x in range(2, l-1):
                               name = name + " " +data[x]
                        aventureros.level_up(name, level)
                        send_message("Nivel modificado con éxito", chat)
                    else:
                        send_message("Número de datos incorrecto. La sintaxis es /subir_nivel NombrePJ Nivel", chat)

                elif text.startswith("/personajes"):
                    data = text.split()
                    if len(data) == 2:
                        characters(data[1], chat)
                    else:
                        send_message("Número de datos incorrecto. La sintaxis es /personajes NombreJugador", chat)

                elif text.startswith("/rango"):
                    data = text.split()
                    if len(data) == 2:
                        ranks(data[1], chat)
                    else:
                        send_message("Número de datos incorrecto. La sintaxis es /rango rangoABuscar", chat)

                elif text.startswith("/monstruo") and chat in USERS:
                    data = text.split()
                    if len(data) == 3:
                        d = float(data[2])
                        if float(d > 0 and d < 21):
                            if d >= 1:
                                d = int(data[2])
                            aux = [user,int(data[1]),d]
                            monsters.append(aux)
                            yourMonsters = ""
                            for x in monsters:
                               if x[0] == user:
                                    if user not in monstersOK:
                                        monstersOK.append(user)
                                    yourMonsters = yourMonsters + str(x[1]) + " monstruos de VD " + str(x[2]) + "\n"
                            send_message("Monstruos añadidos: \n {}".format(yourMonsters), chat);
                        else:
                            send_message("El VD del monstruo introducido no es válido. Debe estar comprendido entre 1 y 20.", chat)
                    else:
                        send_message("Número de datos incorrecto. La sintaxis es /monstruo Cantidad VD", chat)
                    yourMonsters = ""

                elif text.startswith("/aventurero") and chat in USERS:
                    data = text.split()
                    l = len(data)
                    if l > 1:
                        name = data[1]
                        if l > 2:
                            for x in range (2,l):
                                name = name + data[x]
                        auxChar = aventureros.get_pj(name)
                        if auxChar:
                            k = len(auxChar[0])
                            aux = [user, name, int(auxChar[0][k-2]), 0]
                            chars.append(aux)
                            yourChars = ""
                            for x in chars:
                                if x[0] == user:
                                    if user not in charsOK: 
                                        charsOK.append(user)
                                    yourChars = yourChars + x[1] + " de nivel " + str(x[2]) + "\n"
                            send_message("Aventureros añadidos: \n {}".format(yourChars), chat);
                        else:
                            send_message("El nombre que has introducido no corresponde a ningún aventurero existente", chat)
                    else:
                        send_message("Número de datos incorrecto. La sintaxis es /aventurero NombrePJ", chat)
                    yourChars = ""

                elif text.startswith("/calcular") and chat in USERS:
                    data = text.split()
                    if len(data) == 1:
                        if user in monstersOK and user in charsOK:
                            yourMonsters = []
                            for x in monsters:
                                if x[0] == user:
                                    yourMonsters.append(x)
                            yourChars = []
                            for x in chars:
                                if x[0] == user:
                                    yourChars.append(x)
                            VDs = mergeMonsters(yourMonsters, chat)
                            exp = 0
                            report = ""
                            l = len(yourChars)
                            for c in yourChars:
                                for monster in VDs:
                                    exp = exp + expTable[c[2]-1][monster-1]
                                c[3] = exp / l
                                exp = 0
                                report = report + c[1] + " recibe: " + str(round(c[3])) + " puntos de experiencia \n"
                            send_message(report, chat);
                            f = 1
                            while f == 1:
                                f = 0
                                for x in range (0,len(monsters)):
                                    if user in monsters[x]:
                                        monsters.pop(x)
                                        f = 1
                                        break
                                        
                            f = 1
                            while f == 1:
                                f = 0
                                for x in range (0, len(chars)):
                                    if user in chars[x]:
                                        chars.pop(x)
                                        f = 1
                                        break

                            monstersOK.remove(user)
                            charsOK.remove(user)
                            yourMonsters.clear()
                            yourChars.clear() 
                            print(monsters)
                            print(chars)                         
                            
                        else:
                            send_message("El número de monstruos y/o aventureros que has introducido no es válido", chat) 
                    else:
                        send_message("Número de datos incorrecto. La sintaxis es /calcular", chat)

                elif "Finanzas" in text and chat in USERS:
                    items = ["Registrar un ingreso", "Registrar un pago", "Consultar saldo", "Consultar transacciones de un miembro", "Consultar últimas transacciones"]
                    keyboard = build_keyboard(items)
                    send_message("Selecciona la opción que deseas realizar.", chat, keyboard)

                elif text == "Registrar un ingreso" and chat in USERS:
                    send_message("Para realizar un ingreso, utiliza el comando /ingreso seguido del nombre de la persona que lo hizo, la fecha en formato dd/mm/aa y la cantidad aportada. Ejemplo: /ingreso Juan 12/03/19 5", chat)

                elif text == "Registrar un pago" and chat in USERS:
                    send_message("Para realizar un pago, utiliza el comando /pago seguido del nombre de la persona a la que se pagó, la fecha en formato dd/mm/aa y la cantidad pagada. Ejemplo: /pago Juan 12/03/19 5", chat)

                elif text == "Consultar saldo" and chat in USERS:
                    total(chat)

                elif text == "Consultar transacciones de un miembro" and chat in USERS:
                    send_message("Para consultar las transacciones de un miembro, utiliza el comando /miembro seguido del nombre de la persona. Ejemplo; /miembro Juan", chat)

                elif text == "Consultar últimas transacciones" and chat in USERS:
                    last(chat)

                elif text == "Eliminar la última transacción" and user == ADMIN:
                    del_last()
                    send_message("Transacción eliminada con éxito", chat)

                elif "Rol" in text and chat in USERS:
                    items = ["Registrar un nuevo aventurero","Subir de nivel un aventurero", "Ascender a un aventurero", "Calcular experiencia", "Buscar aventureros", "Publicar una misión", "Aposteitor"]
                    keyboard = build_keyboard(items)
                    send_message("Selecciona la opción que deseas realizar.", chat, keyboard)
                elif text == "Registrar un nuevo aventurero" and chat in USERS:
                    send_message("Para añadir un nuevo aventurero, utiliza el comando /nuevo_aventurero seguido de su nombre, su nivel y su rango. Ejemplo: /nuevo_aventurero Jon Snow 5 novato. Ten en cuenta que el aventurero se asignará a tu perfil, no registres aventureros de otros.", chat)
                elif text == "Ascender a un aventurero" and chat in USERS:
                    send_message("Para ascender a un aventurero, utiliza el comando /ascender seguido del nombre del aventurero y su nuevo rango. Ejemplo: /ascender Jon Snow comandante", chat)
                elif text == "Subir de nivel un aventurero" and chat in USERS:
                    send_message("Para subir de nivel a un aventurero, utiliza el comando /subir_nivel seguido del nombre del aventurero y su nuevo nivel. Ejemplo: /subir_nivel Jon Snow 6", chat)
                elif text == "Buscar aventureros" and chat in USERS:
                    send_message("Utiliza los comandos /personajes seguido del nombre de un jugador o /rango seguido de un rango para ver la lista de personajes con esas características. Ejemplos: /personajes Luis o /rango Novato", chat)
                elif text == "Calcular experiencia" and chat in USERS:
                    send_message("Para calcular la experiencia por combate, introduce los monstruos derrotados usando el comando /monstruo seguido de la cantidad de monstruos de ese tipo y de su Valor de Desafío (un comando por cada tipo de criatura). Ejemplo: /monstruo 2 8 añadiría dos monstruos de VD 8. \n A continuación añade los aventureros participantes usando el comando /aventurero seguido de su nombre (deben estar registrado en la base de datos). Ejemplo: /aventurero Jon Snow. \n Por último, utiliza el comando /calcular para indicar que has acabado de introducir los datos y recibirás la experiencia a repartir.", chat)
                elif text == "Publicar una misión" and chat in USERS:
                    send_message("Para publicar una misión, envíame el texto comenzando con #nombreDeLaMision y a continuación el mensaje de la misión. Ejemplo: #orcosSexysEnTuZona blablabla. Si lo envías al grupo, anclaré el mensaje, si no, simplemente lo reenviaré.", chat)
                elif text == "Aposteitor" and chat in USERS:
                    send_message("En construcción", chat)
                elif chat in USERS:
                    send_message("No te he entendido bien, ¿me lo repites?", chat)
            else:
                send_message("Aún no tienes acceso a este bot.", chat)

 



def main():
    db.setup_finantial()
    aventureros.setup_adventurers()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        print(updates)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            menu(updates)


if __name__ == '__main__':
    main()
