import os
import sys
import datetime
import smtplib
import random
import yaml
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
import geocoder


conf = yaml.load(open('./application.yml'))

engine = pyttsx3.init('sapi5')

client = wolframalpha.Client(conf['client_id'])

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[len(voices)-3].id)

def speak(audio):
    print('JARVIS: ' + audio)
    engine.say(audio)
    engine.runAndWait()

def weather(city,country):
    weather_city = "weather forecast in "+city
    speak("You are in "+city+", "+country)
    res = client.query(weather_city)
    output = next(res.results).text
    speak("Temperature in "+ city +" " +output)    

def greetMe():
    g = geocoder.ip('me')
    city = g.city
    country = g.country

    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        speak('Good Morning!')
        weather(city,country)

    if currentH >= 12 and currentH < 18:
        speak('Good Afternoon!')
        weather(city,country)

    if currentH >= 18 and currentH !=0:
        speak('Good Evening!')
        weather(city,country)

# greetMe()

# speak('Hello Sir, I am your digital assistant Jarvis!')
# speak('How may I help you?')


def myCommand():
   
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Listening...")
        r.pause_threshold =  1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print('User: ' + query + '\n')
        
    except sr.UnknownValueError:
        speak('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('Command: '))

    return query
        

if __name__ == '__main__':
    speak('Hello Sir, I am your digital assistant Jarvis!')
    greetMe()
    speak('How may I help you?')

    while True:
    
        query = myCommand();
        query = query.lower()
        
        if 'open youtube' in query:
            speak('okay')
            webbrowser.open('www.youtube.com')

        elif 'open google' in query:
            speak('okay')
            webbrowser.open('www.google.com')

        elif 'open gmail' in query:
            speak('okay')
            webbrowser.open('www.gmail.com')

        elif "what\'s up" in query or 'how are you' in query:
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
            speak(random.choice(stMsgs))

        elif 'how old are you' in query:
            stMsgs = ['I am a baby Jarvis','why sholud i tell you','I am a Program and I have no age']
            speak(random.choice(stMsgs))     

        elif 'email' in query or 'mail' in query:
            speak('Who is the Sender? ')
            sender = myCommand()

            if 'MI' in sender or 'mi' in sender or 'me' in sender:
                try:
                    speak('What is the Subject?')
                    subject = myCommand()
                    speak('What should I say? ')
                    content = myCommand()
                    speak('Ok Sir,Please Wait...')
                    message = 'Subject: {}\n\n{}'.format(subject, content)
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login(conf['email'],conf['password'])
                    server.sendmail(conf['email'], "jm.sajib012@gmail.com", message)
                    server.close()
                    speak('Email Has Been Sent!')

                except:
                    speak('Sorry Sir! I am unable to send your message at this moment!')
            else:
                speak('Something is Wrong,Sir')        


        elif 'nothing' in query or 'abort' in query or 'stop' in query or 'bye' in query or 'quit' in query:
            speak('okay Sir')
            speak('I am Leaving, have a good day,Sir')
            sys.exit()
           
        elif 'hello' in query:
            speak('Hello Sir')
            greetMe()
                                    
        elif 'play music' in query or 'music' in query:
            music_folder = 'C:/Users/jahid/Downloads/audio/'
            music = ['music1', 'music2', 'music3', 'music4', 'music5']
            random_music = music_folder + random.choice(music) + '.mp3'
            speak('Okay, here is your music! Enjoy!')
            os.system(random_music)
                    
        else:
            query = query
            speak('Searching...')
            try:
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    speak('Calculating, Sir - ')
                    speak('Got it.')
                    speak(results)
                    
                except:
                    results = wikipedia.summary(query, sentences=2)
                    speak('Got it.')
                    speak('WIKIPEDIA says - ')
                    speak(results)
        
            except:
                webbrowser.open('www.google.com')
        
        speak('Next Command! Sir!')