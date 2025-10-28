#Primary TODO's: Develop main game screen, establish enemy function, add Base HP,  add game timer, add score counter, establish base player damage
#Imports
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
        self.face = trtl.Turtle()
        self.face.hideturtle()
        self.face.penup()
        self.face.speed(0)
        self.face.color("black")
        self.draw_face()
    
    def draw_face(self):
        self.face.clear()
        x = self.t.xcor()
        y = self.t.ycor()

        if self.value == 100:
            self.face.color("red")
            eye_size = 6
            mouth_width = 10
        else:
            self.face.color("black")
            eye_size = 4
            mouth_width = 8

        self.face.goto(x - 5, y + 5)
        self.face.dot(eye_size)
        self.face.goto(x + 5, y + 5)
        self.face.dot(eye_size)

        self.face.goto(x - mouth_width/2, y - 2)
        self.face.setheading(-60)
        self.face.pendown()
        self.face.circle(mouth_width, 120)
        self.face.penup()


    def spawn(self):
        self.Lane = rand.choice(Lanes)
        self.t.goto(300, self.Lane)

    def move(self):
        if self.hp > 0:
            new_x = self.t.xcor() - self.speed
            self.t.setx(new_x)
            self.draw_face()
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
        self.face.clear()
        self.face.hideturtle()
        if self in Enemies:
            Enemies.remove(self)