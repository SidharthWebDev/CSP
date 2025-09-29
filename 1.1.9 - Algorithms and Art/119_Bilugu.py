#   a116_buggy_image.py
import turtle as trtl
# instead of a descriptive name of the turtle such as painter,
# a less useful variable name x is used
spooder = trtl.Turtle()

#Ask user about pen size
pen_size = input("Enter how big you want the pen to be.")
fill_color = input("What color do you want the body to be?")

#Create a spider body
spooder.pensize(pen_size)
spooder.fillcolor(fill_color)
spooder.begin_fill()
spooder.circle(100)
spooder.end_fill()
####################

#Configure spider legs
legs = 8
leg_length = int(input("How long do you want the legs to be?"))
leg_angle = 160 / legs
spooder.pensize(pen_size)
spooder.setheading(330)
#######################

#Draw spider legs
leg = 0
while (leg < legs):
  spooder.penup()
  spooder.goto(0,80)
  spooder.pendown()
  spooder.pensize(pen_size)
  if (leg<4):
   spooder.setheading(leg_angle*leg-30)
   spooder.circle(-leg_length,60)
  else: 
   spooder.setheading(leg_angle*leg+70)
   spooder.circle(leg_length,60)
  spooder.penup()
  leg = leg + 1
##################

#Ask user for pen size of the head
pen_size2 = input("How big do you want the pen size to be for the head?")

#Ask user for size of the head
head_size = int(input("How big do you want the head to be?"))

#Ask user for color of the head
head_color = input("What color do you want the head to be?")

#Draw head
spooder.penup()
spooder.goto(0,-30)
spooder.pendown()
spooder.pensize(pen_size2)
spooder.fillcolor(head_color)
spooder.begin_fill()
spooder.circle(15)
spooder.end_fill()
spooder.penup()

#Ask user for eye size
eye_size = int(input("How big do you want the eyes to be?"))

#Ask user for eye color
eye_color = input("What color do you want the eyes to be?")

#Add eyes
spooder.penup()
spooder.goto(20,-40)
spooder.pendown()
spooder.pensize(pen_size)
spooder.color(eye_color)
spooder.circle(eye_size)
spooder.penup()
spooder.goto(-20,-40)
spooder.pendown()
spooder.circle(eye_size)
##########

spooder.hideturtle()
wn = trtl.Screen()
wn.mainloop()