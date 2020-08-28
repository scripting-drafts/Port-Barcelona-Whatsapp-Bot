Run it by typing "python3 portbcn-early-release.py" on terminal and scan the QR code with a phone. To start it send him the word "port".

Requirements:
 - Python 3
 - FastAPI
 - pydantic
 - uvicorn
 - selenium (+geckodriver)
 - requests
 - Firefox


Classes of Whatsapp Web change with time, so the code has to be updated with the proper new classes. Example: Line 113 points to the user name ('id'). (More info on /classes/ and in the last lines of portbcn-early-release.py)

By now the location retrieved is always the first one that was sent. If it isn't the first time you run the bot, clear its chat history first as a workaround.
