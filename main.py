import pygame
import random
import noise

def randomColor():
    r = random.randint(50, 200)
    g = random.randint(50, 200)
    b = random.randint(50, 200)
    return (r, g, b) 

class Player:
    def __init__(self):
        self.level = 1
        self.life = 100
        self.ammo = {
            'normal' : 100,
            'explosive' : 40,
            'ultimatum' : 5,
        }
        self.pos = pygame.Rect(int(map_width*0.5)*tile_size , int(map_height*0.5)*tile_size, tile_size, tile_size)
        self.speed = 300
        self.color = 'black'
        self.size = tile_size/2
        self.true_pos = [int(map_width*0.5),int(map_height*0.5)]
        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))

    def input(self, event):
        if event.type == pygame.KEYDOWN:
            sound_file = "sounds/walking.mp3"
            pygame.mixer.music.load(sound_file)

            if event.key == pygame.K_w:
                pygame.mixer.music.play()

                self.true_pos[1] += 1
                for row in map_data:
                    for tile in row:
                        tile.rect.y += tile_size
                if map_data[0][0].rect.y > 0:
                    print('New row top!')
                    row = []
                    previous_row = map_data[0]
                    y =  self.true_pos[1]
                    for x in range(map_width):
                        value = noise.pnoise2(previous_row[x].x * scale,
                                              y * scale,
                                              octaves=4,
                                              persistence=0.5,
                                              lacunarity=2.0,
                                              repeatx=map_width,
                                              repeaty=map_height,
                                              base=seed)
                        if value < threshold:
                            tile = Tile(previous_row[x].x, y, x * tile_size, 0, tile_size, tile_size, (255, 255, 255), 0)
                        else:
                            tile = Tile(previous_row[x].x, y, x * tile_size, 0, tile_size, tile_size, (255, 255, 255), 1)
                        row.append(tile)
                    map_data.insert(0, row)

            elif event.key == pygame.K_s:
                pygame.mixer.music.play()
                self.true_pos[1] += 1
                for row in map_data:
                    for tile in row:
                        tile.rect.y -= tile_size
                if map_data[-1][0].rect.y < screen_height-tile_size:
                    print('New row bottom!')
                    row = []
                    previous_row = map_data[-1]
                    y =  self.true_pos[1]
                    for x in range(map_width):
                        value = noise.pnoise2(previous_row[x].x * scale,
                                              y * scale,
                                              octaves=4,
                                              persistence=0.5,
                                              lacunarity=2.0,
                                              repeatx=map_width,
                                              repeaty=map_height,
                                              base=seed)
                        if value < threshold:
                            tile = Tile(previous_row[x].x, y, x * tile_size, screen_height - tile_size, tile_size, tile_size, (255, 255, 255), 0)
                        else:
                            tile = Tile(previous_row[x].x, y, x * tile_size, screen_height - tile_size, tile_size, tile_size, (255, 255, 255), 1)
                        row.append(tile)
                    map_data.append(row)

            elif event.key == pygame.K_a:
                pygame.mixer.music.play()
                added_column = False
                self.true_pos[0] -= 1
                for row in map_data:
                    for tile in row:
                        tile.rect.x += tile_size
                    if row[0].rect.x>0:
                        added_column = True
                        x = self.true_pos[0]
                        value = noise.pnoise2(x * scale,
                                              row[0].y * scale,
                                              octaves=4,
                                              persistence=0.5,
                                              lacunarity=2.0,
                                              repeatx=map_width,
                                              repeaty=map_height,
                                              base=seed)
                        if value < threshold:
                            tile = Tile(x, row[0].y, 0, row[0].rect.y, tile_size, tile_size, (255, 255, 255), 0)
                        else:
                            tile = Tile(x, row[0].y, 0, row[0].rect.y, tile_size, tile_size, (255, 255, 255), 1)

                        row.insert(0, tile)

                if added_column:
                    print('New column left!')

            elif event.key == pygame.K_d:
                pygame.mixer.music.play()
                added_column = False
                self.true_pos[0] += 1
                for row in map_data:
                    for tile in row:
                        tile.rect.x -= tile_size
                    if row[-1].rect.x+tile_size<screen_width:
                        added_column = True
                        x = self.true_pos[0]
                        value = noise.pnoise2(x * scale,
                                              row[0].y * scale,
                                              octaves=4,
                                              persistence=0.5,
                                              lacunarity=2.0,
                                              repeatx=map_width,
                                              repeaty=map_height,
                                              base=seed)
                        if value < threshold:
                            tile = Tile(x, row[0].y, screen_width - tile_size, row[0].rect.y, tile_size, tile_size, (255, 255, 255), 0)
                        else:
                            tile = Tile(x, row[0].y, screen_width - tile_size, row[0].rect.y, tile_size, tile_size, (255, 255, 255), 1)

                        row.append(tile)

                if added_column:
                    print('New column right!')
    def update(self, event):
        self.input(event)

    def draw(self, screen):
        #pygame.draw.rect(screen, self.color, self.pos, 1)
        #pygame.draw.circle(screen, self.color, self.pos, self.size)
        screen.blit(self.image, self.pos)

class Tile:
    def __init__(self, true_x, true_y, x, y, width, height, line_color, terrain):
        self.rect = pygame.Rect(x, y, width, height)
        self.line_color = line_color

        if terrain==1:
            self.image = water_texture
        else:
            self.image = grass_texture

        self.x = true_x
        self.y = true_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()
running = True
dt = 0
tile_size = 20


screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

mouse_pos = None

map_width = screen_width//tile_size
map_height = screen_height//tile_size

map_data = []
seed = 80#random.randint(0, 100)
scale = 0.05
threshold = 0.2

grass_texture = pygame.image.load('images/grass.png').convert()
grass_texture= pygame.transform.scale(grass_texture, (tile_size, tile_size))

water_texture = pygame.image.load('images/water.png').convert()
water_texture= pygame.transform.scale(water_texture, (tile_size, tile_size))

for y in range(map_height):
    row = []
    for x in range(map_width):
        value = noise.pnoise2(x * scale,
                              y * scale,
                              octaves=4,
                              persistence=0.5,
                              lacunarity=2.0,
                              repeatx=map_width,
                              repeaty=map_height,
                              base=seed)
        if value < threshold:
            tile = Tile(x, y, x * tile_size, y * tile_size, tile_size, tile_size, (255, 255, 255), 0)
        else:
            tile = Tile(x, y, x * tile_size, y * tile_size, tile_size, tile_size, (255, 255, 255), 1)
        row.append(tile)
    map_data.append(row)

player = Player()
while running:
    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
        player.update(event)

    screen.fill("white")

    for row in map_data:
        for tile in row:
            tile.draw(screen)
            if mouse_pos and tile.rect.x < mouse_pos[0] < tile.rect.x+tile_size and \
            tile.rect.y < mouse_pos[1] < tile.rect.y+tile_size:
                pygame.draw.rect(screen, (0, 0, 0), tile.rect, 1)

    player.draw(screen)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
