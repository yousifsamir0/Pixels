import os
import json
import time
import requests
import hashlib
import base64
from PIL import Image
from io import BytesIO

def read_time_and_minutes(filename):
    if os.path.exists(filename):
        with open(filename+'.txt', 'r') as file:
            # Read the first line (time in seconds since the epoch)
            time_str = file.readline().strip()
            time_seconds = float(time_str)
            
            # Read the second line (number of minutes)
            minutes_str = file.readline().strip()
            minutes_float = float(minutes_str)
            
            return time_seconds, minutes_float
    else:
        print(f"File '{filename}' does not exist.")
        return None, None
    
def write_time_and_minutes(filename, minutes):
    # Get the current time in seconds since the epoch
    current_time_seconds = time.time()
    # Convert minutes to a string
    minutes_str = str(minutes)
    # Write the current time and number of minutes to the file
    with open(filename+'.txt', 'w') as file:
        # Write the current time to the first line
        file.write(f"{current_time_seconds}\n")
        
        # Write the number of minutes to the second line
        file.write(f"{minutes_str}\n")


def load_or_create_land_status(land_number, folder):
    # Ensure that the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    filename = f"{folder}/land_{land_number}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    else:
        default_status = {"is_planted": False, "time_planted": None, "minutes_to_harvest": 0}
        with open(filename, 'w') as f:
            json.dump(default_status, f, default=str)
        return default_status

def update_and_save_land_status(land_number, new_is_planted, new_time_planted, new_minutes_to_harvest,accountNumber=None ):
    folder = 'status' if not accountNumber else f'accounts/{accountNumber}/status'
    filename = f"{folder}/land_{land_number}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            land_status = json.load(f)
        land_status["is_planted"] = new_is_planted
        land_status["time_planted"] = new_time_planted
        land_status["minutes_to_harvest"] = new_minutes_to_harvest
        with open(filename, 'w') as f:
            json.dump(land_status, f, default=str)
    else:
        print(f"Land {land_number} does not exist.")

def is_land_need_shear(land_number,accountNumber=None):
    folder = 'status' if not accountNumber else f'accounts/{accountNumber}/status'
    status = load_or_create_land_status(land_number,folder)
    if status['is_planted']:
        return True
    else:
        return False
def wait_if_needed(land_number,accountNumber=None):
    folder = 'status' if not accountNumber else f'accounts/{accountNumber}/status'
    status = load_or_create_land_status(land_number,folder)
    if status['is_planted']:
        diff = status['time_planted']+(60*status['minutes_to_harvest']) - time.time()
        time_to_wait = max(diff,0)
        time.sleep(time_to_wait)



def compare_blob_image_with_disk(driver,blob_url, local_image_path):
        base64_data  = get_blob_content_as_base64(driver,blob_url).split(',')[1]
        # Decode base64 data
        image_bytes = base64.b64decode(base64_data)
        
        # Load image from bytes
        downloaded_image = Image.open(BytesIO(image_bytes))
        # Calculate MD5 hash of the downloaded image
        downloaded_image_md5 = hashlib.md5(image_bytes).hexdigest()
    
        # Calculate MD5 hash of the image on disk
        with open(local_image_path, 'rb') as f:
            local_image_md5 = hashlib.md5(f.read()).hexdigest()

        # Compare MD5 hashes
        if downloaded_image_md5 == local_image_md5:
            # print("Images are exactly the same.")
            return True
        else:
            # print("Images are not the same.")
            return False
        
def get_blob_content_as_base64(driver, blob_url):
    script = f'''
    var callback = arguments[arguments.length - 1];
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "{blob_url}", true);
    xhr.responseType = "blob";
    xhr.onload = function() {{
        var reader = new FileReader();
        reader.onloadend = function() {{
            callback(reader.result);
        }};
        reader.readAsDataURL(xhr.response);
    }};
    xhr.send();
    '''
    return driver.driver.execute_async_script(script)


STATE_FILE = "state.txt"
DEFAULT_STATE = "s1"
def get_state():
    """Read the state from the state file. If file doesn't exist, create it with default state."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return f.read().strip()
    else:
        with open(STATE_FILE, 'w') as f:
            f.write(DEFAULT_STATE)
        return DEFAULT_STATE

def update_state(new_state):
    """Write the new state to the state file."""
    with open(STATE_FILE, 'w') as f:
        f.write(new_state)



def wait_until(condition_fn, timeout=20, interval=0.1):
    """
    Waits until the condition function returns True or timeout is reached.
    
    Args:
        condition_fn: A lambda function that returns True or False.
        timeout (float): Timeout period in seconds (default is 30 seconds).
        interval (float): Interval between checks in seconds (default is 0.1 seconds).
        
    Returns:
        True if the condition becomes True within the timeout period, False otherwise.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition_fn():
            return True
        time.sleep(interval)
    return False