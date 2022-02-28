
import tkinter as tk
from typing import Tuple

from Player import Player

Point = Tuple[int,int]
"""Tuple of two coords, x & y"""

Rect = Tuple[int,int,int,int]
"""Tuple of four coords (x, y, width, height)"""

class App:

    def __init__(self):
        self.root = tk.Tk()                                                         # Create root window
        self.root.title("AI Project Application")
        self.menubar = tk.Menu(self.root)                                           # Create master menu bar
        self.newmenu = tk.Menu(self.root, tearoff=0)                                # Create 'New' menu cascade
        self.menubar.add_cascade(label="New", menu=self.newmenu)                    # Attach 'New' cascade to menu bar
        self.newmenu.add_command(label="Genetic", command=self.setupGenetic)        # Attach 'New Genetic' command
        self.newmenu.add_command(label="Hill Climb", command=self.setupHillclimb)   # Attach 'New Hill Climb' command
        self.newmenu.add_command(label="Annealing", command=self.setupAnnealing)    # Attach 'New Annealing' command
        self.content = tk.Frame(self.root, background="#111111")                    # Create 'Main Content' Frame
        self.cw :int = 512; self.ch :int = 512
        self.canvas = tk.Canvas(self.content, bg="black", width=self.cw, height=self.ch) # Create Canvas within the main content

        self.canvas.pack()
        self.content.pack()
        self.root.config(menu=self.menubar)
        self.root.mainloop()
    
    def setupGenetic (self):
        p = Player.from_random(2)
        self.drawPlayerDnaL(p, 5, 10)

    def setupHillclimb (self):
        self.clearCanvas()
    
    def setupAnnealing (self):
        p = Player.from_random(3)
        self.drawPlayerDnaL(p, 3, 3, w=400, h=50)

    def clearCanvas (self, c:str='#000'):
        self.canvas.create_rectangle(0,0,self.cw+1, self.ch+1, fill=c, width=0)

    @staticmethod
    def colour (b: bool)->str:
        return 'red' if b else 'green'

    def drawPlayerDnaL (self, p:Player, x:int, y:int, w:int=0, h:int=0):
        sm :int = len(p.strategy)
        im :int = len(p.initMoves)
        M :int = sm + im
        if w <= 0: w = 4*M
        if h <= 0: h = 4            
        ix :float = w / M
        wd :int = min(w,h) // 40
        _x=x; _y=y; _X:float=_x+ix; _Y=y+h
        for i in range(sm):
            c :str = App.colour(p.strategy[i])
            self.canvas.create_rectangle(_x, _y, int(_X), _Y, fill=c, width=wd, outline='white')
            _x = int(_X); _X += ix
        for i in range(im):
            c :str = App.colour(p.initMoves[i])
            self.canvas.create_rectangle(_x, _y, int(_X), _Y, fill=c, width=wd, outline='white')
            _x = int(_X); _X += ix
        

    def drawPlayerDnaS (self, p:Player, r:Rect):
        im :int = len(p.initMoves)
        sm_ :int = 2 ** im
        intervalx :float = r[2] / (sm_+1)
        intervaly :float = r[3] / sm_


        c :str = App.colour(p.strategy[0])
        self.canvas.create_rectangle(*r, fill="#", width=0)
    