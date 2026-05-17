import pygame
import random
import sys
import asyncio

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# ── Screen ────────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Destroyer")

# ── Game states  (BUG FIX: PLAYING and PAUSED were both 0) ───────────────────
PLAYING        = "PLAYING"
PAUSED         = "PAUSED"
GAME_OVER      = "GAME_OVER"
LEVEL_COMPLETE = "LEVEL_COMPLETE"
VICTORY        = "VICTORY"

game_state    = PLAYING
current_level = 1
max_level     = 5
score         = 0
direction     = 0          # global facing direction for the player
player_tank   = None       # forward-declare so HUD helper never crashes

# ── Colors ────────────────────────────────────────────────────────────────────
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GREEN      = (0,   200, 0)
RED        = (220, 30,  30)
BLUE       = (0,   80,  200)
YELLOW     = (255, 220, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY  = (30,  30,  30)
CYAN       = (0,   220, 220)
ORANGE     = (255, 140, 0)

# ── Sound helpers  (BUG FIX: missing files crashed the whole game) ────────────
def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception:
        return None

def play_sound(snd):
    if snd:
        try:
            snd.play()
        except Exception:
            pass

gun_sound       = load_sound("gun.mp3")
shot_sound      = load_sound("shot.mp3")
explosion_sound = load_sound("explosion .mp3")
intro_sound     = load_sound("gamestart.ogg")
gameover_sound  = load_sound("gameover.ogg")
bonus_sound     = load_sound("bonus.ogg")
next_sound      = load_sound("Button.mp3")
levelup_sound   = load_sound("Level Up.mp3")
vic_sound       = load_sound("victory.mp3")

play_sound(intro_sound)

# ── Image helpers ─────────────────────────────────────────────────────────────
def load_image(path, size=None, fallback_size=(40, 40), fallback_color=(0, 180, 0)):
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except Exception:
        surf = pygame.Surface(fallback_size if not size else size, pygame.SRCALPHA)
        surf.fill(fallback_color)
        return surf

playertank_up_image    = load_image("green.png")
playertank_down_image  = load_image("greenD.png")
playertank_left_image  = load_image("greenR.png")
playertank_right_image = load_image("greenL.png")
enemy_up_image    = load_image("Up.png",    fallback_color=(180, 20, 20))
enemy_down_image  = load_image("Down.png",  fallback_color=(180, 20, 20))
enemy_left_image  = load_image("Left.png",  fallback_color=(180, 20, 20))
enemy_right_image = load_image("Right.png", fallback_color=(180, 20, 20))

intro_image = load_image("intro_image.png", size=(SCREEN_WIDTH, SCREEN_HEIGHT), fallback_color=(10,10,30))
LVL_image   = load_image("Next.png",        size=(SCREEN_WIDTH, SCREEN_HEIGHT), fallback_color=(10,30,10))
ovr_image   = load_image("ovr.png",         size=(SCREEN_WIDTH, SCREEN_HEIGHT), fallback_color=(30,10,10))
vic_image   = load_image("vic.png",         size=(SCREEN_WIDTH, SCREEN_HEIGHT), fallback_color=(20,20,10))
batt_image  = load_image("battle.png",      size=(SCREEN_WIDTH, SCREEN_HEIGHT), fallback_color=(20,35,20))

try:
    pygame.display.set_icon(pygame.image.load("Destroyer.png"))
except Exception:
    pass

# ── Power-up overlays ─────────────────────────────────────────────────────────
shield_surf = pygame.Surface((52, 52), pygame.SRCALPHA)
pygame.draw.circle(shield_surf, (0, 120, 255, 140), (26, 26), 26)
pygame.draw.circle(shield_surf, (120, 200, 255, 100), (26, 26), 23, 3)

super_weapon_surf = pygame.Surface((52, 52), pygame.SRCALPHA)
pygame.draw.rect(super_weapon_surf, (255, 60, 0, 110), (0, 0, 52, 52), border_radius=6)

plus_speed_surf = pygame.Surface((52, 52), pygame.SRCALPHA)
pygame.draw.polygon(plus_speed_surf, (255, 220, 0, 140),
                    [(26, 2), (50, 50), (26, 37), (2, 50)])

# ── Item spawn timing ─────────────────────────────────────────────────────────
item_spawn_time     = pygame.time.get_ticks()
item_spawn_interval = 10000  # ms

# ── Sprite groups ─────────────────────────────────────────────────────────────
bullets       = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
items         = pygame.sprite.Group()
explosions    = pygame.sprite.Group()
enemy_tanks   = pygame.sprite.Group()
all_sprites   = pygame.sprite.Group()
obstacles     = pygame.sprite.Group()

# ── Fonts ─────────────────────────────────────────────────────────────────────
def try_font(path, size):
    try:
        return pygame.font.Font(path, size)
    except Exception:
        return pygame.font.SysFont("Arial", size, bold=True)

font        = try_font("Minecraft.ttf", 28)
hud_font    = try_font("Minecraft.ttf", 18)
big_font    = try_font("Minecraft.ttf", 38)
button_font = try_font("Minecraft.ttf", 22)
small_font  = try_font("Minecraft.ttf", 14)

# ── Level layouts ─────────────────────────────────────────────────────────────
level_1 = [[1,0,1,0,1,1],[1,1,0,1,0,1],[1,0,1,0,1,1],[1,1,0,1,0,1],[1,0,1,0,1,1]]
level_2 = [[1,1,1,1,1,1],[1,1,0,1,0,1],[1,0,1,0,0,1],[1,0,0,1,0,1],[1,1,1,1,1,1]]
level_3 = [[1,1,1,1,1,1],[1,0,1,0,1,0],[1,1,0,1,1,1],[1,1,1,0,1,0],[1,1,0,1,1,1]]
level_4 = [[1,1,1,1,1,1],[1,1,1,1,0,1],[1,0,1,0,1,1],[1,1,1,0,1,1],[1,1,1,1,1,1]]
level_5 = [[1,1,1,1,1,1],[1,0,1,1,0,1],[1,1,1,0,1,1],[1,0,1,1,0,1],[1,1,1,1,1,1]]

levels = {1: level_1, 2: level_2, 3: level_3, 4: level_4, 5: level_5}

player_start_positions = {
    1: (400, 300),
    2: (50,  75),
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

spacing         = 100
obstacle_width  = 48
obstacle_height = 34

# ── Android control rects (off-screen on desktop — won't interfere) ───────────
button_size = 70
ctrl_rects = {
    'Left':  pygame.Rect(30,  SCREEN_HEIGHT+140, button_size, button_size),
    'Right': pygame.Rect(170, SCREEN_HEIGHT+140, button_size, button_size),
    'Up':    pygame.Rect(100, SCREEN_HEIGHT+80,  button_size, button_size),
    'Down':  pygame.Rect(100, SCREEN_HEIGHT+200, button_size, button_size),
    'Fire':  pygame.Rect(620, SCREEN_HEIGHT+140, button_size, button_size),
}

# ─────────────────────────────────────────────────────────────────────────────
#  UI HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def draw_text_shadow(surf, text, fnt, color, shadow_color, x, y, center=False):
    shadow = fnt.render(text, True, shadow_color)
    main   = fnt.render(text, True, color)
    if center:
        r = main.get_rect(center=(x, y))
        surf.blit(shadow, (r.x + 2, r.y + 2))
        surf.blit(main, r)
    else:
        surf.blit(shadow, (x + 2, y + 2))
        surf.blit(main,   (x,     y))

def draw_panel(surf, rect, color=(15, 15, 15), border=(90, 90, 90),
               alpha=180, radius=10):
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, (*color, alpha),  (0, 0, rect.width, rect.height), border_radius=radius)
    pygame.draw.rect(panel, (*border, 210),   (0, 0, rect.width, rect.height), 2, border_radius=radius)
    surf.blit(panel, rect.topleft)

def draw_bar(surf, x, y, w, h, value, max_value, fg, bg=(80, 0, 0)):
    filled = int(w * max(0, value) / max_value)
    pygame.draw.rect(surf, bg,              (x, y, w, h), border_radius=4)
    if filled:
        pygame.draw.rect(surf, fg,          (x, y, filled, h), border_radius=4)
    pygame.draw.rect(surf, (180, 180, 180), (x, y, w, h), 1, border_radius=4)

def dark_overlay(alpha=140):
    o = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    o.fill((0, 0, 0, alpha))
    screen.blit(o, (0, 0))

# ─────────────────────────────────────────────────────────────────────────────
#  BUTTON  (BUG FIX: sound was played in __init__; action was gated on sound
#           return value which is always truthy but structure was wrong)
# ─────────────────────────────────────────────────────────────────────────────
class Button:
    def __init__(self, text, x, y, width, height,
                 color=BLACK, hover_color=LIGHT_GRAY, action=None):
        self.text        = text
        self.rect        = pygame.Rect(x, y, width, height)
        self.color       = color
        self.hover_color = hover_color
        self.action      = action

    def draw(self):
        hovered  = self.rect.collidepoint(pygame.mouse.get_pos())
        col      = self.hover_color if hovered else self.color
        border_c = YELLOW if hovered else (110, 110, 110)

        # soft shadow
        pygame.draw.rect(screen, (0, 0, 0),   self.rect.move(3, 3), border_radius=9)
        pygame.draw.rect(screen, col,          self.rect,            border_radius=9)
        pygame.draw.rect(screen, border_c,     self.rect, 2,         border_radius=9)

        txt = button_font.render(self.text, True, WHITE)
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def is_clicked(self, event, _arg=None):
        if (event.type == pygame.MOUSEBUTTONDOWN and
                event.button == 1 and
                self.rect.collidepoint(event.pos)):
            play_sound(next_sound)
            if self.action:
                self.action()
            return True
        return False

# ─────────────────────────────────────────────────────────────────────────────
#  FORWARD-DECLARED CALLBACKS  (defined before buttons that reference them)
# ─────────────────────────────────────────────────────────────────────────────
def quit_game():
    pygame.quit()
    sys.exit()

def back_to_intro():
    intro()

def reset_all_groups():
    global bullets, enemy_bullets, items, explosions, enemy_tanks, all_sprites
    for g in (bullets, enemy_bullets, items, explosions, enemy_tanks, all_sprites):
        g.empty()

def play_again():
    global current_level, score
    current_level = 1
    score         = 0
    reset_all_groups()
    load_next_level()
    main_game()

def show_controls():
    controls_screen()

# ── Button dimensions ─────────────────────────────────────────────────────────
BW = 210
BH = 52
BX = SCREEN_WIDTH // 2 - BW // 2

# Shared button instances
start_btn      = Button("Start",      BX, SCREEN_HEIGHT//2 - 65, BW, BH, (20,70,20),  (40,120,40), lambda: _start_game())
controls_btn   = Button("Controls",   BX, SCREEN_HEIGHT//2 +  5, BW, BH, (20,20,70),  (40,40,120), show_controls)
quit_btn       = Button("Quit",       BX, SCREEN_HEIGHT//2 + 75, BW, BH, (70,20,20),  (120,40,40), quit_game)
play_again_btn = Button("Play Again", BX, SCREEN_HEIGHT//2 + 20, BW, BH, (20,70,20),  (40,120,40), play_again)
main_menu_btn  = Button("Main Menu",  BX, SCREEN_HEIGHT//2 + 85, BW, BH, (70,20,20),  (120,40,40), back_to_intro)
next_lvl_btn   = Button("Next Level", BX, SCREEN_HEIGHT//2 + 20, BW, BH, (20,70,20),  (40,120,40))  # action set later
resume_btn     = Button("Resume",     BX, SCREEN_HEIGHT//2 - 35, BW, BH, (20,70,20),  (40,120,40))
menu_btn_p     = Button("Main Menu",  BX, SCREEN_HEIGHT//2 + 35, BW, BH, (70,20,20),  (120,40,40), back_to_intro)

def _start_game():
    global current_level, score
    current_level = 1
    score         = 0
    load_next_level()
    main_game()

# ─────────────────────────────────────────────────────────────────────────────
#  SCREENS
# ─────────────────────────────────────────────────────────────────────────────
def intro():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            start_btn.is_clicked(event)
            controls_btn.is_clicked(event)
            quit_btn.is_clicked(event)

        screen.blit(intro_image, (0, 0))
        dark_overlay(100)

        draw_text_shadow(screen, "TANK DESTROYER", big_font, YELLOW, (80, 60, 0),
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 145, center=True)
        draw_text_shadow(screen, "v2.0", small_font, (180, 180, 180), DARK_GRAY,
                         SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 110, center=True)

        start_btn.draw()
        controls_btn.draw()
        quit_btn.draw()

        pygame.display.flip()
        clock.tick(60)


def controls_screen():
    back_btn = Button("Back", BX, SCREEN_HEIGHT // 2 + 160, BW, BH,
                      (20, 20, 70), (40, 40, 120), back_to_intro)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            back_btn.is_clicked(event)

        screen.blit(intro_image, (0, 0))
        dark_overlay(150)

        panel = pygame.Rect(SCREEN_WIDTH // 2 - 310, 70, 620, 380)
        draw_panel(screen, panel, radius=14)

        draw_text_shadow(screen, "CONTROLS", big_font, YELLOW, (80, 60, 0),
                         SCREEN_WIDTH // 2, 105, center=True)

        rows = [
            ("Keyboard", font,     CYAN),
            ("Arrow Keys  →  Move",          hud_font, WHITE),
            ("Space       →  Shoot",         hud_font, WHITE),
            ("Escape      →  Pause",         hud_font, WHITE),
            ("",          None,     None),
            ("Mobile",    font,     CYAN),
            ("D-pad buttons  →  Move",       hud_font, WHITE),
            ("Fire button    →  Shoot",      hud_font, WHITE),
            ("",          None,     None),
            ("Power-Ups", font,     CYAN),
            ("Shield  -  blocks all damage for 5 s",   hud_font, WHITE),
            ("Speed   -  +2 speed for 5 s",             hud_font, WHITE),
            ("Super   -  heavy bullet for 5 s",         hud_font, WHITE),
            ("Health  -  +25 HP",                       hud_font, WHITE),
        ]
        y = 148
        for text, fnt, col in rows:
            if fnt is None:
                y += 8
                continue
            draw_text_shadow(screen, text, fnt, col, DARK_GRAY,
                             SCREEN_WIDTH // 2, y, center=True)
            y += fnt.get_height() + 4

        back_btn.draw()
        pygame.display.flip()
        clock.tick(60)


def pause_game():
    global game_state
    game_state = PAUSED

    def _resume():
        global game_state
        game_state = PLAYING

    resume_btn.action  = _resume
    menu_btn_p.action  = back_to_intro

    while game_state == PAUSED:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                _resume()
            resume_btn.is_clicked(event)
            menu_btn_p.is_clicked(event)

        dark_overlay(165)
        draw_panel(screen, pygame.Rect(SCREEN_WIDTH//2-160, SCREEN_HEIGHT//2-80, 320, 180))
        draw_text_shadow(screen, "PAUSED", big_font, YELLOW, DARK_GRAY,
                         SCREEN_WIDTH//2, SCREEN_HEIGHT//2-55, center=True)
        resume_btn.draw()
        menu_btn_p.draw()
        pygame.display.flip()
        clock.tick(30)


def game_over_screen():
    global game_state
    play_sound(gameover_sound)
    game_state = GAME_OVER

    while game_state == GAME_OVER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            play_again_btn.is_clicked(event)
            main_menu_btn.is_clicked(event)

        screen.blit(ovr_image, (0, 0))
        dark_overlay(90)

        draw_text_shadow(screen, "GAME OVER", big_font, RED, (80, 0, 0),
                         SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100, center=True)
        draw_text_shadow(screen, f"Final Score: {score}", font, YELLOW, DARK_GRAY,
                         SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 55, center=True)

        play_again_btn.draw()
        main_menu_btn.draw()
        pygame.display.flip()
        clock.tick(60)


def victory_screen():
    global game_state
    play_sound(vic_sound)
    game_state = VICTORY

    while game_state == VICTORY:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            play_again_btn.is_clicked(event)
            main_menu_btn.is_clicked(event)

        screen.blit(vic_image, (0, 0))
        dark_overlay(90)

        draw_text_shadow(screen, "VICTORY!", big_font, YELLOW, (80, 60, 0),
                         SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100, center=True)
        draw_text_shadow(screen, f"Final Score: {score}", font, CYAN, DARK_GRAY,
                         SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 55, center=True)
        draw_text_shadow(screen, "All levels cleared!", hud_font, WHITE, DARK_GRAY,
                         SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20, center=True)

        play_again_btn.draw()
        main_menu_btn.draw()
        pygame.display.flip()
        clock.tick(60)


def level_complete_screen():
    global game_state, current_level
    play_sound(levelup_sound)
    game_state = LEVEL_COMPLETE

    def _next():
        global current_level, game_state
        current_level += 1
        if current_level > max_level:
            victory_screen()
        else:
            game_state = PLAYING
            load_next_level()
            main_game()

    next_lvl_btn.action = _next

    while game_state == LEVEL_COMPLETE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            next_lvl_btn.is_clicked(event)
            main_menu_btn.is_clicked(event)

        screen.blit(LVL_image, (0, 0))
        dark_overlay(90)

        draw_text_shadow(screen, f"LEVEL {current_level} COMPLETE!", big_font,
                         YELLOW, (80, 60, 0), SCREEN_WIDTH//2, SCREEN_HEIGHT//2-110, center=True)
        draw_text_shadow(screen, f"Score: {score}", font, WHITE, DARK_GRAY,
                         SCREEN_WIDTH//2, SCREEN_HEIGHT//2-60, center=True)

        next_lvl_btn.draw()
        main_menu_btn.draw()
        pygame.display.flip()
        clock.tick(60)

# ─────────────────────────────────────────────────────────────────────────────
#  SPRITES
# ─────────────────────────────────────────────────────────────────────────────
class PlayerTank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = {
            0: playertank_up_image,
            1: playertank_right_image,
            2: playertank_down_image,
            3: playertank_left_image,
        }
        self.direction    = 0
        self.image        = self.images[0]
        self.rect         = self.image.get_rect(topleft=(x, y))
        self.tankx_change = 0
        self.tanky_change = 0
        self.health       = 100
        self.speed        = 3

        # power-up flags
        self.shield              = False
        self.shield_timer        = 0
        self.super_weapon        = False
        self.super_weapon_timer  = 0
        self.plus_speed          = False
        self.plus_speed_timer    = 0

        self.shoot_delay         = 350   # ms between shots
        self.last_shot_time      = 0
        self.max_active_bullets  = 6

    def update(self):
        prev = self.rect.topleft
        self.rect.x += self.tankx_change
        self.rect.y += self.tanky_change
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        if pygame.sprite.spritecollide(self, obstacles, False):
            self.rect.topleft = prev

        # update facing direction
        if   self.tankx_change < 0: self.direction = 3
        elif self.tankx_change > 0: self.direction = 1
        elif self.tanky_change < 0: self.direction = 0
        elif self.tanky_change > 0: self.direction = 2
        self.image = self.images[self.direction]

        # expire power-ups
        now = pygame.time.get_ticks()
        if self.shield       and now - self.shield_timer       > 5000: self.shield       = False
        if self.super_weapon and now - self.super_weapon_timer > 5000: self.super_weapon = False
        if self.plus_speed   and now - self.plus_speed_timer   > 5000:
            self.plus_speed = False
            self.speed = max(3, self.speed - 2)

    def draw_overlays(self, surf):
        cx, cy = self.rect.center
        if self.shield:
            r = shield_surf.get_rect(center=(cx, cy))
            surf.blit(shield_surf, r)
        if self.super_weapon:
            r = super_weapon_surf.get_rect(center=(cx, cy))
            surf.blit(super_weapon_surf, r)
        if self.plus_speed:
            r = plus_speed_surf.get_rect(center=(cx, cy))
            surf.blit(plus_speed_surf, r)

    def draw_health_bar(self, surf):
        bw = self.rect.width
        by = self.rect.y - 10
        draw_bar(surf, self.rect.x, by, bw, 6,
                 self.health, 100, (0, 210, 0))

    def take_damage(self, amount):
        if not self.shield:
            self.health = max(0, self.health - amount)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shoot_delay and len(bullets) < self.max_active_bullets:
            cls = SuperBullet if self.super_weapon else PlayerBullet
            b = cls(self.rect.centerx, self.rect.centery, self.direction)
            bullets.add(b)
            self.last_shot_time = now


class EnemyTank(pygame.sprite.Sprite):
    UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3

    def __init__(self, x, y):
        super().__init__()
        self.images = {
            0: enemy_up_image,
            1: enemy_right_image,
            2: enemy_down_image,
            3: enemy_left_image,
        }
        self.direction    = random.randint(0, 3)
        self.image        = self.images[self.direction]
        self.rect         = self.image.get_rect(topleft=(x, y))
        self.speed        = 2
        self.health       = 100
        self.shoot_delay  = 1400
        self.shoot_range  = 280
        self.shoot_timer  = pygame.time.get_ticks() + random.randint(0, 1000)
        self.patrol_timer = pygame.time.get_ticks()
        self.patrol_delay = 1100 + random.randint(0, 600)

    def draw_health_bar(self, surf):
        bw = self.rect.width
        by = self.rect.y + self.rect.height + 4
        draw_bar(surf, self.rect.x, by, bw, 5,
                 self.health, 100, (220, 30, 30), (80, 0, 0))

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def update(self):
        now = pygame.time.get_ticks()

        # patrol: change direction periodically
        if now - self.patrol_timer > self.patrol_delay:
            self.direction    = random.randint(0, 3)
            self.patrol_timer = now
            self.patrol_delay = 900 + random.randint(0, 700)

        # aim & shoot at player when close
        if player_tank and player_tank.alive():
            dx = player_tank.rect.centerx - self.rect.centerx
            dy = player_tank.rect.centery - self.rect.centery
            dist = (dx*dx + dy*dy) ** 0.5
            if dist < self.shoot_range:
                if abs(dx) > abs(dy):
                    self.direction = self.RIGHT if dx > 0 else self.LEFT
                else:
                    self.direction = self.DOWN if dy > 0 else self.UP
                if now - self.shoot_timer > self.shoot_delay:
                    self.shoot_timer = now
                    b = EnemyBullet(self.rect.centerx, self.rect.centery, self.direction)
                    enemy_bullets.add(b)

        # move
        prev = self.rect.topleft
        dx2, dy2 = [(0,-self.speed),(self.speed,0),(0,self.speed),(-self.speed,0)][self.direction]
        self.rect.x += dx2
        self.rect.y += dy2
        self.image = self.images[self.direction]

        if pygame.sprite.spritecollide(self, obstacles, False):
            self.rect.topleft = prev
            self.direction = random.randint(0, 3)

        # wall bounce
        if self.rect.top    <= 0:            self.rect.top    = 0;             self.direction = random.choice([1,2])
        if self.rect.bottom >= SCREEN_HEIGHT: self.rect.bottom = SCREEN_HEIGHT; self.direction = random.choice([0,1])
        if self.rect.left   <= 0:            self.rect.left   = 0;             self.direction = random.choice([1,2])
        if self.rect.right  >= SCREEN_WIDTH:  self.rect.right  = SCREEN_WIDTH;  self.direction = random.choice([0,3])


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, color, speed, damage):
        super().__init__()
        self.damage  = damage
        self.speed_x = 0
        self.speed_y = 0

        # oriented rectangle
        if direction in (0, 2):
            w, h = 6, 18
        else:
            w, h = 18, 6
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, w, h), border_radius=3)
        self.rect = self.image.get_rect()

        offsets = {
            0: (x, y, 0,      -speed),
            1: (x, y, speed,  0),
            2: (x, y, 0,       speed),
            3: (x, y, -speed, 0),
        }
        ox, oy, self.speed_x, self.speed_y = offsets[direction]
        self.rect.center = (ox, oy)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if pygame.sprite.spritecollide(self, obstacles, False):
            self.kill()
        if not pygame.Rect(-20, -20, SCREEN_WIDTH+40, SCREEN_HEIGHT+40).colliderect(self.rect):
            self.kill()


class PlayerBullet(Bullet):
    def __init__(self, x, y, direction):
        play_sound(gun_sound)
        super().__init__(x, y, direction, (255, 240, 60), 7, 20)


class SuperBullet(Bullet):
    def __init__(self, x, y, direction):
        play_sound(shot_sound)
        super().__init__(x, y, direction, (255, 60, 0), 13, 40)


class EnemyBullet(Bullet):
    def __init__(self, x, y, direction):
        play_sound(gun_sound)
        super().__init__(x, y, direction, (20, 20, 20), 5, 20)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        try:
            self.image = pygame.image.load("block.png").convert_alpha()
        except Exception:
            self.image = pygame.Surface((width, height))
            self.image.fill((110, 75, 35))
        self.rect = self.image.get_rect(topleft=(x, y))


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        play_sound(explosion_sound)
        try:
            raw = pygame.image.load("explode.png").convert_alpha()
            self.image = raw.copy()
            self._base = raw
        except Exception:
            s = pygame.Surface((44, 44), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 120, 0, 220), (22, 22), 22)
            self.image = s
            self._base = s.copy()
        self.rect     = self.image.get_rect(center=(x, y))
        self.timer    = pygame.time.get_ticks()
        self.lifetime = 550

    def update(self):
        elapsed = pygame.time.get_ticks() - self.timer
        if elapsed >= self.lifetime:
            self.kill()
        else:
            alpha = max(0, 255 - int(255 * elapsed / self.lifetime))
            self.image = self._base.copy()
            self.image.set_alpha(alpha)


class Item(pygame.sprite.Sprite):
    IMAGES = {
        'shield':       'shield.png',
        'super_weapon': 'bullet.png',
        'plus_health':  'health.png',
        'plus_speed':   'speed.png',
    }
    FALLBACK_COLORS = {
        'shield':       (0,   100, 220),
        'super_weapon': (220,  40,  20),
        'plus_health':  (20,  200,  20),
        'plus_speed':   (220, 200,   0),
    }

    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        try:
            self.image = pygame.image.load(self.IMAGES[item_type]).convert_alpha()
        except Exception:
            self.image = pygame.Surface((26, 26), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (*self.FALLBACK_COLORS[item_type], 220), (13, 13), 13)
        self.rect          = self.image.get_rect(topleft=(x, y))
        self._spawn_time   = pygame.time.get_ticks()
        self._lifetime     = 12000  # disappear after 12 s

    def update(self):
        if pygame.time.get_ticks() - self._spawn_time > self._lifetime:
            self.kill()

    def apply(self, player):
        play_sound(bonus_sound)
        if self.item_type == 'shield':
            player.shield       = True
            player.shield_timer = pygame.time.get_ticks()
        elif self.item_type == 'super_weapon':
            player.super_weapon       = True
            player.super_weapon_timer = pygame.time.get_ticks()
        elif self.item_type == 'plus_health':
            player.health = min(100, player.health + 25)
        elif self.item_type == 'plus_speed':
            if not player.plus_speed:
                player.speed            += 2
                player.plus_speed        = True
                player.plus_speed_timer  = pygame.time.get_ticks()
        self.kill()


def spawn_item():
    t = random.choices(
        ['shield', 'super_weapon', 'plus_health', 'plus_speed'],
        [0.25,     0.10,           0.30,           0.35]
    )[0]
    x = random.randint(40, SCREEN_WIDTH  - 40)
    y = random.randint(50, SCREEN_HEIGHT - 40)
    items.add(Item(x, y, t))

# ─────────────────────────────────────────────────────────────────────────────
#  LEVEL LOADING
# ─────────────────────────────────────────────────────────────────────────────
def create_obstacles_from_layout(layout):
    grp = pygame.sprite.Group()
    for r, row in enumerate(layout):
        for c, cell in enumerate(row):
            if cell == 1:
                grp.add(Obstacle(
                    c * (obstacle_width  + spacing),
                    r * (obstacle_height + spacing),
                    obstacle_width, obstacle_height
                ))
    return grp


def load_next_level():
    """Reset all sprite groups and build the current level."""
    global obstacles, player_tank, enemy_tanks, bullets, enemy_bullets
    global explosions, items, all_sprites

    layout    = levels.get(current_level, level_1)
    obstacles = create_obstacles_from_layout(layout)

    start_pos   = player_start_positions.get(current_level, (100, 300))
    player_tank = PlayerTank(*start_pos)

    enemy_tanks   = pygame.sprite.Group()
    bullets       = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    explosions    = pygame.sprite.Group()
    items         = pygame.sprite.Group()
    all_sprites   = pygame.sprite.Group()
    all_sprites.add(player_tank)

    positions    = enemy_positions_by_level.get(current_level, [])
    num_enemies  = max(current_level, len(positions))
    for i in range(num_enemies):
        if i < len(positions):
            pos = positions[i]
        else:
            pos = (random.randint(40, SCREEN_WIDTH-80),
                   random.randint(40, SCREEN_HEIGHT-80))
        et = EnemyTank(*pos)
        enemy_tanks.add(et)
        all_sprites.add(et)

# ─────────────────────────────────────────────────────────────────────────────
#  HUD
# ─────────────────────────────────────────────────────────────────────────────
def draw_hud():
    # top bar
    draw_panel(screen, pygame.Rect(0, 0, SCREEN_WIDTH, 38),
               color=(8, 8, 8), border=(50, 50, 50), alpha=170, radius=0)

    # HP bar
    hp_w = 160
    draw_bar(screen, 10, 9, hp_w, 18, player_tank.health, 100, (0, 210, 0))
    draw_text_shadow(screen, f"HP {player_tank.health}", hud_font, WHITE, DARK_GRAY, 15, 11)

    # Score (center)
    draw_text_shadow(screen, f"SCORE  {score}", hud_font, YELLOW, DARK_GRAY,
                     SCREEN_WIDTH // 2, 10, center=True)

    # Level + enemies (right)
    draw_text_shadow(screen, f"LEVEL {current_level}", hud_font, CYAN, DARK_GRAY,
                     SCREEN_WIDTH - 160, 10)
    draw_text_shadow(screen, f"ENEMIES {len(enemy_tanks)}", hud_font, RED, DARK_GRAY,
                     SCREEN_WIDTH - 160, 24)

    # Power-up timers (bottom-left)
    px, py = 10, SCREEN_HEIGHT - 30
    now = pygame.time.get_ticks()
    if player_tank.shield:
        rem = max(0, 5000 - (now - player_tank.shield_timer))
        draw_text_shadow(screen, f"SHIELD {rem//1000+1}s", hud_font, CYAN, DARK_GRAY, px, py)
        px += 140
    if player_tank.super_weapon:
        rem = max(0, 5000 - (now - player_tank.super_weapon_timer))
        draw_text_shadow(screen, f"SUPER {rem//1000+1}s", hud_font, ORANGE, DARK_GRAY, px, py)
        px += 130
    if player_tank.plus_speed:
        rem = max(0, 5000 - (now - player_tank.plus_speed_timer))
        draw_text_shadow(screen, f"SPEED {rem//1000+1}s", hud_font, YELLOW, DARK_GRAY, px, py)


def draw_mobile_controls():
    for label, rect in ctrl_rects.items():
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (255, 255, 255, 45), (0, 0, rect.width, rect.height), border_radius=10)
        pygame.draw.rect(s, (255, 255, 255, 110),(0, 0, rect.width, rect.height), 2, border_radius=10)
        screen.blit(s, rect.topleft)
        txt = hud_font.render(label, True, WHITE)
        screen.blit(txt, txt.get_rect(center=rect.center))

# ─────────────────────────────────────────────────────────────────────────────
#  INPUT
# ─────────────────────────────────────────────────────────────────────────────
def handle_events():
    global direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        # ── Keyboard ──────────────────────────────────────────────────────────
        if event.type == pygame.KEYDOWN:
            if   event.key == pygame.K_LEFT:
                player_tank.tankx_change = -player_tank.speed
                direction = 3
            elif event.key == pygame.K_RIGHT:
                player_tank.tankx_change =  player_tank.speed
                direction = 1
            elif event.key == pygame.K_UP:
                player_tank.tanky_change = -player_tank.speed
                direction = 0
            elif event.key == pygame.K_DOWN:
                player_tank.tanky_change =  player_tank.speed
                direction = 2
            elif event.key == pygame.K_SPACE:
                player_tank.direction = direction
                player_tank.shoot()
            elif event.key == pygame.K_ESCAPE:
                pause_game()

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player_tank.tankx_change = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                player_tank.tanky_change = 0

        # ── Mouse / touch ──────────────────────────────────────────────────────
        if event.type == pygame.MOUSEBUTTONDOWN:
            p = event.pos
            if   ctrl_rects['Left'].collidepoint(p):
                player_tank.tankx_change = -player_tank.speed; direction = 3
            elif ctrl_rects['Right'].collidepoint(p):
                player_tank.tankx_change =  player_tank.speed; direction = 1
            elif ctrl_rects['Up'].collidepoint(p):
                player_tank.tanky_change = -player_tank.speed; direction = 0
            elif ctrl_rects['Down'].collidepoint(p):
                player_tank.tanky_change =  player_tank.speed; direction = 2
            elif ctrl_rects['Fire'].collidepoint(p):
                player_tank.direction = direction
                player_tank.shoot()

        if event.type == pygame.MOUSEBUTTONUP:
            player_tank.tankx_change = 0
            player_tank.tanky_change = 0

# ─────────────────────────────────────────────────────────────────────────────
#  COLLISIONS  (BUG FIX: previously returned None, causing `running` to be
#               set to False every frame and breaking the game loop)
# ─────────────────────────────────────────────────────────────────────────────
def check_collisions():
    global score

    # Player bullets → enemies
    for bullet in list(bullets):
        hit = pygame.sprite.spritecollideany(bullet, enemy_tanks)
        if hit:
            hit.take_damage(bullet.damage)
            bullet.kill()
            if not hit.alive():
                explosions.add(Explosion(hit.rect.centerx, hit.rect.centery))
                score += 100 * current_level

    # Enemy bullets → player
    for bullet in list(enemy_bullets):
        if player_tank.alive() and player_tank.rect.colliderect(bullet.rect):
            player_tank.take_damage(bullet.damage)
            bullet.kill()

    # Item pickups
    for item in pygame.sprite.spritecollide(player_tank, items, True):
        item.apply(player_tank)

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN GAME LOOP
# ─────────────────────────────────────────────────────────────────────────────
def main_game():
    global game_state, direction, item_spawn_time

    game_state      = PLAYING
    direction       = 0
    item_spawn_time = pygame.time.get_ticks()

    while game_state == PLAYING:
        clock.tick(60)                       # ← BUG FIX: was outside the loop

        handle_events()

        # Update
        player_tank.update()
        bullets.update()
        enemy_tanks.update()
        enemy_bullets.update()
        explosions.update()
        items.update()

        check_collisions()

        # Item spawn
        now = pygame.time.get_ticks()
        if now - item_spawn_time > item_spawn_interval:
            spawn_item()
            item_spawn_time = now

        # ── Render ────────────────────────────────────────────────────────────
        screen.blit(batt_image, (0, 0))

        obstacles.draw(screen)
        items.draw(screen)
        explosions.draw(screen)

        # enemies
        for et in enemy_tanks:
            screen.blit(et.image, et.rect)
            et.draw_health_bar(screen)

        # player
        if player_tank.alive():
            screen.blit(player_tank.image, player_tank.rect)
            player_tank.draw_overlays(screen)
            player_tank.draw_health_bar(screen)

        bullets.draw(screen)
        enemy_bullets.draw(screen)

        draw_hud()
        # draw_mobile_controls()  # uncomment on Android

        pygame.display.flip()

        # ── End-condition checks ──────────────────────────────────────────────
        if player_tank.health <= 0:
            # show death explosion briefly
            pygame.time.delay(350)
            game_over_screen()
            return

        if len(enemy_tanks) == 0:
            level_complete_screen()
            return

# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
async def main():
    intro()
    while True:
        await asyncio.sleep(0)

asyncio.run(main())