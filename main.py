from enum import IntEnum
from itertools import takewhile
import datetime


class Part(IntEnum):
    X = 1
    A = 2
    B = 3
    C = 4
    D = 5

    def max_num(self):
        if self == Part.X: 
            return 11
        else:
            return 4
            
    def to_x_num(self):
        if (self == Part.X):
            raise ValueError('Not supported for X.')
        return 2 * self - 1

    def to_x_pos(self):
        return Pos.build(Part.X, self.to_x_num())

    def all_positions_asc(self):
        if self == Part.A:
            return [Pos.A1, Pos.A2, Pos.A3, Pos.A4]
        if self == Part.B:
            return [Pos.B1, Pos.B2, Pos.B3, Pos.B4]
        if self == Part.C:
            return [Pos.C1, Pos.C2, Pos.C3, Pos.C4]
        if self == Part.D:
            return [Pos.D1, Pos.D2, Pos.D3, Pos.D4]

        return [Pos.X1, Pos.X2, Pos.X3, Pos.X4, Pos.X5, Pos.X6, Pos.X7, Pos.X8, Pos.X9, Pos.X10, Pos.X11]

    def to_path(self, start, end, include_start):
        start_excluded = start - 1 if include_start else start
        if start_excluded == end:
            return []
        nums = reversed(range(end, start_excluded, -1 if start_excluded < end else 1))
        return list(map(lambda n: Pos.build(self, n), nums))

    def multiplier(self):
        return [0, 1, 10, 100, 1000][self - 1]
   
    def __repr__(self):
        return self.name

class Pos(IntEnum):
    X1 = 1
    X2 = 2
    X3 = 3 # Does this position even matter?
    X4 = 4
    X5 = 5 # Does this position even matter?
    X6 = 6
    X7 = 7 # Does this position even matter? 
    X8 = 8
    X9 = 9 # Does this position even matter?
    X10 = 10
    X11 = 11
    A1 = 21
    A2 = 22
    A3 = 23
    A4 = 24
    B1 = 31
    B2 = 32
    B3 = 33
    B4 = 34
    C1 = 41
    C2 = 42
    C3 = 43
    C4 = 44
    D1 = 51
    D2 = 52
    D3 = 53
    D4 = 54

    def __repr__(self):
        return self.name

    def num(self):
        enum_int = int(self)
        if enum_int >= 20:
            return enum_int % 10
        else:
            return enum_int

    def part(self):
        divide = int(int(self) / 10)
        if divide == 0:
            return Part(1)
        else:
            return Part(divide)

    def dist(self, pos2):
        part1 = self.part()
        part2 = pos2.part()
        num1 = self.num()
        num2 = pos2.num()

        if part1 == part2:
            return abs(num1 - num2)    
        if part1 != Part.X and part2 != Part.X:
            corridor = 2 * abs(part1 - part2)
            dist_from_corr_1 = 5 - num1
            dist_from_corr_2 = 5 - num2
            return corridor + dist_from_corr_1 + dist_from_corr_2
        if part1 == Part.X:
            dist_from_corr = 5 - num2
            dist_to_room = abs(num1 - part2.to_x_num())
            return dist_from_corr + dist_to_room
        dist_from_corr = 5 - num1
        dist_to_room = abs(num2 - part1.to_x_num())
        return dist_from_corr + dist_to_room

    @classmethod
    def build(cls, part: Part, num):
        int_part = int(part)
        if int_part == 1:
            return Pos(num)
        else:
            return Pos(int_part * 10 + num)
    
class Pawn:
    def __init__(self, start_pos: Pos, dest_part: Part):
        self.start_pos = start_pos
        self.curr_pos = start_pos
        self.dest_part = dest_part
        self.total_dist = 0
        self.is_finished_cached = False

    def copy_pawn(self):
        new_pawn = Pawn(self.start_pos, self.dest_part)
        new_pawn.curr_pos = self.curr_pos
        new_pawn.total_dist = self.total_dist
        new_pawn.is_finished_cached = self.is_finished_cached
        return new_pawn

    def num(self):
        return self.curr_pos.num()

    def didnt_move(self):
        return self.moves == 0
    
    def corridor_entry_pos(self): 
        start_part = self.start_pos.part()
        corr_pos = start_part.to_x_num()
        return Pos.build(Part.X, corr_pos)

    def move_to(self, pos: Pos):
        old_pos = self.curr_pos
        self.curr_pos = pos
        self.total_dist += old_pos.dist(pos)

    # def move_new(self, pos: Pos):
     #   old_pos = self.curr_pos
      #  new_pawn = Pawn(self.start_pos, self.dest_part)
      #  new_pawn.curr_pos = pos
      #  new_pawn.total_dist += old_pos.dist(pos)
      #  return new_pawn

    def curr_part(self):
        return self.curr_pos.part()

    def __repr__(self):
        return "Pawn at %s, dest = %s" % (self.curr_pos.name, self.dest_part)
   
