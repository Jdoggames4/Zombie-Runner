# Jacob Dinkel
# Zombie Runner

import random
from pgzhelper import *

# Screen
WIDTH = 800
HEIGHT = 600
TITLE = "Zombie Runner"
ICON = "ghost.txt"
BG = Actor("background.png")

# Music
music.play("music")

# sky & ground
dark_gray = (50, 50, 50)
yellow = (255, 255, 0)
red = (212, 47, 47)
white = (255, 255, 255)

# Running
velocity = 0
gravity = 1.4
score = 0
game_over = False
over_sound = False
road_offset = 0

# Moon
moon = Actor("moon")
moon.x = 700
moon.y = 80
moon.scale = 0.3

# Houses
houses = Actor("houses")
houses.x = 400
houses.y = 355

# Bat
bat = Actor("bat")
bat.x = 400
bat.y = 100
bat.images = ["bat1", "bat2"]
bat.fps = 3

# Player
zombie = Actor("walk1")
zombie.x = 85
zombie.y = 490
zombie.images = ["walk1",
                 "walk2",
                 "walk3",
                 "walk4",
                 "walk5",
                 "walk6",
                 "walk7",
                 "walk8",
                 "walk9",
                 "walk10"]
zombie.fps = 20

#Ghost
ghost = Actor("ghost")
ghost.x = random.randint(900, 5000)
ghost.y = random.randint(250, 350)
ghost.scale = 0.06


# Obstacles
obstacles = []
obstacles_timeout = 0

def update():
    global velocity
    global gravity
    global score
    global obstacles_timeout
    global game_over
    global over_sound
    global road_offset

    # Bat
    bat.animate()
    bat.x -= 4
    if bat.x < -50:
        bat.x = random.randint(800, 1200)
        bat.y = random.randint(100, 250)

    # Zombie
    zombie.animate()
    if keyboard.space and zombie.y == 470:
        velocity = -23
    zombie.y = zombie.y + velocity
    velocity = velocity + gravity
    if zombie.y > 470:
        zombie.y = 470
        velocity = 0

    # Ghost
    ghost.x -= 5
    if ghost.x < 50:
        ghost.x = random.randint(900, 5000)
        ghost.y = random.randint(250, 350)
    if ghost.colliderect(zombie):
        sounds.collect.play()
        ghost.x = random.randint(900, 5000)
        ghost.y = random.randint(250, 350)
        score += 5

    # Obstacles
    obstacles_timeout += 1
    if obstacles_timeout > random.randint(60, 7000):
        spikes = Actor("spikes")
        spikes.x = 860
        spikes.y = 500
        obstacles.append(spikes)
        obstacles_timeout = 0

    for spikes in obstacles:
        spikes.x -= 8
        if spikes.x < -50:
            obstacles.remove(spikes)
            score += 1

    # Collide
    if zombie.collidelist(obstacles) != -1:
        game_over = True
        obstacles.remove(spikes)

        if over_sound == False:
            sounds.gameover.play()
        over_sound = True

    # Road
    road_offset += 5
    if road_offset > 40:
        road_offset = 0


def draw():
    BG.draw()
    # Road
    screen.draw.filled_rect(Rect(0, 500, 800, 100), (50, 50, 50))
    for i in range(-40, 800, 40):
        screen.draw.filled_rect(Rect(i + road_offset, 545, 20, 5), yellow)

    if game_over:
        BG.draw()
        screen.draw.text("Game Over!",
                        centerx = 380,
                        centery = 150,
                        color = (red),
                        fontname = "creepster",
                        fontsize = 80)
        screen.draw.text("Final Score: " + str(score),
                        centerx = 380,
                        centery = 300,
                        color = (white),
                        fontname = "creepster",
                        fontsize = 60)
        music.stop()
    else:
        moon.draw()
        moon.x -= 0.5
        if moon.x < -50:
            moon.x = 850

        houses.draw()
        bat.draw()
        zombie.draw()
        ghost.draw()

        for spikes in obstacles:
            spikes.scale = 0.4
            spikes.draw()

        screen.draw.text("Score: " + str(score),
                        (20, 20),
                        color = red,
                        fontname = "creepster",
                        fontsize = 30)

