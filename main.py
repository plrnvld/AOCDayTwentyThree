from enum import IntEnum, Enum
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

class Part(Enum):
    X = 1
    A = 2
    B = 3
    C = 4
    D = 5

class AmphiPositions:
    def __init__(self, lines):
        self.startPositions = []
        for line in lines:
            self.allValues.append()



def dist(pos1: Pos, pos2: Pos):
    if pos1 == pos2:
        return 0
    else:
        return None

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

pos = Pos.X11
print(f"Engage {get_part(pos)} {get_rel_num(pos)}") 