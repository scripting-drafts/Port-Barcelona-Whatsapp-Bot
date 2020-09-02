from threading import Thread, Event
import subprocess

def uvicorn():
    subprocess.Popen('uvicorn main:app --reload', stdin=None, stderr=None, shell=True).communicate()

thread = Thread(target=uvicorn)

thread.start()

subprocess.Popen('python3.7 portbcn-early-release.py', stdin=None, stderr=None, shell=True).communicate()

thread.join()
