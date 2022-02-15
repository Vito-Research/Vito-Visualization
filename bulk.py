import subprocess
import time
import os

def app_is_open():
    return "Vito" in os.popen("ps ax").read()

def kill_app():
    os.popen("killall Vito")

if __name__ == "__main__":
    while True:
        print("Checking if open...")
        if app_is_open():
            print("App is running.")
        else:
            print("App is not running.")
            subprocess.run("open /Applications/Vito.app".split())
            print("Opened app.")

        time.sleep(30)