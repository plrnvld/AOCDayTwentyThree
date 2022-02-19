from enum import IntEnum
from itertools import takewhile

class Pos(IntEnum):
    X1 = 1
    X2 = 2
    X3 = 3
    X4 = 4
    X5 = 5
    X6 = 6
    X7 = 7
    X8 = 8
    X9 = 9
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

class Part(IntEnum):
    X = 1
    A = 2
    B = 3
    C = 4
    D = 5

class Pawn:
    def __init__(self, start_pos: Pos, dest_part: Part):
        self.moves = 0
        self.start_pos = start_pos
        self.curr_pos = start_pos
        self.dest_part = dest_part

    def didnt_move(self):
        return self.moves == 0

    def is_finished(self): 
        return self.moves == 2

    def corridor_entry_pos(self): 
        start_part = get_part(self.start_pos)
        corr_pos = 2* start_part - 1
        return get_pos(Part.X, corr_pos)

    def corridor_start_blockers(self):
        start_part = get_part(self.start_pos)
        start_num = get_rel_num(self.start_pos)
        return [get_pos(start_part, n) for n in reversed(range(4, start_num, -1))]

class Board:
    def __init__(self, pawns):
        self.pawns: list[Pawn] = pawns
        self.occupied = map(lambda p: p.curr_pos, pawns)

    def is_occupied(self, pos: Pos): 
        return pos in self.occupied

    def dest_open(self, pawn: Pawn):
        if self.is_occupied(get_pos(pawn.dest_part, 4)):
            return False
        return not any(lambda p: get_part(p.curr_pos) == pawn.dest_part and p.dest_part != pawn.dest_part)
        
def is_x_pos(pos: Pos):
    return enum_is_in_range(pos, 1, 11)

def is_a_pos(pos: Pos):
    return enum_is_in_range(pos, 21, 24)

def is_b_pos(pos: Pos):
    return enum_is_in_range(pos, 31, 34)

def is_c_pos(pos: Pos):
    return enum_is_in_range(pos, 41, 44)

def is_d_pos(pos: Pos):
    return enum_is_in_range(pos, 51, 54)

def enum_is_in_range(pos: Pos, min_range, max_range):
    enum_int = int(pos)
    return enum_int >= min_range and enum_int <= max_range

def get_rel_num(pos: Pos):
    enum_int = int(pos)
    if (enum_int >= 20):
        return enum_int % 10
    else:
        return enum_int

def get_part(pos: Pos):
    divide = int(int(pos) / 10)
    if (divide == 0):
        return Pos(1)
    else:
        return Pos(divide)

def get_pos(part: Part, rel_num):
    int_part = int(part)
    if (int_part == 1):
        return Pos(rel_num)
    else:
        return Pos(int_part * 10 + rel_num)

def dist(pos1: Pos, pos2: Pos):
    part1 = get_part(pos1)
    part2 = get_part(pos2)
    num1 = get_rel_num(pos1)
    num2 = get_rel_num(pos2)

    if part1 == part2:
        return abs(num1 - num2)    
    if part1 != Part.X and part2 != Part.X:
        corridor = 2 * abs(part1 - part2)
        dist_from_corr_1 = 5 - num1
        dist_from_corr_2 = 5 - num2
        return corridor + dist_from_corr_1 + dist_from_corr_2
    if part1 == Part.X:
        dist_from_corr = 5 - num2
        dist_to_room = abs(num1 - corridor_entry(part2))
        return dist_from_corr + dist_to_room
    dist_from_corr = 5 - num1
    dist_to_room = abs(num2 - corridor_entry(part1))
    return dist_from_corr + dist_to_room

def corridor_entry(part: Part):
    return 1 + int(part)

pawns = [
    Pawn(Pos.A1, Part.B), Pawn(Pos.A2, Part.D), Pawn(Pos.A3, Part.D), Pawn(Pos.A4, Part.D),
    Pawn(Pos.B1, Part.C), Pawn(Pos.B2, Part.B), Pawn(Pos.B3, Part.C), Pawn(Pos.B4, Part.C),
    Pawn(Pos.C1, Part.D), Pawn(Pos.C2, Part.A), Pawn(Pos.C3, Part.B), Pawn(Pos.C4, Part.A),
    Pawn(Pos.D1, Part.A), Pawn(Pos.D2, Part.C), Pawn(Pos.D3, Part.A), Pawn(Pos.D4, Part.D),
]

board = Board(pawns)

pos1 = Pos.C3
pos2 = Pos.B4
print(f"Dist = {dist(pos1, pos2)}")
print(f"Occupied {pos1.name}: {board.is_occupied(pos1)}")

pawn_test = Pawn(pos1, Part.B)
print(f"Corr pos {pos1.name}: {pawn_test.corridor_entry_pos().name}")

print(f"Start blockers: {pos1.name}: {list(map(lambda p: p.name, pawn_test.corridor_start_blockers()))}")
