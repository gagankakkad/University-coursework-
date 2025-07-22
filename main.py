import random #Generate a number from spinning the roulette
import time #timer to set 45 seconds to bet
import click #clear screen
import pytest
red = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36] #setting numbers for red rest are black except 0
#c_1 = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34] #like red and black columns can be used to bet on for 3 to 1 odds
#c_2 = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
#c_3 = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
customer = ["a", "b", "c", "d", "e"] #creating a list to be later converted into objects 
class Customer: #class of customers created
    def __init__(self, name, age, deposit, winnings):
        self.name = name
        self.age = age#min age set as 18 can be changed
        self.deposit = deposit
        self.winnings = winnings

class Bet: #setting betting class
  def __init__(type, number, colour, parity, len):
    type.number = number
    type.colour = colour
    type.parity = parity
    #type.rows = rows #other bets i intended to create in case of extension
    # type.column = column
    # type.firsthalf = firsthalf
    # type.lasthalf = lasthalf
    type.len = len
def main():
  print("Welcome to Roulette game")
  response = input("Would you like to read the game rules? ")#basic rules to explain the game
  
  if response.rstrip() == 'yes' or response == 'Yes':
    
    print("Basic rules of the game as follows")
    print("Minimum Customer = 1 maximum = 5.\nMinimum age of each customer is 18 ")
    print("Minimum deposit = £50 maximum = £100,000")
    print("Minimum bets on numbers including 0 = £1, side bets(Colour, rows, columns etc.) = £5")
    print("0 excludes any side bets")
  
  input("Press enter to start game")#blank verification
  i = get_int("Please enter number of players ")#max limit 5
  j = i
  while i<=0 or i>= 6:
    print("Invalid number of players, min 1 max 5")
    i = get_int("Please enter right number of players ")
  while (i!= 0):
    customer[i-1] = customer_details()#creating objects in reverse order to store customer data
    print(f"{customer[i-1].name} and {customer[i-1].age}")
    i-=1
  #winnings =0
  clrscr()#clearing screen after input
  print("Customer data stored!")
  
  resp = input("Would you like to bet? ")
  
  while resp == 'yes' or resp =='Yes':# start loop to play 
    spin = int(roll())#spin the dial
    test_random(spin)
    color = is_red(spin)# check to see if colour is red black or 0
    
    par = is_even(spin)  # check if odd or even, some games allow 0 as even  
    
    for i in range(0, j): #starting betting procedure
      print("\nBets open for: ", customer[i].name) #customer 0 to begin with
      start_time = time.time()# starting timer
      timer = start_time + 45#setting time to 45 seconds
      bet = place_bet() #activating bets
      end_time = time.time()#end time once bets have been placed
      diff = end_time - timer #checking if bets are valid within 45 seconds
      if diff>0:
        print("No bets taken bets are void") #sorry too late
      else:
        print("Numbers to bet on", bet.number) #bets accepted, place bets on numbers as many times as you like 
      #print("Bet len = ", bet.len)
        customer[i].deposit = customer[i].deposit - bet.len
        if bet.colour =='Red' or bet.colour =='Black': #deduct if bet on colours
          print("Colour bet = ", bet.colour)
          customer[i].deposit = customer[i].deposit - 5
        if bet.parity =='Even' or bet.parity =='Odd': #deduct if bet on parity
          print("Parity bet = ", bet.parity)
          customer[i].deposit = customer[i].deposit - 5
      
        print("New Balance = ", customer[i].deposit) # balance after bets
    
        for _ in range(0, bet.len): #if bet number matches the spin
          if spin == bet.number[_]: # win 36 to 1 
            customer[i].winnings = customer[i].winnings + 36
    
        if color == bet.colour: #if bet matches the colour win 2 to 1
          customer[i].winnings = customer[i].winnings + 5
              
        if par == bet.parity: #win 2 to 1 for even or odd
          customer[i].winnings = customer[i].winnings + 5
       

    print("=======================================================")  
    print("Winning number is: ", spin)#print detailsfor winning number
    print(color) 
    print(par)
    print("=======================================================")
    for i in range(0, j):#print winnings for each customer and new balance
      print("Total winnings for",customer[i].name, " = ",customer[i].winnings)
      customer[i].deposit = customer[i].deposit + customer[i].winnings
      print("New Balance = ", customer[i].deposit)
      customer[i].winnings = 0
    
    resp = input("Would you like to bet again? ") #loop complete to play again

    clrscr()
  print("Thank you for playing. Hope you enjoyed the simulation!")
 
def customer_details(): #entering customer details
  #customer = customer_details()
  name = input("Name: ")
  while name == "":
    print("Invalid name")
    name = input("Name: ")
    
  age = get_int("Age = ")
  while age <18:#age restriction
    print("Entry denied player has to be over 18.")
    age = get_int("Age = ")
  winnings = 0    
  deposit = get_int("Balance = £")
  while deposit<50 or deposit>100000:#deposit restrictions
    print("Deposit range has to be £50 to £100,000")
    deposit = get_int("Balance = £")
  customer = Customer(name, age, deposit, winnings)#creating objects 
  return customer  
  
def roll(): #randomised number generator
    spin = random.randint(0,36)
    
    return spin  
def is_even(n):#check to see if number is even or odd
  return ("Even") if n%2 ==0 else ("Odd")

def is_red(n):#check to see if number is in red range else 0 or black 
  i=0
  y = len(red)
  #print("Array length = ", y)#for testing
  while(red[i] !='0'):
    if n==0:
      print ("Zero: green")
      return
    elif n == red[i]:
      
      return ("Red")
    elif i == y-1 and n!= red[i]:
      print 
      return ("Black")
    i+=1
def place_bet():# assigning bet values
  number = [] #creating a blank list of numbers to bet on
  len = get_int("How many numbers to bet on ")
  for i in range(0, len):
    num = get_int("Input numbers to bet between 0 to 36: ")
    #test_random(num) for testing
    while num<0 or num>36:
      print("Invalid input try again")
      num = get_int("Input numbers to bet between 0 to 36: ")
    
    number.append(num) #adding to pre populated list
  colour = input("Colour - ") # colour Red or Black
  parity = input("Even or Odd parity - ") # Even or odd input
  # rows = input("Rows bet 1-12 or 13-24 or 25-36 - ")
  # column = input("Column number = ")
  # firsthalf = input("First 18 = ")
  # lasthalf = input("Second 19 = ")
  bet = Bet(number, colour, parity, len)# return bet to object created
  return bet
def clrscr():
   # Clear screen using click.clear() function
    click.clear()
def get_int(prompt): #verify input value is integer only
  while True:
        try:
            return int(input(prompt))# return value if int only
        except ValueError:
            pass

def test_random(spin):
  assert spin>=0
  assert spin<=36

if __name__ == "__main__":
  main()