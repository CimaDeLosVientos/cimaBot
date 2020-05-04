import json
import requests
import time
import urllib
import sys
import math
import random
from ..util.telegram_methods import *
from ..util.methods import *
from ..util.checkinator import *
from ..util.states_handler import *


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

participantes = []
monsters = []
chars = []
monstersOK = []
charsOK = []


class GuildHandler(object):
    """docstring for AposteitorHandler"""
    def __init__(self, database):
        self.database = database


###############
# AVENTUREROS #
###############
    @checkinator(("name", check_string), ("lvl", check_positive_int), ("rank", check_rank), ("exp", check_positive_int), ("money", check_positive_int), contains_command=True)
    def inline_nuevo_aventurero(self, arguments):
        if arguments['chat'] in USERS:
            adv = self.database.get_pj(arguments['name'])
            if not adv:
                self.database.add_adventurer(USERSDICT[arguments['user']], arguments['name'], arguments['lvl'], arguments['rank'], arguments['exp'], arguments['money'])
                cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
                write_log(USERSDICT[arguments['user']], arguments['text'])
                send_message("Aventurero añadido con éxito.", arguments['chat'])
            else:
                send_message("Este aventurero ya ha sido registrado previamente.", arguments['chat'])


    @checkinator(("name", check_string), ("rank", check_rank), contains_command=True)
    def inline_ascender(self, arguments):
        auxChar = self.database.get_pj(arguments['name'])
        if auxChar:   
            self.database.rank_up(arguments['name'], arguments['rank'])
            cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
            write_log(USERSDICT[arguments['user']], arguments['text'])
            send_message("Ascenso realizado con éxito", arguments['chat'])
        else:
            send_message("El aventurero especificado no existe.", arguments['chat'])    


    @checkinator(("name", check_string), ("exp", check_positive_int), contains_command=True)
    def inline_repartir_exp(self, arguments):
        if arguments['chat'] in USERS:
            auxChar = self.database.get_pj(arguments['name'])
            if auxChar:
                self.giveExp(auxChar[0][0], auxChar[0][1], auxChar[0][2], arguments['exp'], arguments['chat'])
                cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
                write_log(USERSDICT[arguments['user']], arguments['text'])
                send_message("Experiencia repartida con éxito.", arguments['chat'])
                string = auxChar[0][1] + " ha recibido " + str(arguments['exp']) + " puntos de experiencia extra."
                send_personal_message(string, auxChar[0][0])
            else:
                send_message("El aventurero especificado no existe.", arguments['chat'])


    @checkinator(("name", check_string), ("loot", check_positive_int), contains_command=True)
    def inline_repartir_recompensa(self, arguments):
        if arguments['chat'] in USERS:
            auxChar = self.database.get_pj(arguments['name'])
            if auxChar:
                self.giveMoney(auxChar[0][1], arguments['loot'])
                cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
                write_log(USERSDICT[arguments['user']], arguments['text'])
                send_message("Recompensa añadida a la bolsa del personaje.", arguments['chat'])
            else:
                send_message("El aventurero especificado no existe.", arguments['chat'])


    @checkinator(("name", check_string), ("invoice", check_positive_int), contains_command=True)
    def inline_cobrar(self, arguments):
        auxChar = self.database.get_pj(arguments['name'])
        if auxChar:
            self.takeMoney(auxChar[0][1], arguments['invoice'])
            cambios.add_change(USERSDICT[arguments['user']], arguments['text'])
            write_log(USERSDICT[arguments['user']], arguments['text'])
            send_message("La cantidad fue cobrada de la bolsa del personaje.", arguments['chat'])
        else:
            send_message("El aventurero especificado no existe.", arguments['chat'])

    def inline_personajes(self, arguments):
        data = arguments['text'].split()
        if len(data) == 2:
            self.characters(data[1], arguments['chat'])
        else:
            send_message("Número de datos incorrecto. La sintaxis es /personajes NombreJugador", arguments['chat'])

    def inline_rango(self, arguments):
        data = arguments['text'].split()
        if len(data) == 2:
            self.ranks(data[1], arguments['chat'])
        else:
            send_message("Número de datos incorrecto. La sintaxis es /rango rangoABuscar", arguments['chat'])


