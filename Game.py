import pygame
import random
import sys 


pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

sounds4_path = r"C:\Users\admin\Documents\TANK DESTROYER\sounds\gamestart.ogg"
sounds5_path = r"C:\Users\admin\Documents\TANK DESTROYER\sounds\gameover.ogg"
sounds6_path = r"C:\Users\admin\Documents\TANK DESTROYER\sounds\bonus.ogg"
sounds9_path = r"C:\Users\admin\Documents\TANK DESTROYER\sounds\victory.mp3"
sounds1_path = r"C:\Users\admin\Documents\TANK DESTROYER\sounds\gun.mp3"
sounds2_path = r"C:\Users\admin\Documents\TANK DESTROYER\sounds\shot.mp3"
sounds7_path = r"C:\Users\admin\Documents\TANK DESTROYER\sounds\Button.mp3"
sounds3_path = r"C:\Users\admin\Documents\TANK DESTROYER\sounds\explosion .mp3"
sounds8_path = r"C:\Users\admin\Documents\TANK DESTROYER\sounds\Level Up.mp3"

item1_path = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Item\bullet.png"
item2_path = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Item\speed.png"
item3_path = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Item\health.png"
item4_path = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Item\shield.png"

object1_path = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Object\block.png"
object2_path = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Object\explode.png"

PlayerTank1 = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Tanks\green.png"
PlayerTank2 = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Tanks\greenL.png"
PlayerTank3 = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Tanks\greenR.png"
PlayerTank4 = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Tanks\greenD.png"

EnemyTank1 = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Tanks\Up.png"
EnemyTank2 = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Tanks\Left.png"
EnemyTank3 = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Tanks\Right.png"
EnemyTank4 = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Tanks\Down.png"
icons = r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Tanks\Destroyer.png"

screen1 =  r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Screen\vic.png"
screen2 =  r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Screen\ovr.png"
screen3 =  r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Screen\intro_image.png"
screen4 =  r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Screen\Next.png"
screen5 =  r"C:\Users\admin\Documents\TANK DESTROYER\Pictures\Screen\battle.png"

# Load game icon
icon = pygame.image.load(icons)
pygame.display.set_icon(icon)

# sounds
gun_sound = pygame.mixer.Sound(sounds1_path)
shot_sound = pygame.mixer.Sound(sounds2_path)
explosion_sound = pygame.mixer.Sound(sounds3_path)
intro_sound = pygame.mixer.Sound(sounds4_path)
gameover_sound = pygame.mixer.Sound(sounds5_path)
bouns_sound = pygame.mixer.Sound(sounds6_path)
next_sound = pygame.mixer.Sound(sounds7_path)
levelup_sound = pygame.mixer.Sound(sounds8_path)
vic_sound = pygame.mixer.Sound(sounds9_path)


# Load images
playertank_up_image = pygame.image.load("green.png")
playertank_down_image = pygame.image.load("greenD.png")
playertank_left_image = pygame.image.load("greenR.png")
playertank_right_image = pygame.image.load("greenL.png")
enemy_up_image = pygame.image.load("Up.png")
enemy_down_image = pygame.image.load("Down.png")
enemy_left_image = pygame.image.load("Left.png")
enemy_right_image = pygame.image.load("Right.png")
block_image = pygame.image.load("block.png")

# Shield
shield_image = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.circle(shield_image, (0, 0, 255, 100), (25, 25), 25)  # Semi-transparent blue circle

## Super weapon bullet
super_weapon_image = pygame.Surface((50, 50), pygame.SRCALPHA)
pygame.draw.rect(super_weapon_image, (255, 0, 0, 100), (0, 0, 50, 50))  # Semi-transparent red square

# Item spawn timer
item_spawn_time = pygame.time.get_ticks()
item_spawn_interval = 10000  # Spawn an item every 15 seconds
 

# Android controls
button_size = 70
controls = {
    'Left': pygame.Rect(30, 740, button_size, button_size),
    'Right': pygame.Rect(170, 740, button_size, button_size),
    'Up': pygame.Rect(100, 680, button_size, button_size),
    'Down': pygame.Rect(100, 800, button_size, button_size),
    'Fire': pygame.Rect(500, 700, button_size, button_size)
}
# Bullet groups
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
items = pygame.sprite.Group()
power_ups = pygame.sprite.Group()
explosions = pygame.sprite.Group()

