import pygame as pg
import random


import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (150,30)
#initializing pygame

pg.init()
move_sound = pg.mixer.Sound("sounds/piece_move.wav")
winning_sound = pg.mixer.Sound("sounds/applause.wav")
pg.mixer.music.load("sounds/background.wav")
move_sound.set_volume(1)
size = (900, 900)  #a tuple of size (width, height)
screen = pg.display.set_mode(size)
background_image = pg.image.load("img/two_players_back.png")
font = pg.font.SysFont(None, 24)
my_color = (71, 40, 21)
red = (225, 0, 0)
yellow = (225, 225, 0)
black = (0,0,0)


#for positioning of pieces the key
def position(x, y):
    x = x
    y = y
    c_x = 88
    c_y = 161

    if x >= 6:
        x += 1
    if y >= 6:
        c_y += 22

    X = c_x + (x * 56)
    Y = c_y + (y*56)

    return (X, Y)


#to roll and save the value of dice
def dice_value():
    value_1 = random.randint(1, 6)
    value_2 = random.randint(1, 6)
    pg.mixer.Sound.play(move_sound)
    dice1.my_dice = pg.image.load(you_dice[value_1-1])
    dice2.my_dice = pg.image.load(you_dice[value_2-1])
    write_in_file("{} {}".format(value_1, value_2), "txt/dice_saving.txt")

def cpu_dice_value():
    value_1 = random.randint(1, 6)
    value_2 = random.randint(1, 6)
    pg.mixer.Sound.play(move_sound)

    dice1_cpu.my_dice = pg.image.load(cpu_dice_list[value_1-1])
    dice2_cpu.my_dice = pg.image.load(cpu_dice_list[value_2-1])
    write_in_file("{} {}".format(value_1, value_2), "txt/cpu_dice_saving.txt")

def write_in_file(content, file_name):
    file = open(file_name, "w")
    file.write(content)
    file.close()

def get_from_file(file_name = "txt/dice_saving.txt"):
    file = open(file_name, "r")
    a = file.read().split()#file.read()[-1]
    file.close()
    return (int(a[0]), int(a[-1]))

#highlighting the keys
def light_white_keys(w):
    light_piece = None
    for i in w:
        i[1].image = pg.image.load("img/white_highlight.png")

    white_light_pieces = L
                # white_light_pieces.append([i, light_piece])

def light_black_keys(stack_list):
    light_piece = None
    for i in stack_list:
        i[1].image = pg.image.load("img/black_highlight.png")

def turn_on_the_turn_light(which_player):
    if which_player == "you":
        screen.blit(turn_light, (328, 6))
    else:
        screen.blit(turn_light, (490, 6))


#dice tolling list
you_dice = [
     "img/you_dice_1.png",
     "img/you_dice_2.png",
     "img/you_dice_3.png",
     "img/you_dice_4.png",
     "img/you_dice_5.png",
     "img/you_dice_6.png"
     ]

cpu_dice_list = [
     "img/cpu_dice_1.png",
     "img/cpu_dice_2.png",
     "img/cpu_dice_3.png",
     "img/cpu_dice_4.png",
     "img/cpu_dice_5.png",
     "img/cpu_dice_6.png"
     ]

white_light_pieces = [ ]
white_legal_destination = [ ]
white_reached_home = [ ]

black_light_pieces = [ ]
black_legal_destination = [ ]
black_reached_home = [ ]

L_e = 0

class my_piece:
    def __init__(self, id, co_ordinates = None):
        self.id = id
        if self.id == "white":
            self.image = pg.image.load("img/white_got.png")
        else:
            self.image = pg.image.load("img/black_got.png")
        self.co_ordinate = co_ordinates
        if self.co_ordinate is not None:
            self.X = self.co_ordinate[0]
            self.Y = self.co_ordinate[1]



