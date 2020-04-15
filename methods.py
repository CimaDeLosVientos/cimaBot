# coding=utf-8
import json
import requests
import time
import urllib
import sys
import math
import random
from telegram_methods import *
from config import *

def income(db, name, date, money, chat):
    if name in USERNAMES:
        db.add_transaction("Ingreso", name, int(date[0]), int(date[1]), int(date[2]), abs(float(money)))
        send_message("Ingreso realizado con éxito", chat)
    else:
        send_message("El nombre introducido no es un miembro válido", chat)

def payment(db, name, date, money, chat):
    moneyFloat = float(money)
    if name in USERNAMES:
        db.add_transaction("Pago", name, int(date[0]), int(date[1]), int(date[2]), -abs(moneyFloat))
        send_message("Pago realizado con éxito", chat)
    else:
        send_message("El nombre introducido no es un miembro válido", chat)

def total(db, chat):
    saldo = db.get_total()
    send_message("El saldo de la cuenta es {}€".format(saldo), chat)

def member(db, name, chat):
    string = ""
    t = db.get_transactions(name)
    for w in t:
        string = string + w[0] + " " + w[1] + " " + str(w[2]) + "/"+ str(w[3]) + "/"+ str(w[4]) + " " + str(w[5]) + "€" + "\n"
    send_message(string, chat)

def last(db, chat):
    string = ""
    t = db.get_last()
    for w in t:
        string = string + w[0] + " " + w[1] + " " + str(w[2]) + "/"+ str(w[3]) + "/"+ str(w[4]) + " " + str(w[5]) + "€" +"\n"
    send_message(string, chat)

def characters(aventureros, player, chat):
    t = aventureros.get_characters(player)
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

def ranks(aventureros, rank, chat):
    t = aventureros.get_ranks(rank)
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
    #print(vdVector)
    send_message("Se han reducido los monstruos de igual VD a monstruos únicos de VDs: {}".format(vdVector), chat)
    return vdVector

def giveExp(aventureros, player, name, currentLevel, xp, chat):
    expPerLevel = {1:0,2:1000,3:3000,4:6000,5:10000,6:15000,7:21000,8:28000,9:36000,10:45000,11:55000,12:66000,13:78000,14:91000,15:105000, 16:120000,17:136000,18:153000,19:171000,20:190000}
    string = "¡"
    currentXP = aventureros.get_xp(name)
    finalXP = currentXP[0][0] + xp
    aventureros.update_xp(name, finalXP)
    #print(finalXP)
    #print(int(currentLevel))
    #print(expPerLevel[int(currentLevel)])
    if finalXP >= expPerLevel[int(currentLevel) + 1]:
        aventureros.level_up(name, int(currentLevel)+1)
        string = string + name + " ha alcanzado el nivel " + str(int(currentLevel) + 1) + "!"
        send_message(string, chat)
        send_personal_message(string, player)

def giveMoney(aventureros, name, money):
    string = ""
    currentMoney = aventureros.get_money(name)
    finalMoney = currentMoney[0][0] + money
    aventureros.update_money(name, finalMoney)

def takeMoney(aventureros, name, money):
    string = ""
    #print(name)
    currentMoney = aventureros.get_money(name)
    finalMoney = currentMoney[0][0] - money
    aventureros.update_money(name, finalMoney)

def showQuests(misiones, chat):
    string = ""
    t = misiones.get_lastQuests()
    for w in t:
        string = string + w[0] + " " + w[1] + " " + str(w[2]) + "/"+ str(w[3]) +"\n"
    send_message(string, chat)

def findQuest(misiones, ID,chat):
    string = ""
    w = misiones.get_quest(ID)
    #print(w[0])
    if not w:
        send_message("La misión introducida no está registrada aún.", chat)
    else:
        string = string + w[0][0] + "\n " + w[0][1] + " " + str(w[0][2]) + "/"+ str(w[0][3]) +"/"+ str(w[0][4]) + "\nPersonajes: " + w[0][5] + "\nInforme: " + w[0][6]
        send_message(string, chat)

def showTriggers(triggers, chat):
    string = ""
    t = triggers.get_triggers()
    for w in t:
        string = string + "<b>Comando:</b> " + w[0] + " <b>Tipo:</b> " + w[1] +"\n"
    send_message(string, chat)

def showTournament(inscripciones, tournament,chat):
    string = ""
    t = inscripciones.get_enrollment(tournament)
    for w in t:
        string = string + "<b>" + w[0] + ": </b>" + w[1]
        if str(w[2]) != "-":
            string = string + " <b>Arma:</b> " + str(w[2])
        string = string + "\n"
    send_message(string, chat)

def showInscriptions(inscripciones, chat):
    for t in TOURNAMENTS:
        data = t.split()
        showTournament(inscripciones, data[0], chat)
