import gradio as gr
import wikipedia
import pywhatkit
import speech_recognition as sr
import datetime
import time
import threading
import pyautogui
from gtts import gTTS
from playsound import playsound
import os
import random

# ----------------- Wikipedia -----------------
def search_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options}"
    except Exception as e:
        return f"Error: {str(e)}"

# ----------------- WhatsApp -----------------
def send_whatsapp_message(number, message):
    try:
        pywhatkit.sendwhatmsg_instantly(f"+{number}", message, wait_time=10, tab_close=True)
        time.sleep(15)
        pyautogui.press('enter')
        return "Message sent successfully!"
    except Exception as e:
        return f"Failed to send message: {str(e)}"

# ----------------- Reminders -----------------
reminders = []

def speak_reminder(message):
    tts = gTTS(text=message, lang='en')
    filename = "reminder.mp3"
    tts.save(filename)
    try:
        playsound(filename)
    except Exception as e:
        print(f"Error playing sound: {str(e)}")
    finally:
        os.remove(filename)  # Ensure file is deleted after playing

def set_reminder(reminder_time, reminder_message):
    try:
        reminder_time = datetime.datetime.strptime(reminder_time, "%Y-%m-%d %H:%M:%S")
        reminders.append({"time": reminder_time, "message": reminder_message})
        return f"Reminder set for '{reminder_message}' at {reminder_time}"
    except ValueError:
        return "Invalid time format. Use YYYY-MM-DD HH:MM:SS."

def check_reminders():
    while True:
        for reminder in reminders[:]:
            if datetime.datetime.now() >= reminder["time"]:
                speak_reminder(f"Reminder alert: {reminder['message']}")
                reminders.remove(reminder)
        time.sleep(10)

# ----------------- Voice Command -----------------
def listen_for_commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        try:
            audio = r.listen(source, timeout=5)
            command = r.recognize_google(audio)
            return f"You said: {command}"
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError:
            return "Error with the speech recognition service."
        except sr.WaitTimeoutError:
            return "Listening timed out."

# ----------------- Extra Features -----------------
def get_datetime():
    now = datetime.datetime.now()
    return now.strftime("Today is %A, %d %B %Y and the time is %I:%M %p")

def get_quote():
    quotes = [
        "Believe in yourself!",
        "Stay focused and never give up.",
        "Make each day your masterpiece.",
        "Push yourself, because no one else will."
    ]
    return random.choice(quotes)

def calculate(expression):
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Invalid expression"

todo_list = []

def add_todo(task):
    todo_list.append(task)
    return "Task added."

def view_todo():
    return "\n".join(f"{i+1}. {task}" for i, task in enumerate(todo_list)) if todo_list else "No tasks yet."

# ----------------- Music Player -----------------
def play_music():
    try:
        pywhatkit.playonyt("https://www.youtube.com/watch?v=D0uGcfKJU_w")  # Example: "Happy" by Pharrell Williams
        return "Playing music on YouTube."
    except Exception as e:
        return f"Error playing music: {str(e)}"

# ----------------- Health Reminders -----------------
def health_reminders():
    reminders = [
        "Drink water! Stay hydrated.",
        "Take a walk! Stretch your legs.",
        "Time for a break! Rest your eyes.",
        "Don't forget to smile today!"
    ]
    while True:
        random_reminder = random.choice(reminders)
        speak_reminder(random_reminder)
        time.sleep(random.randint(1800, 3600))  # Random reminder every 30 minutes to 1 hour

# ----------------- Games -----------------
def rock_paper_scissors(user_choice):
    choices = ["rock", "paper", "scissors"]
    computer_choice = random.choice(choices)
    if user_choice == computer_choice:
        return f"Computer chose {computer_choice}. It's a tie!"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        return f"Computer chose {computer_choice}. You win!"
    else:
        return f"Computer chose {computer_choice}. You lose!"

