import pygame, random # import pygame and random libraries 
 
# --- Globals ---
# declare colour codes for sprites etc 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 149, 0)
YELLOW = (255, 255, 0)
 
# declare play area size
width, height = 600, 600
 
# Margin between each segment
segment_margin = 3
 
# Set the width and height of each snake segment
segment_width = min(height, width) / 40 - segment_margin
segment_height = min(height, width) / 40 - segment_margin

# define some utility functions
def detect_collision(x, y):
    for segment in my_snake.segments:
        if segment.rect.x == x and segment.rect.y == y:
            return True

    for segment in enemy_snake.segments:
        if segment.rect.x == x and segment.rect.y == y:
            return True

    for item in my_food.itemlist:
        if item.rect.x == x and item.rect.y == y:
            return True

    for obstacle in my_obstacles.itemlist:
        if obstacle.rect.x == x and obstacle.rect.y == y:
            return True

    return False

def set_initial_conditions(): # function to reset game
    global enemy_snake, my_snake, my_food, my_obstacles, score, game_ended, done, score 
    my_snake = Snake(10,10, False)
    enemy_snake = Snake(590, 590, True)
    for i in range(3): enemy_snake.grow()
    my_food = Food()
    my_obstacles = Obstacles()
     
    game_ended = False
    score = 0

    my_food.replenish()
    my_obstacles.add()

class Snake():
    """ Class to represent one snake. """
    
    # Constructor
    def __init__(self, x, y, enemy):
        self.segments = []
        self.spriteslist = pygame.sprite.Group()
        self.enemy = enemy
        self.enemymovecount = 0
        self.x_change = segment_width + segment_margin
        self.y_change = 0

        x = round(x/(segment_width + segment_margin)) * (segment_width + segment_margin)
        y = round(y/(segment_height + segment_margin)) * (segment_height + segment_margin) 
        segment = Segment(x, y, enemy)
        self.segments.append(segment)
        self.spriteslist.add(segment)
            
    def move(self):

        # Figure out where new segment will be
        x = self.segments[0].rect.x + self.x_change
        y = self.segments[0].rect.y + self.y_change
        
        # Don't move off the screen
        # At the moment a potential move off the screen means nothing happens, but it should end the game
        if 0 <= x <= width - segment_width and 0 <= y <= height - segment_height:  
            # Insert new segment into the list
            segment = Segment(x, y, self.enemy)
            self.segments.insert(0, segment)
            self.spriteslist.add(segment)
            # Get rid of last segment of the snake
            # .pop() command removes last item in list
            old_segment = self.segments.pop()
            self.spriteslist.remove(old_segment)
        else:
            global game_ended
            game_ended = True

    def enemy_move(self):
        player_location = (my_snake.segments[0].rect.x, my_snake.segments[0].rect.y)

        x_difference = player_location[0] - self.segments[0].rect.x
        y_difference = self.segments[0].rect.y - player_location[1]

        # determine which direction to travel
        if self.enemymovecount % 5 == 0: # only move every 5 blocks (every so often)
            if abs(y_difference) > abs(x_difference):
                if y_difference > 0 and self.y_change != (segment_height+segment_margin):
                    # move up
                    self.x_change = 0
                    self.y_change = (segment_height + segment_margin) * -1
                else:
                    # move down
                    self.x_change = 0
                    self.y_change = (segment_height + segment_margin)
            else:
                if x_difference > 0 and self.x_change != (segment_width+segment_margin)*-1:
                    # move right 
                    self.x_change = (segment_width + segment_margin)
                    self.y_change = 0
                else:
                    # move left
                    self.x_change = (segment_width + segment_margin) * -1
                    self.y_change = 0

        # Figure out where new segment will be
        x = self.segments[0].rect.x + self.x_change
        y = self.segments[0].rect.y + self.y_change
        
        if 0 <= x <= width - segment_width and 0 <= y <= height - segment_height:  
            segment = Segment(x, y, self.enemy)
            self.segments.insert(0, segment)
            self.spriteslist.add(segment)
            old_segment = self.segments.pop()
            self.spriteslist.remove(old_segment)
        else:
            global enemy_snake # if snake hits wall 'kill' him
            enemy_snake = Snake(590, 590, True)
            for i in range(3): enemy_snake.grow()

        self.enemymovecount += 1


    def grow(self):
        x = self.segments[0].rect.x + self.x_change
        y = self.segments[0].rect.y + self.y_change
        segment = Segment(x, y, self.enemy)
        self.segments.append(segment)
        self.spriteslist.add(segment)
    
