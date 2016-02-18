from flask import Flask, request, redirect
import twilio.twiml
from datetime import datetime
import urllib
from bs4 import BeautifulSoup
import os
from random import choice
import random

# get next meal from time
def getNextMeal():
    hour = datetime.now().hour
    minute = datetime.now().minute
    if hour <= 1:
       return "Dinner"
    if hour <= 10:
        return "Breakfast"
    elif hour <= 14:
        return "Lunch"
    elif hour <= 24:
        return "Dinner"

#get Quad Batims
def batim():
    # Get URL
    url = "https://docs.google.com/spreadsheets/d/1UmrKlZSTr--b0x664iOUpCY1PdClNfWWExC_5RmWFNg/pubhtml"

    # Fetch HTML
    f = urllib.urlopen(url)
    html = f.read()

    # Get BeautifulSoup Object
    soup = BeautifulSoup(html, "html.parser")

    # chooses random gossip to share between 1 and 4
    randomNumber = random.randint(1,4)
    # get gossip -> hardcoded to a spreadsheet cell
    if randomNumber == 1:
    	correctContent = soup.find(id="0R1").nextSibling.nextSibling.getText()
    elif randomNumber == 2:
    	correctContent = soup.find(id="0R2").nextSibling.nextSibling.getText()
    elif randomNumber == 3:
    	correctContent = soup.find(id="0R3").nextSibling.nextSibling.getText()
    else:
    	correctContent = soup.find(id="0R4").nextSibling.nextSibling.getText()

    return str(correctContent)

#get tonights party theme
def tonightTheme():
    # Get URL
    url = "https://docs.google.com/spreadsheets/d/1z7AqiLSM96Wqw7lLWNtJv6fylXHlwvtxcCugaGbyqHE/pubhtml"

    # Fetch HTML
    f = urllib.urlopen(url)
    html = f.read()

    # Get BeautifulSoup Object
    soup = BeautifulSoup(html, "html.parser")

    # get meal -> hardcoded to a spreadsheet cell
    correctContent = soup.find(id="0R26").nextSibling.nextSibling.getText()

    return str(correctContent)

#finds the needed hardcoded meal cell ID
def getMealID(day, meal):

    if day == "MONDAY":
    	if meal == "BREAKFAST":
    		return "0R1"
    	elif meal == "LUNCH":
    		return "0R2"
    	else:
    		return "0R3"
    elif day == "TUESDAY":
    	if meal == "BREAKFAST":
    		return "0R4"
    	elif meal == "LUNCH":
    		return "0R5"
    	else:
    		return "0R6"
    elif day == "WEDNESDAY":
    	if meal == "BREAKFAST":
    		return "0R7"
    	elif meal == "LUNCH":
    		return "0R8"
    	else:
    		return "0R9"
    elif day == "THURSDAY":
    	if meal == "BREAKFAST":
    		return "0R10"
    	elif meal == "LUNCH":
    		return "0R11"
    	else:
    		return "0R12"
    elif day == "FRIDAY":
    	if meal == "BREAKFAST":
    		return "0R13"
    	elif meal == "LUNCH":
    		return "0R14"
    	else:
    		return "0R15"
    elif day == "SATURDAY":
    	if meal == "BREAKFAST" or meal == "BRUNCH":
    		return "0R16"
    	elif meal == "LUNCH":
    		return "0R17"
    	else:
    		return "0R18"
    elif day == "SUNDAY":
    	if meal == "BREAKFAST" or meal == "BRUNCH":
    		return "0R19"
    	elif meal == "LUNCH":
    		return "0R20"
    	else:
    		return "0R21"
    else:
    	return "ERROR"

# parses query and gets desired meal
def getMeals(day, meal):
    # Get URL
    url = "https://docs.google.com/spreadsheets/d/1z7AqiLSM96Wqw7lLWNtJv6fylXHlwvtxcCugaGbyqHE/pubhtml"

    # Fetch HTML
    f = urllib.urlopen(url)
    html = f.read()

    # Get BeautifulSoup Object
    soup = BeautifulSoup(html, "html.parser")

    # choose which field to capture
    rightMeal = getMealID(day, meal);

    # get meal
    correctContent = soup.find(id=rightMeal).nextSibling.nextSibling.getText()

    return str(correctContent)

