import os
import sys
import PyPDF2
import cv2
import pyttsx3
# import pywhatkit as kit
import speech_recognition as sr
import datetime
import time
from requests import get
import wikipedia
import webbrowser
import smtplib
import sys
import pyjokes
import requests
import operator
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from googleUi import Ui_googleUi


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M:%p")

    if hour >= 0 and hour <= 12:
        speak(f"good morning mam,its {tt}")
        speak("i m your assistant mam, how may i help you")
    elif hour >= 12 and hour <= 18:
        speak(f"good afternoon mam,its {tt}")
        speak("i m your assistant mam, how may i help you")
    else:
        speak(f"good evening mam,its {tt}")
        speak("i m your assistant mam, how may i help you")


def sendEmail(to, content):
    server = smtplib.SMTP('smpt.gmail.com', 587)
    server.ehlo()
    server.login('preetisingh9351@gmail.com', 'password')
    server.sendmail(to, content)
    speak("email has been sent to ram")


def pdf_reader():
    book = open('py3.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f"total number of pages in this book{pages}")
    speak("mam please enter the page number i have read")
    pg = int(input("please enter the page number:"))
    page = pdfReader.getPage(pg)
    text = page.extracttext()
    speak(text)


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("observing......")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=5, phrase_time_limit=5)

            try:
                print("Recognizing....")
                query = r.recognize_google(audio, language='en-in')
                print(f"user said:{query}")

            except Exception as e:
                speak("please say again ...")
                return "none"
            return query

    def TaskExecution(self):
        wish()
        if 1:
            self.query = self.takecommand()

        if "open notepad" in self.query:
            npath = "C:\\WINDOWS\\system32\\notepad.exe"
            os.startfile(npath)

        elif "close notepad" in self.query:
            speak("okay mam, closing notepad")
            os.system("taskkill /f /im notepad.exe")


        elif "open chrome" in self.query:
            gpath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(gpath)

        elif "read PDF" in self.query:
            pdf_reader()

        elif "open adobe reader" in self.query:
            apath = "C:\\Program Files (x86)\\Adobe\\Acrobat Reader DC\\Reader\\adobe reader.exe"
            os.startfile(apath)

        elif "open command prompt" in self.query:
            os.startfile("start cmd")

        elif "open camera" in self.query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k == 27:
                    break;
            cap.release()
            cv2.destroyAllWindows()


        elif "set alarm" in self.query:
            nn = int(datetime.datetime.now().hour)
            if nn == 22:
                music_dir = 'F://songs'
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[0]))

        elif "ip address" in self.query:
            ip = get('https://api.ipify.org').text
            speak(f"your ip address is {ip}")

        elif "wikipedia" in self.query:
            speak("searching wikipedia....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=5)
            speak("mam according to wikipedia")
            speak(results)
            print(results)

        elif "open youtube" in self.query:
            webbrowser.open("www.youtube.com")

        elif "open facebook" in self.query:
            webbrowser.open("www.facebook.com")

        elif "open instagram" in self.query:
            webbrowser.open("www.instagram.com")

        elif "open telegram" in self.query:
            webbrowser.open("www.telegram.com")

        elif "open google" in self.query:
            speak("mam ,what should i search on google")
            cm = takecommand().lower()
            webbrowser.open(f"{cm}")

        elif "send message" in self.query:
            kit.sendwhatmsg("+919351847535", "hello dad", 20, 12)

        elif "play song on youtube" in self.query:
            speak("tell me song which u want to play")
            sm = takecommand().lower()
            kit.playonyt(sm)

        elif "tell me a joke" in self.query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "email to ram" in self.query:
            try:
                speak("what should i say")
                content = takecommand().lower()
                to = "preetisingh9351@gmail.com"
                sendEmail(to, content)
                speak("email has been sent to u mam")


            except Exception as e:
                print(e)
                speak("sorry mam,i m not able to open")


        elif "can you calculate" in self.query:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                speak("Say what you want to calculate, example: 3 plus 3")
                print("listening.....")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            my_string = r.recognize_google(audio)
            print(my_string)

            def get_operator_fn(op):
                return {
                    '+': operator.add,
                    '-': operator.sub,
                    'x': operator.mul,
                    'divided': operator.__truediv__,
                    'Mod': operator.mod,
                    'mod': operator.mod,
                    '^': operator.xor,
                }[op]

            def eval_binary_expr(op1, oper, op2):
                op1, op2 = int(op1), int(op2)
                return get_operator_fn(oper)(op1, op2)

            print(eval_binary_expr(*(my_string.split())))

        elif "no thanks" in self.query:
            speak("ok mam ,thnx for using me ,have a good day")
            sys.exit()

        elif "where i am" in self.query or "where we are" in self.query:
            speak("wait mam, let me check")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                # print(geo_data)
                city = geo_data['city']
                # state = geo_data['state']
                country = geo_data['country']
                speak(f"mam i am not sure, but i think we are in {city} city of {country} country")
            except Exception as e:
                speak("sorry mam, Due to network issue i am not able to find where we are.")
                pass
startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_googleUi()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("C:/Users/Manoj/Desktop/QT/images.jpg")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Users/Manoj/Desktop/QT/zira 1.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("C:/Users/Manoj/Desktop/QT/ENjk.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        startExecution.start()

app = QApplication(sys.argv)
google = Main()
google.show()
exit(app.exec_())
