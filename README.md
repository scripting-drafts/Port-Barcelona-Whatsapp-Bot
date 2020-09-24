# Port-Bot

This is a prototype I keep developing in my spare time. It could build a good source of data to train an AI. Soon available on GNU/Linux, currently testing on OS X. 

Run it from its folder by typing "python3.7 start.py" and scan the QR code with a phone. Message him from other phones to initialize it. I added a queue in order to handle multiple users.

The frontend is at 127.0.0.1:8000/items/ and 127.0.0.1:8000/invalid_items/

Requirements:
 - Python 3.7
 - Golang 1.12* (OS X)
 - Firefox
 - Geckodriver
 - Drive**
 - Curl
 
Libraries:
 - FastAPI
 - pydantic
 - uvicorn
 - sqlalchemy
 - selenium
 - requests
 - jinja2
 - starlette


Classes of Whatsapp Web change with time, so the code has to be updated with the proper new classes. More info on /classes/ and in the CSS SELECTORS section of port-bot.py

*https://golang.org/doc/install?download=go1.12.darwin-amd64.pkg  
**https://github.com/odeke-em/drive
  
  
# Next Steps

* Port-bot cleanup
* Embedded Google Maps on the Frontend
* Better HTML/Javascript for a more responsive Active/Resolved functionality
