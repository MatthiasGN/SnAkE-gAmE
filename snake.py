import math
import random
import pygame

class Cube:
    def __init__(self, pos, dirx=1, diry=0, colour=(255,0,0)):
        self.pos = pos
        self.dirx = dirx
        self.diry = diry
        self.colour = colour

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0]+self.dirx, self.pos[1]+self.diry)

    def draw(self, cell_width, surface):
        x = self.pos[0]
        y = self.pos[1]
        pygame.draw.rect(surface, self.colour, (x*cell_width+1, y*cell_width+1, cell_width-2, cell_width-2))



class Snake:

    body = []
    turns = {}

    def __init__(self, colour, pos):
        self.head = Cube(pos, colour=colour)
        self.body.append(self.head)
        self.dirx = 1
        self.diry = 0

    def move(self, left, right, up, down, rows, cols):
        # Loop through cubes in the snake and move each cube in the correct direction.
        # Have to take note of turns so that each block moves appropriately.

        if left or right or up or down:
            if left and (self.head.dirx != 1):
                self.dirx = -1
                self.diry = 0

            if right and (self.head.dirx != -1):
                self.dirx = 1
                self.diry = 0
            
            if up and (self.head.diry != 1):
                self.dirx = 0
                self.diry = -1
            
            if down and (self.head.diry != -1):
                self.dirx = 0
                self.diry = 1

            self.turns[self.head.pos] = [self.dirx, self.diry]

        # print("Turns: " + str(self.turns))

        # For each cube, update its direction according to the snake turns.
        # If its position is not at a turn, just move it according to its own direction
        # Then draw each cube.
        for i, cube in enumerate(self.body):
            curr_pos = cube.pos
            if curr_pos in self.turns:
                turn = self.turns[curr_pos]
                cube.move(turn[0], turn[1])
                
                # Remove final turn since cube leaves that position.
                if i == len(self.body)-1:
                    self.turns.pop(curr_pos)
            else:
                # EASY MODE
                # if cube.dirx == -1 and cube.pos[0] <= 0: cube.pos = (rows-1, cube.pos[1])
                # elif cube.dirx == 1 and cube.pos[0] >= rows-1: cube.pos = (0,cube.pos[1])
                # elif cube.diry == 1 and cube.pos[1] >= rows-1: cube.pos = (cube.pos[0], 0)
                # elif cube.diry == -1 and cube.pos[1] <= 0: cube.pos = (cube.pos[0],rows-1)

                # else:
                #     cube.move(cube.dirx, cube.diry)

                # HARD MODE
                cube.move(cube.dirx, cube.diry)
        
    def draw(self, cell_width, rows, cols, surface):
        for i, cube in enumerate(self.body):

            # When a snack is eaten, if the snake's tail is touching the border,
            # the program will attempt to draw a cube outside the borders of the surface.
            # So just avoid drawing these cubes, and once they are within the borders they
            # can once again be drawn properly.
            if cube.pos[0]>= 0 or cube.pos[0]<rows-1 or cube.pos[1]>=0 or cube.pos[1]<cols:
                cube.draw(cell_width, surface)
            # if i == 0:
            #     cube_width = width // rows
            #     eyes_centre = cube_width // 3
            #     radius = 3
            #     eye1_middle = (cube.pos[0]*cube_width, cube.pos[1]*cube_width+eyes_centre)
            #     eye2_middle = (cube.pos[0]*cube_width, cube.pos[1]*cube_width+eyes_centre)
            #     pygame.draw.circle(surface, (100,100,100), eye1_middle, radius)
            #     pygame.draw.circle(surface, (100,100,100), eye2_middle, radius)

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirx = dx
        self.body[-1].diry = dy
        self.body[-1].colour = tail.colour

    def reset(self, rows, cols):
        self.head = Cube((rows//2, cols//2), colour=(255,255,0))
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = 0


def draw_grid(cell_width, rows, cols, surface):
    x = 0
    y = 0

    for row in range(rows):
        x += cell_width
        pygame.draw.line(surface, (255,255,255), (x,0), (x,cell_width*rows))

    for col in range(cols):
        y += cell_width
        pygame.draw.line(surface, (255,255,255), (0,y), (cell_width*cols,y))

def draw_window(cell_width, rows, cols, snake, snack, surface):
    surface.fill((0,0,0))
    snack.draw(cell_width, surface)
    snake.draw(cell_width, surface)
    draw_grid(cell_width, rows, cols, surface)
    pygame.display.update()


def random_snack(snake, rows, cols):
    while True:
        valid_x = True
        valid_y = True

        snack_x = random.randint(0, rows-1)
        snack_y = random.randint(0, cols-1)
        
        for cube in snake.body:
            if snack_x == cube.pos[0]:
                valid_x = False
            if snack_y == cube.pos[1]:
                valid_y = False
        
        if valid_x and valid_y:
            break
    
    return snack_x, snack_y

def pause_game(height, width, surface):
    pause_text = pygame.font.SysFont("helvetica", 50)
    text_surface = pause_text.render("PaUsEd", True, (255,255,0))
    text_rect = text_surface.get_rect(center=(width//2, height//3))
    # surface.fill((0, 0, 0))
    surface.blit(text_surface, text_rect)

    pause = True
    while pause is True:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                pause = False
                break
            

        pygame.display.update()

def reset_game(snake, snack, rows, cols, score, high_score):
    snake.reset(rows, cols)
    if score > high_score:
        high_score = score
    score = 0
    snack.pos = random_snack(snake, rows, cols)
    return score, high_score

def main():
    pygame.init()

    rows = 20
    cols = 20
    cell_width = 30

    width = rows*cell_width
    height = cols*cell_width

    surf = pygame.display.set_mode((height, width))
    snake = Snake((255,255,0), (rows//2,cols//2))
    snack = Cube((random_snack(snake, rows, cols)),0,0,(255,0,0))

    score = 0
    high_score = 0

    play = True
    clock = pygame.time.Clock()

    while play is True:
        pygame.time.delay(50)
        clock.tick(10)

        left = right = up = down = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                break

            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                play = False
                break

            elif keys[pygame.K_p]:
                pause_game(height, width, surf)
                break
            
            if keys[pygame.K_LEFT]:
                left = True
            elif keys[pygame.K_RIGHT]:
                right = True
            elif keys[pygame.K_UP]:
                up = True
            elif keys[pygame.K_DOWN]:
                down = True

        if play is True:
            snake.move(left, right, up, down, rows, cols)

            head_pos, dx, dy = snake.head.pos, snake.head.dirx, snake.head.diry

            # Eat snack
            if head_pos == snack.pos:
                score += 1
                snake.add_cube()
                snack = Cube((random_snack(snake, rows, cols)),0,0,(255,0,0))
                print("delishous")

            # Hit border
            elif (
                dx == -1 and head_pos[0] < 0 or
                dx == 1 and head_pos[0] >= rows or
                dy == 1 and head_pos[1] >= rows or
                dy == -1 and head_pos[1] < 0):

                score, high_score = reset_game(snake, snack, rows, cols, score, high_score)
                print("Borders are not your friend.")
            
            # Hit itself
            for cube in snake.body[1:]:
                if head_pos == cube.pos:
                    score, high_score = reset_game(snake, snack, rows, cols, score, high_score)
                    print("Congrats, you played (hit) yaself")
                    break

            pygame.display.set_caption('SnAkE gAmE.  Score: %s  High Score: %s' % (score, high_score))
            draw_window(cell_width, rows, cols, snake, snack, surf)

    pygame.quit()

main()