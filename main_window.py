import pygame as pg
import random
import math
import time
from threading import Timer
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (150,30)
#initializing pygame
pg.init()
size = (900, 900)  #a tuple of size (width, height)
screen = pg.display.set_mode(size)
background_image = pg.image.load("img/main_back.png")
font = pg.font.SysFont(None, 25)
red = (225, 0, 0)
yellow = (225, 225, 0)
black = (0,0,0)

#message
def message_to_screen(msg, color, pos):
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, pos)

def button(txt, x, y, w, h, i_c, a_c):
    mouse = pg.mouse.get_pos()
    # print(mouse)

    click = pg.mouse.get_pressed()
    print(click)

    if x <= mouse[0] <= x+w and y <= mouse[1] <= y+h:
        pg.draw.rect(screen, a_c, (x, y, w, h))
        if click[0] == 1:
            print("left click has been pressed")
            button("Me", x+100, y+100, w, h, red, yellow)
        elif click[1] == 1:
            print("middle button has been pressed")
        elif click[2] == 1:
            print("right button has been pressed")
    else:
        pg.draw.rect(screen, i_c, (x, y, w, h))

    message_to_screen(txt, (0,0,0), (x+(w*0.30), y+(h*0.30)))



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

#for column_stack positioning (for top part)
def stack_column_position_top(x):
    extra = 0
    if x >= 7:
        x += 1

    x = x-1
    x = 12-x+1


    c_x_t_l = 88+(56*(x-1))
    c_x_t_r = c_x_t_l+56
    c_x_b_r = c_x_t_l+28
    c_x_b_l = c_x_b_r
    c_y_t_l = 161
    c_y_t_r = c_y_t_l
    c_y_b_r = c_y_t_l+339
    c_y_b_l = c_y_b_r


    top_left = (c_x_t_l, c_y_t_l+extra)
    top_right = (c_x_t_r, c_y_t_r+extra)
    bottom_right = (c_x_b_r, c_y_b_r+extra)
    bottom_left = (c_x_b_l, c_y_b_l+extra)

    return (bottom_left, top_left, top_right, bottom_right)

#for column_stack positioning (for bottom part)
def stack_column_position_bottom(x):
    x = x-12
    extra = 352
    if x >= 7:
        x += 1

    c_x_t_l = 88+(56*(x-1))
    c_x_t_r = c_x_t_l+56
    c_x_b_r = c_x_t_l+28
    c_x_b_l = c_x_b_r
    c_y_t_l = 161
    c_y_t_r = c_y_t_l
    c_y_b_r = c_y_t_l+339
    c_y_b_l = c_y_b_r


    top_left = (c_x_t_l, c_y_t_l+extra+339)
    top_right = (c_x_t_r, c_y_t_r+extra+339)
    bottom_right = (c_x_b_r, c_y_b_r+extra-339)
    bottom_left = (c_x_b_l, c_y_b_l+extra-339)

    return (bottom_left, top_left, top_right, bottom_right)

#to roll and save the value of dice
def dice_value():
    value_1 = random.randint(1, 6)
    value_2 = random.randint(1, 6)
    dice1.my_dice = pg.image.load(you_dice[value_1-1])
    dice2.my_dice = pg.image.load(you_dice[value_2-1])
    write_in_file("{} {}".format(value_1, value_2), "txt/dice_saving.txt")

def cpu_dice_value():
    value_1 = random.randint(1, 6)
    value_2 = random.randint(1, 6)
    dice1_cpu.my_dice = pg.image.load(cpu_dice_list[value_1-1])
    dice2_cpu.my_dice = pg.image.load(cpu_dice_list[value_2-1])
    final = "{} {}".format(value_1, value_2)
    return final

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

black_light_pieces = [ ]
black_legal_destination = [ ]


L_e = 0

class black_piece:
    def __init__(self, co_ordinates = None):
        self.image = pg.image.load("img/black_got.png")
        self.co_ordinate = co_ordinates
        self.id = "black"
        if self.co_ordinate is not None:
            self.X = self.co_ordinate[0]
            self.Y = self.co_ordinate[1]
        self.id = "black"

