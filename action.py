import datetime
import speak
import webbrowser
import weather
import os
import random
import smtplib  # for sending emails
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import cv2  # Import OpenCV library
import threading

# Global variable to control the camera
camera_on = False
cap = None

# Function to open camera
def open_camera():
    global camera_on, cap
    if not camera_on:
        cap = cv2.VideoCapture(0)
        camera_on = True

        def show_camera():
            while camera_on:
                ret, frame = cap.read()
                if ret:
                    cv2.imshow('Camera', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        thread = threading.Thread(target=show_camera)
        thread.start()
        speak.speak("Camera is now open")
        return "Camera opened"
    else:
        return "Camera is already open"

# Function to close camera
def close_camera():
    global camera_on, cap
    if camera_on:
        camera_on = False
        cap.release()
        cv2.destroyAllWindows()
        speak.speak("Camera is now closed")
        return "Camera closed"
    else:
        return "Camera is not open"

# Function to track health metrics
def track_health():
    # Placeholder code for tracking health metrics
    calories_burned = random.randint(1, 2000)
    steps_walked = random.randint(1, 2000)
    return f"You have burned {calories_burned} calories and walked {steps_walked} steps today."

# Function to send email
def send_email(recipient, subject, body):
    sender_email = "your_email@example.com"
    sender_password = "your_password"
    smtp_server = "smtp.gmail.com"  # Replace with your SMTP server
    smtp_port = 587  # Replace with your SMTP server's port
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient, text)
        server.quit()
        speak.speak("Email has been sent successfully")
        return "Email sent"
    except Exception as e:
        speak.speak(f"Failed to send email: {str(e)}")
        return f"Failed to send email: {str(e)}"

# Function to send message
def send_message(recipient, message):
    # Placeholder for message sending functionality (e.g., via Twilio or another service)
    speak.speak(f"Message to {recipient}: {message}")
    return f"Message to {recipient}: {message}"

def set_alarm(time):
    current_time = datetime.datetime.now()
    alarm_time = datetime.datetime.strptime(time, "%H:%M")
    time_difference = (alarm_time - current_time).total_seconds()

    if time_difference > 0:
        # Sleep until the alarm time
        time.sleep(time_difference)
        speak.speak("Alarm ringing!")
        return "Alarm ringing!"
    else:
        return "Invalid time. Please provide a future time for the alarm."

# Function to add a note
def add_note(note):
    with open("notes.txt", "a") as file:
        file.write(note + "\n")
    return "Note added successfully."

# Main action function
def Action(send):
    data_btn = send.lower()

    if "what is your name" in data_btn or "who are you" in data_btn or "your introduction" in data_btn:
        response = "My name is Kushal, a virtual assistant"
    elif "hello" in data_btn or "hye" in data_btn or "hay" in data_btn:
        response = "Hey sir, how can I help you?"
    elif "how are you" in data_btn:
        response = "I am doing great these days, sir"
    elif "who is your sir" in data_btn or "who is your owner" in data_btn:
        response = "I Am personal Assistant of Uvesh sir"
    elif "my health" in data_btn:
        response = track_health()  # Call to track health function
    elif "thank you" in data_btn or "thank" in data_btn:
        response = "It's my pleasure, sir, to stay with you"
    elif "good morning" in data_btn:
        response = "Good morning sir, I think you might need some help"
    elif "time now" in data_btn:
        current_time = datetime.datetime.now()
        response = f"{current_time.hour} Hour : {current_time.minute} Minute"
    elif "shutdown" in data_btn or "quit" in data_btn:
        response = "Okay sir"
    elif "set alarm" in data_btn:
        parts = data_btn.split('set alarm ')[1]
        response = set_alarm(parts)
    elif "add note" in data_btn:
        parts = data_btn.split('add note ')[1]
        response = add_note(parts)
    elif "play music" in data_btn or "song" in data_btn:
        webbrowser.open("https://gaana.com/")
        response = "gaana.com is now ready for you, enjoy your music"
    elif 'open google' in data_btn or 'google' in data_btn:
        webbrowser.open('https://google.com/')
        response = "Google opened"
    elif 'send mail' in data_btn or 'send email' in data_btn:
        webbrowser.open('https://gmail.com/')
        response = "gmail opened"
    elif 'youtube' in data_btn or "open youtube" in data_btn:
        webbrowser.open('https://youtube.com/')
        response = "YouTube opened"
    elif 'open wikipedia' in data_btn or 'wikipedia' in data_btn:
        webbrowser.open('https://wikipedia.com/')
        response = "Wikipedia opened"
    elif 'open whatsapp' in data_btn or 'whatsapp' in data_btn:
        webbrowser.open('https://whatsapp.com/')
        response = "WhatsApp opened"
    elif 'weather' in data_btn:
        response = weather.Weather()
    elif 'music from my laptop' in data_btn:
        music_folder = 'D:\\music'
        songs = os.listdir(music_folder)
        if songs:
            os.startfile(os.path.join(music_folder, songs[0]))
            response = "Playing music from your laptop"
        else:
            response = "No music found in the specified folder"
    elif 'send email' in data_btn:
        parts = data_btn.split(';')
        if len(parts) == 4:
            recipient = parts[1].strip()
            subject = parts[2].strip()
            body = parts[3].strip()
            response = send_email(recipient, subject, body)
        else:
            response = "Please provide the email in the format: send email; recipient@example.com; Subject; Email body"
    elif 'send message' in data_btn:
        parts = data_btn.split(';')
        if len(parts) == 3:
            recipient = parts[1].strip()
            message = parts[2].strip()
            response = send_message(recipient, message)
        else:
            response = "Please provide the message in the format: send message; recipient_number; Message body"
    elif 'open camera' in data_btn:
        response = open_camera()
    elif 'close camera' in data_btn:
        response = close_camera()
    else:
        response = "I'm not able to understand!"

    speak.speak(response)
    return response
