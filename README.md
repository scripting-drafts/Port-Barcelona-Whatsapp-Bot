First run the database from its directory by typing "uvicorn main:app --reload".

Then run the bot by typing "python3 portbcn-early-release.py" on terminal and scan the QR with a phone.

Requirements:
 - Python 3
 - FastAPI
 - pydantic
 - uvicorn
 - selenium (+geckodriver)
 - requests
 - Firefox


Classes of Whatsapp Web change with time, so the code has to be updated with the proper new classes. Example: Line 114 points to the user name ('id'). (More info on /classes/ and in the last lines of portbcn-early-release.py)

By now the location retrieved is always the first one that was sent. If it isn't the first time you run the bot, you should clear its chat history first in order to get the proper location.
