# Port-Bot

This is a prototype I kept developing after winning a contest with it. It is unknown if it will be implemented. It could build a good source of data to train an actual bot. For it to be responsive enough and handle multiple users, it should be implemented on WhatsApp Business. I will keep spending my spare time on the database and the frontend. The next steps are to make it handle pictures and build a toggle to check if the incident is solved or not.

Run it from its folder by typing "python3.7 start.py" and scan the QR code with a phone. Message him from another phone to initialize it. It can only handle a message every 7 seconds aprox.

The frontend is at 127.0.0.1:8000/dashboard/

Requirements:
 - Python 3.7
 - Golang 1.12*
 - Firefox
 - Geckodriver
 - Drive**
 
Libraries:
 - FastAPI
 - pydantic
 - uvicorn
 - sqlalchemy
 - selenium
 - requests


Classes of Whatsapp Web change with time, so the code has to be updated with the proper new classes. More info on /classes/ and in the last lines of port-bot.py)

*https://golang.org/doc/install?download=go1.12.darwin-amd64.pkg  
**https://github.com/odeke-em/drive
