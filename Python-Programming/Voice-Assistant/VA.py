import speech_recognition as sr
import sounddevice as sd
import sys  # Import the sys module
import soundfile as sf
from gtts import gTTS
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

def process_command(command):
    if "weather" in command:
        city = extract_city(command)
        if city:
            return get_weather(city)
        else:
            return "Sorry, I didn't recognize the city in your command."
    elif "time" in command:
        return get_current_time()
    elif any(keyword in command for keyword in ["joke", "laugh"]):
        return get_joke()
    elif any(keyword in command for keyword in ["hello", "greet"]):
        return greet_user()
    elif "calculate" in command:
        return perform_calculation(command)
    elif any(keyword in command for keyword in ["capital", "interesting fact"]):
        return provide_knowledge(command)
    elif any(keyword in command for keyword in ["music", "play a song"]):
        return recommend_music()
    elif any(keyword in command for keyword in ["hidden talents", "fun fact"]):
        return share_fun_fact()
    else:
        return "Sorry, I didn't understand the command."

# Define additional functions for the new commands here

def get_joke():
    # Fetch a random joke from an API or use predefined jokes
    # For example, using the JokeAPI: https://v2.jokeapi.dev/
    joke_api_url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(joke_api_url)
    if response.status_code == 200:
        joke_data = response.json()
        if "setup" in joke_data and "delivery" in joke_data:
            return f"{joke_data['setup']} {joke_data['delivery']}"
        elif "joke" in joke_data:
            return joke_data['joke']
    return "Why don't scientists trust atoms? Because they make up everything!" or "I'm sorry, I couldn't fetch a joke at the moment."

def perform_calculation(command):
    # Parse the command to extract the mathematical expression
    expression = command.split("calculate")[-1].strip()
    try:
        result = eval(expression)
        return f"The result of {expression} is {result}."
    except Exception:
        return "Sorry, I couldn't calculate that. Please provide a valid mathematical expression."

def provide_knowledge(command):
    # Extract keywords like "capital" or "interesting fact" and provide relevant information
    if "capital" in command:
        # You can use an API or predefined data to get the capital of a country
        return "The capital of France is Paris."
    elif "interesting fact" in command:
        # You can provide a predefined interesting fact or fetch from a source
        return "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!"

def greet_user():
    current_time = datetime.now().hour
    if 5 <= current_time < 12:
        return "Good morning! How can I assist you today?"
    elif 12 <= current_time < 18:
        return "Good afternoon! What can I do for you?"
    else:
        return "Good evening! How may I help you?"

def share_fun_fact():
    # Fetch a fun fact from an API or provide a predefined list
    # For example, using the Chuck Norris Jokes API: https://api.chucknorris.io/
    chuck_norris_api_url = "https://api.chucknorris.io/jokes/random"
    
    response = requests.get(chuck_norris_api_url)
    if response.status_code == 200:
        fact_data = response.json()
        if 'value' in fact_data:
            return f"Here's a fun fact: {fact_data['value']}"
    
    return "Sorry, I couldn't fetch a fun fact at the moment."

def recommend_music():
    # Fetch a random song recommendation from an API or predefined list
    # For example, using the Last.fm API for music recommendations
    lastfm_api_key = 'aacdab68a479864b36dbc2ae70477045'
    lastfm_api_url = f'http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={lastfm_api_key}&format=json&limit=1'
    
    response = requests.get(lastfm_api_url)
    if response.status_code == 200:
        music_data = response.json()
        if 'tracks' in music_data and 'track' in music_data['tracks'] and music_data['tracks']['track']:
            track_name = music_data['tracks']['track'][0]['name']
            artist_name = music_data['tracks']['track'][0]['artist']['name']
            return f"I recommend listening to '{track_name}' by {artist_name}."
    
    return "Sorry, I couldn't fetch a music recommendation at the moment."

OPENWEATHERMAP_API_KEY = '8f3da761db8d85e97111d7324ce618d5'

def get_weather(city):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'appid': OPENWEATHERMAP_API_KEY, 'units': 'metric'}  # Use 'imperial' for Fahrenheit
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return f"The weather in {city} is {description} with a temperature of {temperature} degrees Celsius."
    else:
        return f"Sorry, couldn't fetch weather information for {city}."

def extract_city(command):
    # Use regular expression to find the city in the command
    matches = re.search(r'\b(?:weather in|weather for)\s*(\w+)\b', command.lower())
    if matches:
        return matches.group(1).capitalize()
    else:
        return None

def get_current_time():
    current_time = datetime.now().strftime("%H:%M")
    return f"The current time is {current_time}."

def speak(text, pitch=70, speed=1.5):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save('output.mp3')
    
    # Convert mp3 to wav using soundfile
    data, samplerate = sf.read('output.mp3', dtype='float32')
    sf.write('output.wav', data, samplerate)
    
    # Play the wav file
    sd.play(data, samplerate=samplerate, blocking=True)

def listen():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"User said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand your command.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)

def main():
    speak("Hello! How can I assist you today?")

    while True:
        command = listen()

        if command:
            if "hello" in command.lower():
                speak("Hello! How can I assist you today?")
            elif "bye" or "cya" or "adios" or "goodbye" or "talk to you later." in command.lower():
                speak("Goodbye! Have a nice day.")
                break
            elif "hello" or "bye" not in command.lower():
                response = process_command(command)
                speak(response)
            else:
                speak("I'm sorry, I don't understand that command.")
        
if __name__ == "__main__":
    source = sd.InputStream(device=None, channels=1, callback=callback)
    source.start()
    main()
