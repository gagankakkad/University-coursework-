# Python program to create a simple root
# calculator using Tkinter
 
# import everything from tkinter module
from tkinter import *
 
# globally declare the expression variable
expression = "" 
 
# Function to update expression
# in the text entry box
def press(num):
    # point out the global expression variable
    global expression
 
    # concatenation of string
    expression = expression + str(num)
 
    # update the expression by using set method
    equation.set(expression) 
 
# Function to evaluate the final expression
def equalpress():
    # Try and except statement is used
    # for handling the errors like zero
    # division error etc.
 
    # Put that code inside the try block
    # which may generate the error
    try:
 
        global expression
 
        # eval function evaluate the expression
        # and str function convert the result
        # into string
        total = str(eval(expression))
 
        equation.set(total)
 
        # initialize the expression variable
        # by empty string
        expression = ""
 
    # if error is generate then handle
    # by the except block
    except:
 
        equation.set(" error ")
        expression = ""
 
 
# Function to clear the contents
# of text entry box
def clear():
    global expression
    expression = ""
    equation.set("")
 
 
# Driver code
if __name__ == "__main__":
    # create a root window
    root = Tk() 
 
    # set the title of root window
    root.title("Simple Calculator")
 
    # set the configuration of root window
    root.geometry("270x150")
 
    # StringVar() is the variable class
    # we create an instance of this class
    equation = StringVar()
 
    # create the text entry box for
    # showing the expression .
    expression_field = Entry(root, textvariable=equation)
 
    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
    expression_field.grid(columnspan=4, ipadx=70)
 
    # create a Buttons and place at a particular
    # location inside the root window .
    # when user press the button, the command or
    # function affiliated to that button is executed .
    button1 = Button(root, text=' 1 ',
                    command=lambda: press(1), height=1, width=7)
    button1.grid(row=2, column=0)
 
    button2 = Button(root, text=' 2 ',
                    command=lambda: press(2), height=1, width=7)
    button2.grid(row=2, column=1)
 
    button0 = Button(root, text=' 0 ',
                    command=lambda: press(0), height=1, width=7)
    button0.grid(row=5, column=0)
 
    plus = Button(root, text=' + ',
                command=lambda: press("+"), height=1, width=7)
    plus.grid(row=2, column=3)
 
    equal = Button(root, text=' = ',
                command=equalpress, height=1, width=7)
    equal.grid(row=5, column=2)
 
    clear = Button(root, text='Clear',
                command=clear, height=1, width=7)
    clear.grid(row=5, column='1')
 
    Decimal= Button(root, text='.',
                    command=lambda: press('.'), height=1, width=7)
    Decimal.grid(row=6, column=0)
    # start the root
    root.mainloop()