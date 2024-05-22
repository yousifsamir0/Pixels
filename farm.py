import vision 
import Player
import time
import math
# from web_driver import Chrome
from driver.pixels_driver import HUD,Items
from utils import is_land_need_shear,wait_if_needed,update_and_save_land_status
from driver.core.commands import plant_command,water_command,shear_command


TIME_TO_GROW = 1 # minuts
SEED_NAME= 'popberrySeeds'
SEED = SEED_NAME+'.png'
ENERGY_BLOL = 'energydrink.png'
ENERGY_DRINK_AMOUNT = 50
REQUIRED_ENERGY = 220
CHECK_ENERGY = False


v = vision.Vision()
p = Player.Player()
# c = Chrome()



def callback_base(item_blob,short_cut_number):
    # if (not Items.is_slot_selected(short_cut_number)):
    #     if (Items.is_slot_empty(short_cut_number)):  
    #         if Items.get_item_count(item_blob):
    #             Items.put_item_in_slot(item_blob,short_cut_number)
    #             Items.shrink_items_if_not()
    #         else:#todo
    #             return False
    v.press('esc')
    v.press(str(short_cut_number))

def farm_shear():
    callback_base('shears.png',1)
    return (0.07)
def farm_plant():
    callback_base(SEED,3)
    return (0.07)
def farm_water():
    callback_base('water.png',2)
    return (0.07)
def farm_energy():
    v.press('esc')
    v.press('4')



def farm_sort_items(seed):
    # Player.check_and_activate_window()
    items =  ['shears.png','water.png',seed,'axe.png']
    if CHECK_ENERGY:
        items.append(ENERGY_BLOL)
    Items.sort_items(items)




def use_energy():
    farm_energy()
    playerPos= (830,550)
    v.click_on(playerPos)
    time.sleep(0.2)
    


def check_energy(first=False):
    if CHECK_ENERGY:
        energy_drink_count = Items.get_item_count(ENERGY_BLOL)
        required_e_count = math.ceil(REQUIRED_ENERGY/ENERGY_DRINK_AMOUNT)
        if energy_drink_count< required_e_count:
            print('[check_energy:LOGS]:energy_drink_count< required_e_count')
            return False
        currentEnergy = Items.get_energy()
        if currentEnergy <  REQUIRED_ENERGY:
            for i in range(required_e_count):
                if (ENERGY_DRINK_AMOUNT+currentEnergy > 1000):
                    print('[LOG:energy] energy will exceed 1000, stopping...')
                    return False
                use_energy()
                currentEnergy = Items.get_energy()
        return True
    else: 
        return True


# from driver.core.parser import WebSocketParser
def farm_land(landNumber,shearOnly = False,accountNumber=None):
    HUD.travel_bookmark(landNumber)
    seed_count = Items.get_item_count(SEED)
    shear = is_land_need_shear(landNumber,accountNumber=accountNumber)
    plant = not shearOnly and bool(seed_count)
    wait_if_needed(landNumber,accountNumber=accountNumber)
    if not check_energy():
        print('[farm_land:LOGS]:energyProblem: ',landNumber)
        return False
    if shear:
        # callbacks.append(farm_shear)
        HUD.driver.sendWS(shear_command())
    if plant:
        HUD.driver.sendWS(plant_command(seed_count,SEED_NAME))
        time.sleep(1)
        HUD.driver.sendWS(water_command())
        # callbacks.extend([farm_plant,farm_water])
        pass
    if not shear and not plant:
        print('[farm_land:LOGS]:no Shear/plant: ',landNumber)
        return False
    update_and_save_land_status(landNumber,plant,time.time(),TIME_TO_GROW,accountNumber=accountNumber)
    return True

def farm_land_range(landrange,shearOnly=False,accountNumber=None):
    for i in range(landrange[0],landrange[1]+1):
        ret = farm_land(landNumber=i,shearOnly=shearOnly,accountNumber=accountNumber)
        if not ret:
            return False
        


if __name__ == '__main__':    
    Player.check_and_activate_window()
    # farm_account(1,1)












