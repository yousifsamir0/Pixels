from pynput import keyboard,mouse
import vision
import time
import pickle
from multiprocessing import Process
import pygetwindow as gw


def check_and_activate_window():
        # Get all windows
    windows = gw.getAllWindows()
    keyword = 'Pixels:'
    # keyword = 'Laka'
    # Filter windows containing the keyword in their titles
    matching_windows = [window for window in windows if keyword in window.title]
    print(matching_windows)
    # Check if any matching window found
    if matching_windows:
        # Activate the first matching window
        
        matching_windows[0].restore()
        matching_windows[0].resizeTo(vision.STD_W+16,vision.STD_H+8) 
        # matching_windows[0].moveTo(vision.DIFF_X_BY_2-8,vision.DIFF_Y_BY_2) 
        matching_windows[0].moveTo(0-8,0)
        matching_windows[0].activate()
        print(f"Window containing '{keyword}' activated.")
    else:
        print(f"No window containing '{keyword}' found.")
    

class Player:

    def __init__(self):
        self.current_file = None
        self.prevKey= None
        self.objList= []
        self.calbacks=[]
        self.clicks = []
        self.vision:vision.Vision = vision.Vision()

    def play(self,filename,reverse=False,callback=False,farm=False,farm_calbacks=[],):
        self.vision.click_on((26,115))
        print('[player]: start walking...')
        if farm:
            self.calbacks = farm_calbacks
        self.current_file = filename
        command_list = self.get_file()
        p=None
        if reverse:
            command_list =self._reverse_commands(command_list)
        # print(command_list)
        if callback:
            p= Process(target=callback)
            p.start()
        self.play_commands(command_list)
        if(callback):
            p.terminate()
            p.join()
    
    def play_commands(self,command_list):
        moving_keys = ['w','a','s','d']
        for key,duration in command_list:
    
            if key in moving_keys:
                self._play_move(key,duration)
            elif key =='mouse':
                self._play_click(key,duration)
            else:
                self._play_action(key,duration)
        if self.prevKey == 'mouse':
            self._play_clicks_with_callbacks()
        time.sleep(0.7) #todo:  check this time


    def _play_move(self,key,duration):
        if self.prevKey == 'mouse':
            self._play_clicks_with_callbacks()
        keyboard.Controller().press(key)
        time.sleep(duration+0.01)  # Hold the key for the recorded duration
        keyboard.Controller().release(key)
        self.prevKey = key
        time.sleep(0.08)  # Adjust this delay as needed
    def _play_click(self,key,position):
        self.prevKey = key
        self.clicks.append(position)
    def _play_action(self,key,duration):
        if self.prevKey == 'mouse':
            self._play_clicks_with_callbacks()
        if self.prevKey == key:
            return
        time.sleep(0.5)
        if key == 'c':
            self.vision.click_nearest_chickens()
        if key == 'h':
            self.vision.click_all_objects(vision.HONEY_TEMPELATE,0.6,vision.HONEY_INNER_TEMPELATE)
        self.prevKey = key

    def _play_clicks_with_callbacks(self):
        if len(self.clicks):
            for callback in self.calbacks:
                for position in self.clicks:
                    wait_time=callback()
                    self.vision.click_on(position)
                    time.sleep(wait_time)
            
                # self.clicks.reverse()
            self.clicks=[]

    def _reverse_commands(self,records):
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
    def get_file(self):   
        try:
            with open(self.current_file+'.pkl', 'rb') as f:
                command_list = pickle.load(f)
            return command_list
        except FileNotFoundError:
            print(f"{self.current_file}: File not found.")
            return []
    def get_commands_from_file(self,filename):   
        self.current_file = filename
        return self.get_file()
    def isRecordAvailable(self,filename):   
        return len(self.get_commands_from_file(filename))!=0
