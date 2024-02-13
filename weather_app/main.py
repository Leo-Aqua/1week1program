import requests
import PySimpleGUI as sg
import webbrowser
import os
import json


def weather(key,region):
    url = "http://api.weatherapi.com/v1/current.json"
    response = requests.get(url, params={
        "key":key,
        "q":region,
        "aqi": "yes"
    })
    data = response.json()
    return data

def downlaod_icon(icon):
    icon = "https:" + icon.replace("64x64", "128x128")
    req = requests.get(icon)
    if req.status_code != 200:
        print("Could not load image")
        return
    with open(os.path.dirname(os.path.realpath(__file__)) + '/icon.png', 'wb') as f:
        f.write(req.content)

def autocomplete(values, key):
    url = "http://api.weatherapi.com/v1/search.json"
    response = requests.get(url, params={
        "key":key,
        "q":values
    })
    data = response.json()
    return data






sg.theme('graygraygray')   # Add a touch of color


# Output related variables
updated_at = ""
temp_c = ""
temp_f = ""
weather_condition = ""
icon = ""
wind_mph = ""
wind_kph = ""
wind_degree = ""
wind_dir = ""
uv = ""
humidity = ""
feelslike_c = ""
feelslike_f = ""
co = ""
no2 = ""
o3 = ""
so2 = ""

# All the stuff inside window.
layout = [  
    [sg.Text('This is a simple weather app! Enter your api key and region below:')],
    [sg.Text("Get your API key", enable_events=True,key=f'-URL-', text_color='blue')],
    [sg.Text('Api key'), sg.InputText(key='-KEY-', password_char='*', enable_events=True), sg.Button('Save key', key='-SAVE-'), sg.Button('Open key', key='-OPENKEY-')],
    [sg.Text('Region'), sg.InputText(key='-REGION-', expand_x=True, enable_events=True, disabled=True)],
    [sg.Listbox([],size=(20,5), expand_x=True, key="-REGIONLIST-", disabled=True, enable_events=True)],
    [sg.Button('Ok'), sg.Button('Cancel')],
    [sg.Text('The weather in your region is: ')],
    [sg.Text(f"""
Updated at {updated_at}
Temperature: {temp_c}°C / {temp_f}°F
Feels like : {feelslike_c}°C / {feelslike_f}°F
Humidity: {humidity}
Condition: {weather_condition}
Wind: {wind_mph} mph / {wind_kph} kph
Wind direction: {wind_dir} / {wind_degree}°
UV index: {uv}
Air Quality:
CO: {co}
NO2: {no2}
O3: {o3}
SO2: {so2}
""", key='-OUTPUT-'), sg.Image(data=icon, key='-ICON-')],
]
# Create the Window
window = sg.Window('Weather App', layout)






while True:
    
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Ok':
        data = weather(values['-KEY-'],values['-REGION-'])
        json_data = json.loads(json.dumps(data))
        updated_at = json_data["current"]["last_updated"]
        temp_c = json_data["current"]["temp_c"]
        temp_f = json_data["current"]["temp_f"]
        weather_condition = json_data["current"]["condition"]["text"]
        icon = json_data["current"]["condition"]["icon"]
        wind_mph = json_data["current"]["wind_mph"]
        wind_kph = json_data["current"]["wind_kph"]
        wind_degree = json_data["current"]["wind_degree"]
        wind_dir = json_data["current"]["wind_dir"]
        uv = json_data["current"]["uv"]
        humidity = json_data["current"]["humidity"]
        feelslike_c = json_data["current"]["feelslike_c"]
        feelslike_f = json_data["current"]["feelslike_f"]
        co = json_data["current"]["air_quality"]["co"]
        no2 = json_data["current"]["air_quality"]["no2"]
        o3 = json_data["current"]["air_quality"]["o3"]
        so2 = json_data["current"]["air_quality"]["so2"]
        window["-OUTPUT-"].update(
            f"""
Updated at {updated_at}
Temperature: {temp_c}°C / {temp_f}°F
Feels like : {feelslike_c}°C / {feelslike_f}°F
Humidity: {humidity}
Condition: {weather_condition}
Wind: {wind_mph} mph / {wind_kph} kph
Wind direction: {wind_dir} / {wind_degree}°
UV index: {uv}
Air Quality:
CO: {co}
NO2: {no2}
O3: {o3}
SO2: {so2}
"""
        )
        downlaod_icon(icon)
        window["-ICON-"].update(os.path.dirname(os.path.realpath(__file__)) + '/icon.png')
    if event == '-URL-':
        webbrowser.open('https://www.weatherapi.com/signup.aspx')
    if event == '-SAVE-':
        with open(os.path.dirname(os.path.realpath(__file__))+'/api.key', 'w') as f:
            f.write(values['-KEY-'])
        window["-REGION-"].update(disabled=False)
        window["-REGIONLIST-"].update(disabled=False)
    if event == '-OPENKEY-':
        with open(os.path.dirname(os.path.realpath(__file__))+'/api.key', 'r') as f:
            window["-KEY-"].update(str(f.read()))
            f.close()
        window["-REGION-"].update(disabled=False)
        window["-REGIONLIST-"].update(disabled=False)
    
    if event == '-REGION-':
        
        data = autocomplete(values['-REGION-'],values['-KEY-'])
        try:
            list_list = []
            for i in data:
                name = i["name"]
                country = i["country"]
                listbox_string = f"{name}, {country}"
                list_list.append(listbox_string)
            # json_data = json.loads(json.dumps(data[0]))
            # print(json_data)
            
            
            window["-REGIONLIST-"].update(list_list)
        except:
            pass
    if event == '-KEY-':
        window["-REGION-"].update(disabled=False)
        window["-REGIONLIST-"].update(disabled=False)
    
    if event == '-REGIONLIST-':
        window["-REGION-"].update(values['-REGIONLIST-'][0])
        
window.close()