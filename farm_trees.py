import time
from Tasks import farm_account,cut_trees ,collect_trees_from_sauna, buy_from_hazel_from_sauna,go_sell_items,go_buy_items,collect_mail_if_any
from account import run_bots
from utils import get_state,update_state
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


if __name__=='__main__':
    firstTime=True
    firstTimeRange=(8,39)
    accountRange=(1,39)
    while(True):
        range = firstTimeRange if firstTime else accountRange
        firstTime = False
        t = time.time()
        callbacks= [collect_mail_if_any]
        state= get_state()
        nextState=""
        if state=='s1':
            nextState='s2'
            callbacks.extend([farm_account_wrap,cut_trees])
        elif state=='s2':
            nextState='s3'
            callbacks.extend([cut_trees])
        elif state=='s3':
            nextState='s4'
            callbacks.extend([cut_trees])
        else:
            nextState='s1'
            callbacks.extend([cut_trees])

        
        callbacks.extend([sell_items_wrap])

        run_bots(range,callbacks)
        update_state(nextState)
        timeTaken = (time.time()-t)/60 
        waitTime = ((6*60)- min(timeTaken,60))
        print('time taken:',timeTaken)
        print('waiting time:',waitTime)
        time.sleep(waitTime*60)




