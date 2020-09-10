# Port-Bot

Run it from its folder by typing "python3.7 start.py" and scan the QR code with a phone. Message him from another phone to initialize it. It can only handle a message every 7 seconds aprox.

Requirements:
 - Python 3.7
 - Firefox
 - Geckodriver
 
Libraries:
 - FastAPI
 - pydantic
 - uvicorn
 - sqlalchemy
 - selenium
 - requests


Classes of Whatsapp Web change with time, so the code has to be updated with the proper new classes. More info on /classes/ and in the last lines of port-bot.py)