########### LAS QUE ESTABAN EN METHODS


    def characters(self, player, chat):
        t = self.database.get_characters(player)
        string = ""
        if not t:
            send_message("El jugador introducido no es correcto. Debe ser uno de los siguientes {}".format(USERNAMES), chat)
        else:
            for w in t:
                l = len(w)
                rank = w[l-3]
                lvl = int(w[l-4])
                xp = int(w[l-2])
                money = float(w[l-1])
                name = w[1]
                if l-5 > 1:
                    for x in range(2, l-4):
                        name = name + " " + w[x]
                string = string + "<b>Jugador:</b> " + w[0] + " <b>PJ:</b> " + name + " " + "<b>Nivel:</b> " + str(lvl) + " " + "<b>Rango:</b> " + rank + " <b>Experiencia:</b> "+ str(xp) + " <b>Dinero:</b> "+ str(money) + "\n"
            send_message(string, chat)

    def ranks(self, rank, chat):
        t = self.database.get_ranks(rank)
        string = ""
        if not t:
            send_message("El rango introducido no es correcto. Debe ser uno de los siguientes {}".format(RANGOS), chat)
        else:
            for w in t:
                l = len(w)
                rank = w[l-3]
                lvl = int(w[l-4])
                xp = int(w[l-2])
                money = float(w[l-1])
                name = w[1]
                if l-5 > 1:
                    for x in range(2, l-4):
                        name = name + " " + w[x]
                string = string + "<b>Jugador:</b> " + w[0] + " <b>PJ:</b> " + name + " " + "<b>Nivel:</b> " + str(lvl) + " " + "<b>Rango:</b> " + rank + " <b>Experiencia:</b> "+ str(xp) + " <b>Dinero:</b> "+ str(money) + "\n"
            send_message(string, chat)

    def mergeMonsters(self, monsters, chat): 
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
        #print(vdVector)
        send_message("Se han reducido los monstruos de igual VD a monstruos únicos de VDs: {}".format(vdVector), chat)
        return vdVector

    def giveExp(self, player, name, currentLevel, xp, chat):
        expPerLevel = {1:0,2:1000,3:3000,4:6000,5:10000,6:15000,7:21000,8:28000,9:36000,10:45000,11:55000,12:66000,13:78000,14:91000,15:105000, 16:120000,17:136000,18:153000,19:171000,20:190000}
        string = "¡"
        currentXP = self.database.get_xp(name)
        finalXP = currentXP[0][0] + xp
        self.database.update_xp(name, finalXP)
        #print(finalXP)
        #print(int(currentLevel))
        #print(expPerLevel[int(currentLevel)])
        if finalXP >= expPerLevel[int(currentLevel) + 1]:
            self.database.level_up(name, int(currentLevel)+1)
            string = string + name + " ha alcanzado el nivel " + str(int(currentLevel) + 1) + "!"
            send_message(string, chat)
            send_personal_message(string, player)

    def giveMoney(self, name, money):
        string = ""
        currentMoney = self.database.get_money(name)
        finalMoney = currentMoney[0][0] + money
        self.database.update_money(name, finalMoney)

    def takeMoney(self, name, money):
        string = ""
        #print(name)
        currentMoney = self.database.get_money(name)
        finalMoney = currentMoney[0][0] - money
        self.database.update_money(name, finalMoney)

    def showQuests(self, chat):
        string = ""
        t = self.database.get_lastQuests()
        for w in t:
            string = string + w[0] + " " + w[1] + " " + str(w[2]) + "/"+ str(w[3]) +"\n"
        send_message(string, chat)

    def findQuest(self, ID,chat):
        string = ""
        w = self.database.get_quest(ID)
        #print(w[0])
        if not w:
            send_message("La misión introducida no está registrada aún.", chat)
        else:
            string = string + w[0][0] + "\n " + w[0][1] + " " + str(w[0][2]) + "/"+ str(w[0][3]) +"/"+ str(w[0][4]) + "\nPersonajes: " + w[0][5] + "\nInforme: " + w[0][6]
            send_message(string, chat)


    def showTournament(self, tournament,chat):
        string = ""
        t = self.database.get_enrollment(tournament)
        for w in t:
            string = string + "<b>" + w[0] + ": </b>" + w[1]
            if str(w[2]) != "-":
                string = string + " <b>Arma:</b> " + str(w[2])
            string = string + "\n"
        send_message(string, chat)

    def showInscriptions(self, chat):
        for t in TOURNAMENTS:
            data = t.split()
            self.showTournament(data[0], chat)

