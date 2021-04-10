
import time
import tkinter as tk
import tkinter.ttk as ttk
from board import LETTER_POINTS, move_dir
from words import ALPHABET

class Interface:
    def __init__(self, board):
        pass
        
        
class ConsoleInterface(Interface):
    def __init__(self):
        pass


def coord_add(p1, p2):
    return p1[0]+p2[0], p1[1]+p2[1]

def coord_rotate(p):
    return -p[1], p[0]


class LetterCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)

    def draw_letter(self, x, y, letter, full=True, small=False, joker=False):
        color = '#f0ecdd' if full else '#b3afa4'
        text_color = '#010101' if not joker else '#747576'
        if not small:
            i1 = self.create_oval(x+1,  y+1,  x+6,  y+6, width=0, fill=color)
            i2 = self.create_oval(x+23, y+1,  x+28, y+6, width=0, fill=color)
            i3 = self.create_oval(x+23, y+23, x+28, y+28, width=0, fill=color)
            i4 = self.create_oval(x+1,  y+23, x+6,  y+28, width=0, fill=color)
            i5 = self.create_rectangle(x+1,y+3, x+29, y+27, width=0, fill=color)
            i6 = self.create_rectangle(x+3,y+1, x+27, y+29, width=0, fill=color)
            i7 = self.create_text(x+15, y+15, text=letter.upper(), state='disabled', font=('Helvetica', '14', 'bold'), fill=text_color)
            L = [i1, i2, i3, i4, i5, i6, i7]
            if letter != ' ' and not joker:
                L += [self.create_text(x+23, y+23, text=str(LETTER_POINTS[letter]), state='disabled', font=('Helvetica', '6'), fill=text_color)]
        else:
            i1 = self.create_rectangle(x,y, x+20, y+20, width=0, fill=color)
            i2 = self.create_text(x+10, y+10, text=letter.upper(), state='disabled', font=('Helvetica', '10', 'bold'))
            L = [i1, i2]
        return L


class CanvasBoard(LetterCanvas):
    def __init__(self, parent, board):
        LetterCanvas.__init__(self, parent, width=30*board.width()+20, height=30*board.height()+20)
        self.board = board
        self.letters = []
        self.temp_letters = []
        self.displayed_opt = None
        self._setup()

    def _setup(self):
        # board back
        self.create_rectangle(10,10,10+30*self.board.width(),10+30*self.board.height(), fill="#7db364", width=0)
        # special cells
        for i in range(self.board.height()):
            for j in range(self.board.width()):
                color = None
                if self.board.back[i][j] == 'w3':
                    color = "#b51d1d"
                elif self.board.back[i][j] == 'w2':
                    color = "#e06767"
                elif self.board.back[i][j] == 'l3':
                    color = "#031691"
                elif self.board.back[i][j] == 'l2':
                    color = "#5a7fe6"
                if color is not None:
                    self.create_rectangle(10+30*j, 10+30*i, 40+30*j, 40+30*i, fill=color, width=0)
                    L = []
                    if i>0:
                        L.append(3)
                    if j>0:
                        L.append(2)
                    if i<self.board.height()-1:
                        L.append(1)
                    if j<self.board.width()-1:
                        L.append(0)
                    for k in L:
                        pts = [(10, 10), (20, 0), (10, -10)]
                        for e in range(k):
                            pts = [coord_rotate(p) for p in pts]
                        pts = [coord_add(p, (25+30*j, 25+30*i)) for p in pts]
                        self.create_polygon(pts, fill=color, width=0)
        # lines
        for i in range(self.board.height()+1):
            self.create_line(10, 10+30*i, 10+30*self.board.width(), 10+30*i, fill="#555555", width=2)
        for j in range(self.board.width()+1):
            self.create_line(10+30*j, 10, 10+30*j, 10+30*self.board.width(), fill="#555555", width=2)

    def update(self):
        for i in self.letters:
            self.delete(i)
        self.letters = []
        for i in range(self.board.height()):
            for j in range(self.board.width()):
                if self.board.front[i][j] is not None:
                    self.letters += self.draw_letter(10+30*j, 10+30*i, self.board.front[i][j], joker=self.board.jokers[i][j])

    def display_opt(self, opt):
        for i in self.temp_letters:
            self.delete(i)
        self.temp_letters = []
        self.displayed_opt = opt
        if opt is None:
            return
        for k in range(len(opt)):
            if opt.main_pattern[k] != '_':
                i,j = move_dir(opt.start, opt.direction, k)
                self.temp_letters += self.draw_letter(10+30*j, 10+30*i, opt.main_pattern[k], full=False, joker=opt.main_jokers[k])


