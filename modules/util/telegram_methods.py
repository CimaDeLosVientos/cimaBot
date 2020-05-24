# coding=utf-8
import json
import requests
import time
import urllib
import sys
import math
import random

from ..config import *


def make_request(url):
    """
    Makes a request. This request can generate events in the bot, such as sending messages.
    
    :param      url:  The url
    :type       url:  String http://es.python-requests.org/es/latest/user/quickstart.html
    """

    ## content = response.content.decode("utf8") # No le veo utilidad a esto. Lo cambio por que retorne el response directamente, donde el content si es interesante.
    return requests.get(URL + url)


def get_json_from_url(url):
    """
    Get the json response from a url request.
    
    :param      url:  The url
    :type       url:  String
    """
    content = make_request(url).content.decode("UTF-8")
    js = json.loads(content)
    return js


def get_updates(offset=None):
    """
    Get the updates. Any interaction with the bot will generate an update. From this update the JSON with which to work is extracted.
    
    :param      offset:  Identifier of the first update to be returned. https://core.telegram.org/bots/api#getting-updates
    :type       offset:  Integer
    """
    url = "getUpdates?timeout=500"
    if offset:
        url += "&offset={}".format(offset)
    json = get_json_from_url(url)
    return json


def get_last_update_id(updates):
    """
    Gets the last update identifier. This is necessary for get the last update only one time. Maybe it could be done differently, but now it works.
    
    :param      updates:  The updates
    :type       updates:  Dict with updates
    """
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def build_keyboard(buttons, one_time_keyboard = True):
    """
    Builds a keyboard.
    
    :param      buttons:            The buttons
    :type       buttons:            String matrix (list of list of String)
    :param      one_time_keyboard:  One time keyboard. If False, the keyboard don't disappear after to push.
    :type       one_time_keyboard:  boolean
    """
    reply_markup = {"keyboard":buttons, "one_time_keyboard": one_time_keyboard}
    return json.dumps(reply_markup)

def send_message(text, chat_id, reply_markup=None):
    """
    Sends a message to a single chat.
    
    :param      text:          The message text 
    :type       text:          String
    :param      chat_id:       The chat identifier
    :type       chat_id:       Integer
    :param      reply_markup:  The reply markup, like a keyboard
    :type       reply_markup:  ReplyMarkup. https://core.telegram.org/type/ReplyMarkup 
    """
    text = urllib.parse.quote_plus(text) # https://docs.python.org/3/library/urllib.parse.html
    url = "sendMessage?text={}&chat_id={}&parse_mode=html".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    make_request(url)

def send_personal_message(text, player, reply_markup=None):
    text = urllib.parse.quote_plus(text)

    chat_id = player #reverseUserDict[player]
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=html".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    make_request(url)

def forward_message(toChat, fromChat, message_id):
    text = urllib.parse.quote_plus(text) # https://docs.python.org/3/library/urllib.parse.html
    url = "forwardMessage?chat_id={}&from_chat_id={}&message_id={}".format(toChat, fromChat, message_id)
    make_request(url)


def write_log(user, text, reply_markup=None):
    LOGGROUP = "-303831194"
    text = user + ":\n" + text
    text = urllib.parse.quote_plus(text)
    url = "sendMessage?text={}&chat_id={}&parse_mode=html".format(text, LOGGROUP)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    make_request(url)


def send_photo(file_id, chat_id):
    """
    Sends a photo. To know the identification of the file, it must be preloaded on the Telegram server.
    
    :param      file_id:  The file identifier
    :type       file_id:  String ?
    :param      chat_id:  The chat identifier
    :type       chat_id:  Integer
    """
    url = "sendPhoto?&chat_id={}&photo={}&parse_mode=html".format(chat_id, file_id)
    make_request(url)


def send_gif(file_id, chat_id):
    """
    Sends a gif. To know the identification of the file, it must be preloaded on the Telegram server.
    
    :param      file_id:  The file identifier
    :type       file_id:  String ?
    :param      chat_id:  The chat identifier
    :type       chat_id:  Integer
    """
    url = "sendAnimation?&chat_id={}&animation={}&parse_mode=html".format(chat_id, file_id)
    make_request(url)

# HACER EL DE STICKERS

# HACER "DE NADA"
def pin_message(chat_id, message_id, notify = False):
    """
    Pins a message in a chat.
    
    :param      chat_id:     The chat identifier
    :type       chat_id:     Integer
    :param      message_id:  The message identifier (the message must be exist already)
    :type       message_id:  Integer
    :param      notif:       The notif
    :type       notif:       boolean
    """
    url = "pinChatMessage?chat_id={}&message_id={}".format(chat_id, message_id)
    if notify:
        url += "&disable_notification=true"
    make_request(url)

