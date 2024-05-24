import Player
from farm import SEED,SEED_NAME, farm_land_range, farm_sort_items,callback_base
from net.client import Client
from utils import wait_until
import vision
import time
from driver.pixels_driver import HUD,Items,Market,Trade
from driver.core.commands import sell_items_command,buy_from_hazel_command, cut_trees_command,collect_wood_command

player = Player.Player()


def collect_from_land(lanRange,bookmarkIndx,start=False,default_postfix="_C"):
    # for j in range(count):
    Player.check_and_activate_window()
    timer_start = None if start else time.time() 
    prefix= 'land_records/'
    start_land= lanRange[1]
    end_land = lanRange[0]     #lower bound
    interval = abs(start_land - end_land)+1
    player.vision.travel_to_bookmark(bookmarkIndx)

    for i in range(interval):
        postfix= default_postfix if not i else '_R'
        landNumber= str(start_land-i)
        commandList = player.get_commands_from_file(prefix+landNumber+postfix)

        if (player.vision.find_image_position(vision.CLOSED_GATE)[2]) or (not len(commandList)): #land #1415:
            player.play(prefix+'leave_R2L')
            player.vision.wait_till_object_notfound(vision.LAND_BTN)
            player.vision.wait_till_object_found(vision.LAND_BTN,timeout=60)
            time.sleep(2.1)
        else:
            player.play(prefix+landNumber+postfix)
            if timer_start==None:
                timer_start = time.time()
            if (i != interval-1):
                player.play(prefix+'leave_L')
                player.vision.wait_till_object_notfound(vision.LAND_BTN)
                player.vision.wait_till_object_found(vision.LAND_BTN,timeout=60)
                time.sleep(2.1)
    #minutes from 1st click to finish the range of land to - from sleep duration
    timer_minutes = (time.time()-timer_start)/60 
    print("finished land range {} after {:.{}f} minutes.".format(lanRange,timer_minutes, 3))
    return timer_minutes
    # time.sleep(60*(every_minutes+1-timer_minutes))
def collect_honey(count,vip=False,wait=False,start=False):
    # for i in range(count):
    if count ==10 and vip :
        collect_vip_sauna()
    timeTaken_m = collect_from_land((2780,2781),2,start=start)
    if vip:
        timeTaken_m +=collect_from_land((4025,4027),3)
        timeTaken_m +=collect_from_land((2072,2074),1)
        timeTaken_m +=collect_from_land((1629,1629),4)
    if wait:
        print('time taken: ',timeTaken_m," minutes")
        time.sleep(60*(48-timeTaken_m))
    else:
        return timeTaken_m
    



def go_to_sauna_from_land(landNumber):
    Player.check_and_activate_window()
    # player.vision.travel_to_bookmark(4)
    HUD.travel_bookmark(landNumber)
    player.play(f'land_records/{landNumber}_sauna')
    player.vision.wait_untill_travel()

def goto_triv_from_sauna(fromLand):
    go_to_sauna_from_land(fromLand)
    player.play('land_records/sauna_leave')
    player.vision.wait_untill_travel()


def travel_from_topFarms_from_sauna(fromLand,toLand):
    goto_triv_from_sauna(fromLand)
    player.play('land_records/sauna_top_farms')
    player.vision.wait_untill_travel()
    player.play('land_records/to_travel_machine')
    player.vision.click_on((1118,377))
    time.sleep(0.3)
    HUD.driver.send_keys(str(toLand))
    time.sleep(0.2)
    player.vision.press('enter')
    player.vision.wait_untill_travel()
    

def go_to_bucks_from_sauna(fromLand):
    goto_triv_from_sauna(fromLand)
    player.play('land_records/sauna_galore')
    player.vision.wait_untill_travel()
    player.vision.left_mouse_hold(800,180,7)

def buy_from_hazel(itemName:str,amount:int):
    HUD.travel_to_bucks_galore()
    time.sleep(0.5)
    HUD.driver.sendWS(buy_from_hazel_command(itemName,int(amount)))
    
def buy_from_hazel_from_sauna(fromLand,itemName,amount):
    goto_triv_from_sauna(fromLand)
    player.play('land_records/sauna_galore')
    player.vision.wait_untill_travel()
    player.vision.left_mouse_hold(912,188,2.8)
    player.vision.click_on((1017,501))
    Market.buy_from_store(itemName,amount)


def collect_vip_sauna(fromLand,):
    
    go_to_sauna_from_land(fromLand)
    player.play('land_records/sauna_vip')
    stone,found=player.vision.wait_till_object_found(vision.SAUNA_STONE)
    # time.sleep(0.4)
    player.vision.click_on(stone)