intro_image = pygame.transform.scale(pygame.image.load(screen3), (SCREEN_WIDTH, SCREEN_HEIGHT))
LVL = pygame.transform.scale(pygame.image.load(screen4), (SCREEN_WIDTH, SCREEN_HEIGHT))
ovr = pygame.transform.scale(pygame.image.load(screen2), (SCREEN_WIDTH, SCREEN_HEIGHT))
vic = pygame.transform.scale(pygame.image.load(screen1), (SCREEN_WIDTH, SCREEN_HEIGHT))
batt = pygame.transform.scale(pygame.image.load(screen5), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Game states
PLAYING = 0
PAUSED = 0
GAME_OVER = 1
LEVEL_COMPLETE = 5
game_state = PLAYING  

level_0 = [
        [1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1]
]

level_1 = [
        [1, 0, 1, 0, 1, 1],
        [1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1],
        [1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1]
]
level_2 = [ 
        [1, 1, 1, 1, 1, 1],
        [1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1]
]   
level_3 = [    
        [1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0],
        [1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 0],
        [1, 1, 0, 1, 1, 1]
     
]
level_4 = [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1]
]
level_5 = [
        [1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 0, 1],
        [1, 1, 1, 0, 1, 1],
        [1, 0, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1]     
]
current_level = 1
max_level = 5
levels = [
    level_0,
    level_1,
    level_2,
    level_3,
    level_4,
    level_5,
]

# Set the player starting positions per level
player_start_positions = {
    1: (400, 300),  #
    2: (50, 75), 
    3: (700, 450),
    4: (150, 470),
    5: (650, 75),      
}

enemy_positions_by_level = {
    1: [(550, 400), (200, 300)],  
    2: [(200, 400), (400, 300), (520, 400)], 
    3: [(100, 100), (300, 300), (400, 450), (400, 100)],  
    4: [(80, 75), (400, 300), (400, 470), (600, 75), (150, 300)], 
    5: [(100, 100), (370, 450), (600, 450), (370, 150), (150, 400), (500, 200)], 

}


grid_rows = 4
grid_cols = 2
spacing = 100

# Obstacle size
obstacle_width = 100
obstacle_height = 100
 

 
# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

# Load fonts
font = pygame.font.Font('Minecraft.ttf', 30)
button_font = pygame.font.Font('Minecraft.ttf', 30)

# Game title text
title_text = font.render("TANK DESTROYER", True, WHITE)


# Button class to handle rendering and clicking
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        pygame.mixer.Sound.play(next_sound)
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)

        text_surface = button_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event, current_level=None):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
         if pygame.mixer.Sound.play(next_sound):
          if self.action:   
           self.action(current_level)
           return True 
        return False

# Button actions
def start_game(current_level):
    global game_state
    game_state = PLAYING
    current_level = next_levels(current_level)
    
    load_next_level()
    main_game()

def next_levels(current_level):
    global game_state 
    
    
    if current_level is None:  
        current_level = 0

    # Move to the next level if possible
    if current_level < len(levels) - 1:
        current_level += 1
    else:
        game_state = "VICTORY"  # Game is complete

    return current_level

def reset_items():
    global items
    items.empty()


def show_controls(current_level):
    controls_screen()

def quit_game(current_level):
    pygame.quit()
    sys.exit()
def Quit_game(current_level):
    intro()

def back_to_intro(curret_level):
    intro()
  
def all_enemies_defeated():
    return len(enemy_tanks) == 0 

def play_again(current_level):
    global game_state
    game_state = PLAYING
    
    reset_items()
    main_game()


# Buttons for various screens
continue_button = Button("Continue", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 60, GREEN, LIGHT_GRAY)
pause_button = Button("Paused", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 60, GREEN, LIGHT_GRAY)
next_level_button = Button("Next Level", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 60, BLACK, LIGHT_GRAY, action=next_levels)
play_again_button = Button("Play Again", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 60, RED, LIGHT_GRAY, play_again)
exit_button = Button("Exit", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 60, GREEN, LIGHT_GRAY, Quit_game)

# Create buttons for intro
start_button = Button("Start", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 60, BLACK, LIGHT_GRAY, start_game)
Quit_button = Button("Quit", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 60, BLACK, LIGHT_GRAY, Quit_game)
controls_button = Button("Controls", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 60, BLACK, LIGHT_GRAY, show_controls)
quit_button = Button("Quit", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 60, BLACK, LIGHT_GRAY, quit_game)