#for column stack class
class column_stack:
    def __init__(self, location, *initial_pieces):
        self.initial_pieces = initial_pieces
        self.location = location
        self.connected = []
        self.elements = []
        if self.initial_pieces[0] is not None:
            self.elements = list(initial_pieces)
        self.positions = []

        my_range = None
        pos_x = None

        if location < 13:
            my_range = range(0, 6)
            pos_x = 12 - location
        else:
            my_range = range(11, 5, -1)
            pos_x = location - 1 - 12

        for i in my_range:
            self.positions.append(position(pos_x, i))

        self.connection()

        self.updating()


    # def highlight_destination(self):
    def connection(self):
        length = len(self.elements)

        for i in range(0, 6):
            if length > 0:
                self.connected.append([self.elements[i], self.positions[i]])
                length -= 1
            else:
                self.connected.append([None, self.positions[i]])

    def updating(self):
        for i in self.connected:
            if i[0] is not None:
                i[0].co_ordinate = i[1]

    def remove_piece(self): #poping
        print(len(self.elements))
        if len(self.elements) > 0:
            deleted_piece = self.elements.pop()
            for i in self.connected:
                if i[0] == deleted_piece:
                    i[0] = None

            self.connection()
            self.updating()

            return deleted_piece
        else:
            "can't delete from empty stack"
        print(len(self.elements))

    def add_piece(self, piece_to_add): #pushing
        print(self.connected)
        if len(self.elements) <= 6:

            self.elements.append(piece_to_add)
            tteemmpp = []
            for i in range(0, 6):
                if i+1 <= len(self.elements):
                    tteemmpp.append([self.elements[i], self.positions[i]])
                else:
                    tteemmpp.append([None, self.positions[i]])
            self.connected = tteemmpp
            self.connection()
            self.updating()
        else:
            "stack is full"
        print(" ")
        print(self.connected)

    def receiving_light(self, which_piece):
        opponent = None
        if which_piece == "white":
            opponent = "black"
        else:
            opponent = "white"

        if (len(self.elements) == 0) or (len(self.elements) == 1 and self.elements[0].id == opponent) or (len(self.elements) < 6 and self.elements[0].id == which_piece):
            if self.location < 13:
                light_image = destination
                screen.blit(light_image, position(12-self.location,0))
            else:
                light_image = destination_bottom
                screen.blit(light_image, position(self.location-13,7))
            return "on"


    def checking_receiving_light(self, which_piece):
        opponent = None
        if which_piece == "white":
            opponent = "black"
        else:
            opponent = "white"

        if (len(self.elements) == 0) or (len(self.elements) == 1 and self.elements[0].id == opponent) or (len(self.elements) < 6 and self.elements[0].id == which_piece):
            return "on"

class bearing_off_stack:
    def __init__(self, location, color):
        self.location = location
        self.color = color
        self.elements = []
        self.positions = []
        self.connected = []
        self.x = 840
        self.y = None

        if self.color == "white":
            self.y = 159
        else:
            self.y = 595

        if self.color == "white":
            for i in range(0, 15):
                self.positions.append((self.x, self.y+(18*i)))
        else:
            for i in range(14, -1, -1):
                self.positions.append((self.x, self.y+(18*i)))

        self.connection()
        self.updating()

        print(self.elements)
        print(self.connected)
        print(self.positions)
        print()

    def add_piece(self, piece_to_add):
        if piece_to_add.id == "white":
            piece_to_add.image = pg.image.load("img/white_beard_off.png")
        else:
            piece_to_add.image = pg.image.load("img/black_beard_off.png")

        self.elements.append(piece_to_add)
        tteemmpp = []
        for i in range(0, 15):
            if i+1 <= len(self.elements):
                tteemmpp.append([self.elements[i], self.positions[i]])
            else:
                tteemmpp.append([None, self.positions[i]])
        self.connected = tteemmpp
        self.connection()
        self.updating()

    def receiving_light(self, colour):
        if colour == "white":
            if len(white_reached_home) == 15:
                screen.blit(bearing_off_light, (838, 153))
        else:
            if len(black_reached_home) == 15:
                screen.blit(bearing_off_light, (838, 589))

    def checking_receiving_light(self, which):
        if which == "white":
            if len(white_reached_home) == 15:
                return "on"
        else:
            if len(black_reached_home) == 15:
                return  "on"

    def connection(self):
        length = len(self.elements)

        for i in range(0, 15):
            if length > 0:
                self.connected.append([self.elements[i], self.positions[i]])
                length -= 1
            else:
                self.connected.append([None, self.positions[i]])

    def updating(self):
        for i in self.connected:
            if i[0] is not None:
                i[0].co_ordinate = i[1]

#dice
class cpu_dice:
    def __init__(self, pic):
        self.my_dice = pg.image.load(pic)


blank_cpu = "img/blank_cpu.png"
blank = "img/blank.png"


class player_dice:
    def __init__(self, pic):
        self.my_dice = pg.image.load(pic)

my_middle_stack = column_stack(0, None)
temp_middle = []
temp_x = 426
temp_y = 450

for i in range(0, 6):
    temp_middle.append((temp_x, temp_y + (i * 56)))

my_middle_stack.positions = temp_middle

white_bearing_stack = bearing_off_stack(0, "white")
black_bearing_stack = bearing_off_stack(0, "black")

dice1 = player_dice(blank)
dice2 = player_dice(blank)

dice1_cpu = cpu_dice(blank_cpu)
dice2_cpu = cpu_dice(blank_cpu)

#black pieces

black_piece1 = my_piece("black")#co-ordinates (x, y)
black_piece2 = my_piece("black")
black_piece3 = my_piece("black")
black_piece4 = my_piece("black")
black_piece5 = my_piece("black")

black_piece6 = my_piece("black")
black_piece7 = my_piece("black")
black_piece8 = my_piece("black")

