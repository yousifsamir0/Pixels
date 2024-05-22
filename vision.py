import pyautogui
import time
import math
# import Player

pyautogui.FAILSAFE =False
STD_W = 1600
STD_H = 900-40 # 40px TaskBar
screenWidth, screenHeight = pyautogui.size()
# DIFF_X_BY_2,DIFF_Y_BY_2 =(int((screenWidth-STD_W)/2),int((screenHeight-STD_H)/2))
# ROI = ((0+DIFF_X_BY_2),(90+DIFF_Y_BY_2),STD_W,775)
ROI = (0,40,STD_W,820)
SELF_XY = (STD_W/2, (STD_H+ 40)/2)
GATE_TEMPELATE = 'images/gate2.png'
CLOSED_GATE = 'images/closed.png'
CHICKENS_TEMPELATE = 'images/chicken3.png'
HONEY_TEMPELATE = 'images/honey.png'
HONEY_INNER_TEMPELATE = 'images/honeytag.png'
EMPTY_HONEY_TEMPELATE = 'images/emptyhoney.png'
LEFT_PORTAL = 'images/leftportal.png'
LAND_BTN = 'images/land_btn.png'
HUD = 'images/hud.png'
BOOKMARK_BTN = 'images/bookmark_btn.png'
GO_TRAVEL_BTN = 'images/go_travel2.png'
PLAYER = 'images/player.png'
PLAYER_LEFT = 'images/player_left.png'
PLAYER_LEFT_PART = 'images/player_left_part.png'
PLAYER_RIGHT = 'images/player_right.png'
PLAYER_RIGHT_PART = 'images/player_right_part.png'
TERRAVILLA = 'images/terravilla.png'
SAUNA_PORTAL = 'images/portal.png'
SAUNA_STONE = 'images/sauna_stone.png'
LOGOUT = 'images/logout.png'
WORLD = 'images/world.png'
START_GAME = 'images/start_game.png'
SERVER_BAR = 'images/serverbar.png'
EMAIL_BTN = 'images/emailbtn.png'
EMAIL_METHOD = 'images/email_method.png'
SUBMIT_BTN = 'images/submit_btn.png'
RONIN_WALLET = 'images/ronin.png'
RONIN_ACCOUNTS = 'images/ronin_accounts.png'
RONIN_NETWORK = 'images/ronin_network.png'
RONIN_CONNECT = 'images/ronin_connect.png'
RONIN_SIGNIN = 'images/ronin_signin.png'
RONIN_SIGNIN_EXTENSION = 'images/ronin_signin_extension.png'
ERROR_RELOAD = 'images/err_reload.png'
ERROR_LOGOUT = 'images/err_logout.png'
R_ACCOUNT_NUMBER = 39




def calculate_distance(target,isBox = False):
    x2,y2 = SELF_XY
    x,y = (0,0)
    if isBox:
        x,y,width,height = target
        x,y = (x+width/2),(y+height/2)
    else:
        x,y = target
    return math.sqrt(((x-x2)**2) + ((y-y2)**2))

def apply_threshold(found_objects,threshold):
    newObjects = []
    for object in found_objects:
        if calculate_distance(object,True) < threshold:
            newObjects.append(object)
    return newObjects

def remove_redundant_boxes1(found_objects, threshold):
    # if len(found_objects) <= 1:
    #     return found_objects
    # Sort the list of found objects based on distance
    sorted_objects = sorted(found_objects, key=lambda x: calculate_distance(x,True))
    # Initialize a list to store the non-redundant objects
    non_redundant_objects = [sorted_objects[0]]
    # Iterate over the sorted list and remove redundant objects
    for i in range(1, len(sorted_objects)):
        if calculate_distance(sorted_objects[i],True) - calculate_distance(non_redundant_objects[-1],True) > threshold:
            non_redundant_objects.append(sorted_objects[i])
    return non_redundant_objects
def remove_redundant_boxes(found_objects, threshold):
    # Sort the list of found objects based on distance
    sorted_objects = sorted(found_objects, key=lambda x: x[0])
    # Initialize a list to store the non-redundant objects
    non_redundant_objects = [sorted_objects[0]]
    # Iterate over the sorted list and remove redundant objects
    for i, object in enumerate(sorted_objects):
        found = False
        if not i : continue
        for nonRobject in non_redundant_objects:        
            if abs(object[0] - nonRobject[0]) < threshold and abs(object[1] - nonRobject[1]) < threshold:
                found=True
                break
        if not found:
            non_redundant_objects.append(object)
            found = False

    return non_redundant_objects


