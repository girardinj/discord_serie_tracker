
import re
import webview
import json
import threading

from models import *


def load_settings(make_settings_global=True):
    with open('settings.json', 'r') as file:
        s = ''
        for line in file.readlines():
            s += line

        if make_settings_global:
            global SETTINGS
        SETTINGS = json.loads(s)
        return SETTINGS

def start_client(client):
    client.run()

def start_gui(client):
    api = Api.Api(client)
    webview.create_window(SETTINGS['TITLE'], './index.html', js_api=api)
    webview.start()


def main():

    load_settings()
    
    client = Client.Client(SETTINGS)
    x = threading.Thread(target=start_client, args=(client,), daemon=True) # daemon to force kill when main is finished
    x.start()
    
    start_gui(client)

def t():
    pattern = Client.Pattern('bonjour [NAME], moi c\'est [SURNAME], au fait il est [HOUR]', '[NAME]', '[SURNAME]', '[HOUR]')

    print(pattern.get({'[NAME]': 'Jarod', '[SURNAME]': 'Chabs', '[HOUR]': '10h10'}))

if __name__ == '__main__':
    main()
