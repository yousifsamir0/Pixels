import time
from pynput import keyboard,mouse

import threading




class Record:
    def __init__(self,key,duration) -> None:
        self.key=key
        self.duration=duration

class Recorder():
    def __init__(self):
        self.records = []
        self.is_recording = False
        self.listener = None
        self.mouseListener = None
        self.key_pressed_time = {}
        self._is_reverse = False
        self._lock = threading.Lock()
    def clear_records(self):
        self.records = []
    def is_empty(self):
        return (not len(self.records))
    def on_click_press(self,x, y, button, pressed):
        if pressed and button == mouse.Button.left :
            self.records.append( ('mouse', (x,y)) )
            print('click recorded at ({},{})'.format(x,y))
        if pressed and button == mouse.Button.right:
            print('mouse record stopped you can use mouse now xD')
            return False        


    def on_press(self, key):
        if hasattr(key,'char'):
            if key.char=='m':
                self.mouseListener = mouse.Listener(on_click=self.on_click_press)
                self.mouseListener.start()
                print('mouse recording started, press right-click to stop it')
            elif self.is_recording and key not in self.key_pressed_time:
                timestamp = time.time()
                self.key_pressed_time[key] = timestamp
                # print('[keyPress]:pressed: ',timestamp)
    def on_release(self, key):
        # print('[keyPress]:pressed: ',key)
        if self.is_recording and key in self.key_pressed_time:
            duration = time.time() - self.key_pressed_time[key]
            self.key_pressed_time.pop(key)  # Remove key press start time
            self.records.append((key.char, duration))


    def start_recording(self):
        self.is_recording = True
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
            

    def stop_recording(self):
        self.is_recording = False
        if self.listener:
            self.listener.stop()
        if self.mouseListener:
            self.mouseListener.stop()
        print(self.records)
        # return self.records

    def _replay(self,records):
     
        for key, duration in records:
            if key != 'mouse':
                keyboard.Controller().press(key)
                time.sleep(duration+0.01)  # Hold the key for the recorded duration
                keyboard.Controller().release(key)
                time.sleep(0.08)  # Adjust this delay as needed
            else:
                print(type(duration))
                print(duration)
                mouse.Controller().position=duration
                mouse.Controller().click(mouse.Button.left,1)
                time.sleep(0.35) #todo


    def play(self,reverse=False):
        self._is_reverse =reverse
        new_thread = threading.Thread(target=self.run)
        new_thread.start()


    def replay_reverse(self,records):
        reversed =  records.copy()
        reversed.reverse()
        for i,tup in enumerate(reversed):
            temp_list = list(tup)  
            duration=temp_list[1]
            key=temp_list[0]
            if   (key=='w'): key =  's'
            elif (key=='s'): key =  'w'  
            elif (key=='a'): key =  'd'   
            elif (key=='d'): key =  'a'  
            reversed[i] = (key,duration)
        return reversed
    def run(self):
        with self._lock:
            print('[LOG]: play Run')
            if self._is_reverse:
                self._replay(self.replay_reverse(self.records))
            else:
                self._replay(self.records)



# recorder = Recorder()
# recorder.start_recording()

# time.sleep(10)  # Simulate 10 seconds of keystrokes

# recorder.stop_recording()

# # Replay the recorded keystrokes
# recorder.replay_keystrokes(reverse=True)
# recorder.replay_keystrokes(reverse=False)