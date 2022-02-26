
from enum import IntEnum
from itertools import takewhile
from itertools import dropwhile

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
            
    def is_room(self):
        return self != Part.X

    def to_x_num(self):
        if (self == Part.X):
            raise ValueError('Not supported for X.')
        return 2 * self - 1

    def to_x_pos(self):
        return Pos.build(Part.X, self.to_x_num())

    def all_positions_asc(self):
        max_num = self.max_num()
        numbers = range(1, max_num + 1)
        return list(map(lambda n: Pos.build(self, n), numbers))

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
        if (enum_int >= 20):
            return enum_int % 10
        else:
            return enum_int

    def part(self):
        divide = int(int(self) / 10)
        if (divide == 0):
            return Part(1)
        else:
            return Part(divide)

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
            dist_to_room = abs(num1 - part2.to_x_num())
            return dist_from_corr + dist_to_room
        dist_from_corr = 5 - num1
        dist_to_room = abs(num2 - part1.to_x_num())
        return dist_from_corr + dist_to_room

    @classmethod
    def build(cls, part: Part, num):
        int_part = int(part)
        if (int_part == 1):
            return Pos(num)
        else:
            return Pos(int_part * 10 + num)

    @classmethod
    def to_path(start, end, part: Part, include_start = False):
        start_excluded = start - 1 if include_start else start
        if start_excluded == end:
            return []
        nums = reversed(range(end, start_excluded, -1 if start_excluded < end else 1))
        return list(map(lambda n: Pos.build(part, n), nums))
   
class Pawn:
    def __init__(self, start_pos: Pos, dest_part: Part):
        self.moves = 0
        self.start_pos = start_pos
        self.curr_pos = start_pos
        self.dest_part = dest_part
        self.total_dist = 0

    def num(self):
        return self.curr_pos.num()

    def didnt_move(self):
        return self.moves == 0
    
    def corridor_entry_pos(self): 
        start_part = self.start_pos.part()
        corr_pos = start_part.to_x_num()
        return Pos.build(Part.X, corr_pos)

    def corridor_start_passage(self):
        start_part =self.start_pos.part()
        start_num = self.start_pos.num()
        return Pos.to_path(start_num, 4, start_part)

    def move_to(self, pos: Pos):
        old_pos = self.curr_pos
        self.curr_pos = pos
        self.total_dist += old_pos.dist(pos)
        self.moves += 1

    def move_new(self, pos: Pos):
        old_pos = self.curr_pos
        new_pawn = Pawn(self.start_pos, self.dest_part)
        new_pawn.curr_pos = pos
        new_pawn.total_dist += old_pos.dist(pos)
        new_pawn.moves = self.moves + 1
        return new_pawn

    def curr_part(self):
        return self.curr_pos.part()

    def __repr__(self):
        return "Pawn at %s, dest = %s" % (self.curr_pos.name, self.dest_part)

