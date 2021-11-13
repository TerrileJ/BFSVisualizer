import pygame

# width of screen
WIDTH = 600
NODE_WIDTH = 15

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (37, 235, 89)
RED = (229, 41, 41)

class Node:
    def __init__(self, x, y, width):
        self.color = WHITE
        self.x = x
        self.y = y
        self.width = width

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, ( self.x, self.y, self.width, self.width) )

# creates 2-d list of Nodes
def make_grid(widthNode):
    numRows = WIDTH // widthNode

    grid = []
    for i in range(numRows):
        rows = []
        for j in range(numRows):
            rows.append(Node(j * widthNode, i * widthNode, widthNode))
        grid.append(rows)

    return grid

# Draws grid lines
def draw_lines(screen, grid, width):
    for i in range(len(grid)):
        pygame.draw.line(screen, BLACK, (0, width * i), (WIDTH, width * i ), 1) # draws horizontal lines
        for j in range(len(grid[i])):
            pygame.draw.line(screen, BLACK, (width * j, 0), (width * j, WIDTH), 1)  # draw vertical lines

# Draws and updates the grid at every frame
def draw_grid(screen, grid):
    screen.fill(WHITE)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].draw(screen)
    draw_lines(screen, grid, NODE_WIDTH)
    pygame.display.update()

# assigns start and end nodes
def designate_nodes(grid, counter):
    pos = pygame.mouse.get_pos()
    row = pos[1] // NODE_WIDTH
    col = pos[0] // NODE_WIDTH
    node = grid[row][col]

    # checks if square is available
    if node.get_color() != WHITE:
        return False

    # sets color according to mouse click, first mouse click = start node = green, etc
    color = BLACK
    if counter == 1:
        color = GREEN
    elif counter == 2:
        color = RED

    grid[row][col].set_color(color)

    return True

# runs entire game and visualization
def main(screen):
    startNode = False
    endNode = False
    grid = make_grid(NODE_WIDTH)
    run = True

    while run:
        draw = True
        draw_grid(screen, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row = pos[1] // NODE_WIDTH
                col = pos[0] // NODE_WIDTH
                node = grid[row][col]
                if not(startNode):
                    node.set_color(GREEN)
                    startNode = True
                elif not(endNode):
                    if node.get_color() != GREEN:
                        node.set_color(RED)
                        endNode = True
                else:
                    if node.get_color() != GREEN and node.get_color() != RED:
                        node.set_color(BLACK)


    pygame.quit()

# setup pygame and screen
pygame.init()
pygame.display.set_caption("Breadth First Search Visualizer")
screen = pygame.display.set_mode((WIDTH, WIDTH))

main(screen)