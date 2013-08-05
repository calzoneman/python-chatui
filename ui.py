import curses

class ChatUI:
    def __init__(self, stdscr, userlist_width=16):
        self.stdscr = stdscr
        self.userlist = []
        self.inputbuffer = ""
        self.chatbuffer = []

        # Curses, why must you confuse me with your height, width, y, x
        userlist_hwyx = (curses.LINES - 2, userlist_width - 1, 0, 0)
        chatbuffer_hwyx = (curses.LINES - 2, curses.COLS-userlist_width-1,
                           0, userlist_width + 1)
        chatline_yx = (curses.LINES - 1, 0)
        self.win_userlist = stdscr.derwin(*userlist_hwyx)
        self.win_chatline = stdscr.derwin(*chatline_yx)
        self.win_chatbuffer = stdscr.derwin(*chatbuffer_hwyx)
        
        self.redraw_ui()

    def redraw_ui(self):
        """Redraws the entire UI"""
        u_h, u_w = self.win_userlist.getmaxyx()
        self.stdscr.vline(0, u_w + 1, "|", curses.LINES - 2)
        self.stdscr.hline(curses.LINES - 2, 0, "-", curses.COLS)
        self.stdscr.refresh()

        self.redraw_userlist()
        self.redraw_chatbuffer()
        self.redraw_chatline()

    def redraw_chatline(self):
        """Redraw the user input textbox"""
        h, w = self.win_chatline.getmaxyx()
        #self.win_chatline.addstr(0, 0, "-" * w)
        start = len(self.inputbuffer) - w + 1
        if start < 0:
            start = 0
        self.win_chatline.addstr(0, 0, self.inputbuffer[start:])
        self.win_chatline.refresh()

    def redraw_userlist(self):
        """Redraw the userlist"""
        self.win_userlist.clear()
        h, w = self.win_userlist.getmaxyx()
        for i, name in enumerate(self.userlist):
            if i >= h:
                break
            #name = name.ljust(w - 1) + "|"
            self.win_userlist.addstr(i, 0, name)
        self.win_userlist.refresh()

    def redraw_chatbuffer(self):
        """Redraw the chat message buffer"""
        self.win_chatbuffer.clear()
        h, w = self.win_chatbuffer.getmaxyx()
        j = len(self.chatbuffer) - h
        if j < 0:
            j = 0
        for i in range(min(h, len(self.chatbuffer))):
            self.win_chatbuffer.addstr(i, 0, self.chatbuffer[j])
            j += 1
        self.win_chatbuffer.refresh()

    def chatbuffer_add(self, msg):
        """

        Add a message to the chat buffer, automatically slicing it to
        fit the width of the buffer

        """
        u_h, u_w = self.win_userlist.getmaxyx()
        w = curses.COLS - u_w
        while len(msg) >= w:
            self.chatbuffer.append(msg[:w])
            msg = msg[w:]
        if msg:
            self.chatbuffer.append(msg)

        self.redraw_chatbuffer()

    def prompt(self, msg):
        """Prompts the user for input and returns it"""
        self.inputbuffer = msg
        self.redraw_chatline()
        res = self.wait_input()
        res = res[len(msg):]
        return res

    def wait_input(self):
        """

        Wait for the user to input a message and hit enter.
        Returns the message

        """
        self.win_chatline.cursyncup()
        last = -1
        while last != ord('\n'):
            last = self.stdscr.getch()
            if last == ord('\n'):
                tmp = self.inputbuffer
                self.inputbuffer = ""
                self.win_chatline.clear()
                self.redraw_chatline()
                self.win_chatline.cursyncup()
                return tmp
            elif last == curses.KEY_BACKSPACE or last == 127:
                self.inputbuffer = self.inputbuffer[:-1]
                self.win_chatline.clear()
            else:
                self.inputbuffer += chr(last)
            self.redraw_chatline()