# Intro function
def intro():
    pygame.mixer.Sound.play(intro_sound)
   
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(current_level)
            for button in [start_button, controls_button, quit_button]:
                button.is_clicked(event, current_level)

        screen.blit(intro_image, (0, 0))

        # Title text
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        screen.blit(title_text, title_rect)

        # Draw buttons
        start_button.draw()
        controls_button.draw()
        quit_button.draw()

        # Update the display
        pygame.display.flip()

# Controls screen function with Back button
def controls_screen():
    back_button = Button("Back", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 60, BLUE, LIGHT_GRAY, back_to_intro)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(current_level)
            back_button.is_clicked(event, current_level)

        screen.blit(intro_image, (0, 0))

        # Display controls information
        title_text = font.render("TANK DESTROYER", True, RED, DARK_GRAY)

        # Render each line separately
        controls_text1_line1 = button_font.render('Computer: Use arrow keys to move', True, WHITE, DARK_GRAY)
        controls_text1_line2 = button_font.render('and space to shoot.', True, WHITE, DARK_GRAY)

        controls_text2_line1 = button_font.render('Android: Use Up, Right, Down, Left', True, WHITE, DARK_GRAY)
        controls_text2_line2 = button_font.render('to move and Fire to Shoot.', True, WHITE,DARK_GRAY)

        # Blit title text
        screen.blit(title_text, (250, 50))

        # Blit each line of control text
        screen.blit(controls_text1_line1, (120, 150))
        screen.blit(controls_text1_line2, (210, 190))

        screen.blit(controls_text2_line1, (120, 240))
        screen.blit(controls_text2_line2, (175, 280))

        # Draw Back button
        back_button.draw()

        # Update the display
        pygame.display.flip()

def next_Levels():
    global game_state
    global current_level
    reset_items()
    current_level = next_levels(current_level)  
    if game_state == "VICTORY":
        
        display_victory_screen()
    else:
        game_state = PLAYING  
        load_next_level()  
        main_game()
   

def game_over_screen():
    pygame.mixer.Sound.play(gameover_sound)
    global game_state
    game_state = GAME_OVER
    reset_items()
    
    

    while game_state == GAME_OVER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(current_level)
            for button in [Quit_button]:
                button.is_clicked(event)
            if play_again_button.is_clicked(event):
                current_level = 0  
                game_state = PLAYING
                main_game()
            

        # Display game over screen
        screen.blit(ovr, (0, 0))
        
        
        play_again_button.draw()
        quit_button.draw()
        pygame.display.update()

def display_victory_screen():
    pygame.mixer.Sound.play(vic_sound)
   
    global game_state
    game_state = "VICTORY"

    while game_state == "VICTORY":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(current_level)
            exit_button.is_clicked(event)
                

        screen.blit(vic, (0, 0))
        
        play_again_button.draw()
        exit_button.draw()
        pygame.display.update()
         
def pause_game():
    global game_state
    game_state = PAUSED

    while game_state == PAUSED:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            continue_button.is_clicked(event)
            quit_button.is_clicked(event)

        # Display pause screen
        screen.fill(DARK_GRAY)
        continue_button.draw()
        quit_button.draw()
        pygame.display.flip()
          
def handle_level_complete():
    pygame.mixer.Sound.play(levelup_sound)
   
    global game_state
    reset_items()
    
    # Check if all enemies are defeated or other conditions for level completion are met
    if all_enemies_defeated():
        game_state = LEVEL_COMPLETE  
        while game_state == LEVEL_COMPLETE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game(current_level)

                if next_level_button.is_clicked(event):
                    game_state = "IN_PROGRESS"
                    next_Levels()  
                    break

                if Quit_button.is_clicked(event):
                    Quit_game()

            
            screen.blit(LVL, (0,0))
            title_text = button_font.render(f"LEVEL {current_level} COMPLETE!", True, GREEN)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150))

            next_level_button.draw()
            Quit_button.draw()
            pygame.display.flip()