black_piece9 = my_piece("black")
black_piece10 = my_piece("black")
black_piece11 = my_piece("black")
black_piece12 = my_piece("black")
black_piece13 = my_piece("black")

black_piece14 = my_piece("black")
black_piece15 = my_piece("black")

#white pieces

white_piece1 = my_piece("white")
white_piece2 = my_piece("white")
white_piece3 = my_piece("white")
white_piece4 = my_piece("white")
white_piece5 = my_piece("white")

white_piece6 = my_piece("white")
white_piece7 = my_piece("white")
white_piece8 = my_piece("white")

white_piece9 = my_piece("white")
white_piece10 = my_piece("white")
white_piece11 = my_piece("white")
white_piece12 = my_piece("white")
white_piece13 = my_piece("white")

white_piece14 = my_piece("white")
white_piece15 = my_piece("white")


#dice button width = 45px, height = 120px
inactive_dice_button = pg.image.load("img/dice_button.png")
active_dice_button = pg.image.load("img/active_dice_button.png")

inactive_player2_dice = pg.image.load("img/inactive_player2_dice.png")
active_player2_dice = pg.image.load("img/active_player2_dice.png")


#blank dice
dice = pg.image.load("img/blank.png")

#checking highlights
# white_piece14.image = pg.image.load("img/white_highlight.png")
# black_piece5.image = pg.image.load("img/black_highlight.png")


#stack objects

stack1 = column_stack(1, black_piece14, black_piece15)
stack2 = column_stack(2, None)
stack3 = column_stack(3, None)
stack4 = column_stack(4, None)
stack5 = column_stack(5, None)
stack6 = column_stack(6, white_piece1, white_piece2, white_piece3, white_piece4, white_piece5)
stack7 = column_stack(7, None)
stack8 = column_stack(8, white_piece6, white_piece7, white_piece8)
stack9 = column_stack(9, None)
stack10 = column_stack(10, None)
stack11 = column_stack(11, None)
stack12 = column_stack(12, black_piece9, black_piece10, black_piece11, black_piece12, black_piece13)
stack13 = column_stack(13, white_piece13, white_piece12, white_piece11, white_piece10, white_piece9)
stack14 = column_stack(14, None)
stack15 = column_stack(15, None)
stack16 = column_stack(16, None)
stack17 = column_stack(17, black_piece8, black_piece7, black_piece6)
stack18 = column_stack(18, None)
stack19 = column_stack(19, black_piece5, black_piece4, black_piece3, black_piece2, black_piece1)
stack20 = column_stack(20, None)
stack21 = column_stack(21, None)
stack22 = column_stack(22, None)
stack23 = column_stack(23, None)
stack24 = column_stack(24, white_piece15, white_piece14)


all_stack_list = [
    stack1, stack2, stack3, stack4, stack5, stack6, stack7, stack8, stack9, stack10, stack11, stack12,
    stack13, stack14, stack15, stack16, stack17, stack18, stack19, stack20, stack21, stack22, stack23, stack24
]

all_stack_dict = {
    1: stack1,
    2: stack2,
    3: stack3,
    4: stack4,
    5: stack5,
    6: stack6,
    7: stack7,
    8: stack8,
    9: stack9,
    10: stack10,
    11: stack11,
    12: stack12,
    13: stack13,
    14: stack14,
    15: stack15,
    16: stack16,
    17: stack17,
    18: stack18,
    19: stack19,
    20: stack20,
    21: stack21,
    22: stack22,
    23: stack23,
    24: stack24
}
#to move piece
def move(FROM, to):
    pg.mixer.Sound.play(move_sound)
    #first poping from current stack
    pg.mixer.Sound.play(move_sound)
    deleted_piece = FROM.remove_piece()
    temp_to_move = deleted_piece

    print(white_light_pieces)
    consideration = None

    if turn == "you":
        consideration = white_light_pieces
    else:
        consideration = black_light_pieces

    for i in consideration:
        if i[1] == deleted_piece:
            del i
    temp_to_dest = to.positions[-1]
    to.add_piece(deleted_piece)
    print(len(to.elements))
    print("length of white ligth pieces = ", len(white_light_pieces))
    consideration.append([to, deleted_piece])


    #then push in desired stack
#move()
#move()
empty = []
white_wins = pg.image.load("img/white_wins.png")
black_wins = pg.image.load("img/black_wins.png")
destination_bottom = pg.image.load("img/destination_light_bottom.png")
destination = pg.image.load("img/destination_light.png")
turn_light = pg.image.load("img/turn_light.png")

cpu_dice_rolled = False
you_dice_rolled = False
temppp = 0
temp = 0
turn = None
speed = 2.1
running = True
player_dice1_moved = False
player_dice2_moved = False
cpu_dice1_moved = False
cpu_dice2_moved = False
light_trigerred = False
black_light_trigerred = False
winner_declared = False
turn_rolling = None
winner_sound = "off"
player1_turn_msg = False
player2_turn_msg = False

