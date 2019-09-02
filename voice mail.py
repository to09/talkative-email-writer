import pprint ,csv
import pyttsx3 ,sys, os
import azure.cognitiveservices.speech as speechsdk
import pandas as pd
import smtplib

#To clear the window 
def cls():
    os.system("CLS")
    return

#Save the email to a email.txt file 
def email_data(text):
    w = open("email_data.txt", "a")
    w.write(text)
    return text

#Function for sending email
def email_sender(dict,email_id,subject,body,mode=1):
    email_address = os.environ.get('EMAIL_USER')
    email_password = os.environ.get('EMAIL_USER')

    #making a connection to smtp server
    con= smtplib.SMTP("smtp.gmail.com",587)

    #connect to server i.e it will send to internet traffic
    con.ehlo()
    con.starttls()
    con.login(email_address,email_password)
    msg_send=f'subject:{subject}\n\n{body}'
    con.sendmail(email_address,email_id,msg_send)
    con.quit()
    return voice_system(dict,mode=1)
    
def listen_data(mode=1):
# open source code   
# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
    speech_key, service_region = "****************", "westus"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    speak_data("Say ...",mode)


# Starts speech recognition, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed.  The task returns the recognition text as result. 
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query. 
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = speech_recognizer.recognize_once()

# Checks result.
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        speak_data("No speech could be recognized: \n",mode)
        return listen_data()
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        speak_data("Speech Recognition canceled:\n",mode)
        return voice_system(dict,mode=1)

#Speak the message given to it
def speak_data(message,mode=1):
    print(message)
    if mode == 1:
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 150)
        engine.say('{}'.format(message))
        engine.runAndWait()
    
    return message

def security_authentication(mode=1):
    try:
        cls()
        speak_data("\nEnter system authentication password and for exit enter 0: \n ",mode)
        passw= input().strip()
        if passw == "12345":
            return True
        elif passw== 0:
            return False
        else:
            return False
    except:
        speak_data("wrong input password type, Try again\n",mode)
        security_authentication(mode)
        
# write user data to output.csv file    
def write_data(dict):
    w = csv.writer(open("output.csv", "a"))
    for key, val in dict.items():
        w.writerow([key, val])
    return dict

# overwrite user data to output.csv file
def write_dataw(dict):
    w = csv.writer(open("output.csv", "w"))
    for key, val in dict.items():
        w.writerow([key, val])
    return dict

# read user data to output.csv file
def read_data(dict):
    with open('output.csv') as csvfile:
        readcsv = csv.reader(csvfile,delimiter=',')
        for row in readcsv:
            try:
                dict[row[0]]=row[1]
            except:
                continue
    return dict

#display the saved users data
def display_data(dict):
    print(pd.series(dict))
    return dict

#delete data from the system
def delete_data(dict,mode=1):
    try:
        cls()
        speak_data("Press : 1 for Format all data \nPress : 2 for Delete specific data \nPress : 3 for exit \n",mode)
        x = int(input())
        if x== 1:
            dict.clear()
            speak_data("succesfully format \n ",mode)
            return dict
                    
        elif x==2:
            speak_data("Enter user id: \n",mode)
            userid = input()
            dict.pop(userid)
            speak_data("successfully deleted\n",mode)
            write_dataw(dict)
            
            return admin(dict)
        elif x==3:
            return dict
        else :
            speak_data("wrong input\n",mode)
            delete_data(dict)
                    
    except:
        speak_data("wrong input type, try again\n",mode)
        delete_data(dict)

#for write mode users        
def write_mode(dict,mode=1):
    cls()
    msg="userid: " + l0 +" Password: "+ l1
    email_data(msg)
    speak_data("Enter sender email.id \n",mode)
    email_id= input()
    text="you have entered :"+ email_id + "\n"
    email_data(text)
    speak_data(text,mode)
    speak_data("enter subject of email\n",mode)
    subject = input()
    text1="you have entered :"+ subject+ "\n"
    email_data(text1)
    speak_data(text1,mode)
    speak_data("enter body of email\n",mode)
    body = input()
    text2="you have entered :"+ body+ "\n"
    email_data(text2)
    speak_data(text2,mode)
    email_data("\n\n\n\n\n")
    speak_data("done",mode)
    email_sender(dict,email_id,subject,body,mode)
    speak_data("emial send successfully",mode)
    email_writer(dict)

#for speak mode users
def speak_mode(dict,mode=1):
    cls()
    msg="userid: " + l0 +" Password: "+ l1
    email_data(msg)
    speak_data("Speak sender email.id \n",mode)
    email_id= listen_data(mode)
    text="you have spoken "+ email_id + "\n"
    email_data(text)
    speak_data(text,mode)
    speak_data("speak subject of email\n")
    subject = listen_data(mode)
    text1="you have spoken "+ subject+ "\n"
    email_data(text1)
    speak_data(text1,mode)
    speak_data("Speak body of email\n",mode)
    body = listen_data(mode)
    text2="you have entered "+ body+ "\n"
    email_data(text2)
    speak_data(text2,mode)
    email_data("\n\n\n\n\n")
    speak_data("done",mode)
    email_sender(dict,email_id,subject,body,mode)
    speak_data("emial send successfully\n",mode)
    email_writer(dict)

    