def collect_trees_from_sauna(fromLand):
    Player.check_and_activate_window()
    def tree_cut():
        Items.sort_items(['shears.png','water.png','popberyseed.png','axe.png'])
        callback_base('axe.png',4)
        return (0.5)
    goto_triv_from_sauna(fromLand)
    player.play('trees/sauna_trees',farm=True,farm_calbacks=[tree_cut])
    player.play('trees/collect_trees')

def cut_trees(i=None):
    HUD.travel_bookmark()
    HUD.driver.sendWS(cut_trees_command(),0.4)
    time.sleep(2)
    HUD.driver.sendWS(collect_wood_command())
    time.sleep(0.5)

def go_sell_items():
    # {'name':'honey','price':15},
    # {'name':'beeswax','price':25},
    itemsList = [
    {'name':'popberryFruit','price':60},
    {'name':'wood','price':59},
    ]
    HUD.travel_to_bucks_galore()
    time.sleep(0.25)
    for item in itemsList:
        #item ={'name':'popberry','price':60}
        HUD.driver.sendWS(sell_items_command(item['name'],1,item['price']))


def go_sell_items_old(fromLand,):
    # {'name':'honey','price':15},
    # {'name':'wax','price':25},
    itemsList = [
    {'name':'popberry','price':51},
    {'name':'softwood','price':58},
    ]
    go_to_bucks_from_sauna(fromLand)
    player.play('walk_left_sell')
    player.vision.click_on((645,400))
    for item in itemsList:
        #item ={'name':'popberry','price':60}
        if (Market.sell(item['name'],item['price'])):
            time.sleep(0.5)
    player.vision.press('esc')

def go_buy_items(itemName,amount,maxPrice):
    go_to_bucks_from_sauna(1629)
    player.play('walk_right_buy')
    player.vision.click_on((1131,400))
    Market.buy(itemName,amount,maxPrice)
    time.sleep(0.9)
    player.vision.press('esc')

def trade(item_blob,amount):
    client = Client('192.168.1.114', 12345)
    try:
        player.vision.click_on((515,415))
        time.sleep(0.5)
        Trade.press_trade_btn()
        time.sleep(1)
        my_username= Trade.get_self_player_name()
        msg= 'start:'+my_username
        client.send_message(msg)
        if client.receive_message() != msg:
            raise Exception("un identical message")
        Trade.trade_item(item_blob,amount)
        time.sleep(0.2)
        msg= 'add'
        client.send_message(msg)
        if client.receive_message() != msg:
            raise Exception("un identical message")
        if wait_until(lambda:(Trade.get_self_trade_value()==Trade.get_other_trade_value())):
            Trade.agree_trade()
            msg= 'end'
            client.send_message(msg)
            if client.receive_message() != msg:
                raise Exception("un identical message")
        else:
            raise Exception('trade values not equal')
    except Exception as e:
        print(f'[gobuyandtrade]: error: {e}')
    finally:
        client.close_connection()

def go_buy_items_then_trade_them(i=None):
    try:
        itemName = "hardwood"
        item_blob = 'hardwood.png'
        item_price = 350
        if HUD.get_gold() > 840+item_price:
            amount = int((HUD.get_gold()-840)/item_price)
            print('amount:',amount)
            go_buy_items(itemName,amount,item_price)
            time.sleep(0.5)
            player.play('walk_left_trade')
            trade(item_blob,amount)

    except Exception as e:
        print(f'[gobuyandtrade]: error: {e}')


def farm_account(count,accountNumber):
    if (Items.get_item_count(SEED)<120):
        buy_from_hazel(SEED_NAME,840)
        time.sleep(1)
    farm_sort_items(SEED)
    for i in range(count+1):
        onlyShear = True if i == count else False
        farm_land_range((1043,1043),shearOnly=onlyShear,accountNumber=accountNumber)
        farm_land_range((1019,1019),shearOnly=onlyShear,accountNumber=accountNumber)

def collect_mail_if_any(accountNumber):
    Market.collect_mail_box()

def setupaccs():

    def add_bookmark():
        player.vision.click_on((804,285))
        time.sleep(0.5)
        player.vision.click_on((686,327))
        time.sleep(0.5)
        player.vision.press('esc')
        time.sleep(0.5)
    
    player.vision.travel_to_terravilla()
    travel_from_topFarms_from_sauna(2781,1629)
    HUD.remove_bookmarks(removeAll=True)
    time.sleep(1)
    add_bookmark()
    travel_from_topFarms_from_sauna(1629,1043)
    add_bookmark()
    travel_from_topFarms_from_sauna(1629,1019)
    add_bookmark()


if __name__=='__main__':
    # timeTaken_m =collect_from_land((2072,2074),1)
    # HUD.travel_bookmark(1629)
    # go_to_hazel_from_sauna()
    # trade('ironite.png',5)
    farm_account(1,None)
    pass