##################


    ############
    # MISIONES #
    ############

    def inline_ultimas_misiones(self, arguments):
        data = arguments['text'].split()
        if len(data) == 1:
            showQuests(misiones, arguments['chat'])
        else:
            send_message("Número de datos incorrecto. La sintaxis es /ultimas_misiones", arguments['chat'])

    def inline_mostrar_mision(self, arguments):
        data = arguments['text'].split()
        if len(data) == 2:
            findQuest(misiones, data[1], arguments['chat'])
        else:
            send_message("Número de datos incorrecto. La sintaxis es /mostrar_mision #mision", arguments['chat'])


    def inline_nueva_mision(self, arguments):
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




    ##############################
    # CALCULADORA DE EXPERIENCIA #
    ##############################
    def inline_monstruo(self, arguments):
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


    def inline_aventurero(self, arguments):
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

    def inline_calcular(self, arguments):
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
    def command_inscripcion_torneo(self, arguments):
        if arguments['chat'] in USERS:
            keyboard = build_keyboard([["Tiro🏹"], ["Fuerza🏋️‍♀️"], ["Obstáculos🚧🏃‍♂️"], ["Magia🔮"]])
            send_message("Selecciona el torneo al que deseas inscribirte.", arguments['chat'], keyboard)

            NextStep(arguments, turney_selection, False)

    @checkinator(("turney", check_turney), contains_command=False)
    def turney_selection(self, arguments):
        if arguments['chat'] in USERS:
            send_message("¿Qué aventurero deseas inscribir?", arguments['chat'])
            if arguments['turney'] == "Tiro":
                NextStep(arguments, adventurer_selection_tiro, False)

            else:
                NextStep(arguments, adventurer_selection, True)

    @checkinator(("name", check_string), contains_command=False)
    def adventurer_selection(self, arguments):
        print("1")
        if arguments['chat'] in USERS:
            inscripciones.add_enrollment(arguments['turney'], arguments['name'], "-")
            send_message("Aventurero inscrito con éxito.", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])

    @checkinator(("name", check_string), contains_command=False)
    def adventurer_selection_tiro(self, arguments):
        print("1")
        if arguments['chat'] in USERS:
            send_message("¿Con qué arma va a competir?", arguments['chat'])
            NextStep(arguments, weapon_selection, True)

    @checkinator(("weapon", check_string), contains_command=False)
    def weapon_selection(self, arguments):
        if arguments['chat'] in USERS:
            inscripciones.add_enrollment(arguments['turney'], arguments['name'], arguments['weapon'])
            send_message("Aventurero inscrito con éxito.", arguments['chat'])
            send_message("Para volver al Menú principal, pincha en /menu", arguments['chat'])


    def inline_inscripciones(self, arguments):
        data = arguments['text'].split()
        if len(data) == 1:
            showInscriptions(inscripciones, arguments['chat'])
        elif len(data) == 2:
            showTournament(inscripciones, data[1], arguments['chat'])
        else:
            send_message("Número de datos incorrecto. La sintaxis es /inscripciones [nombreDelTorneo]", arguments['chat'])



## Tienes que meditar si los metodos inline pueden dar problemas.