#takes a text and finds the meal, day, greeting or other from it
def parse_query(query):
    day = ""
    meal = ""
    query = query.lower()

    #day dictionary
    days   = {
       "sun": "SUNDAY",
       "sunday": "SUNDAY",
       "mon": "MONDAY",
       "monday": "MONDAY",
       "tue": "TUESDAY",
       "tues": "TUESDAY",
       "tuesday": "Tuesday",
       "wed": "WEDNESDAY",
       "wednesday": "WEDNESDAY",
       "thu": "THURSDAY",
       "thur": "THURSDAY",
       "thurs": "THURSDAY",
       "thursday": "THURSDAY",
       "fri": "FRIDAY",
       "friday": "FRIDAY",
       "sat": "SATURDAY",
       "saturday":"SATURDAY"
       }

    # meal dictionary
    meals    = {
       "lunch": "Lunch",
       "bfast": "Breakfast",
       "breakfast": "Breakfast",
       "brunch": "Brunch",
       "dinner": "Dinner",
       "din": "Dinner",
       "morning": "Breakfast",
       "afternoon": "Lunch",
       "tonight": "Dinner"
       }

    # greetings
    greetings    = {
        "hi": "hi",
        "what's up": "hi",
        "whats up": "hi",
        "hey": "hi",
        "yo": "hi",
        "sup": "hi",
        }

    # exception cases
    exception_cases = {
       "what is the time": "hour",
       "what time is it": "hour",
       "who made this app": "Danny copied it from his buddy Max Greenwald",
       "who is the prez": "Katie Panties",
       "who is the bees knees": "Artur the Innocent",
       "top club": "FC-FC-QQQ!",
       "club motto": "Moose heads are bae <3",
       "which club is the best": "FC-FC-QQQ!",
       "tonight's theme": tonightTheme(),
       "batim": batim(),
       "bateem": batim(),
       }

    #days case
    for key in days:
        if key in query:
            type = "food"
            day = days[key]

             # search for meal
            for key in meals:
                 if key in query:
                     meal = meals[key]

             # no specified meal - get next meal function
            if meal == "":
                 meal = getNextMeal()
            return [type, day, meal]

    # greeting case
    for key in greetings:
       if key in query:
          type = "greeting"
          return[type]

    # exception cases
    for key in exception_cases:
       if key in query:
          type = "exception"
          exception_value = exception_cases[key]
          # time case
          if exception_value == "hour":
             exception_value = str(datetime.now())
          return[type, exception_value]

    # no specified day
    if day == "":
        type = "exception"
        exception_name = "Specify a day and meal at Quad! Example: 'wednesday dinner'"
        return[type, exception_name]


#handle greeting case
def greeting(from_number):
	# List of known callers
	callers = {
	"+8135280235": "Danny",
	}

	if from_number in callers:
		name = callers[from_number]
		message = "Hi " + name + "! \n"
	else:
		message = "Hi there!!! Don't tell anyone but you're my favorite member"
	return message

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def quadMeals():

    # get from and body
    from_number = request.values.get('From', None)
    query = request.values.get('Body', None)
    if query is None:
    	query = ""

    #start of return message
    message = ""

    #parse query
    parsedArray = parse_query(query)
    if (parsedArray[0] == "exception"):
        response = parsedArray[1]
    elif (parsedArray[0] == "greeting"):
        response = greeting(from_number)
    elif (parsedArray[0] == "food"):
        # pass days to getMeals and get dictionary
        content = getMeals(parsedArray[1].upper(), parsedArray[2].upper())
        meal = parsedArray[1].upper() + " " + parsedArray[2].upper()
        response = meal + ": " + content + "... have a great day at Quad!"
    else:
       response = "error"

    #add our response message
    resp = twilio.twiml.Response()
    message+=response

    #handle long message case
    if len(message) > 160:
       resp.message("(1)\n" + message[:156])
       resp.message("(2)\n" + message[156:312])
       if len(message) > 312:
          resp.message("(3)\n" + message[312:468])

    else:
       resp.message(message)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