class Vision:
    def __init__(self) -> None:
        pass
      
    def click_nearest_chickens(self,confidence=0.5):
            nearsest_distance = 2000
            nearest_box = None
            boxes,found = self.wait_till_n_objects_found(CHICKENS_TEMPELATE,count=1,confidence=confidence,grayscale=True)
            if not found:
                return False
            # pyautogui.locateAllOnScreen(CHICKENS_TEMPELATE,region=ROI,grayscale=True,confidence=confidence):
            for box in boxes:
                distance = calculate_distance(box,True)
                if distance < nearsest_distance:
                     nearsest_distance = distance
                     nearest_box = box
            self.click_on(nearest_box,checkX=True)
            self.move_on((SELF_XY[0],SELF_XY[1]),duration=0.1)
            return True
    def click_all_objects(self,object,confidence=0.95,innerObj=None):
            # boxes = pyautogui.locateAllOnScreen(object,region=ROI,grayscale=False,confidence=confidence)
            boxes,found = self.wait_till_n_objects_found(object,count=4,confidence=confidence)
            if not found:
                return False
            boxes = apply_threshold(boxes,370)
            for box in boxes:
                print('found object with pos ({},{})',(box[0]),box[1])
                if innerObj != None:
                    # innerPoint = pyautogui.locateCenterOnScreen(innerObj,region=box,confidence=0.6)
                    inner,found = self.wait_till_object_found(innerObj,0.6,roi=box)
                    self.click_on(inner,0.15,checkX=True)
                    # self.move_on(innerPoint,0.15)
                else:
                    self.click_on(box,0.20,checkX=True)
                    # self.move_on(box,0.20)
                # time.sleep(0.25)
            return True

    def find_image_boxes(self,image_path,confedence=0.5,grayscale=False,log=True,roi=ROI):
        try:
            boxes = pyautogui.locateAllOnScreen(image_path,region=roi,grayscale=grayscale,confidence=confedence)
            boxes = [box for box in boxes]
            boxes = remove_redundant_boxes(boxes,20)
            return (boxes,True)
        except pyautogui.ImageNotFoundException:
            if log:
                print('[LOG]:: "{}" template not found in frame'.format(image_path))
            return ([],False)
        except:
            return ([],False)

    def find_image_position(self,image_path,confedence=0.5,grayscale=False,log=True,roi=ROI):
        try:
            x,y = pyautogui.locateCenterOnScreen(image_path,region=roi,grayscale=False,confidence=confedence)
            return (x,y,True)
        except pyautogui.ImageNotFoundException:
            if log:
                print('[LOG]:: "{}" template not found in frame'.format(image_path))
            return (-1,-1,False)
    def find_image_box(self,image_path,confedence=0.5,grayscale=False,log=True,roi=ROI):
        try:
            box = pyautogui.locateOnScreen(image_path,region=roi,grayscale=False,confidence=confedence)
            return (box,True)
        except pyautogui.ImageNotFoundException:
            if log:
                print('[LOG]:: "{}" template not found in frame'.format(image_path))
            return ((-1,-1),False)
      

    
    def travel_to_bookmark(self,bookmark_index):
        print('entered travel')
        self.open_land_travel()
        time.sleep(0.25)
        x,y,found=self.find_image_position(BOOKMARK_BTN,0.8,True)
        if not found:
            print('landBTN not found')
            pass
        self.click_on((x,y),0)
        time.sleep(0.3)
        
        boxes,found=self.find_image_boxes(GO_TRAVEL_BTN,confedence=0.97)
        if not found:
            return False
        boxes = sorted(boxes, key=lambda tup: (tup[1], tup[0]))

        # for box in boxes:
        #     self.move_on(box)
        #     time.sleep(0.9)
        # print(boxes)
        # return
        # #debug
        # print(len(boxes))
        # for box in boxes:
        #     self.move_on(box)
        #     time.sleep(2)
        #     print('clicked box number at {} ',box)
        # return
        # #debug
        # boxes = sorted(boxes,key=lambda x : x[0])
        self.click_on(boxes[bookmark_index-1],0.20)
        self.wait_untill_travel()

    def wait_untill_travel(self):
        time.sleep(0.7)
        self.wait_till_object_found(LAND_BTN,grayscale=True,confidence=0.7,timeout=60)
        print('found HUD')
        time.sleep(1)
    def wait_untill_land_travel(self):
        self.wait_till_object_notfound(LAND_BTN)
        self.wait_till_object_found(LAND_BTN,timeout=60)
        time.sleep(2.1)

    def travel_to_terravilla(self):
        self.open_land_travel()
        time.sleep(0.3)
        x,y,found = self.find_image_position(TERRAVILLA,0.8)
        if not found:
            pass
        self.click_on((x,y),0.2)
        self.wait_till_object_found(LAND_BTN,timeout=60)
        time.sleep(0.5)

    # def get_images_boxes(self,image_path,confidence=0.5):
    #     try: 
    #         boxes = pyautogui.locateAllOnScreen(image_path,region=ROI,grayscale=True,confidence=confidence)
    #         return (list(boxes))
    #     except pyautogui.ImageNotFoundException:
    #         return 
            

    def click_on(self,object_position=None,duration=0.1,save=False,checkX=False):
        if object_position == None:
            pyautogui.click()
            return
        xCurrent,yCurrent = pyautogui.position()
        x,y = (0,0)
        if len(object_position) > 2:
            x,y,width,height = object_position
            x,y = (x+width/2),(y+height/2)
        else:
            x,y = object_position
        pyautogui.click(x,y,duration=duration)
        if checkX :
            time.sleep(0.4)
            x,y,found=self.find_image_position('images/x1.png',0.8)
            if found:
                pyautogui.click(x,y,duration=0.2)
                time.sleep(0.2)
        if save:
            pyautogui.moveTo(xCurrent,yCurrent)
    def move_on(self,object_position,duration=0.1,save=False):
        xCurrent,yCurrent = pyautogui.position()
        x,y = (0,0)
        if len(object_position) > 2:
            x,y,width,height = object_position
            x,y = (x+width/2),(y+height/2)
        else:
            x,y = object_position
        pyautogui.moveTo(x,y,duration=duration)
        if save:
            pyautogui.moveTo(xCurrent,yCurrent)

    def open_land_travel(self):
        x,y,found=self.find_image_position(LAND_BTN,grayscale=True,confedence=0.7)
        if not found:
            print('LAND_BTN not found')
            pass
        self.click_on((x,y),0.25)

    def wait_till_object_found(self,object,confidence=0.8,grayscale=False,roi=ROI,timeout=5):
        # exist = False
        t = time.time()
        while(True):   
            x,y,found = self.find_image_position(object,confidence,grayscale,roi=roi)
            if (found):
                return ((x,y),True)
            if ((time.time()-t) > timeout): return ((x,y),False)
    
    def wait_till_n_objects_found(self,object,count,timeout=5,confidence=0.8,grayscale=False,roi=ROI):
        t = time.time()
        while(True):   
            boxes,found = self.find_image_boxes(object,confidence,grayscale,roi=roi)
            if (found and len(boxes) >= count):
                return (boxes,True)
            if ((time.time()-t) > timeout): return (boxes,True) if len(boxes) else ([],False)
    
    def wait_till_object_notfound(self,object,confidence=0.8,grayscale=False,roi=ROI):
        exist = True
        while(exist):      
            if (not self.find_image_position(object,confidence,grayscale,roi=roi)[2]):
                exist = False
    def scroll_untill_object_found(self,object,position,confidence=0.8,grayscale=False):
        while(True):
            x,y,found = self.find_image_position(object,confidence,grayscale)
            if found:
                return(x,y)
            else:
                pyautogui.moveTo(SELF_XY[0],SELF_XY[1])
                pyautogui.scroll(-250)
    def write(self,text,interval):
        pyautogui.write(text,interval)
    def press(self,key):
        pyautogui.press(key)
    def mouse_move(self,x, y, rel=False):
        if rel:
            pyautogui.moveRel(x,y)
        else:
            pyautogui.moveTo(x,y)
    def left_mouse_hold(self,posX,posY,duration):
        pyautogui.mouseDown(posX,posY)
        time.sleep(duration)  # Holding the click for duration sec
        pyautogui.mouseUp(posX,posY)






def scroll_to_account(acc_indx):
    if acc_indx > R_ACCOUNT_NUMBER:
        print('[LOG::SCROLL] account index out of range')
        return 
    scroll_limit = R_ACCOUNT_NUMBER - 3
    scroll_per_account = -88
    move_per_account = 72

    if (acc_indx>scroll_limit):
        pyautogui.scroll((scroll_limit-1)*scroll_per_account)
        pyautogui.moveRel(0,move_per_account*(acc_indx-scroll_limit))
    else:
        pyautogui.scroll((acc_indx-1)*scroll_per_account)
    time.sleep(0.2)
    pyautogui.click()


if __name__ == '__main__':
    Player.check_and_activate_window()
    vis = Vision()
    vis.click_all_objects(HONEY_TEMPELATE,0.6,HONEY_INNER_TEMPELATE)

    # vis.click_all_objects(HONEY_TEMPELATE,0.5,HONEY_INNER_TEMPELATE)