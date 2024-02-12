from math import *
import PySimpleGUI as sg
import re
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

def contains_letter(string):
    return bool(re.search('[a-zA-Z]', string))


def plot2d(equation):
    add = 0
    s = equation #Inputs function
    temp = s
    s= s.replace('x','(x)')
    ctr, x, y = -10, [], [] #Setting countert to starting values and x,y to empty lists
    while ctr<=10:
            s1 = ''
            add = 0
            s1 = s.replace('x',str(ctr)) #Replaces variable with value at that point
            try:
                    add = eval(s1) #Tries to evaluate function at that point, if defined
                    y.append(add)
                    x.append(ctr)
            except:
                    pass#If beyond domain, pass
            ctr+=0.1
    #print (x)
    #print (y)
    plt.figure(num ='Plot 2D')
    plt.plot(x,y,label = 'y = '+temp,color = 'black')
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')
    #plt.title(temp.upper())
    #plt.style.use('ggplot')
    ax = plt.gca()
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.1, 1.05))
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',0))
    plt.show()
    plt.close()


def solve_equation(equation_str):
   
    try:
        # Splitting the equation into left-hand side and right-hand side
        lhs, rhs = equation_str.split("=")
        
        x = sp.symbols('x')
        lhs_expr = sp.sympify(lhs)
        rhs_expr = sp.sympify(rhs)
        
        # Constructing the equation using Eq
        equation = sp.Eq(lhs_expr, rhs_expr)
        
        # Solving the equation
        solution = sp.solve(equation, x)
        window['-OUTPUT-'].update(str(solution))
    except (sp.SympifyError, ValueError):
        print("Invalid equation. Please enter a valid equation.")



sg.theme('graygraygray')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.InputText('output',readonly=True, expand_x=True, key="-OUTPUT-")],
            [sg.Text('Enter Expression:')],
            [sg.InputText( key="-INPUT-", )],
            [sg.Button('Ok'), sg.Button('Cancel')],
            [sg.Text('Select Mode:'), sg.Radio('Normal', "RADIO", key='-NORMAL-', default=True), sg.Radio('Plot 2D', "RADIO", key='-PLOT2D-'), sg.Radio('Verify', "RADIO", key='-VERIFY-'), sg.Radio('Solve x', "RADIO", key='-SOLVE-')] ]

# Create the Window
window = sg.Window('Window Title', layout)
# varibles for different modes


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    try:
        if values["-NORMAL-"]:
            solution = eval(values['-INPUT-'])
            window['-OUTPUT-'].update(str(solution))
        elif values["-PLOT2D-"]:
            plot2d(values['-INPUT-'])
        elif values["-SOLVE-"]:
            solve_equation(values['-INPUT-'])
        elif values["-VERIFY-"]:
            window['-OUTPUT-'].update(str(eval(str(values['-INPUT-']).replace("==", "=").replace("=", "=="))))
    except Exception as ex:
        window['-OUTPUT-'].update("Error: " + str(ex))


window.close()