class LetterBar(LetterCanvas):
    def __init__(self, parent):
        LetterCanvas.__init__(self, parent, width=300, height=50)
        self.letters = []
        self.string = ['.']*7
        self.selected = None
        self._setup()
        self.update_letters()

        self.bind('<Button-1>', self.on_click)

    def _setup(self):
        self.create_rectangle(5, 20, 295, 40, fill='#03330b', width=0)
        self.create_rectangle(0, 20, 5, 40, fill='#027016', width=0)
        self.create_rectangle(295, 20, 300, 40, fill='#027016', width=0)
        self.create_rectangle(0, 40, 300, 45, fill='#027016', width=0)

    def update_letters(self):
        for i in self.letters:
            self.delete(i)
        self.letters = []
        for k in range(7):
            if self.string[k] == '.':
                y = 0 if k==self.selected else 10
                self.letters += [self.create_oval(30+40*k, y+20, 40+40*k, y+30, fill='#58595a', width=0)]
            else:
                y = 0 if k==self.selected else 10
                self.letters += self.draw_letter(15+40*k, y, self.string[k])

    def on_click(self, event):
        k = (event.x-10)//40
        if k>=0 and k<7:
            if self.selected == k:
                self.selected = None
            else:
                self.selected = k
        else:
            self.selected = None
        self.update_letters()

    def on_key(self, event):
        print("key press: '{}'".format(event.char))
        if self.selected is None:
            return
        if (event.char in ALPHABET or event.char == ' ') and len(event.char)>0:
            self.string[self.selected] = event.char
            if self.selected < 6:
                self.selected += 1
            self.update_letters()

    def on_back(self, event):
        print("key press: '{}'".format(event.char))
        if self.selected is None:
            return
        self.string[self.selected] = '.'
        if self.selected > 0:
            self.selected -= 1
        self.update_letters()

    def remove_used(self, opt):
        current = [e for e in self.string if e != '.']
        for e in opt.used_letters():
            if e in current:
                current.remove(e)
            elif ' ' in current:
                current.remove(' ')
        self.string = current + ['.' for i in range(7-len(current))]
        self.update_letters()


class MultiOptionDisplay(LetterCanvas):
    def __init__(self, parent, cb_select, **kwargs):
        LetterCanvas.__init__(self, parent, width=350, height=0, **kwargs)
        self.cb_select = cb_select
        self.bind('<Button-1>', self.select)
        self.current_options = []

    def draw_option(self, index, pair):
        opt, pt = pair
        back_id = self.create_rectangle(0, 30*index, 350, 30*(index+1), width=0, fill='#868686', state='hidden')
        text_id = self.create_text(1, 30*index+15, text=str(pt), state='disabled', font=('Helvetica', '20', 'bold'), anchor=tk.W)
        letter_ids = []
        text = opt.combined_main()
        for i in range(len(opt)):
            full = opt.main_board[i] == '_'
            letter_ids += self.draw_letter(50+20*i, 30*index+5, text[i], full=full, small=True, joker=opt.main_jokers[i])
        return [back_id, text_id] + letter_ids
    
    def set_options(self, pairs):
        for pair, drawn in self.current_options:
            for d in drawn:
                self.delete(d)
        self.current_options = []
        for i, pair in enumerate(pairs):
            self.current_options.append((pair, self.draw_option(i, pair)))
        self.configure(scrollregion="0 0 350 {}".format(len(pairs)*30))

    def select(self, event):
        ycv = self.canvasy(event.y)
        selected = int(ycv / 30)
        if selected >= 0 and selected < len(self.current_options):
            self.cb_select(self.current_options[selected][0][0])
            full_opt = self.current_options[selected]
            self.itemconfigure(full_opt[1][0], state='normal')

    def deselect(self):
        for full_opt in self.current_options:
            self.itemconfigure(full_opt[1][0], state='hidden')


