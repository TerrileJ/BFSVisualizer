import pygame
from queue import Queue

# width of screen
WIDTH = 600
NODE_WIDTH = 15

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (37, 235, 89)
RED = (229, 41, 41)
TURQUOISE = (64,224,208)
VIOLET = (148,0,211)
PINK = (255,192,203)
GOLD = (255,215,0)

class Node:
    def __init__(self, x, y, width):
        self.color = WHITE
        self.x = x
        self.y = y
        self.width = width
        self.prev = None
        self.neighbors = None

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def get_position(self):
        return (self.x, self.y)

    def set_prev(self, node):
        self.prev = node

    def get_prev(self):
        return self.prev

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, ( self.x, self.y, self.width, self.width) )

    def update_neighbors(self):
        self.neighbors = []

        # find left neighbor if one exists
        if(self.x >= NODE_WIDTH):
            left = ( (self.x - NODE_WIDTH) , self.y)
            self.neighbors.append(left)

        # find right neighbor if one exists
        if(self.x < WIDTH - NODE_WIDTH):
            right = ( (self.x + NODE_WIDTH) , self.y )
            self.neighbors.append(right)

        # find top neighbor if one exists
        if(self.y >= NODE_WIDTH):
            top = ( self.x, (self.y - NODE_WIDTH))
            self.neighbors.append(top)

        # find bottom neighbor if one exists
        if (self.y < (WIDTH - NODE_WIDTH)):
            bottom = (self.x , (self.y + NODE_WIDTH))
            self.neighbors.append(bottom)

    def get_neighbors(self):
        return self.neighbors

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

def reset(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j].set_color(WHITE)

# Given a (x,y) coordinate, return the node at that position
def get_node(grid, pos):
    row = pos[1] // NODE_WIDTH
    col = pos[0] // NODE_WIDTH

    return grid[row][col]

# Runs BFS visualization
def BFS(startNode, endNode, grid, screen):
    queue = Queue()
    queue.put(startNode)
    path = {startNode: startNode}
    while not queue.empty():
        node = queue.get()

        node.set_color(TURQUOISE)

        neighbors = node.get_neighbors()
        for neighbors_pos in neighbors:
            neighbor = get_node(grid, neighbors_pos)

            if(neighbor == endNode):
                path[neighbor] = node
                curr = node
                while curr != startNode:
                    draw_grid(screen, grid)
                    curr.set_color(GOLD)
                    curr = path.get(curr)

                return True

            if(neighbor.get_color() == WHITE):
                path[neighbor] = node
                queue.put(neighbor)
                neighbor.set_color(PINK)

        draw_grid(screen,grid)
        node.set_color(VIOLET)
        startNode.set_color(GREEN)
    return False;


# runs entire game and visualization
def main(screen):
    start, end = False, False
    startNode, endNode = None, None
    grid = make_grid(NODE_WIDTH)
    run = True

    while run:
        draw = True
        draw_grid(screen, grid)
        for event in pygame.event.get():
            # Ends game if window closed
            if event.type == pygame.QUIT:
                run = False

            # handles designation of start/end/barrier nodes
            if pygame.mouse.get_pressed()[0] and start and end:
                pos = pygame.mouse.get_pos()
                node = get_node(grid, pos)

                if node.get_color() != GREEN and node.get_color() != RED:
                    node.set_color(BLACK)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                node = get_node(grid, pos)
                if not (start):
                    node.set_color(GREEN)
                    start = True
                    startNode = node
                elif not (end):
                    if node.get_color() != GREEN:
                        node.set_color(RED)
                        end = True
                        endNode = node

            # empties grid and node designation upon right click
            if pygame.mouse.get_pressed()[2]:
                reset(grid)
                start, end = False, False

            # checks if spacebar has been hit validly to start algorithm
            if pygame.key.get_pressed()[pygame.K_SPACE] and (start and end):
                for i in range(len(grid)):
                    for j in range(len(grid[i])):
                        grid[i][j].update_neighbors()
                BFS(startNode, endNode, grid, screen)

    pygame.quit()

# setup pygame and screen
pygame.init()
pygame.display.set_caption("Breadth First Search Visualizer")
screen = pygame.display.set_mode((WIDTH, WIDTH))

main(screen)