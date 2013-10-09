import curses

stderr = open("stderr.txt", "w")
def dbg(s):
    print(s, file=stderr)

class ChatUI:
    def __init__(self, stdscr, userlist_width=16):
        self.stdscr = stdscr
        self.userlist = []
        self.inputbuffer = ""
        self.linebuffer = []
        self.chatbuffer = []
        self.h, self.w = self.stdscr.getmaxyx()
        self.win_chatbuffer = stdscr.derwin(self.h - 2, self.w, 0, 0)
        self.win_chatline = stdscr.derwin(self.h - 1, 0)
        self.redraw_ui()

    def resize(self):
        """Handles a change in terminal size"""
        h, w = self.stdscr.getmaxyx()

        self.win_chatline.mvwin(h - 1, 0)
        self.win_chatline.resize(1, w)

        self.win_chatbuffer.resize(h - 2, w)

        self.linebuffer = []
        self.redraw_ui()

    def redraw_ui(self):
        """Redraws the entire UI"""
        h, w = self.stdscr.getmaxyx()

        self.stdscr.clear()
        self.stdscr.hline(h - 2, 0, "-", w)
        self.stdscr.refresh()

        self.redraw_chatbuffer()
        self.redraw_chatline()

    def redraw_chatline(self):
        """Redraw the user input textbox"""
        h, w = self.win_chatline.getmaxyx()
        self.win_chatline.clear()
        start = len(self.inputbuffer) - w + 1
        if start < 0:
            start = 0
        self.win_chatline.addstr(0, 0, self.inputbuffer[start:])
        self.win_chatline.refresh()

    def redraw_chatbuffer(self):
        """Redraw the chat message buffer"""
        self.win_chatbuffer.clear()
        h, w = self.win_chatbuffer.getmaxyx()
        lines = []
        for msg in self.chatbuffer[-1:-h:-1][::-1]:
            while len(msg) > w:
                lines.append(msg[:w])
                msg = msg[w:]
            else:
                lines.append(msg)
        dbg(str(lines))
        i = 0
        for msg in lines[-1:-h:-1][::-1]:
            self.win_chatbuffer.addstr(i, 0, msg)
            i += 1
        self.win_chatbuffer.refresh()

    def chatbuffer_add(self, msg):
        """

        Add a message to the chat buffer, automatically slicing it to
        fit the width of the buffer

        """
        self.chatbuffer.append(msg)
        self.redraw_chatbuffer()
        self.redraw_chatline()
        self.win_chatline.cursyncup()

    def prompt(self, msg):
        """Prompts the user for input and returns it"""
        self.inputbuffer = msg
        self.redraw_chatline()
        res = self.wait_input()
        res = res[len(msg):]
        return res

    def wait_input(self, prompt=""):
        """

        Wait for the user to input a message and hit enter.
        Returns the message

        """
        self.inputbuffer = prompt
        self.redraw_chatline()
        self.win_chatline.cursyncup()
        last = -1
        while last != ord('\n'):
            last = self.stdscr.getch()
            if last == ord('\n'):
                tmp = self.inputbuffer
                self.inputbuffer = ""
                self.redraw_chatline()
                self.win_chatline.cursyncup()
                return tmp[len(prompt):]
            elif last == curses.KEY_BACKSPACE or last == 127:
                if len(self.inputbuffer) > len(prompt):
                    self.inputbuffer = self.inputbuffer[:-1]
            elif last == curses.KEY_RESIZE:
                self.resize()
            elif 32 <= last <= 126:
                self.inputbuffer += chr(last)
            self.redraw_chatline()
