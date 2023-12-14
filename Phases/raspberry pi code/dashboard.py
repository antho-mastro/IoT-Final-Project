import dash
import dash_daq as daq
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

import sqlite3
from sqlite3 import Error

from email_sender import *


# MQTT Credentials
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
KEEP_ALIVE = 60
topic = "get-light-intensity"
topic2 = "get-current-tag"
topic3 = "get-current-temperature"
topic4 = "get-current-humidity"




GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ledPin = 21
GPIO.setup(ledPin, GPIO.OUT)

#  For DC Motor
Motor1 = 17 # Enable Pin
Motor2 = 27 # Input Pin
Motor3 = 22 # Input Pin
GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)
GPIO.setup(Motor3,GPIO.OUT)



global current_temperature, current_humidity, current_light_intensity, led_state, fan_state
global uUserID, uTagID, username, uTempThreshold, uHumidityThreshold, uLightThreshold,userState, userLoginState
global current_time, isSentLoginEmail, isSentTempAlertEmail, isSentHumAlertEmail, isSentLightIntensityEmail

current_temperature = 0
current_humidity = 0
current_light_intensity = 0

uTagID = ""
username = ""
uTempThreshold = 0
uHumidityThreshold = 0
uLightThreshold = 0
led_state = False
fan_state = False
userState= False
userLoginState = False
isSentLoginEmail = False
isSentTempAlertEmail = False
isSentHumAlertEmail = False
isSentLightIntensityEmail = False

t = time.localtime()
current_time = time.strftime("%H:%M%p", (time.localtime()))



mqttc = mqtt.Client()
mqttc.connect(MQTT_BROKER, MQTT_PORT, KEEP_ALIVE)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqttc.subscribe(topic)
    mqttc.subscribe(topic2)
    mqttc.subscribe(topic3)
    mqttc.subscribe(topic4)

def on_message(client, userdata, msg):
    global username, uTempThreshold, uHumidityThreshold, uLightThreshold, userState, userLoginState
    global isSentTempAlertEmail, isSentHumAlertEmail, isSentLightIntensityEmail
    isSentTempAlertEmail = False
    isSentHumAlertEmail = False
    isSentLightIntensityEmail = False
    if (msg.topic == topic):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        global current_light_intensity
        current_light_intensity = msg.payload.decode()
        if (int(current_light_intensity) < 100):
            GPIO.output(ledPin, GPIO.HIGH)
            print("LED ON the value is less than 100")
            send_led_on_alert_email(username)
        elif int(current_light_intensity) > 100:
            GPIO.output(ledPin, GPIO.LOW)
            print("LED OFF the value is greater than 100")
            send_led_off_alert_email(username)
        if(userLoginState):
            if round(float(current_light_intensity)) > round(float(uLightThreshold)):
                if not isSentLightIntensityEmail:
                    send_light_intensity_alert_email(username, current_light_intensity)
                    isSentLightIntensityEmail = True
                    print("Light Intensity reach Threshold, Current light intensity is: {}".format(str(current_light_intensity)))
                    
    if (msg.topic == topic2):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic2")
        global uTagID
        if(uTagID!=msg.payload.decode()):
            uTagID = msg.payload.decode()
            logIn(uTagID)

    if (msg.topic == topic3):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic3")

        global current_temperature
        current_temperature = msg.payload.decode()
        if(userLoginState):
            if round(float(current_temperature)) > round(float(uTempThreshold)):
                if not isSentTempAlertEmail:
                    send_temp_alert_email(username, current_temperature)
                    isSentTempAlertEmail = True
                    print("Temperature reach Threshold, Current temperature is: {}".format(str(current_temperature)))

    if (msg.topic == topic4):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic4")
        global current_humidity
        current_humidity = msg.payload.decode()
        if(userLoginState):
            if round(float(current_humidity)) > round(float(uHumidityThreshold)):
                if not isSentHumAlertEmail:
                    send_hum_alert_email(username, current_humidity)
                    print("Humidity reach Threshold, Current Humidity is: {}".format(str(current_humidity)))


mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.loop_start()

# Defining Dash App
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

