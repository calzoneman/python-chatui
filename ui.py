import curses

class ChatUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.userlist = []
        self.win_userlist = stdscr.derwin(curses.LINES - 1, 16, 0, 0)
        self.inputbuffer = ""
        self.win_chatline = stdscr.derwin(2, curses.COLS, 
                                          curses.LINES - 2, 0)
        self._draw_chatline()
        self.chatbuffer = []
        self.win_chatbuffer = stdscr.derwin(curses.LINES - 2,
                                            curses.COLS - 16,
                                            0,
                                            16)

    def _draw_chatline(self):
        h, w = self.win_chatline.getmaxyx()
        self.win_chatline.addstr(0, 0, "-" * w)
        self.win_chatline.addstr(1, 0, self.inputbuffer)
        self.win_chatline.refresh()

    def _draw_userlist(self):
        h, w = self.win_userlist.getmaxyx()
        for i, name in enumerate(self.userlist):
            if i >= h:
                break
            name = name.ljust(15) + "|"
            self.win_userlist.addstr(i, 0, name)
        if len(self.userlist) < h:
            for i in range(len(self.userlist), h - 1):
                self.win_userlist.addstr(i, 0, " " * 15 + "|")
        self.win_userlist.refresh()

    def _draw_chatbuffer(self):
        self.win_chatbuffer.clear()
        h, w = self.win_chatbuffer.getmaxyx()
        j = len(self.chatbuffer) - h
        if j < 0:
            j = 0
        for i in range(min(h, len(self.chatbuffer))):
            self.win_chatbuffer.addstr(i, 0, self.chatbuffer[j])
            j += 1
        self.win_chatbuffer.refresh()

    def userlist_add(self, name):
        inserted = False
        for i in range(len(self.userlist)):
            if self.userlist[i].lower() >= name.lower():
                self.userlist.insert(i, name)
                inserted = True
                break
        if not inserted:
            self.userlist.append(name)

        self._draw_userlist()

    def userlist_remove(self, name):
        self.userlist.remove(name)
        self._draw_userlist()

    def chatbuffer_add(self, msg):
        w = curses.COLS - 17
        while len(msg) >= w:
            self.chatbuffer.append(msg[:w])
            msg = msg[w:]
        if msg:
            self.chatbuffer.append(msg)

        self._draw_chatbuffer()

    def wait_input(self):
        self.win_chatline.cursyncup()
        last = -1
        while last != ord('\n'):
            last = self.stdscr.getch()
            if last == ord('\n'):
                tmp = self.inputbuffer
                self.inputbuffer = ""
                self.win_chatline.clear()
                self._draw_chatline()
                self.win_chatline.cursyncup()
                return tmp
            elif last == curses.KEY_BACKSPACE:
                self.inputbuffer = self.inputbuffer[:-1]
                self.win_chatline.clear()
            else:
                self.inputbuffer += chr(last)
            self._draw_chatline()
