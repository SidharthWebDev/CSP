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