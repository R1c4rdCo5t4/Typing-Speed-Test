import curses
from curses import wrapper
import time
import requests
import json

DEFAULT = 1
RED = 2
GREEN = 3
CYAN = 4
BLUE = 5
YELLOW = 6


def getColor(color):
    return curses.color_pair(color)

def get_text():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        text = json_data[0]['q']

    except:
        text = "The fox jumps over the lazy dog"
    return text.rstrip(".")


def menu(stdscr):
    stdscr.clear()
    stdscr.addstr("Press any key to start the typing test!", getColor(CYAN))
    stdscr.refresh()
    stdscr.getkey()
    

def display_text(stdscr, target, current, wpm,errors):

    display_score(stdscr,wpm,errors)
    for i, char in enumerate(current):
        correct_char = target[i]
        if char == correct_char:
            stdscr.addstr(0,i,char, getColor(CYAN))
        else:
            current.pop()
            

def display_score(stdscr,wpm,errors):
    wpm_color, err_color = DEFAULT, DEFAULT

    if wpm != 0:
        if wpm < 40 :
            wpm_color  = RED
        elif wpm < 70:
            wpm_color = YELLOW
        else:
            wpm_color = GREEN

        if errors > 0:
            err_color = RED

    wpm_text = "WPM:"
    stdscr.addstr(1,0,wpm_text, getColor(DEFAULT))
    stdscr.addstr(1,1+len(wpm_text),str(wpm),getColor(wpm_color))

    err_text = "Errors:"
    stdscr.addstr(1,10,err_text,getColor(DEFAULT))
    stdscr.addstr(1,11+len(err_text),str(errors),getColor(err_color))


def wpm_test(stdscr,target_text):
    current_text = []
    wpm = 0
    errors = 0
    start = time.time()
    stdscr.erase()
    stdscr.addstr(target_text)

    while True:
        elapsed = max(time.time() - start, 1)
        wpm = round((len(current_text) / (elapsed / 60)) / 5)
        
        for i, char in enumerate(current_text):
            correct_char = target_text[i]
            if char != correct_char:
                errors += 1

        display_text(stdscr,target_text,current_text,wpm,errors)
        stdscr.nodelay(True)
        stdscr.refresh()

        if (len("".join(current_text)) == len(target_text)):
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except: 
            continue

        if(ord(key)== 27):
            break
        if key in ("KEY_BACKSPACE", '\b','\x7f'):
            if len(current_text) > 0:
                current_text.pop()

        elif (len(current_text) < len(target_text)):
            current_text.append(key)
            
            

def main(stdscr):
    curses.init_pair(DEFAULT, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(CYAN, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(BLUE,curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(YELLOW,curses.COLOR_YELLOW, curses.COLOR_BLACK)

    menu(stdscr)
    while True:
        text = get_text().replace("  ","")
        wpm_test(stdscr,text)
        stdscr.addstr(2,0,"You completed the text! Press any key to try again...")

        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)
