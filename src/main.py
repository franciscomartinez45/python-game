#import Pygame
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_sheet):
        super().__init__()
        self.frame_width = 64
        self.frame_height = 64
        self.animations = {
            "idle": self.load_frames(sprite_sheet, row=0, count=4),
            "run": self.load_frames(sprite_sheet, row=3, count=8),  
            "jump": self.load_frames(sprite_sheet, row=5, count=6),  
        }
        self.state = "idle"
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations[self.state][0]
        self.rect = self.image.get_rect(topleft=pos)

    def load_frames(self, sheet, row, count):
        frames = []
        for i in range(count):
            x = i * self.frame_width
            y = row * self.frame_height
            frame = sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
            frames.append(frame)
            

        return frames

    def update(self, dt, dx, dy, on_ground):
        if not on_ground:
            self.state = "jump"
        elif dx != 0:
            self.state = "run"
        else:
            self.state = "idle"

        frames = self.animations[self.state]
        self.frame_index += self.animation_speed * dt * 60  
        if self.frame_index >= len(frames):
            self.frame_index = 0
        self.image = frames[int(self.frame_index)]
        if dx < 0:
            self.image = pygame.transform.flip(frames[int(self.frame_index)], True, False)
        else:
            self.image = frames[int(self.frame_index)]


# pygame setup
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT=980
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
TILE_SIZE = 64





map_data = [
    "######################",  
    ".......................",
    "...............########",
    ".......................",
    ".......................",
    ".....############......",
    ".......................",
    ".......................",
    "#########..................",
    "..................#####",
    ".......................",
    "############......................",
    "........................",
    "........................",
    "########################",
  
] 
sprite_sheet = pygame.image.load("assets/sprite_base_addon_2012_12_14.png").convert_alpha()
grass_sprite = pygame.image.load("assets/stone_wall.jpg").convert_alpha()
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_sprite = Player((player_pos.x, player_pos.y), sprite_sheet)
all_sprites = pygame.sprite.Group(player_sprite)
gravity = 1000        
velocity_y = 0          
jump_strength = -750
dt=0

while running:
    
    screen.fill("black")
    solid_tiles = []
    for row_index, row in enumerate(map_data):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if tile == "#":
                rect = pygame.Rect(x,y,TILE_SIZE, TILE_SIZE)
                sprite = pygame.transform.scale(grass_sprite, (TILE_SIZE, TILE_SIZE))
                solid_tiles.append(rect)
                screen.blit(sprite, (x,y))
            # elif tile == "P":
            #     pygame.draw.circle(screen, "red", player_pos, TILE_SIZE)
            elif tile == "o":
                pygame.draw.circle(screen, "yellow", (x,y), TILE_SIZE)
            elif tile == "G": 
                pygame.draw.rect(screen, "green", (x,y,TILE_SIZE, TILE_SIZE))
          
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   
    # for row in range(2):
    #     for i in range(10):  
    #         x = i * 32
    #         y = row * 32
    #         frame = sprite_sheet.subsurface(pygame.Rect(x, y, 32, 32))
    #         screen.blit(frame, (x, y + 300))  
    
    
    # player_rect = pygame.Rect(player_pos.x,player_pos.y, TILE_SIZE, TILE_SIZE)
    # pygame.draw.rect(screen, "red", player_sprite.rect, 2)
    
    is_on_ground = False
    
    keys = pygame.key.get_pressed()  
    dx,dy = 0,0
    if keys[pygame.K_w]:
        dy -= 300 * dt
    if keys[pygame.K_s]:
        dy += 300 * dt
    if keys[pygame.K_a]:
        dx -= 300 * dt
    if keys[pygame.K_d]:
       dx += 300 * dt
    
    
    player_sprite.rect.x += dx 
    
    for tile in solid_tiles:
        if player_sprite.rect.colliderect(tile):
            if dx > 0:  
                player_sprite.rect.right = tile.left
            elif dx < 0:  
                player_sprite.rect.left = tile.right

    velocity_y += gravity * dt
    dy = velocity_y*dt
    player_sprite.rect.y += dy  
   
    

    for tile in solid_tiles:
        if player_sprite.rect.colliderect(tile):
            if velocity_y>0:  
                player_sprite.rect.bottom = tile.top
                is_on_ground = True
            elif velocity_y<0: 
                player_sprite.rect.top = tile.bottom
            velocity_y=0

    
    if keys[pygame.K_SPACE] and is_on_ground:
        velocity_y = jump_strength 

    player_pos.x = player_sprite.rect.x
    player_pos.y = player_sprite.rect.y
    dy = 0

    player_sprite.rect.topleft = (player_sprite.rect.x, player_sprite.rect.y)
    player_sprite.update(dt, dx, dy, is_on_ground)
    all_sprites.draw(screen)
    dt = clock.tick(60) / 1000
   
    pygame.display.flip()
    # print(player_pos)
    # print(velocity_y)
    # print(dy)
  
  
    

pygame.quit()