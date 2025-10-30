#Primary TODO's: Import necessary imports, add essential game variables, create the background

import turtle as trtl
import random as rand

#Game Variables
Base_HP = 100
Score = 0
Game_Duration = 30
Remaining_Time = Game_Duration
Enemies = []
All_Lanes = [-225, -150, -75, 0, 75, 150, 225]
Lanes = All_Lanes[:]
game_running = False
spawn_interval = 1000
available_enemy_types = ["E1", "E2", "E3", "Boss"]
difficulty_bonus = 0
length_bonus = 0
Base_Damage = 5

#Storage For Difficulty Selection
chosen_lanes_temp = []
chosen_enemies_temp = []
chosen_spawn_interval_temp = 1000

#Background
wn = trtl.Screen()
wn.tracer(False)
wn.title("Click-Defense Game")
wn.bgcolor("black")

#Writer
writer = trtl.Turtle()
writer.hideturtle()
writer.color("white")
writer.penup()

Lane_Drawer = trtl.Turtle()
Lane_Drawer.hideturtle()
Lane_Drawer.color("red")
Lane_Drawer.pensize(1)
Lane_Drawer.speed(0)

#Draw Lanes
def Draw_Lanes():
    Lane_Drawer.clear()
    Lane_Drawer.penup()
    for y in Lanes:
        Lane_Drawer.goto(-300, y)
        Lane_Drawer.pendown()
        Lane_Drawer.goto(300, y)
        Lane_Drawer.penup()

#Secondary TODO's: Enemy functions

#Enemy Classification
class Enemy:
    def __init__(self, hp, speed, damage, value, color):
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.value = value
        self.t = trtl.Turtle()
        self.t.shape("circle")
        self.t.color(color)
        self.t.penup()
        self.t.speed(0)
        self.spawn()
        self.t.onclick(self.hit)
        