from curses import wrapper
from ui import ChatUI

def main(stdscr):
    stdscr.clear()
    ui = ChatUI(stdscr)
    name = ui.prompt("Username: ")
    ui.userlist.append(name)
    ui.redraw_userlist()
    inp = ""
    while inp != "/quit":
        inp = ui.wait_input()
        ui.chatbuffer_add(inp)

wrapper(main)
