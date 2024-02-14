import PySimpleGUI as sg
import time


layout = [  [sg.Text('Offline geolocation', font='ANY 15')],
            [sg.ProgressBar(100, orientation='h', size=(20, 20), key='progbar')],
            [sg.Text('You are exactly over the center of the earth. :-)', key='_TEXT_', visible=False)],
           [sg.Button('Start', key='-START-'), sg.Button('Cancel')]
         ]

progress_settings = [
    [0, 50, 0.5],  # Start from 0, end at 50, increment quickly
    [50, 90, 1],  # Start from 50, end at 80, increment slowly
    [90, 50, 0.2],  # Start from 80, end at 50, decrement quickly
    [90, 99, 0.1],
    [99, 10, -2],
    [10, 75, 5],
    [75, 100, 1],
    ["STOP", "STOP", "STOP"]
]


window = sg.Window('Offline geo location').Layout(layout) # Yes I'm running out of ideas
run=False
progress=0
progress_index = 0
while True:  # Event Loop
    event, values = window.read(timeout=25)
    if event in (sg.WINDOW_CLOSED, 'Cancel'):
        break
    try:
        if run:
            start, end, speed = progress_settings[progress_index]
            if start == "STOP":
                run=False

            if speed > 0:  # Increment
                progress += speed
                if progress >= end:
                    progress_index = (progress_index + 1) % len(progress_settings)
            else:  # Decrement
                progress += speed
                if progress <= end:
                    progress_index = (progress_index + 1) % len(progress_settings)
            
            window['progbar'].update_bar(int(progress))
    except TypeError:
        window['progbar'].update(visible=False)
        window['_TEXT_'].update(visible=True)
        

    if event == "-START-":
        run = True

window.close()