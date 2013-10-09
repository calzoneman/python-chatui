from curses import wrapper
from ui import ChatUI

def main(stdscr):
    stdscr.clear()
    ui = ChatUI(stdscr)
    name = ui.wait_input("Username: ")
    inp = ""
    while inp != "/quit":
        inp = ui.wait_input()
        ui.chatbuffer_add(inp)

wrapper(main)
