#Primary TODO's: Import necessary imports, add essential game variables, create the background

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

#Bonus TODO: Super Boss Enemy

#Super Boss Classification
class Super_Boss:
    def __init__(self):
        self.hp = 10000
        self.speed = 0.25
        self.damage = Base_HP
        self.t = trtl.Turtle()
        self.t.shape("circle")
        self.t.color("darkred")
        self.t.shapesize(10, 10)
        self.t.penup()
        self.t.goto(300, 0)
        self.t.onclick(self.hit)
        self.active = True
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
        elif self.kind == "skull":
            self.t.shape("circle")
            self.t.shapesize(3, 3)
            self.t.color("white")
            self.value = None

        self.Lane = rand.choice(Lanes)
        self.x = rand.randint(-250, 250)
        self.t.goto(self.x, self.Lane)
        self.t.showturtle()
        self.t.onclick(self.collect)

        if "Easy" in difficulty_positions[0]:
            self.duration = 5000
        elif "Medium" in difficulty_positions[1]:
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

    if enemy_type == "E1":
        e = Enemy(10, 4, 10, 10, "yellow")
    elif enemy_type == "E2":
        e = Enemy(20, 2.5, 20, 20, "orange")
    elif enemy_type == "E3":
        e = Enemy(60, 2, 60, 60, "red")
        e.t.shapesize(1.5, 2.5)
    else:
        e = Enemy(100, 0.5, 100, 100, "purple")
        e.t.shapesize(3, 3)
    Enemies.append(e)
    wn.ontimer(spawn_enemy, spawn_interval)

def spawn_powerup():
    if not game_running:
        return
    kind = rand.choices(
        population=["small", "medium", "large", "skull"],
        weights=[50, 30, 15, 5],
        k=1
    )[0]

    p=PowerUp(kind)
    PowerUps.append(p)

    wn.ontimer(spawn_powerup, rand.randint(5000, 15000))

#Tertiary TODO's: Draw Game Stats, Create Game Over Function, Update Enemies Function, Countdown Timer

#Draw Stats
def draw_stats():
    writer.clear()
    writer.goto(-250, 250)
    writer.write(f"Base HP: {Base_HP}", align="center", font=("Arial", 18, "bold"))
    writer.goto(-125, 250)
    writer.write(f"Time: {Remaining_Time}", align="center", font=("Arial", 18, "bold"))
    writer.goto(75, 250)
    writer.write(f"Base Damage: {Base_Damage}", align="center", font=("Arial", 18, "bold"))
    writer.goto(250, 250)
    writer.write(f"Score: {Score}", align="center", font=("Arial", 18, "bold"))

#Game Over
def game_over(victory):
    global game_running, Enemies, PowerUps
    game_running = False
    for e in Enemies[:]:
        e.destroy()
    Enemies.clear()
    writer.clear()
    for p in PowerUps[:]:
        p.destroy()
    PowerUps.clear()
    Lane_Drawer.clear()
    wn.update()
    wn.onclick(None)
    writer.goto(0, 0)
    if victory:
        final_score = Score + difficulty_bonus + length_bonus
        writer.write("Victory", align="center", font=("Arial", 28, "bold"))
        writer.goto(0, -40)
        writer.write(f"Final Score: {final_score}", align="center", font=("Arial", 28, "bold"))
    else:
        writer.write("Defeat", align="center", font=("Arial", 28, "bold"))
    wn.ontimer(show_start_screen, 5000)

#Update Enemies
def update_enemies():
    if not game_running:
        return
    if Base_HP > 0 and Remaining_Time > 0:
        for e in Enemies[:]:
            e.move()
        draw_stats()
        wn.update()
        wn.ontimer(update_enemies, 50)
    else:
        game_over(Base_HP > 0)

#Countdown Timer
def countdown():
    global Remaining_Time
    if not game_running:
        return
    if Remaining_Time > 0 and Base_HP > 0:
        Remaining_Time -= 1
        wn.ontimer(countdown, 1000)
    else:
        game_over(Base_HP > 0)

#Quaternary TODO's: Develop Start Screen, Develop Instruction Screen, Develop Difficulty Selection Screen, Distiniguish Difficulties By Game Play, Add Game Length Selection Screen

#Start Screen
def show_start_screen():
    writer.clear()
    Lane_Drawer.clear()
    writer.goto(0, 50)
    writer.write("Click Defense", align="center", font=("Arial", 28, "bold"))
    writer.goto(0, -20)
    writer.write("Click anywhere to start", align="center", font=("Arial", 18, "normal"))
    wn.onclick(show_instruction_screen)

