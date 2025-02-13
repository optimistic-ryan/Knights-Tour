import unittest
import random
import pygame
import sys
import getopt

PATTERN_LOOKBACK = 20

class Square:
    def __init__(self, x, y):
        self.connections = []
        self.x = x
        self.y = y
    
    def is_connected_to(self, other):
        return any(other in connection.squares for connection in self.connections)

def connect_squares(sq1, sq2):
    for connection in sq1.connections:
        if sq2 in connection.squares:
            raise Exception("Connection already exists")
    
    for connection in sq2.connections:
        if sq1 in connection.squares:
            raise Exception("Connection already exists")
    
    connection = Connection(sq1, sq2)
    sq1.connections.append(connection)
    sq2.connections.append(connection)
    return connection

class Connection:
    def __init__(self, sq1, sq2):
        self.squares = (sq1, sq2)
        self.time = 0
        self.state = 0
        self.prev_state = 0
        self.output = {0: random.randint(0, 1)}

    def has_changed(self):
        return self.output[self.time] != self.output[self.time - 1] or self.state != self.prev_state

    def neighbor_sum(self, t):
        return sum(conn.output[t] for sq in self.squares for conn in sq.connections)

    def update(self):
        self.time += 1
        self.prev_state = self.state
        self.state = self.prev_state + 4 - self.neighbor_sum(self.time - 1)

        if self.state > 3:
            self.output[self.time] = 1
        elif self.state < 0:
            self.output[self.time] = 0
        else:
            self.output[self.time] = self.output[self.time - 1]

        if len(self.output) > PATTERN_LOOKBACK:
            del self.output[self.time - PATTERN_LOOKBACK]

class Board:
    def __init__(self, size):
        self.size = size
        self.squares = [[Square(x, y) for y in range(size)] for x in range(size)]
        self.connections = []
        self.initialize_knight_moves()

    def initialize_knight_moves(self):
        moves = [(2, 1), (-2, 1), (1, 2), (-1, 2)]
        for move in moves:
            self.add_knight_move(move)

    def add_knight_move(self, move):
        dx, dy = move
        for x in range(self.size):
            for y in range(self.size):
                if 0 <= x + dx < self.size and 0 <= y + dy < self.size:
                    self.connect_squares((x, y), (x + dx, y + dy))

    def connect_squares(self, pos1, pos2):
        sq1 = self.squares[pos1[0]][pos1[1]]
        sq2 = self.squares[pos2[0]][pos2[1]]
        self.connections.append(connect_squares(sq1, sq2))

    def update(self):
        for connection in self.connections:
            connection.update()

    def is_stable(self):
        return all(not connection.has_changed() for connection in self.connections)

    def reset(self):
        for connection in self.connections:
            connection.__init__(*connection.squares)

pygame.init()

size = 6
optlist, args = getopt.getopt(sys.argv[1:], 's:u', ['size='])
for opt, arg in optlist:
    if opt in ('-s', '--size'):
        size = int(arg)

tour_board = Board(size)
screen = pygame.display.set_mode([size * 50 + 1, size * 50 + 1])
pygame.display.set_caption("Knight's Tour Neural Network")

running = True
update_board = True
frames = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                update_board = False
                tour_board.update()
            elif event.key == pygame.K_RETURN:
                update_board = True
                frames = 0
                tour_board.reset()

    if update_board:
        frames += 1
        tour_board.update()
        if tour_board.is_stable():
            update_board = False
            print(f"Stable after {frames} updates")

    screen.fill((255, 255, 255))
    for x in range(size + 1):
        pygame.draw.line(screen, (0, 255, 255), (x * 50, 0), (x * 50, size * 50))
        pygame.draw.line(screen, (0, 255, 255), (0, x * 50), (size * 50, x * 50))

    for connection in tour_board.connections:
        if connection.output[connection.time] == 1:
            pygame.draw.line(screen, (0, 0, 255),
                             (connection.squares[0].x * 50 + 25, (size - 1 - connection.squares[0].y) * 50 + 25),
                             (connection.squares[1].x * 50 + 25, (size - 1 - connection.squares[1].y) * 50 + 25))

    for row in tour_board.squares:
        for sq in row:
            pygame.draw.circle(screen, (0, 0, 255), (sq.x * 50 + 25, (size - 1 - sq.y) * 50 + 25), 5)

    pygame.display.update()
