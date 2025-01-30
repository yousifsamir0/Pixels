import time
from Tasks import farm_account,cut_trees ,collect_trees_from_sauna, buy_from_hazel_from_sauna,go_sell_items,go_buy_items,collect_mail_if_any
from account import run_bots
from utils import get_state,update_state
from driver.pixels_driver import HUD

LAND = 1629



def farm_account_wrap(accountNumber):
    farm_account(1,accountNumber)

def collect_trees_wrap(accountNumber):
    collect_trees_from_sauna(LAND)

def buy_from_hazel_wrap(accountNumber):
    buy_from_hazel_from_sauna(LAND,'popberry',840)

def sell_items_wrap(accountNumber):
    go_sell_items()

def buy_items_wrap(accountNumber):
    go_buy_items('hardwood')





def tasks(accNumber):
    energy = HUD.get_energy()
    if energy >= 475 :
        farm_account_wrap(accNumber)
    cut_trees(accNumber)
    # sell_items_wrap(accNumber)

if __name__=='__main__':
    firstTime=True
    firstTimeRange=(16,39)
    accountRange=(1,39)
    while(True):
        range = firstTimeRange if firstTime else accountRange
        firstTime = False
        t = time.time()
        run_bots(range,[tasks])
        timeTaken = (time.time()-t)/60 
        waitTime = ((6*60)- min(timeTaken,60))
        print('time taken:',timeTaken)
        print('waiting time:',waitTime)
        time.sleep(waitTime*60)




