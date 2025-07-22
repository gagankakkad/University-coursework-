#Snake game using tkinter gui

from tkinter import *
import random
root = Tk() #main screen
score = 0
direction = "right" #always start with right turn for snake 
size = 2 # basic size of snake
SPACE_SIZE = 20 # pixel size for snake/food
SPEED = 200 #msec gap between each movement

def sel(): #select difficulty level
  global size #initial size = 2
  global SPEED #initial speed = 200
  selection = var.get() #selection using radiobutton later
  if (selection == 2): #intermediate difficulty
    size = 10
    SPEED = 100
    
  elif (selection == 3): #difficult level
    size = 20
    SPEED = 50

class Snake: # creating snake
  def __init__(self):
    self.body_size = size #initial size
    self.coordinates = [] #location
    self.oval = [] #shape
    for i in range(0, size):
      self.coordinates.append([0, 0])# starting from top left

    for x, y in self.coordinates:#using pixel size and adding to snake size to make snake
      oval = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="red", tag="snake") 
      self.oval.append(oval) #adding to size
      
class Food: #making food
 def __init__(self): 
  x = random.randint(0, (500 / SPACE_SIZE) - 1) * SPACE_SIZE #randomising x and y coordinates within the space - 1
  y = random.randint(0, (500 / SPACE_SIZE) - 1) * SPACE_SIZE
  self.coordinates = [x, y] #assigning coordinate to the food
  canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="yellow", tag="food") #creating food with yellow colour

# Function to check the next move of snake
def next_turn(snake, food):
    x, y = snake.coordinates[0] #initial location of snake 
    #assigning direction to coordinates
    if direction == "up": 
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    oval = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill="red")
    snake.oval.insert(0, oval)
    # if snake touches food then score goes up
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        
        score_label = Label(root, text = "Score = "+ str(score))
        score_label.grid (row = 3, column = 0)
        canvas.delete("food") #delete and recreate food
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.oval[-1])
        del snake.oval[-1]

    if check_collisions(snake): #game ends if snake hits outside background or itself
        game_over()
    else:
        root.after(SPEED, next_turn, snake, food) #continue game

# Function to control direction of snake
def change_direction(new_direction):
    global direction
    if new_direction == 'left':
        if direction != 'right':#making sure direction is not opposite
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

# function to check snake's collision and position
def check_collisions(snake):
    x, y = snake.coordinates[0]#if snake goes beyond the boundary snake dies

    if x < 0 or x >= 500:
        return True
    elif y < 0 or y >= 500:
        return True

    for body_part in snake.coordinates[1:]: #if snake hits part of itself
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

  
  
def game_over():

	canvas.delete(ALL)#delete everything 
	canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 40),text="GAME OVER"+"\nFinal Score= "+ str(score), fill="red",tag="GAME OVER")#display game over and final score
  

def start_game():#start button active
  name = name_box.get()#enter name and age
  age = age_box.get()
  if not name or not age:
    message.config(text="Please enter your name and age!")
    return

  age = int(age)

  if age < 18:#not allowed under 18
    message.config(text="Sorry, you must be 18 or older to play this game!")  
    return
  name_label.grid_forget()#clearing start screen options
  name_box.grid(row = 0, column = 0, columnspan = 1)
  age_box.grid_forget()
  start_button.grid_forget()
  L1.grid_forget()
  L2.grid_forget()
  L3.grid_forget()

  canvas.grid(row=1, column=0)#create canvas snake and food
  snake = Snake()
  food = Food()
  #Binding keypad direction buttons with mainscreen
  root.bind("<Left>", lambda event: change_direction("left"))
  root.bind("<Right>", lambda event: change_direction("right"))
  root.bind("<Up>", lambda event: change_direction("up"))
  root.bind("<Down>", lambda event: change_direction("down"))

  next_turn(snake, food)
  
root.title ("Snake Game") #screen title

name_label = Label(root, text = "Name: ") #main screen name age and difficulty level input by user
name_label.grid (row =0, column = 0)

name_box = Entry(root)
name_box.grid(row=0, column =1)

age_label = Label(root, text = "Age: ")
age_label.grid(row =1, column =0)

age_box = Entry(root)
age_box.grid(row =1, column = 1)

var = IntVar()
#radiobuttons help to choose difficulty 
L1 = Radiobutton(root, text = "Easy", variable = var, value =1, command = sel)
L1.grid(row=3,column =1)
L2 = Radiobutton(root, text = "Intermediate", variable = var, value =2, command = sel)
L2.grid(row=4,column =1)
L3 = Radiobutton(root, text = "Difficult", variable = var, value =3, command = sel)
L3.grid(row=5,column =1)

start_button = Button(root, text = "Start Game", command = start_game)
start_button.grid(row = 6, column = 0) #start button hits start game unless age/name error

message = Label(root, fg = "red") #error mesages
message.grid(row = 8, column = 1)
# mess = Label(root, fg = "red")
# mess.grid(row = 9, column = 1)
canvas = Canvas(root, width = 500, height = 500, bg = "black") #creating game canvas

canvas.grid(row=1, column = 0)

canvas.grid_forget()

root.mainloop()