'''
MAJOR PROJECT 2019 - CSE D (203,221,246,249)
'''

# Standard library imports
import requests
import json
import random
import datetime, time

# Kivy imports
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivymd.color_definitions import colors
from kivy.utils import get_color_from_hex
Window.size = (480, 800)
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivymd.theming import ThemeManager
from kivymd.button import MDRaisedButton
from kivymd.bottomsheet import MDListBottomSheet
from kivymd.list import MDList, TwoLineIconListItem, IRightBodyTouch
from kivymd.selectioncontrols import MDCheckbox


# Local package imports
from functions.func import validateSignUpForm, sendDataToAPI, respond
from functions.emotion import getEmotion

# Global Variables
url = 'https://hapd-api.herokuapp.com'
name = ''
age = ''
dob = ''

class IconRightSampleWidget(IRightBodyTouch, MDCheckbox):
    pass


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
        print(pid)
        with open('data/p_information.json', 'r') as p:
            f = json.load(p)
        if(pid != f["current"]["pid"]):
            d = {'pId': pid}
            r = sendDataToAPI(d, url, '/whoAmI')
            info = r["data"]
            info["pid"] = pid
            data = {}
            data["current"] = info
            with open('data/p_information.json','w') as p:
                json.dump(data, p, indent=4)
     
# Class for Who Am I Screen.
class WhoAmI(Screen):
    def __init__(self, **kwargs):
        super(WhoAmI, self).__init__(**kwargs)
    
    def setFields(self, na, age, dob):
        with open("data/p_information.json") as f:
            data = json.load(f)
        print(data["current"]["name"])
        na.text = "Name: " + str(data["current"]["name"]).capitalize()
        age.text = "Age: " + str(data["current"]["age"])
        dob.text = "Date of Birth: " + str(data["current"]["dob"])      
        
# Class for the Chat Screen        
class Chat(Screen):
    def __init__(self, **kwargs):
        super(Chat, self).__init__(**kwargs)
        self.i = "a0"
        self.ptr = 0
        self.w = False
    def addToChatSpaceUser(self, ChatSpace, message):
        print("Sentiment for %s is:"%message, getEmotion(message))
        btn = MDRaisedButton(id = str(self.i), size_hint_y = 0.1, text = str(message), elevation_normal= 9, pos_hint = {"right": 1})
        ChatSpace.add_widget(btn)
        return btn
    def addToChatSpaceSystem(self, ChatSpace, message):
        if(message == "@WELCOME_INTENT"):
            if(self.w == False):
                btn = MDRaisedButton(size_hint_y = 0.1, text = "Hello, I am your assistant.", elevation_normal= 9)
                btn2 = MDRaisedButton(size_hint_y = 0.1, text = "How may I help you?", elevation_normal= 9)
                ChatSpace.add_widget(btn)
                ChatSpace.add_widget(btn2)
                self.w = True
                return btn2
        else:
            res = respond(message)
            btn = MDRaisedButton(size_hint_y = 0.1, text = res, elevation_normal= 9)
            ChatSpace.add_widget(btn)
            return btn
    

# Class for the Schedule Screen
class Schedule(Screen):
    def __init__(self, **kwargs):
        super(Schedule, self).__init__(**kwargs)
        self.field_set = 0
    def setFields(self, ScheduleList, pid):
        if(self.field_set == 0):
            data = {
                "pId": str(pid),
                "req_type": "read_schedule",
            }
            r = sendDataToAPI(data, url, '/schedule')
            status = r["schedule"]["found"]
            if(status == "True"):
                tasks = r["schedule"]["tasks"]
                print(tasks)
                keys = list(tasks.keys())
                for key in keys:
                    temp = tasks[key].split("-")
                    s = ""
                    for i in temp:
                        s += (i+" ") 
                    item = TwoLineIconListItem(text = s, secondary_text = key, theme_text_color =  'Primary', secondary_text_color = 'Errror')
                    ScheduleList.add_widget(item)
                    self.field_set = 1



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