class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of a snake. """

    # Constructor
    def __init__(self, x, y, enemy):
        # Call the parent's constructor
        super().__init__()
 
        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        if enemy:
            self.image.fill(ORANGE)
        else:
            self.image.fill(WHITE)
 
        # Set top-left corner of the bounding rectangle to be the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Food():
    """ class to represent all the food items """ 
    
    def __init__(self):
        self.itemlist = pygame.sprite.Group()

    def replenish(self):
        randx = random.randint(0,width-(segment_width+segment_margin))
        randy = random.randint(0,height-(segment_width+segment_margin))
        x = round(randx/(segment_width + segment_margin)) * (segment_width + segment_margin)
        y = round(randy/(segment_height + segment_margin)) * (segment_height + segment_margin) 

        collision = detect_collision(x,y) 
        if not collision:
            self.itemlist.add(Food_item(x,y))
        else:
            self.replenish()

class Food_item(pygame.sprite.Sprite):
    """ class to represent one food item """

    def __init__(self, x, y):
        super().__init__()
        self.value = random.randint(1,3)
        self.image = pygame.Surface([segment_width, segment_height])
        if self.value == 1: # change colour based on self.value 
            self.image.fill(GREEN)

        elif self.value == 2:
            self.image.fill(YELLOW)
        elif self.value == 3:
            self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        
class Obstacles():
    """ Class to manage the group of obstacles """

    def __init__(self):
        self.itemlist = pygame.sprite.Group()

    def add(self):
        # determine where it will fit on the grid
        randx = random.randint(0,width-(segment_width+segment_margin))
        randy = random.randint(0,height-(segment_width+segment_margin)) 
        x = round(randx/(segment_width + segment_margin)) * (segment_width + segment_margin)
        y = round(randy/(segment_height + segment_margin)) * (segment_height + segment_margin) 

        collision = detect_collision(x,y) # when placing an obstacle make sure it does not collide with anything
        if not collision:
            self.itemlist.add(Obstacle(x,y))
        else:
            self.add()

class Obstacle(pygame.sprite.Sprite):
    # class to represent one obstacle 

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(RED) # obstacle are red 

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        
# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create a 600x600 sized screen
screen = pygame.display.set_mode([width, height+50])
 
# Set the title of the window
pygame.display.set_caption('Snake')
 
set_initial_conditions() # set all the inital conditions etc
 
clock = pygame.time.Clock()
done = False
game_ended = False
score = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        # Set the direction based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN: # added ability to use WASD/HJKL as alternate controls
            if event.key == pygame.K_q:
                quit()
            if event.key in [pygame.K_LEFT, pygame.K_a, pygame.K_h] and my_snake.x_change != (segment_width + segment_margin): # changed it so you can't go back on yourself by pressing the opposite direction
                my_snake.x_change = (segment_width + segment_margin) * -1
                my_snake.y_change = 0
            if event.key in [pygame.K_RIGHT, pygame.K_d, pygame.K_l] and my_snake.x_change != (segment_width + segment_margin) * -1:
                my_snake.x_change = (segment_width + segment_margin)
                my_snake.y_change = 0
            if event.key in [pygame.K_UP, pygame.K_w, pygame.K_k] and my_snake.y_change != (segment_width + segment_margin):
                my_snake.x_change = 0
                my_snake.y_change = (segment_height + segment_margin) * -1
            if event.key in [pygame.K_DOWN, pygame.K_s, pygame.K_j] and my_snake.y_change != (segment_width + segment_margin) * -1:
                my_snake.x_change = 0
                my_snake.y_change = (segment_height + segment_margin)
 
    if not game_ended:
        # move snake one step
        my_snake.move()
        enemy_snake.enemy_move()
    
        # Clear screen
        screen.fill(BLACK)
        my_snake.spriteslist.draw(screen)
        enemy_snake.spriteslist.draw(screen)

        # check if snake picks up food, only one item at a time
        food_collisions = pygame.sprite.spritecollide(my_snake.segments[0], my_food.itemlist, False)
        if len(food_collisions) > 0:
            my_snake.grow()
            my_food.replenish()
            my_obstacles.add()
            score += food_collisions[0].value
            food_collisions[0].kill()

        my_food.itemlist.draw(screen) # update 
        my_obstacles.itemlist.draw(screen)

        # check collisions
        sprites_copy = my_snake.spriteslist.copy()
        sprites_copy.remove(my_snake.segments[0])
        my_snake_collisions = len(pygame.sprite.spritecollide(my_snake.segments[0], sprites_copy, False))
        my_obstacles_collisions = len(pygame.sprite.spritecollide(my_snake.segments[0], my_obstacles.itemlist, False))
        my_enemy_collisions = len(pygame.sprite.groupcollide(my_snake.spriteslist, enemy_snake.spriteslist, False, False)) 
        if  my_snake_collisions > 0 or my_obstacles_collisions > 0 or my_enemy_collisions > 0:
            game_ended = True

        # check if enemy collides with an obstacle
        enemy_snake_obstacles_collisions = len(pygame.sprite.groupcollide(my_obstacles.itemlist, enemy_snake.spriteslist, True, True))
        if enemy_snake_obstacles_collisions > 0:
            enemy_snake = Snake(590, 590, True)
            for i in range(3): enemy_snake.grow()

        # check if enemy collides with food 
        enemy_snake_food_collisions = len(pygame.sprite.groupcollide(my_food.itemlist, enemy_snake.spriteslist, True, False))
        if enemy_snake_food_collisions > 0:
            enemy_snake.grow()
            my_food.replenish()

        # create the score box 
        gutter = pygame.Surface((600, 50))
        gutter.fill((255,255,255))
        screen.blit(gutter, (0,height))

        font = pygame.font.SysFont("comicsansms", 50)
        text = font.render(str(score), True, (0, 0, 0), None)
        textrect = text.get_rect()
        textrect.x,textrect.y = 5, height-12
        screen.blit(text, textrect)
            
    else:
        font = pygame.font.SysFont("comicsansms", 50)
        text = font.render("Game Over", True, (255, 0, 0), None)
        gorect = text.get_rect()
        gorect.x,gorect.y = 180, height-12

        screen.blit(text, gorect)
        pygame.display.flip() # display game over message
        
        while True: # allow replay by any keypress
            event = pygame.event.wait()
            if event.type == pygame.QUIT or event.key == pygame.K_q: # allow quit 
                quit()
            elif event.type == pygame.KEYDOWN: # wait for any event (keypress/mouse move)
                set_initial_conditions() # reset
                break

    pygame.display.flip()
    clock.tick(10)
 
pygame.quit()
