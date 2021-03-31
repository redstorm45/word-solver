
from board import Board
from words import WordMatcher
from solver import Solver
from interface import GraphicalInterface
import threading

class Prog:
    def __init__(self):
        self.board = Board()
        self.matcher = WordMatcher()
        self.solver = Solver()
        self.thread = None
        self.stopping = True
        self.stopped = True
        self.loaded = False

        self.cb_progress = None
        self.cb_options = None

    def attach_interface(self, cb_progress, cb_options):
        self.cb_progress = cb_progress
        self.cb_options = cb_options

    def launch_load(self):
        self._launch(target=self._load)

    def launch_compute(self, letters):
        if not self.loaded:
            return
        self._launch(target=lambda:self._compute(letters))

    def _launch(self, target):
        if self.thread is not None:
            self.stop()
        self.stopping = False
        self.stopped = False
        def wrapped():
            target()
            self.stopped = True
        self.thread = threading.Thread(target=wrapped)
        self.thread.start()

    def stop(self):
        self.stopping = True
        self.thread.join()

    def _load(self):
        def cb_stop():
            return self.stopping

        with open("dico.txt") as file:
            W = file.readlines()
        W = [w.strip().lower() for w in W]
        #W = W[:len(W)//8]
        self.matcher.set_dict(W, self.cb_progress, cb_stop)
        if self.cb_progress is not None:
            self.cb_progress(100, 100)
        self.loaded = True
        print('complete')

    def _compute(self, letters):
        if self.cb_options is None:
            return
        if self.cb_progress is not None:
            self.cb_progress(-1, 30)
        self.cb_options([])
        opts = self.solver.get_options(self.board, self.matcher, letters, lambda:self.cb_progress(-1, 1))
        pairs = [(op, self.board.get_score(op)) for op in opts]
        self.cb_options(pairs)
        if self.cb_progress is not None:
            self.cb_progress(100, 100)

def main():
    prog = Prog()
    itf = GraphicalInterface(prog)
    itf.run()
main()







