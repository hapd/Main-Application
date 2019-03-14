'''
MAJOR PROJECT 2019 - CSE D (203,221,246,249)
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
from kivymd.bottomsheet import MDListBottomSheet


# Local package imports
from functions.func import validateSignUpForm, sendDataToAPI

# Global Variables
url = 'https://jolly-rabbit-50.localtunnel.me'

# Class for Launch Screen
class Launch(Screen):
    def __init__(self, **kwargs):
        super(Launch, self).__init__(**kwargs)
        with open('data.json') as f:
            data = json.load(f)
        self.quote = str(data["quotes"][str(random.randint(1,5))])
   

# Class for Sign Up Screen
class SignUp(Screen):
    def __init__(self, **kwargs):
        super(SignUp, self).__init__(**kwargs)
        self.nurseE = self.nameE = self.pinE = self.dobE = self.genderE = self.contactE = 0
        self.status = 1
        self.gender = None
        self.pid = 'Nil'
    
    def sendFormData(self, name, nurse, dob, pin, mB, fB, contact):
        self.status = 1
        validateSignUpForm(self, name, nurse, dob, pin, mB, fB, contact)
        data = {
            "name": name, 
            "nurse": nurse,
            "gender": self.gender, 
            "dob": dob, 
            "pin": pin,
            "contact": contact 
        }
        if(self.status == 1):
            r = sendDataToAPI(self, data, url, '/addUser')
            self.pid = r['PID']
            
        
            
# Class for Log In Screen
class LogIn(Screen):
    pass

# Class for the Screen Manager
class Manager(ScreenManager):
    pass

def callback():
    Manager().current = 'Log In Screen'

# Class for the main application
class Main(App):
    theme_cls = ThemeManager()  # without this you'll get an error
    def build(self):
        return Builder.load_file('kv/main.kv')

    
    def show_example_bottom_sheet(self, pid):
        bs = MDListBottomSheet()
        bs.add_item("Your Patient ID is %s."%(pid), lambda x: x)
        bs.add_item("Please note this down for future references.", lambda x: x,
                    icon='information')
        bs.add_item("Click on the back button to go to Log In Screen.", lambda x: x,
                    icon='login')
        bs.open()


if __name__ == '__main__':
    Main().run()

