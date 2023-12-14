 # For Sending And Receiving Email
from email.message import EmailMessage
import smtplib, ssl



# Variable For Sending Email
EMAIL_SENDER   =       'anthony.mastronardi2@gmail.com'
EMAIL_RECEIVER =       'tony.mastronardi3@gmail.com'
SMTP_SERVER    =       'smtp.gmail.com'
SMTP_PORT      =        587
APP_PASSWORD   =       'fecywkhswxuxofyi'

#sending email when user login
def send_login_alert_email(user_name, loginTime):
    message = "The current login user is: {}.\nTime: {}".format(user_name, loginTime)
    
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = "User login Alert"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    context=ssl.create_default_context()


    try:
        smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtpObj.starttls(context=context)
        smtpObj.login(msg["From"], APP_PASSWORD)
        smtpObj.send_message(msg)         
        print ("Successfully sent user login alert email")
        
    except smtpObj.SMTPException as e:
        print ("Error: unable to send login alert email: " + str(e))


# Sending Temperature Alert Email
def send_temp_alert_email(user_name, temperatureValue):
    message = "Login User: {}. \nThe current temperature is: {}.".format(user_name, temperatureValue)
    
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = "Current Temperature Reach Threshold Level"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    context=ssl.create_default_context()


    try:
        smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtpObj.starttls(context=context)
        smtpObj.login(msg["From"], APP_PASSWORD)
        smtpObj.send_message(msg)         
        print ("Successfully sent temperature alert email ")
        
    except smtpObj.SMTPException as e:
        print ("Error: unable to send temerature alert email: " + str(e))


# Sending Humidity Alert Email
def send_hum_alert_email(user_name, humidityValue):
    message = "Login User is: {}.\n The current humidity is {}.".format(user_name, humidityValue)
    
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = "Current Humidity Reach Threshold Level"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    context=ssl.create_default_context()


    try:
        smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtpObj.starttls(context=context)
        smtpObj.login(msg["From"], APP_PASSWORD)
        smtpObj.send_message(msg)         
        print ("Successfully sent humidity alert email ")
        
    except smtpObj.SMTPException as e:
        print ("Error: unable to send humidity alert email: " + str(e))


# Sending Light Intensity Alert Email
def send_light_intensity_alert_email(user_name, lightIntensityValue):
    message = "Login User is: {}.\n The current light intesity value is {}.".format(user_name, lightIntensityValue)
    
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = "Current Light Intensity Reach Threshold Level"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    context=ssl.create_default_context()


    try:
        smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtpObj.starttls(context=context)
        smtpObj.login(msg["From"], APP_PASSWORD)
        smtpObj.send_message(msg)         
        print ("Successfully sent light intesity alert email ")
        
    except smtpObj.SMTPException as e:
        print ("Error: unable to send light intesity alert email: " + str(e))

# Sending LED On Alert Email
def send_led_on_alert_email(user_name):
    message = "Login User is: {}.\n The LED turned On beacuse light intensity value less than 100. .\nTime: {}".format(user_name)
    
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = "LED Turned On Alert"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    context=ssl.create_default_context()


    try:
        smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtpObj.starttls(context=context)
        smtpObj.login(msg["From"], APP_PASSWORD)
        smtpObj.send_message(msg)         
        print ("Successfully sent led on alert email ")
        
    except smtpObj.SMTPException as e:
        print ("Error: unable to send led on alert email: " + str(e))

# Sending LED OFF Alert Email
def send_led_off_alert_email(user_name):
    message = "Login User is: {}.\n The LED turned OFF beacuse light intensity value is greater than 100.".format(user_name)
    
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = "LED Turned OFF Alert"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    context=ssl.create_default_context()


    try:
        smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtpObj.starttls(context=context)
        smtpObj.login(msg["From"], APP_PASSWORD)
        smtpObj.send_message(msg)         
        print ("Successfully sent led off alert email ")
        
    except smtpObj.SMTPException as e:
        print ("Error: unable to send led off alert email: " + str(e))