class Board:
    def __init__(self, pawns):
        self.pawns: list[Pawn] = pawns
        self.path_dict = {}
        self.occupied_dict = {}
        self.pawn_dict = {}
        self.finish_pos_dict = {}
        self.moves = []
        self.occupied = [[False] * 11, [False] * 4, [False] * 4, [False] * 4, [False] * 4]
        for pawn in self.pawns:
            part = pawn.curr_part()
            num = pawn.num()
            self.occupied[part - 1][num - 1] = True

    def is_occupied(self, pos: Pos):
        return self.is_occupied_impl2(pos)

    def is_occupied_impl1(self, pos: Pos):
        occupied_value = self.occupied_dict.get(pos)
        if occupied_value != None:
            return occupied_value
    
        is_occupied = pos in map(lambda p: p.curr_pos, self.pawns)
        self.occupied_dict[pos] = is_occupied
        return is_occupied

    def is_occupied_impl2(self, pos: Pos):
        part = pos.part()
        num = pos.num()
        return self.occupied[part - 1][num - 1]

    def path_free(self, part: Part, start: int, end: int, start_included):
        real_start = start if start_included else start + 1
        dict_value = self.get_from_dict(part, real_start, end)
        
        if dict_value != None:
            return dict_value

        path = part.to_path(start, end, start_included)
        for pos in path:
            if self.is_occupied(pos):
                self.store_in_dict(part, real_start, end, False)
                return False
                
        self.store_in_dict(part, real_start, end, False)
        return True

    def store_in_dict(self, part: Part, real_start: int, end: int, result: bool):
        if real_start < end:
            self.path_dict[(part, real_start, end)] = result
        else:
            self.path_dict[(part, end, real_start)] = result

    def get_from_dict(self, part: Part, real_start: int, end: int):
        if real_start < end:
            return self.path_dict.get((part, real_start, end))
        else:
            return self.path_dict.get((part, end, real_start))
            
    def is_allowed(self, pos: Pos):
        return not pos in [Pos.X3, Pos.X5, Pos.X7, Pos.X9]

    def pawn_at(self, pos: Pos):
        if pos in self.pawn_dict:        
            return self.pawn_dict[pos]
        
        pawn = next((p for p in self.pawns if p.curr_pos == pos), None)
        self.pawn_dict[pos] = pawn
        return pawn

    def is_finished(self, pawn: Pawn):
        if pawn.is_finished_cached:
            return True

        curr_pos = pawn.curr_pos
        curr_part = curr_pos.part()
        if curr_pos.part() == pawn.dest_part:
            nums_lower = range(1, pawn.num())
        
            nums_lower = range(1, curr_pos.num())
            for num in nums_lower:
                pawn_lower = self.pawn_at(Pos.build(curr_part, num))
                if pawn_lower == None or pawn_lower.dest_part != curr_part:
                    return False
            
            pawn.is_finished_cached = True
            return True
        
        return False

    def finish_pos(self, part: Part):
        if part in self.finish_pos_dict:
            return self.finish_pos_dict[part]

        all_positions_desc = list(reversed(part.all_positions_asc()))
        all_pawns = list(map(lambda p: self.pawn_at(p), all_positions_desc))
        
        all_open = list(takewhile(lambda p: p == None, all_pawns))
        all_open_len = len(all_open)
        
        if all_open_len > 0 and (all_open_len == 4 or self.is_finished(all_pawns[all_open_len])):
            finish = all_positions_desc[all_open_len - 1]
            self.finish_pos_dict[part] = finish
            return finish
            
        self.finish_pos_dict[part] = None
        return None

    def next_positions(self, pawn: Pawn):
        if self.is_finished(pawn):
            return []

        finish_pos = self.finish_pos(pawn.dest_part)
        if finish_pos != None and self.can_reach(pawn.curr_pos, finish_pos):
            return [finish_pos]
        else: 
            if pawn.curr_part() == Part.X:
                return [] # Pawn is already at X and cannot finish

        x_entry_pos = pawn.curr_part().to_x_pos()
        if self.can_reach(pawn.curr_pos, x_entry_pos):
            accessible_xs = self.accessible_in_x_from_num(x_entry_pos.num())
            allowed_xs = list(filter(lambda p: self.is_allowed(p), accessible_xs))
            return allowed_xs
        return []

    def can_reach(self, start: Pos, end: Pos):
        start_part = start.part()
        end_part = end.part()
        if start_part == end_part:
            return self.path_free(start_part, start.num(), end.num(), False)

        if end_part == Part.X:
            return self.path_free(start_part, start.num(), 4, False) and \
                self.path_free(Part.X, start_part.to_x_num(), end.num(), False)

        if start_part == Part.X:
            return self.path_free(Part.X, start.num(), end_part.to_x_num(), False) and \
                self.path_free(end_part, 4, end.num(), True)

        return self.path_free(start_part, start.num(), 4, False) and \
            self.path_free(Part.X, start_part.to_x_num(), end_part.to_x_num(), False) and \
            self.path_free(end_part, 4, end.num(), True)

    def accessible_in_x(self, curr_pos: Pos):
        num = curr_pos.num()
        part = curr_pos.part()        
        if part == Part.X:
            return self.accessible_in_x_from_num(num)
        route_to_x = part.to_path(num, 4, False)
        if all(lambda p: not self.is_occupied(p), route_to_x):
            entry_x_num = part.to_x_num()
            return self.accessible_in_x_from_num(entry_x_num)
        return []      
            
    def accessible_in_x_from_num(self, x_num):
        lower = Part.X.to_path(x_num, 1, False)
        higher = Part.X.to_path(x_num, 11, False)
        lower_free = list(reversed(list(takewhile(lambda p: not self.is_occupied(p), lower))))
        higher_free = list(takewhile(lambda p: not self.is_occupied(p), higher))
        return lower_free + higher_free

    def move_new_board(self, start: Pos, end: Pos):
        new_pawns = list(map(lambda p: p.copy_pawn(), self.pawns))
        pawn = next(filter(lambda p: p.curr_pos == start, new_pawns), None)
        pawn.move_to(end)
        new_board = Board(new_pawns)
        existing_moves = self.moves.copy()
        existing_moves.append(f"({pawn}) moved {start.name} ➡ {end.name}")
        new_moves = existing_moves
        new_board.moves = new_moves
        return new_board

    # Good that this does not use pawn_at, because that uses cached results
    # and can be outdated after a move
    def pawn_char(self, pos: Pos):
        result = next(filter(lambda p: p.curr_pos == pos, self.pawns), None)
        return " " if result == None else result.dest_part.name

    def print_board(self):
        print()
        print("#############")
        xs_chars = ''.join(list(map(lambda p: self.pawn_char(p), Part.X.all_positions_asc())))
        print("#" + xs_chars + "#")
        print("###" + self.pawn_char(Pos.A4) + "#" + self.pawn_char(Pos.B4) + "#" \
              + self.pawn_char(Pos.C4) + "#" + self.pawn_char(Pos.D4) + "###")
        print("  #" + self.pawn_char(Pos.A3) + "#" + self.pawn_char(Pos.B3) + "#" \
              + self.pawn_char(Pos.C3) + "#" + self.pawn_char(Pos.D3) + "#  ")
        print("  #" + self.pawn_char(Pos.A2) + "#" + self.pawn_char(Pos.B2) + "#" \
              + self.pawn_char(Pos.C2) + "#" + self.pawn_char(Pos.D2) + "#  ")
        print("  #" + self.pawn_char(Pos.A1) + "#" + self.pawn_char(Pos.B1) + "#" \
              + self.pawn_char(Pos.C1) + "#" + self.pawn_char(Pos.D1) + "#  ")
        print("  #########  ")
        print()

    def all_moves(self):
        moves = []
        for pawn in self.pawns:
            next_for_pawn = self.next_positions(pawn)
            moves_for_pawn = list(map(lambda p: Move(pawn.curr_pos, p), next_for_pawn))
            # if len(moves_for_pawn) > 0:
                # print(f"{pawn} has moves: {moves}")
            moves.extend(moves_for_pawn)

        return moves

    def end_reached(self):
        for part in [Part.A, Part.B, Part.C, Part.D]:
            for pos in part.all_positions_asc():
                pawn_on_pos = self.pawn_at(pos)
                if pawn_on_pos == None or pawn_on_pos.dest_part != part:
                    return False
                    
        return True

    def calc_score(self):
        sum = 0
        for pawn in self.pawns:
            sum += pawn.total_dist * pawn.dest_part.multiplier()

        return sum

    def __repr__(self):
        return f"Board with {len(self.moves)} moves"
                    
