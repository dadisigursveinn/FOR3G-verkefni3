import os
import random
import pygame

pygame.init()

# var
block_size = 20 # Block size
# Colors
white = (255,255,255) 
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
orange = (255, 150, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255) 
player_color = orange
gate_color = red
player_keys = 0 # Hold how many keys player has
player_points = 0 # Hold player points

# Font 
font = pygame.font.SysFont(None, 25)

# For points
def text_Objects(text, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
def message_to_screen(msg, color):
    textSurface, textRrect = text_Objects(msg, color)
    textRrect.center = (640/2), 10
    screen.blit(textSurface, textRrect)


# Class for the player
class Player(object):
    
    def __init__(self):
        self.rect = pygame.Rect(block_size, block_size, block_size, block_size)

    def move(self, dx, dy):
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    def move_single_axis(self, dx, dy):
        # Global var
        global player_keys
        global player_color
        global player_points
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy
        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
        # If you collide with a key you take the key
        for key in keys:
            if self.rect.colliderect(key.rect):
                keys.remove(key)
                player_keys += 1
                player_points -= 2
        # If you collide with a bomb you remove it if you have a key
        # If not you cant pass
        for bomb in bombs:
            if self.rect.colliderect(bomb.rect):
                if player_keys > 0:
                    bombs.remove(bomb)
                    player_keys -= 1
                    player_points += 5
                else:
                    if dx > 0: # Moving right; Hit the left side of the bomb
                        self.rect.right = bomb.rect.left
                    if dx < 0: # Moving left; Hit the right side of the bomb
                        self.rect.left = bomb.rect.right
                    if dy > 0: # Moving down; Hit the top side of the bomb
                        self.rect.bottom = bomb.rect.top
                    if dy < 0: # Moving up; Hit the bottom side of the bomb
                        self.rect.top = bomb.rect.bottom
# Nice class to hold a wall rect
class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], block_size, block_size)

# Class for key
class Key(object):
    def __init__(self, pos):
        keys.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], block_size, block_size)
# Class for bomb
class Bomb(object):
    def __init__(self, pos):
        bombs.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], block_size, block_size)
# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Maze game")
screen = pygame.display.set_mode((640, 480))

clock = pygame.time.Clock()
walls = [] # List to hold the walls
player = Player() # Create the player
keys = [] #List for keys
bombs = [] #List for bombs

# Holds the level layout in a list of strings.
level = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W W      K      W            WKW",
"W W WWWWWWWWWWW WWWBWWWWWWWW W W",
"W   W         W   B WK   W W   W",
"WWWWW WWWWWWW WWW W WWW    WWWWW",
"WK  W B    KW  KW W   W WWWW   W",
"W W W WWWWWWW WWW W W      WWW W",
"W W   W           W W     WW   W",
"W WWWWWBWWWWWWWWWWWWWWW   W  WWW",
"W W  B          W         W    W",
"W W WWWWWWWWWWW WWWBWWWW WWWW  W",
"W   W         W   W WK   W  W  W",
"WWWWW W WWWWW WWW W WWW  W  W  W",
"W   W W KW  W   W W   WWWW  W  W",
"W W W WWWWW W WWW W W    W  W  W",
"W W   W           W W    W  WW W",
"W WWWWWWWW WWWWWWWWWWWW  W     W",
"W W         WK  W            WBW",
"W W WWWWWWWWWWW WWW WWWWWWWWWW W",
"W   W         W   W WK     W W W",
"WWBWW WWWWWWW WWW W WWW    W W W",
"W   W W     W   W W   W    WWW W",
"W                     B       EW",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, block_size, block_size)
        if col == "K":
            Key((x, y))
        if col == "B":
            Bomb((x,y))
        x += block_size
    y += block_size
    x = 0

running = True
while running:
    
    clock.tick(60)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)
    
    # Just added this to make it slightly fun ;)
    if player.rect.colliderect(end_rect) and player_points >= 15:
        raise SystemExit, "You won!"
    
    # Check if player has keys to display right color
    if player_keys > 0:
        player_color = yellow
    else:
        player_color = orange
    # Draw the scene
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, white, wall.rect)
    for key in keys:
        pygame.draw.ellipse(screen, yellow, key.rect)
    for bomb in bombs:
        pygame.draw.ellipse(screen, blue, bomb.rect)

    #See if player has enaugh points to exit
    if player_points >= 15:
        gate_color = green
    else:
        gate_color = red

    message_to_screen("Points: " + str(player_points) + " Keys: " + str(player_keys), black)

    pygame.draw.rect(screen, gate_color, end_rect)
    pygame.draw.rect(screen, player_color, player.rect)
    pygame.display.flip()