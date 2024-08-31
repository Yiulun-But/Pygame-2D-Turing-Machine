import pygame


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('2D Turing Machine')

RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = BLACK
        self.width = width
        self.total_rows = total_rows
        
    def get_pos(self):
        return self.row, self.col
    
    def make_black(self):
        self.color = BLACK
        
    def make_red(self):
        self.color = RED
        
    def make_green(self):
        self.color = GREEN
        
    def make_start(self):
        self.color = ORANGE
        
    def reset(self):
        self.color = BLACK
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
            
    return grid

def draw_grid(win, rows, width):
    GAP = width // rows
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * GAP), (width, i * GAP))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * GAP, 0), (j * GAP, width))
    
def draw(win, grid, rows, width):
    win.fill(BLACK)
    
    for row in grid:
        for spot in row:
            spot.draw(win)
            
    draw_grid(win, rows, width)
    pygame.display.update()
    
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    
    row = y // gap
    col = x // gap
    
    return row, col

class Turmite:
    def __init__(self, row, col, grid, face, table, state, total_rows):
        self.row = row
        self.col = col
        self.grid = grid
        self.face = face
        self.table = table
        self.state = state
        self.terminate = False
        self.total_rows = total_rows
        
    def update(self):
        if self.terminate == True:
            return
        cur_color = self.grid[self.row][self.col].color
        (color, dir, state) = self.table[cur_color][self.state]
        self.grid[self.row][self.col].color = color
        self.state = state
        self.move(dir)
        
    def move(self, dir):
        face_encode = {
            "N": 0, "E": 1, "S": 2, "W": 3
        }
        dir_encode = {
            "F": 0, "R": 1, "B": 2, "L": 3
        }
        total = (dir_encode[dir] + face_encode[self.face]) % 4
        if total == 0:
            self.row -= 1
            self.face = "N"
        elif total == 1:
            self.col += 1
            self.face = "E"
        elif total == 2:
            self.row += 1
            self.face = "S"
        elif total == 3:
            self.col -= 1
            self.face = "W"
        if self.col < 0 or self.col > self.total_rows - 1 or self.row < 0 or self.row > self.total_rows - 1:
            self.terminate = True
            
def main(win, width):
    ROWS = 200
    grid = make_grid(ROWS, width)
    
    turmite_table = {
        BLACK: {
            "A": ( RED, "L", "A" ),
        },
        RED: {
            "A": ( BLACK, "R", "A" )
        }
    }
    
    turmite_table2 = {
        BLACK: {
            "A": ( GREEN, "L", "A" ),
            "B": ( GREEN, "R", "A")
        },
        GREEN: {
            "A": ( BLACK, "F", "B" ),
            "B": ( GREEN, "R", "A")
        }
    }
    
    start = None
    turmite = None
    run = True
    started = False
    while run:
        if turmite:
            turmite.update()
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]: #LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                spot = grid[row][col]
                if not start:
                    start = spot
                    start.make_start()
                
                if start:
                    start.reset()
                    start = spot
                    start.make_start()
                    
            elif pygame.mouse.get_pressed()[2]: #RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                spot = grid[row][col]
                spot.reset()
                
                if spot == start:
                    start = None
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start:
                    start.make_black()
                    turmite = Turmite(start.row,start.col,grid,"N",turmite_table2,"A", start.total_rows)
                    
                if event.key == pygame.K_c:
                    start = None
                    grid = make_grid(ROWS, width)
    pygame.quit()
main(WIN, WIDTH)