
'''

-  N

O  0--E  j
   |
   S  +

   i
'''


BOARD_DEF = {
    'w3': [(0,0), (7,0)],
    'w2': [(1,1), (2,2), (3,3), (4,4), (7, 7)],
    'l3': [(5,5), (5, 1)],
    'l2': [(3,0), (6,2), (7,3)]
}

OPPOSITE = {'N':'S', 'S':'N', 'E':'O', 'O':'E'}
SIDES = {'S':'OE', 'E':'NS'}

LETTER_POINTS = {
    'a':1,
    'b':3,
    'c':3,
    'd':2,
    'e':1,
    'f':4,
    'g':2,
    'h':4,
    'i':1,
    'j':8,
    'k':10,
    'l':1,
    'm':2,
    'n':1,
    'o':1,
    'p':3,
    'q':8,
    'r':1,
    's':1,
    't':1,
    'u':1,
    'v':4,
    'w':10,
    'x':10,
    'y':10,
    'z':10,
    ' ':0,
}

def move_dir(pos, direction, times=1):
    i,j = pos
    if direction == 'N':
        return i-times,j
    elif direction == 'S':
        return i+times,j
    elif direction == 'O':
        return i,j-times
    elif direction == 'E':
        return i,j+times

class PlaceOption:
    def __init__(self, start, direction, main_board, main_pattern, main_jokers, sides):
        self.start = start
        self.direction = direction
        self.main_board = main_board
        self.main_pattern = main_pattern
        self.main_jokers = main_jokers
        self.side_patterns = sides

    def combined_main(self):
        s = ''
        for i in range(len(self.main_pattern)):
            if self.main_pattern[i] == '_':
                s += self.main_board[i]
            else:
                s += self.main_pattern[i]
        return s

    def used_letters(self):
        return self.main_pattern.replace('_', '').replace('.', '')

    def complete(self, letter, is_joker):
        k = self.main_pattern.find('.')
        main_pattern = self.main_pattern.replace('.', letter)
        side_patterns = [pat.replace('.', letter) for pat in self.side_patterns]
        jokers = self.main_jokers[:]
        jokers[k] = is_joker
        return PlaceOption(self.start, self.direction, self.main_board, main_pattern, jokers, side_patterns)

    def extend_end(self, board_append, board_sides):
        main_board = self.main_board + '_' + board_append
        main_pattern = self.main_pattern + '.' + '_'*len(board_append)
        side_patterns = self.side_patterns + board_sides
        jokers = self.main_jokers + [False]*(len(board_append)+1)
        return PlaceOption(self.start, self.direction, main_board, main_pattern, jokers, side_patterns)

    def extend_start(self, board_prepend, board_sides):
        main_board = board_prepend + '_' + self.main_board
        main_pattern = '_'*len(board_prepend) + '.' + self.main_pattern
        side_patterns = board_sides + self.side_patterns
        jokers = [False]*(len(board_prepend)+1) + self.main_jokers
        new_start = move_dir(self.start, OPPOSITE[self.direction], 1+len(board_prepend))
        return PlaceOption(new_start, self.direction, main_board, main_pattern, jokers, side_patterns)

    def __len__(self):
        return len(self.main_board)

    def __eq__(self, other):
        return self.start == other.start \
           and self.direction == other.direction \
           and self.main_pattern == other.main_pattern

    def __repr__(self):
        return "({},{})/{}/{}".format(self.start[0], self.start[1], self.direction, self.main_pattern)