class white_piece:
    def __init__(self, co_ordinates = None):
        self.image = pg.image.load("img/white_got.png")
        self.co_ordinate = co_ordinates
        self.id = "white"

        if self.co_ordinate is not None:
            self.X = self.co_ordinate[0]
            self.Y = self.co_ordinate[1]


    def move(self, new_x, new_y):
        self.co_ordinate = position(new_x, new_y)
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

        function = None
        if location < 13:
            function = stack_column_position_top(location)
        else:
            function = stack_column_position_bottom(location)
        self.visible = pg.draw.polygon(screen, (0, 225, 0), function, 2)

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

        if (len(self.elements) == 0) or (len(self.elements) == 1 and self.elements[0].id == opponent) or (len(self.elements) <= 6 and self.elements[0].id == which_piece):
            if self.location < 13:
                light_image = destination
                screen.blit(light_image, position(12-self.location,0))
            else:
                light_image = destination_bottom
                screen.blit(light_image, position(self.location-1-12,7))
            return "on"

    def checking_receiving_light(self, which_piece):
        opponent = None
        if which_piece == "white":
            opponent = "black"
        else:
            opponent = "white"

        if (len(self.elements) == 0) or (len(self.elements) == 1 and self.elements[0].id == opponent) or (len(self.elements) <= 6 and self.elements[0].id == which_piece):
            return "on"



#dice
class cpu_dice:
    def __init__(self, pic):
        self.my_dice = pg.image.load(pic)


blank_cpu = "img/blank_cpu.png"
blank = "img/blank.png"


class player_dice:
    def __init__(self, pic):
        self.my_dice = pg.image.load(pic)

dice1 = player_dice(blank)
dice2 = player_dice(blank)

dice1_cpu = cpu_dice(blank_cpu)
dice2_cpu = cpu_dice(blank_cpu)

#black pieces

black_piece1 = black_piece()#co-ordinates (x, y)
black_piece2 = black_piece()
black_piece3 = black_piece()
black_piece4 = black_piece()
black_piece5 = black_piece()

black_piece6 = black_piece()
black_piece7 = black_piece()
black_piece8 = black_piece()

black_piece9 = black_piece()
black_piece10 = black_piece()
black_piece11 = black_piece()
black_piece12 = black_piece()
black_piece13 = black_piece()

black_piece14 = black_piece()
black_piece15 = black_piece()

#white pieces

white_piece1 = white_piece()
white_piece2 = white_piece()
white_piece3 = white_piece()
white_piece4 = white_piece()
white_piece5 = white_piece()

white_piece6 = white_piece()
white_piece7 = white_piece()
white_piece8 = white_piece()

white_piece9 = white_piece()
white_piece10 = white_piece()
white_piece11 = white_piece()
white_piece12 = white_piece()
white_piece13 = white_piece()

white_piece14 = white_piece()
white_piece15 = white_piece()


#dice button width = 45px, height = 120px
inactive_dice_button = pg.image.load("img/dice_button.png")
active_dice_button = pg.image.load("img/active_dice_button.png")

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
    #first poping from current stack
    deleted_piece = FROM.remove_piece()

    print(white_light_pieces)
    consideration = None

    if turn == "you":
        consideration = white_light_pieces
    else:
        consideration = black_light_pieces

    for i in consideration:
        if i[1] == deleted_piece:
            del i

    to.add_piece(deleted_piece)
    print(len(to.elements))
    print("length of white ligth pieces = ", len(white_light_pieces))
    consideration.append([to, deleted_piece])


    #then push in desired stack
#move()
#move()
empty = []

destination_bottom = pg.image.load("img/destination_light_bottom.png")
destination = pg.image.load("img/destination_light.png")
turn_light = pg.image.load("img/turn_light.png")

cpu_dice_rolled = False
you_dice_rolled = False
temppp = 0
temp = 0
turn = "you"
speed = 2.1
running = True
player_dice1_moved = False
player_dice2_moved = False
light_trigerred = False


# print(stack1.connected)