tempCard = html.Div([
        html.H5("Temperature"),
        html.H5(id='temperature')
    ],
    className="p-4 bg-secondary mb-4 rounded-3 d-flex align-items-center justify-content-between"
)

humCard = html.Div([
        html.H5("Humidity"),
        html.H5(id='humidity')
    ],
    className="p-4 bg-secondary mb-4 rounded-3 d-flex align-items-center justify-content-between"
)

lightIntensityCard = html.Div([
        html.H5("Light Intensity"),
        html.H5(id='light_intensity')
    ],
    className="p-4 bg-secondary mb-4 rounded-3 d-flex align-items-center justify-content-between"
)

ledCard = html.Div([
    html.H5("Light"),
    html.Div(
        daq.ToggleSwitch(
            id='led_button',
            label = ['Off', 'On'],
            value = led_state,
            color='#9eff00'
        )
    )],
    className="p-4 bg-secondary mb-4 rounded-3 d-flex align-items-center justify-content-between"
)

fanCard = html.Div([
    html.H5("Fan"),
    html.Div(
        daq.ToggleSwitch(
            id='fan_button',
            label = ['Off', 'On'],
            value = fan_state,
            color='#9eff00'
        )
    )],
    className="p-4 bg-secondary mb-4 rounded-3 d-flex align-items-center justify-content-between"
)

userLoginCard = dbc.Card(
    html.Div(id='details', children = [
        html.H6("Details",className="mb-4"),
           
            html.P([
                "Username",
                dbc.Input(id="username", value=username, size="md", className=" mb-4 bg-transparent border-bottom border-secondary text-white", readonly=True)
            ]),
            html.P([
                "TagID",
                dbc.Input(id="tagID", value=uTagID, size="md", className=" mb-4 bg-transparent border-bottom border-secondary text-white", readonly=True)
            ]),
            html.P([
                "Temperature Threshold",
                dbc.Input(id="tempThreshold", value=uTempThreshold, size="md", className=" mb-4 bg-transparent border-bottom border-secondary text-white", readonly=False)
            ]),
            html.P([
                "Humidity Threshold",
                dbc.Input(id="humidityThreshold", value=uHumidityThreshold, size="md", className=" mb-4 bg-transparent border-bottom border-secondary text-white", readonly=False)
            ]),
            html.P([
                "Light Intensity Threshold",
                dbc.Input(id="lightIntensity", value=uLightThreshold, size="md", className=" mb-4 bg-transparent border-bottom border-secondary text-white", readonly=False)
            ]),
            html.Button('Update User', id='updateBtn', n_clicks=0),
            html.Div(children="",id="userSaved")
    ]),
    className="p-4"
)


#App Layout
app.layout = dbc.Container(
    [
        dcc.Interval(id='update', n_intervals=0, interval=1000),
        html.Header([
            html.H2("Dashboard"),
            html.H6(id = 'systemTime', children = ["Current time is: ", current_time]),
        ], className = "pt-4 mb-4"),
        html.Hr(),
        dbc.Row([
            dbc.Col(userLoginCard, sm=4),
            dbc.Col([
                tempCard,
                humCard,
                lightIntensityCard,
                ledCard,
                fanCard
            ], sm=8)
        ]),
        html.Hr(),
        
    ]
)


#Time Display
@app.callback(
    Output('systemTime', 'children'),
    Input('update', 'n_intervals'))
def update_time(n_intervals):
    global current_time
    current_time = time.strftime("%H:%M%p", (time.localtime()))
    timeString = 'It is ',current_time
    return timeString



@app.callback(
    Output('temperature', 'children'),
    Input('update', 'n_intervals')
)

def update_temperature(timer):
    global current_temperature
    return (str(current_temperature))

@app.callback(
    Output('humidity', 'children'),
    Input('update', 'n_intervals')
)

def update_humidity(timer):
    global current_humidity
    return (str(current_humidity))

@app.callback(
    Output('light_intensity', 'children'),
    Input('update', 'n_intervals')
)

def update_light_intensity(timer):
    global current_light_intensity
    return (str(current_light_intensity))


@app.callback(
    Output('led_button', 'value'),
    Input('led_button', 'value'),
)

