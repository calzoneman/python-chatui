from curses import wrapper
from ui import ChatUI

def main(stdscr):
    stdscr.clear()
    ui = ChatUI(stdscr, userlist_width=16)
    name = ui.wait_input("Username: ")
    ui.userlist.append(name)
    inp = ""
    while inp != "/quit":
        inp = ui.wait_input()
        ui.chatbuffer_add(inp)

wrapper(main)