class Board:
    def __init__(self, pawns):
        self.pawns: list[Pawn] = pawns

    def is_occupied(self, pos: Pos):
        return pos in map(lambda p: p.curr_pos, self.pawns)

    def path_free(self, part: Part, start, end, start_included):
        path = Pos.to_path(start, end, part, start_included)
        for pos in path:
            if self.is_occupied(pos):
                return False
        return True

    def is_allowed(self, pos: Pos):
        return not pos in [Pos.X3, Pos.X5, Pos.X7, Pos.X9]

    def pawn_at(self, pos: Pos):
        return next((p for p in pawns if p.curr_pos == pos), None)

    def is_finished(self, pawn: Pawn): 
        if pawn.moves == 2:
            return True
        if pawn.curr_part() != pawn.dest_part:
            return False
        
        pawn_num = pawn.num()
        others_lower = list(filter(lambda p: p.curr_part() == pawn.dest_part \
            and p.num() < pawn_num, self.pawns))
        if len(others_lower) != pawn_num - 1:
            return False

        lower_for_part = list(map(lambda p: p.curr_pos.part() == p.dest_part, others_lower))
        return all(lower_for_part)

    def is_finish_pos(self, pos: Pos, dest_part: Part):
        if pos.part() != dest_part:
            return False
        num = pos.num()
        others_lower = self.pawns.filter(lambda p: \
            p.curr_part() == dest_part and p.dest_part == dest_part and p.num() < num)
        return others_lower.size == num - 1

    def finish_pos(self, part: Part):
        all_positions = part.all_positions_asc()
        all_occupied = takewhile(lambda p: self.is_occupied(p), all_positions)
        all_occ_pawns = list(map(lambda p: self.pawn_at(p), all_occupied))
        occupied_length = len(all_occ_pawns)
                
        if occupied_length == 4:
            return []
            
        destinations = list(map(lambda p: p.dest_part, all_occ_pawns))
        if all(map(lambda p: p == part, destinations)):
            return [all_positions[occupied_length]]

        return []

    def next_positions(self, pawn: Pawn):
        if pawn.is_finished():
            return []

        finish_pos = self.finish_pos(pawn)
        if pawn.curr_part() == Part.X:
            return [finish_pos[0]] if any(finish_pos) \
                and self.can_reach(pawn.curr_pos, finish_pos[0]) else []

        if any(finish_pos) and self.can_reach(pawn.curr_pos, finish_pos[0]):
            return finish_pos[0]

        x_entry_pos = pawn.curr_part().to_x_pos()
        if self.can_reach(pawn.curr_pos, x_entry_pos):
            accessible_xs = self.accessible_in_x_from_num(x_entry_pos.num())
            allowed_xs = list(map(lambda p: self.is_allowed(p), accessible_xs))
            return allowed_xs

        return []

    def can_reach(self, start: Pos, end: Pos):
        start_part = start.part()
        end_part = end.part()
        if start_part == end_part:
            return self.path_free(start_part, start.num(), end.num(), False)

        if end_part == Path.X:
            x_entry = start_part.to_x_pos()

        ######### Continue here

        
            

    def accessible_in_x(self, curr_pos: Pos):
        num = curr_pos.num()
        part = curr_pos.part()
        
        if part == Part.X:
            return self.accessible_in_x_from_num(num)

        route_to_x = Pos.to_path(num, 4, part)
        if all(lambda p: not self.is_occupied(p), route_to_x):
            entry_x_num = part.to_x_num()
            return self.accessible_in_x_from_num(entry_x_num)

        return []      
            
    def accessible_in_x_from_num(self, x_num):
        lower = map(lambda n: Pos.build(Part.X, n), reversed(range(1, x_num)))
        higher = map(lambda n: Pos.build(Part.X, n), range(x_num, 12))
        lower_free = list(takewhile(lambda p: not self.is_occupied(p), lower))
        higher_free = list(takewhile(lambda p: not self.is_occupied(p), higher))
        return lower_free + higher_free

pawns = [
    Pawn(Pos.A1, Part.B), Pawn(Pos.A2, Part.D), Pawn(Pos.A3, Part.D), Pawn(Pos.A4, Part.B),
    Pawn(Pos.B1, Part.C), Pawn(Pos.B2, Part.B), Pawn(Pos.B3, Part.C), Pawn(Pos.B4, Part.C),
    Pawn(Pos.C1, Part.D), Pawn(Pos.C2, Part.A), Pawn(Pos.C3, Part.B), Pawn(Pos.C4, Part.A),
    Pawn(Pos.D1, Part.A), Pawn(Pos.D2, Part.C), Pawn(Pos.D3, Part.A), Pawn(Pos.D4, Part.D),
]

board = Board(pawns)

pawn = board.pawn_at(Pos.C4)
print(f"Is finished: {board.is_finished(pawn)}")

pawn.move_to(Pos.A2)
print(f"Is finished: {board.is_finished(pawn)}")

pawn.move_to(Pos.A1)
print(f"Is finished: {board.is_finished(pawn)}")