class OptionSelector(tk.Frame):
    def __init__(self, parent, cb_select):
        tk.Frame.__init__(self, parent)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=True)
        self.canvas = MultiOptionDisplay(self, cb_select=self.handle_select, bd=0, highlightthickness=0, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.drawn = []

        self.cb_select = cb_select
        self.selected = None

    def set_options(self, pairs):
        self.canvas.set_options(pairs)

    def deselect(self):
        self.selected = None
        self.canvas.deselect()

    def scroll(self, delta):
        self.canvas.yview_scroll(delta, "units")

    def handle_select(self, opt):
        self.deselect()
        self.selected = opt
        self.cb_select(opt)


class QuickOptionSelector(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        self.option_list = []
        self.option_widgets = []
        self.active = False
        if 'options' in kwargs.keys():
            self.option_list = kwargs['options']
            del kwargs['options']
        kwargs['command'] = self.show_options
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.make_subframe()
    
    def configure(self, *args, **kwargs):
        if 'options' in kwargs.keys():
            self.option_list = kwargs['options']
            self.make_subframe()
            del kwargs['options']
        kwargs['command'] = self.show_options
        tk.Button.configure(self, *args, **kwargs)
        
    def make_subframe(self):
        self.subframe = tk.Frame(self.master, borderwidth=2, bg='#e2e3e4')
        self.subframe_grower = tk.Frame(self.subframe, width=100, height=0)
        self.subframe_grower.pack()
        self.option_widgets = []
        for opt, cb in self.option_list:
            bt = tk.Label(self.subframe, text=opt, anchor=tk.W, bg='#f2f3f4')
            bt.pack(fill=tk.X)
            self.option_widgets.append(bt)
        def set_active(e):
            self.active = True 
        def set_inactive(e):
            self.active = False
            self.after(100, self.check_active)
        self.subframe.bind('<Enter>', set_active)
        self.subframe.bind('<Leave>', set_inactive)
        self.bind('<Enter>', set_active)
        self.bind('<Leave>', set_inactive)
        
    def show_options(self):
        self.configure(relief=tk.SUNKEN)
        self.subframe.place(anchor="sw", x=self.winfo_x(), y=self.winfo_y())
        
    def check_active(self):
        if not self.active and self.subframe.winfo_ismapped():
            self.subframe.place_forget()
            self.configure(relief=tk.RAISED)


class GraphicalInterface(Interface):
    def __init__(self, prog):
        self.prog = prog

        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.handle_close)
        self.root.title("Scrabble solver")

        self.canvas_board = CanvasBoard(self.root, self.prog.board)
        self.canvas_board.grid(column=0, row=0)

        self.search_bar = tk.Frame(self.root)
        self.search_bar.grid(column=0, row=1)

        self.letter_bar = LetterBar(self.search_bar)
        self.letter_bar.pack(side=tk.LEFT)
        self.root.bind('<Key>', self.letter_bar.on_key)
        self.root.bind('<BackSpace>', self.letter_bar.on_back)
        #self.search_spacer = tk.Frame(self.search_bar, width=50)
        #self.search_spacer.pack(side=tk.LEFT)
        self.search_button = tk.Button(self.search_bar, text='Go', command=self.handle_compute)
        self.search_button.pack(side=tk.LEFT)
        self.clear_button = tk.Button(self.search_bar, text="Clear", command=self.handle_clear)
        self.clear_button.pack(side=tk.LEFT)

        self.selector = OptionSelector(self.root, self.handle_select)
        self.selector.grid(column=1, row=0, columnspan=4, sticky=tk.N+tk.S+tk.E+tk.W, padx=10, pady=10)
        self.root.bind("<Button-4>", self.handle_mousewheel)
        self.root.bind("<Button-5>", self.handle_mousewheel)

        self.place_button = tk.Button(self.root, text="Place", command=self.handle_place)
        self.place_button.grid(column=1, row=1)
        self.import_board_button = QuickOptionSelector(self.root, text="Import board", options=[
            ("Csv/Excel", self.handle_import_csv_board)])
        self.import_board_button.grid(column=2, row=1)
        self.export_board_button = QuickOptionSelector(self.root, text="Export board", options=[
            ("Csv/Excel", self.handle_export_csv_board)])
        self.export_board_button.grid(column=3, row=1)
        self.clear_board_button = tk.Button(self.root, text="Clear board", command=self.handle_clear_board)
        self.clear_board_button.grid(column=4, row=1)

        self.status = tk.Frame(self.root)
        self.status.grid(column=0, columnspan=3, row=2)

        self.status_label_frame = tk.Frame(self.status, width=200, height=20)
        self.status_label_frame.pack_propagate(0)
        self.status_label_frame.pack(side=tk.LEFT)

        self.status_label = tk.Label(self.status_label_frame, text="Loading", anchor=tk.W)
        self.status_label.pack(fill=tk.BOTH, side=tk.LEFT, expand=1)

        self.progress = ttk.Progressbar(self.status, orient=tk.HORIZONTAL, length=350, mode='determinate')
        self.progress.configure(value=0)
        self.progress.pack(side=tk.LEFT)
        
        self.progress_skip = 0
        self.progress_indeterminate = None
        self.invalid_board = True

    def update_progress(self, pos, total):
        self.root.after(0, lambda :self._update_progress(pos, total))
    
    def _update_progress(self, pos, total):
        if pos == -1:
            if self.progress_indeterminate is None:
                self.status_label.configure(text="Computing...")
                self.progress.configure(value=1, maximum=total, mode='indeterminate')
                self.progress_indeterminate = time.time()
            else:
                t = time.time()
                if t-self.progress_indeterminate > 0.2:
                    self.progress.step(2)
                    self.progress_indeterminate += 0.2
        else:
            perc = str(100*pos//total)
            if perc == '100':
                text = "Done"
                self.status_label.configure(text=text)
                self.progress.configure(value=pos, maximum=total, mode='determinate')
                self.progress_indeterminate = None
            else:
                self.progress_skip += 1
                if self.progress_skip%50 == 0:
                    text = "Loading ({}%)".format(perc)
                    self.status_label.configure(text=text)
                    self.progress.configure(value=pos, maximum=total, mode='determinate')

    def update_options(self, pairs):
        if self.invalid_board:
            self.root.after(0, lambda:self.selector.set_options([]))
        else:
            pairs = sorted(pairs, key=lambda p:p[1]+len(p[0])/20, reverse=True)
            self.root.after(0, lambda:self.selector.set_options(pairs))

    def handle_close(self):
        self.prog.stopping = True
        if self.prog.stopped:
            self.root.destroy()
        else:
            self.root.after(10, self.handle_close)
            
    def handle_try_compute(self, letters):
        if self.prog.try_stop_compute():
            self.invalid_board = False
            self.prog.launch_compute(letters)
        else:
            self.root.after(10, lambda:self.handle_try_compute(letters))

    def handle_compute(self):
        if not self.prog.loaded:
            return
        letters = ''.join(self.letter_bar.string).replace('.','')
        self.handle_try_compute(letters)

    def handle_mousewheel(self, event):
        if event.num == 4:
            self.selector.scroll(-1)
        elif event.num == 5:
            self.selector.scroll(1)

    def handle_select(self, opt):
        self.canvas_board.display_opt(opt)

    def handle_clear(self):
        self.selector.deselect()
        self.canvas_board.display_opt(None)

    def handle_clear_board(self):
        self.selector.deselect()
        self.canvas_board.display_opt(None)
        self.prog.board.clear_all()
        self.canvas_board.update()

    def handle_place(self):
        if self.selector.selected is not None:
            self.prog.board.place(self.selector.selected)
            self.canvas_board.display_opt(None)
            self.canvas_board.update()
            self.letter_bar.remove_used(self.selector.selected)
            self.selector.set_options([])
            
    def handle_invalidate(self):
        self.selector.set_options([])
            
    def handle_import_csv_board(self):
        pass
            
    def handle_export_csv_board(self):
        pass
        
    def run(self):
        self.canvas_board.update()
        self.prog.attach_interface(self.update_progress, self.update_options)

        self.root.after(0, self.prog.launch_load())
        self.root.mainloop()

        self.prog.stop()




