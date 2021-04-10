

class Solver:
    def __init__(self):
        pass

    def get_options(self, board, matcher, letters, cb_step=None, cb_stop=None):
        '''
        Gives out all placement options on the board using some or all the letters
        '''
        place_options = []
        # initial options
        incomplete_opts = board.open_positions()
        marked_opts = {repr(op) for op in incomplete_opts}
        # try completions
        while len(incomplete_opts) > 0:
            if cb_step is not None:
                cb_step()
            if cb_stop is not None and cb_stop():
                print('breaking out of solve')
                break
            opt = incomplete_opts.pop(0)
            #print("explore opt:", repr(opt) + str(opt.side_patterns))
            available_letters = self._remove_used(letters, opt)
            possibilities = matcher.get_possibilities(opt)
            for poss in possibilities:
                is_joker = False
                if poss.letter not in available_letters:
                    if ' ' not in available_letters:
                        continue
                    else:
                        is_joker = True
                temp_opt = opt.complete(poss.letter, is_joker)
                if poss.complete and temp_opt not in place_options:
                    place_options.append(temp_opt)
                if len(available_letters) == 1:
                    continue
                if poss.extendable_end:
                    new_opt = board.increase_option_end(temp_opt)
                    if new_opt is not None:
                        rep = repr(new_opt)
                        if rep not in marked_opts:
                            incomplete_opts.append(new_opt)
                            marked_opts.add(rep)
                if poss.extendable_start:
                    new_opt = board.increase_option_start(temp_opt)
                    if new_opt is not None:
                        rep = repr(new_opt)
                        if rep not in marked_opts:
                            incomplete_opts.append(new_opt)
                            marked_opts.add(rep)
        return place_options

    def _remove_used(self, letters, place_option):
        avail = list(letters)
        #print(avail, list(place_option.used_letters()))
        for k in place_option.used_letters():
            if k in avail:
                avail.remove(k)
            else:
                avail.remove(' ')
        return avail