def number_guessing_game(user_guess):
    secret_number = random.randint(1, 10)
    if user_guess == secret_number:
        return "Congratulations! You guessed the number correctly!"
    else:
        return f"Oops! The correct number was {secret_number}. Try again!"

# ----------------- Gradio Interface -----------------
def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("## 🤖 Personal Assistant with Gradio")

        with gr.Tab("🔍 Wikipedia Search"):
            query = gr.Textbox(label="Enter Search Term")
            result = gr.Textbox(label="Wikipedia Result", interactive=False)
            query.submit(search_wikipedia, inputs=query, outputs=result)

        with gr.Tab("💬 Send WhatsApp"):
            number = gr.Textbox(label="Phone Number (include country code, e.g., 91XXXXXXXXXX)")
            message = gr.Textbox(label="Message")
            btn = gr.Button("Send WhatsApp Message")
            output = gr.Textbox(label="Status", interactive=False)
            btn.click(send_whatsapp_message, inputs=[number, message], outputs=output)

        with gr.Tab("⏰ Set Reminder"):
            r_time = gr.Textbox(label="Time (YYYY-MM-DD HH:MM:SS)")
            r_msg = gr.Textbox(label="Reminder Message")
            btn_remind = gr.Button("Set Reminder")
            remind_status = gr.Textbox(label="Reminder Status", interactive=False)
            btn_remind.click(set_reminder, inputs=[r_time, r_msg], outputs=remind_status)

        with gr.Tab("🎤 Voice Command"):
            voice_btn = gr.Button("Listen")
            voice_result = gr.Textbox(label="Heard Command", interactive=False)
            voice_btn.click(listen_for_commands, outputs=voice_result)

        with gr.Tab("📅 Date and Time"):
            dt_btn = gr.Button("Tell me the time")
            dt_output = gr.Textbox(label="Current Date and Time", interactive=False)
            dt_btn.click(get_datetime, outputs=dt_output)

        with gr.Tab("💡 Motivation"):
            quote_btn = gr.Button("Get Quote")
            quote_output = gr.Textbox(label="Daily Motivation", interactive=False)
            quote_btn.click(get_quote, outputs=quote_output)

        with gr.Tab("🧮 Calculator"):
            calc_input = gr.Textbox(label="Enter Expression (e.g., 5 * (2 + 3))")
            calc_output = gr.Textbox(label="Result", interactive=False)
            calc_input.submit(calculate, inputs=calc_input, outputs=calc_output)

        with gr.Tab("📝 To-Do List"):
            todo_input = gr.Textbox(label="Add Task")
            todo_btn = gr.Button("Add to List")
            todo_view_btn = gr.Button("Show To-Do List")
            todo_output = gr.Textbox(label="To-Do List", interactive=False)
            todo_btn.click(add_todo, inputs=todo_input, outputs=todo_output)
            todo_view_btn.click(view_todo, outputs=todo_output)

        with gr.Tab("🎵 Play Music"):
            music_btn = gr.Button("Play YouTube Song")
            music_status = gr.Textbox(label="Music Player Status", interactive=False)
            music_btn.click(play_music, outputs=music_status)

        with gr.Tab("🎮 Rock Paper Scissors"):
            game_choice = gr.Radio(choices=["rock", "paper", "scissors"], label="Choose Rock, Paper, or Scissors")
            game_result = gr.Textbox(label="Game Result", interactive=False)
            game_choice.change(rock_paper_scissors, inputs=game_choice, outputs=game_result)

        with gr.Tab("🎯 Number Guessing Game"):
            guess_input = gr.Number(label="Guess a number between 1 and 10")
            guess_result = gr.Textbox(label="Guessing Game Result", interactive=False)
            guess_input.submit(number_guessing_game, inputs=guess_input, outputs=guess_result)

    return demo

# ----------------- Launch -----------------
thread = threading.Thread(target=check_reminders)
thread.daemon = True
thread.start()

# Start health reminders thread
health_thread = threading.Thread(target=health_reminders)
health_thread.daemon = True
health_thread.start()

app = create_interface()
app.launch()
