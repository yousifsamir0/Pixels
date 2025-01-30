import vision
import Player
import time
from driver.core.utils import save_cookies
from driver.pixels_driver import HUD
from Tasks import collect_mail_if_any, farm_account, collect_trees_from_sauna, buy_from_hazel_from_sauna, go_buy_items_then_trade_them,go_sell_items,go_buy_items
# import gAPI.quickstart as gmail

v=vision.Vision()


def wallet_login(account_index,scroll=False):
    ronin_wallet,found=v.wait_till_object_found(vision.RONIN_WALLET,0.9,timeout=30)
    v.click_on(ronin_wallet)

    ronin_network,found=v.wait_till_object_found(vision.RONIN_NETWORK,0.8,True,timeout=60)
    v.mouse_move(-20,45,rel=True)
    time.sleep(0.1)
    v.click_on()
    time.sleep(0.1)

    v.mouse_move(-270,145,rel=True)
    time.sleep(0.2)

    vision.scroll_to_account(account_index)
    time.sleep(0.1)

    ronin_connect,found=v.wait_till_object_found(vision.RONIN_CONNECT,0.8)
    v.click_on(ronin_connect)
    time.sleep(0.14)

    ronin_signin,found=v.wait_till_object_found(vision.RONIN_SIGNIN,0.8,timeout=10)
    v.click_on(ronin_signin)
    time.sleep(0.15)

    ronin_signin_extension,found=v.wait_till_object_found(vision.RONIN_SIGNIN_EXTENSION,0.8,timeout=50)
    v.click_on(ronin_signin_extension,0.2)
    time.sleep(0.15)
    if scroll:
        world,found=v.wait_till_object_found(vision.WORLD,0.9)
        v.click_on(world)
        time.sleep(0.3)

        server = v.scroll_untill_object_found(vision.SERVER_BAR,vision.SELF_XY,0.75,True)
        v.click_on(server)
    else:
        start_game,found=v.wait_till_object_found(vision.START_GAME,0.9)
        v.click_on(start_game)

    v.wait_till_object_found(vision.LAND_BTN,0.7,True,timeout=60)
    time.sleep(1.5)
    
def save_cookies_routine(acc_number_range):
    def save(accountNumber):
        cookie=HUD.driver.driver.get_cookie('pixels-session')
        save_cookies(cookie,accountNumber)
        time.sleep(0.5)
    for i in range(acc_number_range[0],acc_number_range[1]+1):
        wallet_login(i)
        print(f'accpunt {i} logged in')
        save(i)
        print(f'accpunt {i}  going to logout')
        HUD.cookies_logout()
        print(f'accpunt {i} logged out')
        v.screenshot()


def run_bots(acc_number_range,callbacks=[]):
    muted = [27,30]
    purchase_limit = [28,29]
    Player.check_and_activate_window()
    for i in range(acc_number_range[0],acc_number_range[1]+1):
        if i in muted or i in purchase_limit:
            continue
        HUD.cookis_login(i,137)
        # v.wait_untill_travel()
        print(f'account {i} logged in')
        for callback in callbacks:
            callback(i)
            time.sleep(1)
        print(f'account {i}  going to logout')
        HUD.cookies_logout()
        print(f'account {i} logged out')



if __name__=='__main__':
    def test(i):
        input(str(i))
    from web_driver import task
    run_bots((37,39),[task])

























# def logout():
#         logout,found=v.wait_till_object_found(vision.LOGOUT,0.6)
#         v.click_on(logout)
#         time.sleep(0.74)

# def mail_login(email):

#         email_method,found=v.wait_till_object_found(vision.EMAIL_METHOD,0.9)
#         v.click_on(email_method)
#         time.sleep(0.2)

#         email_btn,found=v.wait_till_object_found(vision.EMAIL_BTN,0.9)
#         v.click_on(email_btn)
#         time.sleep(0.2)

#         v.write(email+"@gmail.com",interval=0.11)
#         time.sleep(0.3)


#         submit,found=v.wait_till_object_found(vision.SUBMIT_BTN,0.9)
#         timestamp= time.time()
#         v.click_on(submit)
#         time.sleep(0.3)

#         otp=gmail.getOTP(email,timestamp)

#         v.write(otp,interval=0.261)
#         time.sleep(0.3)

#         submit,found=v.wait_till_object_found(vision.SUBMIT_BTN,0.9)
#         v.click_on(submit)
#         time.sleep(0.3)

#         world,found=v.wait_till_object_found(vision.WORLD,0.9)
#         v.click_on(world)
#         time.sleep(0.3)

#         server = v.scroll_untill_object_found(vision.SERVER_BAR,vision.SELF_XY,0.75,True)
#         v.click_on(server)
#         v.wait_till_object_found(vision.LAND_BTN,0.7,True,timeout=60)
#         time.sleep(1.5)





# def run_bots_accounts(acc_number_range):

#     for count in range(16):
#         timeTaken_m = 0
#         mail_login('yousifysm')
#         timeTaken_m = Tasks.collect_honey(count, vip=True,wait=False,start=True)
#         logout()
#         t = time.time()
#         for i in range(acc_number_range[0],acc_number_range[1]+1):
#             wallet_login(i)
#             timeTaken_m+=Tasks.collect_honey(0,False,False)
#             logout()
#         print('free acc time: ',((time.time()-t)/60))
#         print('all time taken: ', timeTaken_m)
#         time.sleep(60*(48-timeTaken_m))

# def run_bots_accounts_v2(acc_number_range,setup=False):
#     timeTaken_m = 0
#     t = time.time()
#     for i in range(acc_number_range[0],acc_number_range[1]+1):
#         wallet_login(i)
#         if setup:
#             Tasks.collect_from_land((2781,2781),2,default_postfix='_setup') #remove after firsttime
#         v.click_all_objects(vision.HONEY_TEMPELATE,0.6,vision.HONEY_INNER_TEMPELATE)
#         logout()
#     timeTaken_m = ((time.time()-t)/60)
#     print('time taken: ',timeTaken_m)
#     time.sleep(60*(46-timeTaken_m))