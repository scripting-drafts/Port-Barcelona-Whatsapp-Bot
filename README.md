Run it from its folder by typing "python3.7 start.py" on terminal and scan the QR code with a phone. To start it text him the word "port".

Requirements:
 - Python 3
 - FastAPI
 - pydantic
 - uvicorn
 - sqlalchemy
 - selenium (+geckodriver)
 - requests
 - Firefox


Classes of Whatsapp Web change with time, so the code has to be updated with the proper new classes. Example: Line 125 points to the user name ('id'). (More info on /classes/ and in the last lines of portbcn-early-release.py)

By now the location retrieved is always the first one that was sent. If it isn't the first time you run the bot, clear its chat history first as a workaround.
