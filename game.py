# Partner 1: Sai Sahvir Bhaskaruni bhe5qn
# Partner 2: Matthew Wang hgp7pg

# Game Description: Our game is based off of minesweeper, except you find to find all of the bombs in the given timeframe in order to win the game

# 1. 3 Basic Features (User Input): Comes from the mouse clicking on each tile
# 2. 3 Basic Features (Game Over): If you do not find all of the bombs in the given time or if you click on a bomb you will lose
# 3. 3 Basic Features (Graphics/Images): The background of the game will include images

# 1. 4 Additional Features (Restart from Game Over): Include a button that triggers a command to restart the game
# 2. 4 Additional Features (Timer): Countdown from the allotted time (TBD) that the player can see
# 3. 4 Additional Features (Multiple Levels): Increased difficulty of either # of bombs, # of tiles, or amount of time (TBD)
# 4. 4 Additional Features (File Reading/Writing): Save the times from each trial and output the best times

#Changes: Added Object Oriented Programming and Collectibles as additional features. We added Object Oriented Programming because creating the tiles required the creation of a class -
# We added collectibles because we believed the flags counted as collectibles. We did not include file writing because we believed it was not necessary for the game
import uvage
import random

camera = uvage.Camera(800, 850)

gameplay = True
gameon = False
layered_text = True

class Tile: # creating gameboxes for minesweeper tiles
    def __init__(self, index, x, y, type="safe", number=0, is_flag=False, is_not_bomb=False, is_open=False):
        self.type = type
        self.number = 0
        self.index = index
        self.x = x
        self.y = y
        self.is_flag = is_flag
        self.is_not_bomb = is_not_bomb
        self.is_open = is_open
    def create_gamebox(self):
        x = self.x
        y = self.y
        bomb_image_list = ["minesweeper_0.png","minesweeper_1.png","minesweeper_2.png","minesweeper_3.png","minesweeper_4.png","minesweeper_5.png","minesweeper_6.png","minesweeper_7.png","minesweeper_8.png"]
        if self.is_flag == True:
            new_gamebox = uvage.from_image(self.x, self.y, "minesweeper_flag.png")
        elif self.is_not_bomb == True:
            image = bomb_image_list[self.number]
            new_gamebox = uvage.from_image(self.x, self.y, image)
        else:
            new_gamebox = uvage.from_image(self.x, self.y, "minesweeper_tile.png")
        return new_gamebox

    def get_number(self):
        self.number = 0
        self.is_not_bomb = True
        global adjacent_tiles
        adjacent_tiles = []
        if self.index == 0:
            adjacent_tiles = [1, 10, 11]
        elif self.index == 9:
            adjacent_tiles = [8, 18, 19]
        elif self.index == 90:
            adjacent_tiles = [80, 81, 91]
        elif self.index == 99:
            adjacent_tiles = [88, 89, 98]
        elif self.index % 10 == 0:
            adjacent_tiles = [self.index - 10, self.index - 9, self.index + 1, self.index + 10, self.index + 11]
        elif self.index < 10:
            adjacent_tiles = [self.index - 1, self.index + 1, self.index + 9, self.index + 10, self.index + 11]
        elif self.index > 90:
            adjacent_tiles = [self.index - 1, self.index + 1, self.index - 9, self.index - 10, self.index - 11]
        elif self.index % 10 == 9:
            adjacent_tiles = [self.index - 11, self.index - 10, self.index - 1, self.index + 9, self.index + 10]
        else:
            adjacent_tiles = [self.index + 1, self.index - 1, self.index + 9, self.index + 10, self.index + 11, self.index - 9, self.index - 10 , self.index - 11]
        for i in adjacent_tiles:
            if list_of_tiles[i].type == "bomb":
                self.number = self.number + 1
        self.is_open = True
    def adjacent_tiles(self):
        if self.type != "bomb":
            if self.number == 0:
                for i in adjacent_tiles:
                    if (list_of_tiles[i].type == "safe" and list_of_tiles[i].is_open == False and list_of_tiles[i].number == 0):
                        list_of_tiles[i].get_number()
                        list_of_tiles[i].is_not_bomb = True
                        list_of_tiles[i].create_gamebox()
                        list_of_tiles[i].adjacent_tiles()
                    return

def level_easy():
    global bomb_number
    bomb_number = 10
    setup()

def level_medium():
    global bomb_number
    bomb_number = 15
    setup()

def level_hard():
    global bomb_number
    bomb_number = 20
    setup()