class PlayerTank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = {
            0: playertank_up_image,    # Up
            1: playertank_right_image, # Right
            2: playertank_down_image,  # Down
            3: playertank_left_image   # Left
        }
        self.image = self.images[0]  # Default direction: Up
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tankx_change = 0
        self.tanky_change = 0
        self.direction = 0  
        self.health = 100
        self.speed = 1.5  
         # Shield and Super Weapon attributes
        self.shield = False
        self.shield_timer = 0
        self.super_weapon = False
        self.super_weapon_timer = 0
        self.plus_speed = False
        self.plus_speed_timer = 0
        self.plus_health = False
        self.plus_health_timer = 0         
        self.shoot_delay = 1000
        self.last_shot_time = pygame.time.get_ticks()
        self.max_active_bullets = 5  
        self.shield_surface = shield_image
        self.super_weapon_surface = super_weapon_image   


    def update(self):
   
     previous_position = self.rect.topleft
     self.move()
     self.check_boundary_constraints()
     self.handle_obstacle_collision(previous_position)
     self.update_direction_and_image()
     if self.shield and pygame.time.get_ticks()-self.shield_timer > 500:
         self.shield = False
     if self.super_weapon and pygame.time.get_ticks()-self.super_weapon_timer > 500:
         self.super_weapon = False
     if self.plus_speed and pygame.time.get_ticks()-self.plus_speed_timer > 500:
         self.plus_speed = False
         self.speed = max(1, self.speed - 5)    

     
    def move(self):
     """Apply movement changes to the tank's position."""
     self.rect.x += self.tankx_change
     self.rect.y += self.tanky_change

    def handle_obstacle_collision(self, previous_position):
      """Handle collisions and revert to the previous position if a collision is detected."""
      if pygame.sprite.spritecollide(self, obstacles, False):
        
        self.rect.topleft = previous_position
        self.tankx_change, self.tanky_change = 0, 0

    def check_boundary_constraints(self):
      """Ensure the tank stays within the game screen boundaries."""
    # Horizontal boundary check
      self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
    
    # Vertical boundary check
      self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

    def update_direction_and_image(self):
      """Set the tank's direction based on movement and update the image."""
      if self.tankx_change < 0:
         self.direction = 3  # Left
      elif self.tankx_change > 0:
         self.direction = 1  # Right
      elif self.tanky_change < 0:
         self.direction = 0  # Up
      elif self.tanky_change > 0:
         self.direction = 2  # Down

    # Update the image if the direction is valid
      if self.direction in range(len(self.images)):
        self.image = self.images[self.direction]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        if self.shield:
            shield_rect = self.shield_surface.get_rect(center=self.rect.center)
            screen.blit(self.shield_surface, shield_rect)
        if self.super_weapon:
            super_weapon_rect = self.super_weapon_surface.get_rect(center=self.rect.center)
            screen.blit(self.super_weapon_surface, super_weapon_rect)
      
        if self.plus_speed:
            plus_speed_rect = self.plus_speed_surface.get_rect(center=self.rect.center)
            screen.blit(self.plus_speed_surface, plus_speed_rect)


    def draw_health_bar(self, screen):
        bar_y_position = self.rect.y - 10
        pygame.draw.rect(screen, (100, 0, 0), (self.rect.x, bar_y_position, self.rect.width, 5))  
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, bar_y_position, self.rect.width * (self.health / 100), 5))  

    def take_damage(self, amount):
        if not self.shield:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.kill()
                
    def shoot(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot_time >= self.shoot_delay:
            if len(bullets) < self.max_active_bullets:
                if self.super_weapon:
                    bullet = SuperBullet(self.rect.centerx, self.rect.centery, self.direction)
                else:
                    bullet = PlayerBullet(self.rect.centerx, self.rect.centery, self.direction)
                
                bullets.add(bullet)
                self.last_shot_time = current_time
      
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
       
        self.item_type = item_type
        self.load_image()
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def load_image(self):
        if self.item_type == 'shield':
            self.image = pygame.image.load(item4_path).convert_alpha()
        elif self.item_type == 'super_weapon':
            self.image = pygame.image.load(item1_path).convert_alpha()
        elif self.item_type == 'plus_health':
            self.image = pygame.image.load(item3_path).convert_alpha()
        elif self.item_type == 'plus_speed':
            self.image = pygame.image.load(item2_path).convert_alpha()

    def apply(self, player_tank):
        pygame.mixer.Sound.play(bouns_sound)
        if self.item_type == 'shield':
            player_tank.shield = True
            player_tank.shield_timer = pygame.time.get_ticks()
        elif self.item_type == 'super_weapon':
            player_tank.super_weapon = True
            player_tank.super_weapon_timer = pygame.time.get_ticks()
        elif self.item_type == 'plus_health':
            player_tank.health = min(player_tank.health + 20, 100)
        elif self.item_type == 'plus_speed':
           if not player_tank.plus_speed:
            player_tank.speed += 2
            player_tank.plus_speed = True
            player_tank.plus_speed_timer = pygame.time.get_ticks()
        self.kill()

    def update(self):
        if (self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
            self.rect.right < 0 or self.rect.left > SCREEN_WIDTH):
            self.kill()

def spawn_item():
    item_types = ['shield', 'super_weapon', 'plus_health', 'plus_speed']
    probabilities = [0.3, 0.4, 0.2, 0.5]  
    
    item_type = random.choices(item_types, probabilities)[0]
    x = random.randint(0, SCREEN_WIDTH - 20)
    y = random.randint(0, SCREEN_HEIGHT - 20)
    item = Item(x, y, item_type)
    items.add(item)

class EnemyTank(pygame.sprite.Sprite):
    UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3

    def __init__(self, x, y):
        super().__init__()
        self.images = {
            self.UP: enemy_up_image,
            self.RIGHT: enemy_right_image,
            self.DOWN: enemy_down_image,
            self.LEFT: enemy_left_image
        }
        self.direction = random.choice([self.UP, self.RIGHT, self.DOWN, self.LEFT])
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.health = 100
        self.shoot_delay = 1000  
        self.shoot_range = 100  
        self.timer = pygame.time.get_ticks()
        self.patrol_timer = pygame.time.get_ticks()
        self.patrol_delay = 1000  
        self.patrolling = True

    def draw_health_bar(self, screen):
        bar_y_position = self.rect.y + self.rect.height + 5
        pygame.draw.rect(screen, (100, 0, 0), (self.rect.x, bar_y_position, self.rect.width, 5)) 
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, bar_y_position, self.rect.width * (self.health / 100), 5)) 
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def is_visible_to_enemy(self, grass_group):
        return all(not grass.rect.colliderect(self.rect) for grass in grass_group)

    def update(self):
        current_time = pygame.time.get_ticks()
        self.patrol()
        self.move_tank()
        self.handle_boundaries()

        distance_to_player = pygame.math.Vector2(
            player_tank.rect.centerx - self.rect.centerx,
            player_tank.rect.centery - self.rect.centery
        ).length()

        if distance_to_player < self.shoot_range:
            self.attack_player()
        
        if self.direction is None:             
             self.direction = 0 


    def attack_player(self):
        """Handle attacking behavior towards the player."""
        self.direction = self.get_direction_towards_player()
        
        if pygame.time.get_ticks() - self.timer > self.shoot_delay:
            self.timer = pygame.time.get_ticks()
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, self.direction)
            enemy_bullets.add(bullet)

    def patrol(self):
        """Handle patrolling behavior."""
        if self.patrolling:
            if pygame.time.get_ticks() - self.patrol_timer > self.patrol_delay:
                self.direction = random.choice([self.UP, self.RIGHT, self.DOWN, self.LEFT])
                self.patrol_timer = pygame.time.get_ticks()

    def get_direction_towards_player(self):
        if player_tank.rect.x < self.rect.x:
            return self.LEFT
        elif player_tank.rect.x > self.rect.x:
            return self.RIGHT
        elif player_tank.rect.y < self.rect.y:
            return self.UP
        elif player_tank.rect.y > self.rect.y:
            return self.DOWN

    def move_tank(self):
        previous_position = self.rect.topleft  
        if self.direction == self.UP:
            self.rect.y -= self.speed
        elif self.direction == self.RIGHT:
            self.rect.x += self.speed
        elif self.direction == self.DOWN:
            self.rect.y += self.speed
        elif self.direction == self.LEFT:
            self.rect.x -= self.speed

        self.image = self.images[self.direction]

        # Check for collisions after movement
        if pygame.sprite.spritecollide(self, obstacles, False):
            
            self.rect.topleft = previous_position  

    def handle_boundaries(self):
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction = random.choice([self.RIGHT, self.DOWN])
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.direction = random.choice([self.RIGHT, self.UP])
        if self.rect.left <= 0:
            self.rect.left = 0
            self.direction = random.choice([self.DOWN, self.UP])
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.direction = random.choice([self.LEFT, self.DOWN])

   
   #EnemyBullet     
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        pygame.mixer.Sound.play(gun_sound)
        self.image = pygame.Surface((5, 20))
        self.image.fill((0, 0, 0))  
        self.rect = self.image.get_rect()        
        self.speed_x = 0
        self.speed_y = 0
        if direction == 0:  # Up
            self.rect.centerx = x
            self.rect.bottom = y
            self.speed_x = 0
            self.speed_y = -4
        elif direction == 1:  # Right
            self.rect.left = x
            self.rect.centery = y
            self.speed_x = 4
            self.speed_y = 0
            self.image = pygame.transform.rotate(self.image, -90)  
        elif direction == 2:  # Down
            self.rect.centerx = x
            self.rect.top = y
            self.speed_x = 0
            self.speed_y = 4
        elif direction == 3:  # Left
            self.rect.right = x
            self.rect.centery = y
            self.speed_x = -4
            self.speed_y = 0
            self.image = pygame.transform.rotate(self.image, 90)
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if pygame.sprite.spritecollide(self, obstacles, False):
            self.kill()
        
        if (self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
            self.rect.right < 0 or self.rect.left > SCREEN_WIDTH):
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, color, speed, damage):
        super().__init__()        
        self.image = pygame.Surface((5, 20))
        self.color = color
        self.image.fill(self.color)
        self.speed = speed
        self.damage = damage
        self.rect = self.image.get_rect()
        
        if direction == 0:  # Up
            self.rect.centerx = x
            self.rect.bottom = y
            self.speed_x = 0
            self.speed_y = -self.speed
        elif direction == 1:  # Right
            self.rect.centerx = x
            self.rect.top = y
            self.speed_x = self.speed
            self.speed_y = 0
            self.image = pygame.transform.rotate(self.image, -90)
        elif direction == 2:  # Down
            self.rect.centerx = x
            self.rect.top = y
            self.speed_x = 0
            self.speed_y = self.speed
        elif direction == 3:  # Left
            self.rect.centerx = x
            self.rect.top = y
            self.speed_x = -self.speed
            self.speed_y = 0
            self.image = pygame.transform.rotate(self.image, 90)
  
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
            
        if pygame.sprite.spritecollide(self, obstacles, False):
            self.kill()
        if (self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
            self.rect.right < 0 or self.rect.left > SCREEN_WIDTH):
            self.kill()


