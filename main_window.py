import pygame as pg
import random

#initializing pygame
pg.init()

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

size = (900, 900)  #a tuple of size (width, height)

screen = pg.display.set_mode(size)
background_image = pg.image.load("img/main_back.png")


L = ["img/you_dice_1.png",
     "img/you_dice_2.png",
     "img/you_dice_3.png",
     "img/you_dice_4.png",
     "img/you_dice_5.png",
     "img/you_dice_6.png"
     ]

L_e = 0

class black_piece:
    def __init__(self, co_ordinates):
        self.image = pg.image.load("img/black_got.png")
        self.co_ordinate = co_ordinates
        self.X = self.co_ordinate[0]
        self.Y = self.co_ordinate[1]

class white_piece:
    def __init__(self, co_ordinates):
        self.image = pg.image.load("img/white_got.png")
        self.co_ordinate = co_ordinates
        self.X = self.co_ordinate[0]
        self.Y = self.co_ordinate[1]

    def move(self, new_x, new_y):
        self.co_ordinate = position(new_x, new_y)
        self.X = self.co_ordinate[0]
        self.Y = self.co_ordinate[1]

        # while self.X != a and self.Y != b:
        #     if self.X < a:
        #         self.X += 1
        #     elif self.X > a:
        #         self.X -= 1
        #
        #     if self.Y < b:
        #         self.Y += 1
        #     elif self.Y > b:
        #         self.Y -= 1


#black pieces

black_piece1 = black_piece(position(6,7))#co-ordinates (x, y)
black_piece2 = black_piece(position(6,8))
black_piece3 = black_piece(position(6,9))
black_piece4 = black_piece(position(6,10))
black_piece5 = black_piece(position(6,11))

black_piece6 = black_piece(position(4,9))
black_piece7 = black_piece(position(4,10))
black_piece8 = black_piece(position(4,11))

black_piece9 = black_piece(position(0,0))
black_piece10 = black_piece(position(0,1))
black_piece11 = black_piece(position(0,2))
black_piece12 = black_piece(position(0,3))
black_piece13 = black_piece(position(0,4))

black_piece14 = black_piece(position(11,0))
black_piece15 = black_piece(position(11,1))

#white pieces

white_piece1 = white_piece(position(6,0))
white_piece2 = white_piece(position(6,1))
white_piece3 = white_piece(position(6,2))
white_piece4 = white_piece(position(6,3))
white_piece5 = white_piece(position(6,4))

white_piece6 = white_piece(position(4,0))
white_piece7 = white_piece(position(4,1))
white_piece8 = white_piece(position(4,2))

white_piece9 = white_piece(position(0,7))
white_piece10 = white_piece(position(0,8))
white_piece11 = white_piece(position(0,9))
white_piece12 = white_piece(position(0,10))
white_piece13 = white_piece(position(0,11))

white_piece14 = white_piece(position(11,10))
white_piece15 = white_piece(position(11,11))





speed = 2.1

running = True

while running:

    screen.fill((0,0,0))
    screen.blit(background_image, (0,0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                white_piece1.move(1,1)



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



    screen.blit(pg.image.load(L[L_e]), (0,180))
    if L_e < 5:
        L_e += 1
    pg.display.update()