def setup():
    global gameplay, list_of_tiles, gameon
    global num_ticks
    global num_seconds
    global layered_text
    global num_flags
    global bomb_number
    num_flags = bomb_number
    layered_text = True
    list_of_tiles = [] # calling class to create gamebox for minesweeper tiles
    overall_index = 0
    for y in range(90, 850, 80):
        for x in range(40, 800, 80):
            new_tile = Tile(overall_index, x, y)
            list_of_tiles.append(new_tile)
            overall_index += 1
    bomb_list = random.sample(range(0,99), bomb_number)
    for num in bomb_list:
        list_of_tiles[num].type = "bomb"
    camera.clear("black")
    for tile in list_of_tiles:
        camera.draw(tile.create_gamebox())
    gameplay = True
    gameon = True
    num_ticks = 0
    num_seconds = 240

def place_flag():
    global num_flags
    for tile in list_of_tiles:
        if tile.create_gamebox().contains(camera.mousex, camera.mousey):
            if tile.is_flag == False:
                tile.is_flag = True
                tile.is_open = True
                num_flags -= 1

def remove_flag():
    global num_flags
    for tile in list_of_tiles:
        if tile.create_gamebox().contains(camera.mousex, camera.mousey):
            if tile.is_flag == True:
                tile.is_flag = False
                tile.is_open = False
                num_flags += 1

def reveal_number(tile):
    if tile.type == "bomb":
        global gameplay
        gameplay = False
        return
    else:
        tile.get_number()
        if tile.number == 0:
            tile.adjacent_tiles()

def timer():
    global num_ticks
    global num_seconds
    global gameplay
    global num_correct_flags, bomb_number
    if num_correct_flags != bomb_number:
        num_ticks += 1
        if num_ticks % 30 == 0:
            num_seconds -= 1
        if num_seconds == 0:
            gameplay = False
    camera.draw(uvage.from_text(700,30,str(num_seconds),40, "White"))
def tick():
    global num_ticks
    global num_seconds
    global gameplay, list_of_tiles
    global gameon
    global bomb_number
    global layered_text
    global num_correct_flags
    global num_flags
    num_correct_flags = 0
    camera.clear("Black")
    if gameon == False:
        camera.draw(uvage.from_text(400, 150, 'MINESWEEPER', 100, "white", bold=True))
        camera.draw(uvage.from_text(400, 260, 'Press E for Easy Mode', 50, "white"))
        camera.draw(uvage.from_text(400, 340, 'Press M for Medium Mode', 50, "white"))
        camera.draw(uvage.from_text(400, 420, 'Press H for Hard Mode', 50, "white"))
        camera.draw(uvage.from_text(400, 520, 'Press F to Place a Flag', 25, "white"))
        camera.draw(uvage.from_text(400, 570, 'Press P to Remove a Flag', 25, "white"))
        camera.draw(uvage.from_text(400, 620, 'Left-Click to Reveal a Tile', 25, "white"))
        if uvage.is_pressing('e'):
            level_easy()
            gameon = True
        if uvage.is_pressing('m'):
            level_medium()
            gameon = True
        if uvage.is_pressing('h'):
            level_hard()
            gameon = True
    if gameon == True:
        for tile in list_of_tiles:
            if (gameplay == True and gameon == True):
                camera.draw(tile.create_gamebox())
            if (uvage.is_pressing('f') and num_flags > 0 and gameplay == True and gameon == True):
                place_flag()
            if (uvage.is_pressing('p') and num_flags < bomb_number and gameplay == True and gameon == True):
                remove_flag()
            if (camera.mouseclick and gameplay == True and gameon == True):
                if tile.create_gamebox().contains(camera.mousex, camera.mousey):
                    reveal_number(tile)
            if (tile.is_flag == True and tile.type == "bomb"):
                num_correct_flags += 1
    if gameon == True:
        camera.draw(uvage.from_text(200,30,"Number of Flags Left: " + str(num_flags), 40, "White"))
    if (gameplay == False and gameon == True and layered_text == True):
        camera.clear("black")
        camera.draw(uvage.from_text(400, 340, 'Game Over', 100, "Red", bold=True))
        camera.draw(uvage.from_text(400, 200, 'Press R to Restart', 50, "Red", bold=True))
        camera.draw(uvage.from_text(400, 500, "Number of Correct Flags: " + str(num_correct_flags), 40, "Red"))
        camera.display()
        if uvage.is_pressing('r'):
            layered_text = False
            gameon = False
    if gameon == True:
        if (num_correct_flags == bomb_number and layered_text == True):
            camera.clear("black")
            camera.draw(uvage.from_text(400, 340, "Game Won!", 100, "White", bold=True))
            camera.draw(uvage.from_text(400, 200, 'Press R to Restart', 50, "White", bold=True))
            camera.draw(uvage.from_text(400, 400, "Time: " + str(240 - num_seconds) + " Seconds", 40, "White"))
            if uvage.is_pressing('r'):
                layered_text = False
                gameon = False
    if (gameon == True and gameplay == True):
        timer()
    camera.display()

uvage.timer_loop(30, tick)