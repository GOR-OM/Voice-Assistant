import win32com.client
import speech_recognition as sr
# import wikipedia
import datetime
import webbrowser
import os
import subprocess
import  openai
from dotenv import load_dotenv
from openai import OpenAI

from config import  apikey

speaker = win32com.client.Dispatch("SAPI.SpVoice")
load_dotenv(".env")

def speak(text):
    try:
        speaker.Speak(text)
    except Exception as e:
        print(f"Error in speak function: {e}")



def AI(prompt):
  openai.api_key = apikey
  
  client = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": prompt}]
  )

  response = client.choices[0].message.content
  
  return response





responses_dir = 'responses'
if not os.path.exists(responses_dir):
    os.makedirs(responses_dir)

def save_response(response):
    now = datetime.now()
    filename = now.strftime('%Y-%m-%d_%H-%M-%S') + '.txt'
    filepath = os.path.join(responses_dir, filename)
    with open(filepath, 'w') as f:
        f.write(response)



def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold =  0.9
        r.energy_threshold = 100
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Jarvis"

def greating():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12 :
        speak("Good Morning Sir !")
    elif hour >= 12 and hour < 18 :
        speak("Good Afternoon Sir !")
    else :
        speak("Good Evening Sir !")

def open_application(app_name, app_command):
    speak(f"Opening {app_name} Sir .....")
    subprocess.Popen(app_command, shell=True)

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Harry: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    speak(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

applications = [
            ["vs code", "code"],
            ["terminal", "start cmd"],
            ["notepad", "notepad.exe"],
            ["calculator", "calc.exe"],
            ["file", "explorer.exe"],
            ["folder", "explorer.exe"],  # Assuming "folder" should also open File Explorer
            # Add more applications as needed
        ]

sites = [
            ["Wikipedia", "https://en.wikipedia.org/wiki"],
            ["Instagram", "https://instagram.com"],
            ["Facebook", "https://facebook.com"],
            ["LinkedIn", "https://www.linkedin.com/in"],
            ["Google", "https://www.google.com"],
            ["YouTube", "https://www.youtube.com"],
            ["Twitter", "https://twitter.com"],
            ["GitHub", "https://github.com"],
            ["Stack Overflow", "https://stackoverflow.com"],
            ["Amazon", "https://www.amazon.com"],
            ["Netflix", "https://www.netflix.com"],
            ["Reddit", "https://www.reddit.com"],
            ["CNN", "https://edition.cnn.com"],
            ["BBC News", "https://www.bbc.com/news"],
            ["The New York Times", "https://www.nytimes.com"],
            ["TechCrunch", "https://techcrunch.com"],
            ["Medium", "https://medium.com"],
            ["Quora", "https://www.quora.com"],
            ["LinkedIn Learning", "https://www.linkedin.com/learning"],
            ["Khan Academy", "https://www.khanacademy.org"]
        ]

if __name__ == '__main__':
    print("Welcome to Jarvis")
    greating()
    # speak("I am Jarvis assistant, How can I help you ?")
    while True :
        print("Listening....")
        query = takeCommand()
        # speak(query)
        
        for site in sites :
            if f"Open {site[0]}".lower() in query.lower():
                speak(f"Opening {site[0]} Sir .....")
                webbrowser.open(site[1])

        for app in applications:
            if f"Open {app[0]}".lower() in query.lower():
                speak(f"Opening {app[0]} Sir .....")
                subprocess.Popen(app[1], shell=True)


        if "the time" in query.lower():
            hour = datetime.datetime.now().hour
            minute = datetime.datetime.now().minute
            speak(f"{hour} hour  {minute} minute  ")
        elif "open vs code" in query.lower():
            os.system("code")
            speak("opening  vscode sir...")

        elif "search" in query:
            search_query = query.replace("search", "").strip()
            if search_query:
                search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                speak(f"Searching Google for {query} Sir .....")
                webbrowser.open(search_url)
            else:
                speak("Please provide a search query.")

        elif "using chat gpt".lower() in query.lower():
            save_response(AI(prompt=query.lower()))
            
        elif "Jarvis Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