class Move:
    def __init__(self, start: Pos, end: Pos):
        self.start = start
        self.end = end

    def apply_move(self, board: Board):
        return board.move_new_board(self.start, self.end)

    def __repr__(self):
        return "Move %s ➡ %s" % (self.start.name, self.end.name)

pawns_init_part_2 = [
    Pawn(Pos.A4, Part.B), Pawn(Pos.B4, Part.C), Pawn(Pos.C4, Part.A), Pawn(Pos.D4, Part.D),
    Pawn(Pos.A3, Part.D), Pawn(Pos.B3, Part.C), Pawn(Pos.C3, Part.B), Pawn(Pos.D3, Part.A), 
    Pawn(Pos.A2, Part.D), Pawn(Pos.B2, Part.B), Pawn(Pos.C2, Part.A), Pawn(Pos.D2, Part.C), 
    Pawn(Pos.A1, Part.B), Pawn(Pos.B1, Part.C), Pawn(Pos.C1, Part.D), Pawn(Pos.D1, Part.A)]

pawns_init_part_1 = [
    Pawn(Pos.A4, Part.B), Pawn(Pos.B4, Part.C), Pawn(Pos.C4, Part.A), Pawn(Pos.D4, Part.D),
    Pawn(Pos.A3, Part.B), Pawn(Pos.B3, Part.C), Pawn(Pos.C3, Part.D), Pawn(Pos.D3, Part.A),
    Pawn(Pos.A2, Part.A), Pawn(Pos.B2, Part.B), Pawn(Pos.C2, Part.C), Pawn(Pos.D2, Part.D), 
    Pawn(Pos.A1, Part.A), Pawn(Pos.B1, Part.B), Pawn(Pos.C1, Part.C), Pawn(Pos.D1, Part.D)]

