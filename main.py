from curses import wrapper

def main(stdscr):
    from ui import ChatUI
    stdscr.clear()
    ui = ChatUI(stdscr)
    ui.userlist_add("!calzoneman")
    inp = ""
    while inp != "/quit":
        inp = ui.wait_input()
        ui.chatbuffer_add(inp)

wrapper(main)
