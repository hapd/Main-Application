import datetime, json, requests

def sendDataToAPI(self, data, url, method):
    data = json.dumps(data)
    headers = {'Authorization' : '', 'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    try:
        r = requests.post(url+method, data=data, headers=headers)
        print("Data from api:\n", r.text)
        return json.loads(r.text)    
    except:
        print("Couldn't send to webhook")









def validateSignUpForm(self, name, nurse, dob, pin, mB, fB, contact):
    # Checking if any of the gender is selected
    if(mB.status == False and fB.status == False):
        self.gender = None

    # Checking if the pin is not of 4 digits    
    if(len(str(pin)) != 4 and str(pin) != ''):  
        self.pinE = 1  
        self.status = 0
    elif(str(pin) != ''):
        self.pinE = 200

    # Universal error for empty field    
    if(str(pin) == 0 or str(name) == '' or str(dob) == '' or str(nurse) == '' or str(contact) == ''):
        self.status = 0

    # Checking for the correct date format of date of birth    
    try:  
        if(str(dob) != ''):
            datetime.datetime.strptime(dob,'%d/%m/%Y')  
            self.dobE = 200
        else:
            self.dobE = 2
    except ValueError:  
        self.dobE = 1
        self.status = 0

    # Error for not choosing any gender    
    if(self.gender == None):  
        self.genderE = 2  
        self.status = 0

    # Error when contact number does not contain numeric values    
    if(str(contact).isnumeric() == False and str(contact) != ''):  
        self.contactE = 2
        self.status = 0  
    # Error when contact number is incomplete
    elif(len(str(contact))!=10 and str(contact) != ''):  
        self.contactE = 1  
        self.status = 0
    elif(str(contact) != '' and len(str(contact)) == 10):
        self.contactE = 200    

    # Success code for name
    if(str(name) != '' and str(name).isnumeric() == False):
        self.nameE = 200

    # Success code for nurse
    if(str(nurse) != '' and str(nurse).isnumeric() == False):
        self.nurseE = 200

     
    