pawns_init_experiment = [
    Pawn(Pos.A4, Part.B), Pawn(Pos.B4, Part.A), Pawn(Pos.C4, Part.C), Pawn(Pos.D4, Part.D),
    Pawn(Pos.A3, Part.A), Pawn(Pos.B3, Part.B), Pawn(Pos.C3, Part.C), Pawn(Pos.D3, Part.D),
    Pawn(Pos.A2, Part.A), Pawn(Pos.B2, Part.B), Pawn(Pos.C2, Part.C), Pawn(Pos.D2, Part.D), 
    Pawn(Pos.A1, Part.A), Pawn(Pos.B1, Part.B), Pawn(Pos.C1, Part.C), Pawn(Pos.D1, Part.D)]

lowest_score = 1000000
cycle = 0
move_to_test = 1
winning_moves = []

def check_moves(board_start: Board):
    global cycle
    global move_to_test
    global lowest_score
    global winning_moves

    print("Checking boards started")
    
    boards_to_check = [board_start]

    while len(boards_to_check) > 0:
        # print(f"Boards to check: {boards_to_check}")
        curr_board = boards_to_check.pop(0)
    
        moves = curr_board.all_moves()
        # print(moves)

        if len(moves) > 0:
            boards_to_insert = []
            for move in moves:
                new_board = move.apply_move(curr_board)
                boards_to_insert.append(new_board)             
            for b in boards_to_insert:
                boards_to_check.insert(0, b)

            cycle += 1
            if cycle % 20000 == 0:
                time_format = "%H:%M:%S"
                print(f"> cycle {cycle}, time: {datetime.datetime.now().strftime(time_format)}, boards active: {len(boards_to_check)}")
        else:
            if curr_board.end_reached():
                score = curr_board.calc_score()
                # print(f"---> End reached: score {score}")
                if score < lowest_score:
                    lowest_score = score
                    winning_moves = curr_board.moves.copy()
                    print(f"Lowest score is now {lowest_score}")
            # else:
            #    print("Dead end")

check_moves(Board(pawns_init_part_1))

print("-- All options checked --")
print(f"Lowest score = {lowest_score}")

for move in winning_moves:
    print(">  " + move)


# 166 too low
# 42752 too low
# 42732 too low (😄)
# In total 2.280.000 cycles