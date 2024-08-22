#importing necessary libraries
import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclib
import os
import requests
from gtts import gTTS
import pygame
import torch
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import wikipediaapi
import signal
import psutil

# Initializing a dictionary header for Wikipedia. You can add your GitHub repo and email ID.
headers = {
    'User-Agent': "JARVISBot/1.0 (<your repository link>; <someone@example.com>)"
}

# Initializing Wikipedia API with English language settings and custom headers.
wiki_wiki = wikipediaapi.Wikipedia('en', headers=headers)

# Initialize recognizer (for speech recognition), TTS engine, and AI model.
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# API key for news service (please don't use this API key).
news_api = "<your API key here>"

# Initializing GPT-Neo model and tokenizer for AI response generation.
model_name = "EleutherAI/gpt-neo-125M"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPTNeoForCausalLM.from_pretrained(model_name, ignore_mismatched_sizes=True)

#to close a certian process like youtube or linkedin
def close_process_by_name(process_name):
    for proc in psutil.process_iter():
        # Check if the process name matches
        if process_name.lower() in proc.name().lower():
            proc.send_signal(signal.SIGTERM)  # Send termination signal

# Function to fetch the summary of a topic from Wikipedia.
def fetch_wikipedia_summary(query):
    # Fetch the Wikipedia page for the given query.
    page = wiki_wiki.page(query)
    
    # Check if the page exists and return the summary.
    if page.exists():
        summary = page.summary[:500]  # Limit the summary to the first 500 characters.
        return summary
    else:
        return "Sorry, I couldn't find any information on that topic."

# Check if the tokenizer has a pad token; if not, set the EOS token as the pad token.
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Function to generate a response using GPT-Neo model.
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)
    attention_mask = inputs.attention_mask
    outputs = model.generate(inputs.input_ids, attention_mask=attention_mask, max_length=150, do_sample=True, temperature=0.7, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Function to speak using pyttsx3 (alternative speech method).
def speak_old(text):
    engine.say(text)
    engine.runAndWait()

# Function to speak using gTTS (Google Text-to-Speech) and Pygame.
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove('temp.mp3')

# Function to process commands and execute appropriate actions.
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "close google" in c.lower():
        try:
            close_process_by_name("chrome")  # Replace 'chrome' with your default browser's process name if different.
            speak("Google is now closed.")
        except Exception as e:
            speak("An error occurred while trying to close Google.")
            print(f"Error: {e}")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "close facebook" in c.lower():
        try:
            close_process_by_name("chrome")  # Replace 'chrome' with your default browser's process name if different.
            speak("Facebook is now closed.")
        except Exception as e:
            speak("An error occurred while trying to close Facebook.")
            print(f"Error: {e}")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "close youtube" in c.lower():
        try:
            close_process_by_name("chrome")  # Replace 'chrome' with your default browser's process name if different.
            speak("YouTube is now closed.")
        except Exception as e:
            speak("An error occurred while trying to close YouTube.")
            print(f"Error: {e}")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "close linkedin" in c.lower():
        try:
            close_process_by_name("chrome")  # Replace 'chrome' with your default browser's process name if different.
            speak("LinkedIn is now closed.")
        except Exception as e:
            speak("An error occurred while trying to close LinkedIn.")
            print(f"Error: {e}")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/")
    elif "close instagram" in c.lower():
        try:
            close_process_by_name("chrome")  # Replace 'chrome' with your default browser's process name if different.
            speak("Instagram is now closed.")
        except Exception as e:
            speak("An error occurred while trying to close Instagram.")
            print(f"Error: {e}")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com/")
    elif "close github" in c.lower():
        try:
            close_process_by_name("chrome")  # Replace 'chrome' with your default browser's process name if different.
            speak("Github is now closed.")
        except Exception as e:
            speak("An error occurred while trying to close Github.")
            print(f"Error: {e}")
    elif c.lower().startswith("play"):
        try:
            song = c.lower().split(" ", 1)[1]
            link = musiclib.music[song]
            webbrowser.open(link)
        except KeyError:
            speak("Sorry, I couldn't find the song.")
        except Exception as e:
            speak("An error occurred while trying to play the song.")
            print(f"Error: {e}")
    elif "tell me some news" in c.lower():
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [])
                if articles:
                    speak("Here are the top headlines:")
                    for i, article in enumerate(articles[:5], 1):  # Limit to the top 5 headlines.
                        headline = article["title"]
                        speak(f"Headline {i}: {headline}")
                        print(f"Headline {i}: {headline}")
                else:
                    speak("Sorry, I couldn't find any news articles.")
            else:
                speak(f"Failed to fetch news. Status code: {r.status_code}")
        except Exception as e:
            speak("An error occurred while fetching the news.")
            print(f"Error: {e}")
    elif "what is" in c.lower():
        topic = c.lower().replace("what is", "").strip()
        response = fetch_wikipedia_summary(topic)
        speak(response)
        print(response)
    elif "who is" in c.lower():
        topic = c.lower().replace("who is", "").strip()
        response = fetch_wikipedia_summary(topic)
        speak(response)
        print(response)
    elif "goodbye jarvis" in c.lower():
        speak("Goodbye. Have a great day!")
        return True  # Return True to indicate that the program should exit.
    else:
        # If no specific command is recognized, pass it to the AI for a response.
        response = generate_response(c)
        speak(response)

# Main loop to initialize Jarvis and continuously listen for commands.
if __name__ == "__main__":
    speak("Initializing jarvis...")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise.
                print("Listening for the wake word 'jarvis'...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                word = recognizer.recognize_google(audio)
                print(f"Recognized: {word}")

                if word.lower() == "jarvis":
                    speak("Yes Sir, How may I help you?")
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for ambient noise.
                        print("jarvis Active...")
                        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                        
                        command = recognizer.recognize_google(audio)
                        print(f"Command: {command}")
                        if processCommand(command):
                            break  # Exit the loop if the command indicates to exit.
        except sr.UnknownValueError:
            print("Sorry, I did not catch that. Could you please repeat?")
            speak("Sorry, I did not catch that. Could you please repeat?")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak("There was an error with the speech recognition service.")
        except Exception as e:
            print(f"Error: {e}")
            speak("An error occurred. Please try again.")
