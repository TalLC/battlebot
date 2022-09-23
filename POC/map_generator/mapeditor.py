import json
from pathlib import Path

import pygame
import button
import csv
from tkinter import *

"""
Honteuse copie du script de Giovanni Gatto (formazione)
https://github.com/formazione/timecrystals
Adapté en vitesse pour générer les JSON des terrains du battlebot.
"""


def editor():

    def list_tiles() -> list:
        """
            Liste les fichiers JSON (donc les maps) stockées.
        """
        tiles_dir = Path('img/tiles')
        tiles_list = []

        for png_file in tiles_dir.iterdir():
            if png_file.is_file() and png_file.name.endswith('.png'):
                tiles_list.append(png_file.absolute())

        return tiles_list

    def save():
        tiles_list = list_tiles()
        transco = {}
        for i, e in enumerate(tiles_list):
            transco[i] = Path(e).stem

        for items in transco.items():
            print(items)

        _data = []
        for idx, h in enumerate(world_data):
            for idx2, w in enumerate(h):
                t = transco[w].split('_')[0]
                to = transco[w].split('_')[1]
                _data.append(
                    {
                        'tile': t,
                        'tile_object': to,
                        'x': idx,
                        'z': idx2
                    }
                )

        json_content = {
            "name": MAP_NAME,
            "width": COLS,
            "height": ROWS,
            "data": _data
        }

        with open(f"{MAP_NAME}.json", "w") as json_save:
            json.dump(json_content, json_save)

        # save level data
        with open(f'{MAP_NAME}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)

    def load():
        # load in level data
        with open(f'{MAP_NAME}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

        # function for outputting text onto the screen

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

        # create function for drawing background

    def draw_bg():
        screen.fill(WHITE)

        # draw grid

    def draw_grid():
        # vertical lines
        for c in range(COLS + 1):
            pygame.draw.line(screen, WHITE, (c * TILE_SIZE, 0), (c * TILE_SIZE, SCREEN_HEIGHT))
        # horizontal lines
        for c in range(ROWS + 1):
            pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

        # function for drawing the world tiles

    def draw_world():
        for y, row in enumerate(world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    screen.blit(img_list[tile], (x * TILE_SIZE, y * TILE_SIZE))

    def add_new_tiles():
        # get mouse position
        pos = pygame.mouse.get_pos()
        x = (pos[0]) // TILE_SIZE
        y = pos[1] // TILE_SIZE

        # check that the coordinates are within the tile area
        if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
            # update tile value
            if pygame.mouse.get_pressed()[0] == 1:
                if world_data[y][x] != current_tile:
                    world_data[y][x] = current_tile
            if pygame.mouse.get_pressed()[2] == 1:
                world_data[y][x] = -1

    pygame.init()

    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    print(f"w : {width} h : {height}")

    clock = pygame.time.Clock()
    level = 0
    current_tile = 0

    screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT))
    pygame.display.set_caption('Level Editor')

    # store tiles in a list
    img_list = []

    for elem in list_tiles():
        img = pygame.image.load(elem).convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_list.append(img)

    save_img = pygame.image.load('img/save_btn.png').convert_alpha()
    load_img = pygame.image.load('img/load_btn.png').convert_alpha()

    # create empty tile list
    world_data = []
    for row in range(ROWS):
        r = [-1] * COLS
        world_data.append(r)

    # create ground
    for tile in range(0, COLS):
        world_data[ROWS - 1][tile] = 0

    # create buttons
    # make a button list
    button_list = []
    button_col = 0
    button_row = 0
    for i in range(len(img_list)):
        tile_button = button.Button(SCREEN_WIDTH + ((TILE_SIZE+20) * button_col) + TILE_SIZE, (TILE_SIZE+20) * button_row + TILE_SIZE, img_list[i], 1)
        button_list.append(tile_button)
        button_col += 1
        if button_col == 3:
            button_row += 1
            button_col = 0

    run = True
    while run:
        clock.tick(FPS)

        # draw
        draw_bg()
        draw_grid()
        draw_world()
        # draw tile panel and tiles
        pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

        save_button = button.Button(SCREEN_WIDTH + (SIDE_MARGIN/2), SCREEN_HEIGHT - 150, save_img, 1)
        load_button = button.Button(SCREEN_WIDTH + (SIDE_MARGIN/2), SCREEN_HEIGHT - 100, load_img, 1)

        # save and load data
        save() if save_button.draw(screen) else None
        load() if load_button.draw(screen) else None


        # choose a tile
        button_count = 0
        for button_count, i in enumerate(button_list):
            if i.draw(screen):
                current_tile = button_count

        # highlight the selected tile
        pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

        # add new tiles to the screen
        add_new_tiles()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


def param():
    def click():
        global MAP_NAME, COLS, ROWS
        MAP_NAME = str(map_name.get())
        COLS = int(width.get())
        ROWS = int(height.get())

        param_w.destroy()

    param_w = Tk()
    param_w.title("Param control")
    param_w.geometry('400x300')
    param_w['bg'] = '#ffbf00'

    map_name_lbl = Label(text="Nom map")
    map_name_lbl.pack(side=TOP, pady=5)
    map_name = Entry(param_w)
    map_name.pack(side=TOP, pady=10)

    width_lbl = Label(text="Width (Cols)")
    width_lbl.pack(side=TOP, pady=5)
    width = Entry(param_w)
    width.pack(side=TOP, pady=10)

    height_lbl = Label(text="Height (Rows)")
    height_lbl.pack(side=TOP, pady=5)
    height = Entry(param_w)
    height.pack(side=TOP, pady=10)

    Button(
        param_w,
        text="Créer map",
        padx=10,
        pady=5,
        command=click
    ).pack()

    param_w.mainloop()


if __name__ == '__main__':
    # VARS
    MAP_NAME: str
    COLS: int
    ROWS: int

    param()

    FPS = 60
    # define colours
    GREEN = (144, 201, 120)
    WHITE = (255, 255, 255)
    RED = (200, 25, 25)

    # game window
    TILE_SIZE = 40
    SCREEN_WIDTH = COLS * TILE_SIZE
    SCREEN_HEIGHT = ROWS * TILE_SIZE

    while SCREEN_HEIGHT > 1000 or SCREEN_WIDTH > 2000:
        TILE_SIZE -= 1
        SCREEN_HEIGHT = ROWS * TILE_SIZE
        SCREEN_WIDTH = COLS * TILE_SIZE

    SIDE_MARGIN = TILE_SIZE * 8

    editor()
