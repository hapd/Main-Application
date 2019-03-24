import datetime, json, requests, re, random

# Universal function for sending any data (in dict format) to the API
def sendDataToAPI(data, url, method):
    data = json.dumps(data)
    headers = {'Authorization' : '', 'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    try:
        r = requests.post(url+method, data=data, headers=headers)
        print("Data from api:\n", r.text)
        return json.loads(r.text)    
    except:
        print("Couldn't send to webhook")


# Function to validate the Sign Up Form
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

# This function matches the rules to the message
def match_rule(rules,message):
    possible_fallback_responses = [
        'I didn\'t get that. Can you say it again?', 
        'I missed what you said. What was that?', 
        'Sorry, could you say that again?',
        'Sorry, can you say that again?',
        'Can you say that again?',
        'Sorry, I didn\'t get that. Can you rephrase?',
        'Sorry, what was that?',
        'Say that one more time?',
        'I didn\'t get that. Can you repeat?',
        'I missed that, say that again?'
    ]
    response, phrase=random.choice(possible_fallback_responses), None
    #iterating over dictionary rules
    for pattern,responses in rules.items():
        match=re.search(pattern,message)
        if match is not None:
            response=random.choice(responses)
            if '{0}' in response:
                phrase=match.group(1)
    
    return response.format(phrase)

def replace_pronouns(message):
    message=message.lower()
    if 'me' in message:
        new_message=re.sub('me','you',message)
    if 'my' in message:
        new_message=re.sub('my','your',message)
    if 'your' in message:
        new_message=re.sub('your','my',message)
    if 'you' in message:
        new_message=re.sub('you','me',message)
        
    return new_message

def respond(message):
    rules={
        'hey(.*)': ['Hello there! How are you today?', 'Hey there!'],
        'how are you?(.*)': ['Wonderful as always, thanks for asking.'],
        'i want (.*)': ['Should I call the nurse to get {0}?'],
        'do you remember (.*)': [
            'Did you think I would forget {0}', 
            "Why haven't you been able to forget {0}", 
            'What about {0}',
            'Yes .. and?'
        ],
        'do you think (.*)': ['if {0}? Absolutely.', 'No chance'],
        'if (.*)': [
            "Do you really think it's likely that {0}",
            'Do you wish that {0}','What do you think about {0}',
            'Really--if {0}'
        ]
    }
    message = message.lower()
    response=match_rule(rules,message)
    phrase=match_rule(rules,message)
    if '{0}' in response:
        #Replace pronouns in the phrase
        phrase=replace_pronouns(phrase)
        response=response.format(phrase)
    return response