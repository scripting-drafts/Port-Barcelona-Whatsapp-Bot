# Port-Bot

Currently testing on OS X.

Run it from its folder by typing "python3.7 start.py" and scan the QR code with a phone. Message him from another phone to initialize it. It can only handle a message every 7 seconds aprox.

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