no_move_possible = font.render("No move possible", True, my_color)
#assigning Home of those pieces that are already at home

for i in all_stack_list:
    if i.location <= 6:
        for j in i.elements:
            if j.id == "white":
                white_reached_home.append(j)

    elif i.location >= 19:
        for j in i.elements:
            if j.id == "black":
                black_reached_home.append(j)
#testing
# print(white_reached_home, len(white_reached_home))
# print(black_reached_home, len(black_reached_home))
# print(stack1.connected)


bearing_off_light = pg.image.load("img/bearing_off_light.png")

white_beard_off = pg.image.load("img/white_beard_off.png")

how_to_play = pg.image.load("img/how_to_play.png")

rules = pg.image.load("img/rules.png")

winning_img = pg.image.load("img/winning.png")

losing_img = pg.image.load("img/lose.png")

start = pg.image.load("img/start.png")

start_clicked = False
how_play_understood = False
rules_understood = False
having_first_move = font.render("Having first move", True, my_color)
show_msg_player1 = show_msg_player2 = None

A = 0
turn_a = None
turn_b = None

pg.mixer.music.play(-1)
while running:

    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()

    if turn_rolling == False:
        if A < 20:
            turn_a = random.randint(1, 6)
            dice2_cpu.my_dice = pg.image.load(cpu_dice_list[turn_a-1])
            turn_b = random.randint(1, 6)
            dice1.my_dice = pg.image.load(you_dice[turn_b-1])
            A += 1
            print("A = ",A)
        else:
            print(turn_a, turn_b)
            pg.time.delay(1000)
            if turn_a != turn_b:
                if turn_a > turn_b:
                    turn = "cpu"
                    player2_turn_msg = True

                elif turn_a < turn_b:
                    turn = "you"
                    player1_turn_msg = True

                dice1.my_dice = pg.image.load(blank)
                dice2_cpu.my_dice = pg.image.load(blank_cpu)
                turn_rolling = True
                A = 0
            else:
                A = 0
                turn_rolling = False


    #making all lights off
    if turn == "you":
        for i in all_stack_list:
            for j in i.elements:
                if j.id == "white":
                    j.image = pg.image.load("img/white_got.png")

    #making all lights off
    if turn == "cpu":
        for i in all_stack_list:
            for j in i.elements:
                if j.id == "black":
                    j.image = pg.image.load("img/black_got.png")


    #making lights on if turn is not completed
    if light_trigerred == True:
        light_white_keys(white_light_pieces)

    #making lights on if turn is not completed
    if black_light_trigerred == True:
        light_black_keys(black_light_pieces)

    # when turn of player is completed
    if ((player_dice1_moved == True) and (player_dice2_moved == True)) or ((len(white_legal_destination) == 0) and (you_dice_rolled == True and ((player_dice1_moved == player_dice2_moved == False) or (player_dice1_moved == True) or (player_dice2_moved == True)))):
        player_dice1_moved = False
        player_dice2_moved = False
        light_trigerred = False

        you_dice_rolled = False
        dice1.my_dice = pg.image.load(blank)
        dice2.my_dice = pg.image.load(blank)
        for i in white_light_pieces:
            i[1].image = pg.image.load("img/white_got.png")

        white_light_pieces = []
        white_legal_destination = []
        turn = "cpu"
        temp = 0
        temppp = 0
        if ((you_dice_rolled == True) and ((player_dice1_moved == player_dice2_moved == False) or (player_dice1_moved == True) or (player_dice2_moved == True))):
            show_msg_player1 = True


    # when turn of cpu is completed
    if ((cpu_dice1_moved == True) and (cpu_dice2_moved == True)) or ((len(black_legal_destination) == 0) and (cpu_dice_rolled == True and ((cpu_dice1_moved == cpu_dice2_moved == False) or (cpu_dice1_moved == True) or (cpu_dice2_moved == True)))):
        cpu_dice_rolled = False
        cpu_dice1_moved = False
        cpu_dice2_moved = False
        black_light_trigerred = False

        dice1_cpu.my_dice = pg.image.load(blank_cpu)
        dice2_cpu.my_dice = pg.image.load(blank_cpu)
        for i in black_light_pieces:
            i[1].image = pg.image.load("img/black_got.png")

        black_light_pieces = []
        black_legal_destination = []
        turn = "you"
        if ((cpu_dice_rolled == True) and ((cpu_dice1_moved == cpu_dice2_moved == False) or (cpu_dice1_moved == True) or (cpu_dice2_moved == True))):
            show_msg_player2 = True

    # print(mouse)
    screen.fill((0,0,0))
    screen.blit(background_image, (0,0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                pass
                # time.sleep(2)


        if event.type == pg.MOUSEBUTTONUP and turn == "you" and 840 <= mouse[0] <= 885 and 440 <= mouse[1] <= 560:
            if event.button == 1:
                light_white_keys(white_light_pieces)
                you_dice_rolled = True
                light_trigerred = True

        if event.type == pg.MOUSEBUTTONUP and turn == "cpu" and 3 <= mouse[0] <= 48 and 420 <= mouse[1] <= 540:
            if event.button == 1:
                light_black_keys(black_light_pieces)
                cpu_dice_rolled = True
                black_light_trigerred = True

        # step 5 (movement of player's pieces
        print(len(white_legal_destination))
        if turn == "you":
            for i in white_light_pieces:
                dice_player = get_from_file()
                if event.type == pg.KEYDOWN and (event.key == pg.K_m or event.key == pg.K_SPACE) and you_dice_rolled:
                    if len(my_middle_stack.elements) > 0 and my_middle_stack.elements[-1].id == "white":
                        d1, d2 = 25 - (-(i[0].location - dice_player[0])), 25 - (-(i[0].location - dice_player[1]))
                    else:
                        d1, d2 = i[0].location - dice_player[0], i[0].location - dice_player[1]
                    if click[0] == 1 and i[1].co_ordinate[0] <= mouse[0] <= i[1].co_ordinate[0] + 56 and \
                            i[1].co_ordinate[1] <= mouse[1] <= i[1].co_ordinate[1] + 56:
                        if event.key == pg.K_m:
                            if len(white_reached_home) <= 15:
                                if d1 > 0 and player_dice1_moved == False:
                                    print("M is pressed")
                                    if all_stack_dict[d1] in white_legal_destination:
                                        if len(all_stack_dict[d1].elements) == 1 and (all_stack_dict[d1].elements[0].id == "black"):
                                            move(all_stack_dict[d1], my_middle_stack)
                                        move(i[0], all_stack_dict[d1])
                                        if all_stack_dict[d1].location <= 6:
                                            if all_stack_dict[d1].elements[-1] not in white_reached_home:
                                                white_reached_home.append(all_stack_dict[d1].elements[-1])

                                            print(len(white_reached_home))
                                            print(white_reached_home)

                                        dice1.my_dice = pg.image.load(blank)
                                        player_dice1_moved = True
                                if d1 == 0 and player_dice1_moved == False and len(white_reached_home) == 15:
                                    print("M is pressed")
                                    move(i[0], white_bearing_stack)
                                    player_dice1_moved = True
                                    dice1.my_dice = pg.image.load(blank)

                        if event.key == pg.K_SPACE:
                            if len(white_reached_home) <= 15:
                                if d2 > 0 and player_dice2_moved == False:
                                    print("Space is pressed")
                                    if all_stack_dict[d2] in white_legal_destination:
                                        if len(all_stack_dict[d2].elements) == 1 and (all_stack_dict[d2].elements[0].id == "black"):
                                            move(all_stack_dict[d2], my_middle_stack)
                                        move(i[0], all_stack_dict[d2])
                                        if all_stack_dict[d2].location <= 6:
                                            if all_stack_dict[d2].elements[-1] not in white_reached_home:
                                                white_reached_home.append(all_stack_dict[d2].elements[-1])
                                            print(len(white_reached_home))
                                            print(white_reached_home)
                                        dice2.my_dice = pg.image.load(blank)
                                        player_dice2_moved = True

                                if d2 == 0 and player_dice2_moved == False and len(white_reached_home) == 15:
                                    print("space is pressed")
                                    move(i[0], white_bearing_stack)
                                    dice2.my_dice = pg.image.load(blank)
                                    player_dice2_moved = True

        print("white_light_pieces", white_light_pieces)
        #movement of cpu
        if turn == "cpu":
            for i in black_light_pieces:
                dice_cpu = get_from_file("txt/cpu_dice_saving.txt")
                if event.type == pg.KEYDOWN and (event.key == pg.K_m or event.key == pg.K_SPACE) and cpu_dice_rolled:
                    if len(my_middle_stack.elements) > 0 and my_middle_stack.elements[-1].id == "black":
                        d1, d2 = -(i[0].location - dice_cpu[0]), -(i[0].location - dice_cpu[1])
                    else:
                        d1, d2 = i[0].location + dice_cpu[0], i[0].location + dice_cpu[1]
                    if click[0] == 1 and i[1].co_ordinate[0] <= mouse[0] <= i[1].co_ordinate[0] + 56 and \
                            i[1].co_ordinate[1] <= mouse[1] <= i[1].co_ordinate[1] + 56:
                        if event.key == pg.K_m:
                            if len(black_reached_home) <= 15:
                                if d1 < 25 and cpu_dice1_moved == False:
                                    print("M is pressed")
                                    if all_stack_dict[d1] in black_legal_destination:
                                        if len(all_stack_dict[d1].elements) == 1 and (all_stack_dict[d1].elements[0].id == "white"):
                                            move(all_stack_dict[d1], my_middle_stack)
                                        move(i[0], all_stack_dict[d1])
                                        if all_stack_dict[d1].location >= 19:
                                            if all_stack_dict[d1].elements[-1] not in black_reached_home:
                                                black_reached_home.append(all_stack_dict[d1].elements[-1])

                                            print(len(black_reached_home))
                                            print(black_reached_home)

                                        dice1_cpu.my_dice = pg.image.load(blank_cpu)
                                        cpu_dice1_moved = True
                                if d1 == 25 and cpu_dice1_moved == False and len(black_reached_home) == 15:
                                    print("M is pressed")
                                    move(i[0], black_bearing_stack)
                                    cpu_dice1_moved = True
                                    dice1_cpu.my_dice = pg.image.load(blank_cpu)

                        if event.key == pg.K_SPACE:
                            if len(black_reached_home) <= 15:
                                if d2 < 25 and cpu_dice2_moved == False:
                                    print("Space is pressed")
                                    if all_stack_dict[d2] in black_legal_destination:
                                        if len(all_stack_dict[d2].elements) == 1 and (all_stack_dict[d2].elements[0].id == "white"):
                                            move(all_stack_dict[d2], my_middle_stack)
                                        move(i[0], all_stack_dict[d2])
                                        if all_stack_dict[d2].location >= 19:
                                            if all_stack_dict[d2].elements[-1] not in black_reached_home:
                                                black_reached_home.append(all_stack_dict[d2].elements[-1])
                                            print(len(black_reached_home))
                                            print(black_reached_home)
                                        dice2_cpu.my_dice = pg.image.load(blank_cpu)
                                        cpu_dice2_moved = True

                                if d2 == 25 and cpu_dice2_moved == False and len(black_reached_home) == 15:
                                    print("space is pressed")
                                    move(i[0], black_bearing_stack)
                                    dice2_cpu.my_dice = pg.image.load(blank_cpu)
                                    cpu_dice2_moved = True



    print("white reached home: ", len(white_reached_home))
    print("black reached home: ", len(black_reached_home))
    screen.blit(black_piece1.image, black_piece1.co_ordinate)
    screen.blit(black_piece2.image, black_piece2.co_ordinate)
    screen.blit(black_piece3.image, black_piece3.co_ordinate)
    screen.blit(black_piece4.image, black_piece4.co_ordinate)
    screen.blit(black_piece5.image, black_piece5.co_ordinate)
    screen.blit(black_piece6.image, black_piece6.co_ordinate)
    screen.blit(black_piece7.image, black_piece7.co_ordinate)
    screen.blit(black_piece8.image, black_piece8.co_ordinate)
    screen.blit(black_piece9.image, black_piece9.co_ordinate)
    screen.blit(black_piece10.image, black_piece10.co_ordinate)
    screen.blit(black_piece11.image, black_piece11.co_ordinate)
    screen.blit(black_piece12.image, black_piece12.co_ordinate)
    screen.blit(black_piece13.image, black_piece13.co_ordinate)
    screen.blit(black_piece14.image, black_piece14.co_ordinate)
    screen.blit(black_piece15.image, black_piece15.co_ordinate)

    screen.blit(white_piece1.image, white_piece1.co_ordinate)
    screen.blit(white_piece2.image, white_piece2.co_ordinate)
    screen.blit(white_piece3.image, white_piece3.co_ordinate)
    screen.blit(white_piece4.image, white_piece4.co_ordinate)
    screen.blit(white_piece5.image, white_piece5.co_ordinate)
    screen.blit(white_piece6.image, white_piece6.co_ordinate)
    screen.blit(white_piece7.image, white_piece7.co_ordinate)
    screen.blit(white_piece8.image, white_piece8.co_ordinate)
    screen.blit(white_piece9.image, white_piece9.co_ordinate)
    screen.blit(white_piece10.image, white_piece10.co_ordinate)
    screen.blit(white_piece11.image, white_piece11.co_ordinate)
    screen.blit(white_piece12.image, white_piece12.co_ordinate)
    screen.blit(white_piece13.image, white_piece13.co_ordinate)
    screen.blit(white_piece14.image, white_piece14.co_ordinate)
    screen.blit(white_piece15.image, white_piece15.co_ordinate)

    #for human player
    if turn == "you":
        #step 1 (turn on lights)
        turn_on_the_turn_light(turn)

        # step 2 (dice rolling)
        if you_dice_rolled == False:
            if 840 <= mouse[0] <= 885 and 440 <= mouse[1] <= 560:
                screen.blit(active_dice_button, (840, 440))

                if click[0] == 1:
                    player1_turn_msg = False
                    dice_value()
            else:
                screen.blit(inactive_dice_button, (840, 440))

        #step 3 (lighting the pieces that are allowed to move)
        L = []

        if len(my_middle_stack.elements) > 0 and my_middle_stack.elements[-1].id == "white":
            for i in my_middle_stack.elements:
                if i.id == "white":
                    L.append([my_middle_stack, i])
        else:
            for i in all_stack_list:
                if len(i.elements) > 0:
                    light_piece = i.elements[-1]
                    if light_piece.id == "white":
                        L.append([i, light_piece])
        white_light_pieces = L


        #step 4 (updating the allowed destinations and lighting them on click)
        if you_dice_rolled == True and len(white_light_pieces) > 0:
            temp_destination = []
            dice_player = get_from_file()

            if len(white_reached_home) <= 15:
                for i in white_light_pieces:
                    if len(my_middle_stack.elements) > 0 and my_middle_stack.elements[-1].id == "white":
                        d1, d2 = 25-(-(i[0].location - dice_player[0])), 25-(-(i[0].location - dice_player[1]))
                    else:
                        d1, d2 = i[0].location - dice_player[0], i[0].location - dice_player[1]
                    if d1 > 0 and player_dice1_moved == False:
                        if all_stack_dict[d1].checking_receiving_light("white") == "on":
                            temp_destination.append(all_stack_dict[d1])

                    if d1 == 0 and player_dice1_moved == False:
                        if white_bearing_stack.checking_receiving_light("white") == "on":
                            temp_destination.append(white_bearing_stack)

                    if d2 > 0 and player_dice2_moved == False:
                        if all_stack_dict[d2].checking_receiving_light("white") == "on":
                            temp_destination.append(all_stack_dict[d2])

                    if d2 == 0 and player_dice2_moved == False:
                        if white_bearing_stack.checking_receiving_light("white") == "on":
                            temp_destination.append(white_bearing_stack)


            white_legal_destination = temp_destination
            print("white legal destinations : ", white_legal_destination)

            for i in white_light_pieces:

                if click[0] == 1 and i[1].co_ordinate[0] <= mouse[0] <= i[1].co_ordinate[0] + 56 and i[1].co_ordinate[
                    1] <= mouse[1] <= i[1].co_ordinate[1] + 56:
                    if len(my_middle_stack.elements) > 0 and my_middle_stack.elements[-1].id == "white":                        d1, d2 = 25-(-(i[0].location - dice_player[0])), 25-(-(i[0].location - dice_player[1]))
                    else:
                        d1, d2 = i[0].location - dice_player[0], i[0].location - dice_player[1]
                    print(d1, d2)
                    if len(white_reached_home) <= 15:
                        if d1 > 0 and player_dice1_moved == False:
                            all_stack_dict[d1].receiving_light("white")

                        if d2 > 0 and player_dice2_moved == False:
                            all_stack_dict[d2].receiving_light("white")

                        if d1 == 0 and player_dice1_moved == False:
                            white_bearing_stack.receiving_light("white")

                        if d2 == 0 and player_dice2_moved == False:
                            white_bearing_stack.receiving_light("white")

        #step 5 (movement of pieces)
            #ye uper event waly part mein horaha he line # 567 mein


    #for cpu
    if turn == "cpu":
        #step 1 (turn on the turn lights)
        turn_on_the_turn_light(turn)

        #step 2 (dice rolling)


        if cpu_dice_rolled == False:
            if 3 <= mouse[0] <= 48 and 420 <= mouse[1] <= 540:
                screen.blit(active_player2_dice, (3, 420))

                if click[0] == 1:
                    player2_turn_msg = False
                    cpu_dice_value()
            else:
                screen.blit(inactive_player2_dice, (3, 420))

        L = []

        if len(my_middle_stack.elements) > 0 and my_middle_stack.elements[-1].id == "black":
            for i in my_middle_stack.elements:
                if i.id == "black":
                    L.append([my_middle_stack, i])
        else:
            for i in all_stack_list:
                if len(i.elements) > 0:
                    light_piece = i.elements[-1]
                    if light_piece.id == "black":
                        L.append([i, light_piece])
        black_light_pieces = L


        #step 4 (updating the allowed destinations and lighting them on click)
        if cpu_dice_rolled == True and len(black_light_pieces) > 0:
            temp_destination = []
            dice_cpu = get_from_file("txt/cpu_dice_saving.txt")

            if len(black_reached_home) <= 15:
                for i in black_light_pieces:
                    if len(my_middle_stack.elements) > 0 and my_middle_stack.elements[-1].id == "black":
                        d1, d2 = -(i[0].location - dice_cpu[0]), -(i[0].location - dice_cpu[1])
                    else:
                        d1, d2 = i[0].location + dice_cpu[0], i[0].location + dice_cpu[1]

                    if d1 < 25 and cpu_dice1_moved == False:
                        if all_stack_dict[d1].checking_receiving_light("black") == "on":
                            temp_destination.append(all_stack_dict[d1])

                    if d1 == 25 and cpu_dice1_moved == False:
                        if black_bearing_stack.checking_receiving_light("black") == "on":
                            temp_destination.append(black_bearing_stack)

                    if d2 < 25 and cpu_dice2_moved == False:
                        if all_stack_dict[d2].checking_receiving_light("black") == "on":
                            temp_destination.append(all_stack_dict[d2])

                    if d2 == 25 and cpu_dice2_moved == False:
                        if black_bearing_stack.checking_receiving_light("black") == "on":
                            temp_destination.append(black_bearing_stack)

            black_legal_destination = temp_destination
            print(black_legal_destination)
            print(len(black_legal_destination))

            for i in black_light_pieces:
                print("my middle stack",len(my_middle_stack.elements))
                if click[0] == 1 and i[1].co_ordinate[0] <= mouse[0] <= i[1].co_ordinate[0] + 56 and i[1].co_ordinate[
                    1] <= mouse[1] <= i[1].co_ordinate[1] + 56:
                    if len(my_middle_stack.elements) > 0 and my_middle_stack.elements[-1].id == "black":
                        d1, d2 = -(i[0].location - dice_cpu[0]), -(i[0].location - dice_cpu[1])
                    else:
                        d1, d2 = i[0].location + dice_cpu[0], i[0].location + dice_cpu[1]
                    print(d1, d2)
                    if len(black_reached_home) <= 15:
                        if d1 < 25 and cpu_dice1_moved == False:
                            all_stack_dict[d1].receiving_light("black")

                        if d2 < 25 and cpu_dice2_moved == False:
                            all_stack_dict[d2].receiving_light("black")

                        if d1 == 25 and cpu_dice1_moved == False:
                            black_bearing_stack.receiving_light("black")

                        if d2 == 25 and cpu_dice2_moved == False:
                            black_bearing_stack.receiving_light("black")

        #step 5 (movement of pieces)
            #ye uper event waly part mein horaha he line # 770 mein



    screen.blit(dice1.my_dice, (2, 650))
    screen.blit(dice2.my_dice, (2, 720))

    screen.blit(dice1_cpu.my_dice, (2, 210))
    screen.blit(dice2_cpu.my_dice, (2, 285))

    if len(white_bearing_stack.elements) == 15:
        pg.mixer.music.stop()
        winner_declared = True
        screen.blit(white_wins, (0, 0))
        winner_sound = "on"

    elif len(black_bearing_stack.elements) == 15:
        pg.mixer.music.stop()
        winner_declared = True
        screen.blit(black_wins, (0, 0))
        winner_sound = "on"


    if winner_declared == True:
        if winning_sound == "on":
            pg.mixer.Sound.play(winning_sound)
            winner_sound = "off"

        if 250 <= mouse[0] <= 650 and 484 <= mouse[1] <= 550 and click[0] == 1:
            pass
        if 250 <= mouse[0] <= 650 and 570 <= mouse[1] <= 635 and click[0] == 1:
            pg.display.quit()



    if start_clicked == False:
        screen.blit(start, (0, 0))

        if 250 <= mouse[0] <= 650 and 484 <= mouse[1] <= 550:
            if click[0] == 1:
                start_clicked = True
                start = None
        if 250 <= mouse[0] <= 650 and 570 <= mouse[1] <= 635:
            if click[0] == 1:
                pg.display.quit()

    if start_clicked == True and how_play_understood == False:
        screen.blit(how_to_play, (0, 0))
        if 250 <= mouse[0] <= 650 and 570 <= mouse[1] <= 635:
            if click[0] == 1:
                how_play_understood = True
                how_to_play = None

    if start_clicked == True and how_play_understood == True and rules_understood == False:
        screen.blit(rules, (0, 0))
        if 250 <= mouse[0] <= 650 and 635 <= mouse[1] <= 700:
            if click[0] == 1:
                rules_understood = True
                rules = None
                turn_rolling = False

    if show_msg_player1:
        screen.blit(no_move_possible, (19, 68))
        pg.time.delay(1000)
        show_msg_player1 = None
    if show_msg_player2:
        screen.blit(no_move_possible, (746, 68))
        pg.time.delay(1000)
        show_msg_player2 = None

    if player1_turn_msg:
        screen.blit(having_first_move, (19, 68))
        # pg.time.delay(1000)
        # player1_turn_msg = False

    if player2_turn_msg:
        screen.blit(having_first_move, (746, 68))
        # pg.time.delay(1000)
        # player2_turn_msg = False

    pg.display.update()