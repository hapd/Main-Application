import datetime

def validate(self, name, nurse, dob, pin, mB, fB, contact):
    print(('%s, %s, %s, %s, %s') % (name, nurse, dob, pin,contact))
    if(mB.status == False and fB.status == False):
        self.gender = None
    if(len(str(pin)) != 4):  
        self.pinE = 1  
        self.status = 0
    if(str(pin) == 0 or str(name) == '' or str(dob) == '' or str(nurse) == '' or str(contact) == ''):
        self.status = 0
    try:  
        if(str(dob) != ''):
            datetime.datetime.strptime(dob,'%d/%m/%Y')  
        else:
            self.dobE = 2
    except ValueError:  
        self.dobE = 1
        self.status = 0
    if(self.gender == None):  
        self.genderE = 2  
        self.status = 0
    if(str(contact).isnumeric() == False):  
        self.contactE = 3
        self.status = 0  
    elif(len(str(contact))!=10 and str(contact) != ''):  
        self.contactE = 1  
        self.status = 0

    print('In validate:', self.status)
     
    