class Board:
    def __init__(self):
        self.back = []
        self.front = []
        self.jokers = []
        L = [None for i in range(15)]
        for i in range(15):
            self.back.append(L[:])
            self.front.append(L[:])
            self.jokers.append([False for i in range(15)])
        for k, P in BOARD_DEF.items():
            for i,j in iter(P):
                for c, d in [(i,j), (j, i)]:
                    for a,b in iter([(c,d), (14-c,d), (14-c,14-d), (c,14-d)]):
                        self.back[a][b] = k

    def width(self):
        return 15

    def height(self):
        return 15

    def follow_dir(self, pos, direction):
        '''
        gives a string of all the letters following the direction after pos
        '''
        S = ''
        pos = move_dir(pos, direction)
        while self.has_letter(pos):
            S = S+self.front[pos[0]][pos[1]]
            pos = move_dir(pos, direction)
        return S

    def is_open(self, pos):
        i,j = pos
        if i<0 or i>14 or j<0 or j>14:
            return False
        return self.front[i][j] is None

    def has_letter(self, pos):
        i,j = pos
        if i<0 or i>14 or j<0 or j>14:
            return False
        return self.front[i][j] is not None

    def read_jokers(self, start, direction, length):
        i,j = start
        L = []
        for i in range(length):
            L.append(self.jokers[i][j])
            i,j = move_dir((i,j), direction)
        return L

    def letter_back_multiplier(self, pos):
        i,j = pos
        if self.back[i][j] == 'l2':
            return 2
        elif self.back[i][j] == 'l3':
            return 3
        return 1

    def word_back_multiplier(self, pos):
        i,j = pos
        if self.back[i][j] == 'w2':
            return 2
        elif self.back[i][j] == 'w3':
            return 3
        return 1

    def get_score(self, opt):
        if len(opt) != len(opt.side_patterns):
            print('different:', str(opt), str(opt.side_patterns))
        # main
        text = opt.combined_main()
        total = 0
        multi = 1
        for i in range(len(opt)):
            score = LETTER_POINTS[text[i]] if not opt.main_jokers[i] else 0
            if opt.main_board[i] == '_':
                pos = move_dir(opt.start, opt.direction, i)
                score *= self.letter_back_multiplier(pos)
                multi *= self.word_back_multiplier(pos)
            total += score
        total *= multi
        # sides
        for i in range(len(opt)):
            side = opt.side_patterns[i]
            if len(side) == 1:
                continue
            if opt.main_board[i] != '_':
                continue
            crossing = text[i]
            pos = move_dir(opt.start, opt.direction, i)
            score = LETTER_POINTS[crossing] if not opt.main_jokers[i] else 0
            score *= self.letter_back_multiplier(pos)
            multi = self.word_back_multiplier(pos)
            other_letters = list(side)
            other_letters.remove(crossing)
            score += sum(LETTER_POINTS[k] for k in other_letters)
            score *= multi
            total += score
        # bonus
        if len(opt.used_letters()) == 7:
            total += 50
        return total

    def make_placement(self, start, direction, main_board):
        sides = []
        k = main_board.find('_')
        main_pattern = ['_']*len(main_board)
        main_pattern[k] = '.'
        main_pattern = ''.join(main_pattern)
        merged = main_board.replace('_', '.')
        if direction == 'S':
            for it in range(len(main_board)):
                pos_it = move_dir(start, direction, it)
                LR = self.follow_dir(pos_it, 'O')[::-1], self.follow_dir(pos_it, 'E')
                sides.append(LR[0]+merged[it]+LR[1])
        elif direction == 'E':
            for it in range(len(main_board)):
                pos_it = move_dir(start, direction, it)
                LR = self.follow_dir(pos_it, 'N')[::-1], self.follow_dir(pos_it, 'S')
                sides.append(LR[0]+merged[it]+LR[1])
        jokers = self.read_jokers(start, direction, len(main_board))
        return PlaceOption(start, direction, main_board, main_pattern, jokers, sides)

    def open_positions(self):
        positions = []
        for i in range(15):
            for j in range(15):
                if self.front[i][j] is not None:
                    continue
                around = [self.follow_dir((i,j), d) for d in 'NSOE']
                if any(ar != '' for ar in around):
                    positions.append(self.make_placement((i-len(around[0]),j), 'S', around[0][::-1]+'_'+around[1]))
                    positions.append(self.make_placement((i,j-len(around[2])), 'E', around[2][::-1]+'_'+around[3]))
        if len(positions) == 0:
            # empty board
            positions.append(PlaceOption((7,7), 'S', '_', '.', [False], ['.']))
            positions.append(PlaceOption((7,7), 'E', '_', '.', [False], ['.']))
        return positions

    def increase_option_end(self, opt):
        empty_pos = move_dir(opt.start, opt.direction, len(opt))
        if not self.is_open(empty_pos):
            return None
        follow = self.follow_dir(empty_pos, opt.direction)
        sides = []
        string = '.'+follow
        for it in range(len(follow)+1):
            checked_pos = move_dir(empty_pos, opt.direction, it)
            follow_start = self.follow_dir(checked_pos, SIDES[opt.direction][0])
            follow_end = self.follow_dir(checked_pos, SIDES[opt.direction][1])
            sides.append(follow_start[::-1]+string[it]+follow_end)
        return opt.extend_end(follow, sides)

    def increase_option_start(self, opt):
        oppdir = OPPOSITE[opt.direction]
        empty_pos = move_dir(opt.start, oppdir)
        if not self.is_open(empty_pos):
            return None
        follow = self.follow_dir(empty_pos, oppdir)
        sides = []
        string = '.'+follow
        for it in range(len(follow)+1):
            checked_pos = move_dir(empty_pos, oppdir, it)
            follow_start = self.follow_dir(checked_pos, SIDES[opt.direction][0])
            follow_end = self.follow_dir(checked_pos, SIDES[opt.direction][1])
            sides.append(follow_start[::-1]+string[it]+follow_end)
        return opt.extend_start(follow[::-1], sides)

    def place_letter(self, i, j, letter, is_joker):
        if i < 0 or i >= self.width() or j < 0 or j >= self.width():
            return
        self.front[i][j] = letter
        self.jokers[i][j] = is_joker

    def remove_letter(self, i, j):
        if i < 0 or i >= self.width() or j < 0 or j >= self.width():
            return
        self.front[i][j] = None
        self.jokers[i][j] = False

    def place(self, opt):
        for k in range(len(opt)):
            if opt.main_pattern[k] != '_':
                i,j = move_dir(opt.start, opt.direction, k)
                self.place_letter(i, j, opt.main_pattern[k], opt.main_jokers[k])

    def clear_all(self):
        for i in range(15):
            for j in range(15):
                self.remove_letter(i, j)