# def farm_task():
#     count = 0
#     lastCount = 2
#     farm_sort_items()
#     timer = time.time()-10000
#     state = FARM_STATE
#     time1 =time.time()
#     while (count<=lastCount):
#         farm = False if count == lastCount else True
#         shear = False if count == 0 else True
#         v.travel_to_bookmark(3) #1043
#         p.play('farm/1019_soil')
#         while(time.time()-timer<60):
#             pass
#         farm_land(farm=farm,shear=shear)
#         timer = time.time()
#         v.travel_to_bookmark(2) #1043
#         p.play('farm/1019_soil')
#         farm_land(farm=farm,shear=shear)
#         count +=1
#     print('time taken: ',time.time()-time1)
# def farm_click_area(area_pos):
#     x,y,found = v.find_image_position(area_pos,0.8)
#     # if not found:

#     x,y = SOIL_BL_pos if (area_pos==SOIL_BL) else SOIL_BR_POS if (area_pos==SOIL_BR) else SOIL_TR_POS if (area_pos==SOIL_TR) else SOIL_TL_POS
#     # v.move_on((x,y))
#     x_,y_ = (x,y)
#     y_sign = -1 if area_pos == SOIL_BL or area_pos == SOIL_BR else 1
#     x_sign = 1  if area_pos == SOIL_BL or area_pos == SOIL_TL else -1
#     for ver in range (3):
#         y_ = y+(ver*64*y_sign)
#         for h in range(5):
#             x_ = x+(h*64*x_sign)
#             v.click_on((x_,y_))
#             time.sleep(0.05)

# def farm_land(farm=True,shear=False):
#     areas = [SOIL_BL,SOIL_TL,SOIL_TR,SOIL_BR]
#     moves = [BL_TL,TL_TR,TR_BR]
#     # farm_sort_items()
#     for i in range(4):
#         if (shear):
#             v.press('esc')
#             v.press('1')
#             farm_click_area(areas[i])
#         if (farm):
#             v.press('esc')
#             v.press('3')
#             farm_click_area(areas[i])
#             v.press('esc')
#             v.press('2')
#             farm_click_area(areas[i])
#         if i != 3:
#             p.play(moves[i])

# def defarm_land():
#     areas = [SOIL_BL,SOIL_TL,SOIL_TR,SOIL_BR]
#     moves = [BL_TL,TL_TR,TR_BR]
#     for i in range(4):
#         v.press('esc')
#         v.press('1')
#         # farm_click_area(areas[3-i])
#         farm_click_area(areas[i])
#         if i != 3:
#             # p.play(moves[2-i],reverse=True)
#             p.play(moves[i])

# def farm_sort_items():
#     Player.check_and_activate_window()

#     v.press('b')
#     time.sleep(0.9)

#     shears,found = v.wait_till_object_found(SHEARS)
#     v.click_on(shears)
#     time.sleep(0.2)
#     v.click_on(FIRST_SLOT)
#     time.sleep(0.1)
#     v.press('esc')
#     time.sleep(0.1)

#     water,found = v.wait_till_object_found(WATER)
#     v.click_on(water)
#     time.sleep(0.1)
#     v.click_on(SECOND_SLOT)
#     time.sleep(0.1)
#     v.press('esc')
#     time.sleep(0.1)

#     seeds,found = v.wait_till_object_found(SEEDS)
#     v.click_on(seeds)
#     time.sleep(0.1)
#     v.click_on(THIRD_SLOT)
#     time.sleep(0.1)
#     v.press('esc')
#     time.sleep(0.1)

#     v.press('esc')
#     time.sleep(0.2)
#     v.press('b')
#     time.sleep(0.5)

# def farm_record_land():
#     allCallbacks = [farm_shear,farm_plant,farm_water,]
#     callbacks =[] 
#     count = 0
#     lastCount = 2
#     farm_sort_items()
#     timer = time.time()-10000
#     time1 =time.time()
#     while (count<=lastCount):
#         callbacks.append(farm_shear) if count != 0 else None
#         callbacks.extend([farm_plant,farm_water]) if count != lastCount else None
#         v.travel_to_bookmark(3) #1043
#         # while(time.time()-timer<60):
#         #     pass
#         p.play('1043_farm',farm=True,farm_calbacks=callbacks)
#         # timer = time.time()
#         v.travel_to_bookmark(2) #1043
#         p.play('1043_farm',farm=True,farm_calbacks=callbacks)

#         callbacks = []
#         count += 1
#     print('time taken: ',time.time()-time1)
        