def toggle_led(value):
    global ledState
    if value:
        GPIO.output(ledPin, GPIO.HIGH)
        print("LED ON")
        value = True
        ledState = True
    else:
         GPIO.output(ledPin, GPIO.LOW)
         print("LED OFF")
         value = False
         ledState = False

    return value

@app.callback(
    Output('fan_button', 'value'),
    Input('fan_button', 'value'),
)

def toggle_fan(value):
    global fan_state
    if value:
        GPIO.output(Motor1, GPIO.HIGH)
        GPIO.output(Motor2, GPIO.HIGH)
        GPIO.output(Motor3, GPIO.LOW)
        print("FAN ON")
        fan_state = True
    else:
        GPIO.output(Motor1,GPIO.LOW)
        print("FAN OFF")
        fan_state = False

    return fan_state

@app.callback(
             Output('username', 'value'),
              Output('tagID', 'value'),
             Output('tempThreshold', 'value'),
             Output('humidityThreshold', 'value'),
            Output('lightIntensity', 'value'),
              [Input('update', 'n_intervals'),Input('username', 'value'),
              Input('tagID', 'value'),
             Input('tempThreshold', 'value'),
             Input('humidityThreshold', 'value'),
            Input('lightIntensity', 'value')])

def update_user_info(n_intervals,fullName,tagID,tempThreshold,humidityThreshold,lightIntensity):
    global username,uTagID,uTempThreshold,uHumidityThreshold,uLightThreshold,userState
    if(userState or (username==fullName and uTagID==tagID and
        uTempThreshold==tempThreshold and
        uHumidityThreshold==humidityThreshold and
        uLightThreshold==lightIntensity)):
        userState = False
        return  username, uTagID, str(uTempThreshold), str(uHumidityThreshold), str(uLightThreshold)
    else:
        username=fullName
        uTagID=tagID
        uTempThreshold=tempThreshold
        uHumidityThreshold=humidityThreshold
        uLightThreshold=lightIntensity
        return  fullName, tagID, str(tempThreshold), str(humidityThreshold), str(lightIntensity)

# DB connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def logIn(foundTagID):
    global username, uTempThreshold, uHumidityThreshold, uLightThreshold, uTagID,uUserID, isSentLoginEmail
    isSentLoginEmail = False
    db_file = "database.db"
    conn = create_connection(db_file)
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM users WHERE tagID = ?", [foundTagID])
        user = cur.fetchone()

        if not user:
            print("log in failed")
        else:
            uUserID = user[0]
            uTagID = user[1]
            username = user[2]
            uTempThreshold = user[3]
            uHumidityThreshold = user[4]
            uLightThreshold = user[5]
            global emailLogInSent,userState,userSaved, userLoginState
            print("\tUsername: {}".format(username))
            print("\tuTagID: {}".format(uTagID))
            print("\tuTempThreshold: {}".format(uTempThreshold))
            print("\tuHumidityThreshold: {}".format(uHumidityThreshold))
            print("\tuLightThreshold: {}".format(uLightThreshold))
            print(uTagID,username, uTempThreshold, uHumidityThreshold, uLightThreshold)
            currtime = time.strftime("%H:%M%p", (time.localtime()))
            userState = True
            userLoginState = True
            userSaved=""
            
            if not isSentLoginEmail:
                send_login_alert_email(username, currtime)
                isSentLoginEmail = True
            return user

    finally:
        cur.close()

@app.callback(
    Output('userSaved', 'children'),
    Input('updateBtn', 'n_clicks'),
)
def update_output(n_clicks):
    if(n_clicks>0):
        updateUser()
        return (html.Div(children="User Updated!",className=""))


def updateUser():
    global username, uTempThreshold, uHumidityThreshold, uLightThreshold, uTagID, uUserID,userState
    db_file = "database.db"
    conn = create_connection(db_file)
    cur = conn.cursor()

    try:
        cur.execute("UPDATE users SET tagID = ?, fullName =?, tempThreshold =?, humidityThreshold =?, lightIntensityThreshold =? WHERE userID = ?", (uTagID,username,uTempThreshold,uHumidityThreshold,uLightThreshold,uUserID))

    finally:
        userState=True
        conn.commit()
        conn.close()

#Rasperry Pi Ip
if __name__ == "__main__":
    app.run_server(host='172.20.10.4', port=8050)
    