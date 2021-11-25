# Naimportujeme nejaky ty CV knihovny (a vlastne i vsechny ostatni :D)
import sys
import time

import PySimpleGUI as PySG
import cv2
import keyboard
import numpy as nm
import pytesseract
import yaml
from PIL import ImageGrab

PySG.theme('DarkAmber')  # At to neni uplne osklivy
window = "None"
atf_string_clean = "None"

config_file = open("config.yaml")
config = yaml.load(config_file, Loader=yaml.CLoader)
print(config.items)
print(config.get('skip_confirm'))


def mainmenu():
    mainmenu_layout = [
        [PySG.Text('Vítejte v programu ATFTyper!')],
        [PySG.Button('Jebaitovat ATF')],
        [PySG.Button('Ukončit')]]

    global window
    window = PySG.Window('ATFTyper', mainmenu_layout)

    # Event loop pro mainmenu
    while True:
        event, values = window.read()
        if event == PySG.WIN_CLOSED or event == 'Ukončit':  # kdyz uzivatel zavre okno nebo stiskne ukoncit
            sys.exit()

        elif event == 'Jebaitovat ATF':
            window.close()
            atf_jebaiter_init()


# Jde se jebaitit
def atf_jebaiter_init():
    # Tady musi byt cesta k exe s PyTesseractem
    if config.get('use_system_tesseract') is True:
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    else:
        pytesseract.pytesseract.tesseract_cmd = 'Tesseract-builtin\\tesseract.exe'
    # ImageGrab-Ve smycce zaznamena obrazovku.
    # Bbox nas necha vzit si jenom urcitou oblast.
    cap = ImageGrab.grab(bbox=config.get('bbox'))
    if config.get('area_debug') is True:
        cap.show()
    else:
        pass

    # Pred prevedenim na text si prevedeme obrazek na cernobilou, pro jednodussi rozpoznatelnost
    atf_string = pytesseract.image_to_string(
        cv2.cvtColor(nm.array(cap), cv2.COLOR_BGR2GRAY),
        lang='ces',
        config='-c page_separator='' textord_space_size_is_variable=1')

    print(atf_string)
    global atf_string_clean
    atf_string_clean = atf_string[:-1]
    if atf_string == ' \n':
        atfjebaiter_layout = [
            [PySG.Text('ATF není momentálně spuštěno!')],
            [PySG.Button('Hlavní nabídka')],
            [PySG.Button('Ukončit')]]

        global window
        window = PySG.Window('ATFTyper', atfjebaiter_layout)

        # Event loop pro atffail
        while True:
            event, values = window.read()
            if event == PySG.WIN_CLOSED or event == 'Ukončit':  # kdyz uzivatel zavre okno nebo stiskne ukoncit
                sys.exit()

            elif event == 'Hlavní nabídka':
                window.close()
                mainmenu()

    else:
        if config.get('skip_confirm') is True:
            atf_jebaiter_type()
        else:
            atfjebaiter_layout = [
                [PySG.Text('Text detekován!')],
                [PySG.Text('Zkontrolujte zda je text správný')],
                [PySG.Text(atf_string_clean)],
                [PySG.Button('Zkusit znovu'), PySG.Button('Pokračovat')]]

            window = PySG.Window('ATFTyper', atfjebaiter_layout)

            # Event loop pro atffail
            while True:
                event, values = window.read()
                if event == PySG.WIN_CLOSED or event == 'Ukončit':  # kdyz uzivatel zavre okno nebo stiskne ukoncit
                    sys.exit()

                elif event == 'Zkusit znovu':
                    window.close()
                    atf_jebaiter_init()

                elif event == 'Pokračovat':
                    window.close()
                    atf_jebaiter_type()


def atf_jebaiter_type():
    typing_layout = [
        [PySG.Text('Jste si jisti že chcete začít s jebaitem?')],
        [PySG.Button('Jde se psát!')],
        [PySG.Button('Hlavní nabídka'), PySG.Button('Ukončit')]]

    global window
    global atf_string_clean
    window = PySG.Window('ATFTyper', typing_layout)

    # Event loop pro mainmenu
    while True:
        event, values = window.read()

        if event == PySG.WIN_CLOSED or event == 'Ukončit':  # kdyz uzivatel zavre okno nebo stiskne ukoncit
            sys.exit()

        elif event == 'Jde se psát!':
            time.sleep(2)
            keyboard.write(atf_string_clean)
            window.close()
            linewrite_ok()


def linewrite_ok():
    typing_layout = [
        [PySG.Text('Chcete psát další řádek?')],
        [PySG.Button('Ano!')],
        [PySG.Button('Hlavní nabídka'), PySG.Button('Ukončit')]]

    global window
    global atf_string_clean
    window = PySG.Window('ATFTyper', typing_layout)

    # Event loop pro mainmenu
    while True:
        event, values = window.read()

        if event == PySG.WIN_CLOSED or event == 'Ukončit':  # kdyz uzivatel zavre okno nebo stiskne ukoncit
            sys.exit()

        elif event == 'Ano!':
            time.sleep(2)
            keyboard.write(' ')
            window.close()
            atf_jebaiter_init()

        elif event == 'Hlavní nabídka':
            window.close()
            mainmenu()


# Calling the function
mainmenu()
