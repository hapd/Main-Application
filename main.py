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
from kivy.core.window import Window
Window.size = (480, 800)
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivymd.theming import ThemeManager
from kivymd.bottomsheet import MDListBottomSheet

# Local package imports
from functions.func import validateSignUpForm, sendDataToAPI

# Global Variables
url = 'https://hapd-api.herokuapp.com'




# Class for Launch Screen
class Launch(Screen):
    def __init__(self, **kwargs):
        super(Launch, self).__init__(**kwargs)
        with open('data/data.json') as f:
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
            r = sendDataToAPI(data, url, '/addUser')
            self.pid = r['PID']
            
        
            
# Class for Log In Screen
class LogIn(Screen):
    def __init__(self, **kwargs):
        super(LogIn, self).__init__(**kwargs)
        self.pid = 0

    def fetchPid(self):
        return self.pid
    
    def authenticateUser(self, pid, pin):
        data = {'pId': pid, 'pin': pin}
        r = sendDataToAPI(data, url, '/checkLogin')
        if(r["fullfilmentText"] == "True"):
            self.pid = pid
            return (True, pid)
        else:
            return (False, None)

# Class for the Home Screen
class Home(Screen):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)

    def fetchPersonalInformation(self, pid):
        with open('data/p_information.json', 'r') as p:
            data = json.load(p)
        if(data.get(pid) == None):
            data = {'pId': pid}
            r = sendDataToAPI(data, url, '/whoAmI')
            information = r["data"]
            data[pid] = information
            with open('p_information.json','w') as p:
                json.dump(data, p)
            


class WhoAmI(Screen):
    def __init__(self, **kwargs):
        super(WhoAmI, self).__init__(**kwargs)
        self.information = {}
    def fetchPersonalInformation(self, pid):
        with open('data/p_information.json', 'r') as p:
            data = json.load(p)
        self.information = data.get(pid)

# Class for the Screen Manager
class Manager(ScreenManager):
    pass
    
  

# Class for the main application
class Main(App):
    theme_cls = ThemeManager()  # without this you'll get an error
    def build(self):
        return Builder.load_file('kv/main.kv')

    def setCurrentScreen(self, manager, s):
        manager.current = s

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

