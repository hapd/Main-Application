'''
MAJOR PROJECT 2019 - CSE D (203,221,246,249)
7 - Standard library imports
13 - Kivy imports
'''

# Standard library imports
import requests
import json
import random
import datetime

# Kivy imports
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty, ObjectProperty
from kivy.config import Config
from kivymd.theming import ThemeManager

#Local package imports
from functions.func import validate


#Global Variables

class Launch(Screen):
    def __init__(self, **kwargs):
        super(Launch, self).__init__(**kwargs)
        with open('data.json') as f:
            data = json.load(f)
        self.quote = str(data["quotes"][str(random.randint(1,5))])
   

class SignUp(Screen):
    def __init__(self, **kwargs):
        super(SignUp, self).__init__(**kwargs)
        self.nurseE = self.nameE = self.pinE = self.dobE = self.genderE = self.contactE = 0
        self.status = 1
        self.gender = None
    
    def sendFormData(self, name, nurse, dob, pin, mB, fB, contact):
        self.status = 1
        validate(self, name, nurse, dob, pin, mB, fB, contact)
        print('In sendFormData:', self.status)
            

class LogIn(Screen):
    pass

class Manager(ScreenManager):
    pass

class Main(App):
    theme_cls = ThemeManager()  # without this you'll get an error
    def build(self):
        return Builder.load_file('kv/main.kv')

if __name__ == '__main__':
    Main().run()