#Instruction Screen
def show_instruction_screen(x=None, y=None):
    writer.clear()
    writer.goto(0, 200)
    writer.write("HOW TO PLAY", align="center", font=("Arial", 28, "bold"))
    writer.goto(0, 175)
    writer.write("Enemies spawn on the right side of the screen.", align="center", font=("Arial", 20, "normal"))
    writer.goto(0, 150)
    writer.write("They will approach your base, which is on the left side of the screen.", align="center", font=("Arial", 20, "normal"))
    writer.goto(0, 125)
    writer.write("Enemies will die after being clicked on enough times.", align="center", font=("Arial", 20, "normal"))
    writer.goto(0, 100)
    writer.write("Protect your base until the timer runs out.", align="center", font=("Arial", 20, "normal"))
    writer.goto(0, 75)
    writer.write("Click anywhere to proceed.", align="center", font=("Arial", 20, "normal"))
    wn.onclick(show_difficulty_screen)

#Difficulty Selection Screen
def show_difficulty_screen(x=None, y=None):
    writer.clear()
    writer.goto(0, 100)
    writer.write("Select Difficulty", align="center", font=("Arial", 24, "bold"))

    difficulties = ["Easy", "Medium", "Hard"]
    positions = [50, -20, -90]
    global difficulty_positions
    difficulty_positions = list(zip(difficulties, positions))

    for name, pos in difficulty_positions:
        writer.goto(0, pos)
        writer.write(name, align="center", font=("Arial", 18, "bold"))

    wn.onclick(select_difficulty)

#Handle Difficulty Selection
def select_difficulty(x, y):
    global chosen_lanes_temp, chosen_enemies_temp, chosen_spawn_interval_temp
    for name, pos in difficulty_positions:
        if pos-20 < y < pos+20:
            if name == "Easy":
                chosen_lanes_temp = [-75, 0, 75]
                chosen_enemies_temp = ["E1", "E2"]
                chosen_spawn_interval_temp = 2250
            elif name == "Medium":
                chosen_lanes_temp = [-150, -75, 0, 75, 150]
                chosen_enemies_temp = ["E1", "E2", "E3"]
                chosen_spawn_interval_temp = 1500
            else:
                chosen_lanes_temp = All_Lanes[:]
                chosen_enemies_temp = ["E1", "E2", "E3", "Boss"]
                chosen_spawn_interval_temp = 750
            show_game_length_screen()
            break
    global difficulty_bonus
    if name == "Easy":
        difficulty_bonus = 10
    elif name == "Medium":
        difficulty_bonus = 25
    else:
        difficulty_bonus = 50

#Game Length Selection Screen
def show_game_length_screen():
    writer.clear()
    writer.goto(0, 100)
    writer.write("Select Game Length", align="center", font=("Arial", 24, "bold"))

    lengths = [("Blitz", 30), ("Normal", 60), ("Long", 120), ("Extra Long", 180)]
    positions = [50, 0, -50, -100]
    global length_positions
    length_positions = list(zip(lengths, positions))
    for (name, duration), pos in length_positions:
        writer.goto(0, pos)
        writer.write(name, align="center", font=("Arial", 18, "bold"))

    wn.onclick(select_game_length)

#Handle Game Length Selection
def select_game_length(x, y):
    global Game_Duration, Remaining_Time, length_bonus
    for (name, duration), pos in length_positions:
        if pos-20 < y < pos+20:
            Game_Duration = duration
            Remaining_Time = Game_Duration
            if name == "Blitz":
                length_bonus = 50
            elif name == "Normal":
                length_bonus = 100
            elif name == "Long":
                length_bonus = 200
            else:
                length_bonus = 300
            start_game_difficulty(chosen_lanes_temp, chosen_enemies_temp, chosen_spawn_interval_temp)
            break

#Begin Game With Chosen Difficulty
def start_game_difficulty(chosen_lanes, chosen_enemies, chosen_interval):
    global game_running, Base_HP, Base_Damage, Score, Remaining_Time, Lanes, available_enemy_types, spawn_interval, PowerUps
    wn.onclick(None)
    writer.clear()
    Lane_Drawer.clear()
    PowerUps.clear()
    Base_HP = 100
    Score = 0
    Base_Damage = 5
    Remaining_Time = Game_Duration
    Lanes = chosen_lanes
    available_enemy_types = chosen_enemies
    spawn_interval = chosen_interval
    game_running = True
    Draw_Lanes()
    draw_stats()
    spawn_enemy()
    spawn_powerup()
    update_enemies()
    countdown()

#Launch The Game
show_start_screen()
wn.mainloop()