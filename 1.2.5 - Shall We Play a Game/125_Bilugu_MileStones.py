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

#Secondary TODO's: Enemy functions, PowerUp functions

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

    def spawn(self):
        self.Lane = rand.choice(Lanes)
        self.t.goto(300, self.Lane)

    def move(self):
        if self.hp > 0:
            new_x = self.t.xcor() - self.speed
            self.t.setx(new_x)
            if new_x <= -300:
                self.reach_base()
        else:
            self.destroy()
    
    def hit(self, x, y):
        global Score, Base_Damage
        if not game_running:
            return
        self.hp -= Base_Damage
        if self.hp <= 0:
            Score += self.value
            if self.value == 100:
                Base_Damage += 10
            self.destroy()

    def reach_base(self):
        global Base_HP
        Base_HP -= self.damage
        self.destroy()

    def destroy(self):
        self.t.hideturtle()
        if self in Enemies:
            Enemies.remove(self)
#PowerUp Classification:
PowerUps = []

class PowerUp:
    def __init__(self, kind):
        self.kind = kind
        self.t = trtl.Turtle()
        self.t.hideturtle()
        self.t.penup()
        self.t.speed(0)

        if self.kind == "small":
            self.t.shape("circle")
            self.t.shapesize(1, 0.3)
            self.t.color("green")
            self.value = 10
        elif self.kind == "medium":
            self.t.shape("circle")
            self.t.shapesize(1.5, 0.45)
            self.t.color("blue")
            self.value = 20
        elif self.kind == "large":
            self.t.shape("circle")
            self.t.shapesize(2, 0.6)
            self.t.color("cyan")
            self.value = 40
        elif self.t.kind == "skull":
            self.t.shape("circle")
            self.t.shapesize(3, 3)
            self.t.color("white")
            self.value = None

        self.Lane = rand.choice(Lanes)
        self.x = rand.randint(-250, 250)
        self.t.goto(self.x, self.Lane)
        self.t.showturtle()
        self.t.onclik(self.collect)

        if "Easy" in difficulty_positions[0]:
            self.duration = 5000
        elif "Medium" in difficulty_positions[0]:
            self.duration = 4000
        else:
            self.duration = 3000

        wn.ontimer(self.remove, self.duration)

    def collect(self, x, y):
        global Base_HP, Score, Enemies
        if self.kind in ["small", "medium", "large"]:
            Base_HP += self.value
        elif self.kind == "skull":
            gained_points = 0
            for e in Enemies[:]:
                if e.value != 100:
                    gained_points += e.value
                    e.destroy()
            Score += gained_points
        self.remove()

    def remove(self):
        if self in PowerUps:
            self.t.hideturtle()
            self.t.clear()
            PowerUps.remove(self)

#Spawn Enemy
def spawn_enemy():
    if not game_running:
        return
    weights = []
    for etype in available_enemy_types:
        if etype == "E1":
            weights.append(40)
        elif etype == "E2":
            weights.append(30)
        elif etype == "E3":
            weights.append(20)
        elif etype == "Boss":
            weights.append(10)

    enemy_type = rand.choices(population=available_enemy_types, weights=weights, k=1)[0]
