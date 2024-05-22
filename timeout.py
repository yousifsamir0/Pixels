import vision as v
import Player
import time
import requests

def check_internet():
    while True:
        try:
            # Attempt to make a GET request to a reliable website
            response = requests.get("http://www.google.com", timeout=5)
            # If the response status code is 200, internet connection is available
            if response.status_code == 200:
                print("Internet connection is available.")
                return True
        except Exception as e:
            # If an exception occurs (connection error or timeout), internet connection is not available
            print(f"No internet connection. Waiting 1 minute before retrying...")
            time.sleep(60)  # Wait for 1 minute before retrying

def handle_errors():
    vo = v.Vision()
    check_internet()
    Player.check_and_activate_window()
    time.sleep(0.1)
    reloadX,reloadY,found = vo.find_image_position(v.ERROR_RELOAD,0.8)
    if found:
        vo.click_on((reloadX,reloadY))
    logoutX,logoutY,found = vo.find_image_position(v.ERROR_LOGOUT,0.8)
    if found:
        vo.click_on((logoutX,logoutY))
    

handle_errors()
