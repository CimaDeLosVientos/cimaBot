# coding=utf-8
import json
import requests
import time
import urllib
import sys
import math
import random
from .telegram_methods import *
from ..config import *

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



# AQUI HABÍA COSAS QUE METÍ EN GUILD HANDLER








def showTriggers(triggers, chat):
    string = ""
    t = triggers.get_triggers()
    for w in t:
        string = string + "<b>Comando:</b> " + w[0] + " <b>Tipo:</b> " + w[1] +"\n"
    send_message(string, chat)