class PlayerBullet(Bullet):
    def __init__(self, x, y, direction):
        pygame.mixer.Sound.play(gun_sound)
        damage = 20
        speed = 5
        color = (0, 0, 0)
        super().__init__(x, y, direction, color, speed, damage)
       
class SuperBullet(Bullet):
    def __init__(self, x, y, direction):
        pygame.mixer.Sound.play(shot_sound)
        damage = 20
        speed = 10
        color = (255, 0, 0)
        super().__init__(x, y, direction, color, speed, damage)
        # Set maximum active bullets and cooldown
        self.max_active_bullets = 20
        self.cooldown_color = (255, 100, 100)  
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_delay = 1000  # 1 second cooldown

    def update(self):
        # Check if the cooldown period has passed
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time < self.shoot_delay:
            self.image.fill(self.cooldown_color)
        else:
            self.image.fill((255, 0, 0))  
        
        super().update()
 

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y,width, height):
        super().__init__()
        self.image = pygame.image.load(object1_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
       
# Create a group to hold all the obstacles
obstacles = pygame.sprite.Group()

# Create obstacles in a grid layout
for row in range(grid_rows):
    for col in range(grid_cols):
        x = col * (obstacle_width + spacing)  
        y = row * (obstacle_height + spacing)  
        obstacle = Obstacle(x, y, obstacle_width, obstacle_height)
        obstacles.add(obstacle)
        


def create_level_from_layout(layout, spacing, obstacle_class, obstacle_width, obstacle_height):
    obstacles = pygame.sprite.Group()
    
    # Iterate over the layout to place obstacles
    for row_idx, row in enumerate(layout):
        for col_idx, cell in enumerate(row):
            if cell == 1: 
                x = col_idx * (obstacle_width + spacing)
                y = row_idx * (obstacle_height + spacing)
                              
                obstacle_instance = obstacle_class(x, y, obstacle_width, obstacle_height)
                
                # Add the obstacle to the group
                obstacles.add(obstacle_instance)
    
    return obstacles


def is_level_complete(current_level):
    for row in levels:
        if 0 in row:
            return False
    return True

def all_enemies_defeated():
   
    if len(enemy_tanks) == 0:
        return True
    return False



# Example after moving to the next level:
def load_next_level():
    global current_level, obstacles, player_position
    
    if not isinstance(current_level, int):
        print(f"Error: current_level is not an integer, it is {type(current_level)}")
        current_level = 0 
  
    if current_level < len(levels): 
        current_level_layout = levels[current_level]  
    else:
        print(f"Error: current_level {current_level} is out of bounds.")
        current_level_layout = levels[0]  
    obstacles = create_level_from_layout(current_level_layout, spacing, Obstacle, 48, 34)
    
    
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        pygame.mixer.Sound.play(explosion_sound)
        self.image = pygame.image.load(object2_path)  
        self.rect = self.image.get_rect(center=(x, y))
        self.lifetime = 1000 # Time in milliseconds the explosion lasts
        self.timer = pygame.time.get_ticks()

    def update(self):
        
        current_time = pygame.time.get_ticks()
        if current_time - self.timer > self.lifetime:
            self.kill()
# Function to generate more random positions if there aren't enough
def generate_random_position():
    return (random.randint(0, SCREEN_WIDTH - 40), random.randint(0, SCREEN_HEIGHT - 40))

# Draw a button with a label
def draw_button(screen, rect, label):
    pygame.draw.rect(screen, (0, 0, 0), rect, 5)  
    pygame.draw.rect(screen, (211, 211, 211), rect)
    font = pygame.font.SysFont(None, 0)  # Set font
    text = font.render(label, True, (211, 211, 211)) 
    text_rect = text.get_rect(center=rect.center)  
    screen.blit(text, text_rect) 
def initialize_game():
    global player_tank, enemy_tanks, bullets, enemy_bullets, explosions, all_sprites

   
    player_start_position = player_start_positions.get(current_level, (100, 570))  
    player_tank = PlayerTank(*player_start_position)  
    # Initialize sprite groups
    enemy_tanks = pygame.sprite.Group() 
    bullets = pygame.sprite.Group() 
    enemy_bullets = pygame.sprite.Group() 
    explosions = pygame.sprite.Group() 
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player_tank)
    enemy_positions_list = enemy_positions_by_level.get(current_level, [])

    # Determine the number of enemies to spawn; should spawn at least 'current_level' enemies
    num_enemies = max(current_level, len(enemy_positions_list))  

    for i in range(num_enemies):
        if i < len(enemy_positions_list):
          
            pos = enemy_positions_list[i]
        else:
           
            pos = generate_random_position()

       
        enemy_tank = EnemyTank(pos[0], pos[1])  
        enemy_tanks.add(enemy_tank)  
        all_sprites.add(enemy_tank)  

    
    
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        # Handle keyboard input
        if event.type == pygame.KEYDOWN:
            handle_keydown(event)
        if event.type == pygame.KEYUP:
            handle_keyup(event)
        
       
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_button_down(event)
        if event.type == pygame.MOUSEBUTTONUP:
            handle_mouse_button_up(event)

    return True
