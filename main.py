import pygame

# width of screen
WIDTH = 600
NODE_WIDTH = 15

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)

class Node:
    def __init__(self, x, y, width):
        self.color = WHITE
        self.x = x
        self.y = y
        self.width = width

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

def main(screen):
    grid = make_grid(NODE_WIDTH)
    run = True

    while run:
        screen.fill(WHITE)
        draw_lines(screen, grid, NODE_WIDTH)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

# setup pygame and screen
pygame.init()
pygame.display.set_caption("Breadth First Search Visualizer")
screen = pygame.display.set_mode((WIDTH, WIDTH))

# set up grid
main(screen)