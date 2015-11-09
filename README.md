# cottageMeals
Python script for a Twilio connected number to find out what is for lunch at Cottage Club

This allows a person to text a number and recieve a response as specified by my Python script.

Steps:
1. Acquire a Twilio number
2. Direct Twilio number to a Heroku web server
3. Create a python script that takes a twilio message, parses it and responds (I tested using Flask)
4. Upload python file to Heroku web server
5. Boom!

More specifically my Python script inteprets a message (searches for key words) and goes to a Google Spreadsheet 
to find an appropriate response. In this way I can update the spreadsheet any time I want and the responses will be pushed
to the users. For example if a user types "get me Tues Lunch", my script interprets this as "TUESDAY LUNCH", it then references
the spreadsheet and finds the cell with TUESDAY LUNCH. Maybe it is Lasagna!

I used BeautifulSoup to parse the Google Spreadsheet which I could access after I published it. (Takes 5 mins to republish
changes)