def handle_keydown(event):
    global direction
    player_tank.tankx_change = 0
    player_tank.tanky_change = 0

    
    if event.key == pygame.K_LEFT:
        direction = 3  # Left direction
        player_tank.tankx_change = -player_tank.speed  # Move left
    elif event.key == pygame.K_RIGHT:
        direction = 1  # Right direction
        player_tank.tankx_change = player_tank.speed  # Move right
    elif event.key == pygame.K_UP:
        direction = 0  # Up direction
        player_tank.tanky_change = -player_tank.speed  # Move up
    elif event.key == pygame.K_DOWN:
        direction = 2  # Down direction
        player_tank.tanky_change = player_tank.speed  # Move down
    elif event.key == pygame.K_SPACE:
        player_tank.direction = direction  
        player_tank.shoot()  

    # Update the tank's direction immediately for visual feedback
    player_tank.direction = direction
             

def handle_keyup(event):
    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
        player_tank.tankx_change = 0  
    elif event.key in (pygame.K_UP, pygame.K_DOWN):
        player_tank.tanky_change = 0  
def handle_mouse_button_down(event):
    global direction
    if controls['Left'].collidepoint(event.pos):
        direction = 3
        player_tank.tankx_change = -player_tank.speed  # Move left
        player_tank.tanky_change = 0
    elif controls['Right'].collidepoint(event.pos):
        direction = 1
        player_tank.tankx_change = player_tank.speed  # Move right
        player_tank.tanky_change = 0
    elif controls['Up'].collidepoint(event.pos):
        direction = 0
        player_tank.tankx_change = 0
        player_tank.tanky_change = -player_tank.speed  # Move up
    elif controls['Down'].collidepoint(event.pos):
        direction = 2
        player_tank.tankx_change = 0
        player_tank.tanky_change = player_tank.speed  # Move down
    elif controls['Fire'].collidepoint(event.pos):
        player_tank.direction = direction
        player_tank.shoot()  # Fire weapon