while running:
    if turn == "you":
        for i in all_stack_list:
            for j in i.elements:
                if j.id == "white":
                    j.image = pg.image.load("img/white_got.png")

    if light_trigerred == True:
        light_white_keys(white_light_pieces)

    # when turn of player is completed
    if player_dice1_moved and player_dice2_moved:
        light_trigerred = False
        you_dice_rolled = False
        player_dice1_moved = False
        player_dice2_moved = False
        for i in white_light_pieces:
            i[1].image = pg.image.load("img/white_got.png")
        white_light_pieces = []
        white_legal_destination = []
        turn = "cpu"
        temp = 0
        temppp = 0


    if turn == "cpu":
        L = []
        for i in all_stack_list:
            if len(i.elements) > 0:
                light_piece = i.elements[-1]
                if light_piece.id == "black":
                    L.append([i, light_piece])
        black_light_pieces = L




    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    # print(mouse)
    screen.fill((0,0,0))
    screen.blit(background_image, (0,0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                white_piece1.move(1,1)

        if event.type == pg.MOUSEBUTTONUP and turn == "you" and 840 <= mouse[0] <= 885 and 440 <= mouse[1] <= 560:
            if event.button == 1:
                light_white_keys(white_light_pieces)
                you_dice_rolled = True
                light_trigerred = True

        # step 5 (movement of player's pieces
        for i in white_light_pieces:
            player_dice = get_from_file()
            if event.type == pg.KEYDOWN:
                d1, d2 = i[0].location - dice_player[0], i[0].location - dice_player[1]
                if click[0] == 1 and i[1].co_ordinate[0] <= mouse[0] <= i[1].co_ordinate[0] + 56 and \
                        i[1].co_ordinate[1] <= mouse[1] <= i[1].co_ordinate[1] + 56:
                    if event.key == pg.K_m:
                        if d1 > 0 and player_dice1_moved == False:
                            print("M is pressed")
                            if all_stack_dict[d1] in white_legal_destination:
                                move(i[0], all_stack_dict[d1])
                                light_white_keys(white_light_pieces)
                                dice1.my_dice = pg.image.load(blank)
                                player_dice1_moved = True

                    if event.key == pg.K_SPACE:
                        if d2 > 0 and player_dice2_moved == False:
                            print("Space is pressed")
                            if all_stack_dict[d2] in white_legal_destination:
                                move(i[0], all_stack_dict[d2])
                                dice2.my_dice = pg.image.load(blank)
                                player_dice2_moved = True


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


    if turn == "you":
        #step 1 (turn on lights)
        turn_on_the_turn_light(turn)

        # step 2 (dice rolling)
        if you_dice_rolled == False:
            if 840 <= mouse[0] <= 885 and 440 <= mouse[1] <= 560:
                screen.blit(active_dice_button, (840, 440))

                if click[0] == 1:
                    dice_value()
            else:
                screen.blit(inactive_dice_button, (840, 440))

        #step 3 (lighting the pieces that are allowed to move)
        L = []
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

            for i in white_light_pieces:
                d1, d2 = i[0].location - dice_player[0], i[0].location - dice_player[1]
                if d1 > 0 and player_dice1_moved == False:
                    if all_stack_dict[d1].checking_receiving_light("white") == "on":
                        temp_destination.append(all_stack_dict[d1])
                if d2 > 0 and player_dice2_moved == False:
                    if all_stack_dict[d2].checking_receiving_light("white") == "on":
                        temp_destination.append(all_stack_dict[d2])

            white_legal_destination = temp_destination
            print(white_legal_destination)

            for i in white_light_pieces:

                if click[0] == 1 and i[1].co_ordinate[0] <= mouse[0] <= i[1].co_ordinate[0] + 56 and i[1].co_ordinate[
                    1] <= mouse[1] <= i[1].co_ordinate[1] + 56:
                    d1, d2 = i[0].location - dice_player[0], i[0].location - dice_player[1]
                    if d1 > 0 and player_dice1_moved == False:
                        all_stack_dict[d1].receiving_light("white")
                    if d2 > 0 and player_dice2_moved == False:
                        all_stack_dict[d2].receiving_light("white")

        #step 5 (movement of pieces)
            #ye uper event waly part mein horaha he line # 567 mein


    if turn == "cpu":
        turn_on_the_turn_light(turn)
        if temp == 0:
            a = cpu_dice_value()
            if temppp != 20:
                temppp +=1
            else:
                write_in_file(a, "txt/cpu_dice_saving.txt")
                temp = 1
                light_black_keys(black_light_pieces)
                cpu_dice_rolled = True
                turn = "you"


    if turn == "cpu" and len(black_light_pieces) > 0 and cpu_dice_rolled == True and False:
        dice_player = get_from_file("txt/cpu_dice_saving.txt")
        print(dice_player)
        for i in black_light_pieces:
            d1, d2 = i[0].location+dice_player[0], i[0].location+dice_player[1]

            if d1 < 25:
                all_stack_dict[d1].receiving_light("black")
            else:
                print("no move possible for this piece")
            if d2 < 25:
                all_stack_dict[d2].receiving_light("black")
            else:
                print("no move possible for this piece")


    screen.blit(dice1.my_dice, (2, 650))
    screen.blit(dice2.my_dice, (2, 720))

    screen.blit(dice1_cpu.my_dice, (2, 210))
    screen.blit(dice2_cpu.my_dice, (2, 285))

    # screen.blit(destination, position(0, 7))

    # print(black_light_pieces)



    # for i in range(13, 25):
    #     bottom_stack = column_stack(i)

    # button("Click", 500, 500, 75, 50, red, yellow)



    # if 550 <= mouse[0] <= 650 and 450 <= mouse[1] <= 500:
    #     pg.draw.rect(screen, (225,225,0), (550, 450, 100, 50))
    # else:
    #     pg.draw.rect(screen, (225,0,0), (550, 450, 100, 50))

    # message_to_screen("Wow", black, (0, 500))


    # screen.blit(pg.image.load(L[L_e]), (0,180))
    # if L_e < 5:
    #     L_e += 1



    pg.display.update()