def email_writer(dict,mode=1):
    cls()

    if mode==1:
        speak_mode(dict,mode)
        return voice_system(dict,mode)

    elif mode==2:
        write_mode(dict,mode)
        return voice_system(dict,mode)

    else :
        email_writer(dict,mode)
    
#after succesfully signed in function 
def voice_system(dict,mode=1):
    cls()
    speak_data("Welcome to Talkative Email Writer\n",mode)
    speak_data("\nPress: 1 For start writing email \nPress: 2 For Exit\n ",mode)
    try:
        i = int(input())
        if i == 1:
            email_writer(dict,mode)
            voice_system(dict,mode)

        elif i == 2:
            return dict

        else:
            speak_data("Wrong input\n",mode)
        
    except:
        speak_data("Use numbers only voice\n",mode)
        voice_system(dict,mode)
    return(dict)

def admin(dict,mode=1):
    cls()
    password = security_authentication(mode)
    if password == True :
        speak_data("\nPress: 1 For show all user details \nPress: 2 For Delete User \nPress: 3 For Exit\n ",mode)
        try:
            m=int(input())
            if m==1:
                display_data(dict,mode)
                admin(dict,mode)

            elif m==2:
                delete_data(dict,mode)
                admin(dict,mode)

            elif m==3:
                return dict
    
        except:
            speak_data("use number key only\n",mode)
            admin(dict,mode)
    else :
            return dict

    
#login function    
def login(dict,mode=1):
    cls()
    #check dictionary is empty or not
    if len(dict) == 0:  
        speak_data("Your data is not available, first sign up \n",mode)
        signup(dict,mode)

    
    speak_data("Let me know your user id and password  \n",mode)

    speak_data("Enter Your Userid\n",mode)
    global l0
    l0 = input().strip()
    speak_data("Enter your Password\n",mode)
    global l1
    l1 = input().strip()

    #check userid and password to dictionary database
    if (l0 in list(dict.keys())) and (l1 in list(dict.values())):
        speak_data("successfully login\n",mode)
        voice_system(dict,mode)
    else :
        speak_data("Sorry, You have entered Wrong user id or password \n ",mode)

    return dict

# signup Function 
def signup(dict,mode=1):
    cls()
    
    speak_data("For signup Please enter your user id and password :- \n",mode)
    speak_data("Password Rule:1 -Password length must be greater than 8 and less then 18 characters ",mode)
    speak_data("         Rule:2 -Password must contain 1 lower , 1 upper and 1 number   \n",mode)

    #input list userid and password
    speak_data("Enter Your Userid\n",mode)
    text0=input().strip()
    speak_data("Enter Your Password\n",mode)
    text1=input().strip()

    #Check any dublicate password or userid in system database
    if (text1 in list(dict.values())) or (text0 in list(dict.keys())):
        speak_data("Your password or userid is unsafe , Please use another one! \n",mode)
        return signup(dict,mode)

    #check the length of password between 8 and 18 (Rule 1) 
    if len(text1) < 8 or len(text1) > 18 :
        speak_data(" sorry Password you have entered is wrong according to rules! \n",mode)
        speak_data(" Please signup again \n",mode)
        return signup(dict,mode)

    #check the strongness of password (Rule 2)
    count1=0
    count2=0
    count3=0
    for i in text1:
        
        #check lower case in password
        if i.islower():
            count1=count1+1

        #check upper case in password
        if i.isupper():
            count2 = count2+1

        #check number in password
        if i.isnumeric():
            count3 =count3+1

    #check availability of all 3 cases in password        
    if not(count1>0 and count2>0 and count3>0):
            speak_data(" sorry Password you have entered is wrong according to rules! \n",mode)
            speak_data(" Please signup again \n",mode)
            return signup(dict,mode)

    #assignment of userid and password to empty dictionary    
    dict[text0] = text1
    speak_data("Congratulations, You have successfully signup in security system \n",mode)

    write_data(dict)

    return dict
    
def ask(mode,dict):
    
    read_data(dict)
    cls()
    speak_data("\nWelcome to Talkative Email Writer\n",mode)
    try:
        speak_data(" Press : 1 for login \n Press : 2 for signup\n Press : 3 for Admin Login\n Press : 4 for Exit\n",mode)
        n=int(input())

    #switch case for login and signup
        if n==1:

        #Login for a existing user having userid and password
            login(dict,mode)
            return ask(dict,mode)
        
        elif n==2:
        
        #signup for a new user in the system and with a unique userid and password
            signup(dict,mode)
            return ask(mode,dict)
                
        elif n==3:
            admin(dict,mode)
            return ask(mode,dict)
            
        elif n==4:
            return
        #for exit the application
    
        else :
            speak_data("Sorry, you have given a wrong input \n")
    except:
        speak_data("Wrong input, use numbers key only\n",mode)


#Create a empty dictionary
dict={}
while True:
     speak_data("Would you like to choose which mode \nPress 1: For speak mode\nPress 2: For write mode\nPress 3: For exit\n ")
     try:
         n=int(input())
         if n==1:
             
             ask(1,dict)
             continue
        
         elif n==2:
             ask(2,dict)
             continue
        
         elif n==3:
        #for exit the application
             break
    
         else :
             speak_data("Sorry, you have given a wrong input \n")
     except:
         speak_data("Wrong input, use numbers key only\n")


    
        