def handle_mouse_button_up(event):
    
    player_tank.tankx_change = 0
    player_tank.tanky_change = 0

def update_game_objects(player_tank, tankx_change,tanky_change ):
    player_tank.rect.x += player_tank.tankx_change  
    player_tank.rect.y += player_tank.tanky_change  
    bullets.update()
    enemy_tanks.update()
    enemy_bullets.update()
    explosions.update()
    items.update()
    obstacles.update()
    player_tank.update()
       

def check_collisions():
    for bullet in bullets:
        enemy_tank = pygame.sprite.spritecollideany(bullet, enemy_tanks)
        if enemy_tank:
            enemy_tank.take_damage(bullet.damage)
            bullet.kill()
            if not enemy_tank.alive():
                explosion = Explosion(enemy_tank.rect.centerx, enemy_tank.rect.centery)
                explosions.add(explosion)

    for bullet in enemy_bullets:
        if pygame.sprite.spritecollideany(bullet, pygame.sprite.Group(player_tank)):
            player_tank.take_damage(20)
            bullet.kill()

        if not player_tank.alive():
            explosion = Explosion(player_tank.rect.centerx, player_tank.rect.centery)
            explosions.add(explosion)
              
def render():
    screen.blit(batt, (0,0)) 
          
    #screen.fill((255,255,255))
    screen.blit(player_tank.image, player_tank.rect)
    player_tank.draw_health_bar(screen)
    bullets.draw(screen)
    enemy_tanks.draw(screen)
    enemy_bullets.draw(screen)
    obstacles.draw(screen) 
    explosions.draw(screen)
    power_ups.draw(screen)
    items.draw(screen)  

    for item in pygame.sprite.spritecollide(player_tank, items, True):
        item.apply(player_tank)

    for power_up in power_ups:
        if pygame.sprite.collide_rect(player_tank, power_up):
            if power_up.item_type == 'weapon':
                player_tank.super_weapon = True
            player_tank.super_weapon_timer = pygame.time.get_ticks()

    for enemy in enemy_tanks.sprites():
        enemy.draw_health_bar(screen)

    
    for label, rect in controls.items():
        draw_button(screen, rect, label.capitalize())
           
def main_game():
    global game_state, current_level 
    global tankx_change, tanky_change, direction, item_spawn_time
    game_state = PLAYING
    max_level = 5
    
    tankx_change = 0
    tanky_change = 0
    direction = 0    
    item_spawn_time = pygame.time.get_ticks()  

    initialize_game()
    super_weapon_mode = True
    
    running = True
    while game_state == PLAYING:
        running = handle_events()
        
        
        if not running:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(current_level)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.is_clicked(event):
                    pause_game()
        
        update_game_objects(player_tank, tankx_change, tanky_change)  
        running = running and check_collisions()
        render()

        if player_tank.health <= 0:  
            game_over_screen()
           
            break
        
        # Spawn items at regular intervals
        current_time = pygame.time.get_ticks()
        if current_time - item_spawn_time > item_spawn_interval:
            spawn_item()
            item_spawn_time = current_time
        
        if all_enemies_defeated():
           handle_level_complete()
           current_level += 1 
           if current_level > max_level:
                break
           
       
        pygame.display.update()
    clock.tick(60)

intro()
main_game()
pygame.quit()
sys.exit()

