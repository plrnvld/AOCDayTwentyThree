from enum import IntEnum

class Part(IntEnum):
    X = 1
    A = 2
    B = 3
    C = 4
    D = 5

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

    def num(self):
        enum_int = int(self)
        if (enum_int >= 20):
            return enum_int % 10
        else:
            return enum_int

    def part(self):
        divide = int(int(self) / 10)
        if (divide == 0):
            return Pos(1)
        else:
            return Pos(divide)

    def has_part(self, part):
        return self.part() == part

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
            dist_to_room = abs(num1 - corridor_entry(part2))
            return dist_from_corr + dist_to_room
        dist_from_corr = 5 - num1
        dist_to_room = abs(num2 - corridor_entry(part1))
        return dist_from_corr + dist_to_room

    @classmethod
    def build(cls, part: Part, num):
        int_part = int(part)
        if (int_part == 1):
            return Pos(num)
        else:
            return Pos(int_part * 10 + num)
   
class Pawn:
    def __init__(self, start_pos: Pos, dest_part: Part):
        self.moves = 0
        self.start_pos = start_pos
        self.curr_pos = start_pos
        self.dest_part = dest_part
        self.total_dist = 0

    def didnt_move(self):
        return self.moves == 0
    
    def corridor_entry_pos(self): 
        start_part = self.start_pos.part()
        corr_pos = 2* start_part - 1
        return Pos.build(Part.X, corr_pos)

    def corridor_start_passage(self):
        start_part =self.start_pos.part()
        start_num = self.start_pos.num()
        return [Pos.build(start_part, n) for n in reversed(range(4, start_num, -1))]

    def move_to(self, pos: Pos):
        old_pos = self.curr_pos
        self.curr_pos = pos
        self.total_dist += old_pos.dist(pos)
        self.moves += 1

    def curr_part(self):
        return self.curr_pos.part()   

class Board:
    def __init__(self, pawns):
        self.pawns: list[Pawn] = pawns
        self.occupied = map(lambda p: p.curr_pos, pawns)

    def is_occupied(self, pos: Pos):
        return pos in self.occupied

    def dest_open(self, pawn: Pawn):
        if self.is_occupied(Pos.build(pawn.dest_part, 4)):
            return False
        return not any(lambda p: p.curr_part() == pawn.dest_part and p.dest_part != pawn.dest_part)

    def start_open(self, pawn: Pawn):
        if self.dest_open(pawn):
            return True
        return all(map(lambda p: not self.is_occupied(p), pawn.corridor_start.passage()))

    def is_finished(self, pawn: Pawn): 
        if pawn.moves == 2:
            return True
        if pawn.curr_part() != pawn.dest_part:
            return False
        
        pawn_num = pawn.num()
        others_lower = self.pawns.filter(lambda p: p.curr_part() == pawn.dest_part \
            and p.num() < pawn_num)
        return others_lower.size == pawn_num - 1 and all(lambda p: p.part() == p.dest_part, others_lower)

    def next_positions(self, pawn: Pawn):
        if pawn.is_finished():
            return []
        
        ############### Continue her

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
print(f"Dist = {pos1.dist(pos2)}")
print(f"Occupied {pos1.name}: {board.is_occupied(pos1)}")

pawn_test = Pawn(pos1, Part.B)
print(f"Corr pos {pos1.name}: {pawn_test.corridor_entry_pos().name}")

print(f"Start passage {pos1.name}: {list(map(lambda p: p.name, pawn_test.corridor_start_passage()))}")
