from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Vect2D:
    x: int
    y: int

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other):
        if isinstance(other, tuple):
            # Hash of a given Vect2D is equal to that of the tuple of
            # its coordinates, therefore we MUST implement equality too
            if len(other) != 2:
                return False
            return tuple(self) == other
        if isinstance(other, Vect2D):
            return self.x == other.x and self.y == other.y
        return False

    def __neg__(self):
        return self * -1

    def __mul__(self, other: int):
        return type(self)(self.x * other, self.y * other)

    def __add__(self, other: 'Vect2D'):
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vect2D'):
        return self + (-other)

    def __floordiv__(self, other: int):
        if not isinstance(other, int):
            return NotImplemented
        if self.x % other or self.y % other:
            raise ValueError("Can only divide a vector integrally")
        return type(self)(self.x // other, self.y // other)

    def __invert__(self):
        return type(self)(self.y, self.x)

    def __complex__(self):
        return self.x + self.y * 1j

    def __abs__(self):
        return abs(self.x) + abs(self.y)

    def up(self):
        return self + UP

    def down(self):
        return self + DOWN

    def left(self):
        return self + LEFT

    def right(self):
        return self + RIGHT


UP, DOWN, LEFT, RIGHT = Vect2D(0, 1), Vect2D(0, -1), Vect2D(-1, 0), Vect2D(1, 0)

class Direction(Enum):
    Up = UP
    Down = DOWN
    Left = LEFT
    Right = RIGHT


class Instruction(Enum):
    Left = 'L'
    Right = 'R'
    Move = 'M'


class Walker2D:

    def __init__(self, x: int, y: int, direction: Direction):
        self.pos = Vect2D(x, y)
        self.direction = direction

    def rot_left(self):
        new_dirs = {
            Direction.Up: Direction.Left,
            Direction.Left: Direction.Down,
            Direction.Down: Direction.Right,
            Direction.Right: Direction.Up,
        }
        self.direction = new_dirs[self.direction]

    def rot_right(self):
        new_dirs = {
            Direction.Up: Direction.Right,
            Direction.Left: Direction.Up,
            Direction.Down: Direction.Left,
            Direction.Right: Direction.Down,
        }
        self.direction = new_dirs[self.direction]

    def move(self):
        self.pos += self.direction.value

    def do(self, instruction: Instruction):
        if instruction == Instruction.Left:
            self.rot_left()
        elif instruction == Instruction.Right:
            self.rot_right()
        elif instruction == Instruction.Move:
            self.move()