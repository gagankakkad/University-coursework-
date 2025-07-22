import time #useful to measure process speed
import re
def cocktail_sort(numbers): #define function cocktail sort
  startTime = time.time() #timer start
  length = len(numbers)-1; #setting length of string
  for i in range(length, 0, -1): #starting comparison from right end
    is_swapped = False #no need to swap 1st item on list
    

    for j in range(i, 0, -1):
      if numbers[j]<numbers[j-1]: #comparing right to left
        temp = numbers[j] #swapping numbers
        numbers[j] = numbers[j-1]
        numbers[j-1] = temp
        is_swapped = True #swap complete
        
    for j in range(i):
      if numbers[j]> numbers[j+1]: #compare left to right
        temp = numbers[j] #swapping numbers
        numbers[j] = numbers[j+1]
        numbers[j+1] = temp
        is_swapped = True # swap completed
        
    if not is_swapped: #either no swapping left or no need for swapping
      endTime = time.time() #stop timer
      howMuchTime = endTime - startTime
    
      print("Procedure time = " + str(howMuchTime) + " sec") #print performance
      return numbers
  
  
    
def insertion_sort(numbers): #function for insertion sort
  startTime = time.time() #timer start
  length = len(numbers); #length defined
  for i in range (1, length):
    position = i; #set counter from 2nd position to compare
    temp = numbers[i] #2nd number in list saved
    while position>0 and numbers[position-1]>temp: # compare 1st with 2nd, if 1st>2nd swap numbers
      
      numbers[position]=numbers[position-1]
      position = position-1 #counter reset
      
    numbers[position]=temp # numbers swapped
    #loop till you reach end
    
  endTime = time.time() #stop timer
  howMuchTime = endTime - startTime
    
  print("Procedure time = " + str(howMuchTime) + " sec") #print performance
#time used to perform the sorting function
    
def main():
  print("Welcome to Sorting Algorithm")
  response = input("Would you like to sort numbers or strings?\n")    #sort numbers or strings
  
  if response.rstrip() =='numbers' or response.rstrip() == 'Numbers':
    
    num = input('Please enter numbers to sort seperated by ,\n').strip()# creating list
  
    number = [int(item) for item in re.findall(r'-?\d+',num)]#cocktail sort
    #length = len(number
   
   
    number2= [int(item) for item in re.findall(r'-?\d+',num)]#insertion sort
    
    print("Numbers added by user = ", number)
    
    
    cocktail_sort(number)#call function for cocktail sort
    print("Cocktail sort = ", number) #printing sorted function
    
    
    print("Numbers added by user =", number2)#numbers input by user
    insertion_sort(number2)#  call insertion sort function
    print("Insertion sort = ", number2) #printing sorted function
    return
  if response.rstrip() == 'strings' or response.rstrip() == 'Strings':#extra function added to assignment
    string = input("Please enter a statement to be sorted according to ASCI code.\n")#enter string to sort 
    length = len(string) #length of entered string
    number3 = []
    for i in range(0,length):
      number3.append(ord(string[i]))#converting string to int list using asci values
      #print(number3)
      
    cocktail_sort(number3)#sorting using cocktail function
    string2 = []
    for i in range(0, length):
      string2.append(chr(number3[i]))#converting int asci code to char values
    #print(chr(number3()))
    print("Cocktail sort =", string2)# string sorted using cocktail 
    return
  else:
    print("Invalid response program terminated!")
  
    

def get_response(prompt): #verify input value is integer only
  while True:
        try:
            return int(input(prompt))# return value if int only
        except ValueError:
            pass
      
if __name__ == "__main__":
  
  main()
  